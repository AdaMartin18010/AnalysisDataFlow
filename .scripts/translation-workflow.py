#!/usr/bin/env python3
"""
Translation Workflow Manager for AnalysisDataFlow i18n

This script manages the translation workflow including:
- Extracting content for translation
- Managing translation queues
- Version locking and synchronization
- Quality checks and validation
- Progress tracking and reporting

Usage:
    python translation-workflow.py extract --source Struct/ --lang en
    python translation-workflow.py stats
    python translation-workflow.py check-missing --lang en
    python translation-workflow.py check-format --file en/Struct/01.01-stream-processing.md
"""

import argparse
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import yaml


# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
I18N_ROOT = PROJECT_ROOT / "docs" / "i18n"
CONTENT_ROOT = I18N_ROOT / "i18n-content"
GLOSSARY_DIR = I18N_ROOT / "glossary"
WORKFLOW_DIR = I18N_ROOT / "workflows"
CONFIG_FILE = I18N_ROOT / "config" / "i18n-config.yaml"

# Source directories to translate
SOURCE_DIRS = ["Struct", "Knowledge", "Flink"]


@dataclass
class TranslationStatus:
    """Represents the translation status of a document."""
    file: str
    source_version: str
    translation_status: str  # not_started, in_progress, pending_review, completed
    translator: Optional[str] = None
    reviewer: Optional[str] = None
    translated_at: Optional[str] = None
    reviewed_at: Optional[str] = None
    completion_percentage: int = 0
    target_language: str = "en"
    
    def to_dict(self) -> Dict:
        return {
            "file": self.file,
            "source_version": self.source_version,
            "translation_status": self.translation_status,
            "translator": self.translator,
            "reviewer": self.reviewer,
            "translated_at": self.translated_at,
            "reviewed_at": self.reviewed_at,
            "completion_percentage": self.completion_percentage,
            "target_language": self.target_language,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "TranslationStatus":
        return cls(**data)


@dataclass
class VersionLock:
    """Represents a version lock on a source document."""
    file: str
    locked_at: str
    locked_by: str
    target_language: str
    source_version: str
    expected_completion: str
    status: str  # active, released, cancelled
    
    def to_dict(self) -> Dict:
        return {
            "file": self.file,
            "locked_at": self.locked_at,
            "locked_by": self.locked_by,
            "target_language": self.target_language,
            "source_version": self.source_version,
            "expected_completion": self.expected_completion,
            "status": self.status,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "VersionLock":
        return cls(**data)


class TranslationWorkflowManager:
    """Manages the translation workflow for the project."""
    
    def __init__(self):
        self.config = self._load_config()
        self.translation_queue = self._load_translation_queue()
        self.version_locks = self._load_version_locks()
        self.glossary = self._load_glossary()
    
    def _load_config(self) -> Dict:
        """Load i18n configuration."""
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default configuration."""
        return {
            "i18n": {
                "source_language": "zh",
                "target_languages": ["en"],
                "paths": {
                    "content_root": "docs/i18n/i18n-content",
                    "glossary_dir": "docs/i18n/glossary",
                    "workflow_dir": "docs/i18n/workflows",
                },
                "source_dirs": ["Struct", "Knowledge", "Flink"],
                "extraction": {
                    "skip_patterns": ["*.draft.md", "*.archived.md"],
                    "include_frontmatter": True,
                    "preserve_mermaid": True,
                },
                "quality": {
                    "term_check": True,
                    "format_check": True,
                    "link_check": True,
                    "min_completion_threshold": 95,
                },
            }
        }
    
    def _load_translation_queue(self) -> Dict[str, TranslationStatus]:
        """Load translation queue from file."""
        queue_file = WORKFLOW_DIR / "translation-queue.json"
        if queue_file.exists():
            with open(queue_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {k: TranslationStatus.from_dict(v) for k, v in data.items()}
        return {}
    
    def _save_translation_queue(self):
        """Save translation queue to file."""
        WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)
        queue_file = WORKFLOW_DIR / "translation-queue.json"
        data = {k: v.to_dict() for k, v in self.translation_queue.items()}
        with open(queue_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_version_locks(self) -> List[VersionLock]:
        """Load version locks from file."""
        locks_file = WORKFLOW_DIR / "version-lock.json"
        if locks_file.exists():
            with open(locks_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [VersionLock.from_dict(lock) for lock in data.get("locks", [])]
        return []
    
    def _save_version_locks(self):
        """Save version locks to file."""
        WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)
        locks_file = WORKFLOW_DIR / "version-lock.json"
        data = {"locks": [lock.to_dict() for lock in self.version_locks]}
        with open(locks_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_glossary(self) -> Dict:
        """Load glossary files."""
        glossary = {"core_terms": {}, "prohibited": [], "domain_terms": {}}
        
        core_terms_file = GLOSSARY_DIR / "core-terms.json"
        if core_terms_file.exists():
            with open(core_terms_file, "r", encoding="utf-8") as f:
                glossary["core_terms"] = json.load(f)
        
        prohibited_file = GLOSSARY_DIR / "prohibited-list.json"
        if prohibited_file.exists():
            with open(prohibited_file, "r", encoding="utf-8") as f:
                glossary["prohibited"] = json.load(f).get("prohibited_terms", {})
        
        return glossary
    
    def _compute_file_hash(self, filepath: Path) -> str:
        """Compute SHA256 hash of file content."""
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()[:16]
    
    def _get_source_files(self, source_dir: str) -> List[Path]:
        """Get all Markdown files in source directory."""
        source_path = PROJECT_ROOT / source_dir
        skip_patterns = self.config.get("i18n", {}).get("extraction", {}).get("skip_patterns", [])
        
        files = []
        if source_path.exists():
            for pattern in ["**/*.md"]:
                for file in source_path.glob(pattern):
                    # Check skip patterns
                    should_skip = any(file.match(p) for p in skip_patterns)
                    if not should_skip:
                        files.append(file)
        return sorted(files)
    
    def extract_for_translation(self, source: str, lang: str = "en") -> Dict:
        """Extract content for translation."""
        files = self._get_source_files(source)
        
        extraction_package = {
            "source": source,
            "target_language": lang,
            "extracted_at": datetime.now().isoformat(),
            "files": [],
        }
        
        for file in files:
            rel_path = file.relative_to(PROJECT_ROOT)
            content = file.read_text(encoding="utf-8")
            file_hash = self._compute_file_hash(file)
            
            # Check if already in queue
            queue_key = f"{lang}/{rel_path}"
            existing = self.translation_queue.get(queue_key)
            
            file_data = {
                "path": str(rel_path),
                "hash": file_hash,
                "size": len(content),
                "status": existing.translation_status if existing else "not_started",
            }
            
            extraction_package["files"].append(file_data)
        
        return extraction_package
    
    def lock_document(self, file_path: str, lang: str, translator: str, 
                     duration_days: int = 30) -> bool:
        """Lock a document for translation."""
        # Check if already locked
        existing_lock = next(
            (lock for lock in self.version_locks 
             if lock.file == file_path and lock.target_language == lang and lock.status == "active"),
            None
        )
        
        if existing_lock:
            print(f"Document {file_path} is already locked by {existing_lock.locked_by}")
            return False
        
        # Get source file hash
        source_file = PROJECT_ROOT / file_path
        if not source_file.exists():
            print(f"Source file {file_path} not found")
            return False
        
        file_hash = self._compute_file_hash(source_file)
        
        # Create lock
        now = datetime.now()
        lock = VersionLock(
            file=file_path,
            locked_at=now.isoformat(),
            locked_by=translator,
            target_language=lang,
            source_version=file_hash,
            expected_completion=(now + timedelta(days=duration_days)).isoformat(),
            status="active",
        )
        
        self.version_locks.append(lock)
        self._save_version_locks()
        
        # Update translation queue
        queue_key = f"{lang}/{file_path}"
        self.translation_queue[queue_key] = TranslationStatus(
            file=file_path,
            source_version=file_hash,
            translation_status="in_progress",
            translator=translator,
            target_language=lang,
            completion_percentage=0,
        )
        self._save_translation_queue()
        
        print(f"Locked {file_path} for translation to {lang} by {translator}")
        return True
    
    def release_lock(self, file_path: str, lang: str) -> bool:
        """Release a document lock."""
        lock = next(
            (lock for lock in self.version_locks 
             if lock.file == file_path and lock.target_language == lang and lock.status == "active"),
            None
        )
        
        if not lock:
            print(f"No active lock found for {file_path}")
            return False
        
        lock.status = "released"
        self._save_version_locks()
        
        print(f"Released lock on {file_path}")
        return True
    
    def check_missing_translations(self, lang: str = "en") -> List[Dict]:
        """Check for missing or outdated translations."""
        missing = []
        
        for source_dir in SOURCE_DIRS:
            source_files = self._get_source_files(source_dir)
            
            for source_file in source_files:
                rel_path = source_file.relative_to(PROJECT_ROOT)
                queue_key = f"{lang}/{rel_path}"
                
                # Check if translation exists
                target_file = CONTENT_ROOT / lang / rel_path
                source_hash = self._compute_file_hash(source_file)
                
                status = self.translation_queue.get(queue_key)
                
                if not target_file.exists():
                    missing.append({
                        "file": str(rel_path),
                        "status": "not_started",
                        "message": "Translation not started",
                    })
                elif status and status.source_version != source_hash:
                    missing.append({
                        "file": str(rel_path),
                        "status": "outdated",
                        "message": "Source document changed since translation",
                        "last_translated": status.translated_at,
                    })
                elif status and status.completion_percentage < 100:
                    missing.append({
                        "file": str(rel_path),
                        "status": "incomplete",
                        "message": f"Translation {status.completion_percentage}% complete",
                    })
        
        return missing
    
    def check_format_consistency(self, file_path: str) -> List[Dict]:
        """Check format consistency of a translation file."""
        issues = []
        
        filepath = CONTENT_ROOT / file_path
        if not filepath.exists():
            return [{"type": "error", "message": f"File {file_path} not found"}]
        
        content = filepath.read_text(encoding="utf-8")
        
        # Check for six sections
        required_sections = [
            "## 1. 概念定义",
            "## 1. Concept Definition",
            "## 2. 属性推导",
            "## 2. Property Derivation",
            "## 3. 关系建立",
            "## 3. Relationship Establishment",
            "## 4. 论证过程",
            "## 4. Argumentation Process",
            "## 5. 形式证明",
            "## 5. Formal Proof",
            "## 6. 实例验证",
            "## 6. Examples",
        ]
        
        # Check for Mermaid diagrams
        if "```mermaid" not in content:
            issues.append({
                "type": "warning",
                "message": "No Mermaid diagrams found",
                "suggestion": "Add at least one Mermaid diagram",
            })
        
        # Check for references
        if "## 8. 引用参考" not in content and "## 8. References" not in content:
            issues.append({
                "type": "warning",
                "message": "References section not found",
            })
        
        # Check terminology consistency (basic)
        for cn_term, en_term in self.glossary.get("core_terms", {}).items():
            if cn_term in content and en_term not in content:
                issues.append({
                    "type": "info",
                    "message": f"Consider using English term '{en_term}' for '{cn_term}'",
                })
        
        return issues
    
    def generate_stats(self) -> Dict:
        """Generate translation statistics."""
        stats = {
            "generated_at": datetime.now().isoformat(),
            "languages": {},
        }
        
        for lang in self.config.get("i18n", {}).get("target_languages", ["en"]):
            lang_stats = {
                "total_documents": 0,
                "translated": 0,
                "in_progress": 0,
                "not_started": 0,
                "completion_percentage": 0,
                "by_directory": {},
            }
            
            for source_dir in SOURCE_DIRS:
                source_files = self._get_source_files(source_dir)
                dir_total = len(source_files)
                dir_translated = 0
                dir_in_progress = 0
                
                for source_file in source_files:
                    rel_path = source_file.relative_to(PROJECT_ROOT)
                    queue_key = f"{lang}/{rel_path}"
                    status = self.translation_queue.get(queue_key)
                    
                    if status:
                        if status.translation_status == "completed":
                            dir_translated += 1
                        elif status.translation_status == "in_progress":
                            dir_in_progress += 1
                
                lang_stats["by_directory"][source_dir] = {
                    "total": dir_total,
                    "translated": dir_translated,
                    "in_progress": dir_in_progress,
                    "not_started": dir_total - dir_translated - dir_in_progress,
                    "percentage": round(dir_translated / dir_total * 100, 1) if dir_total > 0 else 0,
                }
                
                lang_stats["total_documents"] += dir_total
                lang_stats["translated"] += dir_translated
                lang_stats["in_progress"] += dir_in_progress
            
            lang_stats["not_started"] = lang_stats["total_documents"] - lang_stats["translated"] - lang_stats["in_progress"]
            lang_stats["completion_percentage"] = round(
                lang_stats["translated"] / lang_stats["total_documents"] * 100, 1
            ) if lang_stats["total_documents"] > 0 else 0
            
            stats["languages"][lang] = lang_stats
        
        return stats
    
    def print_stats(self):
        """Print translation statistics."""
        stats = self.generate_stats()
        
        print("=" * 60)
        print("Translation Progress Report")
        print("=" * 60)
        print(f"Generated at: {stats['generated_at']}")
        print()
        
        for lang, lang_stats in stats["languages"].items():
            print(f"Language: {lang}")
            print("-" * 40)
            print(f"  Total Documents: {lang_stats['total_documents']}")
            print(f"  Translated: {lang_stats['translated']} ({lang_stats['completion_percentage']}%)")
            print(f"  In Progress: {lang_stats['in_progress']}")
            print(f"  Not Started: {lang_stats['not_started']}")
            print()
            
            for dir_name, dir_stats in lang_stats["by_directory"].items():
                print(f"  {dir_name}/: {dir_stats['translated']}/{dir_stats['total']} ({dir_stats['percentage']}%)")
            
            print()
        
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Translation Workflow Manager for AnalysisDataFlow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Extract content for translation
    python translation-workflow.py extract --source Struct/ --lang en
    
    # Show translation statistics
    python translation-workflow.py stats
    
    # Check missing translations
    python translation-workflow.py check-missing --lang en
    
    # Check format consistency
    python translation-workflow.py check-format --file en/Struct/01.01-stream-processing.md
    
    # Lock a document for translation
    python translation-workflow.py lock --file Struct/01.01-stream-processing.md --lang en --translator user123
    
    # Release a lock
    python translation-workflow.py release --file Struct/01.01-stream-processing.md --lang en
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract content for translation")
    extract_parser.add_argument("--source", required=True, help="Source directory (e.g., Struct/)")
    extract_parser.add_argument("--lang", default="en", help="Target language (default: en)")
    extract_parser.add_argument("--output", help="Output file for extraction package")
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show translation statistics")
    
    # Check missing command
    missing_parser = subparsers.add_parser("check-missing", help="Check for missing translations")
    missing_parser.add_argument("--lang", default="en", help="Target language (default: en)")
    
    # Check format command
    format_parser = subparsers.add_parser("check-format", help="Check format consistency")
    format_parser.add_argument("--file", required=True, help="Translation file to check")
    
    # Lock command
    lock_parser = subparsers.add_parser("lock", help="Lock a document for translation")
    lock_parser.add_argument("--file", required=True, help="Source file to lock")
    lock_parser.add_argument("--lang", required=True, help="Target language")
    lock_parser.add_argument("--translator", required=True, help="Translator identifier")
    lock_parser.add_argument("--duration", type=int, default=30, help="Lock duration in days (default: 30)")
    
    # Release command
    release_parser = subparsers.add_parser("release", help="Release a document lock")
    release_parser.add_argument("--file", required=True, help="Source file to release")
    release_parser.add_argument("--lang", required=True, help="Target language")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = TranslationWorkflowManager()
    
    if args.command == "extract":
        package = manager.extract_for_translation(args.source, args.lang)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(package, f, indent=2, ensure_ascii=False)
            print(f"Extraction package saved to {args.output}")
        else:
            print(json.dumps(package, indent=2, ensure_ascii=False))
    
    elif args.command == "stats":
        manager.print_stats()
    
    elif args.command == "check-missing":
        missing = manager.check_missing_translations(args.lang)
        
        if missing:
            print(f"Missing translations in {args.lang}:")
            for item in missing:
                print(f"  - {item['file']}: {item['message']}")
        else:
            print(f"All documents are up to date in {args.lang}")
    
    elif args.command == "check-format":
        issues = manager.check_format_consistency(args.file)
        
        if issues:
            print(f"Format issues in {args.file}:")
            for issue in issues:
                print(f"  [{issue['type'].upper()}] {issue['message']}")
                if 'suggestion' in issue:
                    print(f"    Suggestion: {issue['suggestion']}")
        else:
            print(f"No format issues found in {args.file}")
    
    elif args.command == "lock":
        success = manager.lock_document(args.file, args.lang, args.translator, args.duration)
        sys.exit(0 if success else 1)
    
    elif args.command == "release":
        success = manager.release_lock(args.file, args.lang)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
