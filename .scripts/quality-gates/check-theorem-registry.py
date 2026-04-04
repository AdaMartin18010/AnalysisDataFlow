#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定理注册表检查脚本

功能：
1. 扫描所有形式化元素（定理、定义、引理、命题、推论）
2. 检查编号唯一性、格式正确性
3. 与THEOREM-REGISTRY.md同步检查
4. 输出详细报告和修复建议
5. 生成注册表更新补丁

用法：
    python check-theorem-registry.py [--fix] [--output REPORT.md]

作者: Agent
版本: 1.2.0
"""

import os
import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
from datetime import datetime

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 扫描的目录
SCAN_DIRS = ['Struct', 'Knowledge', 'Flink']

# 形式化元素类型
ELEMENT_TYPES = {
    'Thm': '定理',
    'Def': '定义',
    'Lemma': '引理',
    'Prop': '命题',
    'Cor': '推论'
}

# 阶段标识映射
STAGE_MAP = {
    'S': 'Struct',
    'K': 'Knowledge',
    'F': 'Flink'
}

# 编号正则表达式
ID_PATTERN = re.compile(
    r'\b(Thm|Def|Lemma|Prop|Cor)-([SFK])-(\d{2})-(\d{2})(?:-(\d{2,3}))?\b'
)

# 注册表中的条目正则
REGISTRY_PATTERN = re.compile(
    r'\|\s*(Thm|Def|Lemma|Prop|Cor)-([SFK])-(\d{2}(?:-\d{2})?(?:-\d{2,3})?)\s*\|'
)

# 定义上下文模式
DEFINITION_PATTERNS = [
    re.compile(r'^#{1,4}\s*.*?(Thm|Def|Lemma|Prop|Cor)-'),
    re.compile(r'^\*\*.*?定义.*?\d+\.\d+.*'),
    re.compile(r'^\*\*.*?定理.*?\d+\.\d+.*'),
    re.compile(r'####\s+(Thm|Def|Lemma|Prop|Cor)-'),
    re.compile(r'\*\*(Thm|Def|Lemma|Prop|Cor)-[^*]+\*\s*[:：]'),
]

# 引用模式
REFERENCE_PATTERNS = [
    re.compile(r'见.*?(Thm|Def|Lemma|Prop|Cor)-'),
    re.compile(r'详见.*?(Thm|Def|Lemma|Prop|Cor)-'),
    re.compile(r'引用.*?(Thm|Def|Lemma|Prop|Cor)-'),
    re.compile(r'依赖.*?(Thm|Def|Lemma|Prop|Cor)-'),
    re.compile(r'由.*?(Thm|Def|Lemma|Prop|Cor)-'),
    re.compile(r'根据.*?(Thm|Def|Lemma|Prop|Cor)-'),
    re.compile(r'参见.*?(Thm|Def|Lemma|Prop|Cor)-'),
]


@dataclass
class FormalElement:
    """形式化元素"""
    elem_type: str
    stage: str
    doc_num: str
    seq: str
    full_id: str
    file_path: str
    line_num: int
    line_content: str
    context: str = ""
    is_definition: bool = False


@dataclass
class CheckResult:
    """检查结果"""
    errors: List[Dict] = field(default_factory=list)
    warnings: List[Dict] = field(default_factory=list)
    stats: Dict = field(default_factory=dict)


class TheoremRegistryChecker:
    """定理注册表检查器"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.registry_path = project_root / 'THEOREM-REGISTRY.md'
        self.elements: List[FormalElement] = []
        self.definitions: List[FormalElement] = []
        self.registry_entries: Set[str] = set()
        self.elements_by_id: Dict[str, List[FormalElement]] = defaultdict(list)
        self.definitions_by_id: Dict[str, List[FormalElement]] = defaultdict(list)
        self.result = CheckResult()

    def run(self) -> CheckResult:
        """运行所有检查"""
        print("🔍 开始检查定理注册表...")
        print("=" * 60)

        self._scan_all_files()
        self._load_registry()
        self._check_uniqueness()
        self._check_format()
        self._check_registry_sync()
        self._check_numbering_continuity()
        self._check_stage_consistency()
        self._generate_stats()

        return self.result

    def _is_definition(self, line: str, lines: List[str], line_idx: int) -> bool:
        """判断当前行是否是定义（而非引用）"""
        for pattern in DEFINITION_PATTERNS:
            if pattern.search(line):
                return True

        # 检查是否是目录项
        if line.strip().startswith('- [') or line.strip().startswith('* ['):
            return False

        # 检查是否是引用模式
        for pattern in REFERENCE_PATTERNS:
            if pattern.search(line):
                return False

        # 检查周围上下文
        in_math = False
        for i in range(max(0, line_idx - 3), min(len(lines), line_idx + 1)):
            if '$$' in lines[i] or (lines[i].count('$') % 2 == 1):
                in_math = not in_math

        if in_math:
            if re.search(r'\\text\{.*?(Thm|Def|Lemma|Prop|Cor)-', line):
                return True

        if line.strip().startswith('#'):
            return True

        if re.search(r'^\s*[-*]\s*\*\*(Thm|Def|Lemma|Prop|Cor)-[^*]+\*\*', line):
            return True

        for i in range(max(0, line_idx - 5), line_idx):
            if any(kw in lines[i] for kw in ['**定义', '**定理', '**引理', '**命题', '**推论',
                                              '#### 定义', '#### 定理', '#### 引理', '#### 命题', '#### 推论']):
                return True

        return False

    def _scan_all_files(self):
        """扫描所有Markdown文件"""
        print("\n📁 扫描文档文件...")

        for dir_name in SCAN_DIRS:
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                continue

            for md_file in dir_path.rglob('*.md'):
                if '00-INDEX' in md_file.name or 'README' in md_file.name:
                    continue
                self._scan_file(md_file)

        for elem in self.elements:
            self.elements_by_id[elem.full_id].append(elem)
            if elem.is_definition:
                self.definitions_by_id[elem.full_id].append(elem)

        print(f"   找到 {len(self.elements)} 个形式化元素")
        print(f"   其中 {len(self.definitions)} 个是定义（非引用）")

    def _scan_file(self, file_path: Path):
        """扫描单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                for match in ID_PATTERN.finditer(line):
                    elem_type, stage, doc, seq, subseq = match.groups()

                    if subseq:
                        full_id = f"{elem_type}-{stage}-{doc}-{seq}-{subseq}"
                        doc_num = f"{doc}-{seq}"
                        seq_str = subseq
                    else:
                        full_id = f"{elem_type}-{stage}-{doc}-{seq}"
                        doc_num = doc
                        seq_str = seq

                    is_def = self._is_definition(line, lines, line_num - 1)
                    context = self._extract_context(lines, line_num - 1)

                    elem = FormalElement(
                        elem_type=elem_type,
                        stage=stage,
                        doc_num=doc_num,
                        seq=seq_str,
                        full_id=full_id,
                        file_path=str(file_path.relative_to(self.project_root)),
                        line_num=line_num,
                        line_content=line.strip(),
                        context=context,
                        is_definition=is_def
                    )
                    self.elements.append(elem)
                    if is_def:
                        self.definitions.append(elem)

        except Exception as e:
            self.result.errors.append({
                'type': 'file_read_error',
                'file': str(file_path),
                'message': str(e)
            })

    def _extract_context(self, lines: List[str], line_idx: int) -> str:
        """提取上下文（标题）"""
        for i in range(line_idx, max(-1, line_idx - 10), -1):
            line = lines[i]
            if line.startswith('#'):
                return line.strip('# \n')
            if '**' in line and any(kw in line for kw in ['定义', '定理', '引理', '命题', '推论']):
                return line.strip('* \n')
        return ""

    def _load_registry(self):
        """加载注册表"""
        print("\n📖 加载注册表...")

        if not self.registry_path.exists():
            self.result.errors.append({
                'type': 'registry_missing',
                'message': f'注册表文件不存在: {self.registry_path}'
            })
            return

        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                content = f.read()

            for match in REGISTRY_PATTERN.finditer(content):
                elem_type, stage, num = match.groups()
                full_id = f"{elem_type}-{stage}-{num}"
                self.registry_entries.add(full_id)

            print(f"   注册表中共有 {len(self.registry_entries)} 个条目")

        except Exception as e:
            self.result.errors.append({
                'type': 'registry_read_error',
                'message': str(e)
            })

    def _check_uniqueness(self):
        """检查定义的唯一性"""
        print("\n🔍 检查编号唯一性...")

        duplicates = {k: v for k, v in self.definitions_by_id.items() if len(v) > 1}

        for full_id, elems in duplicates.items():
            files = set(e.file_path for e in elems)
            if len(files) == 1:
                self.result.warnings.append({
                    'type': 'duplicate_definition_same_file',
                    'id': full_id,
                    'count': len(elems),
                    'file': list(files)[0],
                    'locations': [f"{e.file_path}:{e.line_num}" for e in elems],
                    'message': f'编号 {full_id} 在同一文件中定义了 {len(elems)} 次'
                })
            else:
                locations = [f"{e.file_path}:{e.line_num}" for e in elems]
                self.result.errors.append({
                    'type': 'duplicate_id',
                    'id': full_id,
                    'count': len(elems),
                    'locations': locations,
                    'message': f'编号 {full_id} 在多个文件中重复定义 ({len(files)} 个文件)'
                })

        if duplicates:
            total_dups = len([e for elems in duplicates.values() for e in elems])
            print(f"   ⚠️ 发现 {len(duplicates)} 个重复定义 ({total_dups} 个实例)")
        else:
            print("   ✅ 所有定义编号唯一")

    def _check_format(self):
        """检查编号格式"""
        print("\n🔍 检查编号格式...")

        format_errors = []

        for elem in self.definitions:
            expected_stage = self._get_stage_from_path(elem.file_path)
            if expected_stage and elem.stage != expected_stage:
                format_errors.append({
                    'type': 'stage_mismatch',
                    'id': elem.full_id,
                    'file': elem.file_path,
                    'expected_stage': expected_stage,
                    'actual_stage': elem.stage,
                    'message': f'编号阶段标识 {elem.stage} 与文件路径不匹配 (期望 {expected_stage})'
                })

            try:
                seq_int = int(elem.seq)
                if seq_int < 1 or seq_int > 999:
                    format_errors.append({
                        'type': 'invalid_seq',
                        'id': elem.full_id,
                        'message': f'顺序号超出范围: {elem.seq}'
                    })
            except ValueError:
                format_errors.append({
                    'type': 'invalid_seq_format',
                    'id': elem.full_id,
                    'message': f'顺序号格式错误: {elem.seq}'
                })

        for err in format_errors:
            self.result.errors.append(err)

        if format_errors:
            print(f"   ⚠️ 发现 {len(format_errors)} 个格式问题")
        else:
            print("   ✅ 编号格式正确")

    def _get_stage_from_path(self, file_path: str) -> Optional[str]:
        """从文件路径推断阶段标识"""
        if file_path.startswith('Struct/'):
            return 'S'
        elif file_path.startswith('Knowledge/'):
            return 'K'
        elif file_path.startswith('Flink/'):
            return 'F'
        return None

    def _check_registry_sync(self):
        """检查注册表同步"""
        print("\n🔍 检查注册表同步...")

        def_ids = set(e.full_id for e in self.definitions)
        unregistered = def_ids - self.registry_entries
        orphaned = self.registry_entries - def_ids

        for uid in sorted(unregistered):
            elems = self.definitions_by_id.get(uid, [])
            if elems:
                locations = [f"{e.file_path}:{e.line_num}" for e in elems]
                # 检查是否是重复定义导致的未注册
                if uid in self.definitions_by_id and len(self.definitions_by_id[uid]) > 1:
                    self.result.warnings.append({
                        'type': 'unregistered_duplicate',
                        'id': uid,
                        'locations': locations,
                        'message': f'编号 {uid} 未在注册表中登记（可能是重复定义导致的）'
                    })
                else:
                    self.result.errors.append({
                        'type': 'unregistered',
                        'id': uid,
                        'locations': locations,
                        'message': f'编号 {uid} 未在注册表中登记'
                    })

        for oid in sorted(orphaned):
            self.result.warnings.append({
                'type': 'orphaned_registry_entry',
                'id': oid,
                'message': f'注册表条目 {oid} 在文档中未找到（可能已被删除）'
            })

        if unregistered:
            true_errors = len([uid for uid in unregistered if uid in self.definitions_by_id and len(self.definitions_by_id[uid]) == 1])
            print(f"   ⚠️ 发现 {len(unregistered)} 个未注册的编号（其中 {true_errors} 个是真正的错误）")
        else:
            print("   ✅ 所有定义已注册")

        if orphaned:
            print(f"   ⚠️ 发现 {len(orphaned)} 个孤儿注册表条目")

    def _check_numbering_continuity(self):
        """检查编号连续性"""
        print("\n🔍 检查编号连续性...")

        groups = defaultdict(list)
        for elem in self.definitions:
            key = (elem.elem_type, elem.stage, elem.doc_num.split('-')[0])
            groups[key].append(int(elem.seq))

        gaps = []
        for (elem_type, stage, doc), seqs in groups.items():
            seqs = sorted(set(seqs))
            if len(seqs) < 2:
                continue

            for i in range(1, len(seqs)):
                if seqs[i] - seqs[i-1] > 1:
                    gaps.append({
                        'type': 'numbering_gap',
                        'elem_type': elem_type,
                        'stage': stage,
                        'doc': doc,
                        'from': seqs[i-1],
                        'to': seqs[i],
                        'message': f'{elem_type}-{stage}-{doc}: 编号从 {seqs[i-1]:02d} 跳到 {seqs[i]:02d}'
                    })

        for gap in gaps:
            self.result.warnings.append(gap)

        if gaps:
            print(f"   ⚠️ 发现 {len(gaps)} 个编号不连续")
        else:
            print("   ✅ 编号连续")

    def _check_stage_consistency(self):
        """检查阶段标识一致性"""
        print("\n🔍 检查阶段标识一致性...")

        inconsistencies = []

        for elem in self.definitions:
            expected = self._get_stage_from_path(elem.file_path)
            if expected and elem.stage != expected:
                inconsistencies.append({
                    'type': 'stage_inconsistency',
                    'id': elem.full_id,
                    'file': elem.file_path,
                    'expected': expected,
                    'actual': elem.stage
                })

        for inc in inconsistencies:
            self.result.errors.append(inc)

        if inconsistencies:
            print(f"   ⚠️ 发现 {len(inconsistencies)} 个阶段标识不一致")
        else:
            print("   ✅ 阶段标识一致")

    def _generate_stats(self):
        """生成统计信息"""
        print("\n📊 生成统计信息...")

        stats = {
            'total_elements': len(self.elements),
            'total_definitions': len(self.definitions),
            'by_type': defaultdict(int),
            'by_stage': defaultdict(int),
            'by_directory': defaultdict(int),
            'error_count': len(self.result.errors),
            'warning_count': len(self.result.warnings)
        }

        for elem in self.definitions:
            stats['by_type'][elem.elem_type] += 1
            stats['by_stage'][elem.stage] += 1
            dir_name = elem.file_path.split('/')[0]
            stats['by_directory'][dir_name] += 1

        self.result.stats = dict(stats)

        print(f"\n{'='*60}")
        print("📈 统计摘要")
        print(f"{'='*60}")
        print(f"总形式化元素: {stats['total_elements']}")
        print(f"其中定义（非引用）: {stats['total_definitions']}")
        print(f"按类型:")
        for t, c in sorted(stats['by_type'].items()):
            print(f"  - {ELEMENT_TYPES.get(t, t)}: {c}")
        print(f"按阶段:")
        for s, c in sorted(stats['by_stage'].items()):
            print(f"  - {STAGE_MAP.get(s, s)}: {c}")
        print(f"\n❌ 错误: {stats['error_count']}")
        print(f"⚠️  警告: {stats['warning_count']}")

    def generate_patch(self, output_path: Optional[Path] = None) -> str:
        """生成注册表更新补丁"""
        # 找到未注册的条目
        def_ids = set(e.full_id for e in self.definitions)
        unregistered = def_ids - self.registry_entries

        if not unregistered:
            return "# 无更新补丁需要生成\n\n所有定义已在注册表中登记。\n"

        patch = """# 定理注册表更新补丁

> **生成时间**: {timestamp}

以下是需要添加到 THEOREM-REGISTRY.md 的条目：

""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # 按类型分组
        by_type = defaultdict(list)
        for uid in sorted(unregistered):
            elems = self.definitions_by_id.get(uid, [])
            if elems:
                elem = elems[0]  # 取第一个定义
                by_type[elem.elem_type].append(elem)

        for elem_type in ['Thm', 'Def', 'Lemma', 'Prop', 'Cor']:
            if elem_type not in by_type:
                continue

            patch += f"## {ELEMENT_TYPES.get(elem_type, elem_type)}\n\n"
            patch += "| 编号 | 名称 | 位置 | 形式化等级 | 状态 |\n"
            patch += "|------|------|------|-----------|------|\n"

            for elem in by_type[elem_type]:
                context = elem.context[:30] + '...' if len(elem.context) > 30 else elem.context
                location = elem.file_path.split('/')[0] + '/' + elem.file_path.split('/')[1] if '/' in elem.file_path else elem.file_path
                patch += f"| {elem.full_id} | {context} | {location} | L4 | ⏳ |\n"

            patch += "\n"

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(patch)
            print(f"\n📝 补丁已保存: {output_path}")

        return patch

    def generate_report(self, output_path: Optional[Path] = None) -> str:
        """生成详细报告"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        report = f"""# 定理注册表检查报告

> **生成时间**: {timestamp}
> **检查版本**: v1.2.0
> **项目根目录**: {self.project_root}

---

## 执行摘要

| 指标 | 数值 |
|------|------|
| 总形式化元素（含引用） | {self.result.stats.get('total_elements', 0)} |
| 定义（非引用） | {self.result.stats.get('total_definitions', 0)} |
| 错误数 | {len(self.result.errors)} |
| 警告数 | {len(self.result.warnings)} |
| 注册表条目 | {len(self.registry_entries)} |

### 按类型统计（仅定义）

| 类型 | 数量 | 说明 |
|------|------|------|
"""

        for t, c in sorted(self.result.stats.get('by_type', {}).items()):
            report += f"| {t} | {c} | {ELEMENT_TYPES.get(t, t)} |\n"

        report += f"""
### 按阶段统计（仅定义）

| 阶段 | 数量 | 说明 |
|------|------|------|
"""

        for s, c in sorted(self.result.stats.get('by_stage', {}).items()):
            report += f"| {s} | {c} | {STAGE_MAP.get(s, s)} |\n"

        # 错误详情
        if self.result.errors:
            report += f"""
---

## ❌ 错误详情 ({len(self.result.errors)})

"""
            for i, err in enumerate(self.result.errors, 1):
                report += f"""### {i}. {err.get('type', 'Unknown')}

- **编号**: `{err.get('id', 'N/A')}`
- **文件**: {err.get('file', 'N/A')}
- **消息**: {err.get('message', 'N/A')}
"""
                if 'locations' in err:
                    report += "- **位置**:\n"
                    for loc in err['locations'][:10]:
                        report += f"  - `{loc}`\n"
                    if len(err['locations']) > 10:
                        report += f"  - ... 还有 {len(err['locations']) - 10} 个\n"
                report += "\n"

        # 警告详情（简要）
        if self.result.warnings:
            report += f"""
---

## ⚠️ 警告摘要 ({len(self.result.warnings)})

| # | 类型 | 编号 | 消息 |
|---|------|------|------|
"""
            for i, warn in enumerate(self.result.warnings[:50], 1):
                wid = warn.get('id', 'N/A')
                msg = warn.get('message', 'N/A')[:50]
                report += f"| {i} | {warn.get('type', 'Unknown')} | `{wid}` | {msg}... |\n"

            if len(self.result.warnings) > 50:
                report += f"\n... 还有 {len(self.result.warnings) - 50} 个警告\n"

        # 修复建议
        report += f"""
---

## 🔧 修复建议

"""

        if self.result.errors:
            report += """### 高优先级

1. **解决重复编号**: 为在不同文件中重复定义的编号分配新的唯一编号
   - 建议：保留原始文档中的定义，将其他文档中的改为引用
   
2. **注册未登记的编号**: 将文档中发现的未注册编号添加到 THEOREM-REGISTRY.md
   - 可以使用 `--patch` 选项生成补丁文件
   
3. **修正阶段标识**: 确保编号中的阶段标识与文件路径匹配

"""

        if self.result.warnings:
            report += """### 中优先级

1. **清理孤儿条目**: 从注册表中移除已不存在的条目
2. **填补编号空缺**: 考虑重新编号以消除空缺（可选）
3. **合并同一文件中的重复定义**: 检查同一文件中多次出现的定义

"""

        report += """### 使用脚本生成补丁

```bash
# 生成注册表更新补丁
python .scripts/quality-gates/check-theorem-registry.py --patch patch.md

# 生成完整报告
python .scripts/quality-gates/check-theorem-registry.py --output report.md
```

---

## 附录 A: 所有检测到的定义（按类型分组）

"""

        # 按类型分组显示定义
        for elem_type in ['Thm', 'Def', 'Lemma', 'Prop', 'Cor']:
            type_defs = [e for e in self.definitions if e.elem_type == elem_type]
            if not type_defs:
                continue

            report += f"### {ELEMENT_TYPES.get(elem_type, elem_type)} ({len(type_defs)}个)\n\n"
            report += "| 编号 | 阶段 | 文件 | 行号 | 上下文 |\n"
            report += "|------|------|------|------|--------|\n"

            for elem in sorted(type_defs, key=lambda e: e.full_id)[:100]:
                context = elem.context[:30] + '...' if len(elem.context) > 30 else elem.context
                report += f"| {elem.full_id} | {elem.stage} | {elem.file_path} | {elem.line_num} | {context} |\n"

            if len(type_defs) > 100:
                report += f"\n... 还有 {len(type_defs) - 100} 个\n"
            report += "\n"

        report += """---

*报告由 check-theorem-registry.py 自动生成*
"""

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📝 报告已保存: {output_path}")

        return report


def main():
    parser = argparse.ArgumentParser(
        description='定理注册表检查工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python check-theorem-registry.py
    python check-theorem-registry.py --output report.md
    python check-theorem-registry.py --patch registry-patch.md
        """
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        help='输出完整报告文件路径'
    )
    parser.add_argument(
        '--patch', '-p',
        type=Path,
        help='输出注册表更新补丁文件路径'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细信息'
    )

    args = parser.parse_args()

    checker = TheoremRegistryChecker(PROJECT_ROOT)
    result = checker.run()

    if args.output:
        checker.generate_report(args.output)

    if args.patch:
        checker.generate_patch(args.patch)

    # 返回退出码
    if result.errors:
        print(f"\n❌ 检查完成，发现 {len(result.errors)} 个错误")
        sys.exit(1)
    elif result.warnings:
        print(f"\n⚠️ 检查完成，发现 {len(result.warnings)} 个警告")
        sys.exit(0)
    else:
        print("\n✅ 检查完成，一切正常！")
        sys.exit(0)


if __name__ == '__main__':
    main()
