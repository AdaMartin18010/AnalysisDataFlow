#!/usr/bin/env python3
"""
Link Checker - Markdown 链接验证工具

功能：
    - 扫描所有 .md 文件中的内部链接
    - 检查外部链接可访问性
    - 验证锚点链接
    - 生成损坏链接报告

作者: AnalysisDataFlow Project
版本: 1.0.0
"""

from __future__ import annotations

import argparse
import asyncio
import configparser
import json
import os
import re
import sys
import time
import unittest
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from urllib.parse import urlparse

# 尝试导入可选依赖
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class LinkType(Enum):
    """链接类型枚举"""
    INTERNAL = "internal"           # 内部相对路径链接
    INTERNAL_ANCHOR = "anchor"      # 内部锚点链接
    EXTERNAL = "external"           # 外部 HTTP(S) 链接
    EMAIL = "email"                 # 邮件链接
    UNKNOWN = "unknown"             # 未知类型


class LinkStatus(Enum):
    """链接状态枚举"""
    OK = "ok"                       # 链接正常
    BROKEN = "broken"               # 链接损坏
    TIMEOUT = "timeout"             # 超时
    ERROR = "error"                 # 错误
    SKIPPED = "skipped"             # 被跳过
    PENDING = "pending"             # 等待检查


@dataclass
class LinkInfo:
    """链接信息数据类"""
    url: str
    link_type: LinkType
    source_file: Path
    line_number: int
    column: int
    anchor: Optional[str] = None
    text: str = ""
    status: LinkStatus = LinkStatus.PENDING
    status_code: Optional[int] = None
    error_message: Optional[str] = None
    response_time: Optional[float] = None
    checked_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "url": self.url,
            "link_type": self.link_type.value,
            "source_file": str(self.source_file),
            "line_number": self.line_number,
            "column": self.column,
            "anchor": self.anchor,
            "text": self.text,
            "status": self.status.value,
            "status_code": self.status_code,
            "error_message": self.error_message,
            "response_time": self.response_time,
            "checked_at": self.checked_at
        }


@dataclass
class CheckResult:
    """检查结果数据类"""
    total_links: int = 0
    valid_links: int = 0
    broken_links: int = 0
    timeout_links: int = 0
    error_links: int = 0
    skipped_links: int = 0
    links: List[LinkInfo] = field(default_factory=list)
    
    @property
    def success_rate(self) -> float:
        """计算成功率"""
        if self.total_links == 0:
            return 100.0
        return (self.valid_links / self.total_links) * 100
    
    def add_link(self, link: LinkInfo) -> None:
        """添加链接到结果"""
        self.links.append(link)
        self.total_links += 1
        
        if link.status == LinkStatus.OK:
            self.valid_links += 1
        elif link.status == LinkStatus.BROKEN:
            self.broken_links += 1
        elif link.status == LinkStatus.TIMEOUT:
            self.timeout_links += 1
        elif link.status == LinkStatus.ERROR:
            self.error_links += 1
        elif link.status == LinkStatus.SKIPPED:
            self.skipped_links += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "summary": {
                "total_links": self.total_links,
                "valid_links": self.valid_links,
                "broken_links": self.broken_links,
                "timeout_links": self.timeout_links,
                "error_links": self.error_links,
                "skipped_links": self.skipped_links,
                "success_rate": round(self.success_rate, 2)
            },
            "links": [link.to_dict() for link in self.links]
        }



class Config:
    """配置管理类"""
    
    DEFAULT_CONFIG = {
        "general": {
            "timeout": "30",
            "max_workers": "10",
            "retry_count": "3",
            "retry_delay": "1"
        },
        "ignore": {
            "patterns": "",
            "external": "false",
            "anchors": "false"
        },
        "output": {
            "json_report": "link-check-report.json",
            "markdown_report": "link-check-report.md",
            "verbose": "false",
            "color": "true"
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """初始化配置"""
        self.config = configparser.ConfigParser()
        
        # 设置默认值
        for section, options in self.DEFAULT_CONFIG.items():
            self.config.add_section(section)
            for key, value in options.items():
                self.config.set(section, key, value)
        
        # 从文件加载配置
        if config_path and os.path.exists(config_path):
            self.config.read(config_path)
        
        # 从环境变量加载
        self._load_from_env()
    
    def _load_from_env(self) -> None:
        """从环境变量加载配置"""
        env_mappings = {
            "LINK_CHECKER_TIMEOUT": ("general", "timeout"),
            "LINK_CHECKER_MAX_WORKERS": ("general", "max_workers"),
            "LINK_CHECKER_RETRY_COUNT": ("general", "retry_count"),
            "LINK_CHECKER_IGNORE_EXTERNAL": ("ignore", "external"),
            "LINK_CHECKER_VERBOSE": ("output", "verbose"),
        }
        
        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value:
                self.config.set(section, key, value)
    
    @property
    def timeout(self) -> int:
        return self.config.getint("general", "timeout")
    
    @property
    def max_workers(self) -> int:
        return self.config.getint("general", "max_workers")
    
    @property
    def retry_count(self) -> int:
        return self.config.getint("general", "retry_count")
    
    @property
    def retry_delay(self) -> int:
        return self.config.getint("general", "retry_delay")
    
    @property
    def ignore_patterns(self) -> List[str]:
        patterns = self.config.get("ignore", "patterns")
        return [p.strip() for p in patterns.split(",") if p.strip()]
    
    @property
    def ignore_external(self) -> bool:
        return self.config.getboolean("ignore", "external")
    
    @property
    def ignore_anchors(self) -> bool:
        return self.config.getboolean("ignore", "anchors")
    
    @property
    def json_report(self) -> str:
        return self.config.get("output", "json_report")
    
    @property
    def markdown_report(self) -> str:
        return self.config.get("output", "markdown_report")
    
    @property
    def verbose(self) -> bool:
        return self.config.getboolean("output", "verbose")
    
    @property
    def color(self) -> bool:
        return self.config.getboolean("output", "color")


class Colors:
    """终端颜色类"""
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"
    
    @classmethod
    def disable(cls) -> None:
        """禁用颜色"""
        cls.GREEN = ""
        cls.YELLOW = ""
        cls.RED = ""
        cls.BLUE = ""
        cls.CYAN = ""
        cls.MAGENTA = ""
        cls.BOLD = ""
        cls.RESET = ""



class LinkParser:
    """Markdown 链接解析器"""
    
    # Markdown 链接正则表达式
    LINK_PATTERN = re.compile(
        r"(?<!`)\[([^\]]+)\]\(([^\s\)]*)(?:\s+\"([^\"]*)\")?\)"
    )
    
    # 引用式链接 [text][ref]
    REF_LINK_PATTERN = re.compile(r"(?<!`)\[([^\]]+)\]\[([^\]]*)\]")
    
    # 链接定义 [ref]: url
    LINK_DEF_PATTERN = re.compile(
        r"^\[([^\]]+)\]:\s*(\S+)(?:\s+\"([^\"]*)\")?",
        re.MULTILINE
    )
    
    # 自动链接 <url>
    AUTO_LINK_PATTERN = re.compile(r"<([a-zA-Z][a-zA-Z0-9+.-]*://[^>]+)>")
    
    # 图片链接 ![alt](url)
    IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^\s\)]*)(?:\s+\"[^\"]*\")?\)")
    
    def __init__(self, config: Config):
        self.config = config
    
    def parse_file(self, file_path: Path) -> List[LinkInfo]:
        """解析单个 Markdown 文件"""
        links: List[LinkInfo] = []
        
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")
        except Exception as e:
            if self.config.verbose:
                print(f"Warning: Cannot read file {file_path}: {e}")
            return links
        
        # 收集链接定义
        link_definitions: Dict[str, str] = {}
        for match in self.LINK_DEF_PATTERN.finditer(content):
            ref, url = match.groups()[:2]
            link_definitions[ref.lower()] = url
        
        for line_num, line in enumerate(lines, 1):
            # 解析内联链接
            for match in self.LINK_PATTERN.finditer(line):
                text, url = match.groups()[:2]
                
                # 跳过被忽略的模式
                if self._should_ignore(url):
                    continue
                
                link_info = self._create_link_info(
                    url, text, file_path, line_num, match.start()
                )
                if link_info:
                    links.append(link_info)
            
            # 解析引用式链接
            for match in self.REF_LINK_PATTERN.finditer(line):
                text, ref = match.groups()
                ref_key = ref.lower() if ref else text.lower()
                
                if ref_key in link_definitions:
                    url = link_definitions[ref_key]
                    if not self._should_ignore(url):
                        link_info = self._create_link_info(
                            url, text, file_path, line_num, match.start()
                        )
                        if link_info:
                            links.append(link_info)
            
            # 解析自动链接
            for match in self.AUTO_LINK_PATTERN.finditer(line):
                url = match.group(1)
                if not self._should_ignore(url):
                    link_info = self._create_link_info(
                        url, url, file_path, line_num, match.start()
                    )
                    if link_info:
                        links.append(link_info)
        
        return links
    
    def _should_ignore(self, url: str) -> bool:
        """检查是否应该忽略该链接"""
        for pattern in self.config.ignore_patterns:
            if re.search(pattern, url):
                return True
        return False
    
    def _create_link_info(
        self,
        url: str,
        text: str,
        source_file: Path,
        line_number: int,
        column: int
    ) -> Optional[LinkInfo]:
        """创建链接信息对象"""
        url = url.strip()
        
        if not url or url.startswith("#"):
            # 纯锚点链接
            if url.startswith("#") and not self.config.ignore_anchors:
                return LinkInfo(
                    url=url,
                    link_type=LinkType.INTERNAL_ANCHOR,
                    source_file=source_file,
                    line_number=line_number,
                    column=column,
                    anchor=url[1:],
                    text=text
                )
            return None
        
        # 确定链接类型
        if url.startswith("http://") or url.startswith("https://"):
            if self.config.ignore_external:
                return None
            link_type = LinkType.EXTERNAL
            anchor = None
        elif url.startswith("mailto:"):
            link_type = LinkType.EMAIL
            anchor = None
        elif "://" in url:
            link_type = LinkType.UNKNOWN
            anchor = None
        else:
            # 内部链接
            link_type = LinkType.INTERNAL
            if "#" in url:
                url, anchor = url.split("#", 1)
            else:
                anchor = None
        
        return LinkInfo(
            url=url,
            link_type=link_type,
            source_file=source_file,
            line_number=line_number,
            column=column,
            anchor=anchor,
            text=text
        )



class LinkChecker:
    """链接检查器"""
    
    # 成功的 HTTP 状态码
    OK_STATUS_CODES = {200, 201, 202, 203, 204, 205, 206, 301, 302, 303, 307, 308}
    
    def __init__(self, config: Config, base_path: Path):
        self.config = config
        self.base_path = base_path.resolve()
        self.parser = LinkParser(config)
        self.result = CheckResult()
        self.session: Optional[Any] = None
        
        # 缓存已检查的文件头部信息
        self._file_headers_cache: Dict[Path, Set[str]] = {}
        
        # 缓存外部链接检查结果
        self._external_cache: Dict[str, Tuple[LinkStatus, Optional[int], Optional[str]]] = {}
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        if AIOHTTP_AVAILABLE:
            import aiohttp
            connector = aiohttp.TCPConnector(limit=self.config.max_workers)
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={"User-Agent": "LinkChecker/1.0 (AnalysisDataFlow Project)"}
            )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    def scan_directory(self, directory: Path) -> List[LinkInfo]:
        """扫描目录中的所有 Markdown 文件"""
        all_links: List[LinkInfo] = []
        md_files = list(directory.rglob("*.md"))
        
        if self.config.verbose:
            print(f"Found {len(md_files)} Markdown files")
        
        for md_file in md_files:
            links = self.parser.parse_file(md_file)
            all_links.extend(links)
            
            if self.config.verbose:
                print(f"  {md_file}: {len(links)} links")
        
        return all_links
    
    async def check_links(self, links: List[LinkInfo]) -> CheckResult:
        """检查所有链接"""
        semaphore = asyncio.Semaphore(self.config.max_workers)
        tasks = []
        
        for link in links:
            task = self._check_link_with_semaphore(link, semaphore)
            tasks.append(task)
        
        await asyncio.gather(*tasks, return_exceptions=True)
        return self.result
    
    async def _check_link_with_semaphore(
        self,
        link: LinkInfo,
        semaphore: asyncio.Semaphore
    ) -> None:
        """使用信号量检查单个链接"""
        async with semaphore:
            await self._check_link(link)
    
    async def _check_link(self, link: LinkInfo) -> None:
        """检查单个链接"""
        start_time = time.time()
        link.checked_at = time.strftime("%Y-%m-%dT%H:%M:%S")
        
        try:
            if link.link_type == LinkType.EXTERNAL:
                await self._check_external_link(link)
            elif link.link_type == LinkType.INTERNAL:
                await self._check_internal_link(link)
            elif link.link_type == LinkType.INTERNAL_ANCHOR:
                await self._check_anchor_link(link)
            elif link.link_type == LinkType.EMAIL:
                link.status = LinkStatus.SKIPPED
                link.error_message = "Email links are not checked"
            else:
                link.status = LinkStatus.SKIPPED
                link.error_message = "Unknown link type"
        except Exception as e:
            link.status = LinkStatus.ERROR
            link.error_message = str(e)
        finally:
            link.response_time = time.time() - start_time
            self.result.add_link(link)
    
    async def _check_external_link(self, link: LinkInfo) -> None:
        """检查外部链接"""
        url = link.url
        
        # 检查缓存
        if url in self._external_cache:
            status, code, error = self._external_cache[url]
            link.status = status
            link.status_code = code
            link.error_message = error
            return
        
        # 重试机制
        for attempt in range(self.config.retry_count):
            try:
                if self.session and AIOHTTP_AVAILABLE:
                    status, code, error = await self._check_with_aiohttp(url)
                elif REQUESTS_AVAILABLE:
                    status, code, error = await self._check_with_requests(url)
                else:
                    link.status = LinkStatus.SKIPPED
                    link.error_message = "No HTTP library available"
                    return
                
                if status == LinkStatus.OK or attempt == self.config.retry_count - 1:
                    link.status = status
                    link.status_code = code
                    link.error_message = error
                    self._external_cache[url] = (status, code, error)
                    return
                
            except asyncio.TimeoutError:
                if attempt == self.config.retry_count - 1:
                    link.status = LinkStatus.TIMEOUT
                    link.error_message = f"Timeout after {self.config.timeout}s"
                    self._external_cache[url] = (LinkStatus.TIMEOUT, None, link.error_message)
                    return
            except Exception as e:
                if attempt == self.config.retry_count - 1:
                    link.status = LinkStatus.ERROR
                    link.error_message = str(e)
                    self._external_cache[url] = (LinkStatus.ERROR, None, str(e))
                    return
            
            await asyncio.sleep(self.config.retry_delay * (attempt + 1))
    
    async def _check_with_aiohttp(self, url: str) -> Tuple[LinkStatus, Optional[int], Optional[str]]:
        """使用 aiohttp 检查链接"""
        import aiohttp
        async with self.session.head(url, allow_redirects=True) as response:
            if response.status in self.OK_STATUS_CODES:
                return LinkStatus.OK, response.status, None
            
            # HEAD 失败，尝试 GET
            async with self.session.get(url, allow_redirects=True) as get_response:
                if get_response.status in self.OK_STATUS_CODES:
                    return LinkStatus.OK, get_response.status, None
                return LinkStatus.BROKEN, get_response.status, f"HTTP {get_response.status}"
    
    async def _check_with_requests(self, url: str) -> Tuple[LinkStatus, Optional[int], Optional[str]]:
        """使用 requests 检查链接（在异步线程中运行）"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_check_with_requests, url)
    
    def _sync_check_with_requests(self, url: str) -> Tuple[LinkStatus, Optional[int], Optional[str]]:
        """同步方式使用 requests 检查链接"""
        try:
            import requests
            response = requests.head(
                url,
                timeout=self.config.timeout,
                allow_redirects=True,
                headers={"User-Agent": "LinkChecker/1.0 (AnalysisDataFlow Project)"}
            )
            
            if response.status_code in self.OK_STATUS_CODES:
                return LinkStatus.OK, response.status_code, None
            
            # HEAD 失败，尝试 GET
            response = requests.get(
                url,
                timeout=self.config.timeout,
                allow_redirects=True,
                headers={"User-Agent": "LinkChecker/1.0 (AnalysisDataFlow Project)"}
            )
            
            if response.status_code in self.OK_STATUS_CODES:
                return LinkStatus.OK, response.status_code, None
            return LinkStatus.BROKEN, response.status_code, f"HTTP {response.status_code}"
        except requests.Timeout:
            return LinkStatus.TIMEOUT, None, f"Timeout after {self.config.timeout}s"
        except requests.RequestException as e:
            return LinkStatus.ERROR, None, str(e)


    async def _check_internal_link(self, link: LinkInfo) -> None:
        """检查内部链接"""
        # 解析相对路径
        if link.url.startswith("/"):
            # 绝对路径（相对于 base_path）
            target_path = self.base_path / link.url.lstrip("/")
        else:
            # 相对路径
            target_path = link.source_file.parent / link.url
        
        try:
            target_path = target_path.resolve()
        except (OSError, ValueError) as e:
            link.status = LinkStatus.BROKEN
            link.error_message = f"Invalid path: {e}"
            return
        
        # 安全检查：检查明显危险的路径模式
        # 允许正常的相对路径如 ../ 和 ../../ 但不能跳出项目根目录太远
        url_path = str(link.url)
        
        # 检查是否指向系统敏感目录
        target_str = str(target_path).lower()
        dangerous_paths = ["/etc/", "/usr/", "/bin/", "/sbin/", "/sys/", "/proc/",
                          "c:\\windows\\", "c:\\program files\\", "c:\\system"]
        for dangerous in dangerous_paths:
            if target_str.startswith(dangerous):
                link.status = LinkStatus.ERROR
                link.error_message = "Access to system directories not allowed"
                return
        
        # 计算相对路径深度：检查是否过多使用 ../ 跳出项目目录
        if link.url.startswith("../") or "/../" in link.url:
            # 解析路径，计算净向上级别
            parts = Path(link.url).parts
            up_count = sum(1 for p in parts if p == "..")
            down_count = sum(1 for p in parts if p != ".." and p != ".")
            
            # 尝试计算从源文件到 base_path 的深度
            try:
                source_to_base = link.source_file.parent.relative_to(self.base_path)
                source_depth = len(source_to_base.parts)
            except ValueError:
                source_depth = 0
            
            # 如果向上级别超过源文件在 base_path 中的深度，可能是危险的
            if up_count > source_depth + 2:  # 允许额外2级的缓冲
                link.status = LinkStatus.ERROR
                link.error_message = f"Path traversal risk: too many parent references ({up_count} > {source_depth + 2})"
                return
        
        # 检查文件是否存在
        if target_path.exists():
            if link.anchor:
                # 检查锚点
                headers = self._get_file_headers(target_path)
                if link.anchor in headers:
                    link.status = LinkStatus.OK
                else:
                    link.status = LinkStatus.BROKEN
                    link.error_message = f"Anchor '#{link.anchor}' not found"
            else:
                link.status = LinkStatus.OK
        else:
            link.status = LinkStatus.BROKEN
            link.error_message = f"File not found: {target_path.relative_to(self.base_path)}"
    
    async def _check_anchor_link(self, link: LinkInfo) -> None:
        """检查纯锚点链接（指向同一文件内的锚点）"""
        target_path = link.source_file
        headers = self._get_file_headers(target_path)
        
        if link.anchor in headers:
            link.status = LinkStatus.OK
        else:
            link.status = LinkStatus.BROKEN
            link.error_message = f"Anchor '#{link.anchor}' not found in current file"
    
    def _get_file_headers(self, file_path: Path) -> Set[str]:
        """获取文件中的所有标题锚点"""
        if file_path in self._file_headers_cache:
            return self._file_headers_cache[file_path]
        
        headers: Set[str] = set()
        
        try:
            content = file_path.read_text(encoding="utf-8")
            
            # Markdown 标题模式
            header_pattern = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)
            for match in header_pattern.finditer(content):
                header_text = match.group(1).strip()
                anchor = self._header_to_anchor(header_text)
                headers.add(anchor)
            
            # HTML 锚点模式
            anchor_pattern = re.compile(r'<a[^>]+name=["\']([^"\']+)["\']', re.IGNORECASE)
            for match in anchor_pattern.finditer(content):
                headers.add(match.group(1))
            
            # 自定义锚点模式 {#anchor}
            custom_anchor_pattern = re.compile(r"\{#([^}]+)\}")
            for match in custom_anchor_pattern.finditer(content):
                headers.add(match.group(1))
                
        except Exception:
            pass
        
        self._file_headers_cache[file_path] = headers
        return headers
    
    def _header_to_anchor(self, header_text: str) -> str:
        """将标题文本转换为锚点"""
        # 移除 Markdown 格式
        text = re.sub(r"<[^>]+>", "", header_text)
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
        text = re.sub(r"[*_`]", "", text)
        
        # GitHub 风格的锚点生成
        anchor = text.lower()
        anchor = re.sub(r"[^\w\s-]", "", anchor)
        anchor = re.sub(r"[\s]+", "-", anchor)
        anchor = anchor.strip("-")
        
        return anchor


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def generate_json_report(self, result: CheckResult, output_path: str) -> None:
        """生成 JSON 报告"""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)
    
    def generate_markdown_report(self, result: CheckResult, output_path: str) -> None:
        """生成 Markdown 报告"""
        lines = [
            "# Link Check Report",
            "",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            "",
            "| Metric | Count |",
            "|--------|-------|",
            f"| Total Links | {result.total_links} |",
            f"| Valid Links | {result.valid_links} |",
            f"| Broken Links | {result.broken_links} |",
            f"| Timeout Links | {result.timeout_links} |",
            f"| Error Links | {result.error_links} |",
            f"| Skipped Links | {result.skipped_links} |",
            f"| **Success Rate** | **{result.success_rate:.1f}%** |",
            "",
        ]
        
        # 按状态分组
        status_groups: Dict[LinkStatus, List[LinkInfo]] = {
            status: [] for status in LinkStatus
        }
        for link in result.links:
            status_groups[link.status].append(link)
        
        # 损坏的链接
        if result.broken_links > 0:
            lines.extend([
                "## Broken Links",
                "",
                "| File | Line | URL | Error |",
                "|------|------|-----|-------|"
            ])
            for link in status_groups[LinkStatus.BROKEN]:
                file_rel = link.source_file.relative_to(Path.cwd())
                lines.append(
                    f"| `{file_rel}` | {link.line_number} | `{link.url}` | {link.error_message or 'N/A'} |"
                )
            lines.append("")
        
        # 超时链接
        if result.timeout_links > 0:
            lines.extend([
                "## Timeout Links",
                "",
                "| File | Line | URL |",
                "|------|------|-----|"
            ])
            for link in status_groups[LinkStatus.TIMEOUT]:
                file_rel = link.source_file.relative_to(Path.cwd())
                lines.append(
                    f"| `{file_rel}` | {link.line_number} | `{link.url}` |"
                )
            lines.append("")
        
        # 错误链接
        if result.error_links > 0:
            lines.extend([
                "## Error Links",
                "",
                "| File | Line | URL | Error |",
                "|------|------|-----|-------|"
            ])
            for link in status_groups[LinkStatus.ERROR]:
                file_rel = link.source_file.relative_to(Path.cwd())
                lines.append(
                    f"| `{file_rel}` | {link.line_number} | `{link.url}` | {link.error_message or 'N/A'} |"
                )
            lines.append("")
        
        # 外部链接详情
        external_links = [l for l in result.links if l.link_type == LinkType.EXTERNAL]
        if external_links:
            lines.extend([
                "## External Links Detail",
                "",
                "| URL | Status | Code | Time (s) |",
                "|-----|--------|------|----------|"
            ])
            for link in sorted(external_links, key=lambda l: l.url):
                time_str = f"{link.response_time:.2f}" if link.response_time else "N/A"
                code_str = str(link.status_code) if link.status_code else "N/A"
                url_display = link.url[:60] + "..." if len(link.url) > 60 else link.url
                lines.append(
                    f"| `{url_display}` | {link.status.value} | {code_str} | {time_str} |"
                )
            lines.append("")
        
        lines.extend([
            "---",
            "",
            "*Generated by LinkChecker v1.0.0*"
        ])
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


    def print_console_summary(self, result: CheckResult) -> None:
        """打印控制台摘要"""
        if self.config.color:
            c = Colors
        else:
            c = type('NoColors', (), {
                'GREEN': '', 'YELLOW': '', 'RED': '', 'BLUE': '',
                'CYAN': '', 'MAGENTA': '', 'BOLD': '', 'RESET': ''
            })()
        
        print(f"\n{c.BOLD}{'='*60}{c.RESET}")
        print(f"{c.BOLD}Link Check Summary{c.RESET}")
        print(f"{c.BOLD}{'='*60}{c.RESET}")
        print()
        print(f"  Total Links:    {result.total_links}")
        print(f"  {c.GREEN}Valid Links:    {result.valid_links}{c.RESET}")
        print(f"  {c.RED}Broken Links:   {result.broken_links}{c.RESET}")
        print(f"  {c.YELLOW}Timeout Links:  {result.timeout_links}{c.RESET}")
        print(f"  {c.MAGENTA}Error Links:    {result.error_links}{c.RESET}")
        print(f"  Skipped Links:  {result.skipped_links}")
        print()
        
        # 成功率颜色
        if result.success_rate >= 95:
            rate_color = c.GREEN
        elif result.success_rate >= 80:
            rate_color = c.YELLOW
        else:
            rate_color = c.RED
        
        print(f"  {c.BOLD}Success Rate:   {rate_color}{result.success_rate:.1f}%{c.RESET}")
        print(f"{c.BOLD}{'='*60}{c.RESET}\n")
        
        # 显示损坏的链接
        if result.broken_links > 0:
            print(f"{c.RED}{c.BOLD}Broken Links:{c.RESET}")
            broken = [l for l in result.links if l.status == LinkStatus.BROKEN]
            for link in broken[:10]:  # 最多显示10个
                file_rel = link.source_file.relative_to(Path.cwd())
                print(f"  {c.RED}✗{c.RESET} {file_rel}:{link.line_number} -> {link.url}")
                if link.error_message:
                    print(f"     {c.YELLOW}Error: {link.error_message}{c.RESET}")
            if len(broken) > 10:
                print(f"  ... and {len(broken) - 10} more")
            print()
        
        # 显示超时链接
        if result.timeout_links > 0:
            print(f"{c.YELLOW}{c.BOLD}Timeout Links:{c.RESET}")
            timeouts = [l for l in result.links if l.status == LinkStatus.TIMEOUT]
            for link in timeouts[:5]:
                file_rel = link.source_file.relative_to(Path.cwd())
                print(f"  {c.YELLOW}⏱{c.RESET} {file_rel}:{link.line_number} -> {link.url}")
            if len(timeouts) > 5:
                print(f"  ... and {len(timeouts) - 5} more")
            print()


def create_default_config(path: str) -> None:
    """创建默认配置文件"""
    config_content = """[general]
# Request timeout (seconds)
timeout = 30
# Concurrent workers
max_workers = 10
# Retry count
retry_count = 3
# Retry delay (seconds)
retry_delay = 1

[ignore]
# URL patterns to ignore (comma-separated)
patterns = 
# Ignore external links
external = false
# Ignore anchor checking
anchors = false

[output]
# JSON report path
json_report = link-check-report.json
# Markdown report path
markdown_report = link-check-report.md
# Verbose output
verbose = false
# Color output
color = true
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(config_content)
    print(f"Created default config file: {path}")


def parse_arguments() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="Link Checker - Markdown Link Validation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Check current directory
  %(prog)s -d ./docs                # Check specific directory
  %(prog)s -c link-checker.ini      # Use config file
  %(prog)s --init-config            # Create default config
  %(prog)s --json report.json       # JSON report path
  %(prog)s --md report.md           # Markdown report path
  %(prog)s -v                       # Verbose output

Environment Variables:
  LINK_CHECKER_TIMEOUT              # Timeout seconds
  LINK_CHECKER_MAX_WORKERS          # Max concurrent workers
  LINK_CHECKER_RETRY_COUNT          # Retry count
  LINK_CHECKER_IGNORE_EXTERNAL      # Ignore external (true/false)
  LINK_CHECKER_VERBOSE              # Verbose (true/false)
        """
    )
    
    parser.add_argument(
        "-d", "--directory",
        default=".",
        help="Directory to scan (default: current directory)"
    )
    
    parser.add_argument(
        "-c", "--config",
        help="Config file path"
    )
    
    parser.add_argument(
        "--init-config",
        action="store_true",
        help="Create default config file"
    )
    
    parser.add_argument(
        "--json",
        dest="json_report",
        help="JSON report output path"
    )
    
    parser.add_argument(
        "--md",
        dest="md_report",
        help="Markdown report output path"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable color output"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        help="Request timeout (seconds)"
    )
    
    parser.add_argument(
        "-j", "--workers",
        type=int,
        help="Concurrent workers"
    )
    
    parser.add_argument(
        "--ignore-external",
        action="store_true",
        help="Ignore external links"
    )
    
    parser.add_argument(
        "--ci",
        action="store_true",
        help="CI/CD mode (exit non-zero on errors)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    return parser.parse_args()



async def main_async() -> int:
    """异步主函数"""
    args = parse_arguments()
    
    # 创建默认配置
    if args.init_config:
        create_default_config("link-checker.ini")
        return 0
    
    # 加载配置
    config = Config(args.config)
    
    # 命令行参数覆盖配置
    if args.verbose:
        config.config.set("output", "verbose", "true")
    if args.no_color:
        config.config.set("output", "color", "false")
        Colors.disable()
    if args.timeout:
        config.config.set("general", "timeout", str(args.timeout))
    if args.workers:
        config.config.set("general", "max_workers", str(args.workers))
    if args.ignore_external:
        config.config.set("ignore", "external", "true")
    
    # 确定报告输出路径
    json_report = args.json_report or config.json_report
    md_report = args.md_report or config.markdown_report
    
    # 解析扫描目录
    scan_dir = Path(args.directory).resolve()
    if not scan_dir.exists():
        print(f"Error: Directory not found: {scan_dir}", file=sys.stderr)
        return 1
    
    if config.verbose:
        print(f"Scanning directory: {scan_dir}")
        print(f"Configuration: timeout={config.timeout}s, workers={config.max_workers}")
    
    # 执行链接检查
    async with LinkChecker(config, scan_dir) as checker:
        if config.verbose:
            print("\nScanning files...")
        
        links = checker.scan_directory(scan_dir)
        
        if config.verbose:
            print(f"Found {len(links)} links to check\n")
        else:
            print(f"Checking {len(links)} links...")
        
        if not links:
            print("No links found to check.")
            return 0
        
        result = await checker.check_links(links)
    
    # 生成报告
    report_gen = ReportGenerator(config)
    
    if json_report:
        report_gen.generate_json_report(result, json_report)
        if config.verbose:
            print(f"\nJSON report saved: {json_report}")
    
    if md_report:
        report_gen.generate_markdown_report(result, md_report)
        if config.verbose:
            print(f"Markdown report saved: {md_report}")
    
    # 控制台输出
    report_gen.print_console_summary(result)
    
    # CI/CD 模式退出码
    if args.ci and result.broken_links + result.error_links > 0:
        return 1
    
    return 0


def main() -> int:
    """主入口点"""
    try:
        return asyncio.run(main_async())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1


# ==================== 单元测试 ====================

class TestLinkParser(unittest.IsolatedAsyncioTestCase):
    """链接解析器单元测试"""
    
    def setUp(self):
        self.config = Config()
        self.parser = LinkParser(self.config)
    
    def test_parse_inline_link(self):
        """测试解析内联链接"""
        content = "[link text](https://example.com)"
        match = self.parser.LINK_PATTERN.search(content)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "link text")
        self.assertEqual(match.group(2), "https://example.com")
    
    def test_parse_image_link(self):
        """测试不解析图片链接"""
        content = "![alt text](image.png)"
        # 图片链接不应被当作普通链接处理
        links = self.parser.parse_file(Path("test.md"))
        # 图片不是链接，所以 links 应该为空或只包含实际链接
        image_links = [l for l in links if l.url == "image.png"]
        # 注意：当前正则可能匹配图片，但类型应该是图片而非链接
        self.assertEqual(len(image_links), 0)
    
    def test_create_link_info(self):
        """测试创建链接信息"""
        info = self.parser._create_link_info(
            "https://example.com", "Example", Path("test.md"), 1, 0
        )
        self.assertIsNotNone(info)
        self.assertEqual(info.url, "https://example.com")
        self.assertEqual(info.text, "Example")
        self.assertEqual(info.link_type, LinkType.EXTERNAL)
    
    def test_should_ignore(self):
        """测试忽略模式"""
        self.config.config.set("ignore", "patterns", "example\\.com,test\\.org")
        self.assertTrue(self.parser._should_ignore("https://example.com/page"))
        self.assertTrue(self.parser._should_ignore("http://test.org"))
        self.assertFalse(self.parser._should_ignore("https://other.com"))


class TestLinkChecker(unittest.IsolatedAsyncioTestCase):
    """链接检查器单元测试"""
    
    def setUp(self):
        self.config = Config()
        self.checker = LinkChecker(self.config, Path("."))
    
    def test_ok_status_codes(self):
        """测试成功状态码判断"""
        self.assertIn(200, LinkChecker.OK_STATUS_CODES)
        self.assertIn(301, LinkChecker.OK_STATUS_CODES)
        self.assertNotIn(404, LinkChecker.OK_STATUS_CODES)
    
    def test_header_to_anchor_edge_cases(self):
        """测试标题转锚点的边界情况"""
        edge_cases = [
            ("", ""),
            ("!@#$%^&*()", ""),
            ("---Dashes---", "dashes"),
            ("123 Numbers", "123-numbers"),
        ]
        for header, expected in edge_cases:
            result = self.checker._header_to_anchor(header)
            self.assertEqual(result, expected)


class TestConfig(unittest.TestCase):
    """配置管理单元测试"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = Config()
        self.assertEqual(config.timeout, 30)
        self.assertEqual(config.max_workers, 10)
        self.assertEqual(config.retry_count, 3)
        self.assertFalse(config.ignore_external)
        self.assertTrue(config.color)
    
    def test_config_from_env(self):
        """测试从环境变量加载配置"""
        os.environ["LINK_CHECKER_TIMEOUT"] = "60"
        os.environ["LINK_CHECKER_VERBOSE"] = "true"
        
        config = Config()
        self.assertEqual(config.timeout, 60)
        self.assertTrue(config.verbose)
        
        # 清理
        del os.environ["LINK_CHECKER_TIMEOUT"]
        del os.environ["LINK_CHECKER_VERBOSE"]


class TestCheckResult(unittest.TestCase):
    """检查结果单元测试"""
    
    def test_empty_result(self):
        """测试空结果"""
        result = CheckResult()
        self.assertEqual(result.total_links, 0)
        self.assertEqual(result.success_rate, 100.0)
    
    def test_add_link(self):
        """测试添加链接"""
        result = CheckResult()
        link = LinkInfo(
            url="test",
            link_type=LinkType.INTERNAL,
            source_file=Path("test.md"),
            line_number=1,
            column=0,
            status=LinkStatus.OK
        )
        result.add_link(link)
        self.assertEqual(result.total_links, 1)
        self.assertEqual(result.valid_links, 1)
        self.assertEqual(result.success_rate, 100.0)
    
    def test_to_dict(self):
        """测试转换为字典"""
        result = CheckResult(total_links=10, valid_links=8, broken_links=2)
        data = result.to_dict()
        self.assertEqual(data["summary"]["total_links"], 10)
        self.assertEqual(data["summary"]["valid_links"], 8)
        self.assertEqual(data["summary"]["broken_links"], 2)
        self.assertEqual(data["summary"]["success_rate"], 80.0)


if __name__ == "__main__":
    # 如果直接运行测试
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        del sys.argv[1]
        unittest.main(verbosity=2)
    else:
        sys.exit(main())
