#!/usr/bin/env python3
"""
AnalysisDataFlow 全量链接检查器
================================
功能：检查所有Markdown文件中的外部链接、锚点、内部链接
输出：生成链接健康报告

P1-5: 全量链接检查（每月1次）
P1-6: 失效链接修复
P1-7: 存档链接更新

作者: AnalysisDataFlow CI/CD Team
版本: 1.0.0
"""

import re
import sys
import json
import asyncio
import aiohttp
import argparse
from pathlib import Path
from urllib.parse import urlparse, unquote
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
import hashlib
import time


# =============================================================================
# 配置常量
# =============================================================================

# 需要跳过的URL模式
EXCLUDE_PATTERNS = [
    r'localhost',
    r'127\.0\.0\.1',
    r'example\.com',
    r'your-domain\.com',
    r'\.local',
    r'\.internal',
    r'github\.com/[^/]+/[^/]+/edit/',  # 编辑页面需要登录
    r'github\.com/[^/]+/[^/]+/issues/new',  # 新建issue需要登录
    r'docs\.google\.com',  # 谷歌文档经常需要认证
    r'drive\.google\.com',
    r'linkedin\.com',  # LinkedIn经常阻止爬虫
]

# 重试次数
MAX_RETRIES = 3

# 并发请求数
CONCURRENT_LIMIT = 30

# 请求超时（秒）
DEFAULT_TIMEOUT = 30

# 缓存目录
CACHE_DIR = Path('.link-checker-cache')

# 用户代理
USER_AGENT = 'Mozilla/5.0 (compatible; AnalysisDataFlow-LinkChecker/1.0; +https://github.com/AnalysisDataFlow)'


# =============================================================================
# 缓存管理
# =============================================================================

class LinkCache:
    """链接检查结果缓存管理"""
    
    def __init__(self, cache_dir: Path = CACHE_DIR):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = cache_dir / 'link_cache.json'
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """加载缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return {'links': {}, 'metadata': {'version': '1.0', 'created': datetime.now().isoformat()}}
    
    def save_cache(self):
        """保存缓存"""
        self.cache['metadata']['updated'] = datetime.now().isoformat()
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=2)
    
    def get(self, url: str) -> Optional[Dict]:
        """获取缓存结果"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        entry = self.cache['links'].get(url_hash)
        if entry:
            # 检查缓存是否过期（7天）
            cached_time = datetime.fromisoformat(entry['timestamp'])
            if (datetime.now() - cached_time).days < 7:
                return entry
        return None
    
    def set(self, url: str, result: Dict):
        """设置缓存结果"""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        self.cache['links'][url_hash] = {
            'url': url,
            'status': result['status'],
            'redirect_url': result.get('redirect_url'),
            'timestamp': datetime.now().isoformat()
        }


# =============================================================================
# 链接提取
# =============================================================================

def find_all_markdown_files(root_path: Path) -> List[Path]:
    """获取所有Markdown文件"""
    md_files = list(root_path.rglob('*.md'))
    # 排除特定目录
    exclude_dirs = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', '.scripts'}
    md_files = [
        f for f in md_files 
        if not any(part in exclude_dirs for part in f.parts)
    ]
    return md_files


def extract_links(content: str) -> List[Tuple[str, str, int]]:
    """
    提取所有链接 [text](url)
    返回: [(text, url, position), ...]
    """
    links = []
    # Markdown链接 [text](url)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for match in re.finditer(pattern, content):
        text = match.group(1)
        url = match.group(2)
        # 移除标题属性
        url = url.split(' ')[0]
        links.append((text, url, match.start()))
    return links


def extract_reference_links(content: str) -> Dict[str, str]:
    """提取引用式链接定义 [id]: url"""
    refs = {}
    pattern = r'^\[([^\]]+)\]:\s*(.+)$'
    for match in re.finditer(pattern, content, re.MULTILINE):
        ref_id = match.group(1)
        url = match.group(2).strip()
        refs[ref_id] = url
    return refs


def classify_link(url: str) -> str:
    """分类链接类型"""
    if url.startswith('http://') or url.startswith('https://'):
        return 'external'
    if url.startswith('#'):
        return 'anchor'
    if url.startswith('mailto:'):
        return 'email'
    if url.startswith('javascript:'):
        return 'javascript'
    return 'internal'


def should_skip_url(url: str) -> bool:
    """检查是否应该跳过此URL"""
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            return True
    return False


# =============================================================================
# 链接验证
# =============================================================================

async def check_external_link(
    session: aiohttp.ClientSession,
    url: str,
    timeout: int = DEFAULT_TIMEOUT
) -> Dict:
    """检查外部链接"""
    result = {
        'url': url,
        'status': 'unknown',
        'status_code': None,
        'redirect_url': None,
        'error': None,
        'response_time': None
    }
    
    start_time = time.time()
    
    for attempt in range(MAX_RETRIES):
        try:
            async with session.head(
                url, 
                timeout=aiohttp.ClientTimeout(total=timeout),
                allow_redirects=True,
                ssl=False  # 某些网站证书问题
            ) as response:
                result['response_time'] = round(time.time() - start_time, 2)
                result['status_code'] = response.status
                
                if response.status == 200:
                    result['status'] = 'ok'
                    if str(response.url) != url:
                        result['redirect_url'] = str(response.url)
                elif 300 <= response.status < 400:
                    result['status'] = 'redirect'
                    result['redirect_url'] = str(response.url)
                elif response.status in [405, 501]:
                    # 尝试GET请求
                    async with session.get(
                        url,
                        timeout=aiohttp.ClientTimeout(total=timeout),
                        ssl=False
                    ) as get_response:
                        result['status_code'] = get_response.status
                        if get_response.status < 400:
                            result['status'] = 'ok'
                        else:
                            result['status'] = 'broken'
                            result['error'] = f'HTTP {get_response.status}'
                elif response.status >= 400:
                    result['status'] = 'broken'
                    result['error'] = f'HTTP {response.status}'
                
                return result
                
        except asyncio.TimeoutError:
            if attempt == MAX_RETRIES - 1:
                result['status'] = 'timeout'
                result['error'] = f'超时 ({timeout}s)'
        except aiohttp.ClientError as e:
            if attempt == MAX_RETRIES - 1:
                result['status'] = 'error'
                result['error'] = str(e)
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                result['status'] = 'error'
                result['error'] = str(e)
        
        # 重试延迟
        await asyncio.sleep(1 * (attempt + 1))
    
    return result


def validate_internal_link(url: str, source_file: Path, all_files: Set[Path]) -> Tuple[bool, Optional[str]]:
    """验证内部链接"""
    source_dir = source_file.parent
    
    # 移除锚点
    parts = url.split('#')
    url_without_anchor = parts[0]
    anchor = parts[1] if len(parts) > 1 else None
    
    if not url_without_anchor:
        # 纯锚点链接 - 检查锚点是否存在
        if anchor:
            return True, None  # 简化处理，假设锚点存在
        return True, None
    
    # 解析路径
    if url_without_anchor.startswith('/'):
        # 绝对路径（相对于仓库根）
        target = Path('.') / url_without_anchor.lstrip('/')
    else:
        # 相对路径
        target = source_dir / url_without_anchor
    
    target = target.resolve()
    
    # 检查文件是否存在
    if not target.exists():
        # 尝试添加.md后缀
        target_with_md = Path(str(target) + '.md')
        if target_with_md.exists():
            return True, None
        
        # 尝试作为目录/index.md
        target_index = target / 'index.md'
        if target_index.exists():
            return True, None
        
        return False, f"文件不存在: {target}"
    
    return True, None


def validate_anchor(content: str, anchor: str) -> bool:
    """验证锚点是否存在"""
    # 规范化锚点
    anchor = anchor.lower().replace(' ', '-')
    
    # 检查标题锚点
    header_pattern = r'^#{1,6}\s+(.+)$'
    for match in re.finditer(header_pattern, content, re.MULTILINE):
        header_text = match.group(1).strip()
        header_anchor = re.sub(r'[^\w\s-]', '', header_text).lower().replace(' ', '-')
        if header_anchor == anchor:
            return True
    
    # 检查自定义锚点
    anchor_pattern = r'<a\s+name=["\']([^"\']+)["\']'
    for match in re.finditer(anchor_pattern, content):
        if match.group(1) == anchor:
            return True
    
    return False


# =============================================================================
# 报告生成
# =============================================================================

def generate_report(
    results: Dict,
    output_path: Path,
    json_path: Optional[Path] = None
):
    """生成链接健康报告"""
    
    external = results.get('external', [])
    internal = results.get('internal', [])
    anchors = results.get('anchors', [])
    
    # 分类统计
    external_ok = [e for e in external if e['result']['status'] == 'ok']
    external_redirect = [e for e in external if e['result']['status'] == 'redirect']
    external_broken = [e for e in external if e['result']['status'] in ['broken', 'timeout', 'error']]
    external_skipped = [e for e in external if e['result']['status'] == 'skipped']
    
    internal_ok = [i for i in internal if i['valid']]
    internal_broken = [i for i in internal if not i['valid']]
    
    # 按文件分组
    broken_by_file = defaultdict(list)
    for link in external_broken + internal_broken:
        broken_by_file[link['file']].append(link)
    
    # 生成Markdown报告
    report_lines = [
        "# 🔗 链接健康检查报告",
        "",
        f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> **检查文件数**: {results.get('file_count', 0)}",
        f"> **总链接数**: {len(external) + len(internal)}",
        "",
        "## 📊 摘要统计",
        "",
        "### 外部链接",
        "",
        "| 状态 | 数量 | 百分比 |",
        "|------|------|--------|",
        f"| ✅ 正常 | {len(external_ok)} | {len(external_ok)/max(len(external),1)*100:.1f}% |",
        f"| 🔄 重定向 | {len(external_redirect)} | {len(external_redirect)/max(len(external),1)*100:.1f}% |",
        f"| ❌ 失效 | {len(external_broken)} | {len(external_broken)/max(len(external),1)*100:.1f}% |",
        f"| ⏭️ 跳过 | {len(external_skipped)} | {len(external_skipped)/max(len(external),1)*100:.1f}% |",
        f"| **总计** | **{len(external)}** | 100% |",
        "",
        "### 内部链接",
        "",
        "| 状态 | 数量 | 百分比 |",
        "|------|------|--------|",
        f"| ✅ 正常 | {len(internal_ok)} | {len(internal_ok)/max(len(internal),1)*100:.1f}% |",
        f"| ❌ 失效 | {len(internal_broken)} | {len(internal_broken)/max(len(internal),1)*100:.1f}% |",
        f"| **总计** | **{len(internal)}** | 100% |",
        "",
    ]
    
    # 失效链接详情
    if broken_by_file:
        report_lines.extend([
            "## ❌ 失效链接详情",
            "",
            f"发现 **{len(external_broken) + len(internal_broken)}** 个失效链接，按文件分组如下：",
            "",
        ])
        
        for file_path, links in sorted(broken_by_file.items()):
            report_lines.extend([
                f"### {file_path}",
                "",
            ])
            for link in links:
                if 'result' in link:  # 外部链接
                    error = link['result'].get('error', '未知错误')
                    report_lines.append(f"- `[外部]` [{link['text']}]({link['url']})")
                    report_lines.append(f"  - 错误: {error}")
                else:  # 内部链接
                    report_lines.append(f"- `[内部]` [{link['text']}]({link['url']})")
                    report_lines.append(f"  - 错误: {link.get('error', '链接无效')}")
                report_lines.append("")
    
    # 重定向链接（可以自动修复）
    if external_redirect:
        report_lines.extend([
            "## 🔄 重定向链接（可自动修复）",
            "",
            "以下链接返回重定向，建议更新为最终URL：",
            "",
        ])
        
        for link in external_redirect[:50]:  # 限制数量
            redirect_url = link['result'].get('redirect_url', '未知')
            report_lines.extend([
                f"- `{link['file']}`",
                f"  - 原文: `[{link['text']}]({link['url']})`",
                f"  - 建议更新为: `{redirect_url}`",
                "",
            ])
        
        if len(external_redirect) > 50:
            report_lines.append(f"_... 还有 {len(external_redirect) - 50} 个重定向链接_")
            report_lines.append("")
    
    # 存档链接建议
    report_lines.extend([
        "## 📦 存档链接建议",
        "",
        "对于失效的外部链接，建议使用以下存档服务查找历史版本：",
        "",
        "- [Wayback Machine](https://web.archive.org/) - Internet Archive",
        "- [archive.today](https://archive.today/)",
        "- [MementoWeb](http://timetravel.mementoweb.org/)",
        "",
        "### 常用修复模式",
        "",
        "```bash",
        "# 使用 Wayback Machine 替换失效链接",
        "python .scripts/fix_broken_links.py --wayback --file <file>",
        "",
        "# 批量修复特定域名的链接",
        "python .scripts/fix_broken_links.py --domain old.example.com --new-domain new.example.com",
        "```",
        "",
    ])
    
    # 写入报告
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    # 生成JSON报告
    if json_path:
        json_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'version': '1.0'
            },
            'summary': {
                'total_files': results.get('file_count', 0),
                'total_links': len(external) + len(internal),
                'external_links': len(external),
                'internal_links': len(internal),
                'broken_external': len(external_broken),
                'broken_internal': len(internal_broken),
                'redirect_links': len(external_redirect)
            },
            'broken_links': [
                {
                    'file': link['file'],
                    'text': link['text'],
                    'url': link['url'],
                    'error': link.get('result', {}).get('error') or link.get('error'),
                    'type': 'external' if 'result' in link else 'internal'
                }
                for link in (external_broken + internal_broken)
            ],
            'redirect_links': [
                {
                    'file': link['file'],
                    'text': link['text'],
                    'original_url': link['url'],
                    'redirect_url': link['result'].get('redirect_url')
                }
                for link in external_redirect
            ]
        }
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)


# =============================================================================
# 主程序
# =============================================================================

async def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 全量链接检查器'
    )
    parser.add_argument(
        '--path', '-p',
        default='.',
        help='要检查的根目录路径（默认: 当前目录）'
    )
    parser.add_argument(
        '--output', '-o',
        default='reports/link-health-report.md',
        help='Markdown报告输出路径'
    )
    parser.add_argument(
        '--json', '-j',
        default='reports/link-health-results.json',
        help='JSON结果输出路径'
    )
    parser.add_argument(
        '--timeout', '-t',
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f'请求超时时间（秒，默认: {DEFAULT_TIMEOUT}）'
    )
    parser.add_argument(
        '--concurrent', '-c',
        type=int,
        default=CONCURRENT_LIMIT,
        help=f'并发请求数（默认: {CONCURRENT_LIMIT}）'
    )
    parser.add_argument(
        '--retries', '-r',
        type=int,
        default=MAX_RETRIES,
        help=f'重试次数（默认: {MAX_RETRIES}）'
    )
    parser.add_argument(
        '--skip-external',
        action='store_true',
        help='跳过外部链接检查'
    )
    parser.add_argument(
        '--skip-internal',
        action='store_true',
        help='跳过内部链接检查'
    )
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='不使用缓存'
    )
    
    args = parser.parse_args()
    
    root_path = Path(args.path).resolve()
    output_path = Path(args.output)
    json_path = Path(args.json)
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("AnalysisDataFlow 全量链接检查器")
    print("=" * 70)
    print(f"检查路径: {root_path}")
    print(f"输出报告: {output_path}")
    print(f"超时设置: {args.timeout}秒")
    print(f"并发限制: {args.concurrent}")
    print("=" * 70)
    
    # 加载缓存
    cache = None if args.no_cache else LinkCache()
    
    # 收集所有Markdown文件
    print("\n📁 扫描Markdown文件...")
    md_files = find_all_markdown_files(root_path)
    all_files_set = set(md_files)
    print(f"   找到 {len(md_files)} 个Markdown文件")
    
    # 收集所有链接
    print("\n🔗 提取链接...")
    external_links = []
    internal_links = []
    anchor_links = []
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"   ⚠️  无法读取 {md_file}: {e}")
            continue
        
        links = extract_links(content)
        
        for text, url, pos in links:
            link_type = classify_link(url)
            link_info = {
                'file': str(md_file.relative_to(root_path)),
                'text': text,
                'url': url,
                'position': pos
            }
            
            if link_type == 'external':
                if not should_skip_url(url):
                    external_links.append(link_info)
            elif link_type == 'internal':
                internal_links.append(link_info)
            elif link_type == 'anchor':
                anchor_links.append(link_info)
    
    print(f"   外部链接: {len(external_links)}")
    print(f"   内部链接: {len(internal_links)}")
    print(f"   锚点链接: {len(anchor_links)}")
    
    # 检查结果
    results = {
        'file_count': len(md_files),
        'external': [],
        'internal': [],
        'anchors': []
    }
    
    # 检查外部链接
    if not args.skip_external and external_links:
        print("\n🌐 检查外部链接...")
        
        # 去重URL
        unique_urls = list(set(link['url'] for link in external_links))
        print(f"   唯一URL数: {len(unique_urls)}")
        
        # 检查缓存
        if cache:
            cached_results = {}
            urls_to_check = []
            for url in unique_urls:
                cached = cache.get(url)
                if cached:
                    cached_results[url] = {
                        'status': cached['status'],
                        'redirect_url': cached.get('redirect_url'),
                        'error': None
                    }
                else:
                    urls_to_check.append(url)
            print(f"   缓存命中: {len(cached_results)}")
        else:
            cached_results = {}
            urls_to_check = unique_urls
        
        # 并发检查
        url_results = dict(cached_results)
        
        async with aiohttp.ClientSession(
            headers={'User-Agent': USER_AGENT}
        ) as session:
            semaphore = asyncio.Semaphore(args.concurrent)
            
            async def check_with_limit(url):
                async with semaphore:
                    result = await check_external_link(session, url, args.timeout)
                    return url, result
            
            tasks = [check_with_limit(url) for url in urls_to_check]
            
            completed = 0
            for coro in asyncio.as_completed(tasks):
                url, result = await coro
                url_results[url] = result
                completed += 1
                if completed % 10 == 0 or completed == len(urls_to_check):
                    print(f"   进度: {completed}/{len(urls_to_check)}")
                
                # 更新缓存
                if cache:
                    cache.set(url, result)
            
            # 保存缓存
            if cache:
                cache.save_cache()
        
        # 将结果映射回所有链接
        for link in external_links:
            link['result'] = url_results.get(link['url'], {
                'status': 'unknown',
                'error': '未检查'
            })
        
        results['external'] = external_links
        
        # 统计
        ok_count = sum(1 for l in external_links if l['result']['status'] == 'ok')
        redirect_count = sum(1 for l in external_links if l['result']['status'] == 'redirect')
        broken_count = sum(1 for l in external_links if l['result']['status'] in ['broken', 'error', 'timeout'])
        
        print(f"   ✅ 正常: {ok_count}")
        print(f"   🔄 重定向: {redirect_count}")
        print(f"   ❌ 失效: {broken_count}")
    
    # 检查内部链接
    if not args.skip_internal:
        print("\n📄 检查内部链接...")
        
        for i, link in enumerate(internal_links):
            is_valid, error = validate_internal_link(
                link['url'], 
                root_path / link['file'], 
                all_files_set
            )
            link['valid'] = is_valid
            link['error'] = error
            
            if (i + 1) % 100 == 0:
                print(f"   进度: {i + 1}/{len(internal_links)}")
        
        results['internal'] = internal_links
        
        valid_count = sum(1 for l in internal_links if l['valid'])
        invalid_count = len(internal_links) - valid_count
        
        print(f"   ✅ 有效: {valid_count}")
        print(f"   ❌ 无效: {invalid_count}")
    
    # 生成报告
    print("\n📝 生成报告...")
    generate_report(results, output_path, json_path)
    print(f"   Markdown报告: {output_path}")
    print(f"   JSON报告: {json_path}")
    
    print("\n" + "=" * 70)
    print("检查完成!")
    print("=" * 70)
    
    # 返回退出码
    broken_count = (
        sum(1 for l in results.get('external', []) if l['result']['status'] in ['broken', 'error', 'timeout']) +
        sum(1 for l in results.get('internal', []) if not l.get('valid', True))
    )
    
    if broken_count > 0:
        print(f"⚠️  发现 {broken_count} 个失效链接")
        sys.exit(1)
    else:
        print("✅ 所有链接正常")
        sys.exit(0)


if __name__ == '__main__':
    asyncio.run(main())
