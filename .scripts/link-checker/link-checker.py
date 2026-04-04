#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
链接检查器 v2.0 - 外部链接健康检查脚本

功能:
- 递归扫描所有Markdown文件中的外部链接
- HTTP状态检查 (200/404/500/重定向/超时)
- Markdown格式检查报告 (正常/警告/错误分类)
- 并发请求控制与缓存机制
- 支持断点续查

作者: AnalysisDataFlow 项目
版本: 2.0.0
"""

import asyncio
import argparse
import hashlib
import json
import logging
import pickle
import re
import sys
import time
import yaml
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from urllib.parse import urlparse, urljoin, unquote
from collections import defaultdict

import aiohttp
from aiohttp import ClientSession, ClientTimeout, ClientError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('link-checker.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class LinkCheckResult:
    """链接检查结果数据类"""
    url: str
    source_file: str
    line_number: int
    link_type: str  # 'external', 'internal', 'anchor', 'email', 'file'
    status_code: Optional[int] = None
    is_valid: bool = False
    error_message: Optional[str] = None
    response_time: float = 0.0
    redirect_url: Optional[str] = None
    checked_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def get_status_category(self) -> str:
        """获取状态分类: success/warning/error"""
        if not self.is_valid:
            return "error"
        if self.error_message:
            return "warning"
        return "success"


@dataclass
class CheckSummary:
    """检查汇总数据类"""
    total_files: int = 0
    total_links: int = 0
    valid_links: int = 0
    broken_links: int = 0
    warning_links: int = 0
    skipped_links: int = 0
    check_duration: float = 0.0
    started_at: str = ""
    completed_at: str = ""
    cached_results: int = 0
    resumed_from_checkpoint: bool = False


class LinkCache:
    """链接检查结果缓存管理器"""
    
    def __init__(self, cache_dir: Path, ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        self.cache_file = self.cache_dir / "link_cache.pkl"
        self.checkpoint_file = self.cache_dir / "checkpoint.json"
        self._cache: Dict[str, Tuple[LinkCheckResult, datetime]] = {}
        self._load_cache()
    
    def _get_url_hash(self, url: str) -> str:
        """生成URL的哈希键"""
        return hashlib.md5(url.encode('utf-8')).hexdigest()
    
    def _load_cache(self):
        """从磁盘加载缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    data = pickle.load(f)
                    self._cache = {
                        k: (v, timestamp) 
                        for k, (v, timestamp) in data.items()
                        if datetime.now() - timestamp < self.ttl
                    }
                logger.info(f"已加载 {len(self._cache)} 条缓存记录")
            except Exception as e:
                logger.warning(f"加载缓存失败: {e}")
                self._cache = {}
    
    def save_cache(self):
        """保存缓存到磁盘"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self._cache, f)
            logger.info(f"已保存 {len(self._cache)} 条缓存记录")
        except Exception as e:
            logger.error(f"保存缓存失败: {e}")
    
    def get(self, url: str) -> Optional[LinkCheckResult]:
        """获取缓存结果"""
        url_hash = self._get_url_hash(url)
        if url_hash in self._cache:
            result, timestamp = self._cache[url_hash]
            if datetime.now() - timestamp < self.ttl:
                logger.debug(f"缓存命中: {url[:80]}...")
                return result
            else:
                del self._cache[url_hash]
        return None
    
    def set(self, url: str, result: LinkCheckResult):
        """设置缓存结果"""
        url_hash = self._get_url_hash(url)
        self._cache[url_hash] = (result, datetime.now())
    
    def save_checkpoint(self, processed_files: List[str], total_files: int):
        """保存检查点"""
        checkpoint = {
            'processed_files': processed_files,
            'total_files': total_files,
            'saved_at': datetime.now().isoformat(),
            'version': '2.0.0'
        }
        try:
            with open(self.checkpoint_file, 'w', encoding='utf-8') as f:
                json.dump(checkpoint, f, indent=2)
        except Exception as e:
            logger.error(f"保存检查点失败: {e}")
    
    def load_checkpoint(self) -> Optional[Tuple[List[str], int]]:
        """加载检查点，返回已处理的文件列表和总文件数"""
        if not self.checkpoint_file.exists():
            return None
        try:
            with open(self.checkpoint_file, 'r', encoding='utf-8') as f:
                checkpoint = json.load(f)
            processed = checkpoint.get('processed_files', [])
            total = checkpoint.get('total_files', 0)
            saved_at = datetime.fromisoformat(checkpoint.get('saved_at', '2000-01-01'))
            # 检查检查点是否过期（7天）
            if datetime.now() - saved_at > timedelta(days=7):
                logger.info("检查点已过期，重新开始检查")
                return None
            logger.info(f"从检查点恢复: 已处理 {len(processed)}/{total} 个文件")
            return processed, total
        except Exception as e:
            logger.warning(f"加载检查点失败: {e}")
            return None
    
    def clear_checkpoint(self):
        """清除检查点"""
        if self.checkpoint_file.exists():
            self.checkpoint_file.unlink()


class LinkExtractor:
    """Markdown链接提取器"""
    
    # Markdown链接正则: [text](url) 或 [text](url "title")
    MARKDOWN_LINK_PATTERN = re.compile(
        r'\[([^\]]+)\]\(([^\s\)]+)(?:\s+"[^"]*")?\)'
    )
    
    # HTML链接正则: <a href="url">
    HTML_LINK_PATTERN = re.compile(
        r'<a[^>]+href=["\']([^"\'>]+)["\'][^>]*>',
        re.IGNORECASE
    )
    
    # 引用链接正则: [text][ref] 或 [text]
    REFERENCE_LINK_PATTERN = re.compile(
        r'\[([^\]]+)\](?:\[([^\]]*)\])?'
    )
    
    # 引用定义正则: [ref]: url
    REFERENCE_DEF_PATTERN = re.compile(
        r'^\[([^\]]+)\]:\s*(\S+)'
    )
    
    # 自动链接: <url>
    AUTO_LINK_PATTERN = re.compile(
        r'<([a-zA-Z][a-zA-Z0-9+.-]*:[^>]+)>'
    )
    
    # 裸URL正则 (http/https开头)
    BARE_URL_PATTERN = re.compile(
        r'(?<![\[\(])https?://[^\s<>"\')\]]+(?:[^\s<>"\')\].,;!?])'
    )

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.file_cache: Dict[Path, str] = {}

    def extract_links(self, file_path: Path) -> List[Tuple[str, int]]:
        """从Markdown文件中提取所有链接"""
        links = []
        
        try:
            content = self._read_file(file_path)
            lines = content.split('\n')
            in_code_block = False
            
            # 收集引用定义
            references = {}
            for line_num, line in enumerate(lines, 1):
                ref_match = self.REFERENCE_DEF_PATTERN.match(line)
                if ref_match:
                    ref_name = ref_match.group(1)
                    ref_url = ref_match.group(2)
                    references[ref_name] = (ref_url, line_num)
            
            for line_num, line in enumerate(lines, 1):
                # 检测代码块边界
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue
                
                # 跳过代码块内容
                if in_code_block:
                    continue
                
                # 跳过行内代码
                line_without_inline_code = re.sub(r'`[^`]*`', '', line)
                    
                # 提取Markdown链接
                for match in self.MARKDOWN_LINK_PATTERN.finditer(line_without_inline_code):
                    url = match.group(2)
                    links.append((url, line_num))
                
                # 提取HTML链接
                for match in self.HTML_LINK_PATTERN.finditer(line_without_inline_code):
                    url = match.group(1)
                    links.append((url, line_num))
                
                # 提取自动链接
                for match in self.AUTO_LINK_PATTERN.finditer(line_without_inline_code):
                    url = match.group(1)
                    links.append((url, line_num))
                
                # 提取裸URL (仅在非代码行)
                for match in self.BARE_URL_PATTERN.finditer(line_without_inline_code):
                    url = match.group(0)
                    # 排除已捕获的链接
                    if not any(l[0] == url and l[1] == line_num for l in links):
                        links.append((url, line_num))
                
                # 处理引用链接
                for match in self.REFERENCE_LINK_PATTERN.finditer(line_without_inline_code):
                    ref_name = match.group(2) or match.group(1)
                    if ref_name in references:
                        url, _ = references[ref_name]
                        links.append((url, line_num))
                        
        except Exception as e:
            logger.error(f"提取链接时出错 {file_path}: {e}")
            
        return links

    def _read_file(self, file_path: Path) -> str:
        """读取文件内容（带缓存）"""
        if file_path not in self.file_cache:
            try:
                self.file_cache[file_path] = file_path.read_text(encoding='utf-8')
            except Exception as e:
                logger.error(f"读取文件失败 {file_path}: {e}")
                return ""
        return self.file_cache[file_path]


class LinkChecker:
    """链接检查器核心类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.extractor: Optional[LinkExtractor] = None
        self.session: Optional[ClientSession] = None
        self.results: List[LinkCheckResult] = []
        self.cache: Optional[LinkCache] = None
        self.visited_urls: Set[str] = set()
        self.file_exists_cache: Dict[Path, bool] = {}
        self.anchor_cache: Dict[Path, Set[str]] = {}
        self.processed_files: List[str] = []
        
        # 统计信息
        self.summary = CheckSummary()
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        timeout_config = self.config.get('timeout', {})
        timeout = ClientTimeout(
            total=timeout_config.get('total', 30),
            connect=timeout_config.get('connect', 10)
        )
        
        headers = {
            'User-Agent': self.config.get('user_agent', 
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            ),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        
        connector = aiohttp.TCPConnector(
            limit=self.config.get('max_concurrent', 50),
            limit_per_host=self.config.get('max_per_host', 10),
            enable_cleanup_closed=True,
            force_close=True,
        )
        
        self.session = ClientSession(
            timeout=timeout,
            headers=headers,
            connector=connector
        )
        
        # 初始化缓存
        cache_config = self.config.get('cache', {})
        if cache_config.get('enabled', True):
            cache_dir = Path(cache_config.get('cache_dir', '.link-checker-cache'))
            ttl = cache_config.get('ttl', 24)
            self.cache = LinkCache(cache_dir, ttl)
        
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
        if self.cache:
            self.cache.save_cache()

    def _classify_link(self, url: str) -> str:
        """分类链接类型"""
        if url.startswith(('http://', 'https://')):
            return 'external'
        elif url.startswith('mailto:'):
            return 'email'
        elif url.startswith('#'):
            return 'anchor'
        elif url.startswith(('file://', '/', './', '../')):
            return 'file'
        else:
            return 'internal'

    def _is_excluded(self, url: str) -> bool:
        """检查URL是否在排除列表中"""
        exclude_patterns = self.config.get('exclude', [])
        for pattern in exclude_patterns:
            try:
                if re.search(pattern, url):
                    return True
            except re.error:
                logger.warning(f"无效的排除模式: {pattern}")
        return False

    def _get_domain_delay(self, url: str) -> float:
        """获取特定域名的延迟设置"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        rate_limit = self.config.get('rate_limit', {})
        domains = rate_limit.get('domains', {})
        
        for domain_pattern, settings in domains.items():
            if domain_pattern in domain:
                return settings.get('delay', rate_limit.get('domain_delay', 0))
        
        return rate_limit.get('domain_delay', 0)

    async def check_external_link(self, url: str) -> LinkCheckResult:
        """检查外部链接"""
        result = LinkCheckResult(
            url=url,
            source_file="",
            line_number=0,
            link_type='external'
        )
        
        if self._is_excluded(url):
            result.error_message = "URL在排除列表中"
            result.is_valid = True  # 跳过视为有效
            return result
        
        # 检查缓存
        if self.cache:
            cached = self.cache.get(url)
            if cached:
                self.summary.cached_results += 1
                return cached
        
        # 域名速率限制延迟
        domain_delay = self._get_domain_delay(url)
        if domain_delay > 0:
            await asyncio.sleep(domain_delay)
        
        retry_config = self.config.get('retry', {})
        max_retries = retry_config.get('max_retries', 3)
        retry_delay = retry_config.get('delay', 1)
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                
                # 使用HEAD请求先尝试
                try:
                    async with self.session.head(
                        url, 
                        allow_redirects=True,
                        ssl=False
                    ) as response:
                        result.response_time = time.time() - start_time
                        result.status_code = response.status
                        
                        if response.history:
                            result.redirect_url = str(response.url)
                        
                        # 如果HEAD成功，直接使用结果
                        if 200 <= response.status < 300:
                            result.is_valid = True
                            if self.cache:
                                self.cache.set(url, result)
                            return result
                        
                        # 某些服务器不支持HEAD，继续用GET
                        if response.status in [405, 501]:
                            raise aiohttp.ClientError("HEAD not allowed")
                            
                        # 处理其他状态码
                        return self._process_status_code(result, response.status)
                        
                except (aiohttp.ClientError, asyncio.TimeoutError):
                    # HEAD失败，使用GET重试
                    pass
                
                # 使用GET请求
                async with self.session.get(
                    url, 
                    allow_redirects=True,
                    ssl=False
                ) as response:
                    result.response_time = time.time() - start_time
                    result.status_code = response.status
                    
                    if response.history:
                        result.redirect_url = str(response.url)
                    
                    return self._process_status_code(result, response.status)
                    
            except asyncio.TimeoutError:
                result.error_message = f"请求超时 (尝试 {attempt + 1}/{max_retries})"
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))
                    continue
                    
            except ClientError as e:
                result.error_message = f"客户端错误: {str(e)}"
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (attempt + 1))
                    continue
                    
            except Exception as e:
                result.error_message = f"未知错误: {str(e)}"
                break
        
        if self.cache:
            self.cache.set(url, result)
        return result
    
    def _process_status_code(self, result: LinkCheckResult, status: int) -> LinkCheckResult:
        """处理HTTP状态码"""
        result.status_code = status
        
        # 2xx 状态码视为有效
        if 200 <= status < 300:
            result.is_valid = True
        # 3xx 状态码视为警告（但有效）
        elif 300 <= status < 400:
            result.is_valid = True
            if status == 301:
                result.error_message = f"永久重定向: HTTP {status}"
            elif status == 302:
                result.error_message = f"临时重定向: HTTP {status}"
            else:
                result.error_message = f"重定向: HTTP {status}"
        # 4xx 客户端错误
        elif 400 <= status < 500:
            result.is_valid = False
            if status == 404:
                result.error_message = "页面未找到: HTTP 404"
            elif status == 403:
                result.error_message = "访问被拒绝: HTTP 403"
            elif status == 401:
                result.error_message = "需要认证: HTTP 401"
            elif status == 410:
                result.error_message = "资源已删除: HTTP 410"
            else:
                result.error_message = f"客户端错误: HTTP {status}"
        # 5xx 服务器错误
        elif 500 <= status < 600:
            result.is_valid = False
            if status == 500:
                result.error_message = "服务器内部错误: HTTP 500"
            elif status == 502:
                result.error_message = "网关错误: HTTP 502"
            elif status == 503:
                result.error_message = "服务不可用: HTTP 503"
            elif status == 504:
                result.error_message = "网关超时: HTTP 504"
            else:
                result.error_message = f"服务器错误: HTTP {status}"
        else:
            result.error_message = f"未知状态码: HTTP {status}"
        
        if self.cache:
            self.cache.set(result.url, result)
        return result

    def check_internal_link(self, url: str, source_file: Path) -> LinkCheckResult:
        """检查内部链接"""
        result = LinkCheckResult(
            url=url,
            source_file=str(source_file),
            line_number=0,
            link_type='internal'
        )
        
        try:
            # 解析URL
            parsed = urlparse(url)
            
            # 处理锚点链接
            if '#' in url:
                base_url, anchor = url.split('#', 1)
            else:
                base_url, anchor = url, None
            
            # 解析目标文件路径
            if base_url.startswith('/'):
                target_path = self.extractor.base_path / base_url.lstrip('/')
            elif base_url.startswith(('./', '../')) or not base_url.startswith(('http', 'mailto', 'file')):
                target_path = source_file.parent / base_url
                target_path = target_path.resolve()
            else:
                result.error_message = f"无法解析的内部链接: {url}"
                return result
            
            # 检查文件是否存在
            if target_path in self.file_exists_cache:
                file_exists = self.file_exists_cache[target_path]
            else:
                file_exists = target_path.exists()
                self.file_exists_cache[target_path] = file_exists
            
            if not file_exists:
                result.error_message = f"文件不存在: {target_path.relative_to(self.extractor.base_path)}"
                return result
            
            # 如果有锚点，检查锚点是否存在
            if anchor:
                if target_path not in self.anchor_cache:
                    self.anchor_cache[target_path] = self._extract_anchors(target_path)
                
                anchors = self.anchor_cache[target_path]
                decoded_anchor = unquote(anchor).lower().replace(' ', '-')
                
                if decoded_anchor not in anchors:
                    result.error_message = f"锚点不存在: #{anchor}"
                    result.is_valid = False
                    return result
            
            result.is_valid = True
            
        except Exception as e:
            result.error_message = f"检查内部链接时出错: {str(e)}"
        
        return result

    def _extract_anchors(self, file_path: Path) -> Set[str]:
        """从Markdown文件中提取所有锚点"""
        anchors = set()
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 提取标题锚点
            header_pattern = re.compile(r'^#{1,6}\s+(.+)$', re.MULTILINE)
            for match in header_pattern.finditer(content):
                title = match.group(1).strip()
                anchor = title.lower()
                anchor = re.sub(r'[^\w\s-]', '', anchor)
                anchor = re.sub(r'\s+', '-', anchor)
                anchors.add(anchor)
            
            # 提取HTML锚点
            html_anchor_pattern = re.compile(r'<a[^>]+name=["\']([^"\'>]+)["\'][^>]*>', re.IGNORECASE)
            for match in html_anchor_pattern.finditer(content):
                anchors.add(match.group(1).lower())
            
            # 提取id锚点
            id_pattern = re.compile(r'<[^>]+id=["\']([^"\'>]+)["\'][^>]*>', re.IGNORECASE)
            for match in id_pattern.finditer(content):
                anchors.add(match.group(1).lower())
                
        except Exception as e:
            logger.warning(f"提取锚点时出错 {file_path}: {e}")
        
        return anchors

    def check_file_link(self, url: str, source_file: Path) -> LinkCheckResult:
        """检查文件链接"""
        result = LinkCheckResult(
            url=url,
            source_file=str(source_file),
            line_number=0,
            link_type='file'
        )
        
        try:
            if url.startswith('file://'):
                file_path = Path(unquote(url[7:]))
            elif url.startswith('/'):
                file_path = self.extractor.base_path / url.lstrip('/')
            else:
                file_path = source_file.parent / url
                file_path = file_path.resolve()
            
            if file_path.exists():
                result.is_valid = True
            else:
                result.error_message = f"文件不存在: {file_path}"
                
        except Exception as e:
            result.error_message = f"检查文件链接时出错: {str(e)}"
        
        return result

    def check_email_link(self, url: str) -> LinkCheckResult:
        """检查邮件链接"""
        result = LinkCheckResult(
            url=url,
            source_file="",
            line_number=0,
            link_type='email'
        )
        
        email_pattern = re.compile(r'^mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
        if email_pattern.match(url):
            result.is_valid = True
        else:
            result.error_message = "邮件格式无效"
        
        return result

    async def process_file(self, file_path: Path) -> List[LinkCheckResult]:
        """处理单个文件中的所有链接"""
        results = []
        links = self.extractor.extract_links(file_path)
        
        logger.info(f"检查文件: {file_path.relative_to(self.extractor.base_path)} ({len(links)} 个链接)")
        
        external_links = []
        for url, line_num in links:
            link_type = self._classify_link(url)
            
            if link_type == 'external':
                external_links.append((url, line_num))
            else:
                if link_type == 'internal':
                    result = self.check_internal_link(url, file_path)
                elif link_type == 'file':
                    result = self.check_file_link(url, file_path)
                elif link_type == 'email':
                    result = self.check_email_link(url)
                elif link_type == 'anchor':
                    result = self.check_internal_link(url, file_path)
                else:
                    continue
                
                result.source_file = str(file_path)
                result.line_number = line_num
                results.append(result)
        
        # 异步批量检查外部链接
        if external_links:
            semaphore = asyncio.Semaphore(self.config.get('max_concurrent', 50))
            
            async def check_with_limit(url, line_num):
                async with semaphore:
                    result = await self.check_external_link(url)
                    result.source_file = str(file_path)
                    result.line_number = line_num
                    return result
            
            external_results = await asyncio.gather(*[
                check_with_limit(url, line_num) 
                for url, line_num in external_links
            ])
            results.extend(external_results)
        
        return results

    async def run(self, base_path: Path, include_patterns: List[str] = None, 
                  resume: bool = True) -> Tuple[List[LinkCheckResult], CheckSummary]:
        """运行链接检查"""
        self.summary.started_at = datetime.now().isoformat()
        start_time = time.time()
        
        self.extractor = LinkExtractor(base_path)
        
        # 查找所有Markdown文件
        md_files = []
        for pattern in (include_patterns or ['**/*.md']):
            md_files.extend(base_path.glob(pattern))
        
        # 去重并保持顺序
        seen = set()
        md_files = [f for f in md_files if not (f in seen or seen.add(f))]
        
        total_files = len(md_files)
        self.summary.total_files = total_files
        
        # 尝试从检查点恢复
        processed_files_set = set()
        if resume and self.cache:
            checkpoint = self.cache.load_checkpoint()
            if checkpoint:
                processed_files_list, _ = checkpoint
                processed_files_set = set(processed_files_list)
                self.summary.resumed_from_checkpoint = True
                logger.info(f"断点续查: 跳过已处理的 {len(processed_files_set)} 个文件")
        
        # 过滤已处理的文件
        files_to_process = [f for f in md_files if str(f) not in processed_files_set]
        
        logger.info(f"找到 {total_files} 个Markdown文件，待处理: {len(files_to_process)} 个")
        
        # 并发处理所有文件
        all_results = []
        batch_size = self.config.get('file_batch_size', 10)
        
        try:
            for i in range(0, len(files_to_process), batch_size):
                batch = files_to_process[i:i + batch_size]
                batch_results = await asyncio.gather(*[
                    self.process_file(f) for f in batch
                ])
                for results in batch_results:
                    all_results.extend(results)
                
                # 更新已处理文件列表
                self.processed_files.extend(str(f) for f in batch)
                
                # 保存检查点
                if self.cache:
                    self.cache.save_checkpoint(self.processed_files, total_files)
                
                logger.info(f"进度: {len(self.processed_files)}/{total_files} 文件")
                
        except KeyboardInterrupt:
            logger.warning("检查被中断，已保存检查点")
            if self.cache:
                self.cache.save_checkpoint(self.processed_files, total_files)
            raise
        
        self.results = all_results
        self.summary.total_links = len(all_results)
        
        # 统计结果
        for result in all_results:
            if result.is_valid and not result.error_message:
                self.summary.valid_links += 1
            elif result.is_valid and result.error_message:
                self.summary.warning_links += 1
            elif not result.is_valid:
                self.summary.broken_links += 1
        
        self.summary.check_duration = time.time() - start_time
        self.summary.completed_at = datetime.now().isoformat()
        
        # 清除检查点（检查完成）
        if self.cache:
            self.cache.clear_checkpoint()
        
        logger.info(f"检查完成: {self.summary.total_links} 个链接, "
                   f"{self.summary.valid_links} 有效, "
                   f"{self.summary.warning_links} 警告, "
                   f"{self.summary.broken_links} 失效, "
                   f"{self.summary.cached_results} 来自缓存")
        
        return all_results, self.summary

    def save_results(self, output_path: Path):
        """保存检查结果到JSON文件"""
        data = {
            'summary': asdict(self.summary),
            'results': [asdict(r) for r in self.results]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"JSON结果已保存到: {output_path}")

    def generate_markdown_report(self, output_path: Path):
        """生成Markdown格式报告"""
        report_lines = []
        
        # 标题
        report_lines.append("# 链接健康检查报告\n")
        report_lines.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 执行摘要
        report_lines.append("## 执行摘要\n")
        report_lines.append("| 指标 | 数值 |")
        report_lines.append("|------|------|")
        report_lines.append(f"| 扫描文件数 | {self.summary.total_files} |")
        report_lines.append(f"| 检查链接总数 | {self.summary.total_links} |")
        report_lines.append(f"| ✅ 正常链接 | {self.summary.valid_links} |")
        report_lines.append(f"| ⚠️ 警告链接 | {self.summary.warning_links} |")
        report_lines.append(f"| ❌ 错误链接 | {self.summary.broken_links} |")
        report_lines.append(f"| 📦 缓存命中 | {self.summary.cached_results} |")
        report_lines.append(f"| 检查耗时 | {self.summary.check_duration:.2f} 秒 |")
        if self.summary.resumed_from_checkpoint:
            report_lines.append(f"| 断点续查 | 是 |")
        report_lines.append("")
        
        # 状态概览
        report_lines.append("## 状态概览\n")
        
        # 按状态分类统计
        status_stats = defaultdict(int)
        for result in self.results:
            if result.status_code:
                status_stats[result.status_code] += 1
        
        if status_stats:
            report_lines.append("### HTTP状态码分布\n")
            report_lines.append("| 状态码 | 数量 | 说明 |")
            report_lines.append("|--------|------|------|")
            for code in sorted(status_stats.keys()):
                count = status_stats[code]
                desc = self._get_status_description(code)
                emoji = "✅" if 200 <= code < 300 else "⚠️" if 300 <= code < 400 else "❌"
                report_lines.append(f"| {emoji} {code} | {count} | {desc} |")
            report_lines.append("")
        
        # 错误链接详情
        error_results = [r for r in self.results if r.get_status_category() == 'error']
        if error_results:
            report_lines.append(f"## ❌ 错误链接 ({len(error_results)} 个)\n")
            report_lines.append("| 文件 | 行号 | 链接 | 状态码 | 错误信息 |")
            report_lines.append("|------|------|------|--------|----------|")
            for result in error_results:
                rel_path = Path(result.source_file).relative_to(self.extractor.base_path) if self.extractor else result.source_file
                status = result.status_code or "N/A"
                url_short = result.url[:60] + "..." if len(result.url) > 60 else result.url
                error_msg = result.error_message[:50] + "..." if len(result.error_message) > 50 else result.error_message
                report_lines.append(f"| `{rel_path}` | {result.line_number} | [{url_short}]({result.url}) | {status} | {error_msg} |")
            report_lines.append("")
        
        # 警告链接详情
        warning_results = [r for r in self.results if r.get_status_category() == 'warning']
        if warning_results:
            report_lines.append(f"## ⚠️ 警告链接 ({len(warning_results)} 个)\n")
            report_lines.append("| 文件 | 行号 | 链接 | 状态码 | 警告信息 |")
            report_lines.append("|------|------|------|--------|----------|")
            for result in warning_results:
                rel_path = Path(result.source_file).relative_to(self.extractor.base_path) if self.extractor else result.source_file
                status = result.status_code or "N/A"
                url_short = result.url[:60] + "..." if len(result.url) > 60 else result.url
                warn_msg = result.error_message[:50] + "..." if len(result.error_message) > 50 else result.error_message
                report_lines.append(f"| `{rel_path}` | {result.line_number} | [{url_short}]({result.url}) | {status} | {warn_msg} |")
            report_lines.append("")
        
        # 按文件统计
        report_lines.append("## 按文件统计\n")
        file_stats = defaultdict(lambda: {'total': 0, 'success': 0, 'warning': 0, 'error': 0})
        for result in self.results:
            file_path = result.source_file
            file_stats[file_path]['total'] += 1
            cat = result.get_status_category()
            file_stats[file_path][cat] += 1
        
        report_lines.append("| 文件 | 总数 | ✅ 正常 | ⚠️ 警告 | ❌ 错误 |")
        report_lines.append("|------|------|---------|---------|--------|")
        for file_path, stats in sorted(file_stats.items()):
            rel_path = Path(file_path).relative_to(self.extractor.base_path) if self.extractor else file_path
            report_lines.append(f"| `{rel_path}` | {stats['total']} | {stats['success']} | {stats['warning']} | {stats['error']} |")
        report_lines.append("")
        
        # 建议操作
        report_lines.append("## 建议操作\n")
        if error_results:
            report_lines.append("### 高优先级修复\n")
            report_lines.append("以下链接返回错误或无法访问，建议优先修复:\n")
            for result in error_results[:5]:
                rel_path = Path(result.source_file).relative_to(self.extractor.base_path) if self.extractor else result.source_file
                report_lines.append(f"- `{rel_path}:{result.line_number}` - {result.error_message}")
            if len(error_results) > 5:
                report_lines.append(f"- ... 还有 {len(error_results) - 5} 个错误链接\n")
            report_lines.append("")
        
        if warning_results:
            report_lines.append("### 低优先级优化\n")
            report_lines.append("以下链接有重定向或其他警告，建议适时更新:\n")
            for result in warning_results[:5]:
                rel_path = Path(result.source_file).relative_to(self.extractor.base_path) if self.extractor else result.source_file
                report_lines.append(f"- `{rel_path}:{result.line_number}` - {result.error_message}")
            if len(warning_results) > 5:
                report_lines.append(f"- ... 还有 {len(warning_results) - 5} 个警告链接\n")
            report_lines.append("")
        
        # 页脚
        report_lines.append("---\n")
        report_lines.append("*本报告由链接检查器自动生成*\n")
        
        # 写入文件
        report_content = "\n".join(report_lines)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"Markdown报告已保存到: {output_path}")
        return report_content
    
    def _get_status_description(self, code: int) -> str:
        """获取HTTP状态码描述"""
        descriptions = {
            200: "OK - 请求成功",
            301: "Moved Permanently - 永久重定向",
            302: "Found - 临时重定向",
            304: "Not Modified - 未修改",
            400: "Bad Request - 请求错误",
            401: "Unauthorized - 未授权",
            403: "Forbidden - 禁止访问",
            404: "Not Found - 未找到",
            410: "Gone - 已删除",
            500: "Internal Server Error - 服务器错误",
            502: "Bad Gateway - 网关错误",
            503: "Service Unavailable - 服务不可用",
            504: "Gateway Timeout - 网关超时",
        }
        return descriptions.get(code, "未知状态")


def load_config(config_path: Path) -> Dict[str, Any]:
    """加载配置文件"""
    default_config = {
        'timeout': {'total': 30, 'connect': 10},
        'retry': {'max_retries': 3, 'delay': 1},
        'max_concurrent': 50,
        'max_per_host': 10,
        'file_batch_size': 10,
        'cache': {'enabled': True, 'cache_dir': '.link-checker-cache', 'ttl': 24},
        'exclude': [
            '^https?://localhost',
            '^https?://127\\.',
            '^https?://example\\.com',
        ],
        'rate_limit': {'domain_delay': 0}
    }
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f) or {}
            # 合并配置
            for key, value in user_config.items():
                if isinstance(value, dict) and key in default_config:
                    default_config[key].update(value)
                else:
                    default_config[key] = value
            logger.info(f"已加载配置文件: {config_path}")
        except Exception as e:
            logger.warning(f"加载配置文件失败: {e}，使用默认配置")
    else:
        logger.info("未找到配置文件，使用默认配置")
    
    return default_config


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Markdown外部链接健康检查器 v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本使用
  %(prog)s --path ./docs
  
  # 指定配置文件和输出
  %(prog)s --path ./docs --config config.yaml --output report.md
  
  # 生成JSON和Markdown两种格式
  %(prog)s --path ./docs --json results.json --markdown report.md
  
  # 重新开始检查（忽略断点）
  %(prog)s --path ./docs --no-resume
  
  # 清除缓存
  %(prog)s --clear-cache
        """
    )
    
    parser.add_argument('--path', '-p', type=str, default='.',
                       help='要扫描的基础目录路径 (默认: 当前目录)')
    parser.add_argument('--config', '-c', type=str, default='config.yaml',
                       help='配置文件路径 (默认: config.yaml)')
    parser.add_argument('--output', '-o', type=str, default='link-check-report.md',
                       help='输出Markdown报告路径 (默认: link-check-report.md)')
    parser.add_argument('--json', '-j', type=str, default=None,
                       help='输出JSON结果路径 (可选)')
    parser.add_argument('--patterns', type=str, nargs='+', default=['**/*.md'],
                       help='包含的文件模式 (默认: **/*.md)')
    parser.add_argument('--exclude', '-e', type=str, nargs='+', default=[],
                       help='额外排除的域名模式')
    parser.add_argument('--timeout', '-t', type=int, default=30,
                       help='请求超时时间(秒) (默认: 30)')
    parser.add_argument('--retries', '-r', type=int, default=3,
                       help='重试次数 (默认: 3)')
    parser.add_argument('--concurrent', type=int, default=50,
                       help='最大并发数 (默认: 50)')
    parser.add_argument('--no-resume', action='store_true',
                       help='不从断点续查，重新开始')
    parser.add_argument('--clear-cache', action='store_true',
                       help='清除缓存后运行')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='启用详细日志输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    base_path = Path(args.path).resolve()
    config_path = Path(args.config)
    
    # 如果配置文件是相对路径，在脚本目录中查找
    if not config_path.is_absolute():
        script_dir = Path(__file__).parent
        config_path = script_dir / config_path
    
    config = load_config(config_path)
    
    # 命令行参数覆盖配置
    if args.timeout:
        config['timeout']['total'] = args.timeout
    if args.retries:
        config['retry']['max_retries'] = args.retries
    if args.concurrent:
        config['max_concurrent'] = args.concurrent
    if args.exclude:
        config['exclude'].extend(args.exclude)
    
    # 清除缓存
    if args.clear_cache:
        cache_dir = Path(config.get('cache', {}).get('cache_dir', '.link-checker-cache'))
        if cache_dir.exists():
            import shutil
            shutil.rmtree(cache_dir)
            logger.info(f"已清除缓存: {cache_dir}")
    
    logger.info(f"开始链接检查...")
    logger.info(f"基础路径: {base_path}")
    logger.info(f"配置文件: {config_path}")
    
    async with LinkChecker(config) as checker:
        results, summary = await checker.run(
            base_path, 
            args.patterns,
            resume=not args.no_resume
        )
        
        # 保存Markdown报告
        report_path = Path(args.output)
        checker.generate_markdown_report(report_path)
        
        # 保存JSON结果
        if args.json:
            checker.save_results(Path(args.json))
    
    # 输出总结
    print("\n" + "="*60)
    print("链接检查完成")
    print("="*60)
    print(f"总文件数: {summary.total_files}")
    print(f"总链接数: {summary.total_links}")
    print(f"✅ 正常: {summary.valid_links}")
    print(f"⚠️ 警告: {summary.warning_links}")
    print(f"❌ 错误: {summary.broken_links}")
    if summary.cached_results > 0:
        print(f"📦 缓存: {summary.cached_results}")
    print(f"耗时: {summary.check_duration:.2f} 秒")
    print("="*60)
    
    # 如果有失效链接，返回非零退出码
    if summary.broken_links > 0:
        print(f"\n⚠️ 发现 {summary.broken_links} 个失效链接!")
        return 1
    
    print("\n✅ 所有链接检查通过!")
    return 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
