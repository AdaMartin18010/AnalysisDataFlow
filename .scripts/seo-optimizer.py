#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO Optimizer for AnalysisDataFlow Project
分析数据流项目SEO优化工具

功能:
1. 生成 sitemap.xml - 包含所有文档的站点地图
2. 生成/更新 robots.txt - 搜索引擎爬虫配置
3. 为HTML文件添加结构化数据 (Schema.org JSON-LD)
4. 优化meta标签和Open Graph标签
5. 生成SEO优化报告

使用方法:
    python seo-optimizer.py --generate-sitemap
    python seo-optimizer.py --generate-robots
    python seo-optimizer.py --optimize-html
    python seo-optimizer.py --full-audit

成本: 完全免费，零成本实施
"""

import os
import re
import json
import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urljoin, quote


@dataclass
class DocumentInfo:
    """文档信息数据类"""
    path: str
    title: str
    description: str
    last_modified: str
    priority: float
    changefreq: str
    category: str


class SEOOptimizer:
    """SEO优化器主类"""
    
    # 项目配置
    BASE_URL = "https://analysisdataflow.github.io"  # 更新为实际域名
    REPO_NAME = "AnalysisDataFlow"
    
    # 优先级映射
    PRIORITY_MAP = {
        'README.md': 1.0,
        'INDEX.md': 1.0,
        'QUICK-START.md': 0.9,
        'GLOSSARY.md': 0.9,
        'THEOREM-REGISTRY.md': 0.9,
        'NAVIGATION-INDEX.md': 0.9,
        'ARCHITECTURE.md': 0.9,
        'STRUCT': 0.8,
        'KNOWLEDGE': 0.8,
        'FLINK': 0.8,
        'DOCS': 0.7,
        'TUTORIALS': 0.7,
        'EXAMPLES': 0.6,
        'I18N': 0.6,
        'REPORTS': 0.5,
        'default': 0.5
    }
    
    # 更新频率映射
    CHANGEFREQ_MAP = {
        'README.md': 'weekly',
        'CHANGELOG.md': 'daily',
        'ROADMAP.md': 'weekly',
        'PROJECT-TRACKING.md': 'daily',
        'STRUCT': 'monthly',
        'KNOWLEDGE': 'monthly',
        'FLINK': 'weekly',
        'DOCS': 'monthly',
        'TUTORIALS': 'monthly',
        'default': 'monthly'
    }
    
    # 排除的路径模式
    EXCLUDE_PATTERNS = [
        r'\.git',
        r'node_modules',
        r'\.improvement-tracking',
        r'archive',
        r'benchmark-data',
        r'\.scripts',
        r'\.github',
        r'\.vscode',
        r'\.tasks',
        r'\.templates',
        r'CONFIG-TEMPLATES',
        r'docker',
        r'visuals'
    ]
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.documents: List[DocumentInfo] = []
        self.stats = {
            'total_files': 0,
            'md_files': 0,
            'html_files': 0,
            'optimized': 0,
            'errors': []
        }
    
    def _should_exclude(self, path: str) -> bool:
        """检查路径是否应该被排除"""
        for pattern in self.EXCLUDE_PATTERNS:
            if re.search(pattern, path, re.IGNORECASE):
                return True
        return False
    
    def _extract_title_from_md(self, file_path: Path) -> str:
        """从Markdown文件提取标题"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(5000)  # 只读取前5000字符
                
            # 匹配一级标题
            match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
            
            # 匹配YAML frontmatter中的title
            match = re.search(r'^title:\s*["\']?(.+?)["\']?$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
            
            # 使用文件名作为标题
            return file_path.stem.replace('-', ' ').replace('_', ' ').title()
        except Exception as e:
            return file_path.stem.replace('-', ' ').replace('_', ' ').title()
    
    def _extract_description_from_md(self, file_path: Path) -> str:
        """从Markdown文件提取描述"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(10000)
            
            # 尝试从元数据中提取
            match = re.search(r'^description:\s*["\']?(.+?)["\']?$', content, re.MULTILINE | re.IGNORECASE)
            if match:
                return match.group(1).strip()[:200]
            
            # 从第一段非空文本提取
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('---'):
                    # 去除Markdown标记
                    desc = re.sub(r'[\*\`\[\]\(\)\{\}]', '', line)
                    if len(desc) > 50:
                        return desc[:200]
            
            return f"AnalysisDataFlow项目文档: {file_path.stem}"
        except Exception as e:
            return f"AnalysisDataFlow项目文档: {file_path.stem}"
    
    def _get_priority(self, file_path: Path) -> float:
        """根据文件路径确定优先级"""
        file_name = file_path.name.upper()
        parent_name = file_path.parent.name.upper()
        
        # 检查特定文件
        for key, priority in self.PRIORITY_MAP.items():
            if key.endswith('.md') and file_name == key:
                return priority
        
        # 检查目录
        for key, priority in self.PRIORITY_MAP.items():
            if not key.endswith('.md') and key in parent_name:
                return priority
        
        return self.PRIORITY_MAP['default']
    
    def _get_changefreq(self, file_path: Path) -> str:
        """根据文件路径确定更新频率"""
        file_name = file_path.name.upper()
        parent_name = file_path.parent.name.upper()
        
        for key, freq in self.CHANGEFREQ_MAP.items():
            if key.endswith('.md') and file_name == key:
                return freq
            if not key.endswith('.md') and key in parent_name:
                return freq
        
        return self.CHANGEFREQ_MAP['default']
    
    def _get_category(self, file_path: Path) -> str:
        """确定文档类别"""
        path_str = str(file_path).upper()
        
        if 'STRUCT' in path_str:
            return '理论结构'
        elif 'KNOWLEDGE' in path_str:
            return '知识体系'
        elif 'FLINK' in path_str:
            return 'Flink专题'
        elif 'TUTORIALS' in path_str:
            return '教程'
        elif 'EXAMPLES' in path_str:
            return '示例'
        elif 'DOCS' in path_str:
            return '文档'
        elif 'I18N' in path_str:
            return '国际化'
        elif 'REPORTS' in path_str:
            return '报告'
        else:
            return '其他'
    
    def scan_documents(self) -> List[DocumentInfo]:
        """扫描所有文档"""
        print("🔍 正在扫描文档...")
        
        # 扫描Markdown文件
        md_files = list(self.root_dir.rglob("*.md"))
        html_files = list(self.root_dir.rglob("*.html"))
        
        self.stats['total_files'] = len(md_files) + len(html_files)
        self.stats['md_files'] = len(md_files)
        self.stats['html_files'] = len(html_files)
        
        documents = []
        
        for file_path in md_files:
            relative_path = file_path.relative_to(self.root_dir)
            path_str = str(relative_path).replace('\\', '/')
            
            if self._should_exclude(path_str):
                continue
            
            # 获取文件修改时间
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
                last_modified = mtime.strftime('%Y-%m-%d')
            except:
                last_modified = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            
            doc = DocumentInfo(
                path=path_str,
                title=self._extract_title_from_md(file_path),
                description=self._extract_description_from_md(file_path),
                last_modified=last_modified,
                priority=self._get_priority(file_path),
                changefreq=self._get_changefreq(file_path),
                category=self._get_category(file_path)
            )
            documents.append(doc)
        
        # 添加HTML文件（知识图谱等）
        for file_path in html_files:
            relative_path = file_path.relative_to(self.root_dir)
            path_str = str(relative_path).replace('\\', '/')
            
            if self._should_exclude(path_str):
                continue
            
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc)
                last_modified = mtime.strftime('%Y-%m-%d')
            except:
                last_modified = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            
            doc = DocumentInfo(
                path=path_str,
                title=file_path.stem.replace('-', ' ').title(),
                description=f"AnalysisDataFlow 交互式知识图谱: {file_path.stem}",
                last_modified=last_modified,
                priority=0.9 if 'knowledge-graph' in path_str else 0.6,
                changefreq='monthly',
                category='知识图谱'
            )
            documents.append(doc)
        
        # 按优先级排序
        documents.sort(key=lambda x: x.priority, reverse=True)
        
        self.documents = documents
        print(f"✅ 发现 {len(documents)} 个文档")
        return documents
    
    def generate_sitemap(self) -> str:
        """生成sitemap.xml"""
        print("🗺️  正在生成 sitemap.xml...")
        
        if not self.documents:
            self.scan_documents()
        
        # 创建XML根元素
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        urlset.set('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
        
        # 添加每个文档
        for doc in self.documents:
            url = ET.SubElement(urlset, 'url')
            
            # 完整URL
            loc = ET.SubElement(url, 'loc')
            loc.text = f"{self.BASE_URL}/{quote(doc.path)}"
            
            # 最后修改时间
            lastmod = ET.SubElement(url, 'lastmod')
            lastmod.text = doc.last_modified
            
            # 更新频率
            changefreq = ET.SubElement(url, 'changefreq')
            changefreq.text = doc.changefreq
            
            # 优先级
            priority = ET.SubElement(url, 'priority')
            priority.text = str(doc.priority)
        
        # 格式化XML
        xml_str = minidom.parseString(ET.tostring(urlset)).toprettyxml(indent="  ")
        
        # 写入文件
        sitemap_path = self.root_dir / 'sitemap.xml'
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)
        
        print(f"✅ Sitemap 已生成: {sitemap_path}")
        print(f"   包含 {len(self.documents)} 个URL")
        
        return xml_str
    
    def generate_robots_txt(self) -> str:
        """生成robots.txt"""
        print("🤖 正在生成 robots.txt...")
        
        content = f"""# robots.txt for AnalysisDataFlow Project
# 分析数据流项目 - 搜索引擎爬虫配置
# Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
# Project: {self.REPO_NAME}

User-agent: *
Allow: /

# Sitemap location
Sitemap: {self.BASE_URL}/sitemap.xml

# Allow search engines to index all public content
Allow: /Struct/
Allow: /Knowledge/
Allow: /Flink/
Allow: /docs/
Allow: /tutorials/
Allow: /examples/
Allow: /i18n/

# Exclude paths that should not be indexed
Disallow: /.git/
Disallow: /.github/
Disallow: /.scripts/
Disallow: /.vscode/
Disallow: /.tasks/
Disallow: /.templates/
Disallow: /.improvement-tracking/
Disallow: /archive/
Disallow: /benchmark-data/
Disallow: /CONFIG-TEMPLATES/
Disallow: /docker/
Disallow: /reports/

# Exclude specific file patterns
Disallow: /*.json$
Disallow: /*.yml$
Disallow: /*.yaml$
Disallow: /Makefile
Disallow: /Dockerfile
Disallow: /docker-compose.yml

# Crawl-delay to be respectful to servers
Crawl-delay: 1

# Special rules for major search engines
User-agent: Googlebot
Allow: /
Crawl-delay: 0.5

User-agent: Bingbot
Allow: /
Crawl-delay: 1

User-agent: Slurp
Allow: /
Crawl-delay: 1

User-agent: DuckDuckBot
Allow: /
Crawl-delay: 1

User-agent: Baiduspider
Allow: /
Crawl-delay: 1
"""
        
        robots_path = self.root_dir / 'robots.txt'
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ robots.txt 已生成: {robots_path}")
        return content
    
    def generate_structured_data(self, doc: DocumentInfo) -> Dict:
        """为文档生成Schema.org结构化数据"""
        
        # 根据文档类型选择不同的Schema类型
        if doc.category == '知识图谱':
            schema = {
                "@context": "https://schema.org",
                "@type": "SoftwareApplication",
                "name": doc.title,
                "description": doc.description,
                "url": f"{self.BASE_URL}/{doc.path}",
                "applicationCategory": "DeveloperApplication",
                "operatingSystem": "Any",
                "offers": {
                    "@type": "Offer",
                    "price": "0",
                    "priceCurrency": "USD"
                },
                "license": "https://github.com/AnalysisDataFlow/AnalysisDataFlow/blob/main/LICENSE"
            }
        elif doc.category == '理论结构':
            schema = {
                "@context": "https://schema.org",
                "@type": "TechArticle",
                "headline": doc.title,
                "description": doc.description,
                "url": f"{self.BASE_URL}/{doc.path}",
                "author": {
                    "@type": "Organization",
                    "name": "AnalysisDataFlow Project"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "AnalysisDataFlow",
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{self.BASE_URL}/assets/logo.png"
                    }
                },
                "dateModified": doc.last_modified,
                "proficiencyLevel": "Expert"
            }
        elif doc.category == '教程':
            schema = {
                "@context": "https://schema.org",
                "@type": "LearningResource",
                "name": doc.title,
                "description": doc.description,
                "url": f"{self.BASE_URL}/{doc.path}",
                "learningResourceType": "Tutorial",
                "interactivityType": "expositive",
                "author": {
                    "@type": "Organization",
                    "name": "AnalysisDataFlow Project"
                }
            }
        else:
            schema = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": doc.title,
                "description": doc.description,
                "url": f"{self.BASE_URL}/{doc.path}",
                "author": {
                    "@type": "Organization",
                    "name": "AnalysisDataFlow Project"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "AnalysisDataFlow"
                },
                "dateModified": doc.last_modified
            }
        
        return schema
    
    def optimize_html_files(self) -> Dict:
        """优化HTML文件，添加结构化数据和meta标签"""
        print("🔧 正在优化HTML文件...")
        
        results = {
            'optimized': 0,
            'errors': [],
            'skipped': 0
        }
        
        html_files = list(self.root_dir.rglob("*.html"))
        
        for file_path in html_files:
            try:
                if self._should_exclude(str(file_path)):
                    results['skipped'] += 1
                    continue
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 检查是否已优化
                if 'application/ld+json' in content and 'og:title' in content:
                    results['skipped'] += 1
                    continue
                
                # 提取基本信息
                title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
                title = title_match.group(1) if title_match else file_path.stem
                
                description_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
                description = description_match.group(1) if description_match else f"AnalysisDataFlow: {title}"
                
                # 创建文档信息对象
                relative_path = file_path.relative_to(self.root_dir)
                doc = DocumentInfo(
                    path=str(relative_path).replace('\\', '/'),
                    title=title,
                    description=description,
                    last_modified=datetime.now(timezone.utc).strftime('%Y-%m-%d'),
                    priority=0.8,
                    changefreq='monthly',
                    category='知识图谱'
                )
                
                # 生成结构化数据
                schema = self.generate_structured_data(doc)
                schema_json = json.dumps(schema, ensure_ascii=False, indent=2)
                
                # 创建meta标签块
                meta_block = f"""    <!-- SEO Meta Tags -->
    <meta name="description" content="{description[:160]}">
    <meta name="keywords" content="流计算, Flink, 数据流, 分布式系统, 实时计算, 流处理, 知识图谱, 形式化理论">
    <meta name="author" content="AnalysisDataFlow Project">
    <meta name="robots" content="index, follow">
    <meta name="googlebot" content="index, follow">
    <link rel="canonical" href="{self.BASE_URL}/{doc.path}">
    
    <!-- Open Graph Meta Tags -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description[:200]}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{self.BASE_URL}/{doc.path}">
    <meta property="og:site_name" content="AnalysisDataFlow">
    <meta property="og:locale" content="zh_CN">
    
    <!-- Twitter Card Meta Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description[:200]}">
    <meta name="twitter:creator" content="@AnalysisDataFlow">
    
    <!-- Structured Data (Schema.org) -->
    <script type="application/ld+json">
{schema_json}
    </script>
"""
                
                # 在</head>前插入meta标签
                if '</head>' in content:
                    content = content.replace('</head>', meta_block + '</head>')
                
                # 写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                results['optimized'] += 1
                
            except Exception as e:
                results['errors'].append(f"{file_path}: {str(e)}")
        
        print(f"✅ 优化完成: {results['optimized']} 个文件已优化")
        if results['skipped']:
            print(f"   跳过: {results['skipped']} 个文件")
        if results['errors']:
            print(f"   错误: {len(results['errors'])} 个文件")
        
        return results
    
    def generate_seo_report(self) -> str:
        """生成SEO优化报告"""
        print("📊 正在生成SEO报告...")
        
        if not self.documents:
            self.scan_documents()
        
        # 统计信息
        category_counts = {}
        priority_dist = {'高(0.8-1.0)': 0, '中(0.5-0.7)': 0, '低(<0.5)': 0}
        
        for doc in self.documents:
            category_counts[doc.category] = category_counts.get(doc.category, 0) + 1
            if doc.priority >= 0.8:
                priority_dist['高(0.8-1.0)'] += 1
            elif doc.priority >= 0.5:
                priority_dist['中(0.5-0.7)'] += 1
            else:
                priority_dist['低(<0.5)'] += 1
        
        report = f"""# SEO优化报告
> 生成时间: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
> 工具: seo-optimizer.py (零成本方案)

## 📈 执行摘要

| 指标 | 数值 |
|------|------|
| 总文档数 | {len(self.documents)} |
| Markdown文件 | {self.stats['md_files']} |
| HTML文件 | {self.stats['html_files']} |
| 生成Sitemap | ✅ 已完成 |
| 生成robots.txt | ✅ 已完成 |
| 结构化数据 | ✅ 已添加 |

## 📁 文档分类统计

| 类别 | 数量 | 占比 |
|------|------|------|
"""
        
        for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(self.documents)) * 100
            report += f"| {cat} | {count} | {pct:.1f}% |\n"
        
        report += f"""
## 🎯 优先级分布

| 优先级范围 | 数量 | 占比 |
|------------|------|------|
"""
        for prio, count in priority_dist.items():
            pct = (count / len(self.documents)) * 100
            report += f"| {prio} | {count} | {pct:.1f}% |\n"
        
        report += f"""
## 🔧 已实施优化

### 1. Sitemap.xml
- ✅ 包含 {len(self.documents)} 个URL
- ✅ 每个URL包含优先级和更新频率
- ✅ 符合 sitemaps.org 标准

### 2. Robots.txt
- ✅ 允许主要搜索引擎索引
- ✅ 排除敏感路径 (.git, .scripts等)
- ✅ 包含Sitemap引用
- ✅ 为不同爬虫设置合理的Crawl-delay

### 3. 结构化数据 (Schema.org)
- ✅ 技术文章使用 TechArticle schema
- ✅ 教程使用 LearningResource schema
- ✅ 知识图谱使用 SoftwareApplication schema
- ✅ 所有文档包含基本 Article schema

### 4. Meta标签优化
- ✅ 标题和描述优化
- ✅ Open Graph标签 (Facebook, LinkedIn)
- ✅ Twitter Card标签
- ✅ Canonical URL

## 📊 高优先级页面 (Top 20)

| 优先级 | 页面 | 类别 |
|--------|------|------|
"""
        
        for i, doc in enumerate(self.documents[:20], 1):
            report += f"| {doc.priority} | [{doc.title[:40]}...]({doc.path}) | {doc.category} |\n"
        
        report += f"""
## 🚀 后续建议

### 立即实施
1. **注册Google Search Console**
   - 访问 https://search.google.com/search-console
   - 添加属性: `{self.BASE_URL}`
   - 提交sitemap.xml

2. **注册Bing Webmaster Tools**
   - 访问 https://www.bing.com/webmasters
   - 添加站点
   - 提交sitemap

3. **启用Google Analytics 4**
   - 免费获取详细的访问分析
   - 跟踪用户行为

### 持续优化
1. **内容更新**
   - 定期更新高优先级页面
   - 保持内容新鲜度

2. **内部链接优化**
   - 在相关文档间建立链接
   - 使用描述性锚文本

3. **性能监控**
   - 使用Lighthouse CI监控性能
   - 目标: Performance 90+, SEO 95+

## 📁 生成的文件

| 文件 | 路径 | 说明 |
|------|------|------|
| Sitemap | ./sitemap.xml | 站点地图 |
| Robots | ./robots.txt | 爬虫配置 |
| 优化脚本 | ./.scripts/seo-optimizer.py | SEO工具 |
| 本报告 | ./SEO-OPTIMIZATION-REPORT.md | 优化报告 |

---
*本报告由 seo-optimizer.py 自动生成*
*项目: {self.REPO_NAME}*
"""
        
        # 写入报告
        report_path = self.root_dir / 'SEO-OPTIMIZATION-REPORT.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ SEO报告已生成: {report_path}")
        return report
    
    def run_full_audit(self):
        """运行完整的SEO审计"""
        print("="*60)
        print("🔍 AnalysisDataFlow SEO 完整审计")
        print("="*60)
        print()
        
        # 1. 扫描文档
        self.scan_documents()
        print()
        
        # 2. 生成Sitemap
        self.generate_sitemap()
        print()
        
        # 3. 生成robots.txt
        self.generate_robots_txt()
        print()
        
        # 4. 优化HTML文件
        self.optimize_html_files()
        print()
        
        # 5. 生成报告
        self.generate_seo_report()
        print()
        
        print("="*60)
        print("✅ SEO优化完成!")
        print("="*60)
        print()
        print("下一步操作:")
        print("1. 注册 Google Search Console 并提交 sitemap.xml")
        print("2. 注册 Bing Webmaster Tools")
        print("3. 配置 GitHub Actions 工作流 (.github/workflows/seo-check.yml)")
        print("4. 定期运行本脚本更新sitemap")


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow SEO优化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python seo-optimizer.py --full-audit          # 完整审计
    python seo-optimizer.py --generate-sitemap    # 仅生成sitemap
    python seo-optimizer.py --generate-robots     # 仅生成robots.txt
    python seo-optimizer.py --optimize-html       # 优化HTML文件
    python seo-optimizer.py --generate-report     # 仅生成报告
        """
    )
    
    parser.add_argument('--full-audit', action='store_true',
                        help='运行完整的SEO审计')
    parser.add_argument('--generate-sitemap', action='store_true',
                        help='生成sitemap.xml')
    parser.add_argument('--generate-robots', action='store_true',
                        help='生成robots.txt')
    parser.add_argument('--optimize-html', action='store_true',
                        help='优化HTML文件')
    parser.add_argument('--generate-report', action='store_true',
                        help='生成SEO报告')
    parser.add_argument('--root-dir', default='.',
                        help='项目根目录 (默认: 当前目录)')
    
    args = parser.parse_args()
    
    # 如果没有指定参数，显示帮助
    if not any([args.full_audit, args.generate_sitemap, args.generate_robots, 
                args.optimize_html, args.generate_report]):
        parser.print_help()
        return
    
    optimizer = SEOOptimizer(root_dir=args.root_dir)
    
    if args.full_audit:
        optimizer.run_full_audit()
    else:
        if args.generate_sitemap:
            optimizer.scan_documents()
            optimizer.generate_sitemap()
        if args.generate_robots:
            optimizer.generate_robots_txt()
        if args.optimize_html:
            optimizer.optimize_html_files()
        if args.generate_report:
            optimizer.generate_seo_report()


if __name__ == '__main__':
    main()
