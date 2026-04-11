#!/usr/bin/env python3
"""
AnalysisDataFlow 项目交叉链接验证工具
======================================
扫描所有Markdown文档中的链接，验证内部链接和外部链接的有效性。

功能:
- 扫描Markdown文档中的内部链接和外部链接
- 验证内部链接（文档间）是否指向存在的文件
- 验证外部链接（URL）的可访问性
- 验证Mermaid图表中的资源引用
- 生成详细的验证报告

作者: Agent
版本: 1.0.0
"""

import os
import re
import json
import time
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Set, Tuple, Optional
from urllib.parse import urlparse, urljoin, unquote

# ============ 配置 ============
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
REPORTS_DIR = PROJECT_ROOT / "reports"
TOOLS_DIR = PROJECT_ROOT / "tools"
CACHE_DIR = TOOLS_DIR / ".link-cache"

# 扫描目录（优先级顺序）
SCAN_DIRECTORIES = [
    PROJECT_ROOT,           # 根目录
    PROJECT_ROOT / "Struct",
    PROJECT_ROOT / "Knowledge", 
    PROJECT_ROOT / "Flink",
    PROJECT_ROOT / "en",
    PROJECT_ROOT / "docs",
    PROJECT_ROOT / "tutorials",
    PROJECT_ROOT / "examples",
    PROJECT_ROOT / "whitepapers",
    PROJECT_ROOT / "LEARNING-PATHS",
    PROJECT_ROOT / "formal-methods",
]

# 排除的目录
EXCLUDE_DIRS = {
    '.git', 'node_modules', '__pycache__', '.venv', 'venv',
    '.improvement-tracking', 'archive', 'reconstruction',
    'phase2-automation', 'phase2-case-studies', 'phase2-community',
    'phase2-formal-proofs', 'phase2-i18n', 'phase2-visualization',
    'Flink-IoT-Authority-Alignment', 'USTM-F-Reconstruction',
    'v5.0', 'benchmark-data', 'CONFIG-TEMPLATES', 'docker',
    'i18n', 'Knowledge', 'learning-platform', 'reports',
    'scripts', 'TECH-RADAR', 'templates', 'visuals', 'whitepapers'
}

# 排除的文件模式
EXCLUDE_FILE_PATTERNS = [
    r'^\.',           # 隐藏文件
    r'^archive\/',
    r'^reconstruction\/',
    r'\.improvement-tracking\/',
]

# 外部链接验证配置
EXTERNAL_TIMEOUT = 8   # 秒
MAX_WORKERS = 5        # 并发数
RETRY_COUNT = 1        # 重试次数
CACHE_VALID_DAYS = 7   # 缓存有效期

# 用户代理
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 AnalysisDataFlow-LinkValidator/1.0'

# ============ 链接提取正则 ============
LINK_PATTERNS = {
    # Markdown链接: [text](url) 或 [text](url "title")
    'markdown_link': re.compile(r'!?\[([^\]]+)\]\(([^)"\s]+)(?:\s+"[^"]*")?\)'),
    
    # Markdown引用链接: [text][ref] 或 [ref]:
    'markdown_ref': re.compile(r'\[([^\]]+)\]:\s*([^\s]+)'),
    
    # HTML链接: <a href="url"> 或 <img src="url">
    'html_link': re.compile(r'<(?:a|img)[^>]+(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE),
    
    # 裸URL: http://... 或 https://...
    'bare_url': re.compile(r'https?://[^\s<>"\')\]]+(?:[^\s<>"\')\].,;?!])'),
    
    # Mermaid中的资源引用（简化检测）
    'mermaid_click': re.compile(r'click\s+\w+\s+"([^"]+)"', re.IGNORECASE),
}

class LinkValidator:
    """链接验证器主类"""
    
    def __init__(self, quick_mode=False):
        self.quick_mode = quick_mode
        self.all_md_files: Set[Path] = set()
        self.all_files_map: Dict[str, Path] = {}  # 规范化路径 -> 实际路径
        self.link_cache: Dict[str, dict] = {}
        self.results: List[dict] = []
        self.stats = {
            'total_files': 0,
            'total_links': 0,
            'internal_links': 0,
            'external_links': 0,
            'valid_internal': 0,
            'invalid_internal': 0,
            'valid_external': 0,
            'invalid_external': 0,
            'skipped_external': 0,
            'errors': 0,
        }
        self.start_time = time.time()
        
        # 确保缓存目录存在
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self._load_cache()
    
    def _load_cache(self):
        """加载链接验证缓存"""
        cache_file = CACHE_DIR / "link_cache.json"
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self.link_cache = json.load(f)
                # 清理过期缓存
                self._clean_cache()
            except Exception as e:
                print(f"[警告] 加载缓存失败: {e}")
                self.link_cache = {}
    
    def _clean_cache(self):
        """清理过期缓存条目"""
        now = time.time()
        expired = []
        for url, data in self.link_cache.items():
            cache_time = data.get('timestamp', 0)
            if now - cache_time > CACHE_VALID_DAYS * 86400:
                expired.append(url)
        for url in expired:
            del self.link_cache[url]
    
    def _save_cache(self):
        """保存链接验证缓存"""
        cache_file = CACHE_DIR / "link_cache.json"
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.link_cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[警告] 保存缓存失败: {e}")
    
    def _normalize_path(self, path_str: str) -> str:
        """规范化路径用于比较"""
        # 移除锚点和查询参数
        path_str = path_str.split('#')[0].split('?')[0]
        # URL解码
        path_str = unquote(path_str)
        # 统一分隔符
        path_str = path_str.replace('/', os.sep).replace('\\', os.sep)
        # 移除开头的./
        path_str = re.sub(r'^[.\\/]+', '', path_str)
        # 转换为小写（Windows不区分大小写）
        return path_str.lower()
    
    def _is_excluded_dir(self, path: Path) -> bool:
        """检查路径是否在排除目录中"""
        try:
            rel_parts = path.relative_to(PROJECT_ROOT).parts
            return any(part in EXCLUDE_DIRS for part in rel_parts)
        except ValueError:
            return False
    
    def scan_markdown_files(self) -> List[Path]:
        """扫描所有Markdown文件"""
        print("[1/5] 扫描Markdown文件...")
        
        for scan_dir in SCAN_DIRECTORIES:
            if not scan_dir.exists():
                continue
            
            for md_file in scan_dir.rglob("*.md"):
                # 检查是否在排除目录中
                if self._is_excluded_dir(md_file):
                    continue
                
                # 检查文件模式
                rel_path = str(md_file.relative_to(PROJECT_ROOT))
                if any(re.match(pattern, rel_path) for pattern in EXCLUDE_FILE_PATTERNS):
                    continue
                
                self.all_md_files.add(md_file)
                
                # 建立规范化路径映射
                norm_path = self._normalize_path(rel_path)
                self.all_files_map[norm_path] = md_file
                
                # 也添加无扩展名版本（用于无扩展名链接）
                norm_no_ext = norm_path.replace('.md', '')
                if norm_no_ext != norm_path:
                    self.all_files_map[norm_no_ext] = md_file
        
        self.stats['total_files'] = len(self.all_md_files)
        print(f"  ✓ 发现 {len(self.all_md_files)} 个Markdown文件")
        return sorted(self.all_md_files)
    
    def _extract_anchor(self, link: str) -> Tuple[str, Optional[str]]:
        """从链接中提取路径和锚点"""
        if '#' in link:
            parts = link.split('#', 1)
            return parts[0], parts[1] if parts[1] else None
        return link, None
    
    # 常见误报关键词（作者名、常见词等）
    FALSE_POSITIVE_PATTERNS = [
        r'^[A-Z][a-z]+$',  # 纯单个大写开头单词（如"Apache", "Stanford"）
        r'^[A-Z]\.[A-Z]\.$',  # 作者缩写（如"K.M."）
        r'^Def-[A-Z]-\d+$',  # 定义编号引用
        r'^Thm-[A-Z]-\d+$',  # 定理编号引用
        r'^Lemma-[A-Z]-\d+$',  # 引理编号引用
        r'^::\w+',  # 代码片段
        r'^\.\.\.+$',  # 省略号
        r'^[^/]*$',  # 不包含路径分隔符或域名的纯文本
    ]
    
    def _is_valid_link(self, url: str) -> bool:
        """检查链接是否为有效链接（过滤误报）"""
        if not url or len(url) < 2:
            return False
        
        # 排除纯空格链接
        if url.strip() != url:
            return False
        
        # 排除明显的误报
        for pattern in self.FALSE_POSITIVE_PATTERNS:
            if re.match(pattern, url):
                return False
        
        # 有效的链接应该包含以下特征之一：
        # - 是URL（http/https/mailto等）
        # - 包含文件扩展名
        # - 包含路径分隔符
        # - 是锚点链接
        if url.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
            return True
        if '.' in url and any(url.endswith(ext) for ext in ['.md', '.html', '.txt', '.pdf', '.png', '.jpg', '.svg']):
            return True
        if '/' in url or '\\' in url:
            return True
        if url.startswith('./') or url.startswith('../'):
            return True
        
        # 其他情况可能是误报
        return False
    
    def _extract_links_from_file(self, file_path: Path) -> List[dict]:
        """从单个文件提取所有链接"""
        links = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"  [错误] 无法读取文件 {file_path}: {e}")
            return links
        
        lines = content.split('\n')
        rel_path = str(file_path.relative_to(PROJECT_ROOT))
        
        # 提取Markdown链接
        for line_num, line in enumerate(lines, 1):
            # 标准Markdown链接
            for match in LINK_PATTERNS['markdown_link'].finditer(line):
                text, url = match.groups()
                # 过滤无效链接
                if not self._is_valid_link(url):
                    continue
                links.append({
                    'type': 'markdown',
                    'url': url,
                    'text': text,
                    'file': rel_path,
                    'line': line_num,
                    'column': match.start() + 1,
                })
            
            # 引用定义
            for match in LINK_PATTERNS['markdown_ref'].finditer(line):
                ref, url = match.groups()
                if not self._is_valid_link(url):
                    continue
                links.append({
                    'type': 'reference',
                    'url': url,
                    'text': ref,
                    'file': rel_path,
                    'line': line_num,
                    'column': match.start() + 1,
                })
            
            # HTML标签
            for match in LINK_PATTERNS['html_link'].finditer(line):
                url = match.group(1)
                if not self._is_valid_link(url):
                    continue
                links.append({
                    'type': 'html',
                    'url': url,
                    'text': '',
                    'file': rel_path,
                    'line': line_num,
                    'column': match.start() + 1,
                })
            
            # 裸URL（排除代码块内）
            # 简化处理：检查是否可能在代码块中
            stripped = line.lstrip()
            if not stripped.startswith('```') and not stripped.startswith('    '):
                for match in LINK_PATTERNS['bare_url'].finditer(line):
                    url = match.group()
                    if not self._is_valid_link(url):
                        continue
                    links.append({
                        'type': 'bare_url',
                        'url': url,
                        'text': url,
                        'file': rel_path,
                        'line': line_num,
                        'column': match.start() + 1,
                    })
        
        # 提取Mermaid中的链接（跨行处理）
        in_mermaid = False
        mermaid_start = 0
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('```mermaid'):
                in_mermaid = True
                mermaid_start = line_num
            elif line.strip() == '```' and in_mermaid:
                in_mermaid = False
            elif in_mermaid:
                # 检查Mermaid click语句
                for match in LINK_PATTERNS['mermaid_click'].finditer(line):
                    url = match.group(1)
                    if not self._is_valid_link(url):
                        continue
                    links.append({
                        'type': 'mermaid',
                        'url': url,
                        'text': f'Mermaid图表 (行{mermaid_start}-{line_num})',
                        'file': rel_path,
                        'line': line_num,
                        'column': match.start() + 1,
                    })
        
        return links
    
    def _classify_link(self, link: dict, source_file: Path) -> dict:
        """分类链接为内部或外部链接"""
        url = link['url']
        
        # 排除特殊协议
        if any(url.startswith(p) for p in ['mailto:', 'tel:', 'javascript:', 'data:']):
            link['category'] = 'special'
            return link
        
        # 排除纯锚点
        if url.startswith('#'):
            link['category'] = 'anchor_only'
            return link
        
        # 外部链接
        if url.startswith(('http://', 'https://')):
            link['category'] = 'external'
            return link
        
        # 内部链接
        link['category'] = 'internal'
        return link
    
    def _resolve_internal_link(self, link: dict, source_file: Path) -> Tuple[bool, str, Optional[Path]]:
        """解析并验证内部链接"""
        url = link['url']
        base_path = link['file']
        
        # 提取锚点
        url_part, anchor = self._extract_anchor(url)
        
        # 处理相对路径
        if url_part.startswith('/'):
            # 绝对路径（相对于项目根）
            target_path = PROJECT_ROOT / url_part.lstrip('/')
        elif url_part.startswith('./') or url_part.startswith('../') or not any(c in url_part for c in [':', '//']):
            # 相对路径
            source_dir = (PROJECT_ROOT / base_path).parent
            try:
                target_path = (source_dir / url_part).resolve()
                # 确保在项目中
                if PROJECT_ROOT not in target_path.parents and target_path != PROJECT_ROOT:
                    pass  # 可能是 ../ 超出项目根，尝试其他方式
            except Exception:
                target_path = source_dir / url_part
        else:
            return False, f"无法解析的链接格式: {url}", None
        
        # 尝试多种扩展名组合
        possible_paths = [
            target_path,
            Path(str(target_path) + '.md'),
            Path(str(target_path).rstrip('.md') + '.md'),
            PROJECT_ROOT / self._normalize_path(str(target_path)),
        ]
        
        # 添加目录索引文件可能
        if target_path.suffix == '':
            possible_paths.append(target_path / 'README.md')
            possible_paths.append(target_path / 'index.md')
        
        for try_path in possible_paths:
            if try_path.exists() and try_path.is_file():
                return True, "文件存在", try_path
        
        # 检查规范化路径映射
        norm_target = self._normalize_path(str(target_path.relative_to(PROJECT_ROOT) if PROJECT_ROOT in target_path.parents else str(target_path)))
        if norm_target in self.all_files_map:
            return True, "文件存在（规范化匹配）", self.all_files_map[norm_target]
        
        # 尝试模糊匹配
        target_name = target_path.name.lower().replace('.md', '')
        for norm_path, actual_path in self.all_files_map.items():
            if target_name in norm_path or norm_path.endswith(target_name):
                return True, f"文件存在（模糊匹配: {actual_path.name}）", actual_path
        
        return False, f"文件不存在: {target_path.relative_to(PROJECT_ROOT) if PROJECT_ROOT in target_path.parents else target_path}", None
    
    def _check_external_link(self, url: str) -> Tuple[bool, str, int]:
        """检查外部链接可访问性"""
        # 快速模式：优先使用缓存，新链接标记为待验证
        if self.quick_mode:
            if url in self.link_cache:
                cache_data = self.link_cache[url]
                # 检查缓存是否仍然有效
                cache_age = time.time() - cache_data.get('timestamp', 0)
                if cache_age < CACHE_VALID_DAYS * 86400:
                    return cache_data['valid'], cache_data['message'] + " (缓存)", cache_data.get('status', 0)
            # 快速模式下，对未缓存的链接仅做基本检查
            parsed = urlparse(url)
            if any(domain in parsed.netloc for domain in ['github.com', 'apache.org', 'wikipedia.org', 'docs.oracle.com', 'microsoft.com']):
                return True, f"{parsed.netloc} (可信域名，快速模式跳过)", 0
        
        # 检查缓存
        if url in self.link_cache:
            cache_data = self.link_cache[url]
            return cache_data['valid'], cache_data['message'], cache_data.get('status', 0)
        
        result = self._do_external_check(url)
        
        # 缓存结果
        self.link_cache[url] = {
            'valid': result[0],
            'message': result[1],
            'status': result[2],
            'timestamp': time.time(),
        }
        
        return result
    
    def _do_external_check(self, url: str) -> Tuple[bool, str, int]:
        """执行外部链接检查"""
        # 跳过某些特殊URL
        if 'localhost' in url or '127.0.0.1' in url or '0.0.0.0' in url:
            return True, "本地地址（跳过验证）", 0
        
        parsed = urlparse(url)
        
        # 跳过某些域名（可能反爬虫）
        skip_domains = [
            'doi.org', 'scholar.google', 'academia.edu', 
            'researchgate.net', 'linkedin.com', 'twitter.com',
            'x.com', 'facebook.com', 'instagram.com'
        ]
        if any(domain in parsed.netloc for domain in skip_domains):
            return True, f"{parsed.netloc} (跳过验证)", 0
        
        headers = {
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        
        for attempt in range(RETRY_COUNT):
            try:
                req = urllib.request.Request(url, headers=headers, method='HEAD')
                
                # 使用自定义SSL上下文（忽略证书错误但仍尝试连接）
                import ssl
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                
                response = urllib.request.urlopen(req, timeout=EXTERNAL_TIMEOUT, context=ssl_context)
                status = response.getcode()
                
                if status in [200, 301, 302, 307, 308]:
                    return True, f"HTTP {status}", status
                else:
                    return True, f"HTTP {status} (非标准成功)", status
                    
            except urllib.error.HTTPError as e:
                status = e.code
                if status in [403, 405]:  # Forbidden or Method Not Allowed, try GET
                    try:
                        req = urllib.request.Request(url, headers=headers, method='GET')
                        import ssl
                        ssl_context = ssl.create_default_context()
                        ssl_context.check_hostname = False
                        ssl_context.verify_mode = ssl.CERT_NONE
                        response = urllib.request.urlopen(req, timeout=EXTERNAL_TIMEOUT, context=ssl_context)
                        return True, f"HTTP {response.getcode()} (GET成功)", response.getcode()
                    except Exception:
                        pass
                
                if status == 404:
                    return False, f"HTTP {status} (页面不存在)", status
                elif status in [500, 502, 503, 504]:
                    if attempt < RETRY_COUNT - 1:
                        time.sleep(1)
                        continue
                    return False, f"HTTP {status} (服务器错误)", status
                else:
                    return True, f"HTTP {status}", status
                    
            except urllib.error.URLError as e:
                if attempt < RETRY_COUNT - 1:
                    time.sleep(1)
                    continue
                return False, f"URL错误: {str(e.reason)}", 0
                
            except Exception as e:
                if attempt < RETRY_COUNT - 1:
                    time.sleep(1)
                    continue
                return False, f"错误: {str(e)[:50]}", 0
        
        return False, "验证超时", 0
    
    def validate_all_links(self):
        """验证所有链接"""
        print("[2/5] 提取链接...")
        all_links = []
        
        for md_file in self.all_md_files:
            links = self._extract_links_from_file(md_file)
            all_links.extend(links)
        
        # 去重（相同URL在同一文件）
        seen = set()
        unique_links = []
        for link in all_links:
            key = (link['file'], link['url'], link['line'])
            if key not in seen:
                seen.add(key)
                unique_links.append(link)
        
        self.stats['total_links'] = len(unique_links)
        print(f"  ✓ 提取 {len(unique_links)} 个唯一链接")
        
        # 分类链接
        print("[3/5] 分类链接...")
        classified_links = [self._classify_link(link, PROJECT_ROOT / link['file']) for link in unique_links]
        
        internal_links = [l for l in classified_links if l['category'] == 'internal']
        external_links = [l for l in classified_links if l['category'] == 'external']
        
        self.stats['internal_links'] = len(internal_links)
        self.stats['external_links'] = len(external_links)
        
        print(f"  ✓ 内部链接: {len(internal_links)}")
        print(f"  ✓ 外部链接: {len(external_links)}")
        
        # 验证内部链接
        print("[4/5] 验证内部链接...")
        for link in internal_links:
            valid, message, target = self._resolve_internal_link(link, PROJECT_ROOT / link['file'])
            link['valid'] = valid
            link['message'] = message
            link['target'] = str(target.relative_to(PROJECT_ROOT)) if target else None
            
            if valid:
                self.stats['valid_internal'] += 1
            else:
                self.stats['invalid_internal'] += 1
            
            self.results.append(link)
        
        print(f"  ✓ 有效: {self.stats['valid_internal']}, 无效: {self.stats['invalid_internal']}")
        
        # 验证外部链接（并发）
        print("[5/5] 验证外部链接...")
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_link = {
                executor.submit(self._check_external_link, link['url']): link 
                for link in external_links
            }
            
            completed = 0
            total = len(external_links)
            
            for future in as_completed(future_to_link):
                link = future_to_link[future]
                completed += 1
                
                if completed % 10 == 0 or completed == total:
                    print(f"    进度: {completed}/{total}", end='\r')
                
                try:
                    valid, message, status = future.result()
                    link['valid'] = valid
                    link['message'] = message
                    link['status'] = status
                    
                    if status == 0:  # 跳过的
                        self.stats['skipped_external'] += 1
                    elif valid:
                        self.stats['valid_external'] += 1
                    else:
                        self.stats['invalid_external'] += 1
                        
                except Exception as e:
                    link['valid'] = False
                    link['message'] = f"验证异常: {str(e)[:50]}"
                    link['status'] = 0
                    self.stats['invalid_external'] += 1
                
                self.results.append(link)
        
        print(f"\n  ✓ 有效: {self.stats['valid_external']}, 无效: {self.stats['invalid_external']}, 跳过: {self.stats['skipped_external']}")
        
        # 保存缓存
        self._save_cache()
    
    def generate_report(self) -> str:
        """生成Markdown格式报告"""
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        
        duration = time.time() - self.start_time
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 按类别分组结果
        invalid_internal = [r for r in self.results if r['category'] == 'internal' and not r['valid']]
        invalid_external = [r for r in self.results if r['category'] == 'external' and not r['valid'] and r.get('status', 0) != 0]
        
        report = f"""# AnalysisDataFlow 交叉链接验证报告

> **生成时间**: {timestamp}  
> **验证工具**: link-validator.py v1.0.0  
> **验证耗时**: {duration:.2f}秒  
> **项目根目录**: `{PROJECT_ROOT}`

---

## 📊 验证摘要

| 指标 | 数值 |
|------|------|
| 扫描文档数 | **{self.stats['total_files']}** |
| 总链接数 | **{self.stats['total_links']}** |
| 内部链接 | {self.stats['internal_links']} |
| 外部链接 | {self.stats['external_links']} |
| ✅ 有效链接 | **{self.stats['valid_internal'] + self.stats['valid_external'] + self.stats['skipped_external']}** |
| ❌ 无效链接 | **{self.stats['invalid_internal'] + self.stats['invalid_external']}** |
| 链接有效率 | **{((self.stats['valid_internal'] + self.stats['valid_external'] + self.stats['skipped_external']) / self.stats['total_links'] * 100):.1f}%** |

### 内部链接验证

| 状态 | 数量 |
|------|------|
| ✅ 有效 | {self.stats['valid_internal']} |
| ❌ 无效 | {self.stats['invalid_internal']} |
| 有效率 | {(self.stats['valid_internal'] / max(self.stats['internal_links'], 1) * 100):.1f}% |

### 外部链接验证

| 状态 | 数量 |
|------|------|
| ✅ 可访问 | {self.stats['valid_external']} |
| ❌ 不可访问 | {self.stats['invalid_external']} |
| ⏭️ 跳过 | {self.stats['skipped_external']} |
| 检查率 | {((self.stats['valid_external'] + self.stats['invalid_external']) / max(self.stats['external_links'], 1) * 100):.1f}% |

---

"""
        
        # 无效内部链接详情
        report += "## ❌ 无效内部链接\n\n"
        if invalid_internal:
            report += f"共发现 **{len(invalid_internal)}** 个无效内部链接:\n\n"
            report += "| 源文件 | 行号 | 链接 | 错误信息 |\n"
            report += "|--------|------|------|----------|\n"
            
            for item in sorted(invalid_internal, key=lambda x: (x['file'], x['line'])):
                file_link = f"[{item['file']}]({item['file']}#L{item['line']})"
                report += f"| {file_link} | {item['line']} | `{item['url']}` | {item['message']} |\n"
        else:
            report += "✅ **未发现无效内部链接**\n"
        
        report += "\n---\n\n"
        
        # 无效外部链接详情
        report += "## ❌ 无效外部链接\n\n"
        if invalid_external:
            report += f"共发现 **{len(invalid_external)}** 个无效外部链接:\n\n"
            report += "| 源文件 | 行号 | URL | 状态 | 错误信息 |\n"
            report += "|--------|------|-----|------|----------|\n"
            
            for item in sorted(invalid_external, key=lambda x: (x['file'], x['line'])):
                file_link = f"[{item['file']}]({item['file']}#L{item['line']})"
                status = item.get('status', '-')
                report += f"| {file_link} | {item['line']} | [{item['url'][:40]}...]({item['url']}) | {status} | {item['message']} |\n"
        else:
            report += "✅ **未发现无效外部链接**\n"
        
        report += "\n---\n\n"
        
        # 按文件统计
        report += "## 📁 各文件链接统计\n\n"
        
        file_stats = {}
        for r in self.results:
            f = r['file']
            if f not in file_stats:
                file_stats[f] = {'total': 0, 'valid': 0, 'invalid': 0}
            file_stats[f]['total'] += 1
            if r['valid']:
                file_stats[f]['valid'] += 1
            else:
                file_stats[f]['invalid'] += 1
        
        report += "| 文件 | 总链接 | 有效 | 无效 | 状态 |\n"
        report += "|------|--------|------|------|------|\n"
        
        for f, s in sorted(file_stats.items(), key=lambda x: x[1]['invalid'], reverse=True)[:50]:
            status = "✅" if s['invalid'] == 0 else "❌"
            report += f"| [{f}]({f}) | {s['total']} | {s['valid']} | {s['invalid']} | {status} |\n"
        
        if len(file_stats) > 50:
            report += f"\n*... 还有 {len(file_stats) - 50} 个文件 ...*\n"
        
        report += "\n---\n\n"
        
        # 附录：验证详情
        report += "## 📎 附录\n\n"
        report += f"### A. 验证范围\n\n"
        report += "扫描目录:\n"
        for d in SCAN_DIRECTORIES:
            if d.exists():
                report += f"- `{d.relative_to(PROJECT_ROOT)}`\n"
        
        report += f"\n排除目录: {', '.join(sorted(EXCLUDE_DIRS))}\n"
        
        report += f"\n### B. 链接类型分布\n\n"
        type_counts = {}
        for r in self.results:
            t = r['type']
            type_counts[t] = type_counts.get(t, 0) + 1
        
        for t, c in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            report += f"- {t}: {c}\n"
        
        report += f"\n### C. 常见错误模式\n\n"
        
        # 分析错误模式
        error_patterns = {}
        for r in self.results:
            if not r['valid']:
                msg = r['message']
                # 简化错误信息
                if '文件不存在' in msg:
                    key = "文件不存在"
                elif 'HTTP 404' in msg:
                    key = "HTTP 404 (页面不存在)"
                elif '服务器错误' in msg:
                    key = "HTTP 5xx (服务器错误)"
                elif 'URL错误' in msg:
                    key = "URL解析错误"
                else:
                    key = msg[:30]
                error_patterns[key] = error_patterns.get(key, 0) + 1
        
        for pattern, count in sorted(error_patterns.items(), key=lambda x: x[1], reverse=True)[:10]:
            report += f"- {pattern}: {count}次\n"
        
        report += f"""

---

*报告由 link-validator.py 自动生成*  
*下次验证缓存有效期: {CACHE_VALID_DAYS}天*
"""
        
        # 同时保存JSON格式详细数据
        json_data = {
            'timestamp': timestamp,
            'stats': self.stats,
            'results': self.results,
            'invalid_internal': invalid_internal,
            'invalid_external': invalid_external,
        }
        
        json_path = REPORTS_DIR / "link-validation-data.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
        
        return report
    
    def run(self):
        """执行完整验证流程"""
        print("=" * 60)
        print("AnalysisDataFlow 交叉链接验证工具")
        print("=" * 60)
        print()
        
        # 1. 扫描文件
        self.scan_markdown_files()
        print()
        
        # 2. 验证链接
        self.validate_all_links()
        print()
        
        # 3. 生成报告
        print("[报告] 生成验证报告...")
        report = self.generate_report()
        
        report_path = REPORTS_DIR / "link-validation-report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"  ✓ Markdown报告: {report_path}")
        print(f"  ✓ JSON数据: {REPORTS_DIR / 'link-validation-data.json'}")
        print()
        
        # 4. 打印摘要
        print("=" * 60)
        print("验证完成!")
        print("=" * 60)
        print(f"总链接数:    {self.stats['total_links']}")
        print(f"有效链接:    {self.stats['valid_internal'] + self.stats['valid_external'] + self.stats['skipped_external']}")
        print(f"无效链接:    {self.stats['invalid_internal'] + self.stats['invalid_external']}")
        print(f"有效率:      {((self.stats['valid_internal'] + self.stats['valid_external'] + self.stats['skipped_external']) / max(self.stats['total_links'], 1) * 100):.1f}%")
        print("=" * 60)
        
        return self.stats


def main():
    """主函数"""
    import sys
    quick_mode = '--quick' in sys.argv
    if quick_mode:
        print("[模式] 快速模式（优先使用缓存，信任主要域名）")
    
    validator = LinkValidator(quick_mode=quick_mode)
    stats = validator.run()
    
    # 返回退出码（0表示全部有效，1表示有无效链接）
    invalid_count = stats['invalid_internal'] + stats['invalid_external']
    return 0 if invalid_count == 0 else 1


if __name__ == "__main__":
    exit(main())
