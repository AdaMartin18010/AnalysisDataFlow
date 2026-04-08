#!/usr/bin/env python3
"""
知识图谱 v2.0 资源优化器
压缩和优化静态资源
"""

import json
import gzip
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
SITE_DIR = PROJECT_ROOT / "knowledge-graph-site"
DATA_DIR = SITE_DIR / "data"

def optimize_json_files():
    """优化JSON文件 - 压缩和生成gzip版本"""
    print("📦 优化JSON文件...")
    
    json_files = list(DATA_DIR.glob("*.json"))
    json_files.extend(DATA_DIR.glob("chunks/*.json"))
    
    total_original = 0
    total_compressed = 0
    
    for json_file in json_files:
        if json_file.suffix == '.gz':
            continue
            
        # 读取原始内容
        with open(json_file, 'rb') as f:
            content = f.read()
        
        original_size = len(content)
        total_original += original_size
        
        # 生成gzip压缩版本
        gzip_file = str(json_file) + '.gz'
        with gzip.open(gzip_file, 'wb', compresslevel=9) as f:
            f.write(content)
        
        compressed_size = os.path.getsize(gzip_file)
        total_compressed += compressed_size
        
        ratio = (1 - compressed_size / original_size) * 100
        print(f"   ✅ {json_file.name}: {original_size/1024:.1f}KB → {compressed_size/1024:.1f}KB (节省 {ratio:.1f}%)")
    
    if total_original > 0:
        total_ratio = (1 - total_compressed / total_original) * 100
        print(f"\n   📊 总计: {total_original/1024:.1f}KB → {total_compressed/1024:.1f}KB (节省 {total_ratio:.1f}%)")

def generate_service_worker():
    """生成Service Worker用于缓存"""
    print("\n🔧 生成Service Worker...")
    
    sw_code = '''// 知识图谱 v2.0 Service Worker
const CACHE_NAME = 'kg-v2-cache-v1';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/data/metadata.json',
    '/data/graph-data.json',
    '/data/search-index.json',
    '/data/search-suggestions.json',
    '/data/learning-paths.json',
    '/data/skill-tree.json'
];

// 安装时缓存静态资源
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[SW] 缓存静态资源');
                return cache.addAll(STATIC_ASSETS);
            })
            .catch((err) => {
                console.error('[SW] 缓存失败:', err);
            })
    );
    self.skipWaiting();
});

// 激活时清理旧缓存
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((name) => name !== CACHE_NAME)
                    .map((name) => {
                        console.log('[SW] 删除旧缓存:', name);
                        return caches.delete(name);
                    })
            );
        })
    );
    self.clients.claim();
});

// 拦截请求并提供缓存
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // 跳过非GET请求
    if (request.method !== 'GET') {
        return;
    }
    
    // 跳过非同源请求
    if (url.origin !== self.location.origin) {
        return;
    }
    
    // 缓存策略：Stale-While-Revalidate
    event.respondWith(
        caches.match(request).then((cached) => {
            const fetchPromise = fetch(request)
                .then((networkResponse) => {
                    if (networkResponse.ok) {
                        const clone = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(request, clone);
                        });
                    }
                    return networkResponse;
                })
                .catch((err) => {
                    console.log('[SW] 网络请求失败，使用缓存:', err);
                    return cached;
                });
            
            return cached || fetchPromise;
        })
    );
});

// 后台同步
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-search-index') {
        event.waitUntil(
            fetch('/data/search-index.json')
                .then((response) => response.json())
                .then((data) => {
                    console.log('[SW] 搜索索引已同步');
                    return caches.open(CACHE_NAME).then((cache) => {
                        return cache.put('/data/search-index.json', 
                            new Response(JSON.stringify(data)));
                    });
                })
        );
    }
});
'''
    
    sw_file = SITE_DIR / "service-worker.js"
    with open(sw_file, 'w', encoding='utf-8') as f:
        f.write(sw_code)
    
    print(f"   ✅ Service Worker已生成: {sw_file}")

def generate_manifest():
    """生成Web App Manifest"""
    print("\n📱 生成Web App Manifest...")
    
    manifest = {
        "name": "AnalysisDataFlow 知识图谱",
        "short_name": "知识图谱",
        "description": "流计算理论与Flink实践的交互式知识图谱",
        "version": "2.0.0",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0d1117",
        "theme_color": "#58a6ff",
        "orientation": "any",
        "icons": [
            {
                "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='45' fill='%2358a6ff'/%3E%3Ctext x='50' y='65' font-size='45' text-anchor='middle' fill='white'%3EKG%3C/text%3E%3C/svg%3E",
                "sizes": "any",
                "type": "image/svg+xml"
            }
        ],
        "categories": ["education", "developer tools", "productivity"],
        "lang": "zh-CN",
        "dir": "ltr",
        "scope": "/",
        "screenshots": [
            {
                "src": "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1280 720'%3E%3Crect width='1280' height='720' fill='%230d1117'/%3E%3Ctext x='640' y='360' font-size='60' text-anchor='middle' fill='%2358a6ff'%3E知识图谱 v2.0%3C/text%3E%3C/svg%3E",
                "sizes": "1280x720",
                "type": "image/svg+xml",
                "form_factor": "wide"
            }
        ]
    }
    
    manifest_file = SITE_DIR / "manifest.json"
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"   ✅ Manifest已生成: {manifest_file}")

def copy_and_optimize_html():
    """复制并优化HTML文件"""
    print("\n🌐 优化HTML文件...")
    
    source_file = PROJECT_ROOT / "knowledge-graph-v4.html"
    target_file = SITE_DIR / "index.html"
    
    if not source_file.exists():
        print(f"   ⚠️ 源文件不存在: {source_file}")
        return
    
    content = source_file.read_text(encoding='utf-8')
    
    # 添加Service Worker注册
    sw_script = '''
<script>
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js')
            .then((registration) => {
                console.log('[App] SW注册成功:', registration.scope);
            })
            .catch((err) => {
                console.log('[App] SW注册失败:', err);
            });
    });
}
</script>
'''
    
    # 在</body>前插入Service Worker注册
    if '</body>' in content:
        content = content.replace('</body>', sw_script + '</body>')
    
    # 添加manifest链接
    if '<head>' in content and 'manifest.json' not in content:
        content = content.replace('<head>', '<head>\n    <link rel="manifest" href="/manifest.json">')
    
    # 写入优化后的文件
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ HTML已优化: {target_file}")

def generate_404_page():
    """生成404页面"""
    print("\n❌ 生成404页面...")
    
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - 页面未找到</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
        }
        .error-code { font-size: 120px; font-weight: bold; color: #58a6ff; }
        .error-message { font-size: 24px; margin: 20px 0; }
        .error-description { color: #8b949e; margin-bottom: 30px; }
        .home-link {
            display: inline-block;
            padding: 12px 30px;
            background: #58a6ff;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-size: 16px;
            transition: background 0.2s;
        }
        .home-link:hover { background: #79b8ff; }
    </style>
</head>
<body>
    <div class="error-code">404</div>
    <div class="error-message">页面未找到</div>
    <div class="error-description">
        您访问的页面不存在或已被移动。<br>
        请返回知识图谱首页继续浏览。
    </div>
    <a href="/" class="home-link">返回首页</a>
</body>
</html>
'''
    
    page_file = SITE_DIR / "404.html"
    with open(page_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"   ✅ 404页面已生成: {page_file}")

def main():
    """主函数"""
    print("⚡ 开始优化静态资源...")
    
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 复制并优化HTML
    copy_and_optimize_html()
    
    # 优化JSON文件
    optimize_json_files()
    
    # 生成Service Worker
    generate_service_worker()
    
    # 生成Manifest
    generate_manifest()
    
    # 生成404页面
    generate_404_page()
    
    print("\n🎉 资源优化完成!")

if __name__ == "__main__":
    main()
