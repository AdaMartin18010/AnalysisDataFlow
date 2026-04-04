#!/usr/bin/env python3
"""
AnalysisDataFlow 自动化翻译工作流
Automated Translation Workflow

功能:
- 监控源文档变更
- 提取待翻译内容
- 管理翻译状态
- 生成翻译报告
- 触发质量检查

用法:
    python translate_workflow.py <command> [options]

命令:
    monitor      监控文档变更
    extract      提取翻译内容
    update       更新翻译状态
    report       生成翻译报告
    sync         同步翻译与源文档

版本: 1.0.0
作者: AnalysisDataFlow Team
"""

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
import yaml


# =============================================================================
# Configuration
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
I18N_DIR = PROJECT_ROOT / "i18n"
CONFIG_FILE = I18N_DIR / "config" / "i18n.json"
GLOSSARY_FILE = I18N_DIR / "config" / "glossary-core.json"

REPORT_DIR = PROJECT_ROOT / "reports" / "i18n"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_CONFIG = {
    "source_language": "zh",
    "target_languages": ["en"],
    "content_dirs": ["Struct", "Knowledge", "Flink"],
    "priority_docs": ["README.md", "QUICK-START.md", "GLOSSARY.md", "CONTRIBUTING.md"],
    "excluded_patterns": ["*.draft.md", "*.archived.md", "reports/*", "tmp_*"],
}


class TranslationStatus(Enum):
    """翻译状态"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    COMPLETED = "completed"
    OUTDATED = "outdated"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class DocumentMapping:
    """文档映射关系"""
    source_path: str
    target_path: str
    source_hash: str = ""
    target_hash: str = ""
    status: TranslationStatus = TranslationStatus.NOT_STARTED
    completion: float = 0.0
    last_sync: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "source_path": self.source_path,
            "target_path": self.target_path,
            "source_hash": self.source_hash,
            "target_hash": self.target_hash,
            "status": self.status.value,
            "completion": self.completion,
            "last_sync": self.last_sync
        }


@dataclass
class TranslationTask:
    """翻译任务"""
    task_id: str
    source_file: Path
    target_file: Path
    source_lang: str
    target_lang: str
    priority: int  # 1-5, 1 highest
    word_count: int
    created_at: str
    
    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "source_file": str(self.source_file),
            "target_file": str(self.target_file),
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "priority": self.priority,
            "word_count": self.word_count,
            "created_at": self.created_at
        }


# =============================================================================
# Core Classes
# =============================================================================

class FileUtils:
    """文件工具类"""
    
    @staticmethod
    def compute_hash(file_path: Path) -> str:
        """计算文件SHA256哈希"""
        if not file_path.exists():
            return ""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()[:16]
    
    @staticmethod
    def count_words(content: str) -> int:
        """估算字数"""
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        english_words = len(re.findall(r'[a-zA-Z]+', content))
        return chinese_chars + english_words
    
    @staticmethod
    def load_json(file_path: Path) -> Dict:
        """加载JSON文件"""
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def save_json(file_path: Path, data: Dict):
        """保存JSON文件"""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


class GlossaryManager:
    """术语表管理器"""
    
    def __init__(self, glossary_path: Path = GLOSSARY_FILE):
        self.glossary_path = glossary_path
        self.terms: Dict[str, Dict] = {}
        self._load_glossary()
    
    def _load_glossary(self):
        """加载术语表"""
        data = FileUtils.load_json(self.glossary_path)
        for term in data.get("terms", []):
            self.terms[term["chinese"]] = term
    
    def get_translation(self, chinese_term: str, target_lang: str = "en") -> Optional[str]:
        """获取术语翻译"""
        if chinese_term in self.terms:
            return self.terms[chinese_term].get(target_lang)
        return None
    
    def check_consistency(self, content: str, target_lang: str = "en") -> List[Dict]:
        """检查术语一致性"""
        issues = []
        for chinese, term in self.terms.items():
            if chinese in content:
                expected = term.get(target_lang, "")
                # 简单检查：如果中文存在但英文不存在，可能是未翻译
                if target_lang == "en" and expected and expected not in content:
                    issues.append({
                        "term": chinese,
                        "expected": expected,
                        "severity": "warning"
                    })
        return issues


class TranslationWorkflow:
    """翻译工作流管理器"""
    
    def __init__(self, config: Dict = None):
        self.config = config or DEFAULT_CONFIG
        self.source_lang = self.config.get("source_language", "zh")
        self.target_langs = self.config.get("target_languages", ["en"])
        self.mappings: List[DocumentMapping] = []
        self.glossary = GlossaryManager()
    
    def _is_excluded(self, file_path: Path) -> bool:
        """检查文件是否在排除列表"""
        patterns = self.config.get("excluded_patterns", [])
        path_str = str(file_path)
        for pattern in patterns:
            if pattern in path_str or path_str.endswith(pattern.replace("*", "")):
                return True
        return False
    
    def scan_source_files(self) -> List[Path]:
        """扫描源文件"""
        source_files = []
        
        # 扫描根目录MD文件
        for md_file in PROJECT_ROOT.glob("*.md"):
            if not self._is_excluded(md_file):
                source_files.append(md_file)
        
        # 扫描内容目录
        for content_dir in self.config.get("content_dirs", []):
            dir_path = PROJECT_ROOT / content_dir
            if dir_path.exists():
                for md_file in dir_path.rglob("*.md"):
                    if not self._is_excluded(md_file):
                        source_files.append(md_file)
        
        return sorted(source_files)
    
    def build_mappings(self):
        """构建文档映射"""
        self.mappings = []
        source_files = self.scan_source_files()
        
        for src_file in source_files:
            rel_path = src_file.relative_to(PROJECT_ROOT)
            source_hash = FileUtils.compute_hash(src_file)
            
            for target_lang in self.target_langs:
                target_file = I18N_DIR / target_lang / "docs" / rel_path
                
                # 确定状态
                if not target_file.exists():
                    status = TranslationStatus.NOT_STARTED
                    completion = 0.0
                else:
                    target_hash = FileUtils.compute_hash(target_file)
                    target_content = target_file.read_text(encoding='utf-8')
                    
                    # 解析frontmatter检查状态
                    frontmatter = self._extract_frontmatter(target_content)
                    status_str = frontmatter.get("translation_status", "unknown")
                    try:
                        status = TranslationStatus(status_str)
                    except ValueError:
                        status = TranslationStatus.NOT_STARTED
                    
                    completion = frontmatter.get("completion_percentage", 0.0)
                    
                    # 检查是否过期
                    source_version = frontmatter.get("source_version", "")
                    if source_version != source_hash:
                        status = TranslationStatus.OUTDATED
                
                mapping = DocumentMapping(
                    source_path=str(rel_path),
                    target_path=str(target_file.relative_to(PROJECT_ROOT)),
                    source_hash=source_hash,
                    status=status,
                    completion=completion,
                    last_sync=datetime.now().isoformat()
                )
                self.mappings.append(mapping)
    
    def _extract_frontmatter(self, content: str) -> Dict:
        """提取YAML frontmatter"""
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                pass
        return {}
    
    def generate_report(self) -> Dict:
        """生成翻译报告"""
        if not self.mappings:
            self.build_mappings()
        
        total = len(self.mappings)
        stats = {
            "total": total,
            "not_started": 0,
            "in_progress": 0,
            "pending_review": 0,
            "completed": 0,
            "outdated": 0
        }
        
        for mapping in self.mappings:
            stats[mapping.status.value] += 1
        
        completion_rate = (stats["completed"] / total * 100) if total > 0 else 0
        
        # 优先级文档统计
        priority_docs = self.config.get("priority_docs", [])
        priority_stats = {
            "total": len(priority_docs),
            "completed": 0,
            "missing": []
        }
        
        for doc in priority_docs:
            mapping = next((m for m in self.mappings if m.source_path == doc), None)
            if mapping and mapping.status == TranslationStatus.COMPLETED:
                priority_stats["completed"] += 1
            else:
                priority_stats["missing"].append(doc)
        
        return {
            "generated_at": datetime.now().isoformat(),
            "overall": {
                "total_docs": total,
                "completion_rate": round(completion_rate, 2),
                "status_breakdown": stats
            },
            "priority_docs": priority_stats,
            "details": [m.to_dict() for m in self.mappings]
        }
    
    def extract_translation_package(self, target_lang: str = "en", 
                                   priority_only: bool = False) -> List[TranslationTask]:
        """提取翻译包"""
        tasks = []
        
        if priority_only:
            files_to_process = [PROJECT_ROOT / f for f in self.config.get("priority_docs", [])]
        else:
            files_to_process = self.scan_source_files()
        
        task_id = 1
        for src_file in files_to_process:
            if not src_file.exists():
                continue
            
            rel_path = src_file.relative_to(PROJECT_ROOT)
            target_file = I18N_DIR / target_lang / "docs" / rel_path
            
            # 跳过已完成且未过期的
            if target_file.exists():
                target_content = target_file.read_text(encoding='utf-8')
                frontmatter = self._extract_frontmatter(target_content)
                if frontmatter.get("translation_status") == "completed":
                    source_hash = FileUtils.compute_hash(src_file)
                    if frontmatter.get("source_version") == source_hash:
                        continue
            
            # 计算优先级和字数
            content = src_file.read_text(encoding='utf-8')
            word_count = FileUtils.count_words(content)
            priority = 1 if str(rel_path) in self.config.get("priority_docs", []) else 3
            
            task = TranslationTask(
                task_id=f"TASK-{task_id:04d}",
                source_file=src_file,
                target_file=target_file,
                source_lang=self.source_lang,
                target_lang=target_lang,
                priority=priority,
                word_count=word_count,
                created_at=datetime.now().isoformat()
            )
            tasks.append(task)
            task_id += 1
        
        return sorted(tasks, key=lambda t: t.priority)
    
    def save_report(self, report: Dict, output_path: Optional[Path] = None):
        """保存报告"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d")
            output_path = REPORT_DIR / f"translation-report-{timestamp}.json"
        
        FileUtils.save_json(output_path, report)
        print(f"Report saved: {output_path}")
    
    def save_translation_tasks(self, tasks: List[TranslationTask], 
                               output_path: Optional[Path] = None):
        """保存翻译任务"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d")
            output_path = REPORT_DIR / f"translation-tasks-{timestamp}.json"
        
        data = {
            "generated_at": datetime.now().isoformat(),
            "total_tasks": len(tasks),
            "tasks": [t.to_dict() for t in tasks]
        }
        FileUtils.save_json(output_path, data)
        print(f"Translation tasks saved: {output_path}")


# =============================================================================
# CLI Commands
# =============================================================================

def cmd_monitor(args):
    """监控文档变更"""
    print("=" * 60)
    print("  AnalysisDataFlow Translation Monitor")
    print("=" * 60)
    
    workflow = TranslationWorkflow()
    workflow.build_mappings()
    
    outdated = [m for m in workflow.mappings if m.status == TranslationStatus.OUTDATED]
    missing = [m for m in workflow.mappings if m.status == TranslationStatus.NOT_STARTED]
    
    print(f"\n📊 Status Summary:")
    print(f"  Total Documents: {len(workflow.mappings)}")
    print(f"  Outdated: {len(outdated)}")
    print(f"  Missing: {len(missing)}")
    
    if outdated:
        print(f"\n🔄 Outdated Documents (top 10):")
        for m in outdated[:10]:
            print(f"  - {m.source_path}")
    
    if missing:
        print(f"\n📋 Missing Documents (top 10):")
        for m in missing[:10]:
            print(f"  - {m.source_path}")


def cmd_extract(args):
    """提取翻译内容"""
    print("=" * 60)
    print("  Extracting Translation Tasks")
    print("=" * 60)
    
    workflow = TranslationWorkflow()
    tasks = workflow.extract_translation_package(
        target_lang=args.lang or "en",
        priority_only=args.priority
    )
    
    print(f"\n📦 Extracted {len(tasks)} translation tasks")
    print(f"  Target Language: {args.lang or 'en'}")
    print(f"  Priority Only: {args.priority}")
    
    if tasks:
        total_words = sum(t.word_count for t in tasks)
        print(f"  Total Words: {total_words}")
        print(f"\n📝 Task List (top 10):")
        for t in tasks[:10]:
            print(f"  [{t.task_id}] {t.source_file.name}")
            print(f"    Words: {t.word_count} | Priority: {t.priority}")
    
    if args.output:
        workflow.save_translation_tasks(tasks, Path(args.output))


def cmd_report(args):
    """生成翻译报告"""
    print("=" * 60)
    print("  Generating Translation Report")
    print("=" * 60)
    
    workflow = TranslationWorkflow()
    report = workflow.generate_report()
    
    print(f"\n📊 Overall Statistics:")
    print(f"  Total Documents: {report['overall']['total_docs']}")
    print(f"  Completion Rate: {report['overall']['completion_rate']:.1f}%")
    
    print(f"\n📈 Status Breakdown:")
    for status, count in report['overall']['status_breakdown'].items():
        print(f"  {status}: {count}")
    
    print(f"\n🎯 Priority Documents:")
    print(f"  Total: {report['priority_docs']['total']}")
    print(f"  Completed: {report['priority_docs']['completed']}")
    
    if report['priority_docs']['missing']:
        print(f"  Missing: {', '.join(report['priority_docs']['missing'][:5])}")
    
    if args.output:
        workflow.save_report(report, Path(args.output))
    else:
        # 同时生成Markdown报告
        md_report = generate_markdown_report(report)
        md_path = REPORT_DIR / f"translation-report-{datetime.now().strftime('%Y%m%d')}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_report)
        print(f"\n📝 Markdown report saved: {md_path}")


def generate_markdown_report(report: Dict) -> str:
    """生成Markdown格式报告"""
    md = f"""# Translation Progress Report

> Generated: {report['generated_at']}

## Overall Statistics

| Metric | Value |
|--------|-------|
| Total Documents | {report['overall']['total_docs']} |
| Completion Rate | {report['overall']['completion_rate']:.1f}% |

## Status Breakdown

| Status | Count | Percentage |
|--------|-------|------------|
"""
    total = report['overall']['total_docs']
    for status, count in report['overall']['status_breakdown'].items():
        pct = (count / total * 100) if total > 0 else 0
        md += f"| {status} | {count} | {pct:.1f}% |\n"
    
    md += f"""
## Priority Documents

- **Total**: {report['priority_docs']['total']}
- **Completed**: {report['priority_docs']['completed']}
- **Completion Rate**: {(report['priority_docs']['completed'] / report['priority_docs']['total'] * 100):.1f}%

### Missing Priority Documents

"""
    for doc in report['priority_docs']['missing']:
        md += f"- [ ] {doc}\n"
    
    return md


def main():
    parser = argparse.ArgumentParser(
        prog='translate_workflow',
        description='AnalysisDataFlow Automated Translation Workflow',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Monitor document changes
  python translate_workflow.py monitor
  
  # Extract translation tasks
  python translate_workflow.py extract --lang en --priority
  
  # Generate report
  python translate_workflow.py report --output report.json
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor document changes')
    
    # extract command
    extract_parser = subparsers.add_parser('extract', help='Extract translation tasks')
    extract_parser.add_argument('--lang', '-l', default='en', help='Target language')
    extract_parser.add_argument('--priority', '-p', action='store_true', 
                                help='Extract priority documents only')
    extract_parser.add_argument('--output', '-o', help='Output file path')
    
    # report command
    report_parser = subparsers.add_parser('report', help='Generate translation report')
    report_parser.add_argument('--output', '-o', help='Output JSON file path')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'monitor':
        cmd_monitor(args)
    elif args.command == 'extract':
        cmd_extract(args)
    elif args.command == 'report':
        cmd_report(args)


if __name__ == '__main__':
    main()
