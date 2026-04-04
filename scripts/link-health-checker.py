#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
链接健康检查器 v3.0 - 外部链接健康检查自动化系统

功能:
- 扫描所有.md文件中的外部链接
- 异步HTTP请求检查链接状态
- 分类：正常/失效/重定向/超时
- 生成报告 reports/link-health-report.md
- 支持断点续查和缓存机制

作者: AnalysisDataFlow 项目
版本: 3.0.0
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
        logging.FileHandler('link-health-checker.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class LinkCheckResult:
    """链接检查结果数据类"""
    url: str
    source_file: str
    line_number: int
    link_text: str = ""
    link_type: str = 'external'  # 'external', 'redirect', 'broken', 'timeout'
    status_code: Optional[int] = None
    is_valid: bool = False
    error_message: Optional[str] = None
    response_time: float = 0.0
    redirect_url: Optional[str] = None
    final_url: Optional[str] = None
    checked_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def get_status_category(self) -> str:
        """获取状态分类: success/redirect/timeout/error"""
        if self.status_code and 200 <= self.status_code < 300:
            return "success"
        elif self.status_code and 300 <= self.status_code < 400:
            return "redirect"
        elif self.error_message and "超时" in self.error_message:
            return "timeout"
        return "error"


@dataclass
class CheckSummary:
    """检查汇总数据类"""
    total_files: int = 0
    total_links: int = 0
    valid_links: int = 0
    redirect_links: int = 0
    broken_links: int = 0
    timeout_links: int = 0
    skipped_links: int = 0
    check_duration: float = 0.0
    started_at: str = ""
    completed_at: str = ""
    cached_results: int = 0


class LinkCache:
    """链接检查结果缓存管理器"""
    
    def __init__(self, cache_dir: Path, ttl_hours: int = 24):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        self.cache_file = self.cache_dir / "health_check_cache.pkl"
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


class LinkExtractor:
    """Markdown链接提取器"""
    
    MARKDOWN_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^\s\)]+)(?:\s+"[^"]*")?\)')
    HTML_LINK_PATTERN = re.compile(r'<a[^>]+href=["\']([^"\'>]+)["\'][^>]*>', re.IGNORECASE)
    REFERENCE_DEF_PATTERN = re.compile(r'^\[([^\]]+)\]:\s*(\S+)')
    AUTO_LINK_PATTERN = re.compile(r'<([a-zA-Z][a-zA-Z0-9+.-]*:[^>]+)>')
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
    
    def extract_external_links(self, file_path: Path) -> List[Tuple[str, str, int]]:
        """从Markdown文件中提取外部链接，返回 (url, text, line_number)"""
        links = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            in_code_block = False
            
            # 收集引用定义
            references = {}
            for line_num, line in enumerate(lines, 1):
                ref_match = self.REFERENCE_DEF_PATTERN.match(line)
                if ref_match:
                    ref_name = ref_match.group(1)
                    ref_url = ref_match.group(2)
                    if ref_url.startswith(('http://', 'https://')):
                        references[ref_name] = (ref_url, line_num)
            
            for line_num, line in enumerate(lines, 1):
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue
                
                if in_code_block:
                    continue
                
                line_without_inline_code = re.sub(r'`[^`]*`', '', line)
                
                # 提取Markdown链接
                for match in self.MARKDOWN_LINK_PATTERN.finditer(line_without_inline_code):
                    text = match.group(1)
                    url = match.group(2)
                    if url.startswith(('http://', 'https://')):
                        links.append((url, text, line_num))
                
                # 提取HTML链接
                for match in self.HTML_LINK_PATTERN.finditer(line_without_inline_code):
                    url = match.group(1)
                    if url.startswith(('http://', 'https://')):
                        links.append((url, "", line_num))
                
                # 提取自动链接
                for match in self.AUTO_LINK_PATTERN.finditer(line_without_inline_code):
                    url = match.group(1)
                    if url.startswith(('http://', 'https://')):
                        links.append((url, "", line_num))
                        
        except Exception as e:
            logger.error(f"提取链接时出错 {file_path}: {e}")
            
        return links


class ExternalLinkChecker:
    """外部链接检查器核心类"""

    # 排除的URL模式
    EXCLUDE_PATTERNS = [
        r'^https?://localhost',
        r'^https?://127\.',
        r'^https?://192\.168\.',
        r'^https?://10\.',
        r'^https?://172\.(1[6-9]|2[0-9]|3[01])\.',
        r'^https?://example\.com',
        r'^https?://www\.example\.com',
        r'^https?://your-domain\.com',
        r'^https?://your-api\.com',
        r'^https?://api\.example\.com',
        r'^https?://docs\.example\.com',
        r'^https?://doi\.org',
        r'^https?://scholar\.google\.com',
        r'^https?://patents\.google\.com',
        r'^https?://linkedin\.com',
        r'^https?://.*\.linkedin\.com',
        r'^https?://facebook\.com',
        r'^https?://.*\.facebook\.com',
        r'^https?://twitter\.com',
        r'^https?://x\.com',
        r'^https?://.*\.twitter\.com',
        r'github\.com/[^/]+/[^/]+/edit/',
    ]

    def __init__(self, timeout: int = 30, max_concurrent: int = 50, 
                 retries: int = 3, cache_enabled: bool = True):
        self.timeout = timeout
        self.max_concurrent = max_concurrent
        self.retries = retries
        self.cache_enabled = cache_enabled
        self.session: Optional[ClientSession] = None
        self.cache: Optional[LinkCache] = None
        self.results: List[LinkCheckResult] = []
        self.summary = CheckSummary()
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        timeout_config = ClientTimeout(total=self.timeout, connect=10)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 (LinkHealthChecker/3.0.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
        }
        
        connector = aiohttp.TCPConnector(
            limit=self.max_concurrent,
            limit_per_host=10,
            enable_cleanup_closed=True,
            force_close=True,
        )
        
        self.session = ClientSession(
            timeout=timeout_config,
            headers=headers,
            connector=connector
        )
        
        if self.cache_enabled:
            cache_dir = Path('.link-checker-cache')
            self.cache = LinkCache(cache_dir, ttl_hours=24)
        
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
        if self.cache:
            self.cache.save_cache()

    def _is_excluded(self, url: str) -> bool:
        """检查URL是否在排除列表中"""
        for pattern in self.EXCLUDE_PATTERNS:
            if re.search(pattern, url, re.IGNORECASE):
                return True
        return False

    async def check_url(self, url: str, link_text: str = "", 
                        source_file: str = "", line_number: int = 0) -> LinkCheckResult:
        """检查单个URL"""
        result = LinkCheckResult(
            url=url,
            source_file=source_file,
            line_number=line_number,
            link_text=link_text,
            link_type='external'
        )
        
        if self._is_excluded(url):
            result.is_valid = True
            result.error_message = "URL在排除列表中"
            self.summary.skipped_links += 1
            return result
        
        # 检查缓存
        if self.cache:
            cached = self.cache.get(url)
            if cached:
                self.summary.cached_results += 1
                return cached
        
        # 执行检查
        for attempt in range(self.retries):
            try:
                start_time = time.time()
                
                # 首先尝试HEAD请求
                try:
                    async with self.session.head(url, allow_redirects=True, ssl=False) as response:
                        result.response_time = time.time() - start_time
                        result.status_code = response.status
                        
                        if response.history:
                            result.redirect_url = str(response.url)
                        
                        if 200 <= response.status < 300:
                            result.is_valid = True
                            result.link_type = 'external'
                            break
                        elif response.status in [405, 501]:
                            raise aiohttp.ClientError("HEAD not allowed")
                        elif 300 <= response.status < 400:
                            result.is_valid = True
                            result.link_type = 'redirect'
                            result.final_url = str(response.url)
                            break
                        else:
                            # 需要GET请求确认
                            raise aiohttp.ClientError(f"HEAD returned {response.status}")
                            
                except (aiohttp.ClientError, asyncio.TimeoutError):
                    pass
                
                # 使用GET请求
                async with self.session.get(url, allow_redirects=True, ssl=False) as response:
                    result.response_time = time.time() - start_time
                    result.status_code = response.status
                    
                    if response.history:
                        result.redirect_url = str(response.url)
                    
                    if 200 <= response.status < 300:
                        result.is_valid = True
                        result.link_type = 'external'
                    elif 300 <= response.status < 400:
                        result.is_valid = True
                        result.link_type = 'redirect'
                        result.final_url = str(response.url)
                    elif 400 <= response.status < 500:
                        result.is_valid = False
                        result.link_type = 'broken'
                        result.error_message = f"客户端错误: HTTP {response.status}"
                    else:
                        result.is_valid = False
                        result.link_type = 'broken'
                        result.error_message = f"服务器错误: HTTP {response.status}"
                    break
                    
            except asyncio.TimeoutError:
                result.error_message = f"请求超时 (尝试 {attempt + 1}/{self.retries})"
                result.link_type = 'timeout'
                if attempt < self.retries - 1:
                    await asyncio.sleep(1 * (attempt + 1))
                    continue
                result.is_valid = False
                    
            except ClientError as e:
                result.error_message = f"客户端错误: {str(e)}"
                result.link_type = 'broken'
                if attempt < self.retries - 1:
                    await asyncio.sleep(1 * (attempt + 1))
                    continue
                result.is_valid = False
                    
            except Exception as e:
                result.error_message = f"未知错误: {str(e)}"
                result.link_type = 'broken'
                result.is_valid = False
                break
        
        # 保存到缓存
        if self.cache:
            self.cache.set(url, result)
        
        return result

    async def check_file(self, file_path: Path, base_path: Path) -> List[LinkCheckResult]:
        """检查单个文件中的所有外部链接"""
        extractor = LinkExtractor(base_path)
        links = extractor.extract_external_links(file_path)
        
        logger.info(f"检查文件: {file_path.name} ({len(links)} 个外部链接)")
        
        results = []
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def check_with_limit(url, text, line_num):
            async with semaphore:
                result = await self.check_url(
                    url, 
                    link_text=text,
                    source_file=str(file_path.relative_to(base_path)),
                    line_number=line_num
                )
                # 添加延迟避免请求过快
                await asyncio.sleep(0.1)
                return result
        
        if links:
            tasks = [check_with_limit(url, text, line_num) for url, text, line_num in links]
            results = await asyncio.gather(*tasks)
        
        return results

    async def run(self, base_path: Path, include_patterns: List[str] = None) -> Tuple[List[LinkCheckResult], CheckSummary]:
        """运行链接检查"""
        self.summary.started_at = datetime.now().isoformat()
        start_time = time.time()
        
        # 查找所有Markdown文件
        md_files = []
        for pattern in (include_patterns or ['**/*.md']):
            md_files.extend(base_path.glob(pattern))
        
        # 过滤隐藏目录和排除路径
        md_files = [
            f for f in md_files 
            if not any(part.startswith('.') or part in ['node_modules', '__pycache__'] 
                      for part in f.parts)
        ]
        
        # 去重
        seen = set()
        md_files = [f for f in md_files if not (f in seen or seen.add(f))]
        
        self.summary.total_files = len(md_files)
        logger.info(f"找到 {len(md_files)} 个Markdown文件")
        
        # 处理所有文件
        all_results = []
        batch_size = 10
        
        for i in range(0, len(md_files), batch_size):
            batch = md_files[i:i + batch_size]
            batch_results = await asyncio.gather(*[
                self.check_file(f, base_path) for f in batch
            ])
            for results in batch_results:
                all_results.extend(results)
            
            logger.info(f"进度: {min(i + batch_size, len(md_files))}/{len(md_files)} 文件")
        
        self.results = all_results
        self.summary.total_links = len(all_results)
        
        # 统计结果
        for result in all_results:
            cat = result.get_status_category()
            if cat == 'success':
                self.summary.valid_links += 1
            elif cat == 'redirect':
                self.summary.redirect_links += 1
            elif cat == 'timeout':
                self.summary.timeout_links += 1
            else:
                self.summary.broken_links += 1
        
        self.summary.check_duration = time.time() - start_time
        self.summary.completed_at = datetime.now().isoformat()
        
        logger.info(f"检查完成: {self.summary.total_links} 个链接, "
                   f"{self.summary.valid_links} 正常, "
                   f"{self.summary.redirect_links} 重定向, "
                   f"{self.summary.timeout_links} 超时, "
                   f"{self.summary.broken_links} 失效")
        
        return all_results, self.summary

    def generate_markdown_report(self, output_path: Path):
        """生成Markdown格式健康报告"""
        report_lines = []
        now = datetime.now()
        
        # 标题
        report_lines.append("# 外部链接健康检查报告\n")
        report_lines.append(f"**生成时间:** {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_lines.append(f"**报告周期:** 月度检查\n")
        report_lines.append(f"**状态:** {'✅ 健康' if self.summary.broken_links == 0 else '⚠️ 需要关注'}\n")
        
        # 执行摘要
        report_lines.append("## 📊 执行摘要\n")
        report_lines.append("| 指标 | 数值 | 状态 |")
        report_lines.append("|------|------|------|")
        report_lines.append(f"| 扫描文件数 | {self.summary.total_files} | - |")
        report_lines.append(f"| 检查外部链接总数 | {self.summary.total_links} | - |")
        report_lines.append(f"| ✅ 正常链接 | {self.summary.valid_links} | {'✅' if self.summary.valid_links > 0 else '-'} |")
        report_lines.append(f"| 🔄 重定向链接 | {self.summary.redirect_links} | {'⚠️' if self.summary.redirect_links > 0 else '✅'} |")
        report_lines.append(f"| ⏱️ 超时链接 | {self.summary.timeout_links} | {'⚠️' if self.summary.timeout_links > 0 else '✅'} |")
        report_lines.append(f"| ❌ 失效链接 | {self.summary.broken_links} | {'❌' if self.summary.broken_links > 0 else '✅'} |")
        report_lines.append(f"| 📦 缓存命中 | {self.summary.cached_results} | - |")
        report_lines.append(f"| 检查耗时 | {self.summary.check_duration:.2f} 秒 | - |")
        report_lines.append("")
        
        # 健康状态概览
        total_checkable = self.summary.total_links - self.summary.skipped_links
        health_rate = (self.summary.valid_links / total_checkable * 100) if total_checkable > 0 else 0
        
        report_lines.append("## 🏥 健康状态概览\n")
        report_lines.append(f"```")
        report_lines.append(f"总体健康度: {health_rate:.1f}%")
        report_lines.append(f"[{'█' * int(health_rate/5)}{'░' * (20-int(health_rate/5))}]")
        report_lines.append(f"```\n")
        
        # 失效链接详情
        broken_results = [r for r in self.results if r.get_status_category() == 'error']
        if broken_results:
            report_lines.append(f"## ❌ 失效链接 ({len(broken_results)} 个)\n")
            report_lines.append("| 文件 | 行号 | 链接文本 | 链接 | 状态码 | 错误信息 |")
            report_lines.append("|------|------|----------|------|--------|----------|")
            for result in broken_results:
                status = result.status_code or "N/A"
                text_short = result.link_text[:20] + "..." if len(result.link_text) > 20 else result.link_text
                url_short = result.url[:50] + "..." if len(result.url) > 50 else result.url
                error_msg = result.error_message[:40] + "..." if len(result.error_message) > 40 else result.error_message
                report_lines.append(f"| `{result.source_file}` | {result.line_number} | {text_short} | [{url_short}]({result.url}) | {status} | {error_msg} |")
            report_lines.append("")
        
        # 重定向链接详情（可自动修复）
        redirect_results = [r for r in self.results if r.get_status_category() == 'redirect']
        if redirect_results:
            report_lines.append(f"## 🔄 重定向链接 ({len(redirect_results)} 个 - 可自动修复)\n")
            report_lines.append("| 文件 | 行号 | 原链接 | 重定向目标 |")
            report_lines.append("|------|------|--------|------------|")
            for result in redirect_results:
                url_short = result.url[:40] + "..." if len(result.url) > 40 else result.url
                redirect_short = (result.final_url or result.redirect_url or "")[:40] + "..." if len(result.final_url or result.redirect_url or "") > 40 else (result.final_url or result.redirect_url or "")
                report_lines.append(f"| `{result.source_file}` | {result.line_number} | [{url_short}]({result.url}) | {redirect_short} |")
            report_lines.append("")
            report_lines.append("**修复命令:**\n")
            report_lines.append("```bash")
            report_lines.append("python scripts/link-auto-fix.py --fix-redirects")
            report_lines.append("```\n")
        
        # 超时链接详情
        timeout_results = [r for r in self.results if r.get_status_category() == 'timeout']
        if timeout_results:
            report_lines.append(f"## ⏱️ 超时链接 ({len(timeout_results)} 个 - 需手动检查)\n")
            report_lines.append("| 文件 | 行号 | 链接 | 错误信息 |")
            report_lines.append("|------|------|------|----------|")
            for result in timeout_results:
                url_short = result.url[:60] + "..." if len(result.url) > 60 else result.url
                report_lines.append(f"| `{result.source_file}` | {result.line_number} | [{url_short}]({result.url}) | {result.error_message} |")
            report_lines.append("")
        
        # 按文件统计
        report_lines.append("## 📁 按文件统计\n")
        file_stats = defaultdict(lambda: {'total': 0, 'success': 0, 'redirect': 0, 'timeout': 0, 'error': 0})
        for result in self.results:
            file_path = result.source_file
            file_stats[file_path]['total'] += 1
            cat = result.get_status_category()
            file_stats[file_path][cat] += 1
        
        # 只显示有问题的文件
        problematic_files = {k: v for k, v in file_stats.items() if v['error'] > 0 or v['timeout'] > 0}
        if problematic_files:
            report_lines.append("### 需要关注的文件\n")
            report_lines.append("| 文件 | 总数 | ✅ 正常 | 🔄 重定向 | ⏱️ 超时 | ❌ 错误 |")
            report_lines.append("|------|------|---------|-----------|---------|--------|")
            for file_path, stats in sorted(problematic_files.items()):
                report_lines.append(f"| `{file_path}` | {stats['total']} | {stats['success']} | {stats['redirect']} | {stats['timeout']} | {stats['error']} |")
            report_lines.append("")
        
        # 建议操作
        report_lines.append("## 🛠️ 建议操作\n")
        
        if broken_results:
            report_lines.append("### 高优先级 - 失效链接修复\n")
            report_lines.append("以下链接已确认失效，需要手动修复或替换:\n")
            for result in broken_results[:10]:
                report_lines.append(f"- `{result.source_file}:{result.line_number}` - [{result.url}]({result.url})")
                report_lines.append(f"  - 错误: {result.error_message}")
            if len(broken_results) > 10:
                report_lines.append(f"- ... 还有 {len(broken_results) - 10} 个失效链接")
            report_lines.append("")
            report_lines.append("**手动修复命令:**\n")
            report_lines.append("```bash")
            report_lines.append("python scripts/link-quick-fix.py --file <文件名> --line <行号> --new-url <新URL>")
            report_lines.append("```\n")
        
        if redirect_results:
            report_lines.append("### 中优先级 - 重定向链接更新\n")
            report_lines.append("以下链接有重定向，建议更新为最终URL:\n")
            report_lines.append("```bash")
            report_lines.append("# 自动修复所有重定向链接")
            report_lines.append("python scripts/link-auto-fix.py --fix-redirects")
            report_lines.append("")
            report_lines.append("# 查看重定向详情")
            report_lines.append("python scripts/link-auto-fix.py --list-redirects")
            report_lines.append("```\n")
        
        if not broken_results and not redirect_results and not timeout_results:
            report_lines.append("✅ **所有外部链接状态良好，无需操作**\n")
        
        # 历史趋势（占位）
        report_lines.append("## 📈 历史趋势\n")
        report_lines.append("```")
        report_lines.append("失效链接趋势: 待首次月度检查完成后生成")
        report_lines.append("```\n")
        
        # 页脚
        report_lines.append("---\n")
        report_lines.append("*本报告由链接健康检查自动化系统生成*\n")
        report_lines.append("*下次检查时间: 每月1日自动执行*\n")
        
        # 写入文件
        output_path.parent.mkdir(parents=True, exist_ok=True)
        report_content = "\n".join(report_lines)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        logger.info(f"健康报告已保存到: {output_path}")
        return report_content

    def save_json_results(self, output_path: Path):
        """保存JSON格式结果"""
        data = {
            'summary': asdict(self.summary),
            'results': [asdict(r) for r in self.results]
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"JSON结果已保存到: {output_path}")


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='外部链接健康检查器 v3.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本使用（扫描当前目录）
  %(prog)s
  
  # 指定目录和输出
  %(prog)s --path ./docs --output reports/link-health-report.md
  
  # 同时生成JSON结果
  %(prog)s --json reports/link-health-results.json
  
  # 快速模式（减少重试次数）
  %(prog)s --retries 1 --timeout 15
  
  # 清除缓存后运行
  %(prog)s --clear-cache
        """
    )
    
    parser.add_argument('--path', '-p', type=str, default='.',
                       help='要扫描的基础目录路径 (默认: 当前目录)')
    parser.add_argument('--output', '-o', type=str, 
                       default='reports/link-health-report.md',
                       help='输出Markdown报告路径 (默认: reports/link-health-report.md)')
    parser.add_argument('--json', '-j', type=str, 
                       default='reports/link-health-results.json',
                       help='输出JSON结果路径 (默认: reports/link-health-results.json)')
    parser.add_argument('--timeout', '-t', type=int, default=30,
                       help='请求超时时间(秒) (默认: 30)')
    parser.add_argument('--retries', '-r', type=int, default=3,
                       help='重试次数 (默认: 3)')
    parser.add_argument('--concurrent', '-c', type=int, default=50,
                       help='最大并发数 (默认: 50)')
    parser.add_argument('--no-cache', action='store_true',
                       help='禁用缓存')
    parser.add_argument('--clear-cache', action='store_true',
                       help='清除缓存后运行')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='启用详细日志输出')
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    base_path = Path(args.path).resolve()
    
    # 清除缓存
    if args.clear_cache:
        cache_dir = Path('.link-checker-cache')
        if cache_dir.exists():
            import shutil
            shutil.rmtree(cache_dir)
            logger.info(f"已清除缓存: {cache_dir}")
    
    logger.info(f"开始链接健康检查...")
    logger.info(f"基础路径: {base_path}")
    
    async with ExternalLinkChecker(
        timeout=args.timeout,
        max_concurrent=args.concurrent,
        retries=args.retries,
        cache_enabled=not args.no_cache
    ) as checker:
        results, summary = await checker.run(base_path)
        
        # 生成报告
        report_path = Path(args.output)
        checker.generate_markdown_report(report_path)
        
        # 保存JSON结果
        if args.json:
            checker.save_json_results(Path(args.json))
    
    # 输出总结
    print("\n" + "="*70)
    print("外部链接健康检查完成")
    print("="*70)
    print(f"总文件数: {summary.total_files}")
    print(f"总链接数: {summary.total_links}")
    print(f"✅ 正常: {summary.valid_links}")
    print(f"🔄 重定向: {summary.redirect_links}")
    print(f"⏱️ 超时: {summary.timeout_links}")
    print(f"❌ 失效: {summary.broken_links}")
    if summary.cached_results > 0:
        print(f"📦 缓存: {summary.cached_results}")
    print(f"耗时: {summary.check_duration:.2f} 秒")
    print(f"报告: {args.output}")
    print("="*70)
    
    # 返回退出码
    if summary.broken_links > 5:
        print(f"\n⚠️ 发现 {summary.broken_links} 个失效链接，超过阈值(5)!")
        return 2
    elif summary.broken_links > 0:
        print(f"\n⚠️ 发现 {summary.broken_links} 个失效链接")
        return 1
    
    print("\n✅ 所有外部链接检查通过!")
    return 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))
