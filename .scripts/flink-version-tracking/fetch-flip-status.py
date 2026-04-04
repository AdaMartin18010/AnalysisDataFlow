#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink FLIP Status Fetcher

从 Apache Flink GitHub 和 Wiki 获取 FLIP (Flink Improvement Proposals) 状态信息，
解析并输出为结构化 JSON 数据。

作者: Flink Version Tracker
版本: 1.0.0
"""

import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse

# 尝试导入可选依赖
try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    # 使用标准库替代
    import urllib.request
    import urllib.error
    import urllib.parse
    import ssl

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False


# =============================================================================
# 配置和日志设置
# =============================================================================

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """配置日志记录器"""
    logger = logging.getLogger("flip-fetcher")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 清除现有处理器
    logger.handlers.clear()
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # 格式化
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def load_config(config_path: str = "config.json") -> Dict:
    """加载配置文件"""
    default_config = {
        "flink": {
            "github_repo": "apache/flink",
            "flip_base_url": "https://cwiki.apache.org/confluence/display/FLINK",
            "flip_index_url": "https://cwiki.apache.org/confluence/display/FLINK/Flink+Improvement+Proposals"
        },
        "api": {
            "request_timeout": 30,
            "retry_attempts": 3,
            "retry_delay": 2
        },
        "storage": {
            "data_dir": "./data",
            "flip_cache_file": "flip_cache.json"
        }
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合并默认配置
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                    elif isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if sub_key not in config[key]:
                                config[key][sub_key] = sub_value
                return config
        except (json.JSONDecodeError, IOError) as e:
            logging.warning(f"无法加载配置文件 {config_path}: {e}，使用默认配置")
    
    return default_config


# =============================================================================
# 数据模型
# =============================================================================

@dataclass
class FLIP:
    """FLIP 数据模型"""
    number: int
    title: str
    status: str
    author: str
    created_date: Optional[str] = None
    updated_date: Optional[str] = None
    target_version: Optional[str] = None
    implemented_version: Optional[str] = None
    component: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    jira_issue: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @property
    def flip_id(self) -> str:
        """生成 FLIP ID (如 FLIP-123)"""
        return f"FLIP-{self.number}"


@dataclass
class FetchResult:
    """获取结果"""
    success: bool
    flips: List[FLIP]
    errors: List[str]
    timestamp: str
    total_count: int = 0
    new_count: int = 0
    updated_count: int = 0
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "success": self.success,
            "flips": [f.to_dict() for f in self.flips],
            "errors": self.errors,
            "timestamp": self.timestamp,
            "total_count": self.total_count,
            "new_count": self.new_count,
            "updated_count": self.updated_count
        }


# =============================================================================
# HTTP 客户端
# =============================================================================

class HTTPClient:
    """HTTP 客户端封装，支持重试和错误处理"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.timeout = config.get("api", {}).get("request_timeout", 30)
        self.retry_attempts = config.get("api", {}).get("retry_attempts", 3)
        self.retry_delay = config.get("api", {}).get("retry_delay", 2)
        
        if HAS_REQUESTS:
            self.session = self._create_session()
        else:
            self.session = None
    
    def _create_session(self) -> requests.Session:
        """创建带有重试机制的 requests 会话"""
        session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=self.retry_attempts,
            backoff_factor=self.retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # 设置默认请求头
        session.headers.update({
            "User-Agent": "Flink-Version-Tracker/1.0 (Research Purpose)",
            "Accept": "application/json, text/html"
        })
        
        return session
    
    def get(self, url: str, headers: Optional[Dict] = None) -> Optional[str]:
        """
        发送 GET 请求
        
        Args:
            url: 请求 URL
            headers: 可选的自定义请求头
            
        Returns:
            响应内容字符串，失败返回 None
        """
        merged_headers = {}
        if headers:
            merged_headers.update(headers)
        
        try:
            if self.session:
                # 使用 requests
                response = self.session.get(url, headers=merged_headers, timeout=self.timeout)
                response.raise_for_status()
                return response.text
            else:
                # 使用 urllib
                req = urllib.request.Request(url, headers=merged_headers)
                # 创建 SSL 上下文忽略证书验证（仅用于开发/测试）
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                
                with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as response:
                    return response.read().decode('utf-8')
                    
        except Exception as e:
            self.logger.error(f"请求失败 {url}: {e}")
            return None
    
    def get_json(self, url: str, headers: Optional[Dict] = None) -> Optional[Dict]:
        """
        发送 GET 请求并解析 JSON
        
        Args:
            url: 请求 URL
            headers: 可选的自定义请求头
            
        Returns:
            解析后的 JSON 字典，失败返回 None
        """
        content = self.get(url, headers)
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON 解析失败: {e}")
        return None


# =============================================================================
# FLIP 解析器
# =============================================================================

class FLIPParser:
    """FLIP 内容解析器"""
    
    # FLIP 状态映射
    STATUS_MAPPING = {
        "draft": "draft",
        "under discussion": "under_discussion",
        "accepted": "accepted",
        "implemented": "implemented",
        "released": "released",
        "withdrawn": "withdrawn",
        "rejected": "rejected",
        "replaced": "replaced"
    }
    
    # 组件分类关键词
    COMPONENT_PATTERNS = {
        "runtime": ["runtime", "scheduler", "resource manager", "slot", "task manager"],
        "streaming": ["stream", "checkpoint", "state", "watermark", "checkpointing"],
        "sql": ["sql", "table", "query", "optimizer", "planner"],
        "api": ["api", "dataset", "datastream", "connector"],
        "deployment": ["deployment", "kubernetes", "yarn", "mesos", "docker"],
        "security": ["security", "authentication", "authorization", "ssl", "kerberos"],
        "observability": ["metric", "logging", "monitoring", "observability", "trace"]
    }
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.has_bs4 = HAS_BS4
    
    def parse_flip_number(self, text: str) -> Optional[int]:
        """从文本中提取 FLIP 编号"""
        patterns = [
            r'FLIP[-\s]*(\d+)',  # FLIP-123 或 FLIP 123
            r'FLIP\s*#?(\d+)',   # FLIP#123
            r'\b(\d+)\s*-\s*',   # 123 - Title
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    num = int(match.group(1))
                    if 1 <= num <= 9999:  # 合理的 FLIP 编号范围
                        return num
                except ValueError:
                    continue
        return None
    
    def parse_status(self, text: str) -> str:
        """解析 FLIP 状态"""
        text_lower = text.lower().strip()
        
        for keyword, status in self.STATUS_MAPPING.items():
            if keyword in text_lower:
                return status
        
        return "unknown"
    
    def parse_version(self, text: str) -> Optional[str]:
        """从文本中提取版本号"""
        # 匹配版本号模式: 1.18, 2.0, 1.19.0 等
        pattern = r'\b(\d+\.\d+(?:\.\d+)?)\b'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return None
    
    def parse_jira_issue(self, text: str) -> Optional[str]:
        """提取 JIRA 问题编号"""
        pattern = r'(FLINK-\d+)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).upper()
        return None
    
    def determine_component(self, title: str, description: str = "") -> Optional[str]:
        """根据标题和描述确定组件分类"""
        text = (title + " " + description).lower()
        
        component_scores = {}
        for component, keywords in self.COMPONENT_PATTERNS.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                component_scores[component] = score
        
        if component_scores:
            # 返回得分最高的组件
            return max(component_scores.items(), key=lambda x: x[1])[0]
        
        return None
    
    def parse_html_content(self, html_content: str) -> List[FLIP]:
        """
        解析 HTML 内容提取 FLIP 信息
        
        Args:
            html_content: HTML 页面内容
            
        Returns:
            FLIP 对象列表
        """
        flips = []
        
        if not self.has_bs4:
            self.logger.warning("BeautifulSoup 未安装，使用基础正则解析")
            return self._parse_with_regex(html_content)
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 查找 FLIP 表格或列表
            # Confluence 页面通常使用表格组织 FLIP
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                if len(rows) < 2:  # 跳过空表格
                    continue
                
                # 解析表头
                headers = []
                header_row = rows[0]
                for th in header_row.find_all(['th', 'td']):
                    headers.append(th.get_text(strip=True).lower())
                
                # 映射列索引
                col_map = self._map_columns(headers)
                
                # 解析数据行
                for row in rows[1:]:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) < 3:
                        continue
                    
                    flip = self._parse_flip_row(cells, col_map)
                    if flip and flip.number > 0:
                        flips.append(flip)
            
            # 如果没有找到表格，尝试其他解析方式
            if not flips:
                flips = self._parse_alternative(soup)
                
        except Exception as e:
            self.logger.error(f"HTML 解析错误: {e}")
            # 回退到正则解析
            flips = self._parse_with_regex(html_content)
        
        return flips
    
    def _map_columns(self, headers: List[str]) -> Dict[str, int]:
        """映射列名到索引"""
        col_map = {}
        
        for idx, header in enumerate(headers):
            header_lower = header.lower()
            
            if any(k in header_lower for k in ['flip', 'number', 'id', '#']):
                col_map['number'] = idx
            elif any(k in header_lower for k in ['title', 'name', 'proposal']):
                col_map['title'] = idx
            elif any(k in header_lower for k in ['status', 'state']):
                col_map['status'] = idx
            elif any(k in header_lower for k in ['author', 'owner', 'shepherd']):
                col_map['author'] = idx
            elif any(k in header_lower for k in ['version', 'target', 'release']):
                col_map['version'] = idx
            elif any(k in header_lower for k in ['jira', 'issue', 'ticket']):
                col_map['jira'] = idx
            elif any(k in header_lower for k in ['component', 'module', 'area']):
                col_map['component'] = idx
        
        return col_map
    
    def _parse_flip_row(self, cells, col_map: Dict[str, int]) -> Optional[FLIP]:
        """解析单行 FLIP 数据"""
        try:
            # 获取所有文本
            cell_texts = [cell.get_text(strip=True) for cell in cells]
            full_text = ' '.join(cell_texts)
            
            # 提取 FLIP 编号
            number = None
            if 'number' in col_map:
                number = self.parse_flip_number(cell_texts[col_map['number']])
            if number is None:
                number = self.parse_flip_number(full_text)
            
            if number is None:
                return None
            
            # 提取标题
            title = "Unknown"
            if 'title' in col_map:
                title = cell_texts[col_map['title']]
            else:
                # 尝试从第一个包含数字的单元格提取
                for text in cell_texts:
                    clean = re.sub(r'FLIP[-\s]*\d+[-\s:]*', '', text, flags=re.IGNORECASE).strip()
                    if clean and len(clean) > 5:
                        title = clean
                        break
            
            # 提取状态
            status = "unknown"
            if 'status' in col_map:
                status = self.parse_status(cell_texts[col_map['status']])
            
            # 提取作者
            author = "Unknown"
            if 'author' in col_map:
                author = cell_texts[col_map['author']]
            
            # 提取版本
            target_version = None
            if 'version' in col_map:
                target_version = self.parse_version(cell_texts[col_map['version']])
            
            # 提取 JIRA
            jira_issue = None
            if 'jira' in col_map:
                jira_issue = self.parse_jira_issue(cell_texts[col_map['jira']])
            else:
                jira_issue = self.parse_jira_issue(full_text)
            
            # 确定组件
            component = None
            if 'component' in col_map:
                component = cell_texts[col_map['component']]
            else:
                component = self.determine_component(title)
            
            # 查找链接
            url = None
            for cell in cells:
                link = cell.find('a')
                if link and link.get('href'):
                    href = link['href']
                    if 'FLIP' in href.upper() or str(number) in href:
                        url = href
                        if not url.startswith('http'):
                            url = urljoin("https://cwiki.apache.org", url)
                        break
            
            return FLIP(
                number=number,
                title=title,
                status=status,
                author=author,
                target_version=target_version,
                component=component,
                jira_issue=jira_issue,
                url=url
            )
            
        except Exception as e:
            self.logger.error(f"解析 FLIP 行错误: {e}")
            return None
    
    def _parse_with_regex(self, html_content: str) -> List[FLIP]:
        """使用正则表达式解析 FLIP (后备方案)"""
        flips = []
        
        # 查找 FLIP 条目模式
        patterns = [
            r'FLIP[-\s]*(\d+)\s*[-:]\s*([^<\n]+)',
            r'(\d+)\s*[-:]\s*([^<\n]{10,100})',
        ]
        
        found_numbers = set()
        
        for pattern in patterns:
            matches = re.finditer(pattern, html_content, re.IGNORECASE)
            for match in matches:
                try:
                    number = int(match.group(1))
                    if number in found_numbers or number > 9999:
                        continue
                    
                    title = match.group(2).strip()
                    # 清理 HTML 标签
                    title = re.sub(r'<[^>]+>', '', title)
                    title = title[:200]  # 限制长度
                    
                    if len(title) > 10:
                        found_numbers.add(number)
                        
                        flip = FLIP(
                            number=number,
                            title=title,
                            status="unknown",
                            author="Unknown"
                        )
                        flips.append(flip)
                        
                except (ValueError, IndexError):
                    continue
        
        return flips
    
    def _parse_alternative(self, soup) -> List[FLIP]:
        """替代解析方法 - 查找链接和列表项"""
        flips = []
        found_numbers = set()
        
        # 查找所有链接
        for link in soup.find_all('a'):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            number = self.parse_flip_number(text) or self.parse_flip_number(href)
            
            if number and number not in found_numbers:
                found_numbers.add(number)
                
                # 清理标题
                title = re.sub(r'^FLIP[-\s]*\d+\s*[-:]?\s*', '', text, flags=re.IGNORECASE)
                title = re.sub(r'<[^>]+>', '', title).strip()
                
                if len(title) < 5:
                    title = "Unknown"
                
                url = href
                if url and not url.startswith('http'):
                    url = urljoin("https://cwiki.apache.org", url)
                
                flip = FLIP(
                    number=number,
                    title=title[:200],
                    status="unknown",
                    author="Unknown",
                    url=url
                )
                flips.append(flip)
        
        return flips


# =============================================================================
# GitHub API 获取器
# =============================================================================

class GitHubFLIPFetcher:
    """从 GitHub API 获取 FLIP 相关信息"""
    
    def __init__(self, config: Dict, http_client: HTTPClient, logger: logging.Logger):
        self.config = config
        self.http = http_client
        self.logger = logger
        self.repo = config.get("flink", {}).get("github_repo", "apache/flink")
        self.base_url = config.get("api", {}).get("github_api_base", "https://api.github.com")
    
    def fetch_flip_issues(self) -> List[Dict]:
        """
        从 GitHub Issues 中搜索 FLIP 相关条目
        
        Returns:
            问题列表
        """
        issues = []
        
        # 搜索 FLIP 相关 issues
        search_queries = [
            "FLIP in:title is:issue",
            "FLIP in:title is:pr",
            "type:FLIP"
        ]
        
        for query in search_queries:
            url = f"{self.base_url}/search/issues"
            params = f"q={urllib.parse.quote(query)}+repo:{self.repo}&per_page=100"
            full_url = f"{url}?{params}"
            
            data = self.http.get_json(full_url)
            
            if data and "items" in data:
                for item in data["items"]:
                    issues.append({
                        "number": item.get("number"),
                        "title": item.get("title", ""),
                        "state": item.get("state", ""),
                        "url": item.get("html_url", ""),
                        "created_at": item.get("created_at"),
                        "updated_at": item.get("updated_at"),
                        "body": item.get("body", "")[:500]  # 限制内容长度
                    })
            
            # 避免触发 API 限制
            time.sleep(1)
        
        return issues
    
    def fetch_flip_discussions(self) -> List[Dict]:
        """
        获取 FLIP 相关讨论 (如果可用)
        
        Returns:
            讨论列表
        """
        # GitHub Discussions API 需要 GraphQL，这里简化处理
        # 返回空列表作为占位符
        return []
    
    def extract_flip_from_issues(self, issues: List[Dict]) -> List[FLIP]:
        """
        从 GitHub Issues 中提取 FLIP 信息
        
        Args:
            issues: GitHub issue 列表
            
        Returns:
            FLIP 对象列表
        """
        flips = []
        parser = FLIPParser(self.logger)
        
        for issue in issues:
            title = issue.get("title", "")
            
            # 提取 FLIP 编号
            number = parser.parse_flip_number(title)
            if number is None:
                continue
            
            # 解析状态
            state = issue.get("state", "")
            status_map = {
                "open": "under_discussion",
                "closed": "implemented"
            }
            status = status_map.get(state, "unknown")
            
            # 创建 FLIP 对象
            flip = FLIP(
                number=number,
                title=title,
                status=status,
                author="Unknown",
                created_date=issue.get("created_at"),
                updated_date=issue.get("updated_at"),
                url=issue.get("url"),
                description=issue.get("body", "")[:300]
            )
            
            flips.append(flip)
        
        return flips


# =============================================================================
# Wiki 页面获取器
# =============================================================================

class WikiFLIPFetcher:
    """从 Confluence Wiki 获取 FLIP 信息"""
    
    def __init__(self, config: Dict, http_client: HTTPClient, logger: logging.Logger):
        self.config = config
        self.http = http_client
        self.logger = logger
        self.base_url = config.get("flink", {}).get("flip_base_url", 
                                                      "https://cwiki.apache.org/confluence/display/FLINK")
        self.index_url = config.get("flink", {}).get("flip_index_url",
                                                       "https://cwiki.apache.org/confluence/display/FLINK/Flink+Improvement+Proposals")
    
    def fetch_flip_index(self) -> Optional[str]:
        """
        获取 FLIP 索引页面
        
        Returns:
            HTML 内容
        """
        self.logger.info(f"获取 FLIP 索引页面: {self.index_url}")
        return self.http.get(self.index_url)
    
    def fetch_individual_flip(self, flip_number: int) -> Optional[str]:
        """
        获取单个 FLIP 页面
        
        Args:
            flip_number: FLIP 编号
            
        Returns:
            HTML 内容
        """
        url = f"{self.base_url}/FLIP-{flip_number}"
        self.logger.info(f"获取 FLIP 页面: {url}")
        return self.http.get(url)
    
    def parse_flip_details(self, html_content: str, flip_number: int) -> Optional[FLIP]:
        """
        解析单个 FLIP 页面详情
        
        Args:
            html_content: HTML 内容
            flip_number: FLIP 编号
            
        Returns:
            完整的 FLIP 对象
        """
        if not HAS_BS4:
            return None
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            parser = FLIPParser(self.logger)
            
            # 提取标题
            title = "Unknown"
            title_elem = soup.find('h1') or soup.find('h2')
            if title_elem:
                title = title_elem.get_text(strip=True)
                title = re.sub(r'FLIP[-\s]*\d+\s*[-:]?\s*', '', title, flags=re.IGNORECASE)
            
            # 查找状态信息面板
            status = "unknown"
            author = "Unknown"
            target_version = None
            jira_issue = None
            
            # 尝试从表格中提取
            for table in soup.find_all('table'):
                for row in table.find_all('tr'):
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True).lower()
                        value = cells[1].get_text(strip=True)
                        
                        if 'status' in label:
                            status = parser.parse_status(value)
                        elif 'author' in label or 'shepherd' in label or 'owner' in label:
                            author = value
                        elif 'version' in label or 'release' in label:
                            target_version = parser.parse_version(value) or value
                        elif 'jira' in label or 'issue' in label:
                            jira_issue = parser.parse_jira_issue(value) or value
            
            # 尝试从页面内容提取
            page_text = soup.get_text()
            
            if status == "unknown":
                # 搜索状态关键词
                status_patterns = [
                    r'[Ss]tatus\s*[:\-]\s*(\w+)',
                    r'[Ss]tate\s*[:\-]\s*(\w+)',
                ]
                for pattern in status_patterns:
                    match = re.search(pattern, page_text)
                    if match:
                        status = parser.parse_status(match.group(1))
                        break
            
            if author == "Unknown":
                author_match = re.search(r'[Aa]uthor\s*[:\-]\s*([^\n<]+)', page_text)
                if author_match:
                    author = author_match.group(1).strip()[:50]
            
            if not jira_issue:
                jira_issue = parser.parse_jira_issue(page_text)
            
            if not target_version:
                # 查找目标版本
                version_patterns = [
                    r'[Tt]arget\s*[Vv]ersion\s*[:\-]\s*(\d+\.\d+)',
                    r'[Ff]link\s*(\d+\.\d+)',
                    r'[Rr]elease\s*(\d+\.\d+)',
                ]
                for pattern in version_patterns:
                    match = re.search(pattern, page_text)
                    if match:
                        target_version = match.group(1)
                        break
            
            # 提取描述
            description = ""
            content_div = soup.find('div', {'id': 'main-content'}) or soup.find('div', {'class': 'wiki-content'})
            if content_div:
                # 获取前几段文本
                paragraphs = content_div.find_all('p', limit=3)
                description = ' '.join(p.get_text(strip=True) for p in paragraphs)
                description = description[:500]
            
            return FLIP(
                number=flip_number,
                title=title[:200],
                status=status,
                author=author[:50],
                target_version=target_version,
                jira_issue=jira_issue,
                description=description,
                component=parser.determine_component(title, description),
                url=f"{self.base_url}/FLIP-{flip_number}"
            )
            
        except Exception as e:
            self.logger.error(f"解析 FLIP {flip_number} 详情错误: {e}")
            return None


# =============================================================================
# 主控制器
# =============================================================================

class FLIPFetcher:
    """FLIP 获取主控制器"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.http = HTTPClient(config, logger)
        self.parser = FLIPParser(logger)
        self.github_fetcher = GitHubFLIPFetcher(config, self.http, logger)
        self.wiki_fetcher = WikiFLIPFetcher(config, self.http, logger)
        
        # 确保数据目录存在
        self.data_dir = Path(config.get("storage", {}).get("data_dir", "./data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.cache_file = self.data_dir / config.get("storage", {}).get("flip_cache_file", "flip_cache.json")
    
    def load_cache(self) -> Dict:
        """加载缓存数据"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                self.logger.warning(f"加载缓存失败: {e}")
        return {"flips": {}, "last_update": None}
    
    def save_cache(self, flips: List[FLIP]) -> bool:
        """保存缓存数据"""
        try:
            cache_data = {
                "flips": {f.flip_id: f.to_dict() for f in flips},
                "last_update": datetime.now().isoformat(),
                "count": len(flips)
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"缓存已保存: {self.cache_file}")
            return True
            
        except IOError as e:
            self.logger.error(f"保存缓存失败: {e}")
            return False
    
    def fetch_all_flips(self, detailed: bool = False, max_flips: int = 0) -> FetchResult:
        """
        获取所有 FLIP 信息
        
        Args:
            detailed: 是否获取详细信息（会请求每个 FLIP 页面）
            max_flips: 最大获取数量（0 表示无限制）
            
        Returns:
            获取结果
        """
        flips = []
        errors = []
        cache = self.load_cache()
        
        self.logger.info("开始获取 FLIP 数据...")
        
        # 1. 从 Wiki 索引页面获取
        try:
            index_content = self.wiki_fetcher.fetch_flip_index()
            if index_content:
                wiki_flips = self.parser.parse_html_content(index_content)
                self.logger.info(f"从 Wiki 索引解析到 {len(wiki_flips)} 个 FLIP")
                flips.extend(wiki_flips)
            else:
                errors.append("无法获取 Wiki 索引页面")
        except Exception as e:
            self.logger.error(f"Wiki 获取错误: {e}")
            errors.append(f"Wiki 错误: {str(e)}")
        
        # 2. 从 GitHub 获取补充信息
        try:
            github_issues = self.github_fetcher.fetch_flip_issues()
            self.logger.info(f"从 GitHub 获取到 {len(github_issues)} 个相关 issues")
            
            github_flips = self.github_fetcher.extract_flip_from_issues(github_issues)
            
            # 合并 GitHub 数据
            flip_map = {f.number: f for f in flips}
            for gh_flip in github_flips:
                if gh_flip.number in flip_map:
                    # 更新现有数据
                    existing = flip_map[gh_flip.number]
                    if existing.status == "unknown" and gh_flip.status != "unknown":
                        existing.status = gh_flip.status
                    if not existing.url and gh_flip.url:
                        existing.url = gh_flip.url
                else:
                    flip_map[gh_flip.number] = gh_flip
            
            flips = list(flip_map.values())
            
        except Exception as e:
            self.logger.error(f"GitHub 获取错误: {e}")
            errors.append(f"GitHub 错误: {str(e)}")
        
        # 3. 获取详细信息（可选）
        if detailed:
            self.logger.info("获取详细 FLIP 信息...")
            
            # 按编号排序并限制数量
            sorted_flips = sorted(flips, key=lambda f: f.number)
            if max_flips > 0:
                sorted_flips = sorted_flips[:max_flips]
            
            detailed_flips = []
            for flip in sorted_flips:
                try:
                    content = self.wiki_fetcher.fetch_individual_flip(flip.number)
                    if content:
                        detailed = self.wiki_fetcher.parse_flip_details(content, flip.number)
                        if detailed:
                            detailed_flips.append(detailed)
                        else:
                            detailed_flips.append(flip)
                    else:
                        detailed_flips.append(flip)
                    
                    # 避免请求过快
                    time.sleep(0.5)
                    
                except Exception as e:
                    self.logger.warning(f"获取 FLIP-{flip.number} 详情失败: {e}")
                    detailed_flips.append(flip)
            
            flips = detailed_flips
        
        # 去重并按编号排序
        unique_flips = {}
        for flip in flips:
            if flip.number not in unique_flips or flip.status != "unknown":
                unique_flips[flip.number] = flip
        
        flips = sorted(unique_flips.values(), key=lambda f: f.number)
        
        # 统计变更
        new_count = 0
        updated_count = 0
        cached_flips = cache.get("flips", {})
        
        for flip in flips:
            flip_id = flip.flip_id
            if flip_id not in cached_flips:
                new_count += 1
            elif cached_flips[flip_id].get("status") != flip.status:
                updated_count += 1
        
        # 保存缓存
        self.save_cache(flips)
        
        return FetchResult(
            success=len(errors) == 0 or len(flips) > 0,
            flips=flips,
            errors=errors,
            timestamp=datetime.now().isoformat(),
            total_count=len(flips),
            new_count=new_count,
            updated_count=updated_count
        )
    
    def export_to_json(self, flips: List[FLIP], output_path: Optional[str] = None) -> str:
        """
        导出 FLIP 数据到 JSON 文件
        
        Args:
            flips: FLIP 列表
            output_path: 输出路径（可选）
            
        Returns:
            输出文件路径
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.data_dir / f"flips_{timestamp}.json"
        
        data = {
            "generated_at": datetime.now().isoformat(),
            "total": len(flips),
            "flips": [f.to_dict() for f in flips]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"数据已导出: {output_path}")
        return str(output_path)
    
    def generate_status_summary(self, flips: List[FLIP]) -> Dict:
        """
        生成状态摘要
        
        Args:
            flips: FLIP 列表
            
        Returns:
            状态统计字典
        """
        status_counts = {}
        component_counts = {}
        version_targets = {}
        
        for flip in flips:
            # 状态统计
            status = flip.status or "unknown"
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # 组件统计
            if flip.component:
                component_counts[flip.component] = component_counts.get(flip.component, 0) + 1
            
            # 目标版本统计
            if flip.target_version:
                version_targets[flip.target_version] = version_targets.get(flip.target_version, 0) + 1
        
        return {
            "by_status": status_counts,
            "by_component": component_counts,
            "by_target_version": version_targets,
            "total": len(flips)
        }


# =============================================================================
# 命令行接口
# =============================================================================

def main():
    """主入口函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Flink FLIP Status Fetcher - 获取 Apache Flink FLIP 状态",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          # 基础获取模式
  %(prog)s --detailed               # 获取详细信息
  %(prog)s --detailed --max 50      # 只获取前 50 个 FLIP
  %(prog)s --output flips.json      # 指定输出文件
  %(prog)s --config custom.json     # 使用自定义配置
        """
    )
    
    parser.add_argument("-c", "--config", default="config.json",
                        help="配置文件路径 (默认: config.json)")
    parser.add_argument("-o", "--output", default=None,
                        help="输出 JSON 文件路径")
    parser.add_argument("-d", "--detailed", action="store_true",
                        help="获取详细 FLIP 信息（较慢）")
    parser.add_argument("-m", "--max", type=int, default=0,
                        help="最大 FLIP 获取数量")
    parser.add_argument("-l", "--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                        help="日志级别")
    parser.add_argument("--summary", action="store_true",
                        help="显示状态摘要")
    parser.add_argument("--status-filter", default=None,
                        help="按状态过滤 (如: accepted,implemented)")
    
    args = parser.parse_args()
    
    # 设置日志
    logger = setup_logging(args.log_level)
    
    # 检查依赖
    if not HAS_REQUESTS:
        logger.warning("未安装 requests 库，使用 urllib 作为后备方案")
        logger.warning("建议: pip install requests")
    
    if not HAS_BS4:
        logger.warning("未安装 beautifulsoup4 库，解析能力受限")
        logger.warning("建议: pip install beautifulsoup4 lxml")
    
    # 加载配置
    config = load_config(args.config)
    
    # 创建获取器
    fetcher = FLIPFetcher(config, logger)
    
    # 执行获取
    logger.info("=" * 60)
    logger.info("Flink FLIP Status Fetcher v1.0")
    logger.info("=" * 60)
    
    result = fetcher.fetch_all_flips(
        detailed=args.detailed,
        max_flips=args.max
    )
    
    # 过滤
    flips = result.flips
    if args.status_filter:
        allowed_statuses = [s.strip().lower() for s in args.status_filter.split(",")]
        flips = [f for f in flips if f.status in allowed_statuses]
    
    # 输出结果
    print("\n" + "=" * 60)
    print(f"获取结果:")
    print(f"  成功: {result.success}")
    print(f"  总数: {result.total_count}")
    print(f"  新增: {result.new_count}")
    print(f"  更新: {result.updated_count}")
    print(f"  错误: {len(result.errors)}")
    
    if result.errors:
        print("\n错误详情:")
        for error in result.errors:
            print(f"  - {error}")
    
    # 导出数据
    if args.output or True:  # 默认导出
        output_path = fetcher.export_to_json(flips, args.output)
        print(f"\n数据已导出: {output_path}")
    
    # 显示摘要
    if args.summary:
        summary = fetcher.generate_status_summary(flips)
        print("\n状态摘要:")
        print(f"  按状态: {summary['by_status']}")
        print(f"  按组件: {summary['by_component']}")
        print(f"  按目标版本: {summary['by_target_version']}")
    
    # 示例输出
    print("\n前 5 个 FLIP:")
    for flip in flips[:5]:
        print(f"  {flip.flip_id}: {flip.title[:50]}... [{flip.status}]")
    
    # 返回码
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
