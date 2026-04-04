#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
README自动更新器 (README Updater)

功能:
    - 自动更新README.md中的统计数据
    - 更新徽章(Badges)
    - 更新进度条
    - 支持标记区域自动替换
    - 保持原有格式不变

作者: AnalysisDataFlow Project
版本: 1.0.0
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ReadmeUpdater:
    """README更新器"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化README更新器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.root_dir = Path(self.config["project"]["root_dir"]).resolve()
        self.stats_dir = self.root_dir / ".stats"
        self.readme_file = self.root_dir / "README.md"
        
    def _load_config(self, config_path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "project": {"root_dir": "../.."},
                "update_targets": {
                    "readme": {
                        "file": "README.md",
                        "markers": {
                            "stats_start": "<!-- STATS:START -->",
                            "stats_end": "<!-- STATS:END -->",
                            "progress_start": "<!-- PROGRESS:START -->",
                            "progress_end": "<!-- PROGRESS:END -->"
                        }
                    }
                }
            }
    
    def load_stats(self) -> Optional[Dict]:
        """加载统计数据"""
        stats_file = self.stats_dir / "project-stats.json"
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def update_readme(self) -> bool:
        """
        更新README文件
        
        Returns:
            bool: 是否成功更新
        """
        if not self.readme_file.exists():
            print(f"❌ README文件不存在: {self.readme_file}")
            return False
        
        stats = self.load_stats()
        if not stats:
            print("❌ 无法加载统计数据，请先运行 stats-collector.py")
            return False
        
        # 读取现有README
        content = self.readme_file.read_text(encoding='utf-8')
        original_content = content
        
        # 更新各个部分
        content = self._update_badges(content, stats)
        content = self._update_summary_table(content, stats)
        content = self._update_formal_elements_table(content, stats)
        content = self._update_content_stats(content, stats)
        content = self._update_progress_section(content, stats)
        content = self._update_timestamp(content)
        
        # 检查是否有变化
        if content == original_content:
            print("ℹ️ README内容无变化，无需更新")
            return True
        
        # 保存更新后的README
        self.readme_file.write_text(content, encoding='utf-8')
        print(f"✅ README已更新: {self.readme_file}")
        return True
    
    def _update_badges(self, content: str, stats: Dict) -> str:
        """
        更新徽章部分
        
        注意: 这里生成的是文本徽章，如果使用shields.io需要适配
        """
        summary = stats.get("summary", {})
        
        # 查找并更新文档数量徽章行
        # 格式: ![文档](...) 或 文档: xxx
        docs_count = summary.get("total_docs", 0)
        
        # 更新"总计"行中的统计
        patterns = [
            (r'总计[:\s]+\d+[^篇]*篇[^|]*技术文档', f'总计: {docs_count} 篇技术文档'),
            (r'总计[:\s]+\*\*\d+\*\*[^|]*篇[^|]*技术文档', f'总计: **{docs_count}** 篇技术文档'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def _update_summary_table(self, content: str, stats: Dict) -> str:
        """更新概览表格"""
        summary = stats.get("summary", {})
        dirs = stats.get("directories", {})
        
        # 更新四大核心目录表格
        # 查找表格并更新
        for dir_key, dir_data in dirs.items():
            dir_name = dir_key.capitalize()
            file_count = dir_data.get("file_count", 0)
            
            # 匹配形如: | **Struct/** | ... | 43文档, 92定理, 192定义 |
            pattern = rf'(\| \*?\*{dir_name}/\*?\*? \| [^|]+ \| [^|]+ \| )\d+[^|]*文档[^|]*\|'
            replacement = rf'\g<1>{file_count}文档 |'
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # 更新总计行
        total_docs = summary.get("total_docs", 0)
        formal = summary.get("formal_elements", {})
        total_formal = formal.get("total", 0)
        charts = summary.get("mermaid_charts", 0)
        code_examples = summary.get("code_examples", 0)
        size_mb = summary.get("total_size_mb", 0)
        
        # 更新总计行: **总计: xxx 篇技术文档 | xxx 形式化元素**
        total_patterns = [
            (r'\*\*总计[:\s]+\d+[^|]*篇[^|]*技术文档[^|]*\|[^|]*形式化元素[^|]*\*\*',
             f'**总计: {total_docs} 篇技术文档 | {total_formal:,} 形式化元素 | {charts}+ Mermaid图表 | {code_examples}+ 代码示例 | {size_mb} MB**'),
        ]
        
        for pattern, replacement in total_patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        return content
    
    def _update_formal_elements_table(self, content: str, stats: Dict) -> str:
        """更新形式化元素统计表"""
        formal = stats.get("summary", {}).get("formal_elements", {})
        
        # 形式化元素映射
        elements = {
            "定理": formal.get("theorems", 0),
            "定义": formal.get("definitions", 0),
            "引理": formal.get("lemmas", 0),
            "命题": formal.get("propositions", 0),
            "推论": formal.get("corollaries", 0),
            "总计": formal.get("total", 0),
        }
        
        # 更新表格中的数字
        for elem_name, count in elements.items():
            # 匹配 | 定理 (Thm) | 443 | 格式
            pattern = rf'(\| {elem_name}[^|]*\| )(\d{{1,4}}|\d,\d{{3}}|\*\*\d{{1,4}}\*\*|\*\*\d,\d{{3}}\*\*)( \|)'
            
            def replace_count(match):
                prefix = match.group(1)
                suffix = match.group(3)
                # 保留加粗格式
                if '**' in match.group(2):
                    return f"{prefix}**{count:,}**{suffix}"
                else:
                    return f"{prefix}{count:,}{suffix}"
            
            content = re.sub(pattern, replace_count, content, flags=re.IGNORECASE)
        
        return content
    
    def _update_content_stats(self, content: str, stats: Dict) -> str:
        """更新内容规模统计表"""
        summary = stats.get("summary", {})
        
        stats_mapping = {
            "技术文档": summary.get("total_docs", 0),
            "Mermaid图表": summary.get("mermaid_charts", 0),
            "代码示例": summary.get("code_examples", 0),
        }
        
        for stat_name, count in stats_mapping.items():
            # 匹配 | Mermaid图表 | 850+ | 格式
            pattern = rf'(\| {stat_name}[^|]*\| )(\d+\+?|\d{{1,4}}|\*\*\d+\*\*|\*\*\d{{1,4}}\+?\*\*)( \|)'
            
            def replace_count(match):
                prefix = match.group(1)
                suffix = match.group(3)
                original = match.group(2)
                # 保留加粗格式和+号
                has_bold = '**' in original
                has_plus = '+' in original
                value = f"{count:,}{'+' if has_plus else ''}"
                if has_bold:
                    value = f"**{value}**"
                return f"{prefix}{value}{suffix}"
            
            content = re.sub(pattern, replace_count, content, flags=re.IGNORECASE)
        
        return content
    
    def _update_progress_section(self, content: str, stats: Dict) -> str:
        """更新进度部分"""
        dirs = stats.get("directories", {})
        
        # 更新各目录进度行
        for dir_key, dir_data in dirs.items():
            dir_name = dir_key.capitalize()
            file_count = dir_data.get("file_count", 0)
            formal = dir_data.get("formal_elements", {})
            theorems = formal.get("theorems", 0)
            definitions = formal.get("definitions", 0)
            
            # 匹配进度行: | Struct/ | [████████] 100% | 43文档, 92定理, 192定义 |
            pattern = rf'(\| {dir_name}/ \| [^|]+ \| )\d+[^|]*文档[^,]*,[^|]*定理[^,]*,[^|]*定义[^|]*\|'
            
            def replace_progress(match):
                prefix = match.group(1)
                return f"{prefix}{file_count}文档, {theorems}定理, {definitions}定义 |"
            
            content = re.sub(pattern, replace_progress, content, flags=re.IGNORECASE)
        
        return content
    
    def _update_timestamp(self, content: str) -> str:
        """更新时间戳"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        # 更新最后更新时间
        patterns = [
            (r'最后更新[:\s]+\d{4}-\d{2}-\d{2}', f'最后更新: {timestamp}'),
            (r'最后更新 \([^)]+\)', f'最后更新 ({timestamp}'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def generate_badge_url(self, label: str, message: str, color: str = "blue") -> str:
        """
        生成shields.io徽章URL
        
        Args:
            label: 徽章标签
            message: 徽章消息
            color: 徽章颜色
            
        Returns:
            str: 徽章URL
        """
        import urllib.parse
        label_encoded = urllib.parse.quote(label)
        message_encoded = urllib.parse.quote(message)
        return f"https://img.shields.io/badge/{label_encoded}-{message_encoded}-{color}"
    
    def insert_badges_section(self, content: str, stats: Dict) -> str:
        """
        插入徽章部分（如果不存在）
        
        生成类似:
        ![文档](https://img.shields.io/badge/文档-422-blue)
        ![定理](https://img.shields.io/badge/定理-443-green)
        """
        summary = stats.get("summary", {})
        formal = summary.get("formal_elements", {})
        
        badges = [
            f"![文档]({self.generate_badge_url('文档', str(summary.get('total_docs', 0)), 'blue')})",
            f"![定理]({self.generate_badge_url('定理', str(formal.get('theorems', 0)), 'green')})",
            f"![定义]({self.generate_badge_url('定义', str(formal.get('definitions', 0)), 'orange')})",
            f"![进度]({self.generate_badge_url('进度', '100%', 'brightgreen')})",
        ]
        
        badge_section = "\n".join(badges)
        
        # 在标题后插入徽章
        title_pattern = r'(^(# .+\n))'
        if re.search(title_pattern, content, re.MULTILINE):
            content = re.sub(title_pattern, rf'\1\n{badge_section}\n', content, count=1)
        
        return content


def main():
    """主函数"""
    import sys
    
    script_dir = Path(__file__).parent
    config_path = script_dir / "config.json"
    
    updater = ReadmeUpdater(str(config_path))
    
    print("🚀 正在更新README.md...")
    
    if updater.update_readme():
        print("\n✅ README更新完成!")
        return 0
    else:
        print("\n❌ README更新失败!")
        return 1


if __name__ == "__main__":
    exit(main())
