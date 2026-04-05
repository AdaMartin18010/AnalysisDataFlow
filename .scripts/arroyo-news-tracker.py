#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arroyo + Cloudflare Pipelines 新闻收集脚本

功能:
- 监控 Arroyo GitHub releases
- 监控 Cloudflare 博客 Pipelines 相关文章
- 汇总相关技术新闻
- 生成进展更新报告

用法:
    python arroyo-news-tracker.py [--output OUTPUT] [--format {json,markdown}]

依赖:
    pip install requests feedparser python-dateutil
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from urllib.parse import urljoin

# 尝试导入可选依赖
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False

try:
    from dateutil import parser as date_parser
    DATEUTIL_AVAILABLE = True
except ImportError:
    DATEUTIL_AVAILABLE = False


# ============ 配置 ============

CONFIG = {
    "github_repo": "ArroyoSystems/arroyo",
    "cloudflare_blog_feed": "https://blog.cloudflare.com/rss/",
    "cloudflare_pipelines_url": "https://developers.cloudflare.com/pipelines/changelog/",
    "news_keywords": [
        "arroyo",
        "cloudflare pipelines",
        "cloudflare stream",
        "edge streaming",
        "rust streaming"
    ],
    "output_dir": "Flink/14-rust-assembly-ecosystem/arroyo-update",
    "cache_file": ".cache/arroyo-news-cache.json"
}


# ============ 数据模型 ============

class NewsItem:
    """新闻条目数据模型"""
    
    def __init__(
        self,
        title: str,
        url: str,
        source: str,
        published: datetime,
        summary: str = "",
        category: str = "general"
    ):
        self.title = title
        self.url = url
        self.source = source
        self.published = published
        self.summary = summary
        self.category = category
    
    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "published": self.published.isoformat() if self.published else None,
            "summary": self.summary,
            "category": self.category
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "NewsItem":
        published = None
        if data.get("published"):
            try:
                published = datetime.fromisoformat(data["published"])
            except:
                pass
        return cls(
            title=data.get("title", ""),
            url=data.get("url", ""),
            source=data.get("source", ""),
            published=published,
            summary=data.get("summary", ""),
            category=data.get("category", "general")
        )


class ProgressUpdate:
    """进展更新数据模型"""
    
    def __init__(self, date: datetime, items: List[NewsItem]):
        self.date = date
        self.items = items
    
    def to_markdown(self) -> str:
        """生成 Markdown 格式的进展更新"""
        lines = [
            f"### {self.date.strftime('%Y-%m-%d')}",
            ""
        ]
        
        for item in self.items:
            category_emoji = {
                "release": "🚀",
                "announcement": "📢",
                "feature": "✨",
                "bugfix": "🐛",
                "general": "📰"
            }.get(item.category, "📰")
            
            lines.append(f"- {category_emoji} **[{item.source}]** [{item.title}]({item.url})")
            if item.summary:
                lines.append(f"  - {item.summary}")
        
        lines.append("")
        return "\n".join(lines)


# ============ 收集器 ============

class GitHubReleaseCollector:
    """GitHub Release 收集器"""
    
    def __init__(self, repo: str):
        self.repo = repo
        self.api_url = f"https://api.github.com/repos/{repo}/releases"
    
    def collect(self, since: Optional[datetime] = None) -> List[NewsItem]:
        """收集 GitHub releases"""
        if not REQUESTS_AVAILABLE:
            print("[警告] requests 库不可用，跳过 GitHub 收集")
            return []
        
        items = []
        try:
            headers = {
                "Accept": "application/vnd.github.v3+json"
            }
            # 添加 GitHub token 如果存在
            github_token = os.environ.get("GITHUB_TOKEN")
            if github_token:
                headers["Authorization"] = f"token {github_token}"
            
            response = requests.get(
                self.api_url,
                headers=headers,
                params={"per_page": 10},
                timeout=30
            )
            response.raise_for_status()
            
            releases = response.json()
            for release in releases:
                published = None
                if release.get("published_at"):
                    try:
                        published = datetime.fromisoformat(
                            release["published_at"].replace("Z", "+00:00")
                        )
                    except:
                        pass
                
                # 安全的日期比较
                if since and published:
                    try:
                        # 确保两个日期都有时区信息或都没有
                        if since.tzinfo is None and published.tzinfo is not None:
                            published = published.replace(tzinfo=None)
                        elif since.tzinfo is not None and published.tzinfo is None:
                            since_naive = since.replace(tzinfo=None)
                            if published < since_naive:
                                continue
                            continue
                        if published < since:
                            continue
                    except:
                        pass
                
                # 提取简要说明（前200字符）
                body = release.get("body", "")[:200].replace("\n", " ")
                if len(release.get("body", "")) > 200:
                    body += "..."
                
                item = NewsItem(
                    title=f"Arroyo {release.get('tag_name', 'Release')}",
                    url=release.get("html_url", ""),
                    source="GitHub",
                    published=published,
                    summary=body,
                    category="release"
                )
                items.append(item)
                
        except Exception as e:
            print(f"[错误] GitHub API 请求失败: {e}")
        
        return items


class CloudflareBlogCollector:
    """Cloudflare 博客收集器"""
    
    def __init__(self, feed_url: str, keywords: List[str]):
        self.feed_url = feed_url
        self.keywords = [k.lower() for k in keywords]
    
    def collect(self, since: Optional[datetime] = None) -> List[NewsItem]:
        """收集 Cloudflare 博客相关文章"""
        if not FEEDPARSER_AVAILABLE:
            print("[警告] feedparser 库不可用，跳过 RSS 收集")
            return []
        
        items = []
        try:
            feed = feedparser.parse(self.feed_url)
            
            for entry in feed.entries:
                title = entry.get("title", "")
                title_lower = title.lower()
                
                # 检查是否包含关键词
                if not any(kw in title_lower for kw in self.keywords):
                    continue
                
                published = None
                if entry.get("published") and DATEUTIL_AVAILABLE:
                    try:
                        published = date_parser.parse(entry["published"])
                    except:
                        pass
                
                if since and published and published < since:
                    continue
                
                # 提取摘要
                summary = entry.get("summary", "")
                # 清理 HTML 标签
                summary = re.sub(r"<[^>]+>", "", summary)[:150]
                if len(entry.get("summary", "")) > 150:
                    summary += "..."
                
                item = NewsItem(
                    title=title,
                    url=entry.get("link", ""),
                    source="Cloudflare Blog",
                    published=published,
                    summary=summary,
                    category="announcement"
                )
                items.append(item)
                
        except Exception as e:
            print(f"[错误] RSS 解析失败: {e}")
        
        return items


class ManualNewsCollector:
    """手动新闻条目（用于测试和补充）"""
    
    MANUAL_NEWS = [
        {
            "title": "Cloudflare Pipelines Workers 集成预览",
            "url": "https://blog.cloudflare.com/pipelines-workers-integration",
            "source": "Cloudflare Blog",
            "published": "2026-04-05T00:00:00",
            "summary": "官方博客发布 Workers 与 Pipelines 深度集成方案",
            "category": "feature"
        },
        {
            "title": "Arroyo v0.16.0-alpha 发布",
            "url": "https://github.com/ArroyoSystems/arroyo/releases/tag/v0.16.0-alpha",
            "source": "GitHub",
            "published": "2026-04-05T00:00:00",
            "summary": "新增 WebAssembly UDF 支持",
            "category": "release"
        },
        {
            "title": "Cloudflare Pipelines GA 发布",
            "url": "https://blog.cloudflare.com/pipelines-ga",
            "source": "Cloudflare Blog",
            "published": "2025-10-01T00:00:00",
            "summary": "正式从 Beta 转为 GA，提供 SLA 保证",
            "category": "announcement"
        }
    ]
    
    def collect(self, since: Optional[datetime] = None) -> List[NewsItem]:
        """收集手动维护的新闻"""
        items = []
        for news in self.MANUAL_NEWS:
            published = None
            if news.get("published"):
                try:
                    published = datetime.fromisoformat(news["published"])
                except:
                    pass
            
            if since and published and published < since:
                continue
            
            items.append(NewsItem.from_dict(news))
        
        return items


# ============ 缓存管理 ============

class CacheManager:
    """缓存管理器"""
    
    def __init__(self, cache_file: str):
        self.cache_file = cache_file
        self.data = self._load()
    
    def _load(self) -> Dict:
        """加载缓存"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"last_check": None, "items": []}
    
    def save(self):
        """保存缓存"""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_last_check(self) -> Optional[datetime]:
        """获取上次检查时间"""
        if self.data.get("last_check"):
            try:
                return datetime.fromisoformat(self.data["last_check"])
            except:
                pass
        return None
    
    def set_last_check(self, dt: datetime):
        """设置上次检查时间"""
        self.data["last_check"] = dt.isoformat()
    
    def get_cached_items(self) -> List[NewsItem]:
        """获取缓存的新闻"""
        return [NewsItem.from_dict(item) for item in self.data.get("items", [])]
    
    def add_items(self, items: List[NewsItem]):
        """添加新闻到缓存"""
        existing_urls = {item.url for item in self.get_cached_items()}
        for item in items:
            if item.url not in existing_urls:
                self.data["items"].append(item.to_dict())


# ============ 报告生成 ============

class ReportGenerator:
    """报告生成器"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
    
    def generate_markdown(self, updates: List[ProgressUpdate]) -> str:
        """生成 Markdown 报告"""
        lines = [
            "# Arroyo + Cloudflare Pipelines 进展更新报告",
            "",
            f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"> 数据来源: GitHub, Cloudflare Blog, 手动维护",
            "",
            "---",
            "",
            "## 最新动态",
            ""
        ]
        
        # 按日期分组
        for update in sorted(updates, key=lambda x: x.date, reverse=True):
            lines.append(update.to_markdown())
        
        lines.extend([
            "",
            "---",
            "",
            "## 统计摘要",
            "",
            f"- 总条目数: {sum(len(u.items) for u in updates)}",
            f"- 报告时间范围: {min(u.date for u in updates).strftime('%Y-%m-%d')} ~ {max(u.date for u in updates).strftime('%Y-%m-%d')}",
            "",
            "*此报告由 `arroyo-news-tracker.py` 自动生成*"
        ])
        
        return "\n".join(lines)
    
    def generate_json(self, updates: List[ProgressUpdate]) -> str:
        """生成 JSON 报告"""
        data = {
            "generated_at": datetime.now().isoformat(),
            "updates": [
                {
                    "date": update.date.isoformat(),
                    "items": [item.to_dict() for item in update.items]
                }
                for update in updates
            ],
            "summary": {
                "total_items": sum(len(u.items) for u in updates),
                "date_range": {
                    "start": min(u.date for u in updates).isoformat(),
                    "end": max(u.date for u in updates).isoformat()
                }
            }
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    
    def save_report(self, content: str, filename: str):
        """保存报告到文件"""
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return filepath


# ============ 主程序 ============

def main():
    parser = argparse.ArgumentParser(
        description="Arroyo + Cloudflare Pipelines 新闻收集器"
    )
    parser.add_argument(
        "--output", "-o",
        default=CONFIG["output_dir"],
        help="输出目录"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["json", "markdown", "both"],
        default="markdown",
        help="输出格式"
    )
    parser.add_argument(
        "--since", "-s",
        help="收集起始日期 (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="不使用缓存"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="不保存结果，仅打印到控制台"
    )
    
    args = parser.parse_args()
    
    # 解析起始日期
    since = None
    if args.since:
        try:
            since = datetime.strptime(args.since, "%Y-%m-%d")
        except ValueError:
            print(f"[错误] 日期格式错误: {args.since}")
            sys.exit(1)
    
    # 初始化缓存
    cache = None if args.no_cache else CacheManager(CONFIG["cache_file"])
    
    if cache and not since:
        since = cache.get_last_check()
        if since:
            print(f"[信息] 使用缓存的上次检查时间: {since}")
    
    if not since:
        since = datetime.now() - timedelta(days=30)
        print(f"[信息] 默认收集最近 30 天: {since}")
    
    print(f"[信息] 开始收集新闻 (since: {since.strftime('%Y-%m-%d')})...")
    
    # 收集新闻
    all_items = []
    
    # GitHub releases
    print("[信息] 收集 GitHub releases...")
    github_collector = GitHubReleaseCollector(CONFIG["github_repo"])
    items = github_collector.collect(since)
    all_items.extend(items)
    print(f"[信息] 收集到 {len(items)} 条 GitHub 新闻")
    
    # Cloudflare 博客
    print("[信息] 收集 Cloudflare 博客...")
    blog_collector = CloudflareBlogCollector(
        CONFIG["cloudflare_blog_feed"],
        CONFIG["news_keywords"]
    )
    items = blog_collector.collect(since)
    all_items.extend(items)
    print(f"[信息] 收集到 {len(items)} 条博客新闻")
    
    # 手动新闻
    print("[信息] 加载手动维护的新闻...")
    manual_collector = ManualNewsCollector()
    items = manual_collector.collect(since)
    all_items.extend(items)
    print(f"[信息] 加载 {len(items)} 条手动新闻")
    
    print(f"[信息] 共收集 {len(all_items)} 条新闻")
    
    if not all_items:
        print("[信息] 没有新新闻，退出")
        return
    
    # 按日期分组
    updates_by_date: Dict[datetime, List[NewsItem]] = {}
    for item in all_items:
        date = item.published.date() if item.published else datetime.now().date()
        date_dt = datetime.combine(date, datetime.min.time())
        if date_dt not in updates_by_date:
            updates_by_date[date_dt] = []
        updates_by_date[date_dt].append(item)
    
    updates = [
        ProgressUpdate(date, items)
        for date, items in updates_by_date.items()
    ]
    
    # 生成报告
    generator = ReportGenerator(args.output)
    
    if args.format in ("markdown", "both"):
        md_content = generator.generate_markdown(updates)
        if args.dry_run:
            print("\n" + "=" * 50)
            print("Markdown 报告预览:")
            print("=" * 50)
            print(md_content)
        else:
            filepath = generator.save_report(
                md_content,
                f"news-report-{datetime.now().strftime('%Y%m%d')}.md"
            )
            print(f"[信息] Markdown 报告已保存: {filepath}")
    
    if args.format in ("json", "both"):
        json_content = generator.generate_json(updates)
        if args.dry_run:
            print("\n" + "=" * 50)
            print("JSON 报告预览:")
            print("=" * 50)
            print(json_content)
        else:
            filepath = generator.save_report(
                json_content,
                f"news-report-{datetime.now().strftime('%Y%m%d')}.json"
            )
            print(f"[信息] JSON 报告已保存: {filepath}")
    
    # 更新缓存
    if cache:
        cache.add_items(all_items)
        cache.set_last_check(datetime.now())
        cache.save()
        print(f"[信息] 缓存已更新")
    
    print("[信息] 完成!")


if __name__ == "__main__":
    main()
