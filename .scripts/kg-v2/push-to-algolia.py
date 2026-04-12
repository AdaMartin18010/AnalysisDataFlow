#!/usr/bin/env python3
"""
知识图谱 v2.0 Algolia 搜索索引推送工具
将本地搜索索引推送到 Algolia 云服务
"""

import json
import os
import sys
from pathlib import Path

# 尝试导入 algoliasearch
try:
    from algoliasearch.search_client import SearchClient
except ImportError:
    print("⚠️  algoliasearch 未安装，尝试安装...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "algoliasearch>=2.0", "-q"])
    from algoliasearch.search_client import SearchClient

# 配置
PROJECT_ROOT = Path(__file__).parent.parent.parent
SEARCH_INDEX_FILE = PROJECT_ROOT / "knowledge-graph-site" / "data" / "search-index.json"

# 从环境变量读取配置
APP_ID = os.environ.get("ALGOLIA_APP_ID", "")
ADMIN_KEY = os.environ.get("ALGOLIA_ADMIN_KEY", "")
INDEX_NAME = os.environ.get("ALGOLIA_INDEX_NAME", "analysisdataflow_kg")

def load_search_index():
    """加载本地搜索索引"""
    if not SEARCH_INDEX_FILE.exists():
        print(f"❌ 搜索索引文件不存在: {SEARCH_INDEX_FILE}")
        print("请先运行: python .scripts/kg-v2/generate-search-index.py")
        sys.exit(1)
    
    with open(SEARCH_INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def push_to_algolia(documents):
    """推送文档到 Algolia"""
    if not APP_ID or not ADMIN_KEY:
        print("⚠️  未配置 Algolia 凭证，跳过推送")
        print("请设置环境变量: ALGOLIA_APP_ID, ALGOLIA_ADMIN_KEY")
        return False
    
    try:
        # 初始化客户端
        client = SearchClient.create(APP_ID, ADMIN_KEY)
        index = client.init_index(INDEX_NAME)
        
        # 添加对象ID（必需）
        for i, doc in enumerate(documents):
            doc["objectID"] = doc.get("id", f"doc_{i}")
        
        # 批量上传（每次 1000 条）
        batch_size = 1000
        total = len(documents)
        
        for i in range(0, total, batch_size):
            batch = documents[i:i + batch_size]
            index.save_objects(batch)
            print(f"   📤 已上传批次 {i//batch_size + 1}/{(total-1)//batch_size + 1} ({len(batch)} 条)")
        
        print(f"✅ 共上传 {total} 条记录到 Algolia 索引 '{INDEX_NAME}'")
        
        # 配置索引设置
        index.set_settings({
            "searchableAttributes": [
                "name",
                "description", 
                "content",
                "category",
                "tags"
            ],
            "attributesForFaceting": [
                "category",
                "type",
                "searchable(tags)"
            ],
            "ranking": [
                "typo",
                "words",
                "filters",
                "proximity",
                "attribute",
                "exact",
                "custom"
            ],
            "highlightPreTag": "<mark>",
            "highlightPostTag": "</mark>",
            "snippetEllipsisText": "…",
            "attributesToSnippet": ["description:50", "content:30"],
            "hitsPerPage": 20
        })
        
        print("✅ 索引设置已更新")
        return True
        
    except Exception as e:
        print(f"❌ 推送失败: {e}")
        return False

def main():
    """主函数"""
    print("🔍 Algolia 搜索索引推送工具")
    print("=" * 50)
    
    # 加载数据
    print("\n📂 加载搜索索引...")
    documents = load_search_index()
    print(f"   找到 {len(documents)} 条记录")
    
    # 推送到 Algolia
    print("\n☁️  推送到 Algolia...")
    success = push_to_algolia(documents)
    
    if success:
        print("\n🎉 推送完成！")
        print(f"\n💡 搜索端点: https://{APP_ID}.algolia.net")
        print(f"💡 索引名称: {INDEX_NAME}")
    else:
        print("\n⚠️  推送被跳过或失败")
        print("   本地搜索功能仍可正常使用")

if __name__ == "__main__":
    main()
