#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate-sitemap.py
扫描 AnalysisDataFlow 项目核心 .md 文件与知识图谱节点，
生成 KNOWLEDGE-GRAPH/sitemap-full.xml（≥200 个 URL）。
"""

import os
import sys
import json
import glob
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KG_DIR = os.path.join(PROJECT_ROOT, "KNOWLEDGE-GRAPH")
OUTPUT_PATH = os.path.join(KG_DIR, "sitemap-full.xml")

# 基础配置
SITE_BASE = "https://analysisdataflow.github.io/AnalysisDataFlow"
GITHUB_BLOB_BASE = "https://github.com/AnalysisDataFlow/AnalysisDataFlow/blob/main"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# 核心内容目录（相对根目录）
CORE_DIRS = [
    "Struct",
    "Knowledge",
    "Flink",
    "en",
    "LEARNING-PATHS",
    "COMMUNITY",
    "docs",
    "formal-methods",
    "formal-proofs",
]

# 排除的文件名/目录片段
EXCLUDE_PATTERNS = {
    "README.md",
    "00-INDEX.md",
    "TEMPLATE.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "LICENSE",
    "archive",
    "node_modules",
    ".git",
    ".github",
    ".vscode",
    ".scripts",
    ".tasks",
    ".templates",
    ".improvement-tracking",
    "AcotorCSPWorkflow",
    "knowledge-graph-site",
}


def is_excluded(rel_path: str) -> bool:
    parts = rel_path.replace("\\", "/").split("/")
    for part in parts:
        if part in EXCLUDE_PATTERNS:
            return True
    filename = parts[-1]
    if filename.startswith(".") or filename.startswith("_"):
        return True
    return False


def collect_md_files() -> list:
    urls = []
    for core_dir in CORE_DIRS:
        abs_dir = os.path.join(PROJECT_ROOT, core_dir)
        if not os.path.isdir(abs_dir):
            continue
        for root, dirs, files in os.walk(abs_dir):
            # 排除隐藏/系统目录
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in EXCLUDE_PATTERNS]
            for f in files:
                if not f.endswith(".md"):
                    continue
                abs_path = os.path.join(root, f)
                rel_path = os.path.relpath(abs_path, PROJECT_ROOT).replace("\\", "/")
                if is_excluded(rel_path):
                    continue
                # 使用 GitHub 永久链接作为文档 URL（这些页面在 GitHub 上可直接渲染阅读）
                loc = f"{GITHUB_BLOB_BASE}/{rel_path}"
                urls.append({
                    "loc": loc,
                    "lastmod": TODAY,
                    "changefreq": "monthly",
                    "priority": "0.6",
                })
    return urls


def collect_kg_nodes() -> list:
    """从 KNOWLEDGE-GRAPH/data/*.json 中提取节点，生成应用内 hash URL。"""
    urls = []
    data_dir = os.path.join(KG_DIR, "data")
    if not os.path.isdir(data_dir):
        return urls

    node_ids = set()
    for json_file in glob.glob(os.path.join(data_dir, "*.json")):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        nodes = data.get("nodes", [])
        if not nodes and isinstance(data, list):
            # 有些文件可能直接是节点数组
            nodes = data
        for node in nodes:
            if isinstance(node, dict):
                nid = node.get("id")
                if nid and isinstance(nid, str):
                    node_ids.add(nid)

    for nid in sorted(node_ids):
        loc = f"{SITE_BASE}/#{nid}"
        urls.append({
            "loc": loc,
            "lastmod": TODAY,
            "changefreq": "weekly",
            "priority": "0.8",
        })
    return urls


def build_xml(urls: list) -> str:
    urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    # 首页
    home = SubElement(urlset, "url")
    SubElement(home, "loc").text = f"{SITE_BASE}/"
    SubElement(home, "lastmod").text = TODAY
    SubElement(home, "changefreq").text = "daily"
    SubElement(home, "priority").text = "1.0"

    # 实体列表页
    entity_list = SubElement(urlset, "url")
    SubElement(entity_list, "loc").text = f"{GITHUB_BLOB_BASE}/KNOWLEDGE-GRAPH/ENTITY-LIST.md"
    SubElement(entity_list, "lastmod").text = TODAY
    SubElement(entity_list, "changefreq").text = "weekly"
    SubElement(entity_list, "priority").text = "0.9"

    for u in urls:
        url_elem = SubElement(urlset, "url")
        SubElement(url_elem, "loc").text = u["loc"]
        SubElement(url_elem, "lastmod").text = u["lastmod"]
        SubElement(url_elem, "changefreq").text = u["changefreq"]
        SubElement(url_elem, "priority").text = u["priority"]

    rough_string = tostring(urlset, encoding="unicode")
    reparsed = minidom.parseString(rough_string)
    pretty = reparsed.toprettyxml(indent="  ")
    # 移除空行
    lines = [line for line in pretty.splitlines() if line.strip()]
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + "\n".join(lines[1:]) + "\n"


def main():
    md_urls = collect_md_files()
    node_urls = collect_kg_nodes()
    all_urls = md_urls + node_urls

    if len(all_urls) < 200:
        print(f"⚠️ 警告：当前仅收集到 {len(all_urls)} 个 URL，低于 200 的目标。", file=sys.stderr)
        # 如果不足，放宽条件收集更多根级 md
        extra_dirs = [d for d in os.listdir(PROJECT_ROOT)
                      if os.path.isdir(os.path.join(PROJECT_ROOT, d))
                      and d not in EXCLUDE_PATTERNS
                      and d not in CORE_DIRS]
        for extra_dir in extra_dirs:
            abs_dir = os.path.join(PROJECT_ROOT, extra_dir)
            for root, dirs, files in os.walk(abs_dir):
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in EXCLUDE_PATTERNS]
                for f in files:
                    if not f.endswith(".md"):
                        continue
                    abs_path = os.path.join(root, f)
                    rel_path = os.path.relpath(abs_path, PROJECT_ROOT).replace("\\", "/")
                    if is_excluded(rel_path):
                        continue
                    all_urls.append({
                        "loc": f"{GITHUB_BLOB_BASE}/{rel_path}",
                        "lastmod": TODAY,
                        "changefreq": "monthly",
                        "priority": "0.5",
                    })
                if len(all_urls) >= 200:
                    break
            if len(all_urls) >= 200:
                break

    xml_content = build_xml(all_urls)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(xml_content)

    print(f"✅ sitemap-full.xml 已生成：{OUTPUT_PATH}")
    print(f"   总计 URL 数：{len(all_urls)}（文档 {len(md_urls)}，知识节点 {len(node_urls)}）")


if __name__ == "__main__":
    main()
