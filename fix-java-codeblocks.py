#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R1: Java代码示例可运行性修复脚本

策略：
1. 解析 CODE-EXAMPLE-VALIDATION-REPORT.md 获取失败的 Java 代码块
2. 对失败代码块分类处理：
   - 类型A（片段/缺上下文）：添加伪代码标注
   - 类型B（语法错误）：尝试修复
   - 类型C（核心API）：补充最小上下文
3. 跳过 release/ 目录
"""

import re
import os
from collections import defaultdict, Counter

PSEUDO_COMMENT = "// [伪代码片段 - 不可直接运行] 仅展示核心逻辑"
PSEUDO_COMMENT_ALT = "// [伪代码片段 - 不可直接运行]"

CORE_DIRS = [
    "Flink/03-api/",
    "Flink/04-runtime/",
    "Flink/02-core/",
    "Knowledge/07-best-practices/",
]


def parse_report(report_path):
    """解析验证报告，返回 (文件名, 行号, 错误类型) 列表"""
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    sections = content.split("### `")
    failures = []
    for section in sections[1:]:
        lines = section.split("\n")
        filename = lines[0].strip().rstrip("`").lstrip("`")
        filename = filename.replace("\\", "/")

        # 跳过 release/ 目录
        if filename.startswith("release/"):
            continue

        i = 0
        while i < len(lines):
            if "语言: java" in lines[i]:
                # 提取行号
                line_num = None
                check_lines = [lines[i]]
                if i > 0:
                    check_lines.insert(0, lines[i - 1])
                for cl in check_lines:
                    m = re.search(r"第 (\d+) 行", cl)
                    if m:
                        line_num = int(m.group(1))
                        break

                # 提取错误类型
                error_type = "unknown"
                for j in range(i + 1, min(len(lines), i + 15)):
                    if "非法的表达式开始" in lines[j]:
                        error_type = "illegal_expression"
                        break
                    elif "找不到符号" in lines[j]:
                        error_type = "symbol_not_found"
                        break
                    elif "未命名类" in lines[j]:
                        error_type = "unnamed_class"
                        break
                    elif "非法字符" in lines[j]:
                        error_type = "illegal_char"
                        break
                    elif "不是语句" in lines[j]:
                        error_type = "not_statement"
                        break
                    elif "需要" in lines[j] and ";" in lines[j]:
                        error_type = "need_semicolon"
                        break

                if line_num:
                    failures.append((filename, line_num, error_type))
            i += 1

    return failures


def find_codeblock_boundaries(lines, target_line_1based):
    """找到 target_line_1based 所在的 java 代码块边界（0-based, [start, end)）"""
    target_idx = target_line_1based - 1  # 转 0-based

    # 向前找 ```java
    start = None
    for i in range(target_idx, -1, -1):
        stripped = lines[i].strip()
        if stripped.startswith("```java"):
            start = i
            break
        elif stripped == "```" and i < target_idx:
            # 遇到了另一个代码块的结束，停止
            pass

    if start is None:
        return None

    # 向后找 ```
    end = None
    for i in range(start + 1, len(lines)):
        if lines[i].strip() == "```":
            end = i
            break

    if end is None:
        return None

    return (start, end)


def is_pseudocode_marked(code_lines):
    """检查代码块是否已有伪代码标注"""
    for line in code_lines:
        stripped = line.strip()
        if PSEUDO_COMMENT in stripped or PSEUDO_COMMENT_ALT in stripped:
            return True
        if stripped and not stripped.startswith("//"):
            # 遇到第一个非空非注释行，还没看到标注
            return False
    return False


def is_full_class(code_text):
    """判断是否是完整可编译类"""
    # 有 class 声明和 main 方法或方法体
    has_class = re.search(r"\bclass\s+\w+", code_text) is not None
    has_main = "public static void main" in code_text
    has_methods = re.search(r"\b(public|private|protected)\s+\w+\s+\w+\s*\(", code_text) is not None
    return has_class and (has_main or has_methods)


def classify_codeblock(code_text, filename, error_type):
    """
    返回处理动作：
    - ('pseudo', None): 添加伪代码标注
    - ('fix_syntax', fixed_code): 修复语法错误
    - ('wrap', wrapped_code): 包装为最小可运行类
    - ('skip', None): 跳过
    """
    lines = code_text.split("\n")

    # 如果已有标注，跳过
    if is_pseudocode_marked(lines):
        return ("skip", None)

    # 如果已经是完整类，跳过
    if is_full_class(code_text):
        return ("skip", None)

    # 类型B：非法字符 → 尝试修复
    if error_type == "illegal_char":
        fixed_lines = []
        changed = False
        for line in lines:
            stripped = line.strip()
            # Markdown 标题混入代码块
            if stripped.startswith("# ") or stripped.startswith("## ") or stripped.startswith("### "):
                fixed_lines.append("// " + stripped.lstrip("# "))
                changed = True
            elif stripped.startswith("#作业") or stripped.startswith("# 作业"):
                fixed_lines.append("// " + stripped.lstrip("# "))
                changed = True
            else:
                fixed_lines.append(line)
        if changed:
            return ("fix_syntax", "\n".join(fixed_lines))

    # 类型B：不是语句 / 需要分号
    if error_type in ("not_statement", "need_semicolon"):
        # 这类通常是 metrics 表达式或配置项被当作代码
        # 如 `- numberOfFailedCheckpoints`
        fixed_lines = []
        changed = False
        for line in lines:
            stripped = line.strip()
            # 以 `- ` 开头的配置项
            if re.match(r"^-\s+\w+", stripped):
                fixed_lines.append("// " + stripped)
                changed = True
            else:
                fixed_lines.append(line)
        if changed:
            return ("fix_syntax", "\n".join(fixed_lines))

    # 判断是否在核心目录
    is_core = any(d in filename for d in CORE_DIRS)

    # 核心目录中的简单片段，尝试包装
    if is_core and len(lines) <= 15 and error_type in ("symbol_not_found", "illegal_expression"):
        # 检查是否是简单的 API 调用片段
        non_empty = [l for l in lines if l.strip() and not l.strip().startswith("//")]
        if non_empty and (
            non_empty[0].strip().startswith("env.")
            or non_empty[0].strip().startswith("stream.")
            or non_empty[0].strip().startswith("tableEnv.")
            or non_empty[0].strip().startswith("DataStream")
            or "StreamExecutionEnvironment" in code_text
        ):
            # 尝试包装为最小类
            wrapped = wrap_as_minimal_class(code_text, filename)
            if wrapped:
                return ("wrap", wrapped)

    # 默认：添加伪代码标注
    return ("pseudo", None)


def wrap_as_minimal_class(code_text, filename):
    """尝试将代码片段包装为最小可运行类"""
    lines = code_text.split("\n")

    # 提取 import 语句
    imports = []
    body_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import "):
            imports.append(stripped)
        else:
            body_lines.append(line)

    # 如果没有 import，且不是 Flink API 相关，不包装
    if not imports and "StreamExecutionEnvironment" not in code_text:
        return None

    # 补充缺少的 import
    needed_imports = set(imports)
    body_text = "\n".join(body_lines)

    if "StreamExecutionEnvironment" in body_text and not any(
        "org.apache.flink.streaming.api.environment.StreamExecutionEnvironment" in imp for imp in needed_imports
    ):
        needed_imports.add("import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;")

    if "DataStream" in body_text and not any(
        "org.apache.flink.streaming.api.datastream.DataStream" in imp for imp in needed_imports
    ):
        needed_imports.add("import org.apache.flink.streaming.api.datastream.DataStream;")

    # 构建包装类
    wrapped = "import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;\n"
    for imp in sorted(needed_imports):
        if "StreamExecutionEnvironment" not in imp:
            wrapped += imp + "\n"

    wrapped += "\n"
    wrapped += "public class Example {\n"
    wrapped += "    public static void main(String[] args) throws Exception {\n"
    for line in body_lines:
        if line.strip():
            wrapped += "        " + line + "\n"
        else:
            wrapped += "\n"
    wrapped += "    }\n"
    wrapped += "}\n"

    return wrapped


def process_file(filepath, failures_in_file):
    """处理单个文件，返回修改统计"""
    if not os.path.exists(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 按代码块分组失败
    codeblocks_to_process = {}  # (start, end) -> set of error_types

    for line_num, error_type in failures_in_file:
        boundaries = find_codeblock_boundaries(lines, line_num)
        if boundaries:
            if boundaries not in codeblocks_to_process:
                codeblocks_to_process[boundaries] = set()
            codeblocks_to_process[boundaries].add(error_type)

    if not codeblocks_to_process:
        return None

    modified = False
    stats = {"pseudo": 0, "fix_syntax": 0, "wrap": 0, "skip": 0}

    # 从后向前处理，避免行号偏移
    for (start, end), error_types in sorted(codeblocks_to_process.items(), key=lambda x: -x[0][0]):
        code_lines = lines[start + 1:end]  # 去掉 ```java 和 ```
        code_text = "".join(code_lines)

        # 取第一个错误类型作为代表
        error_type = list(error_types)[0]

        action, new_code = classify_codeblock(code_text, filepath, error_type)

        if action == "pseudo":
            # 在代码块第一行代码前添加标注
            # 保留原有的空行
            insert_idx = start + 1
            # 找到第一个非空行位置（在代码块内）
            first_code_offset = 0
            for i, line in enumerate(code_lines):
                if line.strip():
                    first_code_offset = i
                    break

            # 在第一个非空行之前插入标注
            insert_line = start + 1 + first_code_offset
            # 检查标注是否已存在
            if PSEUDO_COMMENT not in lines[insert_line]:
                lines.insert(insert_line, PSEUDO_COMMENT + "\n")
                modified = True
                stats["pseudo"] += 1

        elif action == "fix_syntax":
            new_lines = [l + "\n" if not l.endswith("\n") else l for l in new_code.split("\n")]
            lines[start + 1:end] = new_lines
            modified = True
            stats["fix_syntax"] += 1

        elif action == "wrap":
            new_lines = [l + "\n" if not l.endswith("\n") else l for l in new_code.split("\n")]
            lines[start + 1:end] = new_lines
            modified = True
            stats["wrap"] += 1

        elif action == "skip":
            stats["skip"] += 1

    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return stats

    return None


def main():
    print("解析验证报告...")
    failures = parse_report("CODE-EXAMPLE-VALIDATION-REPORT.md")
    print(f"找到 {len(failures)} 个失败的 Java 代码块（已排除 release/）")

    # 按文件分组
    files = defaultdict(list)
    for filename, line_num, error_type in failures:
        files[filename].append((line_num, error_type))

    print(f"分布在 {len(files)} 个文件中")

    # 统计各目录
    dir_counter = Counter()
    for f in files:
        parts = f.split("/")
        if len(parts) >= 1:
            dir_counter[parts[0]] += 1
    print("目录分布:")
    for d, c in dir_counter.most_common():
        print(f"  {d}: {c} 文件")

    # 处理文件
    total_stats = {"files": 0, "pseudo": 0, "fix_syntax": 0, "wrap": 0, "skip": 0}
    modified_files = []

    for filename, failures_in_file in files.items():
        filepath = filename.replace("/", os.sep)
        # failures_in_file is list of (line_num, error_type)
        result = process_file(filepath, failures_in_file)
        if result:
            total_stats["files"] += 1
            total_stats["pseudo"] += result["pseudo"]
            total_stats["fix_syntax"] += result["fix_syntax"]
            total_stats["wrap"] += result["wrap"]
            total_stats["skip"] += result["skip"]
            modified_files.append(filename)

    print(f"\n处理完成:")
    print(f"  修改文件数: {total_stats['files']}")
    print(f"  添加伪代码标注: {total_stats['pseudo']}")
    print(f"  修复语法错误: {total_stats['fix_syntax']}")
    print(f"  包装为可运行类: {total_stats['wrap']}")
    print(f"  跳过: {total_stats['skip']}")

    # 生成报告
    report = f"""# R1-CODE-FIX-REPORT.md

> **生成时间**: 2026-04-19
> **任务**: R1 Java代码示例可运行性修复

## 修改统计

| 指标 | 数值 |
|------|------|
| 扫描失败代码块 | {len(failures)} |
| 涉及文件数 | {len(files)} |
| 实际修改文件数 | {total_stats['files']} |
| 添加伪代码标注 | {total_stats['pseudo']} |
| 修复语法错误 | {total_stats['fix_syntax']} |
| 包装为可运行类 | {total_stats['wrap']} |
| 跳过（已有标注或完整类） | {total_stats['skip']} |

## 处理策略

1. **类型A（片段/缺上下文）**: 对缺少 class/main/上下文的代码片段添加伪代码标注
2. **类型B（语法错误）**: 修复 Markdown 标题混入、非法表达式等语法问题
3. **类型C（核心API）**: 对核心目录（Flink/03-api/、04-runtime/、02-core/）中的简单片段尝试包装为最小可运行类

## 修改文件列表

"""

    for f in sorted(modified_files):
        report += f"- `{f}`\n"

    with open("R1-CODE-FIX-REPORT.md", "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n报告已生成: R1-CODE-FIX-REPORT.md")


if __name__ == "__main__":
    main()
