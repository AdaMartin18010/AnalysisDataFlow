#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目统计收集器 (Stats Collector)

功能:
    - 统计文档数量
    - 统计代码行数
    - 统计形式化元素(定理、定义、引理、命题、推论)
    - 统计代码示例
    - 统计Mermaid图表
    - 生成统计历史记录

作者: AnalysisDataFlow Project
版本: 1.0.0
"""

import os
import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class FileStats:
    """单个文件的统计信息"""
    path: str
    size_bytes: int
    lines: int
    words: int
    last_modified: str
    
    
@dataclass
class FormalElementStats:
    """形式化元素统计"""
    theorems: int = 0
    definitions: int = 0
    lemmas: int = 0
    propositions: int = 0
    corollaries: int = 0
    
    @property
    def total(self) -> int:
        return self.theorems + self.definitions + self.lemmas + self.propositions + self.corollaries


@dataclass
class DirectoryStats:
    """目录统计信息"""
    name: str
    path: str
    file_count: int = 0
    total_size: int = 0
    total_lines: int = 0
    formal_elements: FormalElementStats = None
    code_examples: int = 0
    mermaid_charts: int = 0
    
    def __post_init__(self):
        if self.formal_elements is None:
            self.formal_elements = FormalElementStats()


@dataclass
class ProjectStats:
    """项目整体统计"""
    timestamp: str
    version: str
    total_docs: int
    total_size_bytes: int
    total_lines: int
    directories: Dict[str, DirectoryStats]
    formal_elements: FormalElementStats
    code_examples: int
    mermaid_charts: int
    languages: Dict[str, int]  # 代码语言统计


class StatsCollector:
    """统计收集器主类"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化统计收集器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.root_dir = Path(self.config["project"]["root_dir"]).resolve()
        self.stats_dir = self.root_dir / ".stats"
        
        # 确保统计目录存在
        self.stats_dir.mkdir(exist_ok=True)
        
        # 编译正则表达式模式
        self._compile_patterns()
        
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"警告: 配置文件 {config_path} 不存在，使用默认配置")
            return self._default_config()
        except json.JSONDecodeError as e:
            print(f"错误: 配置文件格式错误: {e}")
            raise
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "project": {
                "root_dir": "../..",
                "directories": {
                    "struct": "Struct",
                    "knowledge": "Knowledge",
                    "flink": "Flink",
                    "visuals": "visuals"
                }
            },
            "statistics": {
                "formal_elements": {
                    "patterns": {
                        "theorem": ["Thm-", "**定理**"],
                        "definition": ["Def-", "**定义**"],
                        "lemma": ["Lemma-", "**引理**"],
                        "proposition": ["Prop-", "**命题**"],
                        "corollary": ["Cor-", "**推论**"]
                    }
                },
                "code_examples": {
                    "languages": ["java", "scala", "python", "go", "rust", "sql"],
                    "min_lines": 2
                },
                "mermaid_charts": {
                    "types": ["graph", "flowchart", "sequenceDiagram", "classDiagram"]
                }
            }
        }
    
    def _compile_patterns(self):
        """编译正则表达式模式以提高性能"""
        patterns_config = self.config["statistics"]["formal_elements"]["patterns"]
        
        # 形式化元素模式
        self.formal_patterns = {}
        for elem_type, patterns in patterns_config.items():
            # 创建匹配模式: 匹配 Thm-xxx 或 **定理**
            regex_parts = []
            for p in patterns:
                if p.endswith('-'):
                    # 编号模式，如 Thm-S-01-01
                    regex_parts.append(rf'{re.escape(p)}[A-Z]-\d+-\d+')
                else:
                    # 标题模式，如 **定理**
                    regex_parts.append(re.escape(p))
            self.formal_patterns[elem_type] = re.compile('|'.join(regex_parts), re.IGNORECASE)
        
        # 代码块模式
        code_langs = self.config["statistics"]["code_examples"]["languages"]
        lang_pattern = '|'.join(code_langs)
        self.code_block_pattern = re.compile(
            rf'```(?:{lang_pattern})\s*\n(.*?)```',
            re.DOTALL | re.IGNORECASE
        )
        
        # Mermaid图表模式
        mermaid_types = self.config["statistics"]["mermaid_charts"]["types"]
        self.mermaid_pattern = re.compile(
            r'```mermaid\s*\n(.*?)```',
            re.DOTALL | re.IGNORECASE
        )
        # Mermaid类型检测
        self.mermaid_type_patterns = [
            re.compile(rf'^\s*{t}\s', re.MULTILINE | re.IGNORECASE)
            for t in mermaid_types
        ]
        
    def collect_all(self) -> ProjectStats:
        """
        收集所有统计信息
        
        Returns:
            ProjectStats: 项目整体统计信息
        """
        print("🚀 开始收集项目统计信息...")
        
        directories = {}
        total_formal = FormalElementStats()
        total_code_examples = 0
        total_mermaid = 0
        total_docs = 0
        total_size = 0
        total_lines = 0
        languages = defaultdict(int)
        
        # 遍历配置的目录
        for dir_key, dir_name in self.config["project"]["directories"].items():
            dir_path = self.root_dir / dir_name
            if not dir_path.exists():
                print(f"⚠️  目录不存在: {dir_path}")
                continue
                
            print(f"📁 正在分析目录: {dir_name}")
            dir_stats = self._analyze_directory(dir_key, dir_path)
            directories[dir_key] = dir_stats
            
            # 累加总计
            total_docs += dir_stats.file_count
            total_size += dir_stats.total_size
            total_lines += dir_stats.total_lines
            
            # 累加形式化元素
            total_formal.theorems += dir_stats.formal_elements.theorems
            total_formal.definitions += dir_stats.formal_elements.definitions
            total_formal.lemmas += dir_stats.formal_elements.lemmas
            total_formal.propositions += dir_stats.formal_elements.propositions
            total_formal.corollaries += dir_stats.formal_elements.corollaries
            
            total_code_examples += dir_stats.code_examples
            total_mermaid += dir_stats.mermaid_charts
        
        stats = ProjectStats(
            timestamp=datetime.now().isoformat(),
            version=self.config.get("version", "1.0.0"),
            total_docs=total_docs,
            total_size_bytes=total_size,
            total_lines=total_lines,
            directories=directories,
            formal_elements=total_formal,
            code_examples=total_code_examples,
            mermaid_charts=total_mermaid,
            languages=dict(languages)
        )
        
        print("✅ 统计收集完成!")
        return stats
    
    def _analyze_directory(self, name: str, path: Path) -> DirectoryStats:
        """
        分析单个目录
        
        Args:
            name: 目录标识名
            path: 目录路径
            
        Returns:
            DirectoryStats: 目录统计信息
        """
        stats = DirectoryStats(name=name, path=str(path))
        
        # 遍历所有markdown文件
        for md_file in path.rglob("*.md"):
            # 跳过隐藏目录和node_modules等
            if any(part.startswith('.') or part in ['node_modules', '__pycache__'] 
                   for part in md_file.parts):
                continue
                
            file_stats = self._analyze_file(md_file)
            
            stats.file_count += 1
            stats.total_size += file_stats.size_bytes
            stats.total_lines += file_stats.lines
            
            # 分析文件内容
            content = md_file.read_text(encoding='utf-8')
            formal_stats = self._count_formal_elements(content)
            
            stats.formal_elements.theorems += formal_stats.theorems
            stats.formal_elements.definitions += formal_stats.definitions
            stats.formal_elements.lemmas += formal_stats.lemmas
            stats.formal_elements.propositions += formal_stats.propositions
            stats.formal_elements.corollaries += formal_stats.corollaries
            
            stats.code_examples += self._count_code_examples(content)
            stats.mermaid_charts += self._count_mermaid_charts(content)
        
        return stats
    
    def _analyze_file(self, file_path: Path) -> FileStats:
        """
        分析单个文件的基本信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            FileStats: 文件统计信息
        """
        stat = file_path.stat()
        content = file_path.read_text(encoding='utf-8')
        
        return FileStats(
            path=str(file_path.relative_to(self.root_dir)),
            size_bytes=stat.st_size,
            lines=len(content.splitlines()),
            words=len(content.split()),
            last_modified=datetime.fromtimestamp(stat.st_mtime).isoformat()
        )
    
    def _count_formal_elements(self, content: str) -> FormalElementStats:
        """
        统计形式化元素数量
        
        Args:
            content: 文档内容
            
        Returns:
            FormalElementStats: 形式化元素统计
        """
        stats = FormalElementStats()
        
        # 统计各类形式化元素
        stats.theorems = len(self.formal_patterns['theorem'].findall(content))
        stats.definitions = len(self.formal_patterns['definition'].findall(content))
        stats.lemmas = len(self.formal_patterns['lemma'].findall(content))
        stats.propositions = len(self.formal_patterns['proposition'].findall(content))
        stats.corollaries = len(self.formal_patterns['corollary'].findall(content))
        
        return stats
    
    def _count_code_examples(self, content: str) -> int:
        """
        统计代码示例数量
        
        Args:
            content: 文档内容
            
        Returns:
            int: 代码示例数量
        """
        min_lines = self.config["statistics"]["code_examples"]["min_lines"]
        matches = self.code_block_pattern.findall(content)
        
        count = 0
        for code in matches:
            lines = [l for l in code.split('\n') if l.strip()]
            if len(lines) >= min_lines:
                count += 1
        
        return count
    
    def _count_mermaid_charts(self, content: str) -> int:
        """
        统计Mermaid图表数量
        
        Args:
            content: 文档内容
            
        Returns:
            int: Mermaid图表数量
        """
        matches = self.mermaid_pattern.findall(content)
        return len(matches)
    
    def save_stats(self, stats: ProjectStats):
        """
        保存统计数据到文件
        
        Args:
            stats: 项目统计信息
        """
        # 保存当前统计
        stats_file = self.stats_dir / "project-stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self._stats_to_dict(stats), f, ensure_ascii=False, indent=2)
        
        # 更新历史记录
        self._update_history(stats)
        
        print(f"💾 统计数据已保存到: {stats_file}")
    
    def _stats_to_dict(self, stats: ProjectStats) -> Dict:
        """将统计对象转换为字典"""
        return {
            "timestamp": stats.timestamp,
            "version": stats.version,
            "summary": {
                "total_docs": stats.total_docs,
                "total_size_mb": round(stats.total_size_bytes / (1024 * 1024), 2),
                "total_lines": stats.total_lines,
                "formal_elements": {
                    "theorems": stats.formal_elements.theorems,
                    "definitions": stats.formal_elements.definitions,
                    "lemmas": stats.formal_elements.lemmas,
                    "propositions": stats.formal_elements.propositions,
                    "corollaries": stats.formal_elements.corollaries,
                    "total": stats.formal_elements.total
                },
                "code_examples": stats.code_examples,
                "mermaid_charts": stats.mermaid_charts
            },
            "directories": {
                name: {
                    "path": d.path,
                    "file_count": d.file_count,
                    "size_kb": round(d.total_size / 1024, 2),
                    "lines": d.total_lines,
                    "formal_elements": {
                        "theorems": d.formal_elements.theorems,
                        "definitions": d.formal_elements.definitions,
                        "lemmas": d.formal_elements.lemmas,
                        "propositions": d.formal_elements.propositions,
                        "corollaries": d.formal_elements.corollaries,
                        "total": d.formal_elements.total
                    },
                    "code_examples": d.code_examples,
                    "mermaid_charts": d.mermaid_charts
                }
                for name, d in stats.directories.items()
            }
        }
    
    def _update_history(self, stats: ProjectStats):
        """更新历史记录"""
        history_file = self.stats_dir / "stats-history.json"
        
        # 加载现有历史
        history = []
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        
        # 添加新记录
        history.append({
            "timestamp": stats.timestamp,
            "total_docs": stats.total_docs,
            "formal_elements": stats.formal_elements.total,
            "code_examples": stats.code_examples,
            "mermaid_charts": stats.mermaid_charts
        })
        
        # 限制历史记录数量（保留最近100条）
        if len(history) > 100:
            history = history[-100:]
        
        # 保存历史
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def load_stats(self) -> Optional[Dict]:
        """加载当前统计数据"""
        stats_file = self.stats_dir / "project-stats.json"
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def load_history(self) -> List[Dict]:
        """加载历史统计数据"""
        history_file = self.stats_dir / "stats-history.json"
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def print_summary(self, stats: ProjectStats):
        """打印统计摘要"""
        print("\n" + "=" * 60)
        print("📊 项目统计摘要")
        print("=" * 60)
        print(f"📅 统计时间: {stats.timestamp}")
        print(f"📝 总文档数: {stats.total_docs}")
        print(f"📦 总大小: {stats.total_size_bytes / (1024*1024):.2f} MB")
        print(f"📄 总行数: {stats.total_lines:,}")
        print()
        print("🔬 形式化元素:")
        print(f"   - 定理: {stats.formal_elements.theorems}")
        print(f"   - 定义: {stats.formal_elements.definitions}")
        print(f"   - 引理: {stats.formal_elements.lemmas}")
        print(f"   - 命题: {stats.formal_elements.propositions}")
        print(f"   - 推论: {stats.formal_elements.corollaries}")
        print(f"   - 总计: {stats.formal_elements.total}")
        print()
        print(f"💻 代码示例: {stats.code_examples}")
        print(f"📈 Mermaid图表: {stats.mermaid_charts}")
        print()
        print("📁 各目录统计:")
        for name, d in stats.directories.items():
            print(f"   {name:12} | 文档: {d.file_count:3} | "
                  f"大小: {d.total_size/1024:6.1f}KB | "
                  f"形式化: {d.formal_elements.total:4}")
        print("=" * 60)


def main():
    """主函数"""
    import sys
    
    # 确定配置文件路径
    script_dir = Path(__file__).parent
    config_path = script_dir / "config.json"
    
    # 创建收集器实例
    collector = StatsCollector(str(config_path))
    
    # 收集统计
    stats = collector.collect_all()
    
    # 保存统计
    collector.save_stats(stats)
    
    # 打印摘要
    collector.print_summary(stats)
    
    print("\n✅ 统计收集完成!")
    return 0


if __name__ == "__main__":
    exit(main())
