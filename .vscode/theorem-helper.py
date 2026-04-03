#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AnalysisDataFlow 定理证明辅助工具

功能:
1. 定理编号生成器 - 生成并检查定理编号冲突
2. 定理引用检查器 - 扫描并验证文档中的定理引用
3. 证明链生成器 - 生成从公理到目标的证明链
4. 定理统计报告 - 生成统计报告和未使用定理识别
5. 定理模板生成 - 生成标准定理模板

用法:
    python theorem-helper.py <command> [options]

命令:
    generate    生成定理编号
    check       检查文档中的定理引用
    chain       生成证明链
    stats       生成统计报告
    template    生成定理模板
"""

import re
import os
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional, Iterator
from collections import defaultdict
from datetime import datetime


# ============== 常量定义 ==============

PROJECT_ROOT = Path(__file__).parent.parent
REGISTRY_PATH = PROJECT_ROOT / "THEOREM-REGISTRY.md"
STRUCT_DIR = PROJECT_ROOT / "Struct"
KNOWLEDGE_DIR = PROJECT_ROOT / "Knowledge"
FLINK_DIR = PROJECT_ROOT / "Flink"

# 定理类型映射
TYPE_MAP = {
    "Thm": "定理",
    "Lemma": "引理",
    "Def": "定义",
    "Prop": "命题",
    "Cor": "推论"
}

# 阶段映射
STAGE_MAP = {
    "S": "Struct",
    "K": "Knowledge",
    "F": "Flink"
}

# 阶段到目录的映射
STAGE_TO_DIR = {
    "S": STRUCT_DIR,
    "K": KNOWLEDGE_DIR,
    "F": FLINK_DIR
}

# 正则表达式模式
THEOREM_ID_PATTERN = re.compile(
    r'(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d{2})-(\d{2})'
)

THEOREM_REF_PATTERN = re.compile(
    r'`?(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d{2})-(\d{2})`?'
)

REGISTRY_TABLE_PATTERN = re.compile(
    r'\|\s*(Thm|Lemma|Def|Prop|Cor)-([SKF])-(\d{2})-(\d{2})\s*\|'
)


# ============== 数据类定义 ==============

@dataclass
class TheoremEntry:
    """定理条目"""
    theorem_id: str
    name: str
    location: str
    level: Optional[str] = None
    status: str = "✅"
    theorem_type: str = ""
    stage: str = ""
    doc_num: str = ""
    seq_num: str = ""
    
    def __post_init__(self):
        """解析定理ID"""
        match = THEOREM_ID_PATTERN.match(self.theorem_id)
        if match:
            self.theorem_type = match.group(1)
            self.stage = match.group(2)
            self.doc_num = match.group(3)
            self.seq_num = match.group(4)
    
    @property
    def full_id(self) -> str:
        return self.theorem_id
    
    @property
    def type_name(self) -> str:
        return TYPE_MAP.get(self.theorem_type, self.theorem_type)


@dataclass
class DocumentReference:
    """文档中的定理引用"""
    theorem_id: str
    line_num: int
    line_content: str
    context: str = ""


@dataclass
class DocumentInfo:
    """文档信息"""
    path: Path
    theorems: List[TheoremEntry] = field(default_factory=list)
    references: List[DocumentReference] = field(default_factory=list)
    

# ============== 定理注册表解析器 ==============

class TheoremRegistry:
    """定理注册表管理器"""
    
    def __init__(self, registry_path: Path = REGISTRY_PATH):
        self.registry_path = registry_path
        self.theorems: Dict[str, TheoremEntry] = {}
        self.by_type: Dict[str, List[TheoremEntry]] = defaultdict(list)
        self.by_stage: Dict[str, List[TheoremEntry]] = defaultdict(list)
        self.by_doc: Dict[Tuple[str, str], List[TheoremEntry]] = defaultdict(list)
        self._parsed = False
    
    def parse(self) -> 'TheoremRegistry':
        """解析注册表文件"""
        if self._parsed:
            return self
        
        if not self.registry_path.exists():
            print(f"警告: 注册表文件不存在: {self.registry_path}")
            return self
        
        content = self.registry_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        current_section = ""
        for line in lines:
            line = line.strip()
            
            # 检测章节标题
            if line.startswith('## '):
                current_section = line
                continue
            
            # 解析表格行
            if line.startswith('|') and not line.startswith('|----'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 3:
                    theorem_id = parts[0]
                    match = THEOREM_ID_PATTERN.match(theorem_id)
                    if match:
                        name = parts[1] if len(parts) > 1 else ""
                        location = parts[2] if len(parts) > 2 else ""
                        level = parts[3] if len(parts) > 3 else None
                        status = parts[4] if len(parts) > 4 else "✅"
                        
                        entry = TheoremEntry(
                            theorem_id=theorem_id,
                            name=name,
                            location=location,
                            level=level,
                            status=status
                        )
                        self._add_entry(entry)
        
        self._parsed = True
        return self
    
    def _add_entry(self, entry: TheoremEntry):
        """添加定理条目"""
        self.theorems[entry.theorem_id] = entry
        self.by_type[entry.theorem_type].append(entry)
        self.by_stage[entry.stage].append(entry)
        self.by_doc[(entry.stage, entry.doc_num)].append(entry)
    
    def exists(self, theorem_id: str) -> bool:
        """检查定理是否存在"""
        return theorem_id in self.theorems
    
    def get(self, theorem_id: str) -> Optional[TheoremEntry]:
        """获取定理条目"""
        return self.theorems.get(theorem_id)
    
    def get_next_seq_num(self, theorem_type: str, stage: str, doc_num: str) -> int:
        """获取下一个可用的序号"""
        key = (stage, doc_num)
        existing = [
            int(t.seq_num) for t in self.by_doc.get(key, [])
            if t.theorem_type == theorem_type
        ]
        return max(existing, default=0) + 1
    
    def suggest_number(self, theorem_type: str, stage: str, doc_num: str) -> str:
        """建议定理编号"""
        next_seq = self.get_next_seq_num(theorem_type, stage, doc_num)
        return f"{theorem_type}-{stage}-{doc_num}-{next_seq:02d}"
    
    def get_dependencies(self, theorem_id: str) -> List[str]:
        """获取定理的依赖（基于名称中的引用）"""
        entry = self.get(theorem_id)
        if not entry:
            return []
        
        # 从关键作用字段提取依赖
        deps = []
        if hasattr(entry, 'key_role'):
            matches = THEOREM_REF_PATTERN.findall(entry.key_role or "")
            deps = [f"{m[0]}-{m[1]}-{m[2]}-{m[3]}" for m in matches]
        return deps


# ============== 文档扫描器 ==============

class DocumentScanner:
    """文档扫描器"""
    
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.documents: List[DocumentInfo] = []
    
    def scan_directory(self, directory: Path) -> Iterator[Path]:
        """扫描目录中的所有markdown文件"""
        if not directory.exists():
            return
        for path in directory.rglob('*.md'):
            if path.name.startswith('00-INDEX'):
                continue
            yield path
    
    def scan_document(self, doc_path: Path) -> DocumentInfo:
        """扫描单个文档"""
        info = DocumentInfo(path=doc_path)
        
        try:
            content = doc_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # 扫描定理引用
                for match in THEOREM_REF_PATTERN.finditer(line):
                    theorem_id = f"{match.group(1)}-{match.group(2)}-{match.group(3)}-{match.group(4)}"
                    ref = DocumentReference(
                        theorem_id=theorem_id,
                        line_num=line_num,
                        line_content=line.strip()
                    )
                    info.references.append(ref)
        except Exception as e:
            print(f"警告: 无法读取文档 {doc_path}: {e}")
        
        return info
    
    def scan_all(self) -> List[DocumentInfo]:
        """扫描所有文档"""
        self.documents = []
        for directory in [STRUCT_DIR, KNOWLEDGE_DIR, FLINK_DIR]:
            for doc_path in self.scan_directory(directory):
                info = self.scan_document(doc_path)
                if info.references:
                    self.documents.append(info)
        return self.documents


# ============== 命令实现 ==============

class TheoremNumberGenerator:
    """定理编号生成器"""
    
    def __init__(self, registry: TheoremRegistry):
        self.registry = registry
    
    def generate(self, theorem_type: str, stage: str, doc_num: str, 
                 check_conflicts: bool = True) -> dict:
        """生成定理编号"""
        # 标准化输入
        theorem_type = theorem_type.capitalize()
        stage = stage.upper()
        doc_num = doc_num.zfill(2)
        
        # 验证输入
        if theorem_type not in TYPE_MAP:
            return {"error": f"无效的类型: {theorem_type}. 可选: {', '.join(TYPE_MAP.keys())}"}
        if stage not in STAGE_MAP:
            return {"error": f"无效的阶段: {stage}. 可选: {', '.join(STAGE_MAP.keys())}"}
        
        # 生成建议编号
        suggested = self.registry.suggest_number(theorem_type, stage, doc_num)
        
        # 检查现有定理
        existing = self.registry.by_doc.get((stage, doc_num), [])
        existing_same_type = [t for t in existing if t.theorem_type == theorem_type]
        
        result = {
            "suggested_id": suggested,
            "type": theorem_type,
            "type_name": TYPE_MAP[theorem_type],
            "stage": stage,
            "stage_name": STAGE_MAP[stage],
            "doc_num": doc_num,
            "existing_count": len(existing),
            "existing_same_type": len(existing_same_type),
            "next_sequence": int(suggested.split('-')[-1]),
            "conflicts": []
        }
        
        # 检查编号冲突（如果启用）
        if check_conflicts and existing:
            for t in existing:
                if t.seq_num == suggested.split('-')[-1]:
                    result["conflicts"].append({
                        "id": t.theorem_id,
                        "name": t.name,
                        "location": t.location
                    })
        
        return result
    
    def print_result(self, result: dict):
        """打印生成结果"""
        if "error" in result:
            print(f"❌ 错误: {result['error']}")
            return
        
        print(f"\n{'='*60}")
        print(f"📋 定理编号生成结果")
        print(f"{'='*60}")
        print(f"建议编号:      {result['suggested_id']}")
        print(f"类型:          {result['type_name']} ({result['type']})")
        print(f"阶段:          {result['stage_name']} ({result['stage']})")
        print(f"文档序号:      {result['doc_num']}")
        print(f"该文档已存在:  {result['existing_count']} 个形式化元素")
        print(f"同类型已有:    {result['existing_same_type']} 个")
        print(f"新序号:        {result['next_sequence']:02d}")
        
        if result['conflicts']:
            print(f"\n⚠️  发现编号冲突:")
            for c in result['conflicts']:
                print(f"   - {c['id']}: {c['name']} ({c['location']})")
        else:
            print(f"\n✅ 无编号冲突，可以安全使用")
        
        print(f"{'='*60}")


class TheoremReferenceChecker:
    """定理引用检查器"""
    
    def __init__(self, registry: TheoremRegistry):
        self.registry = registry
        self.scanner = DocumentScanner(PROJECT_ROOT)
    
    def check_document(self, doc_path: Path) -> dict:
        """检查单个文档"""
        info = self.scanner.scan_document(doc_path)
        
        valid_refs = []
        invalid_refs = []
        
        for ref in info.references:
            if self.registry.exists(ref.theorem_id):
                entry = self.registry.get(ref.theorem_id)
                valid_refs.append({
                    "theorem_id": ref.theorem_id,
                    "name": entry.name if entry else "",
                    "line": ref.line_num,
                    "content": ref.line_content[:80]
                })
            else:
                invalid_refs.append({
                    "theorem_id": ref.theorem_id,
                    "line": ref.line_num,
                    "content": ref.line_content[:80]
                })
        
        return {
            "document": str(doc_path),
            "total_refs": len(info.references),
            "valid_refs": valid_refs,
            "invalid_refs": invalid_refs,
            "valid_count": len(valid_refs),
            "invalid_count": len(invalid_refs)
        }
    
    def check_all(self) -> dict:
        """检查所有文档"""
        self.scanner.scan_all()
        
        all_results = []
        total_valid = 0
        total_invalid = 0
        
        for info in self.scanner.documents:
            result = self.check_document(info.path)
            all_results.append(result)
            total_valid += result['valid_count']
            total_invalid += result['invalid_count']
        
        return {
            "documents_checked": len(all_results),
            "total_valid": total_valid,
            "total_invalid": total_invalid,
            "results": all_results
        }
    
    def print_result(self, result: dict, verbose: bool = False):
        """打印检查结果"""
        print(f"\n{'='*60}")
        print(f"🔍 定理引用检查报告")
        print(f"{'='*60}")
        print(f"检查文档数: {result['documents_checked']}")
        print(f"有效引用:   {result['total_valid']}")
        print(f"无效引用:   {result['total_invalid']}")
        
        if result['total_invalid'] > 0:
            print(f"\n❌ 发现无效引用:")
            for doc_result in result['results']:
                if doc_result['invalid_count'] > 0:
                    print(f"\n  📄 {doc_result['document']}")
                    for inv in doc_result['invalid_refs']:
                        print(f"     行 {inv['line']}: `{inv['theorem_id']}`")
                        if verbose:
                            print(f"        {inv['content']}")
        
        if verbose and result['total_valid'] > 0:
            print(f"\n✅ 有效引用示例:")
            shown = 0
            for doc_result in result['results']:
                for valid in doc_result['valid_refs'][:3]:
                    print(f"   - {valid['theorem_id']}: {valid['name']}")
                    shown += 1
                    if shown >= 10:
                        break
                if shown >= 10:
                    break
        
        print(f"{'='*60}")


class ProofChainGenerator:
    """证明链生成器"""
    
    def __init__(self, registry: TheoremRegistry):
        self.registry = registry
        self.dependency_graph = self._build_dependency_graph()
    
    def _build_dependency_graph(self) -> Dict[str, Set[str]]:
        """构建依赖图"""
        graph = defaultdict(set)
        
        # 基于引理的关键作用字段构建依赖关系
        for entry in self.registry.theorems.values():
            # 解析依赖（从其他定理引用中推断）
            if entry.theorem_type == "Lemma":
                # 引理通常支撑某个定理
                for theorem in self.registry.by_type.get("Thm", []):
                    if entry.location == theorem.location:
                        graph[theorem.theorem_id].add(entry.theorem_id)
            elif entry.theorem_type == "Thm":
                # 定理可能依赖定义
                for df in self.registry.by_type.get("Def", []):
                    if df.location == entry.location:
                        graph[entry.theorem_id].add(df.theorem_id)
        
        return graph
    
    def generate_chain(self, target_id: str, max_depth: int = 10) -> dict:
        """生成证明链"""
        if not self.registry.exists(target_id):
            return {"error": f"定理不存在: {target_id}"}
        
        target = self.registry.get(target_id)
        chain = []
        visited = set()
        
        def dfs(theorem_id: str, depth: int):
            if depth > max_depth or theorem_id in visited:
                return
            visited.add(theorem_id)
            
            entry = self.registry.get(theorem_id)
            if entry:
                chain.append({
                    "id": theorem_id,
                    "name": entry.name,
                    "type": entry.type_name,
                    "depth": depth
                })
            
            # 获取依赖
            deps = self.dependency_graph.get(theorem_id, set())
            for dep in sorted(deps):
                dfs(dep, depth + 1)
        
        dfs(target_id, 0)
        
        return {
            "target": target_id,
            "target_name": target.name if target else "",
            "chain_length": len(chain),
            "chain": chain
        }
    
    def generate_mermaid(self, target_id: str) -> str:
        """生成Mermaid依赖图"""
        chain_result = self.generate_chain(target_id)
        
        if "error" in chain_result:
            return f"%% Error: {chain_result['error']}"
        
        lines = ["graph TD"]
        
        # 添加节点
        for node in chain_result['chain']:
            node_id = node['id'].replace('-', '_')
            lines.append(f'    {node_id}["{node["id"]}<br/>{node["name"][:30]}..."]')
        
        # 添加边
        for node in chain_result['chain']:
            deps = self.dependency_graph.get(node['id'], set())
            node_id = node['id'].replace('-', '_')
            for dep in deps:
                dep_id = dep.replace('-', '_')
                lines.append(f'    {dep_id} --> {node_id}')
        
        return '\n'.join(lines)
    
    def print_result(self, result: dict, mermaid: bool = False):
        """打印证明链"""
        if "error" in result:
            print(f"❌ 错误: {result['error']}")
            return
        
        print(f"\n{'='*60}")
        print(f"🔗 证明链: {result['target']}")
        print(f"{'='*60}")
        print(f"目标定理: {result['target_name']}")
        print(f"链长度:   {result['chain_length']}")
        
        print(f"\n证明链 (从目标到依赖):")
        for node in result['chain']:
            indent = "  " * node['depth']
            print(f"{indent}└─ [{node['type']}] {node['id']}: {node['name']}")
        
        print(f"{'='*60}")
        
        if mermaid:
            print(f"\n📊 Mermaid 图:")
            print(self.generate_mermaid(result['target']))


class TheoremStatistics:
    """定理统计报告"""
    
    def __init__(self, registry: TheoremRegistry):
        self.registry = registry
        self.scanner = DocumentScanner(PROJECT_ROOT)
    
    def generate_report(self) -> dict:
        """生成统计报告"""
        # 按类型统计
        type_stats = {}
        for t_type, entries in self.registry.by_type.items():
            type_stats[t_type] = {
                "count": len(entries),
                "name": TYPE_MAP.get(t_type, t_type)
            }
        
        # 按阶段统计
        stage_stats = {}
        for stage, entries in self.registry.by_stage.items():
            stage_stats[stage] = {
                "count": len(entries),
                "name": STAGE_MAP.get(stage, stage)
            }
        
        # 按文档统计
        doc_stats = []
        for (stage, doc_num), entries in sorted(self.registry.by_doc.items()):
            type_counts = defaultdict(int)
            for e in entries:
                type_counts[e.theorem_type] += 1
            
            doc_stats.append({
                "stage": stage,
                "doc_num": doc_num,
                "total": len(entries),
                "type_counts": dict(type_counts)
            })
        
        # 检查未使用的定理
        all_refs = self._collect_all_references()
        unused = []
        for theorem_id in self.registry.theorems.keys():
            if theorem_id not in all_refs and theorem_id.startswith('Thm'):
                entry = self.registry.get(theorem_id)
                unused.append({
                    "id": theorem_id,
                    "name": entry.name if entry else ""
                })
        
        return {
            "total_theorems": len(self.registry.theorems),
            "by_type": type_stats,
            "by_stage": stage_stats,
            "by_document": doc_stats,
            "unused_theorems": unused[:20],  # 限制数量
            "unused_count": len(unused)
        }
    
    def _collect_all_references(self) -> Set[str]:
        """收集所有引用"""
        self.scanner.scan_all()
        refs = set()
        for info in self.scanner.documents:
            for ref in info.references:
                refs.add(ref.theorem_id)
        return refs
    
    def print_report(self, report: dict):
        """打印统计报告"""
        print(f"\n{'='*70}")
        print(f"📊 AnalysisDataFlow 定理统计报告")
        print(f"{'='*70}")
        
        print(f"\n📈 总体统计")
        print(f"   总形式化元素数: {report['total_theorems']}")
        
        print(f"\n📚 按类型分布")
        for t_type, stats in sorted(report['by_type'].items(), 
                                     key=lambda x: x[1]['count'], reverse=True):
            bar = '█' * (stats['count'] // 5)
            print(f"   {stats['name']:<8} ({t_type}): {stats['count']:>3} {bar}")
        
        print(f"\n📁 按阶段分布")
        for stage, stats in sorted(report['by_stage'].items()):
            print(f"   {stats['name']:<12} ({stage}): {stats['count']}")
        
        print(f"\n📝 按文档统计 (Top 10)")
        for doc in sorted(report['by_document'], 
                         key=lambda x: x['total'], reverse=True)[:10]:
            type_str = ', '.join([f"{k}:{v}" for k, v in doc['type_counts'].items()])
            print(f"   {doc['stage']}-{doc['doc_num']}: {doc['total']:>2} ({type_str})")
        
        if report['unused_theorems']:
            print(f"\n⚠️  可能未使用的定理 (Top 10)")
            for t in report['unused_theorems'][:10]:
                print(f"   - {t['id']}: {t['name']}")
            if report['unused_count'] > 10:
                print(f"   ... 还有 {report['unused_count'] - 10} 个")
        
        print(f"{'='*70}")


class TheoremTemplateGenerator:
    """定理模板生成器"""
    
    TEMPLATES = {
        "Thm": """### 定理 {number} ({name})

**定理陈述**:
> 在此陈述定理内容

**形式化表述**:
```
∀x ∈ D. P(x) ⇒ Q(x)
```

**证明**:
1. **基础步骤**: ...
2. **归纳步骤**: ...
3. **结论**: ...

∎

---
""",
        "Lemma": """### 引理 {number} ({name})

**引理陈述**:
> 在此陈述引理内容

**证明**:
... 

∎

---
""",
        "Def": """### 定义 {number} ({name})

**定义**:
$$
\\text{{{name}}} ::= \\langle \\text{{组件列表}} \\rangle
$$

| 组件 | 类型 | 语义 |
|------|------|------|
| ... | ... | ... |

**解释**: 
...

---
""",
        "Prop": """### 命题 {number} ({name})

**命题**:
> 在此陈述命题内容

**论证**:
...

---
""",
        "Cor": """### 推论 {number} ({name})

**推论**:
> 在此陈述推论内容

**推导**:
由 {parent_theorem} 直接可得。

---
"""
    }
    
    def generate(self, theorem_type: str, number: str, name: str, 
                 parent_theorem: str = "") -> str:
        """生成定理模板"""
        template = self.TEMPLATES.get(theorem_type, self.TEMPLATES["Thm"])
        return template.format(
            number=number,
            name=name,
            parent_theorem=parent_theorem
        )
    
    def generate_document_template(self, stage: str, doc_num: str) -> str:
        """生成完整文档模板"""
        stage_name = STAGE_MAP.get(stage, stage)
        
        return f"""# 文档标题

> **所属阶段**: {stage_name}/ | **前置依赖**: [] | **形式化等级**: L4

---

## 1. 概念定义 (Definitions)

<!-- 在此添加定义，每个定义使用 Def-{stage}-{doc_num}-XX 编号 -->

{self.generate("Def", f"{stage}-{doc_num}-01", "示例定义")}

## 2. 属性推导 (Properties)

<!-- 在此添加引理，每个引理使用 Lemma-{stage}-{doc_num}-XX 编号 -->

{self.generate("Lemma", f"{stage}-{doc_num}-01", "示例引理")}

## 3. 关系建立 (Relations)

<!-- 描述与其他概念/模型的关系 -->

## 4. 论证过程 (Argumentation)

<!-- 辅助分析、边界讨论 -->

## 5. 形式证明 (Proofs)

<!-- 在此添加定理，每个定理使用 Thm-{stage}-{doc_num}-XX 编号 -->

{self.generate("Thm", f"{stage}-{doc_num}-01", "示例定理")}

## 6. 实例验证 (Examples)

<!-- 代码片段、配置示例 -->

## 7. 可视化 (Visualizations)

```mermaid
graph TD
    A[起点] --> B[中间节点]
    B --> C[终点]
```

## 8. 引用参考 (References)

[^1]: 引用来源

---

*文档创建时间: {datetime.now().strftime('%Y-%m-%d')}*
"""


# ============== 命令行接口 ==============

def main():
    parser = argparse.ArgumentParser(
        description="AnalysisDataFlow 定理证明辅助工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 生成定理编号
    python theorem-helper.py generate Thm S 01
    
    # 检查文档引用
    python theorem-helper.py check
    
    # 生成证明链
    python theorem-helper.py chain Thm-S-17-01 --mermaid
    
    # 生成统计报告
    python theorem-helper.py stats
    
    # 生成模板
    python theorem-helper.py template Thm "新定理名称"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # generate 命令
    gen_parser = subparsers.add_parser('generate', help='生成定理编号')
    gen_parser.add_argument('type', choices=['Thm', 'Lemma', 'Def', 'Prop', 'Cor'],
                          help='定理类型')
    gen_parser.add_argument('stage', choices=['S', 'K', 'F'],
                          help='阶段 (S=Struct, K=Knowledge, F=Flink)')
    gen_parser.add_argument('doc_num', help='文档序号 (如: 01, 02)')
    
    # check 命令
    check_parser = subparsers.add_parser('check', help='检查文档中的定理引用')
    check_parser.add_argument('--doc', '-d', type=Path, help='指定文档路径')
    check_parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    # chain 命令
    chain_parser = subparsers.add_parser('chain', help='生成证明链')
    chain_parser.add_argument('theorem_id', help='目标定理ID (如: Thm-S-17-01)')
    chain_parser.add_argument('--mermaid', '-m', action='store_true', help='输出Mermaid图')
    
    # stats 命令
    stats_parser = subparsers.add_parser('stats', help='生成统计报告')
    stats_parser.add_argument('--json', '-j', action='store_true', help='输出JSON格式')
    
    # template 命令
    tmpl_parser = subparsers.add_parser('template', help='生成定理模板')
    tmpl_parser.add_argument('type', choices=['Thm', 'Lemma', 'Def', 'Prop', 'Cor', 'Doc'],
                          help='模板类型')
    tmpl_parser.add_argument('name', nargs='?', default='新定理', help='定理名称')
    tmpl_parser.add_argument('--number', '-n', help='定理编号')
    tmpl_parser.add_argument('--stage', '-s', choices=['S', 'K', 'F'], help='阶段')
    tmpl_parser.add_argument('--doc-num', '-d', help='文档序号')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 初始化注册表
    registry = TheoremRegistry().parse()
    
    # 执行命令
    if args.command == 'generate':
        generator = TheoremNumberGenerator(registry)
        result = generator.generate(args.type, args.stage, args.doc_num)
        generator.print_result(result)
    
    elif args.command == 'check':
        checker = TheoremReferenceChecker(registry)
        if args.doc:
            result = checker.check_document(args.doc)
            checker.print_result({"results": [result], **result}, args.verbose)
        else:
            result = checker.check_all()
            checker.print_result(result, args.verbose)
    
    elif args.command == 'chain':
        chain_gen = ProofChainGenerator(registry)
        result = chain_gen.generate_chain(args.theorem_id)
        chain_gen.print_result(result, args.mermaid)
    
    elif args.command == 'stats':
        stats = TheoremStatistics(registry)
        report = stats.generate_report()
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            stats.print_report(report)
    
    elif args.command == 'template':
        tmpl_gen = TheoremTemplateGenerator()
        
        if args.type == 'Doc':
            if not args.stage or not args.doc_num:
                print("❌ 生成文档模板需要 --stage 和 --doc-num 参数")
                return
            template = tmpl_gen.generate_document_template(args.stage, args.doc_num)
        else:
            if not args.number:
                print("❌ 生成定理模板需要 --number 参数")
                return
            template = tmpl_gen.generate(args.type, args.number, args.name)
        
        print(template)


if __name__ == '__main__':
    main()
