#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flink Release Checker

检查 Apache Flink 新版本发布，对比 Maven Central 和 GitHub Releases，
检测新版本并生成变更通知。

作者: Flink Version Tracker
版本: 1.0.0
"""

import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from packaging import version as pkg_version

# 尝试导入可选依赖
try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    import urllib.request
    import urllib.error
    import urllib.parse
    import ssl


# =============================================================================
# 配置和日志
# =============================================================================

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """配置日志记录器"""
    logger = logging.getLogger("release-checker")
    logger.setLevel(getattr(logging, log_level.upper()))
    logger.handlers.clear()
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
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
            "maven_group": "org.apache.flink",
            "maven_artifact": "flink-core"
        },
        "api": {
            "github_api_base": "https://api.github.com",
            "maven_central_base": "https://search.maven.org/solrsearch/select",
            "request_timeout": 30,
            "retry_attempts": 3,
            "retry_delay": 2
        },
        "storage": {
            "data_dir": "./data",
            "release_cache_file": "release_cache.json",
            "changelog_file": "version_changelog.json"
        },
        "tracking": {
            "check_interval_hours": 24,
            "release_track": ["1.18", "1.19", "1.20", "2.0"]
        }
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                    elif isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if sub_key not in config[key]:
                                config[key][sub_key] = sub_value
                return config
        except (json.JSONDecodeError, IOError) as e:
            logging.warning(f"无法加载配置文件: {e}，使用默认配置")
    
    return default_config


# =============================================================================
# 数据模型
# =============================================================================

@dataclass
class Release:
    """发布版本数据模型"""
    version: str
    release_date: Optional[str] = None
    is_stable: bool = True
    is_lts: bool = False
    download_url: Optional[str] = None
    release_notes_url: Optional[str] = None
    source_url: Optional[str] = None
    maven_url: Optional[str] = None
    changelog: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    new_features: List[str] = field(default_factory=list)
    bug_fixes: List[str] = field(default_factory=list)
    
    # 元数据
    discovered_at: str = field(default_factory=lambda: datetime.now().isoformat())
    source: str = "unknown"  # github, maven, docker
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @property
    def version_tuple(self) -> Tuple[int, ...]:
        """版本号转换为元组用于比较"""
        try:
            return tuple(int(x) for x in self.version.split('.'))
        except ValueError:
            return (0,)
    
    @property
    def major_minor(self) -> str:
        """获取主.次版本号"""
        parts = self.version.split('.')
        return '.'.join(parts[:2]) if len(parts) >= 2 else self.version


@dataclass
class ReleaseCheckResult:
    """检查结果"""
    success: bool
    new_releases: List[Release]
    updated_releases: List[Release]
    all_releases: List[Release]
    errors: List[str]
    timestamp: str
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "success": self.success,
            "new_releases": [r.to_dict() for r in self.new_releases],
            "updated_releases": [r.to_dict() for r in self.updated_releases],
            "all_releases": [r.to_dict() for r in self.all_releases],
            "errors": self.errors,
            "timestamp": self.timestamp,
            "summary": {
                "new_count": len(self.new_releases),
                "updated_count": len(self.updated_releases),
                "total_count": len(self.all_releases)
            }
        }


# =============================================================================
# HTTP 客户端
# =============================================================================

class HTTPClient:
    """HTTP 客户端"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.timeout = config.get("api", {}).get("request_timeout", 30)
        
        if HAS_REQUESTS:
            self.session = self._create_session()
        else:
            self.session = None
    
    def _create_session(self):
        """创建 requests 会话"""
        import requests
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({
            "User-Agent": "Flink-Version-Tracker/1.0",
            "Accept": "application/json"
        })
        return session
    
    def get(self, url: str, headers: Optional[Dict] = None) -> Optional[str]:
        """发送 GET 请求"""
        try:
            if self.session:
                response = self.session.get(url, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                return response.text
            else:
                req = urllib.request.Request(url, headers=headers or {})
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as r:
                    return r.read().decode('utf-8')
        except Exception as e:
            self.logger.error(f"请求失败 {url}: {e}")
            return None
    
    def get_json(self, url: str, headers: Optional[Dict] = None) -> Optional[Dict]:
        """获取 JSON 数据"""
        content = self.get(url, headers)
        if content:
            try:
                return json.loads(content)
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON 解析失败: {e}")
        return None


# =============================================================================
# GitHub Releases 获取器
# =============================================================================

class GitHubReleaseFetcher:
    """从 GitHub 获取发布信息"""
    
    def __init__(self, config: Dict, http_client: HTTPClient, logger: logging.Logger):
        self.config = config
        self.http = http_client
        self.logger = logger
        self.repo = config.get("flink", {}).get("github_repo", "apache/flink")
        self.base_url = config.get("api", {}).get("github_api_base", "https://api.github.com")
    
    def fetch_all_releases(self, per_page: int = 100) -> List[Release]:
        """
        获取所有 GitHub Releases
        
        Args:
            per_page: 每页数量
            
        Returns:
            Release 对象列表
        """
        releases = []
        page = 1
        max_pages = 10  # 限制最大页数
        
        self.logger.info(f"获取 GitHub Releases: {self.repo}")
        
        while page <= max_pages:
            url = f"{self.base_url}/repos/{self.repo}/releases"
            params = f"?per_page={per_page}&page={page}"
            full_url = url + params
            
            data = self.http.get_json(full_url)
            
            if not data:
                break
            
            if isinstance(data, list):
                for item in data:
                    release = self._parse_release(item)
                    if release:
                        releases.append(release)
                
                if len(data) < per_page:
                    break
            
            page += 1
            time.sleep(0.5)  # 避免 API 限制
        
        self.logger.info(f"从 GitHub 获取到 {len(releases)} 个 releases")
        return releases
    
    def _parse_release(self, data: Dict) -> Optional[Release]:
        """解析 GitHub release 数据"""
        try:
            tag_name = data.get("tag_name", "")
            
            # 提取版本号
            version = self._extract_version(tag_name)
            if not version:
                return None
            
            # 解析发布日期
            published = data.get("published_at", "")
            release_date = published.split("T")[0] if published else None
            
            # 判断是否为预发布版本
            is_stable = not data.get("prerelease", False)
            
            # 解析变更日志
            body = data.get("body", "")
            changelog = self._parse_changelog(body)
            
            # 提取各类变更
            breaking, features, fixes = self._categorize_changes(body)
            
            return Release(
                version=version,
                release_date=release_date,
                is_stable=is_stable,
                release_notes_url=data.get("html_url"),
                source_url=data.get("zipball_url") or data.get("tarball_url"),
                changelog=changelog,
                breaking_changes=breaking,
                new_features=features,
                bug_fixes=fixes,
                source="github"
            )
            
        except Exception as e:
            self.logger.error(f"解析 release 错误: {e}")
            return None
    
    def _extract_version(self, tag: str) -> Optional[str]:
        """从标签提取版本号"""
        # 移除前缀
        clean = tag
        for prefix in ["release-", "v", "flink-"]:
            if clean.lower().startswith(prefix):
                clean = clean[len(prefix):]
        
        # 匹配版本号模式
        match = re.match(r'^(\d+\.\d+(?:\.\d+)?)', clean)
        if match:
            return match.group(1)
        return None
    
    def _parse_changelog(self, body: str) -> List[str]:
        """解析变更日志内容"""
        if not body:
            return []
        
        # 简单的行分割
        lines = body.split('\n')
        # 过滤并清理
        changelog = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 10:
                # 移除 markdown 格式
                clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)
                clean = re.sub(r'[*\-`]', '', clean).strip()
                if clean:
                    changelog.append(clean[:200])
        
        return changelog[:20]  # 限制数量
    
    def _categorize_changes(self, body: str) -> Tuple[List[str], List[str], List[str]]:
        """分类变更：破坏性变更、新特性、Bug修复"""
        breaking = []
        features = []
        fixes = []
        
        if not body:
            return breaking, features, fixes
        
        lines = body.split('\n')
        current_section = None
        
        for line in lines:
            line_lower = line.lower()
            
            # 检测章节
            if 'breaking' in line_lower or 'backward' in line_lower or 'incompatible' in line_lower:
                current_section = 'breaking'
                continue
            elif 'feature' in line_lower or 'new' in line_lower or 'add' in line_lower:
                current_section = 'features'
                continue
            elif 'fix' in line_lower or 'bug' in line_lower or 'resolve' in line_lower:
                current_section = 'fixes'
                continue
            elif line.startswith('#') or line.startswith('---'):
                current_section = None
                continue
            
            # 收集条目
            clean = re.sub(r'[*\-`] ', '', line).strip()
            if clean and len(clean) > 10 and not clean.startswith('http'):
                if current_section == 'breaking':
                    breaking.append(clean[:200])
                elif current_section == 'features':
                    features.append(clean[:200])
                elif current_section == 'fixes':
                    fixes.append(clean[:200])
        
        return breaking[:10], features[:10], fixes[:10]


# =============================================================================
# Maven Central 获取器
# =============================================================================

class MavenReleaseFetcher:
    """从 Maven Central 获取发布信息"""
    
    def __init__(self, config: Dict, http_client: HTTPClient, logger: logging.Logger):
        self.config = config
        self.http = http_client
        self.logger = logger
        self.group = config.get("flink", {}).get("maven_group", "org.apache.flink")
        self.artifact = config.get("flink", {}).get("maven_artifact", "flink-core")
        self.base_url = config.get("api", {}).get("maven_central_base", 
                                                     "https://search.maven.org/solrsearch/select")
    
    def fetch_all_versions(self, rows: int = 500) -> List[Release]:
        """
        获取所有 Maven 版本
        
        Args:
            rows: 返回结果数量
            
        Returns:
            Release 对象列表
        """
        releases = []
        
        self.logger.info(f"查询 Maven Central: {self.group}:{self.artifact}")
        
        # 构建查询 URL
        query = f'g:"{self.group}" AND a:"{self.artifact}"'
        params = {
            'q': query,
            'rows': rows,
            'wt': 'json'
        }
        
        import urllib.parse
        query_string = urllib.parse.urlencode(params)
        url = f"{self.base_url}?{query_string}"
        
        data = self.http.get_json(url)
        
        if data and 'response' in data:
            docs = data['response'].get('docs', [])
            
            for doc in docs:
                release = self._parse_maven_doc(doc)
                if release:
                    releases.append(release)
        
        self.logger.info(f"从 Maven Central 获取到 {len(releases)} 个版本")
        return releases
    
    def _parse_maven_doc(self, doc: Dict) -> Optional[Release]:
        """解析 Maven 文档"""
        try:
            version = doc.get('latestVersion') or doc.get('v')
            if not version:
                return None
            
            # 过滤非标准版本
            if not re.match(r'^\d+\.\d+', version):
                return None
            
            # 解析时间戳
            timestamp = doc.get('timestamp')
            release_date = None
            if timestamp:
                try:
                    # Maven 时间戳是毫秒
                    dt = datetime.fromtimestamp(timestamp / 1000)
                    release_date = dt.strftime('%Y-%m-%d')
                except (ValueError, OverflowError):
                    pass
            
            # 构建 Maven URL
            maven_url = f"https://search.maven.org/artifact/{self.group}/{self.artifact}/{version}/jar"
            
            return Release(
                version=version,
                release_date=release_date,
                is_stable=self._is_stable(version),
                maven_url=maven_url,
                source="maven"
            )
            
        except Exception as e:
            self.logger.error(f"解析 Maven 文档错误: {e}")
            return None
    
    def _is_stable(self, version: str) -> bool:
        """判断是否为稳定版本"""
        unstable_patterns = ['-SNAPSHOT', '-alpha', '-beta', '-rc', '-preview', '-incubating']
        return not any(p.lower() in version.lower() for p in unstable_patterns)


# =============================================================================
# 版本比较器
# =============================================================================

class VersionComparator:
    """版本比较工具"""
    
    @staticmethod
    def compare(v1: str, v2: str) -> int:
        """
        比较两个版本号
        
        Returns:
            -1: v1 < v2
             0: v1 = v2
             1: v1 > v2
        """
        try:
            pv1 = pkg_version.parse(v1)
            pv2 = pkg_version.parse(v2)
            
            if pv1 < pv2:
                return -1
            elif pv1 > pv2:
                return 1
            else:
                return 0
        except Exception:
            # 回退到简单比较
            return VersionComparator._simple_compare(v1, v2)
    
    @staticmethod
    def _simple_compare(v1: str, v2: str) -> int:
        """简单版本比较"""
        try:
            parts1 = [int(x) for x in v1.split('.')]
            parts2 = [int(x) for x in v2.split('.')]
            
            # 补齐长度
            max_len = max(len(parts1), len(parts2))
            parts1.extend([0] * (max_len - len(parts1)))
            parts2.extend([0] * (max_len - len(parts2)))
            
            for p1, p2 in zip(parts1, parts2):
                if p1 < p2:
                    return -1
                elif p1 > p2:
                    return 1
            return 0
        except ValueError:
            return 0 if v1 == v2 else (-1 if v1 < v2 else 1)
    
    @staticmethod
    def is_newer(v1: str, v2: str) -> bool:
        """检查 v1 是否比 v2 新"""
        return VersionComparator.compare(v1, v2) > 0
    
    @staticmethod
    def filter_by_version_range(
        releases: List[Release],
        min_version: Optional[str] = None,
        max_version: Optional[str] = None
    ) -> List[Release]:
        """按版本范围过滤"""
        filtered = []
        
        for rel in releases:
            v = rel.version
            
            if min_version and VersionComparator.compare(v, min_version) < 0:
                continue
            if max_version and VersionComparator.compare(v, max_version) > 0:
                continue
            
            filtered.append(rel)
        
        return filtered


# =============================================================================
# 主控制器
# =============================================================================

class ReleaseChecker:
    """发布检查主控制器"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.http = HTTPClient(config, logger)
        self.github_fetcher = GitHubReleaseFetcher(config, self.http, logger)
        self.maven_fetcher = MavenReleaseFetcher(config, self.http, logger)
        
        # 数据目录
        self.data_dir = Path(config.get("storage", {}).get("data_dir", "./data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.cache_file = self.data_dir / config.get("storage", {}).get("release_cache_file", "release_cache.json")
        self.changelog_file = self.data_dir / config.get("storage", {}).get("changelog_file", "version_changelog.json")
    
    def load_cache(self) -> Dict:
        """加载缓存"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                self.logger.warning(f"加载缓存失败: {e}")
        return {"releases": {}, "last_check": None}
    
    def save_cache(self, releases: List[Release]) -> bool:
        """保存缓存"""
        try:
            cache_data = {
                "releases": {f"flink-{r.version}": r.to_dict() for r in releases},
                "last_check": datetime.now().isoformat(),
                "count": len(releases)
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            return True
        except IOError as e:
            self.logger.error(f"保存缓存失败: {e}")
            return False
    
    def load_changelog(self) -> Dict:
        """加载变更日志历史"""
        if self.changelog_file.exists():
            try:
                with open(self.changelog_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"history": []}
    
    def save_changelog_entry(self, result: ReleaseCheckResult) -> bool:
        """保存变更日志条目"""
        try:
            changelog = self.load_changelog()
            
            entry = {
                "timestamp": result.timestamp,
                "new_versions": [r.version for r in result.new_releases],
                "updated_versions": [r.version for r in result.updated_releases],
                "total_versions": len(result.all_releases)
            }
            
            changelog["history"].append(entry)
            # 保留最近 100 条
            changelog["history"] = changelog["history"][-100:]
            
            with open(self.changelog_file, 'w', encoding='utf-8') as f:
                json.dump(changelog, f, ensure_ascii=False, indent=2)
            
            return True
        except IOError as e:
            self.logger.error(f"保存变更日志失败: {e}")
            return False
    
    def check_releases(
        self,
        include_github: bool = True,
        include_maven: bool = True,
        version_filter: Optional[str] = None
    ) -> ReleaseCheckResult:
        """
        检查新版本发布
        
        Args:
            include_github: 是否包含 GitHub
            include_maven: 是否包含 Maven
            version_filter: 版本过滤表达式
            
        Returns:
            检查结果
        """
        all_releases = []
        errors = []
        
        # 1. 获取 GitHub Releases
        if include_github:
            try:
                gh_releases = self.github_fetcher.fetch_all_releases()
                all_releases.extend(gh_releases)
            except Exception as e:
                self.logger.error(f"GitHub 获取错误: {e}")
                errors.append(f"GitHub: {str(e)}")
        
        # 2. 获取 Maven 版本
        if include_maven:
            try:
                maven_releases = self.maven_fetcher.fetch_all_versions()
                all_releases.extend(maven_releases)
            except Exception as e:
                self.logger.error(f"Maven 获取错误: {e}")
                errors.append(f"Maven: {str(e)}")
        
        # 3. 合并和去重
        version_map = {}
        for rel in all_releases:
            v = rel.version
            if v not in version_map:
                version_map[v] = rel
            else:
                # 合并信息
                existing = version_map[v]
                if not existing.release_date and rel.release_date:
                    existing.release_date = rel.release_date
                if not existing.release_notes_url and rel.release_notes_url:
                    existing.release_notes_url = rel.release_notes_url
                if not existing.maven_url and rel.maven_url:
                    existing.maven_url = rel.maven_url
        
        all_releases = list(version_map.values())
        
        # 4. 应用版本过滤
        if version_filter:
            # 支持简单的通配符
            if version_filter.endswith('.*'):
                prefix = version_filter[:-2]
                all_releases = [r for r in all_releases if r.version.startswith(prefix)]
            elif '*' in version_filter:
                import fnmatch
                all_releases = [r for r in all_releases if fnmatch.fnmatch(r.version, version_filter)]
            else:
                # 范围过滤
                all_releases = VersionComparator.filter_by_version_range(
                    all_releases,
                    min_version=version_filter
                )
        
        # 5. 与缓存比较
        cache = self.load_cache()
        cached_versions = set(cache.get("releases", {}).keys())
        
        new_releases = []
        updated_releases = []
        
        for rel in all_releases:
            cache_key = f"flink-{rel.version}"
            
            if cache_key not in cached_versions:
                new_releases.append(rel)
                self.logger.info(f"发现新版本: {rel.version}")
            else:
                # 检查更新
                cached = cache["releases"].get(cache_key, {})
                if cached.get("release_date") != rel.release_date:
                    updated_releases.append(rel)
        
        # 6. 保存缓存和日志
        self.save_cache(all_releases)
        
        result = ReleaseCheckResult(
            success=len(errors) == 0 or len(all_releases) > 0,
            new_releases=new_releases,
            updated_releases=updated_releases,
            all_releases=all_releases,
            errors=errors,
            timestamp=datetime.now().isoformat()
        )
        
        self.save_changelog_entry(result)
        
        return result
    
    def export_results(self, result: ReleaseCheckResult, output_path: Optional[str] = None) -> str:
        """导出结果到文件"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.data_dir / f"releases_{timestamp}.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"结果已导出: {output_path}")
        return str(output_path)
    
    def generate_notification_content(self, result: ReleaseCheckResult) -> Dict:
        """生成通知内容"""
        return {
            "title": f"Flink 版本更新检测 - {datetime.now().strftime('%Y-%m-%d')}",
            "new_count": len(result.new_releases),
            "updated_count": len(result.updated_releases),
            "new_versions": [
                {
                    "version": r.version,
                    "date": r.release_date,
                    "features": len(r.new_features),
                    "fixes": len(r.bug_fixes)
                }
                for r in result.new_releases
            ],
            "summary": f"发现 {len(result.new_releases)} 个新版本，{len(result.updated_releases)} 个更新版本"
        }


# =============================================================================
# 命令行接口
# =============================================================================

def main():
    """主入口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Flink Release Checker - 检查 Flink 新版本发布",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          # 基础检查
  %(prog)s --github-only            # 只检查 GitHub
  %(prog)s --maven-only             # 只检查 Maven
  %(prog)s --filter 1.18.*          # 过滤 1.18.x 版本
  %(prog)s --notify                 # 检测到更新时发送通知
        """
    )
    
    parser.add_argument("-c", "--config", default="config.json",
                        help="配置文件路径")
    parser.add_argument("-o", "--output", default=None,
                        help="输出文件路径")
    parser.add_argument("--github-only", action="store_true",
                        help="只检查 GitHub Releases")
    parser.add_argument("--maven-only", action="store_true",
                        help="只检查 Maven Central")
    parser.add_argument("-f", "--filter", default=None,
                        help="版本过滤表达式 (如: 1.18.*, >=1.17)")
    parser.add_argument("--notify", action="store_true",
                        help="有新版本时发送通知")
    parser.add_argument("-l", "--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    parser.add_argument("--stable-only", action="store_true",
                        help="只显示稳定版本")
    
    args = parser.parse_args()
    
    # 检查依赖
    try:
        import packaging
    except ImportError:
        print("错误: 需要 packaging 库")
        print("安装: pip install packaging")
        sys.exit(1)
    
    # 设置日志
    logger = setup_logging(args.log_level)
    
    if not HAS_REQUESTS:
        logger.warning("未安装 requests 库，使用 urllib 作为后备")
    
    # 加载配置
    config = load_config(args.config)
    
    # 创建检查器
    checker = ReleaseChecker(config, logger)
    
    # 执行检查
    logger.info("=" * 60)
    logger.info("Flink Release Checker v1.0")
    logger.info("=" * 60)
    
    include_github = not args.maven_only
    include_maven = not args.github_only
    
    result = checker.check_releases(
        include_github=include_github,
        include_maven=include_maven,
        version_filter=args.filter
    )
    
    # 过滤稳定版本
    if args.stable_only:
        result.all_releases = [r for r in result.all_releases if r.is_stable]
        result.new_releases = [r for r in result.new_releases if r.is_stable]
    
    # 按版本排序
    result.all_releases.sort(key=lambda r: pkg_version.parse(r.version), reverse=True)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("检查结果:")
    print(f"  成功: {result.success}")
    print(f"  总版本数: {len(result.all_releases)}")
    print(f"  新版本: {len(result.new_releases)}")
    print(f"  更新版本: {len(result.updated_releases)}")
    
    if result.errors:
        print("\n错误:")
        for error in result.errors:
            print(f"  - {error}")
    
    if result.new_releases:
        print("\n新版本:")
        for rel in result.new_releases[:5]:
            print(f"  - {rel.version} ({rel.release_date or '日期未知'})")
            print(f"    {rel.release_notes_url or rel.maven_url or ''}")
    
    # 导出结果
    output = checker.export_results(result, args.output)
    print(f"\n结果已保存: {output}")
    
    # 生成通知内容
    if args.notify or result.new_releases:
        notification = checker.generate_notification_content(result)
        print("\n通知内容:")
        print(json.dumps(notification, ensure_ascii=False, indent=2))
    
    # 返回码
    return 0 if len(result.new_releases) == 0 else 2  # 2 表示发现新版本


if __name__ == "__main__":
    sys.exit(main())
