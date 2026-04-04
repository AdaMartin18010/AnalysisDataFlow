# 质量门检查脚本

本目录包含用于检查项目质量的脚本工具。

## check-theorem-registry.py - 定理编号检查脚本

### 功能

1. **扫描所有形式化元素**
   - 定理 (Thm-XXX)
   - 定义 (Def-XXX)
   - 引理 (Lemma-XXX)
   - 命题 (Prop-XXX)
   - 推论 (Cor-XXX)

2. **唯一性检查**
   - 检测重复编号（跨文件定义冲突）
   - 检测同一文件内重复定义

3. **注册表同步检查**
   - 对比 THEOREM-REGISTRY.md
   - 检测未注册的定理
   - 检测已删除但未移除的注册表条目

4. **编号规范检查**
   - 格式: {Type}-{Stage}-{Doc}-{Seq}
   - 阶段标识正确性 (S/K/F)
   - 文档序号连续性

5. **输出报告**
   - 错误列表
   - 修复建议
   - 统计信息
   - 注册表更新补丁

### 使用方法

```bash
# 基本检查
python check-theorem-registry.py

# 生成详细报告
python check-theorem-registry.py --output report.md

# 生成注册表更新补丁
python check-theorem-registry.py --patch patch.md

# 同时生成报告和补丁
python check-theorem-registry.py --output report.md --patch patch.md
```

### 输出文件

- `theorem-check-report.md` - 详细的检查报告
- `registry-patch.md` - 注册表更新补丁（可直接复制到注册表）

### 退出码

- `0` - 检查通过或有警告
- `1` - 发现错误

### 错误类型

| 错误类型 | 描述 | 修复建议 |
|----------|------|----------|
| `duplicate_id` | 跨文件重复定义 | 保留原始文档定义，其他改为引用 |
| `unregistered` | 未在注册表中登记 | 使用补丁文件添加到注册表 |
| `stage_mismatch` | 阶段标识与路径不匹配 | 修正编号中的阶段标识 |
| `invalid_seq` | 顺序号格式错误 | 检查编号格式 |

### 警告类型

| 警告类型 | 描述 | 优先级 |
|----------|------|--------|
| `orphaned_registry_entry` | 注册表中有但文档中无 | 中 |
| `numbering_gap` | 编号不连续 | 低 |
| `duplicate_definition_same_file` | 同一文件中多次定义 | 中 |

### 智能检测

脚本使用启发式规则区分"定义"和"引用"：

**视为定义的情况：**
- 标题行中的编号 (`### Thm-S-01-01`)
- 四级标题定义 (`#### Def-S-01-01: ...`)
- 粗体定义名 (`**Thm-S-01-01**: ...`)
- 数学公式环境中的定义

**视为引用的情况：**
- 包含"见"、"详见"、"参见"等词的文本
- 目录项 (`- [Thm-S-01-01]`)
- 包含"引用"、"依赖"等词的文本

### 统计信息

脚本会输出以下统计：
- 总形式化元素数量
- 定义（非引用）数量
- 按类型分布（定理/定义/引理/命题/推论）
- 按阶段分布（Struct/Knowledge/Flink）
- 错误和警告数量

### 维护

- **版本**: 1.2.0
- **作者**: Agent
- **更新日期**: 2026-04-04
