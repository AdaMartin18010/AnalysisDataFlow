#!/usr/bin/env python3
"""
外部链接健康检测工具
检测项目中的所有外部链接，标记失效链接并提供修复建议

Author: AnalysisDataFlow Project
Version: 1.0.0
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
import time


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
    priority: int = 0  # 0=低, 1=中, 2=高, 3=核心
    
    def __post_init__(self):
        if self.source_files is None:
            self.source_files = []
        if not self.check_time:
            self.check_time = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        return asdict(self)


class ExternalLinkChecker:
    """外部链接检测器"""
    
    # 高优先级域名模式（核心链接）
    CORE_PATTERNS = [
        r'nightlies\.apache\.org/flink',
        r'flink\.apache\.org',
        r'github\.com/apache/flink',
        r'doi\.org',
        r'arxiv\.org',
        r'apache\.org',
    ]
    
    # 中优先级域名模式
    MEDIUM_PATTERNS = [
        r'github\.com',
        r'medium\.com',
        r'developer\.',
        r'docs\.(oracle|microsoft|aws|google)',
        r'stackoverflow\.com',
    ]
    
    # 用户代理列表（轮换使用）
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.0',
    ]
    
    def __init__(self, cache_file: str = ".scripts/.link_cache.pkl", 
                 cache_ttl_hours: int = 24,
                 concurrent_limit: int = 10,
                 delay_seconds: float = 0.5):
        """
        初始化检测器
        
        Args:
            cache_file: 缓存文件路径
            cache_ttl_hours: 缓存有效期（小时）
            concurrent_limit: 并发请求数限制
            delay_seconds: 请求间隔延迟（秒）
        """
        self.cache_file = Path(cache_file)
        self.cache_ttl = timedelta(hours=cache_ttl_hours)
        self.concurrent_limit = concurrent_limit
        self.delay_seconds = delay_seconds
        self.cache: Dict[str, LinkStatus] = {}
        self.load_cache()
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore: Optional[asyncio.Semaphore] = None
        
    def load_cache(self):
        """加载缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    self.cache = pickle.load(f)
                # 清理过期缓存
                now = datetime.now()
                expired_keys = [
                    k for k, v in self.cache.items() 
                    if now - datetime.fromisoformat(v.check_time) > self.cache_ttl
                ]
                for k in expired_keys:
                    del self.cache[k]
                print(f"📦 已加载缓存: {len(self.cache)} 条有效记录，清理 {len(expired_keys)} 条过期记录")
            except Exception as e:
                print(f"⚠️ 缓存加载失败: {e}")
                self.cache = {}
    
    def save_cache(self):
        """保存缓存"""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
            print(f"💾 缓存已保存: {len(self.cache)} 条记录")
        except Exception as e:
            print(f"⚠️ 缓存保存失败: {e}")
    
    def get_priority(self, url: str) -> int:
        """获取链接优先级"""
        url_lower = url.lower()
        for pattern in self.CORE_PATTERNS:
            if re.search(pattern, url_lower):
                return 3  # 核心
        for pattern in self.MEDIUM_PATTERNS:
            if re.search(pattern, url_lower):
                return 2  # 中
        return 1  # 低
    
    def is_external_link(self, url: str) -> bool:
        """判断是否为外部链接"""
        if not url or url.startswith('#') or url.startswith('./'):
            return False
        if url.startswith('http://') or url.startswith('https://'):
            return True
        return False
    
    async def init_session(self):
        """初始化HTTP会话"""
        if self.session is None:
            connector = aiohttp.TCPConnector(
                limit=self.concurrent_limit * 2,
                limit_per_host=self.concurrent_limit,
                enable_cleanup_closed=True,
                force_close=True,
            )
            timeout = aiohttp.ClientTimeout(total=30, connect=10)
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
        """
        检测单个链接
        
        Args:
            url: 要检测的URL
            source_files: 引用该链接的源文件列表
            
        Returns:
            LinkStatus: 链接状态
        """
        # 检查缓存
        if url in self.cache:
            cached = self.cache[url]
            age = datetime.now() - datetime.fromisoformat(cached.check_time)
            if age < self.cache_ttl:
                if source_files:
                    cached.source_files = list(set(cached.source_files + source_files))
                return cached
        
        await self.init_session()
        
        priority = self.get_priority(url)
        status = LinkStatus(
            url=url,
            source_files=source_files or [],
            priority=priority
        )
        
        async with self.semaphore:
            start_time = time.time()
            user_agent = self.USER_AGENTS[hash(url) % len(self.USER_AGENTS)]
            
            try:
                headers = {'User-Agent': user_agent}
                async with self.session.head(
                    url, 
                    headers=headers, 
                    allow_redirects=True,
                    ssl=False  # 允许自签名证书
                ) as response:
                    status.status_code = response.status
                    status.response_time_ms = (time.time() - start_time) * 1000
                    
                    if response.status == 200:
                        status.is_accessible = True
                    elif 300 <= response.status < 400:
                        status.is_accessible = True
                        if response.history:
                            status.redirect_url = str(response.url)
                    elif response.status in (405,):  # Method Not Allowed
                        # 尝试GET请求
                        async with self.session.get(
                            url, 
                            headers=headers, 
                            allow_redirects=True,
                            ssl=False
                        ) as get_response:
                            status.status_code = get_response.status
                            status.response_time_ms = (time.time() - start_time) * 1000
                            status.is_accessible = 200 <= get_response.status < 400
                    else:
                        status.is_accessible = False
                        status.error_message = f"HTTP {response.status}"
                        
            except asyncio.TimeoutError:
                status.error_message = "连接超时"
                status.response_time_ms = (time.time() - start_time) * 1000
            except aiohttp.ClientError as e:
                status.error_message = f"客户端错误: {str(e)[:50]}"
                status.response_time_ms = (time.time() - start_time) * 1000
            except Exception as e:
                status.error_message = f"未知错误: {str(e)[:50]}"
                status.response_time_ms = (time.time() - start_time) * 1000
        
        # 更新缓存
        self.cache[url] = status
        
        # 延迟避免限流
        await asyncio.sleep(self.delay_seconds)
        
        return status
    
    async def check_batch(self, urls: List[Tuple[str, List[str]]]) -> List[LinkStatus]:
        """
        批量检测链接
        
        Args:
            urls: (url, source_files) 元组列表
            
        Returns:
            List[LinkStatus]: 链接状态列表
        """
        await self.init_session()
        
        # 按优先级排序
        sorted_urls = sorted(urls, key=lambda x: self.get_priority(x[0]), reverse=True)
        
        # 分批处理，每批10个
        batch_size = 10
        results = []
        
        for i in range(0, len(sorted_urls), batch_size):
            batch = sorted_urls[i:i+batch_size]
            print(f"🔍 检测批次 {i//batch_size + 1}/{(len(sorted_urls) + batch_size - 1)//batch_size} ({len(batch)} 个链接)")
            
            tasks = [self.check_link(url, files) for url, files in batch]
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in batch_results:
                if isinstance(result, Exception):
                    print(f"⚠️ 检测异常: {result}")
                else:
                    results.append(result)
            
            # 批次间延迟
            if i + batch_size < len(sorted_urls):
                await asyncio.sleep(2)
        
        return results
    
    def get_archive_link(self, url: str) -> Optional[str]:
        """
        获取Archive.org备份链接
        
        Args:
            url: 原始URL
            
        Returns:
            Optional[str]: Archive.org备份链接
        """
        try:
            encoded_url = quote(url, safe='')
            return f"https://web.archive.org/web/*/{url}"
        except Exception:
            return None
    
    def extract_links_from_file(self, file_path: Path) -> Set[str]:
        """
        从Markdown文件中提取外部链接
        
        Args:
            file_path: Markdown文件路径
            
        Returns:
            Set[str]: 外部链接集合
        """
        links = set()
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # 匹配Markdown链接 [text](url)
            md_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
            for match in re.finditer(md_pattern, content):
                url = match.group(2).strip()
                if self.is_external_link(url):
                    # 去除锚点
                    url = url.split('#')[0]
                    links.add(url)
            
            # 匹配引用式链接 [text][ref] 和 [ref]: url
            ref_def_pattern = r'^\[([^\]]+)\]:\s*(\S+)'
            for match in re.finditer(ref_def_pattern, content, re.MULTILINE):
                url = match.group(2).strip()
                if self.is_external_link(url):
                    url = url.split('#')[0]
                    links.add(url)
            
            # 匹配裸URL <http://...>
            bare_url_pattern = r'<(https?://[^>]+)>'
            for match in re.finditer(bare_url_pattern, content):
                url = match.group(1).strip()
                url = url.split('#')[0]
                links.add(url)
                
        except Exception as e:
            print(f"⚠️ 读取文件失败 {file_path}: {e}")
        
        return links
    
    def extract_all_links(self, root_dir: Path, include_dirs: List[str] = None) -> Dict[str, List[str]]:
        """
        从项目中提取所有外部链接
        
        Args:
            root_dir: 项目根目录
            include_dirs: 要包含的目录列表
            
        Returns:
            Dict[str, List[str]]: URL -> 源文件列表的映射
        """
        url_to_files: Dict[str, List[str]] = {}
        
        if include_dirs is None:
            include_dirs = ['.', 'Struct', 'Knowledge', 'Flink', 'docs', 'tutorials']
        
        md_files = []
        for dir_name in include_dirs:
            dir_path = root_dir / dir_name
            if dir_path.exists():
                md_files.extend(dir_path.glob('*.md'))
                md_files.extend(dir_path.glob('**/*.md'))
        
        # 去重
        md_files = list(set(md_files))
        print(f"📄 找到 {len(md_files)} 个Markdown文件")
        
        for md_file in md_files:
            links = self.extract_links_from_file(md_file)
            relative_path = str(md_file.relative_to(root_dir))
            for link in links:
                if link not in url_to_files:
                    url_to_files[link] = []
                url_to_files[link].append(relative_path)
        
        return url_to_files
    
    def generate_report(self, results: List[LinkStatus], output_file: str = "EXTERNAL-LINK-HEALTH-REPORT.md") -> str:
        """
        生成检测报告
        
        Args:
            results: 检测结果列表
            output_file: 输出报告文件名
            
        Returns:
            str: 报告内容
        """
        total = len(results)
        accessible = sum(1 for r in results if r.is_accessible)
        failed = total - accessible
        redirects = sum(1 for r in results if r.redirect_url and r.is_accessible)
        
        # 按优先级分组
        core_links = [r for r in results if r.priority == 3]
        medium_links = [r for r in results if r.priority == 2]
        low_links = [r for r in results if r.priority <= 1]
        
        # 按状态分组
        failed_links = [r for r in results if not r.is_accessible]
        redirect_links = [r for r in results if r.redirect_url and r.is_accessible]
        slow_links = [r for r in results if r.response_time_ms > 5000 and r.is_accessible]
        
        report_lines = [
            "# 外部链接健康检测报告",
            "",
            f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"> 检测链接总数: {total}",
            f"> 缓存有效期: {self.cache_ttl.total_seconds() / 3600:.0f} 小时",
            "",
            "## 📊 检测统计",
            "",
            "| 指标 | 数量 | 百分比 |",
            "|------|------|--------|",
            f"| 总链接数 | {total} | 100% |",
            f"| ✅ 可访问 | {accessible} | {accessible/total*100:.1f}% |" if total > 0 else "| ✅ 可访问 | 0 | 0% |",
            f"| ❌ 失效 | {failed} | {failed/total*100:.1f}% |" if total > 0 else "| ❌ 失效 | 0 | 0% |",
            f"| 🔄 301重定向 | {redirects} | {redirects/total*100:.1f}% |" if total > 0 else "| 🔄 301重定向 | 0 | 0% |",
            "",
            "### 按优先级分布",
            "",
            "| 优先级 | 数量 | 可访问 | 失效 |",
            "|--------|------|--------|------|",
            f"| 🔴 核心 (高) | {len(core_links)} | {sum(1 for r in core_links if r.is_accessible)} | {sum(1 for r in core_links if not r.is_accessible)} |",
            f"| 🟡 中等 | {len(medium_links)} | {sum(1 for r in medium_links if r.is_accessible)} | {sum(1 for r in medium_links if not r.is_accessible)} |",
            f"| 🟢 低 | {len(low_links)} | {sum(1 for r in low_links if r.is_accessible)} | {sum(1 for r in low_links if not r.is_accessible)} |",
            "",
        ]
        
        # 核心链接状态
        if core_links:
            report_lines.extend([
                "## 🔴 核心链接状态",
                "",
                "| 链接 | 状态 | HTTP | 响应时间 | 源文件 |",
                "|------|------|------|----------|--------|",
            ])
            for r in sorted(core_links, key=lambda x: x.url):
                status_icon = "✅" if r.is_accessible else "❌"
                code = r.status_code if r.status_code else "N/A"
                time_str = f"{r.response_time_ms:.0f}ms" if r.response_time_ms else "N/A"
                files = ", ".join(r.source_files[:2]) + ("..." if len(r.source_files) > 2 else "")
                report_lines.append(f"| [{r.url[:60]}...]({r.url}) | {status_icon} | {code} | {time_str} | {files[:40]} |")
            report_lines.append("")
        
        # 失效链接清单
        if failed_links:
            report_lines.extend([
                "## ❌ 失效链接清单",
                "",
                "| 链接 | HTTP | 错误信息 | 源文件 | 建议操作 |",
                "|------|------|----------|--------|----------|",
            ])
            for r in sorted(failed_links, key=lambda x: -x.priority):
                code = r.status_code if r.status_code else "N/A"
                error = r.error_message if r.error_message else "Unknown"
                files = ", ".join(r.source_files[:2])
                archive = self.get_archive_link(r.url)
                suggestion = f"[Archive备份]({archive})" if archive else "手动检查"
                report_lines.append(f"| [{r.url[:50]}...]({r.url}) | {code} | {error[:30]} | {files[:30]} | {suggestion} |")
            report_lines.append("")
        
        # 301重定向链接
        if redirect_links:
            report_lines.extend([
                "## 🔄 301重定向链接（建议更新）",
                "",
                "| 原链接 | 重定向目标 | 源文件 |",
                "|--------|------------|--------|",
            ])
            for r in sorted(redirect_links, key=lambda x: -x.priority):
                files = ", ".join(r.source_files[:2])
                report_lines.append(f"| [{r.url[:50]}...]({r.url}) | [{r.redirect_url[:50]}...]({r.redirect_url}) | {files[:30]} |")
            report_lines.append("")
        
        # 响应慢的链接
        if slow_links:
            report_lines.extend([
                "## 🐌 响应缓慢的链接 (>5s)",
                "",
                "| 链接 | 响应时间 | 源文件 |",
                "|------|----------|--------|",
            ])
            for r in sorted(slow_links, key=lambda x: -x.response_time_ms):
                files = ", ".join(r.source_files[:2])
                report_lines.append(f"| [{r.url[:50]}...]({r.url}) | {r.response_time_ms/1000:.1f}s | {files[:30]} |")
            report_lines.append("")
        
        # 修复建议
        report_lines.extend([
            "## 🔧 修复建议",
            "",
            "### 自动修复",
            "",
            "运行自动修复脚本更新301重定向：",
            "```bash",
            "python .scripts/fix-external-links.py --mode fix-redirects",
            "```",
            "",
            "### 手动修复",
            "",
            "1. **失效链接**: 使用Archive.org备份或寻找替代链接",
            "2. **404错误**: 检查链接是否拼写正确",
            "3. **超时链接**: 可能是暂时性问题，稍后重试",
            "",
            "### Archive.org备份",
            "",
            "对于失效链接，可以使用以下方式查找备份：",
            "- 直接访问: `https://web.archive.org/web/*/{URL}`",
            "- 使用工具批量查询: `python .scripts/fix-external-links.py --mode find-archive`",
            "",
        ])
        
        report = "\n".join(report_lines)
        
        # 保存报告
        output_path = Path(output_file)
        output_path.write_text(report, encoding='utf-8')
        print(f"📝 报告已保存: {output_file}")
        
        return report
    
    def export_json(self, results: List[LinkStatus], output_file: str = ".scripts/.link_check_results.json"):
        """导出结果为JSON格式"""
        data = {
            "check_time": datetime.now().isoformat(),
            "total": len(results),
            "accessible": sum(1 for r in results if r.is_accessible),
            "failed": sum(1 for r in results if not r.is_accessible),
            "results": [r.to_dict() for r in results]
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"📊 JSON结果已保存: {output_file}")


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='外部链接健康检测工具')
    parser.add_argument('--root', default='.', help='项目根目录')
    parser.add_argument('--limit', type=int, default=0, help='限制检测链接数量（0=全部）')
    parser.add_argument('--priority', choices=['all', 'core', 'medium', 'low'], default='all',
                        help='检测优先级（all=全部, core=仅核心）')
    parser.add_argument('--output', default='EXTERNAL-LINK-HEALTH-REPORT.md', help='输出报告文件名')
    parser.add_argument('--cache-ttl', type=int, default=24, help='缓存有效期（小时）')
    parser.add_argument('--no-cache', action='store_true', help='不使用缓存')
    args = parser.parse_args()
    
    root_dir = Path(args.root)
    
    # 创建检测器
    checker = ExternalLinkChecker(
        cache_file=".scripts/.link_cache.pkl" if not args.no_cache else "/dev/null",
        cache_ttl_hours=0 if args.no_cache else args.cache_ttl
    )
    
    # 提取所有链接
    print("🔍 正在提取外部链接...")
    url_to_files = checker.extract_all_links(root_dir)
    print(f"🔗 找到 {len(url_to_files)} 个唯一外部链接")
    
    # 根据优先级过滤
    if args.priority == 'core':
        url_to_files = {k: v for k, v in url_to_files.items() if checker.get_priority(k) == 3}
    elif args.priority == 'medium':
        url_to_files = {k: v for k, v in url_to_files.items() if checker.get_priority(k) >= 2}
    
    # 限制数量
    urls = list(url_to_files.items())
    if args.limit > 0:
        urls = urls[:args.limit]
    
    print(f"🎯 准备检测 {len(urls)} 个链接（优先级: {args.priority}）")
    
    # 批量检测
    start_time = time.time()
    results = await checker.check_batch(urls)
    elapsed = time.time() - start_time
    
    print(f"\n⏱️ 检测完成，耗时: {elapsed:.1f}秒")
    print(f"📈 结果: {sum(1 for r in results if r.is_accessible)}/{len(results)} 可访问")
    
    # 生成报告
    checker.generate_report(results, args.output)
    
    # 导出JSON
    checker.export_json(results)
    
    # 保存缓存
    if not args.no_cache:
        checker.save_cache()
    
    # 关闭会话
    await checker.close_session()


if __name__ == '__main__':
    asyncio.run(main())
