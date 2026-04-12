#!/usr/bin/env python3
"""
外部链接健康检测工具 - Link Health Checker v4.1 (Q1-3)
检测项目中的所有外部链接，标记失效链接并提供修复建议

Author: AnalysisDataFlow Project
Version: 4.1.0
Date: 2026-04-12
"""

import asyncio
import aiohttp
import re
import json
import pickle
import hashlib
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set, Tuple
from urllib.parse import urlparse, urljoin, quote
from collections import defaultdict
import time
import argparse


@dataclass
class LinkStatus:
    """链接状态数据类"""
    url: str
    status_code: Optional[int] = None
    is_accessible: bool = False
    redirect_url: Optional[str] = None
    error_message: Optional[str] = None
    response_time_ms: float = 0.0
    source_files: List[str] = None
    check_time: str = ""
    archive_url: Optional[str] = None
    category: str = ""  # 分类: ok, redirect, not_found, timeout, ssl_error, other
    
    def __post_init__(self):
        if self.source_files is None:
            self.source_files = []
        if not self.check_time:
            self.check_time = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return asdict(self)


class LinkHealthChecker:
    """外部链接健康检测器 v4.1"""
    
    # 用户代理列表（轮换使用）
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.0',
    ]
    
    def __init__(self, 
                 cache_file: str = ".scripts/.link_health_cache_v4.1.pkl",
                 cache_ttl_hours: int = 24,
                 concurrent_limit: int = 20,
                 delay_seconds: float = 0.2,
                 timeout_seconds: int = 15):
        self.cache_file = Path(cache_file)
        self.cache_ttl = timedelta(hours=cache_ttl_hours)
        self.concurrent_limit = concurrent_limit
        self.delay_seconds = delay_seconds
        self.timeout_seconds = timeout_seconds
        self.cache: Dict[str, LinkStatus] = {}
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore: Optional[asyncio.Semaphore] = None
        
    def is_external_link(self, url: str) -> bool:
        """判断是否为外部链接"""
        if not url or url.startswith('#') or url.startswith('./') or url.startswith('../'):
            return False
        if url.startswith('http://') or url.startswith('https://'):
            return True
        return False
    
    def normalize_url(self, url: str) -> str:
        """规范化URL"""
        url = url.split('#')[0]
        if url.endswith('/') and not url.count('/') <= 3:
            url = url.rstrip('/')
        return url
    
    async def init_session(self):
        """初始化HTTP会话"""
        if self.session is None:
            connector = aiohttp.TCPConnector(
                limit=self.concurrent_limit * 2,
                limit_per_host=self.concurrent_limit,
                enable_cleanup_closed=True,
                force_close=True,
            )
            timeout = aiohttp.ClientTimeout(total=self.timeout_seconds, connect=8)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            )
            self.semaphore = asyncio.Semaphore(self.concurrent_limit)
    
    async def close_session(self):
        """关闭HTTP会话"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def check_link(self, url: str, source_files: List[str] = None) -> LinkStatus:
        """检测单个链接"""
        status = LinkStatus(
            url=url,
            source_files=source_files or [],
        )
        
        await self.init_session()
        
        async with self.semaphore:
            start_time = time.time()
            user_agent = self.USER_AGENTS[hash(url) % len(self.USER_AGENTS)]
            
            try:
                headers = {'User-Agent': user_agent}
                
                # 首先尝试HEAD请求
                async with self.session.head(
                    url, 
                    headers=headers, 
                    allow_redirects=False,
                    ssl=False
                ) as response:
                    status.status_code = response.status
                    status.response_time_ms = (time.time() - start_time) * 1000
                    
                    if response.status == 200:
                        status.is_accessible = True
                        status.category = "ok"
                    elif response.status in (301, 302, 307, 308):
                        status.is_accessible = True
                        status.category = "redirect"
                        if 'Location' in response.headers:
                            status.redirect_url = response.headers['Location']
                    elif response.status == 404:
                        status.is_accessible = False
                        status.category = "not_found"
                        status.error_message = f"HTTP 404 Not Found"
                    elif response.status == 403:
                        status.is_accessible = False
                        status.category = "forbidden"
                        status.error_message = f"HTTP 403 Forbidden"
                    elif response.status == 405:
                        # 方法不允许，尝试GET请求
                        async with self.session.get(
                            url, 
                            headers=headers, 
                            allow_redirects=True,
                            ssl=False
                        ) as get_response:
                            status.status_code = get_response.status
                            status.response_time_ms = (time.time() - start_time) * 1000
                            status.is_accessible = 200 <= get_response.status < 400
                            if status.is_accessible:
                                status.category = "ok"
                            elif get_response.status == 404:
                                status.category = "not_found"
                            else:
                                status.category = "other"
                            if get_response.history:
                                status.redirect_url = str(get_response.url)
                                status.category = "redirect"
                    elif 400 <= response.status < 500:
                        status.is_accessible = False
                        status.category = "client_error"
                        status.error_message = f"HTTP {response.status}"
                    elif 500 <= response.status < 600:
                        status.is_accessible = False
                        status.category = "server_error"
                        status.error_message = f"HTTP {response.status}"
                    else:
                        status.is_accessible = 200 <= response.status < 400
                        status.category = "ok" if status.is_accessible else "other"
                        if not status.is_accessible:
                            status.error_message = f"HTTP {response.status}"
                        
            except asyncio.TimeoutError:
                status.error_message = "Timeout"
                status.category = "timeout"
                status.response_time_ms = self.timeout_seconds * 1000
            except aiohttp.ClientSSLError as e:
                status.error_message = f"SSL Error: {str(e)[:50]}"
                status.category = "ssl_error"
                status.response_time_ms = (time.time() - start_time) * 1000
            except aiohttp.ClientError as e:
                status.error_message = f"Connection Error: {str(e)[:50]}"
                status.category = "connection_error"
                status.response_time_ms = (time.time() - start_time) * 1000
            except Exception as e:
                status.error_message = f"Error: {str(e)[:50]}"
                status.category = "other"
                status.response_time_ms = (time.time() - start_time) * 1000
        
        # 延迟避免限流
        await asyncio.sleep(self.delay_seconds)
        
        return status
    
    async def check_batch(self, urls: List[Tuple[str, List[str]]]) -> List[LinkStatus]:
        """批量检测链接"""
        await self.init_session()
        
        results = []
        total = len(urls)
        
        for i, (url, files) in enumerate(urls, 1):
            print(f"🔍 [{i}/{total}] Checking: {url[:80]}...")
            result = await self.check_link(url, files)
            results.append(result)
            
            # 状态显示
            if result.is_accessible:
                if result.redirect_url:
                    print(f"   🔄 {result.status_code} -> Redirect")
                else:
                    print(f"   ✅ {result.status_code} OK ({result.response_time_ms:.0f}ms)")
            else:
                print(f"   ❌ {result.error_message}")
        
        return results
    
    def extract_links_from_file(self, file_path: Path) -> Set[str]:
        """从Markdown文件中提取外部链接"""
        links = set()
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 匹配Markdown链接 [text](url)
            md_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            for match in re.finditer(md_pattern, content):
                url = match.group(2).strip()
                if self.is_external_link(url):
                    links.add(self.normalize_url(url))
            
            # 匹配引用式链接定义 [ref]: url
            ref_def_pattern = r'^\[([^\]]+)\]:\s*(\S+)'
            for match in re.finditer(ref_def_pattern, content, re.MULTILINE):
                url = match.group(2).strip()
                if self.is_external_link(url):
                    links.add(self.normalize_url(url))
            
            # 匹配裸URL <http://...>
            bare_url_pattern = r'<(https?://[^>]+)>'
            for match in re.finditer(bare_url_pattern, content):
                url = match.group(1).strip()
                links.add(self.normalize_url(url))
                
        except Exception as e:
            print(f"⚠️ Failed to read file {file_path}: {e}")
        
        return links
    
    def extract_all_links(self, root_dir: Path, include_dirs: List[str] = None) -> Dict[str, List[str]]:
        """从项目中提取所有外部链接"""
        url_to_files: Dict[str, List[str]] = {}
        
        if include_dirs is None:
            include_dirs = ['.', 'Struct', 'Knowledge', 'Flink', 'docs', 'tutorials', 'en', 'visuals', 'LEARNING-PATHS', 'i18n']
        
        md_files = []
        for dir_name in include_dirs:
            dir_path = root_dir / dir_name
            if dir_path.exists():
                md_files.extend(dir_path.rglob('*.md'))
        
        md_files = list(set(md_files))
        md_files = [f for f in md_files if 'node_modules' not in str(f) and '.git' not in str(f)]
        
        print(f"📄 Found {len(md_files)} Markdown files")
        
        for md_file in md_files:
            links = self.extract_links_from_file(md_file)
            relative_path = str(md_file.relative_to(root_dir)).replace('\\', '/')
            for link in links:
                if link not in url_to_files:
                    url_to_files[link] = []
                if relative_path not in url_to_files[link]:
                    url_to_files[link].append(relative_path)
        
        return url_to_files
    
    def get_wayback_url(self, url: str) -> str:
        """获取Wayback Machine存档链接"""
        return f"https://web.archive.org/web/*/{url}"
    
    def generate_report(self, results: List[LinkStatus], output_file: str = "EXTERNAL-LINK-HEALTH-REPORT-v4.1.md") -> str:
        """生成检测报告"""
        total = len(results)
        
        # 分类统计
        ok_links = [r for r in results if r.category == "ok"]
        redirect_links = [r for r in results if r.category == "redirect"]
        not_found_links = [r for r in results if r.category == "not_found"]
        timeout_links = [r for r in results if r.category == "timeout"]
        ssl_error_links = [r for r in results if r.category == "ssl_error"]
        forbidden_links = [r for r in results if r.category == "forbidden"]
        client_error_links = [r for r in results if r.category == "client_error"]
        server_error_links = [r for r in results if r.category == "server_error"]
        other_error_links = [r for r in results if r.category in ("other", "connection_error")]
        
        failed_links = [r for r in results if not r.is_accessible]
        
        # 统计来源文档数量
        all_files = set()
        for r in results:
            all_files.update(r.source_files)
        
        report_lines = [
            "# 外部链接健康检测报告 v4.1",
            "",
            f"**检测时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**检测文档总数**: {len(all_files)}",
            f"**外部链接总数**: {total}",
            "",
            "## 📊 检测统计",
            "",
            "### 总体统计",
            "",
            "| 类别 | 数量 | 百分比 | 状态 |",
            "|------|------|--------|------|",
            f"| 总链接数 | {total} | 100% | - |",
            f"| 有效链接 (200 OK) | {len(ok_links)} | {len(ok_links)/total*100:.1f}% | ✅ |" if total > 0 else "| 有效链接 (200 OK) | 0 | 0% | ✅ |",
            f"| 重定向链接 (301/302) | {len(redirect_links)} | {len(redirect_links)/total*100:.1f}% | 🔄 |" if total > 0 else "| 重定向链接 (301/302) | 0 | 0% | 🔄 |",
            f"| 失效链接 | {len(failed_links)} | {len(failed_links)/total*100:.1f}% | ❌ |" if total > 0 else "| 失效链接 | 0 | 0% | ❌ |",
            "",
            "### 问题链接分类统计",
            "",
            "| 问题类型 | 数量 | 百分比 | 说明 |",
            "|----------|------|--------|------|",
            f"| 404 Not Found | {len(not_found_links)} | {len(not_found_links)/total*100:.1f}% | 页面不存在 |",
            f"| Timeout | {len(timeout_links)} | {len(timeout_links)/total*100:.1f}% | 连接超时 |",
            f"| SSL Error | {len(ssl_error_links)} | {len(ssl_error_links)/total*100:.1f}% | 证书错误 |",
            f"| 403 Forbidden | {len(forbidden_links)} | {len(forbidden_links)/total*100:.1f}% | 访问被拒绝 |",
            f"| Client Error (4xx) | {len(client_error_links)} | {len(client_error_links)/total*100:.1f}% | 其他客户端错误 |",
            f"| Server Error (5xx) | {len(server_error_links)} | {len(server_error_links)/total*100:.1f}% | 服务器错误 |",
            f"| Connection Error | {len(other_error_links)} | {len(other_error_links)/total*100:.1f}% | 连接错误 |",
            "",
        ]
        
        # 重定向链接列表
        if redirect_links:
            report_lines.extend([
                "## 🔄 重定向链接列表 (301/302)",
                "",
                "> 建议：更新为最终目标URL",
                "",
                "| 原链接 | 重定向目标 | 来源文档 |",
                "|--------|------------|----------|",
            ])
            for r in sorted(redirect_links, key=lambda x: x.url)[:30]:
                files = ", ".join(r.source_files[:2]) + ("..." if len(r.source_files) > 2 else "")
                url_display = r.url[:50] + "..." if len(r.url) > 50 else r.url
                redirect_display = r.redirect_url[:50] + "..." if r.redirect_url and len(r.redirect_url) > 50 else (r.redirect_url or "N/A")
                report_lines.append(f"| [{url_display}]({r.url}) | [{redirect_display}]({r.redirect_url}) | {files[:30]} |")
            if len(redirect_links) > 30:
                report_lines.append(f"| ... | ... | *还有 {len(redirect_links) - 30} 个* |")
            report_lines.append("")
        
        # 404 Not Found 列表
        if not_found_links:
            report_lines.extend([
                "## ❌ 404 Not Found 链接",
                "",
                "> 建议：使用 Wayback Machine 获取存档链接或查找替代链接",
                "",
                "| 链接 | 来源文档 | Wayback备份 |",
                "|------|----------|-------------|",
            ])
            for r in sorted(not_found_links, key=lambda x: x.url):
                files = ", ".join(r.source_files[:2])
                url_display = r.url[:60] + "..." if len(r.url) > 60 else r.url
                wayback = self.get_wayback_url(r.url)
                report_lines.append(f"| [{url_display}]({r.url}) | {files[:35]} | [查看]({wayback}) |")
            report_lines.append("")
        
        # Timeout 列表
        if timeout_links:
            report_lines.extend([
                "## ⏱️ 超时链接",
                "",
                "> 建议：可能是暂时性问题，稍后重试或使用替代链接",
                "",
                "| 链接 | 来源文档 | Wayback备份 |",
                "|------|----------|-------------|",
            ])
            for r in sorted(timeout_links, key=lambda x: x.url):
                files = ", ".join(r.source_files[:2])
                url_display = r.url[:60] + "..." if len(r.url) > 60 else r.url
                wayback = self.get_wayback_url(r.url)
                report_lines.append(f"| [{url_display}]({r.url}) | {files[:35]} | [查看]({wayback}) |")
            report_lines.append("")
        
        # SSL Error 列表
        if ssl_error_links:
            report_lines.extend([
                "## 🔒 SSL 错误链接",
                "",
                "> 建议：检查证书问题或使用 HTTP 替代 HTTPS",
                "",
                "| 链接 | 来源文档 | Wayback备份 |",
                "|------|----------|-------------|",
            ])
            for r in sorted(ssl_error_links, key=lambda x: x.url):
                files = ", ".join(r.source_files[:2])
                url_display = r.url[:60] + "..." if len(r.url) > 60 else r.url
                wayback = self.get_wayback_url(r.url)
                report_lines.append(f"| [{url_display}]({r.url}) | {files[:35]} | [查看]({wayback}) |")
            report_lines.append("")
        
        # 其他失效链接
        other_failed = forbidden_links + client_error_links + server_error_links + other_error_links
        if other_failed:
            report_lines.extend([
                "## ⚠️ 其他失效链接",
                "",
                "| 链接 | 错误类型 | 错误信息 | 来源文档 |",
                "|------|----------|----------|----------|",
            ])
            for r in sorted(other_failed, key=lambda x: x.url)[:50]:
                files = ", ".join(r.source_files[:2])
                url_display = r.url[:50] + "..." if len(r.url) > 50 else r.url
                error_type = r.category
                error_msg = (r.error_message or "Unknown")[:30]
                report_lines.append(f"| [{url_display}]({r.url}) | {error_type} | {error_msg} | {files[:25]} |")
            if len(other_failed) > 50:
                report_lines.append(f"| ... | ... | ... | *还有 {len(other_failed) - 50} 个* |")
            report_lines.append("")
        
        # 修复建议
        report_lines.extend([
            "## 🔧 修复建议",
            "",
            "### 自动修复脚本",
            "",
            "运行以下命令自动修复301重定向：",
            "",
            "```bash",
            "python .scripts/fix-external-links.py --mode fix-redirects",
            "```",
            "",
            "### 手动修复指南",
            "",
            "1. **404 Not Found**: 使用 Wayback Machine 获取存档链接",
            "   - 访问: `https://web.archive.org/web/*/{URL}`",
            "   - 或使用工具批量查询",
            "",
            "2. **Timeout**: 可能是暂时性问题，稍后重试",
            "   - 检查链接是否拼写正确",
            "   - 考虑使用替代链接",
            "",
            "3. **SSL Error**: 检查证书问题",
            "   - 尝试使用 HTTP 替代 HTTPS",
            "   - 或更新为正确的 HTTPS 链接",
            "",
            "4. **Redirect (301/302)**: 更新为最终目标URL",
            "   - 使用脚本自动更新",
            "   - 或手动替换链接",
            "",
            "### 已修复链接清单",
            "",
            "| 原链接 | 修复后链接 | 修复方式 | 修复时间 |",
            "|--------|-----------|----------|----------|",
            "| - | - | - | - |",
            "",
            "### 待人工处理链接",
            "",
            "| 链接 | 问题类型 | 来源文档 | 建议操作 |",
            "|------|----------|----------|----------|",
        ])
        
        # 添加待处理链接
        for r in sorted(failed_links, key=lambda x: x.url)[:30]:
            files = ", ".join(r.source_files[:2])
            url_display = r.url[:50] + "..." if len(r.url) > 50 else r.url
            if r.category == "not_found":
                suggestion = "查找Wayback存档或替代链接"
            elif r.category == "timeout":
                suggestion = "稍后重试或寻找替代"
            elif r.category == "ssl_error":
                suggestion = "检查证书或使用HTTP"
            else:
                suggestion = "手动检查"
            report_lines.append(f"| [{url_display}]({r.url}) | {r.category} | {files[:25]} | {suggestion} |")
        
        if len(failed_links) > 30:
            report_lines.append(f"| ... | ... | ... | *还有 {len(failed_links) - 30} 个待处理* |")
        
        report_lines.extend([
            "",
            "## 📈 统计摘要",
            "",
            "```",
            f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"检测文档: {len(all_files)} 个",
            f"外部链接: {total} 个",
            f"  - 有效 (200): {len(ok_links)} 个 ({len(ok_links)/total*100:.1f}%)",
            f"  - 重定向: {len(redirect_links)} 个 ({len(redirect_links)/total*100:.1f}%)",
            f"  - 失效: {len(failed_links)} 个 ({len(failed_links)/total*100:.1f}%)",
            f"    - 404 Not Found: {len(not_found_links)} 个",
            f"    - Timeout: {len(timeout_links)} 个",
            f"    - SSL Error: {len(ssl_error_links)} 个",
            f"    - 403 Forbidden: {len(forbidden_links)} 个",
            f"    - Client Error (4xx): {len(client_error_links)} 个",
            f"    - Server Error (5xx): {len(server_error_links)} 个",
            f"    - Connection Error: {len(other_error_links)} 个",
            "```",
            "",
            "---",
            "",
            "*此报告由 Link Health Checker v4.1 自动生成*",
            "",
            f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        ])
        
        report = "\n".join(report_lines)
        
        # 保存报告
        output_path = Path(output_file)
        output_path.write_text(report, encoding='utf-8')
        print(f"📝 Report saved: {output_file}")
        
        return report
    
    def export_json(self, results: List[LinkStatus], output_file: str = ".scripts/.link_health_results_v4.1.json"):
        """导出结果为JSON格式"""
        data = {
            "check_time": datetime.now().isoformat(),
            "total": len(results),
            "categories": {
                "ok": sum(1 for r in results if r.category == "ok"),
                "redirect": sum(1 for r in results if r.category == "redirect"),
                "not_found": sum(1 for r in results if r.category == "not_found"),
                "timeout": sum(1 for r in results if r.category == "timeout"),
                "ssl_error": sum(1 for r in results if r.category == "ssl_error"),
                "forbidden": sum(1 for r in results if r.category == "forbidden"),
                "client_error": sum(1 for r in results if r.category == "client_error"),
                "server_error": sum(1 for r in results if r.category == "server_error"),
                "other": sum(1 for r in results if r.category in ("other", "connection_error")),
            },
            "results": [r.to_dict() for r in results]
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"📊 JSON results saved: {output_file}")


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='外部链接健康检测工具 v4.1')
    parser.add_argument('--root', default='.', help='项目根目录')
    parser.add_argument('--limit', type=int, default=0, help='限制检测链接数量（0=全部）')
    parser.add_argument('--output', default='EXTERNAL-LINK-HEALTH-REPORT-v4.1.md', help='输出报告文件名')
    parser.add_argument('--json', default='.scripts/.link_health_results_v4.1.json', help='JSON输出文件')
    parser.add_argument('--timeout', type=int, default=15, help='请求超时时间（秒）')
    parser.add_argument('--concurrent', type=int, default=20, help='并发请求数')
    args = parser.parse_args()
    
    root_dir = Path(args.root)
    
    # 创建检测器
    checker = LinkHealthChecker(
        timeout_seconds=args.timeout,
        concurrent_limit=args.concurrent
    )
    
    # 提取所有链接
    print("🔍 Extracting external links...")
    url_to_files = checker.extract_all_links(root_dir)
    print(f"🔗 Found {len(url_to_files)} unique external links")
    
    # 限制数量
    urls = list(url_to_files.items())
    if args.limit > 0:
        urls = urls[:args.limit]
    
    print(f"🎯 Preparing to check {len(urls)} links")
    
    # 批量检测
    start_time = time.time()
    results = await checker.check_batch(urls)
    elapsed = time.time() - start_time
    
    # 统计
    ok_count = sum(1 for r in results if r.category == "ok")
    redirect_count = sum(1 for r in results if r.category == "redirect")
    failed_count = sum(1 for r in results if not r.is_accessible)
    
    print(f"\n⏱️ 检测完成，耗时: {elapsed:.1f}秒")
    print(f"📈 结果:")
    print(f"   ✅ OK: {ok_count}")
    print(f"   🔄 Redirect: {redirect_count}")
    print(f"   ❌ Failed: {failed_count}")
    
    # 生成报告
    checker.generate_report(results, args.output)
    
    # 导出JSON
    checker.export_json(results, args.json)
    
    # 关闭会话
    await checker.close_session()
    
    # 返回退出码
    return 1 if failed_count > 10 else 0


if __name__ == '__main__':
    exit_code = asyncio.run(main())
    exit(exit_code)
