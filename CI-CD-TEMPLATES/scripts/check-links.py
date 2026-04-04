#!/usr/bin/env python3
"""
================================================================================
AnalysisDataFlow 自动链接检查脚本
================================================================================
描述: 检查Markdown文档中的内部和外部链接有效性
功能:
  - 验证内部链接（文档间引用）
  - 验证外部链接（HTTP/HTTPS URL）
  - 并发检查提高效率
  - 生成详细报告

使用方法:
  python check-links.py [选项]

选项:
  --check-external    检查外部链接（默认只检查内部链接）
  --timeout N         外部链接超时时间（秒，默认30）
  --format FORMAT     输出格式: text|json|html（默认text）
  --output FILE       输出文件路径
  --verbose           显示详细信息

示例:
  # 仅检查内部链接
  python check-links.py

  # 检查所有链接（包括外部）
  python check-links.py --check-external --timeout 30

  # 生成JSON格式报告
  python check-links.py --format json --output link-report.json
================================================================================
"""

import argparse
import re
import sys
import json
import html
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
from datetime import datetime
from typing import List, Dict, Tuple, Optional

# 尝试导入requests，如果没有则提供错误提示
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("警告: requests库未安装，外部链接检查不可用")
    print("安装命令: pip install requests")


class LinkChecker:
    """链接检查器类"""
    
    def __init__(self, timeout: int = 30, verbose: bool = False):
        self.timeout = timeout
        self.verbose = verbose
        self.broken_internal: List[Dict] = []
        self.broken_external: List[Dict] = []
        self.stats = {
            'total': 0,
            'internal': 0,
            'external': 0,
            'anchor': 0,
            'email': 0,
            'broken_internal': 0,
            'broken_external': 0
        }
        
        # 外部链接排除模式
        self.exclude_patterns = [
            r'localhost',
            r'127\.0\.0\.1',
            r'example\.com',
            r'your-domain\.com',
            r'github\.com/[^/]+/[^/]+/edit/',  # 需要登录的页面
        ]
    
    def log(self, message: str):
        """打印日志（仅在verbose模式）"""
        if self.verbose:
            print(message)
    
    def find_markdown_files(self, root: Path = Path('.')) -> List[Path]:
        """查找所有Markdown文件"""
        md_files = list(root.rglob('*.md'))
        # 排除隐藏目录和依赖目录
        md_files = [
            f for f in md_files 
            if not any(
                part.startswith('.') or part in ['node_modules', '__pycache__', 'venv', '.venv']
                for part in f.parts
            )
        ]
        return md_files
    
    def extract_links(self, content: str) -> List[Tuple[str, str]]:
        """从Markdown内容中提取所有链接"""
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        return re.findall(pattern, content)
    
    def classify_link(self, url: str) -> str:
        """分类链接类型"""
        if url.startswith(('http://', 'https://')):
            return 'external'
        if url.startswith('#'):
            return 'anchor'
        if url.startswith('mailto:'):
            return 'email'
        return 'internal'
    
    def should_skip_external(self, url: str) -> bool:
        """检查是否应该跳过此外部链接"""
        for pattern in self.exclude_patterns:
            if re.search(pattern, url):
                return True
        return False
    
    def validate_internal_link(
        self, 
        url: str, 
        source_file: Path, 
        all_files: List[Path]
    ) -> Tuple[bool, Optional[str]]:
        """验证内部链接是否有效"""
        source_dir = source_file.parent
        
        # 移除锚点
        url_without_anchor = url.split('#')[0]
        
        if not url_without_anchor:
            # 纯锚点链接，认为是有效的
            return True, None
        
        # 解析路径
        if url_without_anchor.startswith('/'):
            # 绝对路径（相对于仓库根目录）
            target = Path('.') / url_without_anchor.lstrip('/')
        else:
            # 相对路径
            target = source_dir / url_without_anchor
        
        target = target.resolve()
        
        # 检查文件是否存在
        if not target.exists():
            # 尝试添加.md后缀
            target_with_md = Path(str(target) + '.md')
            if target_with_md.exists():
                return True, None
            
            # 尝试作为目录/index.md
            target_index = target / 'index.md'
            if target_index.exists():
                return True, None
            
            return False, f"文件不存在: {target.relative_to(Path('.').resolve())}"
        
        return True, None
    
    def check_external_url(self, url: str) -> Tuple[bool, Optional[str]]:
        """检查外部URL是否可访问"""
        if not REQUESTS_AVAILABLE:
            return False, "requests库不可用"
        
        if self.should_skip_external(url):
            return True, None
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; AnalysisDataFlow-LinkChecker/1.0)'
            }
            
            # 首先尝试HEAD请求
            response = requests.head(
                url, 
                timeout=self.timeout, 
                headers=headers,
                allow_redirects=True
            )
            
            # 某些网站不支持HEAD请求，尝试GET
            if response.status_code in [405, 501]:
                response = requests.get(
                    url, 
                    timeout=self.timeout, 
                    headers=headers,
                    stream=True,
                    allow_redirects=True
                )
                response.close()
            
            # 检查状态码
            if response.status_code >= 400:
                return False, f"HTTP {response.status_code}"
            
            return True, None
            
        except requests.exceptions.Timeout:
            return False, "请求超时"
        except requests.exceptions.ConnectionError:
            return False, "连接错误"
        except requests.exceptions.TooManyRedirects:
            return False, "重定向过多"
        except Exception as e:
            return False, f"请求错误: {str(e)[:50]}"
    
    def check_links(
        self, 
        check_external: bool = False,
        progress_callback=None
    ) -> Dict:
        """执行链接检查"""
        print("=" * 70)
        print("AnalysisDataFlow 链接检查")
        print("=" * 70)
        
        # 查找所有Markdown文件
        md_files = self.find_markdown_files()
        print(f"\n发现 {len(md_files)} 个Markdown文件")
        
        # 第一步：收集所有链接
        all_links = []
        external_urls = set()
        
        for file_path in md_files:
            try:
                content = file_path.read_text(encoding='utf-8')
            except Exception as e:
                print(f"⚠️  无法读取 {file_path}: {e}")
                continue
            
            links = self.extract_links(content)
            
            for text, url in links:
                link_type = self.classify_link(url)
                all_links.append({
                    'source': file_path,
                    'text': text,
                    'url': url,
                    'type': link_type
                })
                
                self.stats['total'] += 1
                self.stats[link_type] += 1
                
                if link_type == 'external':
                    external_urls.add(url)
        
        print(f"\n📊 链接统计:")
        print(f"  总链接数: {self.stats['total']}")
        print(f"  内部链接: {self.stats['internal']}")
        print(f"  外部链接: {self.stats['external']}")
        print(f"  锚点链接: {self.stats['anchor']}")
        print(f"  邮件链接: {self.stats['email']}")
        
        # 第二步：验证内部链接
        print("\n🔍 检查内部链接...")
        internal_links = [l for l in all_links if l['type'] == 'internal']
        
        for i, link in enumerate(internal_links):
            is_valid, error = self.validate_internal_link(
                link['url'], link['source'], md_files
            )
            
            if not is_valid:
                self.broken_internal.append({
                    'source': str(link['source']),
                    'text': link['text'],
                    'url': link['url'],
                    'error': error
                })
                self.stats['broken_internal'] += 1
            
            if progress_callback:
                progress_callback(i + 1, len(internal_links), 'internal')
            elif self.verbose:
                if (i + 1) % 100 == 0:
                    print(f"  已检查 {i + 1}/{len(internal_links)} 个内部链接...")
        
        # 第三步：验证外部链接（可选）
        if check_external and REQUESTS_AVAILABLE:
            print(f"\n🌐 检查外部链接（{len(external_urls)} 个唯一URL）...")
            
            # 并发检查
            url_status = {}
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_url = {
                    executor.submit(self.check_external_url, url): url 
                    for url in external_urls
                }
                
                for i, future in enumerate(as_completed(future_to_url)):
                    url = future_to_url[future]
                    try:
                        is_valid, error = future.result()
                        url_status[url] = (is_valid, error)
                        
                        if not is_valid:
                            self.stats['broken_external'] += 1
                        
                        if progress_callback:
                            progress_callback(i + 1, len(external_urls), 'external')
                        elif self.verbose:
                            if (i + 1) % 10 == 0:
                                print(f"  已检查 {i + 1}/{len(external_urls)} 个外部URL...")
                            
                    except Exception as e:
                        url_status[url] = (False, str(e))
                        self.stats['broken_external'] += 1
            
            # 记录损坏的外部链接
            for link in all_links:
                if link['type'] == 'external':
                    is_valid, error = url_status.get(link['url'], (False, '未知错误'))
                    if not is_valid:
                        self.broken_external.append({
                            'source': str(link['source']),
                            'text': link['text'],
                            'url': link['url'],
                            'error': error
                        })
        
        return self.get_result()
    
    def get_result(self) -> Dict:
        """获取检查结果"""
        return {
            'stats': self.stats,
            'broken_internal': self.broken_internal,
            'broken_external': self.broken_external,
            'success': len(self.broken_internal) == 0 and len(self.broken_external) == 0
        }
    
    def print_report(self):
        """打印文本格式报告"""
        print("\n" + "=" * 70)
        print("检查结果报告")
        print("=" * 70)
        
        if self.broken_internal:
            print(f"\n❌ 发现 {len(self.broken_internal)} 个无效内部链接:")
            print("-" * 70)
            
            # 按源文件分组
            by_source = defaultdict(list)
            for link in self.broken_internal:
                by_source[link['source']].append(link)
            
            for source, links in sorted(by_source.items()):
                print(f"\n  📄 {source}")
                for link in links:
                    print(f"    - [{link['text']}]({link['url']})")
                    print(f"      错误: {link['error']}")
        
        if self.broken_external:
            print(f"\n❌ 发现 {len(self.broken_external)} 个无效外部链接:")
            print("-" * 70)
            
            # 按源文件分组
            by_source = defaultdict(list)
            for link in self.broken_external:
                by_source[link['source']].append(link)
            
            for source, links in sorted(by_source.items())[:10]:  # 只显示前10个文件
                print(f"\n  📄 {source}")
                for link in links[:5]:  # 每个文件最多显示5个
                    print(f"    - [{link['text']}]({link['url']})")
                    print(f"      错误: {link['error']}")
                if len(links) > 5:
                    print(f"    ...还有 {len(links) - 5} 个")
            
            if len(by_source) > 10:
                print(f"\n  ...还有 {len(by_source) - 10} 个文件")
        
        if not self.broken_internal and not self.broken_external:
            print("\n✅ 所有链接有效！")
        
        print("\n" + "=" * 70)
        print(f"总计: {self.stats['total']} 个链接")
        print(f"  - 无效内部链接: {len(self.broken_internal)}")
        print(f"  - 无效外部链接: {len(self.broken_external)}")
        print("=" * 70)
    
    def generate_json_report(self) -> str:
        """生成JSON格式报告"""
        result = self.get_result()
        result['timestamp'] = datetime.now().isoformat()
        return json.dumps(result, indent=2, ensure_ascii=False)
    
    def generate_html_report(self) -> str:
        """生成HTML格式报告"""
        result = self.get_result()
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>链接检查报告 - AnalysisDataFlow</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #2563eb, #1e40af);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-card h3 {{
            margin: 0 0 10px 0;
            font-size: 14px;
            color: #666;
        }}
        .stat-card .number {{
            font-size: 32px;
            font-weight: bold;
            color: #2563eb;
        }}
        .section {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .error-item {{
            padding: 10px;
            margin: 10px 0;
            background: #fee;
            border-left: 4px solid #e11;
            border-radius: 4px;
        }}
        .success {{
            background: #efe;
            border-left-color: #2c2;
        }}
        pre {{
            background: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔗 链接检查报告</h1>
        <p>AnalysisDataFlow 项目文档链接有效性检查</p>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <h3>总链接数</h3>
            <div class="number">{self.stats['total']}</div>
        </div>
        <div class="stat-card">
            <h3>内部链接</h3>
            <div class="number">{self.stats['internal']}</div>
        </div>
        <div class="stat-card">
            <h3>外部链接</h3>
            <div class="number">{self.stats['external']}</div>
        </div>
        <div class="stat-card">
            <h3>无效链接</h3>
            <div class="number" style="color: {'#e11' if self.broken_internal or self.broken_external else '#2c2'}">
                {len(self.broken_internal) + len(self.broken_external)}
            </div>
        </div>
    </div>
"""
        
        if self.broken_internal:
            html_content += """
    <div class="section">
        <h2>❌ 无效内部链接</h2>
"""
            by_source = defaultdict(list)
            for link in self.broken_internal:
                by_source[link['source']].append(link)
            
            for source, links in sorted(by_source.items()):
                html_content += f"""
        <h3>{html.escape(source)}</h3>
"""
                for link in links:
                    html_content += f"""
        <div class="error-item">
            <code>[{html.escape(link['text'])}]({html.escape(link['url'])})</code>
            <br><small>错误: {html.escape(link['error'])}</small>
        </div>
"""
            html_content += "    </div>"
        
        if self.broken_external:
            html_content += """
    <div class="section">
        <h2>❌ 无效外部链接</h2>
"""
            by_source = defaultdict(list)
            for link in self.broken_external:
                by_source[link['source']].append(link)
            
            for source, links in sorted(by_source.items()):
                html_content += f"""
        <h3>{html.escape(source)}</h3>
"""
                for link in links:
                    html_content += f"""
        <div class="error-item">
            <code>[{html.escape(link['text'])}]({html.escape(link['url'])})</code>
            <br><small>错误: {html.escape(link['error'])}</small>
        </div>
"""
            html_content += "    </div>"
        
        if not self.broken_internal and not self.broken_external:
            html_content += """
    <div class="section success">
        <h2>✅ 所有链接有效</h2>
        <p>未发现无效链接！</p>
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        return html_content


def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 链接检查工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python check-links.py
  python check-links.py --check-external --timeout 30
  python check-links.py --format json --output report.json
        """
    )
    
    parser.add_argument(
        '--check-external',
        action='store_true',
        help='检查外部链接（需要requests库）'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='外部链接检查超时时间（秒，默认30）'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'html'],
        default='text',
        help='输出格式（默认text）'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='输出文件路径'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细信息'
    )
    
    args = parser.parse_args()
    
    # 创建检查器
    checker = LinkChecker(timeout=args.timeout, verbose=args.verbose)
    
    # 执行检查
    result = checker.check_links(check_external=args.check_external)
    
    # 生成报告
    if args.format == 'text':
        checker.print_report()
        output = None
    elif args.format == 'json':
        output = checker.generate_json_report()
        print(output)
    elif args.format == 'html':
        output = checker.generate_html_report()
        print(output)
    
    # 保存到文件
    if args.output and output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"\n报告已保存到: {args.output}")
    
    # 返回退出码
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()
