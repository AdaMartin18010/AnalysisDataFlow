#!/usr/bin/env python3
"""
同步追踪器 - 检测中文文档变更并同步翻译状态

功能:
1. 监控中文文档变更
2. 检测翻译过期状态
3. 生成翻译任务队列
4. 同步翻译状态

作者: AnalysisDataFlow i18n Team
版本: 4.0-prep
"""

import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


class SyncTracker:
    """翻译同步追踪器"""
    
    # 源语言目录配置
    SOURCE_DIRS = [
        "Struct",
        "Knowledge", 
        "Flink"
    ]
    
    # 状态文件路径
    STATE_FILE = "i18n/translation-workflow/state/translation-state.json"
    QUEUE_FILE = "i18n/translation-workflow/state/translation-queue.json"
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.state: Dict = {}
        self.changes: List[Dict] = []
        
    def load_state(self) -> Dict:
        """加载当前翻译状态"""
        state_path = self.project_root / self.STATE_FILE
        if state_path.exists():
            with open(state_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "version": "4.0-prep",
            "last_scan": None,
            "documents": {}
        }
    
    def save_state(self) -> None:
        """保存翻译状态"""
        state_path = self.project_root / self.STATE_FILE
        state_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.state["last_scan"] = datetime.now().isoformat()
        
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def compute_file_hash(self, file_path: Path) -> str:
        """计算文件哈希值"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()[:16]
    
    def scan_source_files(self) -> List[Path]:
        """扫描所有中文源文件"""
        source_files = []
        
        for source_dir in self.SOURCE_DIRS:
            dir_path = self.project_root / source_dir
            if not dir_path.exists():
                continue
                
            for md_file in dir_path.rglob("*.md"):
                # 排除归档和草稿文件
                if any(x in str(md_file) for x in ['.archived', '.draft', 'archive/']):
                    continue
                source_files.append(md_file)
        
        # 同时扫描根目录的关键文件
        root_files = ["README.md", "QUICK-START.md", "ARCHITECTURE.md"]
        for root_file in root_files:
            file_path = self.project_root / root_file
            if file_path.exists():
                source_files.append(file_path)
        
        return sorted(source_files)
    
    def get_translation_path(self, source_path: Path) -> Path:
        """获取对应的英文翻译文件路径"""
        relative_path = source_path.relative_to(self.project_root)
        return self.project_root / "i18n" / "en" / relative_path
    
    def detect_changes(self) -> List[Dict]:
        """检测文档变更"""
        self.state = self.load_state()
        changes = []
        
        source_files = self.scan_source_files()
        
        for source_file in source_files:
            relative_path = str(source_file.relative_to(self.project_root))
            current_hash = self.compute_file_hash(source_file)
            
            doc_state = self.state["documents"].get(relative_path, {})
            
            # 检查文件是否为新文件或已变更
            if not doc_state:
                change_type = "new"
            elif doc_state.get("hash") != current_hash:
                change_type = "modified"
            else:
                continue
            
            # 获取文件统计信息
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
                word_count = len(content)
                line_count = content.count('\n') + 1
            
            change_info = {
                "file": relative_path,
                "type": change_type,
                "old_hash": doc_state.get("hash"),
                "new_hash": current_hash,
                "detected_at": datetime.now().isoformat(),
                "word_count": word_count,
                "line_count": line_count,
                "translation_path": str(self.get_translation_path(source_file)),
                "translation_exists": self.get_translation_path(source_file).exists()
            }
            
            changes.append(change_info)
            
            # 更新状态
            self.state["documents"][relative_path] = {
                "hash": current_hash,
                "word_count": word_count,
                "line_count": line_count,
                "last_detected": datetime.now().isoformat(),
                "change_type": change_type
            }
        
        # 检测已删除的文件
        current_files = {str(f.relative_to(self.project_root)) for f in source_files}
        for tracked_file in list(self.state["documents"].keys()):
            if tracked_file not in current_files:
                changes.append({
                    "file": tracked_file,
                    "type": "deleted",
                    "detected_at": datetime.now().isoformat()
                })
                self.state["documents"][tracked_file]["status"] = "deleted"
        
        self.changes = changes
        return changes
    
    def determine_priority(self, file_path: str, word_count: int) -> str:
        """确定翻译优先级"""
        # P0: README和核心导航
        if file_path in ["README.md", "QUICK-START.md", "ARCHITECTURE.md"]:
            return "P0"
        
        # P0: Struct核心理论 (前15篇)
        if file_path.startswith("Struct/"):
            struct_index = ["01", "02", "03", "04", "05"]
            if any(file_path.startswith(f"Struct/{idx}") for idx in struct_index):
                return "P0"
            return "P2"
        
        # P1: Knowledge设计模式 (前20篇)
        if file_path.startswith("Knowledge/"):
            if file_path.startswith("Knowledge/02-design-patterns/"):
                return "P1"
            if file_path.startswith("Knowledge/01-concept-atlas/"):
                return "P1"
            return "P2"
        
        # P1: Flink快速入门
        if file_path.startswith("Flink/"):
            if any(file_path.startswith(f"Flink/{d}") for d in ["01-architecture", "02-core-mechanisms"]):
                return "P1"
            return "P2"
        
        return "P3"
    
    def generate_translation_queue(self) -> Dict:
        """生成翻译任务队列"""
        queue = {
            "version": "4.0-prep",
            "generated_at": datetime.now().isoformat(),
            "tasks": [],
            "statistics": {
                "total": 0,
                "by_priority": {"P0": 0, "P1": 0, "P2": 0, "P3": 0},
                "by_type": {"new": 0, "modified": 0, "deleted": 0}
            }
        }
        
        for change in self.changes:
            priority = self.determine_priority(
                change["file"], 
                change.get("word_count", 0)
            )
            
            task = {
                "id": f"TASK-{hash(change['file']) % 100000:05d}",
                "source_file": change["file"],
                "target_file": change["translation_path"],
                "change_type": change["type"],
                "priority": priority,
                "word_count": change.get("word_count", 0),
                "status": "pending",
                "created_at": change["detected_at"],
                "assigned_to": None,
                "estimated_hours": max(1, change.get("word_count", 0) // 500)
            }
            
            queue["tasks"].append(task)
            queue["statistics"]["total"] += 1
            queue["statistics"]["by_priority"][priority] += 1
            queue["statistics"]["by_type"][change["type"]] += 1
        
        # 按优先级排序
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
        queue["tasks"].sort(key=lambda x: priority_order.get(x["priority"], 4))
        
        return queue
    
    def save_queue(self, queue: Dict) -> None:
        """保存翻译队列"""
        queue_path = self.project_root / self.QUEUE_FILE
        queue_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(queue_path, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
    
    def generate_report(self) -> str:
        """生成同步报告"""
        report_lines = [
            "# 翻译同步追踪报告",
            "",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**版本**: v4.0-prep",
            "",
            "## 变更摘要",
            ""
        ]
        
        # 按类型统计
        type_counts = {"new": 0, "modified": 0, "deleted": 0}
        for change in self.changes:
            type_counts[change["type"]] += 1
        
        report_lines.extend([
            f"- 新增文件: {type_counts['new']}",
            f"- 修改文件: {type_counts['modified']}",
            f"- 删除文件: {type_counts['deleted']}",
            f"- **总计**: {len(self.changes)}",
            "",
            "## 详细变更列表",
            ""
        ])
        
        # 按优先级分组
        priority_groups = {"P0": [], "P1": [], "P2": [], "P3": []}
        for change in self.changes:
            priority = self.determine_priority(
                change["file"],
                change.get("word_count", 0)
            )
            priority_groups[priority].append(change)
        
        for priority in ["P0", "P1", "P2", "P3"]:
            if priority_groups[priority]:
                report_lines.extend([
                    f"### {priority} 优先级",
                    "",
                    "| 文件 | 类型 | 字数 | 翻译状态 |",
                    "|------|------|------|----------|"
                ])
                
                for change in priority_groups[priority]:
                    trans_status = "✅ 已翻译" if change.get("translation_exists") else "❌ 未翻译"
                    report_lines.append(
                        f"| {change['file']} | {change['type']} | {change.get('word_count', '-')} | {trans_status} |"
                    )
                
                report_lines.append("")
        
        report_lines.extend([
            "## 下一步行动",
            "",
            "1. 查看 `i18n/translation-workflow/state/translation-queue.json` 获取任务队列",
            "2. 优先处理 P0 优先级任务",
            "3. 使用 `auto-translate.py` 进行AI预翻译",
            "4. 使用 `quality-checker.py` 验证翻译质量",
            ""
        ])
        
        return '\n'.join(report_lines)
    
    def run(self) -> None:
        """运行同步追踪"""
        print("🔍 开始扫描中文源文件...")
        
        changes = self.detect_changes()
        print(f"📊 检测到 {len(changes)} 个文件变更")
        
        # 保存状态
        self.save_state()
        print(f"💾 状态已保存到 {self.STATE_FILE}")
        
        # 生成队列
        if changes:
            queue = self.generate_translation_queue()
            self.save_queue(queue)
            print(f"📝 翻译队列已生成 ({queue['statistics']['total']} 个任务)")
            
            # 打印摘要
            print("\n📈 优先级分布:")
            for p, count in queue["statistics"]["by_priority"].items():
                if count > 0:
                    print(f"   {p}: {count} 个任务")
        
        # 生成报告
        report = self.generate_report()
        report_path = self.project_root / "i18n/translation-workflow/reports/sync-report.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 报告已保存: {report_path}")
        print("\n✅ 同步追踪完成!")


def main():
    """主入口"""
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    
    tracker = SyncTracker(project_root)
    tracker.run()


if __name__ == "__main__":
    main()
