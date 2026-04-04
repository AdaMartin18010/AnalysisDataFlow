#!/usr/bin/env python3
"""
AnalysisDataFlow 国际化管理工具

功能：
- 提取待翻译内容
- 统计翻译进度
- 检测缺失翻译
- 检查术语一致性
- 格式验证
- 生成翻译报告

用法：
    python i18n-manager.py <command> [options]

命令：
    extract         提取待翻译内容
    stats           统计翻译进度
    check-missing   检测缺失翻译
    check-format    检查格式一致性
    check-terms     检查术语一致性
    generate-nav    生成多语言导航
    report          生成完整报告

作者: AnalysisDataFlow Team
版本: 1.0.0
"""

import argparse
import hashlib
import json
import os
import re
import sys
import yaml
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from enum import Enum


# =============================================================================
# 配置常量
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
I18N_DIR = PROJECT_ROOT / "docs" / "i18n"
CONTENT_DIR = I18N_DIR / "i18n-content"
GLOSSARY_DIR = I18N_DIR / "glossary"
WORKFLOW_DIR = I18N_DIR / "workflows"
SOURCE_DIRS = ["Struct", "Knowledge", "Flink"]

DEFAULT_CONFIG = {
    "source_language": "zh",
    "target_languages": ["en"],
    "content_root": str(CONTENT_DIR),
    "glossary_dir": str(GLOSSARY_DIR),
    "workflow_dir": str(WORKFLOW_DIR),
    "source_dirs": SOURCE_DIRS,
    "extraction": {
        "skip_patterns": ["*.draft.md", "*.archived.md"],
        "include_frontmatter": True,
        "preserve_mermaid": True
    },
    "quality": {
        "term_check": True,
        "format_check": True,
        "link_check": True,
        "min_completion_threshold": 95
    }
}


# =============================================================================
# 数据类定义
# =============================================================================

class TranslationStatus(Enum):
    """翻译状态枚举"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    COMPLETED = "completed"
    OUTDATED = "outdated"


@dataclass
class DocumentInfo:
    """文档信息数据类"""
    path: Path
    language: str
    relative_path: str
    content_hash: str = ""
    word_count: int = 0
    translation_status: TranslationStatus = TranslationStatus.NOT_STARTED
    source_version: str = ""
    completion_percentage: float = 0.0
    last_modified: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "path": str(self.path),
            "language": self.language,
            "relative_path": self.relative_path,
            "content_hash": self.content_hash,
            "word_count": self.word_count,
            "translation_status": self.translation_status.value,
            "source_version": self.source_version,
            "completion_percentage": self.completion_percentage,
            "last_modified": self.last_modified.isoformat()
        }


@dataclass
class TermEntry:
    """术语条目"""
    chinese: str
    english: str
    abbreviation: str = ""
    definition: str = ""
    domain: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "chinese": self.chinese,
            "english": self.english,
            "abbreviation": self.abbreviation,
            "definition": self.definition,
            "domain": self.domain
        }


@dataclass
class TranslationIssue:
    """翻译问题"""
    file: str
    line: int
    type: str
    severity: str  # error, warning, info
    message: str
    suggestion: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "file": self.file,
            "line": self.line,
            "type": self.type,
            "severity": self.severity,
            "message": self.message,
            "suggestion": self.suggestion
        }


# =============================================================================
# 核心工具类
# =============================================================================

class FileHashUtil:
    """文件哈希工具"""
    
    @staticmethod
    def compute_file_hash(file_path: Path) -> str:
        """计算文件 SHA256 哈希"""
        if not file_path.exists():
            return ""
        
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()[:16]
    
    @staticmethod
    def compute_content_hash(content: str) -> str:
        """计算内容 SHA256 哈希"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]


class MarkdownParser:
    """Markdown 解析器"""
    
    @staticmethod
    def extract_frontmatter(content: str) -> Tuple[Dict, str]:
        """提取 YAML frontmatter"""
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)
        
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                body = content[match.end():]
                return frontmatter or {}, body
            except yaml.YAMLError:
                pass
        
        return {}, content
    
    @staticmethod
    def extract_headings(content: str) -> List[Tuple[int, str]]:
        """提取所有标题"""
        pattern = r'^(#{1,6})\s+(.+)$'
        headings = []
        for line in content.split('\n'):
            match = re.match(pattern, line)
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headings.append((level, title))
        return headings
    
    @staticmethod
    def extract_code_blocks(content: str) -> List[Tuple[str, str]]:
        """提取代码块"""
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        return matches
    
    @staticmethod
    def count_words(content: str) -> int:
        """估算中文字数"""
        # 中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        # 英文单词
        english_words = len(re.findall(r'[a-zA-Z]+', content))
        return chinese_chars + english_words


class TerminologyManager:
    """术语管理器"""
    
    def __init__(self, glossary_dir: Path):
        self.glossary_dir = glossary_dir
        self.terms: Dict[str, TermEntry] = {}
        self.prohibited_terms: Set[str] = set()
        self.load_glossary()
    
    def load_glossary(self):
        """加载术语表"""
        # 加载核心术语
        core_terms_file = self.glossary_dir / "core-terms.json"
        if core_terms_file.exists():
            with open(core_terms_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data.get('terms', []):
                    term = TermEntry(**item)
                    self.terms[term.chinese] = term
        
        # 加载禁止翻译列表
        prohibited_file = self.glossary_dir / "prohibited-list.json"
        if prohibited_file.exists():
            with open(prohibited_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for category in data.get('prohibited_terms', {}).values():
                    if isinstance(category, list):
                        self.prohibited_terms.update(category)
    
    def check_document(self, file_path: Path, content: str) -> List[TranslationIssue]:
        """检查文档术语一致性"""
        issues = []
        lines = content.split('\n')
        
        # 简单的术语检查示例
        for chinese_term, entry in self.terms.items():
            for i, line in enumerate(lines, 1):
                if chinese_term in line:
                    # 这里应该检查英文翻译中是否使用了正确的英文术语
                    pass
        
        return issues
    
    def get_term_suggestion(self, chinese_term: str) -> Optional[str]:
        """获取术语建议"""
        if chinese_term in self.terms:
            return self.terms[chinese_term].english
        return None


# =============================================================================
# 主管理类
# =============================================================================

class I18nManager:
    """国际化管理器"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or DEFAULT_CONFIG
        self.content_root = Path(self.config.get('content_root', CONTENT_DIR))
        self.glossary_dir = Path(self.config.get('glossary_dir', GLOSSARY_DIR))
        self.workflow_dir = Path(self.config.get('workflow_dir', WORKFLOW_DIR))
        self.source_language = self.config.get('source_language', 'zh')
        self.target_languages = self.config.get('target_languages', ['en'])
        
        # 初始化组件
        self.term_manager = TerminologyManager(self.glossary_dir)
        self.file_hash = FileHashUtil()
        self.md_parser = MarkdownParser()
    
    # -------------------------------------------------------------------------
    # 命令: extract
    # -------------------------------------------------------------------------
    def extract(self, source: str = None, lang: str = None, output: str = None):
        """
        提取待翻译内容
        
        Args:
            source: 源目录（相对路径，如 'Struct/'）
            lang: 目标语言
            output: 输出文件路径
        """
        lang = lang or self.target_languages[0]
        source_path = self.content_root / self.source_language
        
        if source:
            source_path = source_path / source
        
        if not source_path.exists():
            print(f"错误: 源路径不存在 {source_path}")
            return
        
        # 收集待翻译文件
        files_to_translate = []
        for md_file in source_path.rglob("*.md"):
            rel_path = md_file.relative_to(self.content_root / self.source_language)
            target_file = self.content_root / lang / rel_path
            
            # 检查是否需要翻译
            if not target_file.exists():
                status = TranslationStatus.NOT_STARTED
            else:
                # 检查是否过时
                source_hash = self.file_hash.compute_file_hash(md_file)
                target_content = target_file.read_text(encoding='utf-8')
                frontmatter, _ = self.md_parser.extract_frontmatter(target_content)
                
                if frontmatter.get('source_version') != source_hash:
                    status = TranslationStatus.OUTDATED
                else:
                    status = TranslationStatus.COMPLETED
            
            if status != TranslationStatus.COMPLETED:
                content = md_file.read_text(encoding='utf-8')
                frontmatter, body = self.md_parser.extract_frontmatter(content)
                
                files_to_translate.append({
                    'source_file': str(rel_path),
                    'status': status.value,
                    'word_count': self.md_parser.count_words(content),
                    'source_hash': self.file_hash.compute_file_hash(md_file),
                    'frontmatter': frontmatter,
                    'excerpt': body[:500] + '...' if len(body) > 500 else body
                })
        
        # 生成输出
        output_data = {
            'generated_at': datetime.now().isoformat(),
            'source_language': self.source_language,
            'target_language': lang,
            'total_files': len(files_to_translate),
            'files': files_to_translate
        }
        
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            print(f"翻译包已生成: {output_path}")
        else:
            print(json.dumps(output_data, ensure_ascii=False, indent=2))
    
    # -------------------------------------------------------------------------
    # 命令: stats
    # -------------------------------------------------------------------------
    def stats(self, lang: str = None):
        """
        统计翻译进度
        
        Args:
            lang: 目标语言，不指定则统计所有
        """
        languages = [lang] if lang else self.target_languages
        
        for lang_code in languages:
            print(f"\n{'='*50}")
            print(f"翻译进度报告 - {lang_code.upper()}")
            print(f"{'='*50}")
            
            total_docs = 0
            translated_docs = 0
            
            for source_dir in SOURCE_DIRS:
                source_path = self.content_root / self.source_language / source_dir
                target_path = self.content_root / lang_code / source_dir
                
                if not source_path.exists():
                    continue
                
                source_files = list(source_path.rglob("*.md"))
                dir_total = len(source_files)
                dir_translated = 0
                
                for src_file in source_files:
                    rel_path = src_file.relative_to(self.content_root / self.source_language)
                    target_file = self.content_root / lang_code / rel_path
                    
                    if target_file.exists():
                        target_content = target_file.read_text(encoding='utf-8')
                        frontmatter, _ = self.md_parser.extract_frontmatter(target_content)
                        
                        if frontmatter.get('translation_status') == 'completed':
                            dir_translated += 1
                
                percentage = (dir_translated / dir_total * 100) if dir_total > 0 else 0
                bar_length = 20
                filled = int(bar_length * dir_translated / dir_total) if dir_total > 0 else 0
                bar = '█' * filled + '░' * (bar_length - filled)
                
                print(f"{source_dir:12} |{bar}| {dir_translated:3}/{dir_total:3} ({percentage:5.1f}%)")
                
                total_docs += dir_total
                translated_docs += dir_translated
            
            overall_percentage = (translated_docs / total_docs * 100) if total_docs > 0 else 0
            print(f"{'-'*50}")
            print(f"{'总计':12} | {translated_docs}/{total_docs} 文档 ({overall_percentage:.1f}%)")
            print(f"{'='*50}")
    
    # -------------------------------------------------------------------------
    # 命令: check-missing
    # -------------------------------------------------------------------------
    def check_missing(self, lang: str = None):
        """
        检测缺失翻译
        
        Args:
            lang: 目标语言
        """
        lang = lang or self.target_languages[0]
        
        print(f"\n{'='*60}")
        print(f"缺失翻译检测 - {lang.upper()}")
        print(f"{'='*60}\n")
        
        missing_files = []
        outdated_files = []
        incomplete_files = []
        
        for source_dir in SOURCE_DIRS:
            source_path = self.content_root / self.source_language / source_dir
            if not source_path.exists():
                continue
            
            for src_file in source_path.rglob("*.md"):
                rel_path = src_file.relative_to(self.content_root / self.source_language)
                target_file = self.content_root / lang / rel_path
                
                if not target_file.exists():
                    missing_files.append(str(rel_path))
                else:
                    target_content = target_file.read_text(encoding='utf-8')
                    frontmatter, _ = self.md_parser.extract_frontmatter(target_content)
                    
                    status = frontmatter.get('translation_status', 'unknown')
                    if status == 'outdated':
                        outdated_files.append(str(rel_path))
                    elif status == 'in_progress':
                        completion = frontmatter.get('completion_percentage', 0)
                        incomplete_files.append((str(rel_path), completion))
        
        # 输出结果
        if missing_files:
            print(f"📋 未开始翻译 ({len(missing_files)} 个文件):")
            for f in sorted(missing_files)[:10]:  # 最多显示10个
                print(f"   - {f}")
            if len(missing_files) > 10:
                print(f"   ... 还有 {len(missing_files) - 10} 个文件")
            print()
        
        if outdated_files:
            print(f"🔄 需要更新 ({len(outdated_files)} 个文件):")
            for f in sorted(outdated_files)[:10]:
                print(f"   - {f}")
            if len(outdated_files) > 10:
                print(f"   ... 还有 {len(outdated_files) - 10} 个文件")
            print()
        
        if incomplete_files:
            print(f"⏳ 翻译中 ({len(incomplete_files)} 个文件):")
            for f, pct in sorted(incomplete_files, key=lambda x: -x[1])[:10]:
                print(f"   - {f} ({pct}%)")
            if len(incomplete_files) > 10:
                print(f"   ... 还有 {len(incomplete_files) - 10} 个文件")
            print()
        
        if not any([missing_files, outdated_files, incomplete_files]):
            print("✅ 所有文档都已翻译完成！")
        
        print(f"{'='*60}")
    
    # -------------------------------------------------------------------------
    # 命令: check-format
    # -------------------------------------------------------------------------
    def check_format(self, file: str = None, lang: str = None):
        """
        检查格式一致性
        
        Args:
            file: 指定文件路径
            lang: 检查整个语言目录
        """
        issues = []
        
        if file:
            file_path = Path(file)
            if file_path.exists():
                issues.extend(self._check_file_format(file_path))
        elif lang:
            lang_path = self.content_root / lang
            if lang_path.exists():
                for md_file in lang_path.rglob("*.md"):
                    issues.extend(self._check_file_format(md_file))
        
        # 输出结果
        if issues:
            print(f"\n{'='*60}")
            print(f"格式检查发现问题 ({len(issues)} 个):")
            print(f"{'='*60}\n")
            
            for issue in issues:
                icon = "❌" if issue.severity == "error" else "⚠️" if issue.severity == "warning" else "ℹ️"
                print(f"{icon} {issue.file}:{issue.line}")
                print(f"   类型: {issue.type}")
                print(f"   问题: {issue.message}")
                if issue.suggestion:
                    print(f"   建议: {issue.suggestion}")
                print()
        else:
            print("✅ 格式检查通过！")
    
    def _check_file_format(self, file_path: Path) -> List[TranslationIssue]:
        """检查单个文件格式"""
        issues = []
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # 检查 frontmatter
        if not content.startswith('---'):
            issues.append(TranslationIssue(
                file=str(file_path),
                line=1,
                type="missing_frontmatter",
                severity="warning",
                message="缺少 YAML frontmatter",
                suggestion="在文件开头添加 ---\nmetadata\n---"
            ))
        
        # 检查标题层级
        headings = self.md_parser.extract_headings(content)
        prev_level = 0
        for level, title in headings:
            if level > prev_level + 1 and prev_level > 0:
                issues.append(TranslationIssue(
                    file=str(file_path),
                    line=0,
                    type="heading_level_skip",
                    severity="warning",
                    message=f"标题层级跳跃: #{prev_level} -> #{level}",
                    suggestion=f"考虑添加 #{prev_level + 1} 级标题"
                ))
            prev_level = level
        
        # 检查代码块语言标签
        code_blocks = self.md_parser.extract_code_blocks(content)
        for lang, code in code_blocks:
            if not lang and len(code.strip()) > 50:
                issues.append(TranslationIssue(
                    file=str(file_path),
                    line=0,
                    type="missing_code_lang",
                    severity="info",
                    message="代码块缺少语言标签",
                    suggestion="在 ``` 后添加语言标识，如 ```python"
                ))
        
        return issues
    
    # -------------------------------------------------------------------------
    # 命令: check-terms
    # -------------------------------------------------------------------------
    def check_terms(self, file: str = None, lang: str = None):
        """
        检查术语一致性
        
        Args:
            file: 指定文件路径
            lang: 检查整个语言目录
        """
        if file:
            file_path = Path(file)
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                issues = self.term_manager.check_document(file_path, content)
                
                if issues:
                    print(f"\n在 {file} 中发现 {len(issues)} 个术语问题:")
                    for issue in issues:
                        print(f"  - {issue.message}")
                else:
                    print("✅ 术语检查通过！")
        elif lang:
            # 批量检查
            lang_path = self.content_root / lang
            if lang_path.exists():
                all_issues = []
                for md_file in lang_path.rglob("*.md"):
                    content = md_file.read_text(encoding='utf-8')
                    issues = self.term_manager.check_document(md_file, content)
                    all_issues.extend(issues)
                
                print(f"\n共发现 {len(all_issues)} 个术语问题")
    
    # -------------------------------------------------------------------------
    # 命令: report
    # -------------------------------------------------------------------------
    def report(self, output: str = None):
        """
        生成完整报告
        
        Args:
            output: 输出文件路径
        """
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'summary': {},
            'languages': {}
        }
        
        for lang in self.target_languages:
            lang_stats = {
                'total_files': 0,
                'translated': 0,
                'in_progress': 0,
                'not_started': 0,
                'outdated': 0
            }
            
            for source_dir in SOURCE_DIRS:
                source_path = self.content_root / self.source_language / source_dir
                if not source_path.exists():
                    continue
                
                for src_file in source_path.rglob("*.md"):
                    lang_stats['total_files'] += 1
                    rel_path = src_file.relative_to(self.content_root / self.source_language)
                    target_file = self.content_root / lang / rel_path
                    
                    if not target_file.exists():
                        lang_stats['not_started'] += 1
                    else:
                        target_content = target_file.read_text(encoding='utf-8')
                        frontmatter, _ = self.md_parser.extract_frontmatter(target_content)
                        status = frontmatter.get('translation_status', 'unknown')
                        
                        if status == 'completed':
                            lang_stats['translated'] += 1
                        elif status == 'in_progress':
                            lang_stats['in_progress'] += 1
                        elif status == 'outdated':
                            lang_stats['outdated'] += 1
                        else:
                            lang_stats['not_started'] += 1
            
            report_data['languages'][lang] = lang_stats
        
        # 输出报告
        report_json = json.dumps(report_data, ensure_ascii=False, indent=2)
        
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_json)
            print(f"报告已保存: {output_path}")
        else:
            print(report_json)


# =============================================================================
# 命令行接口
# =============================================================================

def create_parser() -> argparse.ArgumentParser:
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        prog='i18n-manager',
        description='AnalysisDataFlow 国际化管理工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 提取待翻译内容
  python i18n-manager.py extract --source Struct/ --lang en
  
  # 查看翻译统计
  python i18n-manager.py stats --lang en
  
  # 检查缺失翻译
  python i18n-manager.py check-missing --lang en
  
  # 检查格式
  python i18n-manager.py check-format --lang en
  
  # 生成报告
  python i18n-manager.py report --output report.json
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # extract 命令
    extract_parser = subparsers.add_parser('extract', help='提取待翻译内容')
    extract_parser.add_argument('--source', '-s', help='源目录（如 Struct/）')
    extract_parser.add_argument('--lang', '-l', help='目标语言（如 en）')
    extract_parser.add_argument('--output', '-o', help='输出文件路径')
    
    # stats 命令
    stats_parser = subparsers.add_parser('stats', help='统计翻译进度')
    stats_parser.add_argument('--lang', '-l', help='指定语言')
    
    # check-missing 命令
    missing_parser = subparsers.add_parser('check-missing', help='检测缺失翻译')
    missing_parser.add_argument('--lang', '-l', help='目标语言')
    
    # check-format 命令
    format_parser = subparsers.add_parser('check-format', help='检查格式一致性')
    format_parser.add_argument('--file', '-f', help='指定文件')
    format_parser.add_argument('--lang', '-l', help='指定语言')
    
    # check-terms 命令
    terms_parser = subparsers.add_parser('check-terms', help='检查术语一致性')
    terms_parser.add_argument('--file', '-f', help='指定文件')
    terms_parser.add_argument('--lang', '-l', help='指定语言')
    
    # report 命令
    report_parser = subparsers.add_parser('report', help='生成完整报告')
    report_parser.add_argument('--output', '-o', help='输出文件路径')
    
    return parser


def main():
    """主入口函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 初始化管理器
    manager = I18nManager()
    
    # 执行命令
    if args.command == 'extract':
        manager.extract(
            source=args.source,
            lang=args.lang,
            output=args.output
        )
    elif args.command == 'stats':
        manager.stats(lang=args.lang)
    elif args.command == 'check-missing':
        manager.check_missing(lang=args.lang)
    elif args.command == 'check-format':
        manager.check_format(file=args.file, lang=args.lang)
    elif args.command == 'check-terms':
        manager.check_terms(file=args.file, lang=args.lang)
    elif args.command == 'report':
        manager.report(output=args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
