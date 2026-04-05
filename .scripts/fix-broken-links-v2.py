#!/usr/bin/env python3
"""
AnalysisDataFlow 失效链接自动修复脚本 v2.0
=========================================
功能：分类处理失效链接，自动修复可修复的链接，标记无法修复的链接

类型A: 永久失效（404）-> 查找替代链接或标记[已失效]
类型B: 重定向（301/302）-> 更新为最终URL
类型C: 临时失效（5xx/timeout）-> 标记待复查

作者: AnalysisDataFlow CI/CD Team
版本: 2.0.0
日期: 2026-04-05
"""

import re
import json
import argparse
import asyncio
import aiohttp
from pathlib import Path
from urllib.parse import urlparse, quote, unquote
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from collections import defaultdict


# =============================================================================
# 配置常量
# =============================================================================

# 已知可自动修复的URL映射
KNOWN_REPLACEMENTS = {
    # 域名迁移
    'https://ci.apache.org/projects/flink/': 'https://nightlies.apache.org/flink/',
    'http://ci.apache.org/projects/flink/': 'https://nightlies.apache.org/flink/',
    
    # 论文链接更新
    'https://sites.cs.ucsb.edu/~rich/class/cs293b-cloud/papers/brewer_cap.pdf': 
        'https://web.archive.org/web/20230000000000*/https://sites.cs.ucsb.edu/~rich/class/cs293b-cloud/papers/brewer_cap.pdf',
    'https://users.cs.duke.edu/~badi/papers/cap.pdf': 
        'https://web.archive.org/web/20230000000000*/https://users.cs.duke.edu/~badi/papers/cap.pdf',
    'https://www.usenix.org/legacy/publications/library/proceedings/osdi06/tech/full_papers/chang/chang.pdf':
        'https://web.archive.org/web/20230000000000*/https://www.usenix.org/legacy/publications/library/proceedings/osdi06/tech/full_papers/chang/chang.pdf',
    'https://lamport.azurewebsites.net/pubs/tla+book.pdf':
        'https://lamport.azurewebsites.net/tla/book.html',
    'https://www.cs.ucl.ac.uk/staff/p.ohearn/seplogic/Separation_Logic_Lecture_Notes.pdf':
        'https://web.archive.org/web/20230000000000*/https://www.cs.ucl.ac.uk/staff/p.ohearn/seplogic/Separation_Logic_Lecture_Notes.pdf',
        
    # GitHub项目迁移
    'https://github.com/rust-lang-nursery/wg-async': 'https://github.com/rust-lang/wg-async',
    'https://github.com/irontools/iron-functions/releases': 'https://github.com/iron-io/functions/releases',
}

# 需要标记为[已失效]的域名
DEAD_DOMAINS = [
    'blog.twitter.com',
    'twitter.com/engineering',
]

# Wayback Machine API
WAYBACK_API = 'https://archive.org/wayback/available'

# HTTP状态码分类
STATUS_BROKEN = [404, 410, 400]  # 永久失效
STATUS_REDIRECT = [301, 302, 307, 308]  # 重定向
STATUS_RETRY = [500, 502, 503, 504, 429]  # 临时失效，需要重试


# =============================================================================
# 链接检查与修复
# =============================================================================

class LinkFixerV2:
    """链接修复器 v2"""
    
    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.fixes_applied = []
        self.fixes_skipped = []
        self.fixes_marked = []
        self.wayback_cache = {}
        
    def log(self, msg: str):
        """打印日志"""
        if self.verbose:
            print(msg)
    
    def classify_link_status(self, status_code: int, error: str = None) -> str:
        """分类链接状态"""
        if status_code in STATUS_BROKEN:
            return 'broken'
        elif status_code in STATUS_REDIRECT:
            return 'redirect'
        elif status_code in STATUS_RETRY or error == 'timeout':
            return 'retry'
        elif status_code == 200:
            return 'ok'
        else:
            return 'unknown'
    
    def get_replacement_url(self, url: str) -> Tuple[Optional[str], str]:
        """获取替换URL"""
        # 检查精确匹配
        if url in KNOWN_REPLACEMENTS:
            return KNOWN_REPLACEMENTS[url], 'known_replacement'
        
        # 检查前缀匹配
        for old_prefix, new_prefix in KNOWN_REPLACEMENTS.items():
            if url.startswith(old_prefix):
                new_url = url.replace(old_prefix, new_prefix)
                return new_url, 'prefix_replacement'
        
        # 检查是否为死域名
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if any(dead in domain for dead in DEAD_DOMAINS):
            return None, 'dead_domain'
        
        return None, 'no_replacement'
    
    async def find_wayback_url(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """查找 Wayback Machine 存档链接"""
        if url in self.wayback_cache:
            return self.wayback_cache[url]
        
        try:
            api_url = f'{WAYBACK_API}?url={quote(url, safe="")}'
            async with session.get(api_url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'archived_snapshots' in data and 'closest' in data['archived_snapshots']:
                        snapshot = data['archived_snapshots']['closest']
                        if snapshot.get('available'):
                            archive_url = snapshot.get('url')
                            self.wayback_cache[url] = archive_url
                            return archive_url
        except Exception as e:
            self.log(f"   Wayback查询失败: {e}")
        
        self.wayback_cache[url] = None
        return None
    
    def fix_link_in_file(self, file_path: Path, old_url: str, new_url: str) -> bool:
        """修复文件中的链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 使用正则表达式替换链接，保留链接文本
            # 匹配 [text](url) 或 [text](url "title")
            escaped_url = re.escape(old_url)
            pattern = rf'\[([^\]]+)\]\({escaped_url}(\s+"[^"]*")?\)'
            
            def replace_link(match):
                text = match.group(1)
                title = match.group(2) or ''
                return f'[{text}]({new_url}{title})'
            
            new_content = re.sub(pattern, replace_link, content)
            
            if new_content == original_content:
                # 尝试简单替换
                new_content = original_content.replace(old_url, new_url)
            
            if new_content != original_content:
                if not self.dry_run:
                    # 备份原文件
                    backup_path = file_path.with_suffix('.md.bak')
                    if not backup_path.exists():
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(original_content)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"   ❌ 修复失败 {file_path}: {e}")
            return False
    
    def mark_link_as_broken(self, file_path: Path, url: str, text: str) -> bool:
        """标记链接为[已失效]"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 查找并修改链接文本
            escaped_url = re.escape(url)
            pattern = rf'\[([^\]]+)\]\({escaped_url}(\s+"[^"]*")?\)'
            
            def mark_broken(match):
                original_text = match.group(1)
                if '[已失效]' not in original_text:
                    return f'[{original_text} [已失效]]({url})'
                return match.group(0)
            
            new_content = re.sub(pattern, mark_broken, content)
            
            if new_content != original_content:
                if not self.dry_run:
                    backup_path = file_path.with_suffix('.md.bak')
                    if not backup_path.exists():
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(original_content)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"   ❌ 标记失败 {file_path}: {e}")
            return False


# =============================================================================
# 批处理功能
# =============================================================================

async def process_broken_links(
    report_path: Path,
    fixer: LinkFixerV2,
    use_wayback: bool = True
) -> Dict:
    """处理失效链接"""
    
    # 读取JSON报告
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    broken_links = report.get('broken_links', [])
    external_broken = [l for l in broken_links if l.get('type') == 'external']
    
    print(f"\n📊 分析 {len(external_broken)} 个外部失效链接...")
    
    stats = {
        'fixed': 0,
        'marked': 0,
        'wayback_found': 0,
        'skipped': 0,
        'by_category': defaultdict(int)
    }
    
    async with aiohttp.ClientSession() as session:
        for link in external_broken:
            file_path = Path(link['file'])
            url = link['url']
            text = link.get('text', '')
            error = link.get('error', '')
            
            if not file_path.exists():
                continue
            
            # 尝试已知替换
            replacement, reason = fixer.get_replacement_url(url)
            
            if replacement:
                print(f"\n🔧 [{reason}] {file_path}")
                print(f"   原文: {url[:80]}...")
                print(f"   替换: {replacement[:80]}...")
                
                if fixer.fix_link_in_file(file_path, url, replacement):
                    fixer.fixes_applied.append({
                        'file': str(file_path),
                        'old_url': url,
                        'new_url': replacement,
                        'reason': reason
                    })
                    stats['fixed'] += 1
                    stats['by_category'][reason] += 1
                continue
            
            if reason == 'dead_domain':
                print(f"\n🏴 [dead_domain] {file_path}")
                print(f"   链接: {url[:80]}...")
                
                if fixer.mark_link_as_broken(file_path, url, text):
                    fixer.fixes_marked.append({
                        'file': str(file_path),
                        'url': url,
                        'reason': 'dead_domain'
                    })
                    stats['marked'] += 1
                    stats['by_category']['dead_domain'] += 1
                continue
            
            # 尝试Wayback Machine
            if use_wayback and error in ['HTTP 404', 'timeout']:
                print(f"\n🔍 [wayback] 查询存档: {url[:60]}...")
                wayback_url = await fixer.find_wayback_url(session, url)
                
                if wayback_url:
                    print(f"   找到存档: {wayback_url[:80]}...")
                    
                    if fixer.fix_link_in_file(file_path, url, wayback_url):
                        fixer.fixes_applied.append({
                            'file': str(file_path),
                            'old_url': url,
                            'new_url': wayback_url,
                            'reason': 'wayback_archive'
                        })
                        stats['wayback_found'] += 1
                        stats['by_category']['wayback_archive'] += 1
                    continue
            
            # 无法自动修复
            fixer.fixes_skipped.append({
                'file': str(file_path),
                'url': url,
                'error': error,
                'suggested_action': 'manual_fix'
            })
            stats['skipped'] += 1
    
    return stats


def fix_code_pattern_links(fixer: LinkFixerV2, root_path: Path) -> int:
    """
    修复代码模式链接 - 将代码中的泛型参数误识别为链接的情况
    例如: `[Transaction](Duration.ofSeconds(30))` -> `[Transaction](Duration.ofSeconds(30))` (代码)
    """
    print("\n🔍 扫描代码模式链接...")
    
    fixed_count = 0
    md_files = list(root_path.rglob('*.md'))
    
    # 代码模式正则：匹配常见的代码语法
    # 注意：这些模式会将看起来像链接的代码转换为代码格式
    code_patterns = [
        # Duration.ofSeconds(30) - Java/Kotlin代码
        (r'\[([^\]]+)\]\(Duration\.(ofSeconds|ofMillis|ofMinutes)\((\d+)\)\s*\)', 
         lambda m: f'`{m.group(1)}(Duration.{m.group(2)}({m.group(3)}))`'),
        # 字符串参数如 "first", "late-data"
        (r'\[([^\]]+)\]\("([^"]+)"\s*[,\)]', 
         lambda m: f'`{m.group(1)}("{m.group(2)}")`'),
        # 泛型参数如 [T](stream:), [K, V](name:)
        (r'\[([^\]]*[:<][^\]]*)\]\(([a-zA-Z_]+):\)', 
         lambda m: f'`{m.group(1)}({m.group(2)}:)`'),
        # 下划线访问如 _.eventTime, _.length
        (r'\[([^\]]+)\]\((_\.[a-zA-Z_]+)\)', 
         lambda m: f'`{m.group(1)}({m.group(2)})`'),
        # 纯泛型参数 [T](using)
        (r'\[([A-Z][a-zA-Z0-9_]*)\]\((using|extractFn|stream|fun|value|values|tag|future|name|key|selector|operation|oldDescriptor|updateFunction)\)', 
         lambda m: f'`{m.group(1)}({m.group(2)})`'),
        # 空括号 [T](\n)
        (r'\[([^\]]+)\]\(\s*\n\s*\)', 
         lambda m: f'`{m.group(1)}()`'),
    ]
    
    for md_file in md_files:
        if any(part.startswith('.') for part in md_file.parts):
            continue
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            for pattern, replacement in code_patterns:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            if content != original_content:
                if not fixer.dry_run:
                    backup_path = md_file.with_suffix('.md.bak')
                    if not backup_path.exists():
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(original_content)
                    
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                
                fixed_count += 1
                fixer.log(f"   ✅ {md_file}")
                
        except Exception as e:
            fixer.log(f"   ⚠️  处理失败 {md_file}: {e}")
    
    print(f"   修复了 {fixed_count} 个文件中的代码模式链接")
    return fixed_count


def generate_fix_report(fixer: LinkFixerV2, output_path: Path, stats: Dict):
    """生成修复报告"""
    lines = [
        "# 🔧 链接修复报告 v2.0",
        "",
        f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> **运行模式**: {'试运行' if fixer.dry_run else '实际修复'}",
        "",
        "## 📊 修复统计",
        "",
        f"| 类别 | 数量 |",
        f"|------|------|",
        f"| ✅ 自动修复 | {stats.get('fixed', 0)} |",
        f"| 📦 Wayback存档 | {stats.get('wayback_found', 0)} |",
        f"| 🏴 标记失效 | {stats.get('marked', 0)} |",
        f"| ⏭️ 跳过/需人工 | {stats.get('skipped', 0)} |",
        f"| **总计处理** | **{stats.get('fixed', 0) + stats.get('wayback_found', 0) + stats.get('marked', 0) + stats.get('skipped', 0)}** |",
        "",
    ]
    
    # 按类别统计
    if stats.get('by_category'):
        lines.extend([
            "### 修复类别详情",
            "",
            f"| 类别 | 数量 |",
            f"|------|------|",
        ])
        for category, count in sorted(stats['by_category'].items()):
            lines.append(f"| {category} | {count} |")
        lines.append("")
    
    # 已应用的修复
    if fixer.fixes_applied:
        lines.extend([
            "## ✅ 已应用的修复",
            "",
        ])
        for fix in fixer.fixes_applied[:50]:  # 限制显示数量
            lines.extend([
                f"### {fix['file']}",
                "",
                f"**原因**: {fix['reason']}",
                "",
                f"- 原文: `{fix['old_url'][:100]}{'...' if len(fix['old_url']) > 100 else ''}`",
                f"- 修复: `{fix['new_url'][:100]}{'...' if len(fix['new_url']) > 100 else ''}`",
                "",
            ])
        
        if len(fixer.fixes_applied) > 50:
            lines.append(f"_... 还有 {len(fixer.fixes_applied) - 50} 个修复_")
            lines.append("")
    
    # 标记的失效链接
    if fixer.fixes_marked:
        lines.extend([
            "## 🏴 标记为失效的链接",
            "",
        ])
        for item in fixer.fixes_marked[:30]:
            lines.extend([
                f"- `{item['file']}`",
                f"  - URL: `{item['url'][:80]}...`",
                f"  - 原因: {item['reason']}",
                "",
            ])
    
    # 需要人工修复的链接
    if fixer.fixes_skipped:
        lines.extend([
            "## 📝 需要人工修复的链接",
            "",
            "以下链接无法自动修复，请人工处理：",
            "",
        ])
        
        # 按文件分组
        by_file = defaultdict(list)
        for item in fixer.fixes_skipped:
            by_file[item['file']].append(item)
        
        for file, items in sorted(by_file.items())[:20]:  # 限制文件数量
            lines.extend([
                f"### {file}",
                "",
            ])
            for item in items[:5]:  # 每文件限制数量
                lines.extend([
                    f"- URL: `{item['url'][:80]}...`",
                    f"  - 错误: {item['error']}",
                    "",
                ])
        
        lines.extend([
            "### 人工修复指南",
            "",
            "1. **使用Wayback Machine**: 访问 https://web.archive.org/ 搜索历史存档",
            "2. **查找官方迁移文档**: 检查原站点是否有迁移公告",
            "3. **移除链接**: 如果内容无法访问，考虑移除链接保留文字",
            "",
        ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"\n📝 修复报告已保存: {output_path}")


# =============================================================================
# 主程序
# =============================================================================

async def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 失效链接自动修复脚本 v2.0'
    )
    
    parser.add_argument(
        'report',
        nargs='?',
        default='reports/link-health-results.json',
        help='JSON格式链接健康报告路径'
    )
    
    parser.add_argument(
        '--path', '-p',
        default='.',
        help='项目根目录'
    )
    
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='试运行模式（不实际修改文件）'
    )
    
    parser.add_argument(
        '--fix-code-patterns', '-c',
        action='store_true',
        help='修复代码模式链接'
    )
    
    parser.add_argument(
        '--use-wayback', '-w',
        action='store_true',
        default=True,
        help='使用Wayback Machine查找存档'
    )
    
    parser.add_argument(
        '--output', '-o',
        default='reports/LINK-FIX-REPORT-v2.md',
        help='修复报告输出路径'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='详细输出'
    )
    
    args = parser.parse_args()
    
    # 创建修复器
    fixer = LinkFixerV2(dry_run=args.dry_run, verbose=args.verbose)
    
    print("=" * 70)
    print("AnalysisDataFlow 失效链接自动修复脚本 v2.0")
    print("=" * 70)
    
    if args.dry_run:
        print("🧪 试运行模式 - 不会实际修改文件\n")
    
    all_stats = {}
    
    # 1. 修复代码模式链接
    if args.fix_code_patterns:
        code_fixed = fix_code_pattern_links(fixer, Path(args.path))
        all_stats['code_patterns_fixed'] = code_fixed
    
    # 2. 处理失效链接报告
    report_path = Path(args.report)
    if report_path.exists():
        stats = await process_broken_links(report_path, fixer, use_wayback=args.use_wayback)
        all_stats.update(stats)
    else:
        print(f"⚠️  报告文件不存在: {report_path}")
        print("   请先运行: python .scripts/link_checker.py")
    
    # 3. 生成报告
    print("\n" + "=" * 70)
    print("📊 修复摘要")
    print("=" * 70)
    print(f"   ✅ 自动修复: {all_stats.get('fixed', 0)}")
    print(f"   📦 Wayback存档: {all_stats.get('wayback_found', 0)}")
    print(f"   🏴 标记失效: {all_stats.get('marked', 0)}")
    print(f"   ⏭️ 跳过/需人工: {all_stats.get('skipped', 0)}")
    if 'code_patterns_fixed' in all_stats:
        print(f"   🔧 代码模式修复: {all_stats['code_patterns_fixed']} 文件")
    print("=" * 70)
    
    # 生成修复报告
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generate_fix_report(fixer, output_path, all_stats)
    
    # 返回退出码
    total_fixed = all_stats.get('fixed', 0) + all_stats.get('wayback_found', 0) + all_stats.get('marked', 0)
    if total_fixed > 0 and not args.dry_run:
        print(f"\n✅ 成功修复 {total_fixed} 个链接")
        return 0
    elif args.dry_run:
        print(f"\n🧪 试运行完成，将修复 {total_fixed} 个链接")
        return 0
    else:
        print("\nℹ️ 没有需要修复的链接")
        return 0


if __name__ == '__main__':
    asyncio.run(main())
