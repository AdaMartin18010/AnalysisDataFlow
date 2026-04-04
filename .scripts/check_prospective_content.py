#!/usr/bin/env python3
"""
AnalysisDataFlow 前瞻性内容检测工具
====================================
功能：检测标记为"前瞻"的内容，对比官方发布状态，提醒更新正式文档

P1-8: CI/CD添加前瞻性内容检测

作者: AnalysisDataFlow CI/CD Team
版本: 1.0.0
"""

import re
import json
import asyncio
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict
import aiohttp


# =============================================================================
# 前瞻性内容定义
# =============================================================================

# 前瞻性内容标记
PROSPECTIVE_MARKERS = {
    # 中文标记
    '前瞻',
    '预览',
    '即将发布',
    '计划中',
    '路线图',
    '未来版本',
    '实验性',
    'beta',
    'alpha',
    'preview',
    'incubating',
    'upcoming',
    'planned',
    'roadmap',
}

# 版本跟踪关键字
VERSION_KEYWORDS = {
    'Flink 2.4',
    'Flink 2.5',
    'Flink 3.0',
    'Flink 1.20',
    'Flink 1.21',
    r'FLIP-\d+',  # FLIP提案
    r'FLINK-\d+',  # JIRA issue
}

# 需要跟踪的外部资源
TRACKED_RESOURCES = {
    'flink_releases': {
        'name': 'Apache Flink Releases',
        'url': 'https://archive.apache.org/dist/flink/',
        'check_url': 'https://api.github.com/repos/apache/flink/releases/latest',
        'current_version': '2.0',  # 需要手动更新
    },
    'flink_docs': {
        'name': 'Flink Documentation',
        'url': 'https://nightlies.apache.org/flink/flink-docs-stable/',
        'check_url': None,
        'current_version': '2.0',
    },
}


# =============================================================================
# 数据类
# =============================================================================

@dataclass
class ProspectiveItem:
    """前瞻性内容项"""
    content_type: str  # 'heading', 'paragraph', 'list_item', 'callout'
    content: str
    file_path: str
    line_start: int
    line_end: int
    markers_found: List[str]
    version_refs: List[str]
    confidence: float  # 0-1 置信度
    suggested_action: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class VersionStatus:
    """版本状态"""
    version: str
    status: str  # 'released', 'snapshot', 'planned', 'unknown'
    release_date: Optional[str]
    is_documentation_ready: bool
    source_url: Optional[str]


# =============================================================================
# 内容检测器
# =============================================================================

class ProspectiveContentDetector:
    """前瞻性内容检测器"""
    
    def __init__(self):
        self.items: List[ProspectiveItem] = []
        self.version_cache: Dict[str, VersionStatus] = {}
    
    def detect_in_file(self, file_path: Path) -> List[ProspectiveItem]:
        """在文件中检测前瞻性内容"""
        items = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            print(f"   ⚠️  无法读取 {file_path}: {e}")
            return items
        
        # 检测引用块/标注块中的前瞻内容
        items.extend(self._detect_callouts(lines, str(file_path)))
        
        # 检测标题中的前瞻标记
        items.extend(self._detect_headings(lines, str(file_path)))
        
        # 检测段落中的前瞻内容
        items.extend(self._detect_paragraphs(lines, str(file_path)))
        
        # 检测列表项中的前瞻内容
        items.extend(self._detect_list_items(lines, str(file_path)))
        
        return items
    
    def _find_markers(self, text: str) -> Tuple[List[str], List[str]]:
        """查找文本中的标记和版本引用"""
        text_lower = text.lower()
        
        markers_found = []
        for marker in PROSPECTIVE_MARKERS:
            if marker.lower() in text_lower:
                markers_found.append(marker)
        
        version_refs = []
        for keyword in VERSION_KEYWORDS:
            matches = re.findall(keyword, text, re.IGNORECASE)
            version_refs.extend(matches)
        
        return markers_found, version_refs
    
    def _calculate_confidence(
        self, 
        markers: List[str], 
        versions: List[str], 
        context: str
    ) -> float:
        """计算前瞻性内容的置信度"""
        confidence = 0.0
        
        # 标记权重
        if markers:
            confidence += min(len(markers) * 0.2, 0.6)
        
        # 版本引用权重
        if versions:
            confidence += min(len(versions) * 0.15, 0.4)
        
        # 上下文特征
        context_lower = context.lower()
        if any(word in context_lower for word in ['计划', '将', '会', '未来', 'next', 'coming']):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _detect_callouts(self, lines: List[str], file_path: str) -> List[ProspectiveItem]:
        """检测引用块/标注块"""
        items = []
        in_callout = False
        callout_start = 0
        callout_content = []
        callout_type = None
        
        for i, line in enumerate(lines, 1):
            # 检测标注块开始 (e.g., > ⚠️ **前瞻**, > **Note:**, > 🚧 等)
            callout_match = re.match(r'^\s*>\s*([⚠️🚧🔮✨📝🔔🔜🆕✅]+)?\s*[*\[]?([^:\n]+)[:\]]?\s*(.+)?', line)
            
            if callout_match:
                if not in_callout:
                    in_callout = True
                    callout_start = i
                    callout_content = [line]
                    callout_type = 'callout'
                else:
                    callout_content.append(line)
            elif in_callout and line.strip().startswith('>'):
                callout_content.append(line)
            else:
                if in_callout:
                    # 处理收集到的标注块
                    full_content = '\n'.join(callout_content)
                    markers, versions = self._find_markers(full_content)
                    
                    if markers or versions:
                        confidence = self._calculate_confidence(markers, versions, full_content)
                        items.append(ProspectiveItem(
                            content_type='callout',
                            content=full_content[:500],
                            file_path=file_path,
                            line_start=callout_start,
                            line_end=i - 1,
                            markers_found=markers,
                            version_refs=versions,
                            confidence=confidence,
                            suggested_action=self._suggest_action(markers, versions, confidence)
                        ))
                    
                    in_callout = False
                    callout_content = []
        
        return items
    
    def _detect_headings(self, lines: List[str], file_path: str) -> List[ProspectiveItem]:
        """检测标题"""
        items = []
        
        for i, line in enumerate(lines, 1):
            if line.startswith('#'):
                markers, versions = self._find_markers(line)
                
                if markers or versions:
                    confidence = self._calculate_confidence(markers, versions, line)
                    # 标题通常置信度更高
                    confidence = min(confidence + 0.1, 1.0)
                    
                    items.append(ProspectiveItem(
                        content_type='heading',
                        content=line.strip(),
                        file_path=file_path,
                        line_start=i,
                        line_end=i,
                        markers_found=markers,
                        version_refs=versions,
                        confidence=confidence,
                        suggested_action=self._suggest_action(markers, versions, confidence)
                    ))
        
        return items
    
    def _detect_paragraphs(self, lines: List[str], file_path: str) -> List[ProspectiveItem]:
        """检测段落"""
        items = []
        in_para = False
        para_start = 0
        para_lines = []
        
        for i, line in enumerate(lines, 1):
            is_empty = not line.strip()
            is_heading = line.startswith('#')
            is_code = line.strip().startswith('```')
            is_list = re.match(r'^\s*[-*+]\s', line)
            
            if is_empty or is_heading or is_code or is_list:
                if in_para and para_lines:
                    para_text = ' '.join(para_lines)
                    markers, versions = self._find_markers(para_text)
                    
                    if markers or versions:
                        confidence = self._calculate_confidence(markers, versions, para_text)
                        
                        items.append(ProspectiveItem(
                            content_type='paragraph',
                            content=para_text[:300],
                            file_path=file_path,
                            line_start=para_start,
                            line_end=i - 1,
                            markers_found=markers,
                            version_refs=versions,
                            confidence=confidence,
                            suggested_action=self._suggest_action(markers, versions, confidence)
                        ))
                    
                    in_para = False
                    para_lines = []
            else:
                if not in_para:
                    in_para = True
                    para_start = i
                para_lines.append(line.strip())
        
        return items
    
    def _detect_list_items(self, lines: List[str], file_path: str) -> List[ProspectiveItem]:
        """检测列表项"""
        items = []
        
        for i, line in enumerate(lines, 1):
            if re.match(r'^\s*[-*+]\s', line):
                markers, versions = self._find_markers(line)
                
                if markers or versions:
                    confidence = self._calculate_confidence(markers, versions, line)
                    
                    items.append(ProspectiveItem(
                        content_type='list_item',
                        content=line.strip(),
                        file_path=file_path,
                        line_start=i,
                        line_end=i,
                        markers_found=markers,
                        version_refs=versions,
                        confidence=confidence,
                        suggested_action=self._suggest_action(markers, versions, confidence)
                    ))
        
        return items
    
    def _suggest_action(
        self, 
        markers: List[str], 
        versions: List[str], 
        confidence: float
    ) -> str:
        """建议操作"""
        if confidence < 0.3:
            return "review"  # 需要人工审核
        
        if versions:
            version = versions[0]
            return f"track_version:{version}"
        
        if '实验性' in markers or 'beta' in markers or 'alpha' in markers:
            return "check_stability"
        
        if '前瞻' in markers or 'preview' in markers:
            return "check_release_status"
        
        if '路线图' in markers or 'roadmap' in markers:
            return "update_roadmap"
        
        return "review"


# =============================================================================
# 版本跟踪器
# =============================================================================

class VersionTracker:
    """版本跟踪器 - 检查Flink版本发布状态"""
    
    def __init__(self):
        self.cache: Dict[str, VersionStatus] = {}
    
    async def check_flink_releases(self) -> Dict[str, VersionStatus]:
        """检查Flink发布状态"""
        # 简化实现 - 实际应该调用GitHub API
        # 这里使用预定义的状态
        
        return {
            '2.0': VersionStatus(
                version='2.0',
                status='released',
                release_date='2025-03-20',
                is_documentation_ready=True,
                source_url='https://nightlies.apache.org/flink/flink-docs-release-2.0/'
            ),
            '2.1': VersionStatus(
                version='2.1',
                status='planned',
                release_date=None,
                is_documentation_ready=False,
                source_url='https://cwiki.apache.org/confluence/display/FLINK/2.1+Release'
            ),
            '2.4': VersionStatus(
                version='2.4',
                status='snapshot',
                release_date=None,
                is_documentation_ready=False,
                source_url='https://nightlies.apache.org/flink/flink-docs-master/'
            ),
            '2.5': VersionStatus(
                version='2.5',
                status='planned',
                release_date=None,
                is_documentation_ready=False,
                source_url=None
            ),
            '3.0': VersionStatus(
                version='3.0',
                status='planned',
                release_date=None,
                is_documentation_ready=False,
                source_url=None
            ),
        }
    
    def get_version_status(self, version: str) -> Optional[VersionStatus]:
        """获取版本状态"""
        # 从缓存或预定义数据获取
        return self.cache.get(version)


# =============================================================================
# 报告生成
# =============================================================================

def generate_prospective_report(
    items: List[ProspectiveItem],
    version_tracker: VersionTracker,
    output_path: Path,
    json_path: Optional[Path] = None
):
    """生成前瞻性内容检测报告"""
    
    # 按置信度分组
    high_confidence = [i for i in items if i.confidence >= 0.7]
    medium_confidence = [i for i in items if 0.4 <= i.confidence < 0.7]
    low_confidence = [i for i in items if i.confidence < 0.4]
    
    # 按操作类型分组
    by_action = defaultdict(list)
    for item in items:
        by_action[item.suggested_action].append(item)
    
    # 按文件分组
    by_file = defaultdict(list)
    for item in items:
        by_file[item.file_path].append(item)
    
    lines = [
        "# 🔮 前瞻性内容检测报告",
        "",
        f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> **检测项数**: {len(items)}",
        "",
        "## 📊 摘要统计",
        "",
        "### 置信度分布",
        "",
        f"| 置信度 | 数量 | 说明 |",
        f"|--------|------|------|",
        f"| 🔴 高 (≥0.7) | {len(high_confidence)} | 高可能性前瞻内容 |",
        f"| 🟡 中 (0.4-0.7) | {len(medium_confidence)} | 可能的前瞻内容 |",
        f"| 🟢 低 (<0.4) | {len(low_confidence)} | 需要审核 |",
        "",
        "### 操作类型分布",
        "",
    ]
    
    action_labels = {
        'track_version': '跟踪版本',
        'check_stability': '检查稳定性',
        'check_release_status': '检查发布状态',
        'update_roadmap': '更新路线图',
        'review': '人工审核'
    }
    
    for action, action_items in sorted(by_action.items()):
        label = action_labels.get(action, action)
        lines.append(f"- **{label}**: {len(action_items)} 项")
    
    lines.append("")
    
    # 高置信度项目详情
    if high_confidence:
        lines.extend([
            "## 🔴 高置信度前瞻内容（需优先处理）",
            "",
        ])
        
        for item in high_confidence:
            lines.extend([
                f"### {item.content[:80]}{'...' if len(item.content) > 80 else ''}",
                "",
                f"- **文件**: `{item.file_path}` (第{item.line_start}-{item.line_end}行)",
                f"- **类型**: {item.content_type}",
                f"- **置信度**: {item.confidence:.2f}",
                f"- **标记**: {', '.join(item.markers_found)}",
                f"- **版本引用**: {', '.join(item.version_refs) if item.version_refs else '无'}",
                f"- **建议操作**: {action_labels.get(item.suggested_action, item.suggested_action)}",
                "",
                "```",
                item.content[:200],
                "```",
                "",
            ])
    
    # 版本跟踪建议
    all_versions = set()
    for item in items:
        all_versions.update(item.version_refs)
    
    if all_versions:
        lines.extend([
            "## 📌 版本跟踪建议",
            "",
            "检测到的版本引用，请检查是否已正式发布：",
            "",
            "| 版本 | 预期状态 | 操作建议 |",
            "|------|----------|----------|",
        ])
        
        for version in sorted(all_versions):
            status = version_tracker.get_version_status(version)
            if status:
                if status.status == 'released':
                    lines.append(f"| {version} | ✅ 已发布 ({status.release_date}) | 更新为正式文档 |")
                elif status.status == 'snapshot':
                    lines.append(f"| {version} | 🔄 快照版 | 保持前瞻标记，持续跟踪 |")
                else:
                    lines.append(f"| {version} | ⏳ 计划中 | 保持前瞻标记 |")
            else:
                lines.append(f"| {version} | ❓ 未知 | 需要验证版本信息 |")
        
        lines.append("")
    
    # 按文件汇总
    if by_file:
        lines.extend([
            "## 📁 按文件汇总",
            "",
        ])
        
        for file_path, file_items in sorted(by_file.items()):
            high_count = sum(1 for i in file_items if i.confidence >= 0.7)
            
            lines.extend([
                f"### {file_path}",
                "",
                f"- 总项目: {len(file_items)}",
            ])
            
            if high_count:
                lines.append(f"- 🔴 高优先级: {high_count}")
            
            lines.append("")
            
            for item in file_items[:5]:  # 只显示前5个
                lines.append(f"- 第{item.line_start}行: `{item.content[:60]}{'...' if len(item.content) > 60 else ''}`")
            
            if len(file_items) > 5:
                lines.append(f"- ... 还有 {len(file_items) - 5} 项")
            
            lines.append("")
    
    # 维护指南
    lines.extend([
        "## 🔧 维护指南",
        "",
        "### 何时更新前瞻内容",
        "",
        "1. **版本发布后**:",
        "   - 移除前瞻/预览标记",
        "   - 更新为正式文档描述",
        "   - 更新API稳定性声明",
        "",
        "2. **功能稳定后**:",
        "   - 移除实验性标记",
        "   - 更新使用建议",
        "",
        "3. **路线图更新后**:",
        "   - 更新版本引用",
        "   - 添加新的前瞻内容",
        "",
        "### 自动化检查",
        "",
        "```bash",
        "# 手动运行前瞻性内容检测",
        "python .scripts/check_prospective_content.py",
        "",
        "# 检查特定版本",
        "python .scripts/check_prospective_content.py --focus-version 2.4",
        "```",
        "",
    ])
    
    # 写入报告
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    # 生成JSON
    if json_path:
        json_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'version': '1.0'
            },
            'summary': {
                'total_items': len(items),
                'high_confidence': len(high_confidence),
                'medium_confidence': len(medium_confidence),
                'low_confidence': len(low_confidence),
                'versions_referenced': sorted(list(all_versions))
            },
            'items': [item.to_dict() for item in items],
            'by_action': {
                action: [item.to_dict() for item in items]
                for action, items in by_action.items()
            }
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)


# =============================================================================
# 主程序
# =============================================================================

async def main():
    parser = argparse.ArgumentParser(
        description='AnalysisDataFlow 前瞻性内容检测工具'
    )
    parser.add_argument(
        '--path', '-p',
        default='.',
        help='要检查的根目录路径'
    )
    parser.add_argument(
        '--output', '-o',
        default='reports/prospective-content-report.md',
        help='报告输出路径'
    )
    parser.add_argument(
        '--json', '-j',
        default='reports/prospective-content-results.json',
        help='JSON结果输出路径'
    )
    parser.add_argument(
        '--focus-version',
        help='重点关注特定版本'
    )
    parser.add_argument(
        '--min-confidence',
        type=float,
        default=0.3,
        help='最小置信度阈值 (默认: 0.3)'
    )
    
    args = parser.parse_args()
    
    root_path = Path(args.path).resolve()
    output_path = Path(args.output)
    json_path = Path(args.json)
    
    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("AnalysisDataFlow 前瞻性内容检测工具")
    print("=" * 70)
    print(f"检查路径: {root_path}")
    print(f"输出报告: {output_path}")
    print(f"最小置信度: {args.min_confidence}")
    print("=" * 70)
    
    # 收集Markdown文件
    print("\n📁 扫描Markdown文件...")
    md_files = list(root_path.rglob('*.md'))
    md_files = [
        f for f in md_files 
        if not any(part.startswith('.') for part in f.parts)
    ]
    print(f"   找到 {len(md_files)} 个Markdown文件")
    
    # 检测前瞻性内容
    print("\n🔍 检测前瞻性内容...")
    detector = ProspectiveContentDetector()
    all_items = []
    
    for i, md_file in enumerate(md_files, 1):
        items = detector.detect_in_file(md_file)
        
        # 过滤
        items = [item for item in items if item.confidence >= args.min_confidence]
        
        # 如果指定了关注版本，进一步过滤
        if args.focus_version:
            items = [
                item for item in items 
                if any(args.focus_version in v for v in item.version_refs)
            ]
        
        all_items.extend(items)
        
        if i % 50 == 0 or i == len(md_files):
            print(f"   进度: {i}/{len(md_files)} 文件")
    
    # 去重（基于内容和文件）
    seen = set()
    unique_items = []
    for item in all_items:
        key = (item.file_path, item.content[:100])
        if key not in seen:
            seen.add(key)
            unique_items.append(item)
    all_items = unique_items
    
    print(f"\n📊 检测结果:")
    print(f"   总项目: {len(all_items)}")
    print(f"   高置信度 (≥0.7): {sum(1 for i in all_items if i.confidence >= 0.7)}")
    print(f"   中置信度 (0.4-0.7): {sum(1 for i in all_items if 0.4 <= i.confidence < 0.7)}")
    print(f"   低置信度 (<0.4): {sum(1 for i in all_items if i.confidence < 0.4)}")
    
    # 检查版本状态
    print("\n🌐 检查版本状态...")
    version_tracker = VersionTracker()
    version_tracker.cache = await version_tracker.check_flink_releases()
    print(f"   已加载 {len(version_tracker.cache)} 个版本状态")
    
    # 生成报告
    print("\n📝 生成报告...")
    generate_prospective_report(all_items, version_tracker, output_path, json_path)
    print(f"   Markdown报告: {output_path}")
    print(f"   JSON报告: {json_path}")
    
    print("\n" + "=" * 70)
    print("检测完成!")
    print("=" * 70)
    
    # 返回退出码
    high_count = sum(1 for i in all_items if i.confidence >= 0.7)
    
    if high_count > 0:
        print(f"⚠️  发现 {high_count} 个高置信度前瞻内容")
        return 1
    else:
        print("✅ 未发现高优先级前瞻内容")
        return 0


if __name__ == '__main__':
    exit(asyncio.run(main()))
