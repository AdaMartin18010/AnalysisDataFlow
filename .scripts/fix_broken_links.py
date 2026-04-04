#!/usr/bin/env python3
"""
AnalysisDataFlow 失效链接修复工具
=================================
功能：自动修复已知模式的失效链接，标记需要人工修复的链接

P1-6: 失效链接修复
P1-7: 存档链接更新

作者: AnalysisDataFlow CI/CD Team
版本: 1.0.0
"""

import re
import json
import argparse
from pathlib import Path
from urllib.parse import urlparse, quote
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import time


# =============================================================================
# 已知修复模式
# =============================================================================

# 域名迁移映射
DOMAIN_REDIRECTS = {
    # Apache项目
    'flink.apache.org': {
        'new_domain': 'nightlies.apache.org/flink',
        'pattern': r'https?://flink\.apache\.org/(.*)',
        'replacement': r'https://nightlies.apache.org/flink/flink-docs-stable/\1'
    },
    
    # GitHub Raw内容
    'raw.githubusercontent.com': {
        'note': '通常需要更新到特定分支或tag'
    },
    
    # 文档站点迁移
    'docs.oracle.com/javase': {
        'new_domain': 'docs.oracle.com/en/java/javase',
        'pattern': r'https?://docs\.oracle\.com/javase/(\d+)/(.*)',
        'replacement': r'https://docs.oracle.com/en/java/javase/\1/docs/api/\2'
    },
    
    # Scala文档
    'scala-lang.org/api': {
        'new_domain': 'scala-lang.org/api/current',
        'pattern': r'https?://www\.scala-lang\.org/api/([^/]+)/(.*)',
        'replacement': r'https://www.scala-lang.org/api/current/\2'
    },
    
    # 学术论文（DOI优先）
    'dl.acm.org': {
        'note': '建议使用DOI链接'
    },
    'ieeexplore.ieee.org': {
        'note': '建议使用DOI链接'
    },
}

# 特定URL重定向映射
URL_REDIRECTS = {
    # Flink文档
    'https://ci.apache.org/projects/flink/flink-docs-stable/': 
        'https://nightlies.apache.org/flink/flink-docs-stable/',
    'https://ci.apache.org/projects/flink/flink-docs-master/':
        'https://nightlies.apache.org/flink/flink-docs-master/',
}

# 存档服务模板
ARCHIVE_SERVICES = {
    'wayback': 'https://web.archive.org/web/{timestamp}/{url}',
    'archive_today': 'https://archive.today/{url}',
}


# =============================================================================
# 链接修复器
# =============================================================================

class LinkFixer:
    """链接修复器"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.fixes_applied = []
        self.fixes_needed = []
    
    def fix_domain_redirect(self, url: str) -> Tuple[str, bool, str]:
        """
        尝试修复域名重定向
        返回: (new_url, was_fixed, reason)
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # 移除www前缀
        if domain.startswith('www.'):
            domain = domain[4:]
        
        # 检查域名映射
        if domain in DOMAIN_REDIRECTS:
            config = DOMAIN_REDIRECTS[domain]
            
            if 'pattern' in config and 'replacement' in config:
                pattern = config['pattern']
                replacement = config['replacement']
                new_url = re.sub(pattern, replacement, url, flags=re.IGNORECASE)
                
                if new_url != url:
                    return new_url, True, f"域名迁移: {domain} -> {config.get('new_domain', 'new URL')}"
            
            if 'note' in config:
                return url, False, config['note']
        
        return url, False, "无匹配的修复模式"
    
    def fix_specific_redirect(self, url: str) -> Tuple[str, bool, str]:
        """修复特定URL重定向"""
        if url in URL_REDIRECTS:
            return URL_REDIRECTS[url], True, "特定URL重定向"
        
        # 尝试去掉末尾斜杠匹配
        url_no_slash = url.rstrip('/')
        if url_no_slash in URL_REDIRECTS:
            return URL_REDIRECTS[url_no_slash], True, "特定URL重定向（斜杠差异）"
        
        return url, False, "无特定重定向"
    
    def create_archive_link(self, url: str, service: str = 'wayback') -> str:
        """创建存档链接"""
        timestamp = datetime.now().strftime('%Y%m%d')
        template = ARCHIVE_SERVICES.get(service, ARCHIVE_SERVICES['wayback'])
        return template.format(timestamp=timestamp, url=quote(url, safe=''))
    
    def fix_link(self, url: str) -> Dict:
        """
        尝试修复链接
        返回修复结果字典
        """
        result = {
            'original_url': url,
            'fixed_url': url,
            'was_fixed': False,
            'fix_type': None,
            'reason': None,
            'needs_manual': False
        }
        
        # 尝试特定URL重定向
        new_url, was_fixed, reason = self.fix_specific_redirect(url)
        if was_fixed:
            result['fixed_url'] = new_url
            result['was_fixed'] = True
            result['fix_type'] = 'specific_redirect'
            result['reason'] = reason
            return result
        
        # 尝试域名重定向
        new_url, was_fixed, reason = self.fix_domain_redirect(url)
        if was_fixed:
            result['fixed_url'] = new_url
            result['was_fixed'] = True
            result['fix_type'] = 'domain_redirect'
            result['reason'] = reason
            return result
        
        # 检查是否需要人工修复
        if '需要' in reason or '建议' in reason:
            result['needs_manual'] = True
            result['reason'] = reason
        else:
            result['reason'] = "无自动修复模式可用"
        
        return result
    
    def apply_fix_to_file(
        self, 
        file_path: Path, 
        old_url: str, 
        new_url: str,
        context: str = None
    ) -> bool:
        """应用修复到文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 计算行号
            lines_before = content[:content.find(old_url)].count('\n') + 1 if old_url in content else 0
            
            # 替换URL
            new_content = content.replace(old_url, new_url)
            
            if new_content == content:
                return False
            
            if not self.dry_run:
                # 备份原文件
                backup_path = file_path.with_suffix('.md.bak')
                if not backup_path.exists():
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                
                # 写入修复后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            
            self.fixes_applied.append({
                'file': str(file_path),
                'line': lines_before,
                'old_url': old_url,
                'new_url': new_url,
                'context': context
            })
            
            return True
            
        except Exception as e:
            print(f"   ❌ 修复失败 {file_path}: {e}")
            return False
    
    def mark_link_for_manual_fix(
        self, 
        file_path: Path, 
        url: str, 
        reason: str
    ) -> bool:
        """标记链接需要人工修复"""
        self.fixes_needed.append({
            'file': str(file_path),
            'url': url,
            'reason': reason,
            'suggested_archive': self.create_archive_link(url)
        })
        return True


# =============================================================================
# 批量处理
# =============================================================================

def process_link_health_report(
    report_path: Path,
    fixer: LinkFixer,
    auto_fix: bool = False,
    archive_broken: bool = False
) -> Dict:
    """处理链接健康报告"""
    
    # 读取报告
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    broken_links = report.get('broken_links', [])
    redirect_links = report.get('redirect_links', [])
    
    print(f"\n📋 报告摘要:")
    print(f"   失效链接: {len(broken_links)}")
    print(f"   重定向链接: {len(redirect_links)}")
    
    # 处理重定向链接（自动修复）
    if redirect_links and auto_fix:
        print(f"\n🔄 处理重定向链接...")
        fixed_count = 0
        
        for link in redirect_links:
            file_path = Path(link['file'])
            old_url = link['original_url']
            new_url = link.get('redirect_url', old_url)
            
            if fixer.apply_fix_to_file(file_path, old_url, new_url, 'auto_redirect'):
                fixed_count += 1
                print(f"   ✅ {file_path}: {old_url[:60]}...")
        
        print(f"   已修复 {fixed_count} 个重定向链接")
    
    # 处理失效链接
    if broken_links:
        print(f"\n🔧 分析失效链接...")
        
        for link in broken_links:
            file_path = Path(link['file'])
            url = link['url']
            
            # 尝试自动修复
            fix_result = fixer.fix_link(url)
            
            if fix_result['was_fixed'] and auto_fix:
                # 应用自动修复
                fixer.apply_fix_to_file(
                    file_path,
                    url,
                    fix_result['fixed_url'],
                    fix_result['reason']
                )
            elif fix_result['needs_manual'] or not fix_result['was_fixed']:
                # 标记需要人工修复
                fixer.mark_link_for_manual_fix(
                    file_path,
                    url,
                    fix_result['reason']
                )
                
                if archive_broken:
                    # 生成存档链接建议
                    archive_url = fixer.create_archive_link(url)
                    print(f"   📝 {file_path}: {url[:50]}...")
                    print(f"      建议存档: {archive_url[:60]}...")
    
    return {
        'fixed': len(fixer.fixes_applied),
        'needs_manual': len(fixer.fixes_needed)
    }


def fix_specific_pattern(
    root_path: Path,
    fixer: LinkFixer,
    old_pattern: str,
    new_pattern: str,
    use_regex: bool = False
) -> int:
    """修复特定模式的链接"""
    print(f"\n🔍 搜索模式: {old_pattern}")
    
    md_files = list(root_path.rglob('*.md'))
    md_files = [
        f for f in md_files 
        if not any(part.startswith('.') for part in f.parts)
    ]
    
    fixed_count = 0
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            if use_regex:
                new_content = re.sub(old_pattern, new_pattern, content)
            else:
                new_content = content.replace(old_pattern, new_pattern)
            
            if new_content != original_content:
                if not fixer.dry_run:
                    # 备份
                    backup_path = md_file.with_suffix('.md.bak')
                    if not backup_path.exists():
                        with open(backup_path, 'w', encoding='utf-8') as f:
                            f.write(original_content)
                    
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                
                fixed_count += 1
                print(f"   ✅ {md_file}")
                
        except Exception as e:
            print(f"   ❌ 处理失败 {md_file}: {e}")
    
    return fixed_count


# =============================================================================
# 报告生成
# =============================================================================

def generate_fix_report(fixer: LinkFixer, output_path: Path):
    """生成修复报告"""
    lines = [
        "# 🔧 链接修复报告",
        "",
        f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 📊 修复统计",
        "",
        f"- ✅ 自动修复: {len(fixer.fixes_applied)} 个链接",
        f"- 📝 需要人工修复: {len(fixer.fixes_needed)} 个链接",
        "",
    ]
    
    # 自动修复详情
    if fixer.fixes_applied:
        lines.extend([
            "## ✅ 自动修复详情",
            "",
        ])
        
        for fix in fixer.fixes_applied:
            lines.extend([
                f"### {fix['file']} (第{fix['line']}行)",
                "",
                f"**原文:**",
                f"```",
                f"[{fix['old_url']}]({fix['old_url']})",
                f"```",
                "",
                f"**修复后:**",
                f"```",
                f"[{fix['new_url']}]({fix['new_url']})",
                f"```",
                "",
            ])
    
    # 需要人工修复的链接
    if fixer.fixes_needed:
        lines.extend([
            "## 📝 需要人工修复",
            "",
            "以下链接无法自动修复，请人工处理：",
            "",
        ])
        
        # 按文件分组
        by_file = {}
        for item in fixer.fixes_needed:
            file = item['file']
            if file not in by_file:
                by_file[file] = []
            by_file[file].append(item)
        
        for file, items in sorted(by_file.items()):
            lines.extend([
                f"### {file}",
                "",
            ])
            
            for item in items:
                lines.extend([
                    f"- **URL**: `{item['url']}`",
                    f"  - 原因: {item['reason']}",
                    f"  - 建议存档: [{item['suggested_archive'][:50]}...]({item['suggested_archive']})",
                    "",
                ])
        
        lines.extend([
            "### 人工修复指南",
            "",
            "1. **使用Wayback Machine存档**:",
            "   - 访问 https://web.archive.org/",
            "   - 输入失效URL搜索历史版本",
            "   - 使用存档链接替换原链接",
            "",
            "2. **查找官方迁移文档**:",
            "   - 检查原站点是否有迁移公告",
            "   - 搜索新域名下的对应页面",
            "",
            "3. **移除不可用的链接**:",
            "   - 如果内容完全无法访问，考虑移除链接",
            "   - 保留文字说明但移除超链接",
            "",
        ])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


# =============================================================================
# 主程序
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 失效链接修复工具'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # process-report 命令
    process_parser = subparsers.add_parser(
        'process-report',
        help='处理链接健康报告'
    )
    process_parser.add_argument(
        'report',
        help='JSON格式链接健康报告路径'
    )
    process_parser.add_argument(
        '--auto-fix', '-a',
        action='store_true',
        help='自动应用可修复的更改'
    )
    process_parser.add_argument(
        '--archive-broken', '-A',
        action='store_true',
        help='为失效链接生成存档建议'
    )
    
    # fix-pattern 命令
    pattern_parser = subparsers.add_parser(
        'fix-pattern',
        help='修复特定模式的链接'
    )
    pattern_parser.add_argument(
        'old_pattern',
        help='要查找的模式'
    )
    pattern_parser.add_argument(
        'new_pattern',
        help='替换为的模式'
    )
    pattern_parser.add_argument(
        '--regex', '-r',
        action='store_true',
        help='使用正则表达式'
    )
    pattern_parser.add_argument(
        '--path', '-p',
        default='.',
        help='搜索的根目录'
    )
    
    # 通用参数
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='试运行（不实际修改文件）'
    )
    parser.add_argument(
        '--output', '-o',
        default='reports/link-fix-report.md',
        help='修复报告输出路径'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 创建修复器
    fixer = LinkFixer(dry_run=args.dry_run)
    
    if args.dry_run:
        print("🧪 试运行模式 - 不会实际修改文件")
    
    print("=" * 70)
    print("AnalysisDataFlow 失效链接修复工具")
    print("=" * 70)
    
    if args.command == 'process-report':
        report_path = Path(args.report)
        if not report_path.exists():
            print(f"❌ 报告文件不存在: {report_path}")
            return
        
        stats = process_link_health_report(
            report_path,
            fixer,
            auto_fix=args.auto_fix,
            archive_broken=args.archive_broken
        )
        
        print("\n📊 处理结果:")
        print(f"   已修复: {stats['fixed']}")
        print(f"   需要人工: {stats['needs_manual']}")
    
    elif args.command == 'fix-pattern':
        root_path = Path(args.path)
        fixed = fix_specific_pattern(
            root_path,
            fixer,
            args.old_pattern,
            args.new_pattern,
            use_regex=args.regex
        )
        
        print(f"\n📊 修复了 {fixed} 个文件")
    
    # 生成修复报告
    if fixer.fixes_applied or fixer.fixes_needed:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        generate_fix_report(fixer, output_path)
        print(f"\n📝 修复报告已保存: {output_path}")


if __name__ == '__main__':
    main()
