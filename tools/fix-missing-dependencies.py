#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缺失依赖修复工具 - Missing Dependency Fixer

功能：
1. 分析验证报告中的 MISSING_DEPENDENCY 警告
2. 分类处理缺失依赖：
   - 类型A: 依赖元素不存在 → 需要添加定义或修正依赖
   - 类型B: 依赖元素存在但未扫描到 → 修复扫描路径
   - 类型C: 依赖声明错误 → 修正依赖声明
3. 自动修复可修复的问题
4. 生成待办清单用于手动修复

作者: AnalysisDataFlow Automation Team
版本: 1.0.0
日期: 2026-04-11
"""

import os
import re
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional, Any
from collections import defaultdict
from enum import Enum


class FixType(Enum):
    """修复类型"""
    AUTO_FIXED = "auto_fixed"          # 已自动修复
    MANUAL_REQUIRED = "manual_required" # 需要手动修复
    FALSE_POSITIVE = "false_positive"   # 误报（依赖实际存在但格式问题）
    DEFINITION_MISSING = "definition_missing"  # 需要添加定义
    DEPENDENCY_INVALID = "dependency_invalid"  # 依赖声明错误


@dataclass
class MissingDependency:
    """缺失依赖数据结构"""
    element_id: str           # 依赖元素ID (如 Def-S-01-04)
    referenced_by: str        # 引用此依赖的元素ID
    file_path: Optional[str]  # 引用元素所在文件
    line_number: Optional[int] # 引用元素行号
    fix_type: FixType = FixType.MANUAL_REQUIRED
    fix_suggestion: str = ""  # 修复建议


@dataclass
class FixResult:
    """修复结果数据结构"""
    missing_dep: MissingDependency
    status: str               # "fixed", "pending", "error"
    message: str              # 详细消息


class MissingDependencyFixer:
    """缺失依赖修复器主类"""
    
    def __init__(self, project_root: str, validation_report_path: str, verbose: bool = False):
        self.project_root = Path(project_root)
        self.validation_report_path = Path(validation_report_path)
        self.verbose = verbose
        self.missing_deps: List[MissingDependency] = []
        self.fix_results: List[FixResult] = []
        self.all_element_ids: Set[str] = set()
        self.registry_elements: Set[str] = set()
        
        # 统计
        self.stats = {
            "total_missing": 0,
            "auto_fixed": 0,
            "manual_required": 0,
            "false_positive": 0,
            "definition_missing": 0,
            "dependency_invalid": 0,
        }
        
    def _log(self, message: str, level: str = "info"):
        """输出日志信息"""
        if not self.verbose and level == "debug":
            return
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level.upper()}] {message}")
    
    def load_validation_report(self) -> bool:
        """加载验证报告"""
        try:
            with open(self.validation_report_path, 'r', encoding='utf-8') as f:
                report = json.load(f)
            
            # 提取 MISSING_DEPENDENCY 问题
            issues = report.get("issues", [])
            for issue in issues:
                if issue.get("code") == "MISSING_DEPENDENCY":
                    # 解析消息: "依赖的元素不存在: Def-S-01-04"
                    message = issue.get("message", "")
                    match = re.search(r'依赖的元素不存在:\s*(\S+)', message)
                    if match:
                        element_id = match.group(1)
                        missing_dep = MissingDependency(
                            element_id=element_id,
                            referenced_by=issue.get("element_id", ""),
                            file_path=issue.get("file_path"),
                            line_number=issue.get("line_number"),
                        )
                        self.missing_deps.append(missing_dep)
            
            # 加载已存在的元素
            elements = report.get("elements", {})
            self.all_element_ids = set(elements.keys())
            
            self.stats["total_missing"] = len(self.missing_deps)
            self._log(f"从验证报告加载了 {len(self.missing_deps)} 个缺失依赖", "info")
            return True
            
        except Exception as e:
            self._log(f"加载验证报告失败: {e}", "error")
            return False
    
    def scan_theorem_registry(self):
        """扫描 THEOREM-REGISTRY.md 获取所有注册的元素"""
        registry_path = self.project_root / "THEOREM-REGISTRY.md"
        if not registry_path.exists():
            self._log("THEOREM-REGISTRY.md 不存在", "warning")
            return
        
        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 匹配所有元素编号
            pattern = re.compile(r'(Thm|Def|Lemma|Prop|Cor)-([SKF])-(\d{2})-(\d{2,3})')
            for match in pattern.finditer(content):
                element_id = match.group(0)
                self.registry_elements.add(element_id)
            
            self._log(f"从注册表扫描到 {len(self.registry_elements)} 个元素", "info")
            
        except Exception as e:
            self._log(f"扫描注册表失败: {e}", "error")
    
    def categorize_missing_dependencies(self):
        """分类缺失依赖"""
        self._log("开始分类缺失依赖...", "info")
        
        for dep in self.missing_deps:
            element_id = dep.element_id
            
            # 检查是否在注册表中
            if element_id in self.registry_elements:
                # 注册表中有，但扫描时没找到 → 可能是扫描问题或文件未在扫描范围内
                dep.fix_type = FixType.FALSE_POSITIVE
                dep.fix_suggestion = f"元素 {element_id} 存在于注册表但未在文档扫描中发现。可能原因: 1) 文档不在扫描范围内 2) 格式问题导致未识别"
                self.stats["false_positive"] += 1
                continue
            
            # 检查元素编号格式是否正确
            if not self._is_valid_element_id(element_id):
                dep.fix_type = FixType.DEPENDENCY_INVALID
                dep.fix_suggestion = f"元素编号 {element_id} 格式可能不正确，请检查引用"
                self.stats["dependency_invalid"] += 1
                continue
            
            # 检查是否是文档编号错误（如 Def-S-01-04 可能应该是 Def-S-02-04）
            similar_id = self._find_similar_element(element_id)
            if similar_id:
                dep.fix_type = FixType.AUTO_FIXED
                dep.fix_suggestion = f"可能拼写错误，建议将 {element_id} 改为 {similar_id}"
                self.stats["auto_fixed"] += 1
                continue
            
            # 需要添加定义
            dep.fix_type = FixType.DEFINITION_MISSING
            dep.fix_suggestion = f"需要在合适位置创建 {element_id} 的定义"
            self.stats["definition_missing"] += 1
            self.stats["manual_required"] += 1
        
        self._log(f"分类完成: 可自动修复={self.stats['auto_fixed']}, "
                  f"需手动修复={self.stats['manual_required']}, "
                  f"误报={self.stats['false_positive']}", "info")
    
    def _is_valid_element_id(self, element_id: str) -> bool:
        """检查元素ID格式是否有效"""
        pattern = re.compile(r'^(Thm|Def|Lemma|Prop|Cor)-[SKF]-\d{2}-\d{2,3}$')
        return bool(pattern.match(element_id))
    
    def _find_similar_element(self, element_id: str) -> Optional[str]:
        """查找相似的元素（可能是拼写错误）"""
        if not self._is_valid_element_id(element_id):
            return None
        
        parts = element_id.split('-')
        if len(parts) != 4:
            return None
        
        type_, stage, doc_num, seq_num = parts
        
        # 尝试不同的文档编号（常见错误：文档编号差1）
        doc_num_int = int(doc_num)
        for delta in [-1, 1, -2, 2]:
            new_doc_num = f"{doc_num_int + delta:02d}"
            candidate = f"{type_}-{stage}-{new_doc_num}-{seq_num}"
            if candidate in self.all_element_ids:
                return candidate
        
        # 尝试不同的序号
        seq_num_int = int(seq_num)
        for delta in [-1, 1]:
            new_seq_num = f"{seq_num_int + delta:02d}"
            candidate = f"{type_}-{stage}-{doc_num}-{new_seq_num}"
            if candidate in self.all_element_ids:
                return candidate
        
        return None
    
    def generate_fix_script(self, output_path: str):
        """生成自动修复脚本"""
        fixes = [r for r in self.fix_results if r.status == "fixed"]
        
        lines = [
            "#!/usr/bin/env python3",
            "# -*- coding: utf-8 -*-",
            f'"""',
            f'自动生成的依赖修复脚本',
            f'生成时间: {datetime.now().isoformat()}',
            f'"""',
            "",
            "import re",
            "from pathlib import Path",
            "",
            "# 修复映射表: (文件路径, 原依赖ID, 新依赖ID)",
            "FIXES = [",
        ]
        
        for result in fixes:
            dep = result.missing_dep
            if dep.file_path:
                # 提取建议的新ID
                suggestion = dep.fix_suggestion
                match = re.search(r'改为\s+(\S+)', suggestion)
                if match:
                    new_id = match.group(1)
                    lines.append(f'    ("{dep.file_path}", "{dep.element_id}", "{new_id}"),')
        
        lines.extend([
            "]",
            "",
            "def apply_fixes():",
            "    for file_path, old_id, new_id in FIXES:",
            "        path = Path(file_path)",
            "        if not path.exists():",
            "            print(f'文件不存在: {file_path}')",
            "            continue",
            "        ",
            "        with open(path, 'r', encoding='utf-8') as f:",
            "            content = f.read()",
            "        ",
            "        # 替换依赖引用",
            "        content = re.sub(rf'\\\\b{re.escape(old_id)}\\\\b', new_id, content)",
            "        ",
            "        with open(path, 'w', encoding='utf-8') as f:",
            "            f.write(content)",
            "        ",
            "        print(f'已修复: {file_path} - {old_id} -> {new_id}')",
            "",
            "if __name__ == '__main__':",
            "    apply_fixes()",
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        self._log(f"自动修复脚本已生成: {output_path}", "info")
    
    def generate_todo_list(self, output_path: str):
        """生成待办清单"""
        manual_deps = [d for d in self.missing_deps 
                      if d.fix_type in (FixType.DEFINITION_MISSING, FixType.MANUAL_REQUIRED)]
        
        lines = [
            "# 缺失依赖待办清单",
            "",
            f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"> **总计**: {len(manual_deps)} 个需要手动处理的缺失依赖",
            "",
            "## 分类统计",
            "",
            f"- 需要添加定义: {self.stats['definition_missing']}",
            f"- 依赖声明错误: {self.stats['dependency_invalid']}",
            f"- 需手动确认: {self.stats['manual_required']}",
            "",
            "## 待办任务列表",
            "",
            "| 序号 | 缺失元素 | 被引用位置 | 修复建议 | 优先级 |",
            "|------|----------|------------|----------|--------|",
        ]
        
        # 按类型分组
        definition_missing = [d for d in manual_deps if d.fix_type == FixType.DEFINITION_MISSING]
        dependency_invalid = [d for d in manual_deps if d.fix_type == FixType.DEPENDENCY_INVALID]
        
        idx = 1
        for dep in definition_missing:
            location = f"{dep.file_path}:{dep.line_number}" if dep.file_path else "未知"
            lines.append(f"| {idx} | {dep.element_id} | {location} | {dep.fix_suggestion} | P1 |")
            idx += 1
        
        for dep in dependency_invalid:
            location = f"{dep.file_path}:{dep.line_number}" if dep.file_path else "未知"
            lines.append(f"| {idx} | {dep.element_id} | {location} | {dep.fix_suggestion} | P2 |")
            idx += 1
        
        lines.extend([
            "",
            "## 处理指南",
            "",
            "### P1 - 需要添加定义",
            "",
            "这些元素在依赖声明中被引用，但在项目中不存在。处理方式:",
            "",
            "1. **检查是否是引用错误**: 确认引用的元素编号是否正确",
            "2. **检查是否在草稿中**: 某些定义可能在草稿文档中，需要移动到正式文档",
            "3. **创建缺失定义**: 如果确实需要，在合适的位置创建该元素的定义",
            "",
            "### P2 - 依赖声明错误",
            "",
            "这些依赖声明可能存在格式错误或指向不存在的元素。处理方式:",
            "",
            "1. **修正编号格式**: 确保使用正确的元素编号格式",
            "2. **更新引用**: 将引用指向正确的元素",
            "3. **删除无效引用**: 如果引用不再适用，删除该依赖声明",
            "",
            "## 元素创建模板",
            "",
            "如需创建缺失的定义，可使用以下模板:",
            "",
            "```markdown",
            "**Def-S-XX-YY**: [定义名称]",
            "",
            "**定义**: ...",
            "",
            "**解释**: ...",
            "```",
            "",
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        self._log(f"待办清单已生成: {output_path}", "info")
    
    def generate_report(self, output_path: str):
        """生成修复报告"""
        lines = [
            "# 缺失依赖修复报告",
            "",
            f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"> **验证报告**: {self.validation_report_path}",
            "",
            "## 执行摘要",
            "",
            f"- **缺失依赖总数**: {self.stats['total_missing']}",
            f"- **可自动修复**: {self.stats['auto_fixed']}",
            f"- **需手动处理**: {self.stats['manual_required']}",
            f"- **误报**: {self.stats['false_positive']}",
            "",
            "## 分类详情",
            "",
            "### 可自动修复",
            "",
            "以下依赖可以通过脚本自动修复（可能是拼写错误）:",
            "",
        ]
        
        auto_fixes = [d for d in self.missing_deps if d.fix_type == FixType.AUTO_FIXED]
        if auto_fixes:
            lines.extend([
                "| 缺失元素 | 引用位置 | 修复建议 |",
                "|----------|----------|----------|",
            ])
            for dep in auto_fixes:
                location = f"{dep.file_path}:{dep.line_number}" if dep.file_path else "未知"
                lines.append(f"| {dep.element_id} | {location} | {dep.fix_suggestion} |")
        else:
            lines.append("*无可自动修复的依赖*")
        
        lines.extend([
            "",
            "### 需要添加定义",
            "",
            "以下元素在依赖声明中被引用但不存在于项目中:",
            "",
        ])
        
        definition_missing = [d for d in self.missing_deps if d.fix_type == FixType.DEFINITION_MISSING]
        if definition_missing:
            lines.extend([
                "| 缺失元素 | 引用位置 | 建议操作 |",
                "|----------|----------|----------|",
            ])
            # 去重
            seen = set()
            for dep in definition_missing:
                if dep.element_id not in seen:
                    seen.add(dep.element_id)
                    location = dep.file_path or "未知"
                    lines.append(f"| {dep.element_id} | {location} | 创建定义或修正引用 |")
        else:
            lines.append("*无需要添加定义的依赖*")
        
        lines.extend([
            "",
            "### 可能的误报",
            "",
            "以下元素在注册表中存在但未在文档扫描中发现:",
            "",
        ])
        
        false_positives = [d for d in self.missing_deps if d.fix_type == FixType.FALSE_POSITIVE]
        if false_positives:
            lines.extend([
                "| 元素 | 引用位置 | 说明 |",
                "|------|----------|------|",
            ])
            for dep in false_positives[:20]:  # 限制数量
                location = f"{dep.file_path}:{dep.line_number}" if dep.file_path else "未知"
                lines.append(f"| {dep.element_id} | {location} | 注册表中有但文档中未扫描到 |")
            if len(false_positives) > 20:
                lines.append(f"| ... | ... | 还有 {len(false_positives) - 20} 个 |")
        else:
            lines.append("*无误报*")
        
        lines.extend([
            "",
            "### 依赖声明错误",
            "",
        ])
        
        invalid_deps = [d for d in self.missing_deps if d.fix_type == FixType.DEPENDENCY_INVALID]
        if invalid_deps:
            lines.extend([
                "| 元素 | 引用位置 | 问题 |",
                "|------|----------|------|",
            ])
            for dep in invalid_deps:
                location = f"{dep.file_path}:{dep.line_number}" if dep.file_path else "未知"
                lines.append(f"| {dep.element_id} | {location} | 格式可能不正确 |")
        else:
            lines.append("*无依赖声明错误*")
        
        lines.extend([
            "",
            "## 修复建议汇总",
            "",
            "1. **优先处理可自动修复的依赖**: 运行生成的修复脚本",
            "2. **检查误报**: 确认注册表和文档扫描范围是否一致",
            "3. **创建缺失定义**: 对于确实需要的元素，在适当位置创建定义",
            "4. **修正错误引用**: 更新指向错误元素编号的依赖声明",
            "",
            "## 后续步骤",
            "",
            "1. 执行自动修复脚本（如有）",
            "2. 按待办清单手动处理剩余问题",
            "3. 重新运行验证工具检查修复效果",
            "",
            "---",
            "",
            "*报告由 Missing Dependency Fixer 自动生成*",
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        self._log(f"修复报告已生成: {output_path}", "info")
    
    def run(self, output_dir: str):
        """运行完整的修复流程"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print("\n" + "=" * 60)
        print(" 缺失依赖修复工具 v1.0.0 ")
        print("=" * 60 + "\n")
        
        # 1. 加载验证报告
        if not self.load_validation_report():
            print("无法加载验证报告，退出")
            return False
        
        # 2. 扫描注册表
        self.scan_theorem_registry()
        
        # 3. 分类缺失依赖
        self.categorize_missing_dependencies()
        
        print("\n" + "-" * 60)
        print("正在生成输出文件...")
        print("-" * 60 + "\n")
        
        # 4. 生成输出文件
        self.generate_report(str(output_path / "fix-missing-dependencies-report.md"))
        self.generate_todo_list(str(output_path / "TODO-MISSING-DEPENDENCIES.md"))
        
        # 5. 如果有可自动修复的，生成修复脚本
        if self.stats["auto_fixed"] > 0:
            self.generate_fix_script(str(output_path / "apply-auto-fixes.py"))
        
        # 6. 打印摘要
        self._print_summary()
        
        return True
    
    def _print_summary(self):
        """打印修复摘要"""
        print("\n" + "=" * 60)
        print(" 修复完成摘要 ")
        print("=" * 60)
        print()
        print(f"  缺失依赖总数:     {self.stats['total_missing']}")
        print(f"  可自动修复:       {self.stats['auto_fixed']}")
        print(f"  需手动处理:       {self.stats['manual_required']}")
        print(f"  误报:             {self.stats['false_positive']}")
        print()
        print("  输出文件:")
        print("    - fix-missing-dependencies-report.md")
        print("    - TODO-MISSING-DEPENDENCIES.md")
        if self.stats["auto_fixed"] > 0:
            print("    - apply-auto-fixes.py")
        print()
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="缺失依赖修复工具 - 分析并修复 MISSING_DEPENDENCY 警告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  python fix-missing-dependencies.py
  
  # 指定验证报告和输出目录
  python fix-missing-dependencies.py -r ./reports/validation-report.json -o ./reports
  
  # 详细输出
  python fix-missing-dependencies.py -v
        """
    )
    
    parser.add_argument(
        '-r', '--report',
        default='./reports/validation-report-2026-04-11.json',
        help='验证报告JSON文件路径 (默认: ./reports/validation-report-2026-04-11.json)'
    )
    parser.add_argument(
        '-o', '--output',
        default='./reports',
        help='输出目录 (默认: ./reports)'
    )
    parser.add_argument(
        '--root',
        default='.',
        help='项目根目录 (默认: 当前目录)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='启用详细输出'
    )
    
    args = parser.parse_args()
    
    # 创建修复器实例
    fixer = MissingDependencyFixer(
        project_root=args.root,
        validation_report_path=args.report,
        verbose=args.verbose
    )
    
    # 运行修复流程
    try:
        success = fixer.run(args.output)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
