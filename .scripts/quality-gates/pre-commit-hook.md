# Git Pre-commit Hook 配置指南

本文档介绍如何在本地开发环境和CI/CD流水线中集成文档质量门禁系统。

## 目录

1. [本地Pre-commit Hook配置](#本地pre-commit-hook配置)
2. [CI/CD集成](#cicd集成)
3. [配置选项](#配置选项)
4. [绕过机制](#绕过机制)
5. [故障排除](#故障排除)

---

## 本地Pre-commit Hook配置

### 自动安装

运行提供的安装脚本：

```bash
# Windows PowerShell
.\.scripts\quality-gates\install-hooks.ps1

# Linux/macOS
chmod +x .scripts/quality-gates/install-hooks.sh
./.scripts/quality-gates/install-hooks.sh
```

### 手动配置

#### 1. 创建Pre-commit钩子

在项目根目录创建 `.git/hooks/pre-commit` 文件：

**Windows (pre-commit.bat)**
```batch
@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo Running Document Quality Gates
echo ========================================

set SCRIPT_DIR=.scripts\quality-gates
set ERROR_COUNT=0

:: Run structure validator
echo [1/4] Structure Validation...
python "%SCRIPT_DIR%\structure-validator.py" Struct/ Knowledge/ Flink/ --ci
if %ERRORLEVEL% NEQ 0 set /a ERROR_COUNT+=1

:: Run format checker
echo [2/4] Format Checking...
python "%SCRIPT_DIR%\format-checker.py" Struct/ Knowledge/ Flink/ --ci
if %ERRORLEVEL% NEQ 0 set /a ERROR_COUNT+=1

:: Run reference validator
echo [3/4] Reference Validation...
python "%SCRIPT_DIR%\reference-validator.py" . --ci
if %ERRORLEVEL% NEQ 0 set /a ERROR_COUNT+=1

:: Run content quality checker (non-blocking)
echo [4/4] Content Quality Check...
python "%SCRIPT_DIR%\content-quality-checker.py" Struct/ Knowledge/ Flink/ --ci --threshold 60

if %ERRORCOUNT% GTR 0 (
    echo.
    echo ========================================
    echo Quality checks FAILED: %ERROR_COUNT% errors found
    echo ========================================
    echo.
    echo To bypass quality checks (not recommended):
    echo   git commit --no-verify
    echo.
    exit /b 1
)

echo.
echo ========================================
echo All quality checks passed!
echo ========================================
exit /b 0
```

**Linux/macOS (pre-commit)**
```bash
#!/bin/bash
set -e

echo "========================================"
echo "Running Document Quality Gates"
echo "========================================"

SCRIPT_DIR=".scripts/quality-gates"
ERROR_COUNT=0

# Run structure validator
echo "[1/4] Structure Validation..."
python "$SCRIPT_DIR/structure-validator.py" Struct/ Knowledge/ Flink/ --ci || ((ERROR_COUNT++))

# Run format checker
echo "[2/4] Format Checking..."
python "$SCRIPT_DIR/format-checker.py" Struct/ Knowledge/ Flink/ --ci || ((ERROR_COUNT++))

# Run reference validator
echo "[3/4] Reference Validation..."
python "$SCRIPT_DIR/reference-validator.py" . --ci || ((ERROR_COUNT++))

# Run content quality checker (non-blocking)
echo "[4/4] Content Quality Check..."
python "$SCRIPT_DIR/content-quality-checker.py" Struct/ Knowledge/ Flink/ --ci --threshold 60 || true

if [ $ERROR_COUNT -gt 0 ]; then
    echo ""
    echo "========================================"
    echo "Quality checks FAILED: $ERROR_COUNT errors found"
    echo "========================================"
    echo ""
    echo "To bypass quality checks (not recommended):"
    echo "  git commit --no-verify"
    echo ""
    exit 1
fi

echo ""
echo "========================================"
echo "All quality checks passed!"
echo "========================================"
exit 0
```

#### 2. 设置可执行权限

```bash
# Linux/macOS
chmod +x .git/hooks/pre-commit

# Windows
# 无需特殊权限，确保文件扩展名为 .bat
```

#### 3. 测试钩子

```bash
# 尝试提交一个文件
git add .
git commit -m "Test commit"

# 应该看到质量检查输出
```

---

## CI/CD集成

### GitHub Actions

创建 `.github/workflows/quality-gates.yml`：

```yaml
name: Document Quality Gates

on:
  push:
    branches: [ main, develop ]
    paths:
      - '**.md'
      - '.scripts/quality-gates/**'
  pull_request:
    branches: [ main, develop ]
    paths:
      - '**.md'

jobs:
  quality-check:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      with:
        fetch-depth: 0  # 需要完整历史进行引用验证
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Cache quality results
      uses: actions/cache@v3
      with:
        path: .quality-cache
        key: quality-${{ github.sha }}
        restore-keys: |
          quality-
    
    - name: Run Structure Validator
      run: |
        echo "## Structure Validation" >> $GITHUB_STEP_SUMMARY
        python .scripts/quality-gates/structure-validator.py \
          Struct/ Knowledge/ Flink/ \
          --ci \
          --output .quality-structure.json || true
    
    - name: Run Format Checker
      run: |
        echo "## Format Checking" >> $GITHUB_STEP_SUMMARY
        python .scripts/quality-gates/format-checker.py \
          Struct/ Knowledge/ Flink/ \
          --ci \
          --output .quality-format.json || true
    
    - name: Run Reference Validator
      run: |
        echo "## Reference Validation" >> $GITHUB_STEP_SUMMARY
        python .scripts/quality-gates/reference-validator.py \
          . \
          --ci \
          --output .quality-reference.json || true
    
    - name: Run Content Quality Checker
      run: |
        echo "## Content Quality" >> $GITHUB_STEP_SUMMARY
        python .scripts/quality-gates/content-quality-checker.py \
          Struct/ Knowledge/ Flink/ \
          --ci \
          --threshold 70 \
          --output .quality-content.json || true
    
    - name: Generate Quality Report
      run: |
        python .scripts/quality-gates/quality-report.py \
          --run-all . \
          --format markdown \
          --output quality-report.md \
          --ci
        cat quality-report.md >> $GITHUB_STEP_SUMMARY
    
    - name: Upload Quality Report
      uses: actions/upload-artifact@v4
      if: always()
      with:
        name: quality-report
        path: |
          quality-report.md
          quality-report.html
          .quality-*.json
    
    - name: Check Quality Gate
      run: |
        # 解析质量报告判断是否通过
        python -c "
import json
import sys

with open('.quality-structure.json') as f:
    data = json.load(f)
    errors = data['summary']['error_count']
    if errors > 0:
        print(f'❌ Structure validation failed: {errors} errors')
        sys.exit(1)

with open('.quality-reference.json') as f:
    data = json.load(f)
    errors = data['summary']['error_count']
    if errors > 0:
        print(f'❌ Reference validation failed: {errors} errors')
        sys.exit(1)

print('✅ All quality gates passed')
        "
```

### GitLab CI

创建 `.gitlab-ci.yml`：

```yaml
stages:
  - quality

variables:
  PYTHON_VERSION: "3.11"

.document_quality_template: &document_quality
  image: python:$PYTHON_VERSION
  cache:
    paths:
      - .quality-cache/
  artifacts:
    when: always
    paths:
      - quality-report.md
      - .quality-*.json
    reports:
      junit: quality-junit.xml

structure_validation:
  <<: *document_quality
  stage: quality
  script:
    - python .scripts/quality-gates/structure-validator.py 
        Struct/ Knowledge/ Flink/
        --output .quality-structure.json
  allow_failure: false

format_checking:
  <<: *document_quality
  stage: quality
  script:
    - python .scripts/quality-gates/format-checker.py
        Struct/ Knowledge/ Flink/
        --output .quality-format.json
  allow_failure: true

reference_validation:
  <<: *document_quality
  stage: quality
  script:
    - python .scripts/quality-gates/reference-validator.py
        .
        --output .quality-reference.json
  allow_failure: false

content_quality:
  <<: *document_quality
  stage: quality
  script:
    - python .scripts/quality-gates/content-quality-checker.py
        Struct/ Knowledge/ Flink/
        --threshold 70
        --output .quality-content.json
  allow_failure: true

quality_report:
  <<: *document_quality
  stage: quality
  dependencies:
    - structure_validation
    - format_checking
    - reference_validation
    - content_quality
  script:
    - python .scripts/quality-gates/quality-report.py
        --run-all .
        --format markdown
        --output quality-report.md
```

### Azure DevOps

创建 `azure-pipelines.yml`：

```yaml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - '**.md'
      - '.scripts/quality-gates/**'

pr:
  branches:
    include:
      - main
      - develop

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: UsePythonVersion@0
  inputs:
    versionSpec: '3.11'
  displayName: 'Use Python 3.11'

- script: |
    echo "##vso[task.setvariable variable=quality_gate_passed]true"
  displayName: 'Initialize Quality Gate'

- script: |
    python .scripts/quality-gates/structure-validator.py \
      Struct/ Knowledge/ Flink/ \
      --ci \
      --output .quality-structure.json
    if [ $? -ne 0 ]; then
      echo "##vso[task.setvariable variable=quality_gate_passed]false"
      echo "##vso[task.logissue type=error]Structure validation failed"
    fi
  displayName: 'Structure Validation'
  continueOnError: true

- script: |
    python .scripts/quality-gates/format-checker.py \
      Struct/ Knowledge/ Flink/ \
      --ci \
      --output .quality-format.json
  displayName: 'Format Checking'
  continueOnError: true

- script: |
    python .scripts/quality-gates/reference-validator.py \
      . \
      --ci \
      --output .quality-reference.json
    if [ $? -ne 0 ]; then
      echo "##vso[task.setvariable variable=quality_gate_passed]false"
      echo "##vso[task.logissue type=error]Reference validation failed"
    fi
  displayName: 'Reference Validation'
  continueOnError: true

- script: |
    python .scripts/quality-gates/content-quality-checker.py \
      Struct/ Knowledge/ Flink/ \
      --ci \
      --threshold 70 \
      --output .quality-content.json
  displayName: 'Content Quality Check'
  continueOnError: true

- script: |
    python .scripts/quality-gates/quality-report.py \
      --run-all . \
      --format html \
      --output quality-report.html
  displayName: 'Generate Quality Report'

- task: PublishHtmlReport@1
  inputs:
    reportDir: 'quality-report.html'
    tabName: 'Quality Report'
  condition: always()

- task: PublishBuildArtifacts@1
  inputs:
    pathToPublish: '.'
    artifactName: 'quality-reports'
    storeAsTar: false
  condition: always()

- script: |
    if [ "$(quality_gate_passed)" = "false" ]; then
      echo "Quality gate failed"
      exit 1
    fi
    echo "Quality gate passed"
  displayName: 'Final Quality Gate Check'
```

---

## 配置选项

### 配置文件示例

创建 `.quality-gates.json`：

```json
{
  "structure_validator": {
    "min_sections": 6,
    "strict_mode": false,
    "required_sections": [
      ["概念定义", "Definitions"],
      ["属性推导", "Properties"],
      ["关系建立", "Relations"],
      ["论证过程", "Argumentation"],
      ["形式证明", "Proof"],
      ["工程论证", "Engineering Argument"],
      ["实例验证", "Examples"],
      ["可视化", "Visualizations"],
      ["引用参考", "References"]
    ]
  },
  "format_checker": {
    "check_code_blocks": true,
    "check_tables": true,
    "check_lists": true,
    "check_headers": true,
    "check_punctuation": false,
    "check_whitespace": true,
    "max_line_length": 120
  },
  "reference_validator": {
    "registry_file": "THEOREM-REGISTRY.md",
    "check_external_links": false
  },
  "content_checker": {
    "min_section_content": 50,
    "min_mermaid_count": 1,
    "min_code_examples": 0,
    "min_definitions": 1,
    "quality_threshold": 70.0,
    "key_terms": [
      "Dataflow",
      "Checkpoint",
      "Watermark",
      "Actor",
      "CSP"
    ]
  },
  "report_generator": {
    "quality_threshold": 70,
    "max_errors": 0,
    "max_warnings": 100
  }
}
```

### 目录特定配置

可以为不同目录设置不同规则：

```json
{
  "overrides": [
    {
      "path": "Struct/",
      "config": {
        "content_checker": {
          "quality_threshold": 80,
          "min_definitions": 3
        }
      }
    },
    {
      "path": "Knowledge/",
      "config": {
        "content_checker": {
          "quality_threshold": 65,
          "min_code_examples": 1
        }
      }
    }
  ]
}
```

---

## 绕过机制

### 本地开发绕过

```bash
# 绕过所有pre-commit hooks
git commit --no-verify -m "Your message"
# 或
git commit -n -m "Your message"

# 绕过特定hook（如果配置了多个）
SKIP=quality-gates git commit -m "Your message"
```

### CI/CD绕过

使用特定提交消息标记：

```bash
# 提交消息中包含 [skip-quality] 或 [quality-skip]
git commit -m "Fix urgent bug [skip-quality]"
```

CI配置中检查：

```yaml
# GitHub Actions
- name: Check skip flag
  run: |
    if [[ "${{ github.event.head_commit.message }}" == *"[skip-quality]"* ]]; then
      echo "Quality checks skipped by commit message"
      exit 0
    fi
```

### 条件性绕过

创建 `.quality-skip` 文件临时禁用：

```bash
# 创建跳过标记
touch .quality-skip
git add .
git commit -m "Work in progress"

# 完成后删除标记
rm .quality-skip
git add .
git commit -m "Final version"
```

Pre-commit钩子检查：

```bash
#!/bin/bash
if [ -f ".quality-skip" ]; then
    echo "Quality checks disabled by .quality-skip file"
    exit 0
fi
# ... 继续执行检查
```

---

## 故障排除

### 常见问题

#### 1. Python路径问题

**症状**: `python: command not found`

**解决方案**:
```bash
# 使用完整路径或python3
#!/usr/bin/env python3

# 或在钩子中设置PATH
export PATH="/usr/local/bin:$PATH"
```

#### 2. 权限问题

**症状**: `Permission denied`

**解决方案**:
```bash
# Linux/macOS
chmod +x .git/hooks/pre-commit
chmod +x .scripts/quality-gates/*.py

# Windows
# 检查文件扩展名关联
assoc .py=Python.File
ftype Python.File="C:\Python311\python.exe" "%1" %*
```

#### 3. 编码问题

**症状**: `UnicodeDecodeError`

**解决方案**:
确保所有Python脚本有正确的编码声明：
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```

#### 4. 执行时间过长

**症状**: 提交等待时间过长

**解决方案**:
- 只检查修改的文件
- 使用缓存
- 并行执行检查

```bash
# 优化后的pre-commit钩子
# 只检查暂存区中的markdown文件
STAGED_MD=$(git diff --cached --name-only --diff-filter=ACM | grep '\.md$' || true)
if [ -z "$STAGED_MD" ]; then
    exit 0
fi

# 只检查修改的文件
python .scripts/quality-gates/structure-validator.py $STAGED_MD --ci
```

### 调试模式

启用详细输出：

```bash
# 设置环境变量
export QUALITY_GATES_DEBUG=1

# 手动运行检查
python .scripts/quality-gates/structure-validator.py document.md -v
```

### 获取帮助

```bash
# 查看帮助
python .scripts/quality-gates/structure-validator.py --help
python .scripts/quality-gates/format-checker.py --help
python .scripts/quality-gates/reference-validator.py --help
python .scripts/quality-gates/content-quality-checker.py --help
python .scripts/quality-gates/quality-report.py --help
```

---

## 最佳实践

1. **渐进式采用**: 先在CI中启用，待团队适应后再强制本地pre-commit
2. **配置合理阈值**: 初期可以放宽阈值，逐步收紧
3. **定期审查**: 每月审查质量报告，识别共性问题
4. **团队培训**: 确保团队成员理解质量规则和修复方法
5. **自动化修复**: 对于格式问题，考虑添加自动修复脚本

---

## 附录

### 质量门禁检查清单

- [ ] 文档有正确的六段式结构
- [ ] 包含必要的元信息（所属阶段、前置依赖、形式化等级）
- [ ] 定理/定义编号全局唯一
- [ ] 所有内部链接有效
- [ ] 代码块有正确的语法高亮
- [ ] 表格格式正确
- [ ] 包含至少一个Mermaid可视化
- [ ] 引用格式正确且有定义
- [ ] 内容完整，章节不空

### 快速修复命令

```bash
# 修复行尾空格
find . -name "*.md" -exec sed -i 's/[[:space:]]*$//' {} \;

# 修复Tab缩进
find . -name "*.md" -exec sed -i 's/\t/    /g' {} \;

# 添加缺少的代码块语言
# 需要手动检查和添加
```
