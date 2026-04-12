# 代码质量检查报告

生成时间: 2026-04-12 22:42:14

## 汇总统计

- **总文件数**: 316
- **Python文件**: 242
- **YAML文件**: 46
- **SQL文件**: 28
- **问题文件数**: 273
- **平均分数**: 60.7/100

## 问题统计

- **错误**: 24
- **警告**: 1335
- **建议**: 3466
- **总计**: 4825

## 详细结果

### ❌ .improvement-tracking\scripts\maintenance-report-generator.py

- **文件类型**: python
- **总行数**: 561
- **代码行**: 378
- **注释行**: 50
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第12行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第22行): 函数 'run_script' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第22行): 函数 'run_script' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第50行): 函数 'parse_script_output' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第50行): 函数 'parse_script_output' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第112行): 函数 'count_documents' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第147行): 函数 'count_formal_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第178行): 函数 'calculate_health_score' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第178行): 函数 'calculate_health_score' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第197行): 函数 'generate_maintenance_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第197行): 函数 'generate_maintenance_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第441行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第112行): 'count_documents' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第147行): 'count_formal_elements' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第178行): 'calculate_health_score' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第197行): 'generate_maintenance_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第441行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第60行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第60行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第65行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第65行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第172行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第172行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第73行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第73行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第80行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第80行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第88行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第88行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第93行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第93行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第101行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第101行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第106行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第106行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第50行): 函数 'parse_script_output' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第197行): 函数 'generate_maintenance_report' 过长 (241行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第441行): 函数 'main' 过长 (115行)
  - 建议: 考虑拆分函数

### ❌ .scripts\automation\doc-quality-dashboard.py

- **文件类型**: python
- **总行数**: 974
- **代码行**: 809
- **注释行**: 35
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第884行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第115行): 函数名 '_load_report' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第131行): 函数名 '_calculate_cross_ref_score' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第163行): 函数名 '_calculate_template_score' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第196行): 函数名 '_calculate_formal_element_score' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第227行): 函数名 '_calculate_mermaid_score' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第256行): 函数名 '_calculate_readability_score' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第387行): 函数名 '_load_trends' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第409行): 函数名 '_save_trend' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第439行): 函数名 '_generate_recommendations' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第768行): 函数名 '_get_score_class' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第779行): 函数名 '_get_status_class' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第788行): 函数名 '_get_status_text' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第799行): 函数名 '_generate_metric_items' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第812行): 函数名 '_generate_file_list' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第887行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第37行): 'QualityMetric' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第47行): 'FileQuality' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第58行): 'TrendData' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第68行): 'DashboardData' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第82行): 'QualityDashboardGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第887行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第115行): '_load_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第131行): '_calculate_cross_ref_score' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第163行): '_calculate_template_score' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第196行): '_calculate_formal_element_score' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第309行): 'aggregate_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第387行): '_load_trends' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第439行): '_generate_recommendations' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第479行): 'generate_html_dashboard' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第788行): '_get_status_text' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第799行): '_generate_metric_items' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第417行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第417行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第887行): 函数 'main' 过长 (82行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第256行): 函数 '_calculate_readability_score' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第309行): 函数 'aggregate_data' 过长 (76行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第479行): 函数 'generate_html_dashboard' 过长 (287行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第826行): 函数 'generate_github_actions_output' 过长 (55行)
  - 建议: 考虑拆分函数

### ❌ .scripts\automation\mermaid-syntax-checker.py

- **文件类型**: python
- **总行数**: 900
- **代码行**: 702
- **注释行**: 47
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第23行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第27行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第487行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第243行): 函数名 '_should_skip_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第248行): 函数名 '_detect_diagram_type' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第255行): 函数名 '_extract_direction' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第262行): 函数名 '_parse_flowchart' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第324行): 函数名 '_parse_node_def' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第360行): 函数名 '_parse_edge' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第373行): 函数名 '_parse_sequence_diagram' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第434行): 函数名 '_parse_class_diagram' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第453行): 函数名 '_parse_diagram' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第477行): 函数名 '_check_with_cli' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第799行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第36行): 'DiagramType' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): 'SyntaxErrorType' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第69行): 'SyntaxError' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第79行): 'NodeInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第89行): 'EdgeInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第99行): 'DiagramInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第120行): 'ValidationResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第799行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第248行): '_detect_diagram_type' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第255行): '_extract_direction' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第324行): '_parse_node_def' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第360行): '_parse_edge' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第373行): '_parse_sequence_diagram' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第434行): '_parse_class_diagram' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第453行): '_parse_diagram' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第627行): 'generate_json_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第799行): 函数 'main' 过长 (96行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第262行): 函数 '_parse_flowchart' 过长 (60行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第373行): 函数 '_parse_sequence_diagram' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第668行): 函数 'generate_markdown_report' 过长 (60行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第730行): 函数 'generate_preview_html' 过长 (66行)
  - 建议: 考虑拆分函数

### ❌ .scripts\automation\template-validator.py

- **文件类型**: python
- **总行数**: 867
- **代码行**: 701
- **注释行**: 41
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第26行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第188行): 函数名 '_should_skip_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第193行): 函数名 '_extract_sections' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第229行): 函数名 '_classify_section' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第237行): 函数名 '_extract_formal_elements' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第271行): 函数名 '_count_mermaid_diagrams' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第275行): 函数名 '_check_header_meta' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第284行): 函数名 '_validate_section_completeness' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第330行): 函数名 '_validate_formal_elements' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第408行): 函数名 '_validate_references' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第452行): 函数名 '_validate_mermaid' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第771行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第35行): 'ValidationLevel' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第42行): 'SectionType' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): 'ValidationIssue' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第66行): 'FormalElement' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第78行): 'SectionInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第89行): 'ValidationResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第102行): 'TemplateValidator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第771行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第193行): '_extract_sections' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第229行): '_classify_section' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第237行): '_extract_formal_elements' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第275行): '_check_header_meta' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第284行): '_validate_section_completeness' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第330行): '_validate_formal_elements' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第408行): '_validate_references' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第608行): 'generate_json_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第771行): 函数 'main' 过长 (91行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第330行): 函数 '_validate_formal_elements' 过长 (76行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第452行): 函数 '_validate_mermaid' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第505行): 函数 'validate_file' 过长 (71行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第608行): 函数 'generate_json_report' 过长 (67行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第677行): 函数 'generate_markdown_report' 过长 (91行)
  - 建议: 考虑拆分函数

### ❌ .scripts\benchmarks\flink-benchmark-runner.py

- **文件类型**: python
- **总行数**: 864
- **代码行**: 648
- **注释行**: 69
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第18行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第20行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第22行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第24行): 导入顺序问题: dataclasses
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第27行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第227行): 函数名 '_generate_flink_config' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第242行): 函数名 '_generate_deployment_yaml' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第267行): 函数名 '_wait_for_cluster_ready' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第459行): 函数名 '_run_throughput_test' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第505行): 函数名 '_run_state_access_test' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第545行): 函数名 '_run_checkpoint_test' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第586行): 函数名 '_run_recovery_test' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第607行): 函数名 '_submit_benchmark_job' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第615行): 函数名 '_get_last_checkpoint_duration' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第623行): 函数名 '_inject_failure' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第632行): 函数名 '_wait_for_recovery' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第655行): 函数名 '_generate_markdown_report' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第696行): 函数名 '_generate_html_report' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第779行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第459行): 函数 '_run_throughput_test' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第505行): 函数 '_run_state_access_test' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第545行): 函数 '_run_checkpoint_test' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第586行): 函数 '_run_recovery_test' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第623行): 函数 '_inject_failure' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第711行): 函数 'save_results' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第77行): 'TestType' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第85行): 'TestStatus' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第95行): 'BenchmarkResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第139行): 'TestConfig' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第154行): 'setup_logging' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第300行): 'MetricsCollector' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第779行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第122行): 'duration_sec' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第128行): 'to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第184行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第194行): 'create_namespace' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第267行): '_wait_for_cluster_ready' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第280行): 'cleanup_cluster' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第290行): 'get_pod_logs' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第303行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第322行): 'collect_throughput_metrics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第337行): 'collect_latency_metrics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第349行): 'collect_resource_metrics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第373行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第385行): 'run_all_benchmarks' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第400行): 'run_test' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第438行): 'run_throughput_test' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第459行): '_run_throughput_test' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第484行): 'run_state_access_test' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第565行): 'run_recovery_test' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第586行): '_run_recovery_test' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第623行): '_inject_failure' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第632行): '_wait_for_recovery' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第641行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第711行): 'save_results' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第779行): 函数 'main' 过长 (80行)
  - 建议: 考虑拆分函数

### ❌ .scripts\code-quality-checker.py

- **文件类型**: python
- **总行数**: 715
- **代码行**: 570
- **注释行**: 40
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第20行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第183行): 函数名 '_check_python_header' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第209行): 函数名 '_check_import_order' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第238行): 函数名 '_check_naming_conventions' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第270行): 函数名 '_check_type_hints' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第307行): 函数名 '_check_docstrings' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第332行): 函数名 '_check_exception_handling' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第360行): 函数名 '_check_complexity' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第377行): 函数名 '_calculate_score' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第656行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第183行): 函数 '_check_python_header' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第209行): 函数 '_check_import_order' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第238行): 函数 '_check_naming_conventions' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第270行): 函数 '_check_type_hints' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第307行): 函数 '_check_docstrings' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第332行): 函数 '_check_exception_handling' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第360行): 函数 '_check_complexity' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第377行): 函数 '_calculate_score' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第568行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第637行): 函数 'generate_json_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第31行): 'QualityIssue' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第42行): 'FileQualityReport' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): 'QualitySummary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第70行): 'CodeQualityChecker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第656行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第79行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第209行): '_check_import_order' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第238行): '_check_naming_conventions' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第270行): '_check_type_hints' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第307行): '_check_docstrings' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第332行): '_check_exception_handling' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第360行): '_check_complexity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第377行): '_calculate_score' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第458行): 'check_sql_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第523行): 'run_checks' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第407行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第656行): 函数 'main' 过长 (54行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第112行): 函数 'check_python_file' 过长 (69行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第391行): 函数 'check_yaml_file' 过长 (65行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第458行): 函数 'check_sql_file' 过长 (63行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第568行): 函数 'generate_markdown_report' 过长 (67行)
  - 建议: 考虑拆分函数

### ❌ .scripts\document-quality-auditor.py

- **文件类型**: python
- **总行数**: 854
- **代码行**: 649
- **注释行**: 64
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第23行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第314行): 函数名 '_create_error_result' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第362行): 函数名 '_check_sections' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第369行): 函数名 '_check_formalization' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第388行): 函数名 '_check_mermaid' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第421行): 函数名 '_check_references' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第441行): 函数名 '_check_code_examples' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第451行): 函数名 '_check_images' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第476行): 函数名 '_check_tables' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第493行): 函数名 '_check_meta_info' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第501行): 函数名 '_calculate_score' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第548行): 函数名 '_collect_issues' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第649行): 函数名 '_generate_report' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第663行): 函数名 '_generate_summary' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第684行): 函数名 '_check_theorem_continuity' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第712行): 函数名 '_generate_issue_summary' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第732行): 函数名 '_generate_score_distribution' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第757行): 函数名 '_generate_document_breakdown' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第802行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第776行): 函数 'save_results' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第32行): 'DocumentQualityScore' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第53行): 'QualityIssue' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第64行): 'DocumentAuditResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第120行): 'DocumentQualityAuditor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第802行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第41行): FunctionDef 'total' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第164行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第205行): 'detect_doc_type' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第219行): 'audit_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第314行): '_create_error_result' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第362行): '_check_sections' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第369行): '_check_formalization' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第421行): '_check_references' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第441行): '_check_code_examples' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第451行): '_check_images' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第476行): '_check_tables' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第493行): '_check_meta_info' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第501行): '_calculate_score' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第548行): '_collect_issues' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第617行): 'run_audit' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第649行): '_generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第663行): '_generate_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第684行): '_check_theorem_continuity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第712行): '_generate_issue_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第732行): '_generate_score_distribution' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第757行): '_generate_document_breakdown' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第776行): 'save_results' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第696行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第219行): 函数 'audit_document' 过长 (93行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第548行): 函数 '_collect_issues' 过长 (67行)
  - 建议: 考虑拆分函数

### ❌ .scripts\kg-v2\implicit-relation-miner.py

- **文件类型**: python
- **总行数**: 733
- **代码行**: 529
- **注释行**: 55
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第24行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第248行): 函数名 '_extract_node_features' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第280行): 函数名 '_create_sample_graph' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第425行): 函数名 '_sample_negative_edges' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第488行): 函数名 '_discover_by_structural_similarity' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第533行): 函数名 '_infer_relation_type' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第588行): 函数名 '_heuristic_predict' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第645行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第137行): 函数 'encode' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第137行): 函数 'encode' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第147行): 函数 'decode' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第147行): 函数 'decode' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第153行): 函数 'forward' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第153行): 函数 'forward' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第182行): 函数 'encode' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第182行): 函数 'encode' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第188行): 函数 'decode' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第188行): 函数 'decode' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第361行): 函数 'train_gnn' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第613行): 函数 'save_results' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第84行): 'RelationPrediction' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第94行): 'ImplicitRelation' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第108行): 'GCNLinkPredictor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第198行): 'KnowledgeGraphLoader' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第351行): 'ImplicitRelationMiner' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第645行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第111行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第137行): 'encode' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第147行): 'decode' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第153行): FunctionDef 'forward' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第161行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第182行): FunctionDef 'encode' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第188行): FunctionDef 'decode' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第201行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第209行): 'load' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第248行): '_extract_node_features' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第280行): '_create_sample_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第354行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第361行): 'train_gnn' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第425行): '_sample_negative_edges' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第613行): 'save_results' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第645行): 函数 'main' 过长 (83行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第361行): 函数 'train_gnn' 过长 (62行)
  - 建议: 考虑拆分函数

### ❌ .scripts\knowledge-graph\knowledge-search-engine.py

- **文件类型**: python
- **总行数**: 940
- **代码行**: 723
- **注释行**: 45
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第16行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第104行): 函数名 '_init_whoosh' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第220行): 函数名 '_determine_doc_type' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第233行): 函数名 '_update_inverted_index' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第334行): 函数名 '_search_whoosh' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第374行): 函数名 '_search_inverted_index' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第583行): 函数名 '_show_help' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第599行): 函数名 '_display_results' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第708行): 函数名 '_setup_routes' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第874行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第104行): 函数 '_init_whoosh' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第129行): 函数 'load_bert_model' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第233行): 函数 '_update_inverted_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第243行): 函数 'index_directory' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第261行): 函数 'save_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第518行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第583行): 函数 '_show_help' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第599行): 函数 '_display_results' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第708行): 函数 '_setup_routes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第770行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第795行): 函数 'build_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第832行): 函数 'run_cli' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第840行): 函数 'run_web' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第711行): 函数 'index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第716行): 函数 'search' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第746行): 函数 'api_search' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第60行): 'SearchResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第80行): 'DocumentIndexer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第316行): 'SearchEngine' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第512行): 'CLISearch' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第783行): 'KnowledgeSearchSystem' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第849行): 'load_config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第874行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第69行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第86行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第157行): 'extract_formal_ids' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第161行): 'index_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第220行): '_determine_doc_type' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第233行): '_update_inverted_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第243行): 'index_directory' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第261行): 'save_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第283行): 'load_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第319行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第322行): 'search_fulltext' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第374行): '_search_inverted_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第480行): 'search_by_formal_id' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第494行): 'generate_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第515行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第518行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第583行): '_show_help' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第599行): '_display_results' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第699行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第708行): '_setup_routes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第770行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第786行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第795行): 'build_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第820行): 'load_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第832行): 'run_cli' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第840行): 'run_web' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第711行): FunctionDef 'index' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第716行): FunctionDef 'search' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第746行): FunctionDef 'api_search' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第874行): 函数 'main' 过长 (61行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第161行): 函数 'index_document' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第518行): 函数 'run' 过长 (63行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第708行): 函数 '_setup_routes' 过长 (60行)
  - 建议: 考虑拆分函数

### ❌ .scripts\relationship-query-tool.py

- **文件类型**: python
- **总行数**: 801
- **代码行**: 631
- **注释行**: 24
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第25行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第142行): 函数名 '_build_indices' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第274行): 函数名 '_dijkstra' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第335行): 函数名 '_bfs_path' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第529行): 函数名 '_find_critical_paths' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第553行): 函数名 '_generate_html' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第625行): 函数 'print_results' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第647行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第57行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第64行): 函数 '**hash**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第67行): 函数 '**eq**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第67行): 函数 '**eq**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第83行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第90行): 函数 '**repr**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第142行): 函数 '_build_indices' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第544行): 函数 'export_html' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第380行): 函数 'dfs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第34行): 'RelationType' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第47行): 'Node' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第74行): 'Edge' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第625行): 'print_results' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第647行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第57行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第61行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第64行): FunctionDef '**hash**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第67行): FunctionDef '**eq**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第83行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第87行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第90行): FunctionDef '**repr**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第97行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第142行): '_build_indices' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第529行): '_find_critical_paths' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第553行): '_generate_html' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第380行): FunctionDef 'dfs' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第647行): 函数 'main' 过长 (149行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第274行): 函数 '_dijkstra' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第362行): 函数 'find_all_paths' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第553行): 函数 '_generate_html' 过长 (69行)
  - 建议: 考虑拆分函数

### ❌ CONFIG-TEMPLATES\testing\test-data-generator.py

- **文件类型**: python
- **总行数**: 637
- **代码行**: 466
- **注释行**: 55
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第17行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第308行): 函数名 '_open_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第472行): 函数名 '_print_stats' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第495行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第308行): 函数 '_open_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第472行): 函数 '_print_stats' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第480行): 函数 'stop' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第29行): 'UserEvent' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第46行): 'Transaction' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第63行): 'SensorReading' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第79行): 'LogEntry' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第100行): 'DataGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第136行): 'UserEventGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第158行): 'TransactionGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第187行): 'SensorReadingGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第214行): 'LogEntryGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第295行): 'FileSender' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第495行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第41行): FunctionDef 'to_json' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第58行): FunctionDef 'to_json' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第74行): FunctionDef 'to_json' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第92行): FunctionDef 'to_json' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第103行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第112行): 'generate_user_id' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第116行): 'generate_session_id' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第120行): 'generate_ip' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第124行): 'generate_timestamp' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第144行): FunctionDef 'generate' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第165行): FunctionDef 'generate' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第199行): FunctionDef 'generate' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第227行): FunctionDef 'generate' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第251行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第256行): AsyncFunctionDef 'connect' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第264行): AsyncFunctionDef 'send' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第267行): AsyncFunctionDef 'close' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第275行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第280行): AsyncFunctionDef 'connect' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第284行): AsyncFunctionDef 'send' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第289行): AsyncFunctionDef 'close' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第298行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第305行): AsyncFunctionDef 'connect' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第308行): FunctionDef '_open_file' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第316行): AsyncFunctionDef 'send' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第325行): AsyncFunctionDef 'close' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第333行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第339行): AsyncFunctionDef 'connect' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第342行): AsyncFunctionDef 'send' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第347行): AsyncFunctionDef '_flush' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第356行): AsyncFunctionDef 'close' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第383行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第433行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第472行): '_print_stats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第480行): 'stop' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第484行): 'cleanup' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第597行): AsyncFunctionDef 'run_with_timeout' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第495行): 函数 'main' 过长 (123行)
  - 建议: 考虑拆分函数

### ❌ Flink-IoT-Authority-Alignment\Phase-1-Architecture\project-skeleton\mock-data\sensor-generator.py

- **文件类型**: python
- **总行数**: 670
- **代码行**: 512
- **注释行**: 36
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第21行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第77行): 函数名 '_generate_default_devices' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第202行): 函数名 '_generate_temperature_data' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第226行): 函数名 '_generate_pressure_data' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第241行): 函数名 '_generate_humidity_data' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第257行): 函数名 '_generate_multi_sensor_data' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第274行): 函数名 '_generate_smart_meter_data' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第329行): 函数名 '_on_mqtt_connect' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第336行): 函数名 '_on_mqtt_publish' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第463行): 函数名 '_signal_handler' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第600行): 函数名 '_publish_reading' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第620行): 函数名 '_publish_device_event' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第630行): 函数名 '_print_stats' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第656行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第61行): 函数 'load_registry' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第77行): 函数 '_generate_default_devices' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第329行): 函数 '_on_mqtt_connect' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第329行): 函数 '_on_mqtt_connect' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第336行): 函数 '_on_mqtt_publish' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第336行): 函数 '_on_mqtt_publish' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第340行): 函数 'publish_to_kafka' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第353行): 函数 'publish_to_mqtt' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第367行): 函数 'publish_to_console' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第377行): 函数 'close' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第463行): 函数 '_signal_handler' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第463行): 函数 '_signal_handler' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第468行): 函数 'initialize' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第506行): 函数 'run_realtime_mode' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第560行): 函数 'run_batch_mode' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第600行): 函数 '_publish_reading' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第620行): 函数 '_publish_device_event' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第630行): 函数 '_print_stats' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第641行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第51行): 'DeviceRegistry' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第109行): 'SensorDataGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第426行): 'SensorSimulator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第656行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第54行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第61行): 'load_registry' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第97行): 'get_active_devices' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第101行): 'get_device_by_id' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第144行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第226行): '_generate_pressure_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第241行): '_generate_humidity_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第257行): '_generate_multi_sensor_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第274行): '_generate_smart_meter_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第296行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第329行): '_on_mqtt_connect' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第336行): '_on_mqtt_publish' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第340行): 'publish_to_kafka' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第353行): 'publish_to_mqtt' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第373行): 'get_stats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第377行): 'close' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第393行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第429行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第463行): '_signal_handler' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第468行): 'initialize' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第506行): 'run_realtime_mode' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第560行): 'run_batch_mode' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第620行): '_publish_device_event' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第630行): '_print_stats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第641行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第148行): 函数 'generate_reading' 过长 (52行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第506行): 函数 'run_realtime_mode' 过长 (52行)
  - 建议: 考虑拆分函数

### ❌ formal-methods\.scripts\concept-lineage.py

- **文件类型**: python
- **总行数**: 1150
- **代码行**: 863
- **注释行**: 84
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第24行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第29行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第244行): 函数名 '_should_ignore' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第252行): 函数名 '_process_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第270行): 函数名 '_extract_concepts' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第329行): 函数名 '_extract_relations' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第356行): 函数名 '_categorize_concept' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第375行): 函数名 '_extract_year' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第407行): 函数名 '_determine_relation_type' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第423行): 函数名 '_build_hierarchies' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第454行): 函数名 '_calculate_hierarchy_level' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第472行): 函数名 '_build_timeline' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第505行): 函数名 '_update_statistics' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **short_docstring** (第126行): 'Concept' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第147行): 'TimelineEvent' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第158行): 'ConceptHierarchy' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第166行): 'LineageResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第735行): 'JSONExporter' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第807行): 'ReportGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1036行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第142行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第193行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第252行): '_process_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第270行): '_extract_concepts' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第329行): '_extract_relations' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第356行): '_categorize_concept' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第375行): '_extract_year' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第407行): '_determine_relation_type' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第423行): '_build_hierarchies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第454行): '_calculate_hierarchy_level' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第472行): '_build_timeline' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第505行): '_update_statistics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第536行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第738行): 'export_full_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第780行): 'export_category_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第810行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第919行): 'generate_console_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第957行): 函数 'create_argument_parser' 过长 (76行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第1036行): 函数 'main' 过长 (109行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第270行): 函数 '_extract_concepts' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第662行): 函数 'generate_focused_lineage' 过长 (66行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第815行): 函数 'generate_markdown_report' 过长 (102行)
  - 建议: 考虑拆分函数

### ❌ formal-methods\.scripts\doc-code-consistency.py

- **文件类型**: python
- **总行数**: 976
- **代码行**: 745
- **注释行**: 72
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第20行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第22行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第27行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第227行): 函数名 '_scan_documents' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第240行): 函数名 '_process_doc_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第269行): 函数名 '_parse_doc_reference' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第313行): 函数名 '_scan_lean_code' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第325行): 函数名 '_process_lean_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第367行): 函数名 '_extract_lean_docstrings' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第392行): 函数名 '_find_nearby_docstring' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第414行): 函数名 '_check_consistency' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第463行): 函数名 '_find_matching_implementations' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第508行): 函数名 '_update_statistics' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第527行): 函数名 '_should_ignore' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **short_docstring** (第83行): 'Severity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第91行): 'DocReference' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第126行): 'ConsistencyResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第153行): 'CheckerConfig' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第508行): '_update_statistics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第579行): FunctionDef 'serialize_mapping' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第602行): FunctionDef 'serialize_impl' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第833行): 函数 'create_argument_parser' 过长 (71行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第907行): 函数 'main' 过长 (60行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第572行): 函数 'generate_json_report' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第631行): 函数 'generate_markdown_report' 过长 (117行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第750行): 函数 'generate_console_report' 过长 (76行)
  - 建议: 考虑拆分函数

### ❌ formal-methods\.scripts\link-checker.py

- **文件类型**: python
- **总行数**: 1282
- **代码行**: 996
- **注释行**: 76
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第20行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第26行): 导入顺序问题: dataclasses
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第28行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第190行): 函数名 '_load_from_env' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第361行): 函数名 '_should_ignore' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第368行): 函数名 '_create_link_info' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第589行): 函数名 '_sync_check_with_requests' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第698行): 函数名 '_get_file_headers' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第731行): 函数名 '_header_to_anchor' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第1148行): 函数名 'setUp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第1191行): 函数名 'setUp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第1148行): 函数 'setUp' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1152行): 函数 'test_parse_inline_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1160行): 函数 'test_parse_image_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1170行): 函数 'test_create_link_info' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1180行): 函数 'test_should_ignore' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1191行): 函数 'setUp' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1195行): 函数 'test_ok_status_codes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1201行): 函数 'test_header_to_anchor_edge_cases' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1217行): 函数 'test_default_config' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1226行): 函数 'test_config_from_env' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1243行): 函数 'test_empty_result' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1249行): 函数 'test_add_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1265行): 函数 'test_to_dict' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第46行): 'LinkType' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): 'LinkStatus' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第66行): 'LinkInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第100行): 'CheckResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第150行): 'Config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第251行): 'Colors' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第425行): 'LinkChecker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第747行): 'ReportGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第917行): 'create_default_config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第952行): 'parse_arguments' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1051行): 'main_async' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1131行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1145行): 'TestLinkParser' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1188行): 'TestLinkChecker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1214行): 'TestConfig' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1240行): 'TestCheckResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第81行): 'to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第111行): 'success_rate' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第117行): 'add_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第133行): 'to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第173行): '**init**' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第190行): '_load_from_env' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第206行): FunctionDef 'timeout' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第210行): FunctionDef 'max_workers' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第214行): FunctionDef 'retry_count' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第218行): FunctionDef 'retry_delay' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第222行): FunctionDef 'ignore_patterns' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第227行): FunctionDef 'ignore_external' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第231行): FunctionDef 'ignore_anchors' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第235行): FunctionDef 'json_report' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第239行): FunctionDef 'markdown_report' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第243行): FunctionDef 'verbose' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第247行): FunctionDef 'color' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第263行): 'disable' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第299行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第368行): '_create_link_info' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第431行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第479行): 'check_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第500行): '_check_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第525行): '_check_external_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第620行): '_check_internal_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第750行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第859行): 'print_console_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第1148行): FunctionDef 'setUp' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第1152行): 'test_parse_inline_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1160行): 'test_parse_image_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1170行): 'test_create_link_info' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1180行): 'test_should_ignore' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第1191行): FunctionDef 'setUp' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第1195行): 'test_ok_status_codes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1217行): 'test_default_config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1243行): 'test_empty_result' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1249行): 'test_add_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1265行): 'test_to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第725行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第952行): 函数 'parse_arguments' 过长 (95行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第302行): 函数 'parse_file' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第368行): 函数 '_create_link_info' 过长 (53行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第758行): 函数 'generate_markdown_report' 过长 (98行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第859行): 函数 'print_console_summary' 过长 (55行)
  - 建议: 考虑拆分函数

### ❌ formal-methods\.scripts\mermaid-validator.py

- **文件类型**: python
- **总行数**: 1075
- **代码行**: 828
- **注释行**: 63
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第32行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第38行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第296行): 函数名 '_validate_block' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第331行): 函数名 '_detect_diagram_type' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第358行): 函数名 '_validate_flowchart' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第405行): 函数名 '_check_flowchart_line' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第423行): 函数名 '_validate_arrow_syntax' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第444行): 函数名 '_check_unquoted_chinese' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第469行): 函数名 '_check_bracket_balance' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第490行): 函数名 '_check_chinese_punctuation' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第504行): 函数名 '_validate_sequence_diagram' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第535行): 函数名 '_validate_declaration_diagram' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第542行): 函数名 '_validate_state_diagram' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第579行): 函数名 '_validate_generic' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第624行): 函数名 '_color' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第712行): 函数名 '_get_timestamp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第782行): 函数名 '_get_timestamp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第852行): 函数名 '_get_timestamp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_docstring** (第621行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第862行): 函数 'create_argument_parser' 过长 (84行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第995行): 函数 'main' 过长 (75行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第241行): 函数 'validate_file' 过长 (53行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第630行): 函数 'generate' 过长 (80行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第721行): 函数 'generate' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第791行): 函数 'generate' 过长 (59行)
  - 建议: 考虑拆分函数

### ❌ formal-methods\.scripts\theorem-validator.py

- **文件类型**: python
- **总行数**: 1103
- **代码行**: 855
- **注释行**: 69
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第24行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第29行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第229行): 函数名 '_should_ignore' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第253行): 函数名 '_process_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第293行): 函数名 '_parse_element' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第337行): 函数名 '_check_invalid_formats' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第375行): 函数名 '_detect_duplicates' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第400行): 函数名 '_detect_missing_numbers' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第452行): 函数名 '_validate_cross_references' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第492行): 函数名 '_update_statistics' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **short_docstring** (第79行): 'Severity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第86行): 'ValidationError' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第97行): 'FormalElement' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第110行): 'ValidationResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第132行): 'ValidatorConfig' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第744行): 函数 'create_argument_parser' 过长 (109行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第885行): 函数 'main' 过长 (72行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第1010行): 函数 'pre_commit_hook' 过长 (80行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第172行): 函数 'scan_directory' 过长 (55行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第536行): 函数 'generate_console_report' 过长 (84行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第622行): 函数 'generate_json_report' 过长 (52行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第676行): 函数 'generate_markdown_report' 过长 (61行)
  - 建议: 考虑拆分函数

### ❌ neo4j\simulate_deployment.py

- **文件类型**: python
- **总行数**: 478
- **代码行**: 368
- **注释行**: 27
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **naming_convention** (第60行): 函数名 '_dfs_path' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第100行): 函数名 '_group_by_stage' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第108行): 函数名 '_group_by_formal_level' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第457行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第21行): 函数 'create_node' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第21行): 函数 'create_node' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第33行): 函数 'create_edge' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第33行): 函数 'create_edge' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第41行): 函数 'query_nodes' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第41行): 函数 'query_nodes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第47行): 函数 'query_edges' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第47行): 函数 'query_edges' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第53行): 函数 'match_path' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第53行): 函数 'match_path' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第60行): 函数 '_dfs_path' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第60行): 函数 '_dfs_path' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第73行): 函数 'get_isolated_nodes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第81行): 函数 'search_by_name' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第81行): 函数 'search_by_name' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第90行): 函数 'get_stats' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第100行): 函数 '_group_by_stage' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第108行): 函数 '_group_by_formal_level' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第120行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_type_hints** (第131行): 函数 'log_step' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第131行): 函数 'log_step' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第142行): 函数 'simulate_step1_load_schema' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第158行): 函数 'simulate_step2_import_nodes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第184行): 函数 'simulate_step3_import_edges' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第234行): 函数 'run_query_1_total_nodes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第246行): 函数 'run_query_2_total_relations' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第258行): 函数 'run_query_3_checkpoint_nodes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第273行): 函数 'run_query_4_dependency_paths' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第288行): 函数 'run_query_5_isolated_nodes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第299行): 函数 'run_query_6_by_formal_level' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第309行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第417行): 函数 'run_all' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第117行): 'DeploymentSimulator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第457行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第16行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第21行): 'create_node' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第33行): 'create_edge' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第41行): 'query_nodes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第47行): 'query_edges' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第53行): 'match_path' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第60行): '_dfs_path' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第73行): 'get_isolated_nodes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第81行): 'search_by_name' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第90行): 'get_stats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第100行): '_group_by_stage' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第108行): '_group_by_formal_level' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第120行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第131行): 'log_step' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第158行): 'simulate_step2_import_nodes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第184行): 'simulate_step3_import_edges' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第234行): 'run_query_1_total_nodes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第246行): 'run_query_2_total_relations' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第273行): 'run_query_4_dependency_paths' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第288行): 'run_query_5_isolated_nodes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第309行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第417行): 'run_all' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第309行): 函数 'generate_report' 过长 (106行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\docs\formal-methods\.scripts\concept-lineage.py

- **文件类型**: python
- **总行数**: 1150
- **代码行**: 863
- **注释行**: 84
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第24行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第29行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第244行): 函数名 '_should_ignore' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第252行): 函数名 '_process_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第270行): 函数名 '_extract_concepts' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第329行): 函数名 '_extract_relations' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第356行): 函数名 '_categorize_concept' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第375行): 函数名 '_extract_year' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第407行): 函数名 '_determine_relation_type' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第423行): 函数名 '_build_hierarchies' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第454行): 函数名 '_calculate_hierarchy_level' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第472行): 函数名 '_build_timeline' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第505行): 函数名 '_update_statistics' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **short_docstring** (第126行): 'Concept' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第147行): 'TimelineEvent' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第158行): 'ConceptHierarchy' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第166行): 'LineageResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第735行): 'JSONExporter' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第807行): 'ReportGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1036行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第142行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第193行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第252行): '_process_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第270行): '_extract_concepts' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第329行): '_extract_relations' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第356行): '_categorize_concept' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第375行): '_extract_year' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第407行): '_determine_relation_type' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第423行): '_build_hierarchies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第454行): '_calculate_hierarchy_level' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第472行): '_build_timeline' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第505行): '_update_statistics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第536行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第738行): 'export_full_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第780行): 'export_category_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第810行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第919行): 'generate_console_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第957行): 函数 'create_argument_parser' 过长 (76行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第1036行): 函数 'main' 过长 (109行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第270行): 函数 '_extract_concepts' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第662行): 函数 'generate_focused_lineage' 过长 (66行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第815行): 函数 'generate_markdown_report' 过长 (102行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\docs\formal-methods\.scripts\doc-code-consistency.py

- **文件类型**: python
- **总行数**: 976
- **代码行**: 745
- **注释行**: 72
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第20行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第22行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第27行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第227行): 函数名 '_scan_documents' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第240行): 函数名 '_process_doc_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第269行): 函数名 '_parse_doc_reference' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第313行): 函数名 '_scan_lean_code' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第325行): 函数名 '_process_lean_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第367行): 函数名 '_extract_lean_docstrings' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第392行): 函数名 '_find_nearby_docstring' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第414行): 函数名 '_check_consistency' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第463行): 函数名 '_find_matching_implementations' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第508行): 函数名 '_update_statistics' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第527行): 函数名 '_should_ignore' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **short_docstring** (第83行): 'Severity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第91行): 'DocReference' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第126行): 'ConsistencyResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第153行): 'CheckerConfig' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第508行): '_update_statistics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第579行): FunctionDef 'serialize_mapping' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第602行): FunctionDef 'serialize_impl' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第833行): 函数 'create_argument_parser' 过长 (71行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第907行): 函数 'main' 过长 (60行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第572行): 函数 'generate_json_report' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第631行): 函数 'generate_markdown_report' 过长 (117行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第750行): 函数 'generate_console_report' 过长 (76行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\docs\formal-methods\.scripts\link-checker.py

- **文件类型**: python
- **总行数**: 1282
- **代码行**: 996
- **注释行**: 76
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第20行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第26行): 导入顺序问题: dataclasses
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第28行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第190行): 函数名 '_load_from_env' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第361行): 函数名 '_should_ignore' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第368行): 函数名 '_create_link_info' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第589行): 函数名 '_sync_check_with_requests' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第698行): 函数名 '_get_file_headers' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第731行): 函数名 '_header_to_anchor' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第1148行): 函数名 'setUp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第1191行): 函数名 'setUp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第1148行): 函数 'setUp' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1152行): 函数 'test_parse_inline_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1160行): 函数 'test_parse_image_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1170行): 函数 'test_create_link_info' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1180行): 函数 'test_should_ignore' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1191行): 函数 'setUp' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1195行): 函数 'test_ok_status_codes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1201行): 函数 'test_header_to_anchor_edge_cases' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1217行): 函数 'test_default_config' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1226行): 函数 'test_config_from_env' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1243行): 函数 'test_empty_result' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1249行): 函数 'test_add_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1265行): 函数 'test_to_dict' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第46行): 'LinkType' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): 'LinkStatus' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第66行): 'LinkInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第100行): 'CheckResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第150行): 'Config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第251行): 'Colors' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第425行): 'LinkChecker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第747行): 'ReportGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第917行): 'create_default_config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第952行): 'parse_arguments' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1051行): 'main_async' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1131行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1145行): 'TestLinkParser' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1188行): 'TestLinkChecker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1214行): 'TestConfig' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1240行): 'TestCheckResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第81行): 'to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第111行): 'success_rate' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第117行): 'add_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第133行): 'to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第173行): '**init**' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第190行): '_load_from_env' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第206行): FunctionDef 'timeout' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第210行): FunctionDef 'max_workers' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第214行): FunctionDef 'retry_count' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第218行): FunctionDef 'retry_delay' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第222行): FunctionDef 'ignore_patterns' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第227行): FunctionDef 'ignore_external' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第231行): FunctionDef 'ignore_anchors' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第235行): FunctionDef 'json_report' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第239行): FunctionDef 'markdown_report' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第243行): FunctionDef 'verbose' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第247行): FunctionDef 'color' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第263行): 'disable' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第299行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第368行): '_create_link_info' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第431行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第479行): 'check_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第500行): '_check_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第525行): '_check_external_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第620行): '_check_internal_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第750行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第859行): 'print_console_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第1148行): FunctionDef 'setUp' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第1152行): 'test_parse_inline_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1160行): 'test_parse_image_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1170行): 'test_create_link_info' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1180行): 'test_should_ignore' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第1191行): FunctionDef 'setUp' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第1195行): 'test_ok_status_codes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1217行): 'test_default_config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1243行): 'test_empty_result' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1249行): 'test_add_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1265行): 'test_to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第725行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第952行): 函数 'parse_arguments' 过长 (95行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第302行): 函数 'parse_file' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第368行): 函数 '_create_link_info' 过长 (53行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第758行): 函数 'generate_markdown_report' 过长 (98行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第859行): 函数 'print_console_summary' 过长 (55行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\docs\formal-methods\.scripts\mermaid-validator.py

- **文件类型**: python
- **总行数**: 1075
- **代码行**: 828
- **注释行**: 63
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第32行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第38行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第296行): 函数名 '_validate_block' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第331行): 函数名 '_detect_diagram_type' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第358行): 函数名 '_validate_flowchart' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第405行): 函数名 '_check_flowchart_line' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第423行): 函数名 '_validate_arrow_syntax' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第444行): 函数名 '_check_unquoted_chinese' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第469行): 函数名 '_check_bracket_balance' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第490行): 函数名 '_check_chinese_punctuation' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第504行): 函数名 '_validate_sequence_diagram' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第535行): 函数名 '_validate_declaration_diagram' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第542行): 函数名 '_validate_state_diagram' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第579行): 函数名 '_validate_generic' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第624行): 函数名 '_color' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第712行): 函数名 '_get_timestamp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第782行): 函数名 '_get_timestamp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第852行): 函数名 '_get_timestamp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_docstring** (第621行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第862行): 函数 'create_argument_parser' 过长 (84行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第995行): 函数 'main' 过长 (75行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第241行): 函数 'validate_file' 过长 (53行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第630行): 函数 'generate' 过长 (80行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第721行): 函数 'generate' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第791行): 函数 'generate' 过长 (59行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\docs\formal-methods\.scripts\theorem-validator.py

- **文件类型**: python
- **总行数**: 1103
- **代码行**: 855
- **注释行**: 69
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第24行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第29行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第229行): 函数名 '_should_ignore' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第253行): 函数名 '_process_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第293行): 函数名 '_parse_element' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第337行): 函数名 '_check_invalid_formats' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第375行): 函数名 '_detect_duplicates' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第400行): 函数名 '_detect_missing_numbers' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第452行): 函数名 '_validate_cross_references' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第492行): 函数名 '_update_statistics' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **short_docstring** (第79行): 'Severity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第86行): 'ValidationError' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第97行): 'FormalElement' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第110行): 'ValidationResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第132行): 'ValidatorConfig' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第744行): 函数 'create_argument_parser' 过长 (109行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第885行): 函数 'main' 过长 (72行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第1010行): 函数 'pre_commit_hook' 过长 (80行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第172行): 函数 'scan_directory' 过长 (55行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第536行): 函数 'generate_console_report' 过长 (84行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第622行): 函数 'generate_json_report' 过长 (52行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第676行): 函数 'generate_markdown_report' 过长 (61行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\ai-features\document-summarizer.py

- **文件类型**: python
- **总行数**: 455
- **代码行**: 342
- **注释行**: 29
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第17行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第64行): 函数名 '_get_cache_path' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第69行): 函数名 '_load_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第78行): 函数名 '_save_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第84行): 函数名 '_extract_title' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第92行): 函数名 '_extract_theorems' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第117行): 函数名 '_extract_key_concepts' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第139行): 函数名 '_categorize_term' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第153行): 函数名 '_calculate_difficulty' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第171行): 函数名 '_extract_prerequisites' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第183行): 函数名 '_generate_summary_with_llm' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第221行): 函数名 '_generate_heuristic_summary' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第345行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第78行): 函数 '_save_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第298行): 函数 'generate_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第321行): 函数 'print_summary' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第41行): 'DocumentSummary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): 'DocumentSummarizer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第345行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第58行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第64行): '_get_cache_path' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第69行): '_load_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第78行): '_save_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第84行): '_extract_title' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第92行): '_extract_theorems' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第117行): '_extract_key_concepts' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第139行): '_categorize_term' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第171行): '_extract_prerequisites' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第183行): '_generate_summary_with_llm' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第221行): '_generate_heuristic_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第243行): 'summarize' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第298行): 'generate_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第321行): 'print_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第345行): 函数 'main' 过长 (105行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第243行): 函数 'summarize' 过长 (53行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\ai-features\learning-path-personalizer.py

- **文件类型**: python
- **总行数**: 601
- **代码行**: 475
- **注释行**: 23
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第18行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第217行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第202行): 函数名 '_analyze_background' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第215行): 函数名 '_extract_years' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第303行): 函数名 '_estimate_difficulty' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第329行): 函数名 '_estimate_hours' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第351行): 函数名 '_get_prerequisites' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第361行): 函数名 '_get_outcomes' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第369行): 函数名 '_get_resources' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第376行): 函数名 '_get_phase_name' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第381行): 函数名 '_get_milestone' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第391行): 函数名 '_generate_milestones' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第411行): 函数名 '_generate_markdown_report' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第481行): 函数名 '_generate_text_report' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第507行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第34行): 'SkillLevel' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第43行): 'LearningNode' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第56行): 'LearningPath' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第68行): 'LearningPathGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第507行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第167行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第171行): 'analyze_goal' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第202行): '_analyze_background' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第215行): '_extract_years' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第226行): 'generate_path' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第303行): '_estimate_difficulty' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第329行): '_estimate_hours' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第351行): '_get_prerequisites' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第361行): '_get_outcomes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第369行): '_get_resources' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第376行): '_get_phase_name' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第381行): '_get_milestone' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第391行): '_generate_milestones' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第402行): 'generate_learning_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第481行): '_generate_text_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第507行): 函数 'main' 过长 (89行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第226行): 函数 'generate_path' 过长 (75行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第411行): 函数 '_generate_markdown_report' 过长 (68行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\ai-features\qa-bot-knowledge-base.py

- **文件类型**: python
- **总行数**: 498
- **代码行**: 358
- **注释行**: 32
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第17行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第316行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第139行): 函数名 '_clean_text' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第146行): 函数名 '_categorize' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第163行): 函数名 '_extract_tags' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第234行): 函数名 '_deduplicate' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第248行): 函数名 '_save_knowledge_base' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第271行): 函数名 '_generate_markdown_faq' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第314行): 函数名 '_get_timestamp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第349行): 函数名 '_calculate_similarity' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第388行): 函数 'print_qa_result' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第407行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第45行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第198行): 函数 'build_knowledge_base' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第248行): 函数 '_save_knowledge_base' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第271行): 函数 '_generate_markdown_faq' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第35行): 'QAEntry' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第51行): 'FAQSection' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第58行): 'QuestionExtractor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第182行): 'FAQGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第388行): 'print_qa_result' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第407行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第45行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第83行): 'extract_from_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第139行): '_clean_text' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第146行): '_categorize' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第163行): '_extract_tags' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第194行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第198行): 'build_knowledge_base' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第234行): '_deduplicate' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第248行): '_save_knowledge_base' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第314行): '_get_timestamp' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第319行): 'answer_question' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第349行): '_calculate_similarity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第407行): 函数 'main' 过长 (86行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\doc-relationship-mapper.py

- **文件类型**: python
- **总行数**: 802
- **代码行**: 604
- **注释行**: 37
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第21行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第119行): 函数名 '_parse_document' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第166行): 函数名 '_path_to_id' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第170行): 函数名 '_extract_title' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第181行): 函数名 '_determine_category' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第192行): 函数名 '_extract_metadata' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第207行): 函数名 '_extract_dependencies' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第237行): 函数名 '_extract_references' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第249行): 函数名 '_resolve_path' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第337行): 函数名 '_determine_cycle_severity' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第348行): 函数名 '_describe_cycle' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第718行): 函数名 '_calculate_depth_distribution' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第726行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第273行): 函数 'build_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第459行): 函数 'generate_all_reports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第470行): 函数 'generate_json_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第529行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第616行): 函数 'generate_dot_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第694行): 函数 'generate_statistics' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第294行): 函数 'dfs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第29行): 'DocumentNode' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第43行): 'RelationshipEdge' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第53行): 'CycleInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第61行): 'DocumentParser' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第264行): 'DependencyAnalyzer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第448行): 'ReportGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第726行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第90行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第95行): 'scan_documents' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第119行): '_parse_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第166行): '_path_to_id' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第170行): '_extract_title' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第181行): '_determine_category' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第192行): '_extract_metadata' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第207行): '_extract_dependencies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第237行): '_extract_references' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第267行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第273行): 'build_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第286行): 'detect_cycles' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第348行): '_describe_cycle' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第451行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第459行): 'generate_all_reports' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第694行): 'generate_statistics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第718行): '_calculate_depth_distribution' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第294行): FunctionDef 'dfs' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第421行): FunctionDef 'get_depth' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第726行): 函数 'main' 过长 (71行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第470行): 函数 'generate_json_report' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第529行): 函数 'generate_markdown_report' 过长 (85行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第616行): 函数 'generate_dot_graph' 过长 (76行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\knowledge-graph-generator.py

- **文件类型**: python
- **总行数**: 814
- **代码行**: 621
- **注释行**: 48
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第23行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第232行): 函数名 '_extract_description' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第324行): 函数名 '_parse_document' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第369行): 函数名 '_extract_title' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第378行): 函数名 '_extract_metadata' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第392行): 函数名 '_extract_links' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第401行): 函数名 '_extract_dependencies' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第454行): 函数名 '_add_document_nodes' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第473行): 函数名 '_add_formal_element_nodes' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第499行): 函数名 '_add_contains_edges' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第510行): 函数名 '_add_dependency_edges' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第529行): 函数名 '_add_citation_edges' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第549行): 函数名 '_add_hierarchy_edges' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第571行): 函数名 '_node_to_dict' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第583行): 函数名 '_edge_to_dict' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第592行): 函数名 '_calculate_stats' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第610行): 函数名 '_count_isolated_docs' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第632行): 函数名 '_load_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第642行): 函数名 '_save_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第678行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第454行): 函数 '_add_document_nodes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第473行): 函数 '_add_formal_element_nodes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第499行): 函数 '_add_contains_edges' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第510行): 函数 '_add_dependency_edges' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第529行): 函数 '_add_citation_edges' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第549行): 函数 '_add_hierarchy_edges' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第642行): 函数 '_save_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第659行): 函数 'update_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第31行): 'GraphNode' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第43行): 'GraphEdge' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第52行): 'FormalElement' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第63行): 'FormalElementExtractor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第272行): 'DocumentScanner' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第414行): 'GraphBuilder' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第625行): 'IncrementalUpdater' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第678行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第121行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第255行): 'extract_cross_references' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第296行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第300行): 'scan_all' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第324行): '_parse_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第369行): '_extract_title' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第378行): '_extract_metadata' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第392行): '_extract_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第401行): '_extract_dependencies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第417行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第423行): 'build' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第454行): '_add_document_nodes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第473行): '_add_formal_element_nodes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第499行): '_add_contains_edges' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第510行): '_add_dependency_edges' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第529行): '_add_citation_edges' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第571行): '_node_to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第583行): '_edge_to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第592行): '_calculate_stats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第610行): '_count_isolated_docs' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第628行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第632行): '_load_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第642行): '_save_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第648行): 'get_file_hash' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第659行): 'update_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第638行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第638行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第678行): 函数 'main' 过长 (131行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第124行): 函数 'extract_from_content' 过长 (106行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\theorem-dependency-graph.py

- **文件类型**: python
- **总行数**: 1124
- **代码行**: 887
- **注释行**: 60
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第62行): 函数 'parse_theorem_registry' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第62行): 函数 'parse_theorem_registry' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第114行): 函数 'classify_topic' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第114行): 函数 'classify_topic' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第123行): 函数 'generate_topic_graph' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第123行): 函数 'generate_topic_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第153行): 函数 'generate_stage_graph' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第153行): 函数 'generate_stage_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第158行): 函数 'detect_cycles' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第158行): 函数 'detect_cycles' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第204行): 函数 'find_isolated_elements' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第204行): 函数 'find_isolated_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第213行): 函数 'find_longest_dependency_chains' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第213行): 函数 'find_longest_dependency_chains' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第290行): 函数 'generate_mermaid_graph' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第290行): 函数 'generate_mermaid_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第357行): 函数 'generate_interactive_html' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第357行): 函数 'generate_interactive_html' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第865行): 函数 'generate_statistics_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第865行): 函数 'generate_statistics_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1042行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第164行): 函数 'dfs' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第164行): 函数 'dfs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第218行): 函数 'get_depth' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第218行): 函数 'get_depth' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第250行): 函数 'reconstruct_chain' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第250行): 函数 'reconstruct_chain' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第114行): 'classify_topic' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第158行): 'detect_cycles' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第213行): 'find_longest_dependency_chains' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第865行): 'generate_statistics_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1042行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第164行): FunctionDef 'dfs' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第218行): FunctionDef 'get_depth' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第250行): FunctionDef 'reconstruct_chain' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **empty_except** (第170行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第213行): 函数 'find_longest_dependency_chains' 过长 (74行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第290行): 函数 'generate_mermaid_graph' 过长 (64行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第357行): 函数 'generate_interactive_html' 过长 (505行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第865行): 函数 'generate_statistics_report' 过长 (174行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第1042行): 函数 'main' 过长 (77行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\website\theorem-dependency-graph.py

- **文件类型**: python
- **总行数**: 1124
- **代码行**: 887
- **注释行**: 60
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第62行): 函数 'parse_theorem_registry' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第62行): 函数 'parse_theorem_registry' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第114行): 函数 'classify_topic' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第114行): 函数 'classify_topic' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第123行): 函数 'generate_topic_graph' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第123行): 函数 'generate_topic_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第153行): 函数 'generate_stage_graph' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第153行): 函数 'generate_stage_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第158行): 函数 'detect_cycles' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第158行): 函数 'detect_cycles' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第204行): 函数 'find_isolated_elements' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第204行): 函数 'find_isolated_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第213行): 函数 'find_longest_dependency_chains' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第213行): 函数 'find_longest_dependency_chains' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第290行): 函数 'generate_mermaid_graph' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第290行): 函数 'generate_mermaid_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第357行): 函数 'generate_interactive_html' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第357行): 函数 'generate_interactive_html' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第865行): 函数 'generate_statistics_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第865行): 函数 'generate_statistics_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1042行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第164行): 函数 'dfs' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第164行): 函数 'dfs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第218行): 函数 'get_depth' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第218行): 函数 'get_depth' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第250行): 函数 'reconstruct_chain' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第250行): 函数 'reconstruct_chain' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第114行): 'classify_topic' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第158行): 'detect_cycles' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第213行): 'find_longest_dependency_chains' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第865行): 'generate_statistics_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1042行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第164行): FunctionDef 'dfs' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第218行): FunctionDef 'get_depth' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第250行): FunctionDef 'reconstruct_chain' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **empty_except** (第170行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第213行): 函数 'find_longest_dependency_chains' 过长 (74行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第290行): 函数 'generate_mermaid_graph' 过长 (64行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第357行): 函数 'generate_interactive_html' 过长 (505行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第865行): 函数 'generate_statistics_report' 过长 (174行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第1042行): 函数 'main' 过长 (77行)
  - 建议: 考虑拆分函数

### ❌ scripts\ai-features\document-summarizer.py

- **文件类型**: python
- **总行数**: 455
- **代码行**: 342
- **注释行**: 29
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第17行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第64行): 函数名 '_get_cache_path' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第69行): 函数名 '_load_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第78行): 函数名 '_save_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第84行): 函数名 '_extract_title' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第92行): 函数名 '_extract_theorems' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第117行): 函数名 '_extract_key_concepts' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第139行): 函数名 '_categorize_term' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第153行): 函数名 '_calculate_difficulty' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第171行): 函数名 '_extract_prerequisites' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第183行): 函数名 '_generate_summary_with_llm' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第221行): 函数名 '_generate_heuristic_summary' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第345行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第78行): 函数 '_save_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第298行): 函数 'generate_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第321行): 函数 'print_summary' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第41行): 'DocumentSummary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): 'DocumentSummarizer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第345行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第58行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第64行): '_get_cache_path' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第69行): '_load_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第78行): '_save_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第84行): '_extract_title' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第92行): '_extract_theorems' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第117行): '_extract_key_concepts' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第139行): '_categorize_term' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第171行): '_extract_prerequisites' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第183行): '_generate_summary_with_llm' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第221行): '_generate_heuristic_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第243行): 'summarize' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第298行): 'generate_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第321行): 'print_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第345行): 函数 'main' 过长 (105行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第243行): 函数 'summarize' 过长 (53行)
  - 建议: 考虑拆分函数

### ❌ scripts\ai-features\learning-path-personalizer.py

- **文件类型**: python
- **总行数**: 601
- **代码行**: 475
- **注释行**: 23
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第18行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第217行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第202行): 函数名 '_analyze_background' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第215行): 函数名 '_extract_years' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第303行): 函数名 '_estimate_difficulty' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第329行): 函数名 '_estimate_hours' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第351行): 函数名 '_get_prerequisites' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第361行): 函数名 '_get_outcomes' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第369行): 函数名 '_get_resources' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第376行): 函数名 '_get_phase_name' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第381行): 函数名 '_get_milestone' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第391行): 函数名 '_generate_milestones' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第411行): 函数名 '_generate_markdown_report' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第481行): 函数名 '_generate_text_report' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第507行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第34行): 'SkillLevel' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第43行): 'LearningNode' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第56行): 'LearningPath' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第68行): 'LearningPathGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第507行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第167行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第171行): 'analyze_goal' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第202行): '_analyze_background' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第215行): '_extract_years' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第226行): 'generate_path' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第303行): '_estimate_difficulty' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第329行): '_estimate_hours' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第351行): '_get_prerequisites' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第361行): '_get_outcomes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第369行): '_get_resources' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第376行): '_get_phase_name' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第381行): '_get_milestone' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第391行): '_generate_milestones' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第402行): 'generate_learning_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第481行): '_generate_text_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第507行): 函数 'main' 过长 (89行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第226行): 函数 'generate_path' 过长 (75行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第411行): 函数 '_generate_markdown_report' 过长 (68行)
  - 建议: 考虑拆分函数

### ❌ scripts\ai-features\qa-bot-knowledge-base.py

- **文件类型**: python
- **总行数**: 498
- **代码行**: 358
- **注释行**: 32
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第17行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第316行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第139行): 函数名 '_clean_text' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第146行): 函数名 '_categorize' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第163行): 函数名 '_extract_tags' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第234行): 函数名 '_deduplicate' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第248行): 函数名 '_save_knowledge_base' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第271行): 函数名 '_generate_markdown_faq' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第314行): 函数名 '_get_timestamp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第349行): 函数名 '_calculate_similarity' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第388行): 函数 'print_qa_result' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第407行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第45行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第198行): 函数 'build_knowledge_base' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第248行): 函数 '_save_knowledge_base' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第271行): 函数 '_generate_markdown_faq' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第35行): 'QAEntry' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第51行): 'FAQSection' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第58行): 'QuestionExtractor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第182行): 'FAQGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第388行): 'print_qa_result' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第407行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第45行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第83行): 'extract_from_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第139行): '_clean_text' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第146行): '_categorize' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第163行): '_extract_tags' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第194行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第198行): 'build_knowledge_base' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第234行): '_deduplicate' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第248行): '_save_knowledge_base' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第314行): '_get_timestamp' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第319行): 'answer_question' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第349行): '_calculate_similarity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第407行): 函数 'main' 过长 (86行)
  - 建议: 考虑拆分函数

### ❌ scripts\doc-relationship-mapper.py

- **文件类型**: python
- **总行数**: 802
- **代码行**: 604
- **注释行**: 37
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第21行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第119行): 函数名 '_parse_document' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第166行): 函数名 '_path_to_id' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第170行): 函数名 '_extract_title' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第181行): 函数名 '_determine_category' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第192行): 函数名 '_extract_metadata' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第207行): 函数名 '_extract_dependencies' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第237行): 函数名 '_extract_references' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第249行): 函数名 '_resolve_path' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第337行): 函数名 '_determine_cycle_severity' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第348行): 函数名 '_describe_cycle' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第718行): 函数名 '_calculate_depth_distribution' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第726行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第273行): 函数 'build_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第459行): 函数 'generate_all_reports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第470行): 函数 'generate_json_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第529行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第616行): 函数 'generate_dot_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第694行): 函数 'generate_statistics' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第294行): 函数 'dfs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第29行): 'DocumentNode' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第43行): 'RelationshipEdge' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第53行): 'CycleInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第61行): 'DocumentParser' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第264行): 'DependencyAnalyzer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第448行): 'ReportGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第726行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第90行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第95行): 'scan_documents' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第119行): '_parse_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第166行): '_path_to_id' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第170行): '_extract_title' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第181行): '_determine_category' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第192行): '_extract_metadata' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第207行): '_extract_dependencies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第237行): '_extract_references' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第267行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第273行): 'build_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第286行): 'detect_cycles' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第348行): '_describe_cycle' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第451行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第459行): 'generate_all_reports' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第694行): 'generate_statistics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第718行): '_calculate_depth_distribution' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第294行): FunctionDef 'dfs' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第421行): FunctionDef 'get_depth' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第726行): 函数 'main' 过长 (71行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第470行): 函数 'generate_json_report' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第529行): 函数 'generate_markdown_report' 过长 (85行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第616行): 函数 'generate_dot_graph' 过长 (76行)
  - 建议: 考虑拆分函数

### ❌ scripts\knowledge-graph-generator.py

- **文件类型**: python
- **总行数**: 814
- **代码行**: 621
- **注释行**: 48
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第23行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第232行): 函数名 '_extract_description' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第324行): 函数名 '_parse_document' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第369行): 函数名 '_extract_title' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第378行): 函数名 '_extract_metadata' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第392行): 函数名 '_extract_links' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第401行): 函数名 '_extract_dependencies' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第454行): 函数名 '_add_document_nodes' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第473行): 函数名 '_add_formal_element_nodes' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第499行): 函数名 '_add_contains_edges' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第510行): 函数名 '_add_dependency_edges' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第529行): 函数名 '_add_citation_edges' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第549行): 函数名 '_add_hierarchy_edges' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第571行): 函数名 '_node_to_dict' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第583行): 函数名 '_edge_to_dict' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第592行): 函数名 '_calculate_stats' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第610行): 函数名 '_count_isolated_docs' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第632行): 函数名 '_load_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第642行): 函数名 '_save_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第678行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第454行): 函数 '_add_document_nodes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第473行): 函数 '_add_formal_element_nodes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第499行): 函数 '_add_contains_edges' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第510行): 函数 '_add_dependency_edges' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第529行): 函数 '_add_citation_edges' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第549行): 函数 '_add_hierarchy_edges' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第642行): 函数 '_save_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第659行): 函数 'update_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第31行): 'GraphNode' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第43行): 'GraphEdge' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第52行): 'FormalElement' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第63行): 'FormalElementExtractor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第272行): 'DocumentScanner' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第414行): 'GraphBuilder' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第625行): 'IncrementalUpdater' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第678行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第121行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第255行): 'extract_cross_references' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第296行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第300行): 'scan_all' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第324行): '_parse_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第369行): '_extract_title' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第378行): '_extract_metadata' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第392行): '_extract_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第401行): '_extract_dependencies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第417行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第423行): 'build' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第454行): '_add_document_nodes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第473行): '_add_formal_element_nodes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第499行): '_add_contains_edges' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第510行): '_add_dependency_edges' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第529行): '_add_citation_edges' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第571行): '_node_to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第583行): '_edge_to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第592行): '_calculate_stats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第610行): '_count_isolated_docs' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第628行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第632行): '_load_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第642行): '_save_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第648行): 'get_file_hash' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第659行): 'update_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第638行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第638行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第678行): 函数 'main' 过长 (131行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第124行): 函数 'extract_from_content' 过长 (106行)
  - 建议: 考虑拆分函数

### ❌ theorem-dependency-graph.py

- **文件类型**: python
- **总行数**: 1124
- **代码行**: 887
- **注释行**: 60
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第62行): 函数 'parse_theorem_registry' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第62行): 函数 'parse_theorem_registry' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第114行): 函数 'classify_topic' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第114行): 函数 'classify_topic' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第123行): 函数 'generate_topic_graph' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第123行): 函数 'generate_topic_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第153行): 函数 'generate_stage_graph' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第153行): 函数 'generate_stage_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第158行): 函数 'detect_cycles' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第158行): 函数 'detect_cycles' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第204行): 函数 'find_isolated_elements' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第204行): 函数 'find_isolated_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第213行): 函数 'find_longest_dependency_chains' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第213行): 函数 'find_longest_dependency_chains' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第290行): 函数 'generate_mermaid_graph' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第290行): 函数 'generate_mermaid_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第357行): 函数 'generate_interactive_html' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第357行): 函数 'generate_interactive_html' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第865行): 函数 'generate_statistics_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第865行): 函数 'generate_statistics_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第1042行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第164行): 函数 'dfs' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第164行): 函数 'dfs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第218行): 函数 'get_depth' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第218行): 函数 'get_depth' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第250行): 函数 'reconstruct_chain' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第250行): 函数 'reconstruct_chain' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第114行): 'classify_topic' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第158行): 'detect_cycles' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第213行): 'find_longest_dependency_chains' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第865行): 'generate_statistics_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第1042行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第164行): FunctionDef 'dfs' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第218行): FunctionDef 'get_depth' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第250行): FunctionDef 'reconstruct_chain' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **empty_except** (第170行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第213行): 函数 'find_longest_dependency_chains' 过长 (74行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第290行): 函数 'generate_mermaid_graph' 过长 (64行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第357行): 函数 'generate_interactive_html' 过长 (505行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第865行): 函数 'generate_statistics_report' 过长 (174行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第1042行): 函数 'main' 过长 (77行)
  - 建议: 考虑拆分函数

### ❌ tools\link-validator.py

- **文件类型**: python
- **总行数**: 882
- **代码行**: 643
- **注释行**: 84
- **质量分数**: 0.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第25行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第28行): 导入顺序问题: typing
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第867行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第126行): 函数名 '_load_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第139行): 函数名 '_clean_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第150行): 函数名 '_save_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第159行): 函数名 '_normalize_path' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第172行): 函数名 '_is_excluded_dir' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第213行): 函数名 '_extract_anchor' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第232行): 函数名 '_is_valid_link' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第263行): 函数名 '_extract_links_from_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第365行): 函数名 '_classify_link' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第388行): 函数名 '_resolve_internal_link' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第443行): 函数名 '_check_external_link' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第475行): 函数名 '_do_external_check' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第865行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第102行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第126行): 函数 '_load_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第139行): 函数 '_clean_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第150行): 函数 '_save_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第554行): 函数 'validate_all_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第825行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第99行): 'LinkValidator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第865行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第102行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第126行): '_load_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第139行): '_clean_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第150行): '_save_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第159行): '_normalize_path' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第388行): '_resolve_internal_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第475行): '_do_external_check' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第554行): 'validate_all_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第825行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第527行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第263行): 函数 '_extract_links_from_file' 过长 (100行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第388行): 函数 '_resolve_internal_link' 过长 (53行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第475行): 函数 '_do_external_check' 过长 (77行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第554行): 函数 'validate_all_links' 过长 (94行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第650行): 函数 'generate_report' 过长 (173行)
  - 建议: 考虑拆分函数

### ❌ tools\theorem-dependency-validator.py

- **文件类型**: python
- **总行数**: 970
- **代码行**: 758
- **注释行**: 55
- **质量分数**: 0.0/100

**问题列表**:

- ⚠️ **import_order** (第24行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第458行): 导入顺序问题: collections
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第139行): 函数名 '_color' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第145行): 函数名 '_log' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第188行): 函数名 '_scan_single_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第246行): 函数名 '_scan_registry_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第273行): 函数名 '_extract_dependencies' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第292行): 函数名 '_detect_formal_level' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第872行): 函数名 '_print_summary' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第898行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第145行): 函数 '_log' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第188行): 函数 '_scan_single_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第246行): 函数 '_scan_registry_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第301行): 函数 'validate_dependencies' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第498行): 函数 'generate_mermaid_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第529行): 函数 'generate_neo4j_csv' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第552行): 函数 'generate_graphviz_dot' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第631行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第779行): 函数 'generate_json_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第831行): 函数 'run_full_validation' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第872行): 函数 '_print_summary' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第334行): 函数 'dfs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第32行): 'ElementType' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第41行): 'Severity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第49行): 'FormalElement' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第66行): 'ValidationIssue' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第77行): 'Colors' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第89行): 'TheoremDependencyValidator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第898行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第129行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第145行): '_log' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第292行): '_detect_formal_level' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第301行): 'validate_dependencies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第326行): 'detect_circular_dependencies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第434行): 'generate_dependency_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第593行): 'calculate_coverage' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第831行): 'run_full_validation' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第872行): '_print_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第334行): FunctionDef 'dfs' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第898行): 函数 'main' 过长 (67行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第188行): 函数 '_scan_single_file' 过长 (56行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第441行): 函数 'find_critical_path' 过长 (55行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第631行): 函数 'generate_markdown_report' 过长 (146行)
  - 建议: 考虑拆分函数

### ❌ .scripts\knowledge-graph\theorem-dependency-analyzer.py

- **文件类型**: python
- **总行数**: 747
- **代码行**: 570
- **注释行**: 46
- **质量分数**: 2.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第16行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第164行): 函数名 '_extract_statement_and_proof' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第211行): 函数名 '_extract_from_proof' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第233行): 函数名 '_extract_from_statement' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第407行): 函数名 '_find_longest_path_in_subgraph' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第422行): 函数名 '_backtrack_from_node' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第702行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第193行): 函数 'extract_dependencies' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第211行): 函数 '_extract_from_proof' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第233行): 函数 '_extract_from_statement' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第277行): 函数 'build_dependency_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第322行): 函数 'compute_proof_depth' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第361行): 函数 'compute_complexity' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第470行): 函数 'export_json' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第523行): 函数 'export_critical_path_txt' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第630行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第74行): 'DependencyEdge' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第83行): 'TheoremParser' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第268行): 'DependencyAnalyzer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第463行): 'DependencyExporter' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第682行): 'load_config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第702行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第56行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第113行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第164行): '_extract_statement_and_proof' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第271行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第277行): 'build_dependency_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第304行): 'detect_cycles' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第361行): 'compute_complexity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第422行): '_backtrack_from_node' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第466行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第470行): 'export_json' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第621行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第630行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第470行): 函数 'export_json' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第523行): 函数 'export_critical_path_txt' 过长 (92行)
  - 建议: 考虑拆分函数

### ❌ .improvement-tracking\scripts\merge-docs.py

- **文件类型**: python
- **总行数**: 647
- **代码行**: 483
- **注释行**: 32
- **质量分数**: 3.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第21行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第23行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第25行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第63行): 函数名 '_read_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第204行): 函数名 '_generate_steps' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第266行): 函数名 '_identify_risks' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第292行): 函数名 '_estimate_time' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第360行): 函数名 '_extract_unique_sections' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第375行): 函数名 '_insert_section' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第492行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第37行): 'DocumentAnalyzer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第141行): 'MergePlanner' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第310行): 'MergeExecutor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第492行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第40行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第63行): '_read_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第114行): 'compare_documents' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第144行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第204行): '_generate_steps' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第266行): '_identify_risks' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第313行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第318行): 'backup_files' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第422行): 'delete_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第436行): 'execute_merge' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第492行): 函数 'main' 过长 (150行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第148行): 函数 'generate_merge_plan' 过长 (54行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第204行): 函数 '_generate_steps' 过长 (60行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第436行): 函数 'execute_merge' 过长 (53行)
  - 建议: 考虑拆分函数

### ❌ .scripts\kg-v2\learning-path-recommender-v2.py

- **文件类型**: python
- **总行数**: 727
- **代码行**: 500
- **注释行**: 77
- **质量分数**: 3.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第24行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第194行): 函数名 '_create_sample_graph' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第287行): 函数名 '_calculate_reward' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第640行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第137行): 函数 'load_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第194行): 函数 '_create_sample_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第397行): 函数 'store_transition' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第401行): 函数 'learn' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第444行): 函数 'update_target_network' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第525行): 函数 'train' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第64行): 'UserState' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第103行): 'LearningPath' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第319行): 'DQN' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第341行): 'DQNAgent' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第454行): 'LearningPathGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第596行): 'evaluate_path' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第640行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第76行): 'progress_rate' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第110行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第126行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第137行): 'load_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第194行): '_create_sample_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第238行): 'reset' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第287行): '_calculate_reward' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第322行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第332行): FunctionDef 'forward' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第344行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第397行): 'store_transition' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第401行): 'learn' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第444行): 'update_target_network' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第457行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第461行): 'generate_path' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第525行): 'train' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第640行): 函数 'main' 过长 (82行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第137行): 函数 'load_graph' 过长 (55行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第461行): 函数 'generate_path' 过长 (62行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第525行): 函数 'train' 过长 (64行)
  - 建议: 考虑拆分函数

### ❌ .scripts\automation\formal-element-tracker.py

- **文件类型**: python
- **总行数**: 814
- **代码行**: 627
- **注释行**: 50
- **质量分数**: 4.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第166行): 函数名 '_should_skip_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第171行): 函数名 '_extract_title' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第190行): 函数名 '_extract_dependencies' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第331行): 函数名 '_analyze_conflicts' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第375行): 函数名 '_generate_statistics' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第414行): 函数名 '_generate_suggestions' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第693行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第67行): 函数 '**hash**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第70行): 函数 '**eq**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第70行): 函数 '**eq**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第36行): 'ElementType' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第45行): 'Stage' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第53行): 'FormalElement' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第77行): 'ConflictInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第86行): 'TrackingResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第94行): 'FormalElementTracker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第693行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第67行): FunctionDef '**hash**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第70行): FunctionDef '**eq**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第171行): '_extract_title' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第190行): '_extract_dependencies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第331行): '_analyze_conflicts' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第375行): '_generate_statistics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第414行): '_generate_suggestions' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第693行): 函数 'main' 过长 (116行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第205行): 函数 'scan_file' 过长 (77行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第489行): 函数 'generate_json_database' 过长 (54行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第545行): 函数 'update_registry' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第606行): 函数 'generate_markdown_report' 过长 (84行)
  - 建议: 考虑拆分函数

### ❌ .scripts\kg-v2\enhance-graph-data.py

- **文件类型**: python
- **总行数**: 733
- **代码行**: 605
- **注释行**: 31
- **质量分数**: 5.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **naming_convention** (第185行): 函数名 '_estimate_word_count' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第618行): 函数名 '_build_proof_chains' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第722行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第65行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第89行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第683行): 函数 'save_all' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第55行): 'Node' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第81行): 'Edge' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第102行): 'GraphDataEnhancer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第722行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第65行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第69行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第89行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第93行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第105行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第117行): 'parse_theorem_registry' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第153行): 'scan_documents' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第185行): '_estimate_word_count' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第196行): 'extract_dependencies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第239行): 'build_concept_hierarchy' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第292行): 'build_theorem_network' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第482行): 'generate_enhanced_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第565行): 'generate_theorem_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第618行): '_build_proof_chains' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第635行): 'generate_frontier_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第683行): 'save_all' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第192行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第192行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第239行): 函数 'build_concept_hierarchy' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第342行): 函数 'build_document_network' 过长 (60行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第404行): 函数 'build_frontier_data' 过长 (76行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第482行): 函数 'generate_enhanced_data' 过长 (81行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第565行): 函数 'generate_theorem_data' 过长 (51行)
  - 建议: 考虑拆分函数

### ❌ .improvement-tracking\scripts\quality-score-calculator.py

- **文件类型**: python
- **总行数**: 617
- **代码行**: 439
- **注释行**: 49
- **质量分数**: 6.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第40行): 函数 'get_file_age_days' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第40行): 函数 'get_file_age_days' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第49行): 函数 'parse_datetime' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第49行): 函数 'parse_datetime' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第60行): 函数 'analyze_structure' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第60行): 函数 'analyze_structure' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第137行): 函数 'analyze_completeness' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第137行): 函数 'analyze_completeness' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第196行): 函数 'analyze_freshness' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第196行): 函数 'analyze_freshness' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第249行): 函数 'analyze_references' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第249行): 函数 'analyze_references' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第299行): 函数 'calculate_quality_score' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第299行): 函数 'calculate_quality_score' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第363行): 函数 'scan_documents' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第363行): 函数 'scan_documents' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第380行): 函数 'generate_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第380行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第540行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第49行): 'parse_datetime' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第60行): 'analyze_structure' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第137行): 'analyze_completeness' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第196行): 'analyze_freshness' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第249行): 'analyze_references' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第380行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第540行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第45行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **bare_except** (第205行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **bare_except** (第55行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第60行): 函数 'analyze_structure' 过长 (74行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第137行): 函数 'analyze_completeness' 过长 (56行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第299行): 函数 'calculate_quality_score' 过长 (61行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第380行): 函数 'generate_report' 过长 (157行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第540行): 函数 'main' 过长 (72行)
  - 建议: 考虑拆分函数

### ❌ .scripts\knowledge-graph\concept-map-builder.py

- **文件类型**: python
- **总行数**: 662
- **代码行**: 503
- **注释行**: 45
- **质量分数**: 6.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第16行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第205行): 函数名 '_extract_cross_references' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第544行): 函数名 '_export_summary' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第620行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第205行): 函数 '_extract_cross_references' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第321行): 函数 'export' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第387行): 函数 'export' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第497行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第544行): 函数 '_export_summary' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第52行): 'Concept' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第68行): 'ConceptRelation' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第484行): 'ConceptMapBuilder' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第594行): 'load_config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第620行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第105行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第224行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第260行): 'compute_centrality' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第302行): 'get_top_concepts' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第318行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第383行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第387行): 'export' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第487行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第497行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第544行): '_export_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第31行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第39行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第115行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第115行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第118行): 函数 'extract_from_file' 过长 (64行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第321行): 函数 'export' 过长 (56行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第387行): 函数 'export' 过长 (94行)
  - 建议: 考虑拆分函数

### ❌ tools\fix-missing-dependencies.py

- **文件类型**: python
- **总行数**: 602
- **代码行**: 489
- **注释行**: 28
- **质量分数**: 9.0/100

**问题列表**:

- ⚠️ **import_order** (第25行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第83行): 函数名 '_log' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第187行): 函数名 '_is_valid_element_id' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第192行): 函数名 '_find_similar_element' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第518行): 函数名 '_print_summary' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第538行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第83行): 函数 '_log' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第125行): 函数 'scan_theorem_registry' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第147行): 函数 'categorize_missing_dependencies' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第221行): 函数 'generate_fix_script' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第280行): 函数 'generate_todo_list' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第357行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第481行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第518行): 函数 '_print_summary' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第33行): 'FixType' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第43行): 'MissingDependency' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第54行): 'FixResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第61行): 'MissingDependencyFixer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第538行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第64行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第83行): '_log' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第90行): 'load_validation_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第147行): 'categorize_missing_dependencies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第221行): 'generate_fix_script' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第280行): 'generate_todo_list' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第357行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第481行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第518行): '_print_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第538行): 函数 'main' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第221行): 函数 'generate_fix_script' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第280行): 函数 'generate_todo_list' 过长 (75行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第357行): 函数 'generate_report' 过长 (122行)
  - 建议: 考虑拆分函数

### ❌ .improvement-tracking\scripts\detect-duplicate-content.py

- **文件类型**: python
- **总行数**: 463
- **代码行**: 314
- **注释行**: 30
- **质量分数**: 10.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第13行): 导入顺序问题: collections
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第24行): 函数 'normalize_text' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第24行): 函数 'normalize_text' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第47行): 函数 'get_shingles' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第47行): 函数 'get_shingles' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第55行): 函数 'jaccard_similarity' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第55行): 函数 'jaccard_similarity' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第64行): 函数 'get_file_hash' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第64行): 函数 'get_file_hash' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第74行): 函数 'extract_sections' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第74行): 函数 'extract_sections' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第93行): 函数 'analyze_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第93行): 函数 'analyze_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第129行): 函数 'scan_documents' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第129行): 函数 'scan_documents' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第146行): 函数 'find_exact_duplicates' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第146行): 函数 'find_exact_duplicates' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第165行): 函数 'find_similar_documents' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第165行): 函数 'find_similar_documents' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第199行): 函数 'find_title_duplicates' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第199行): 函数 'find_title_duplicates' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第221行): 函数 'categorize_duplicates' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第221行): 函数 'categorize_duplicates' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第237行): 函数 'generate_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第237行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第385行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第64行): 'get_file_hash' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第74行): 'extract_sections' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第93行): 'analyze_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第146行): 'find_exact_duplicates' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第165行): 'find_similar_documents' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第199行): 'find_title_duplicates' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第221行): 'categorize_duplicates' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第237行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第385行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第70行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第237行): 函数 'generate_report' 过长 (145行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第385行): 函数 'main' 过长 (73行)
  - 建议: 考虑拆分函数

### ❌ .scripts\automation\cross-ref-validator.py

- **文件类型**: python
- **总行数**: 760
- **代码行**: 603
- **注释行**: 39
- **质量分数**: 10.0/100

**问题列表**:

- ⚠️ **import_order** (第24行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第151行): 函数名 '_load_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第162行): 函数名 '_save_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第171行): 函数名 '_get_file_hash' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第176行): 函数名 '_should_check_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第183行): 函数名 '_is_external_url' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第188行): 函数名 '_extract_anchors' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第207行): 函数名 '_extract_references' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第216行): 函数名 '_parse_link' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第643行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第39行): 'LinkType' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第47行): 'LinkStatus' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第57行): 'LinkInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第72行): 'ValidationResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第86行): 'CrossRefValidator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第643行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第151行): '_load_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第162行): '_save_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第171行): '_get_file_hash' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第207行): '_extract_references' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第289行): 'validate_internal_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第330行): 'validate_external_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第396行): 'validate_reference' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第483行): AsyncFunctionDef 'validate_with_limit' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第643行): 函数 'main' 过长 (112行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第228行): 函数 'scan_file' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第558行): 函数 'generate_markdown_summary' 过长 (82行)
  - 建议: 考虑拆分函数

### ❌ .scripts\seo-optimizer.py

- **文件类型**: python
- **总行数**: 827
- **代码行**: 619
- **注释行**: 64
- **质量分数**: 12.0/100

**问题列表**:

- ⚠️ **import_order** (第29行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第117行): 函数名 '_should_exclude' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第124行): 函数名 '_extract_title_from_md' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第145行): 函数名 '_extract_description_from_md' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第170行): 函数名 '_get_priority' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第187行): 函数名 '_get_changefreq' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第200行): 函数名 '_get_category' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第774行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第736行): 函数 'run_full_audit' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第37行): 'DocumentInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第48行): 'SEOOptimizer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第774行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第106行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第200行): '_get_category' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第223行): 'scan_documents' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第593行): 'generate_seo_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第248行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **bare_except** (第273行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第223行): 函数 'scan_documents' 过长 (69行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第340行): 函数 'generate_robots_txt' 过长 (76行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第418行): 函数 'generate_structured_data' 过长 (74行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第494行): 函数 'optimize_html_files' 过长 (97行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第593行): 函数 'generate_seo_report' 过长 (141行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\link-health-checker.py

- **文件类型**: python
- **总行数**: 770
- **代码行**: 606
- **注释行**: 42
- **质量分数**: 12.0/100

**问题列表**:

- ⚠️ **import_order** (第20行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第23行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第26行): 导入顺序问题: dataclasses
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第31行): 导入顺序问题: collections
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第102行): 函数名 '_get_url_hash' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第106行): 函数名 '_load_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第293行): 函数名 '_is_excluded' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第106行): 函数 '_load_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第122行): 函数 'save_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第143行): 函数 'set' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第501行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第647行): 函数 'save_json_results' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第49行): 'LinkCheckResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第76行): 'CheckSummary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第661行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第94行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第102行): '_get_url_hash' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第106行): '_load_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第122行): 'save_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第131行): 'get' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第143行): 'set' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第157行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第243行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第300行): 'check_url' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第437行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第419行): AsyncFunctionDef 'check_with_limit' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **empty_except** (第353行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第160行): 函数 'extract_external_links' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第501行): 函数 'generate_markdown_report' 过长 (144行)
  - 建议: 考虑拆分函数

### ❌ scripts\link-health-checker.py

- **文件类型**: python
- **总行数**: 770
- **代码行**: 606
- **注释行**: 42
- **质量分数**: 12.0/100

**问题列表**:

- ⚠️ **import_order** (第20行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第23行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第26行): 导入顺序问题: dataclasses
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第31行): 导入顺序问题: collections
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第102行): 函数名 '_get_url_hash' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第106行): 函数名 '_load_cache' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第293行): 函数名 '_is_excluded' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第106行): 函数 '_load_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第122行): 函数 'save_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第143行): 函数 'set' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第501行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第647行): 函数 'save_json_results' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第49行): 'LinkCheckResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第76行): 'CheckSummary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第661行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第94行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第102行): '_get_url_hash' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第106行): '_load_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第122行): 'save_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第131行): 'get' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第143行): 'set' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第157行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第243行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第300行): 'check_url' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第437行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第419行): AsyncFunctionDef 'check_with_limit' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **empty_except** (第353行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第160行): 函数 'extract_external_links' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第501行): 函数 'generate_markdown_report' 过长 (144行)
  - 建议: 考虑拆分函数

### ❌ .scripts\knowledge-graph\doc-similarity-analyzer.py

- **文件类型**: python
- **总行数**: 732
- **代码行**: 549
- **注释行**: 40
- **质量分数**: 14.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第16行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第691行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第497行): 函数 'export_similarity_matrix' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第528行): 函数 'export_clusters' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第552行): 函数 'export_recommendations' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第588行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第51行): 'Document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第75行): 'TextPreprocessor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第131行): 'DocumentLoader' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第195行): 'SimilarityCalculator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第339行): 'DocumentClusterer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第436行): 'GapAnalyzer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第490行): 'SimilarityExporter' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第667行): 'load_config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第691行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第64行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第104行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第114行): 'remove_stopwords' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第120行): 'preprocess' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第134行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第139行): 'load_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第198行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第246行): 'compute_bert_embeddings' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第280行): 'compute_similarity_matrix' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第295行): 'find_similar_pairs' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第313行): 'find_duplicates' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第342行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第377行): 'cluster_hierarchical' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第408行): 'analyze_clusters' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第439行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第442行): 'analyze_topic_coverage' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第473行): 'identify_gaps' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第493行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第497行): 'export_similarity_matrix' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第528行): 'export_clusters' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第552行): 'export_recommendations' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第577行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第588行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第588行): 函数 'run' 过长 (76行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\ai-features\smart-search-indexer.py

- **文件类型**: python
- **总行数**: 557
- **代码行**: 402
- **注释行**: 41
- **质量分数**: 14.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第19行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第149行): 函数名 '_get_cache_key' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第226行): 函数名 '_get_index_path' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第229行): 函数名 '_get_metadata_path' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第261行): 函数名 '_index_document' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第434行): 函数 'print_results' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第456行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第232行): 函数 'build' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第261行): 函数 '_index_document' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第296行): 函数 'generate_embeddings' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第397行): 函数 'save' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第49行): 'SearchResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第60行): 'DocumentChunk' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第70行): 'TextProcessor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第141行): 'EmbeddingGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第214行): 'SearchIndex' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第434行): 'print_results' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第456行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第80行): 'tokenize' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第91行): 'chunk_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第144行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第149行): FunctionDef '_get_cache_key' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第152行): 'generate' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第200行): 'cosine_similarity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第217行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第226行): FunctionDef '_get_index_path' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第229行): FunctionDef '_get_metadata_path' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第232行): 'build' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第261行): '_index_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第296行): 'generate_embeddings' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第397行): 'save' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第417行): 'load' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第456行): 函数 'main' 过长 (96行)
  - 建议: 考虑拆分函数

### ❌ scripts\ai-features\smart-search-indexer.py

- **文件类型**: python
- **总行数**: 557
- **代码行**: 402
- **注释行**: 41
- **质量分数**: 14.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第19行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第149行): 函数名 '_get_cache_key' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第226行): 函数名 '_get_index_path' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第229行): 函数名 '_get_metadata_path' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第261行): 函数名 '_index_document' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第434行): 函数 'print_results' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第456行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第232行): 函数 'build' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第261行): 函数 '_index_document' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第296行): 函数 'generate_embeddings' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第397行): 函数 'save' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第49行): 'SearchResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第60行): 'DocumentChunk' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第70行): 'TextProcessor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第141行): 'EmbeddingGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第214行): 'SearchIndex' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第434行): 'print_results' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第456行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第80行): 'tokenize' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第91行): 'chunk_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第144行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第149行): FunctionDef '_get_cache_key' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第152行): 'generate' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第200行): 'cosine_similarity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第217行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第226行): FunctionDef '_get_index_path' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第229行): FunctionDef '_get_metadata_path' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第232行): 'build' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第261行): '_index_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第296行): 'generate_embeddings' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第397行): 'save' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第417行): 'load' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第456行): 函数 'main' 过长 (96行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\audit-fictional-content.py

- **文件类型**: python
- **总行数**: 538
- **代码行**: 425
- **注释行**: 28
- **质量分数**: 18.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第449行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第76行): 函数名 '_load_config' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第85行): 函数名 '_compile_patterns' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第120行): 函数名 '_compile_exclusions' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第145行): 函数名 '_should_exclude_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第159行): 函数名 '_should_exclude_line' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第166行): 函数名 '_get_context' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第470行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第31行): 'Finding' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第63行): 'FictionalContentAuditor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第470行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第45行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第66行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第120行): '_compile_exclusions' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第166行): '_get_context' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第183行): 'scan_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第224行): 'scan_project' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第263行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第133行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第140行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第470行): 函数 'main' 过长 (63行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第263行): 函数 'generate_report' 过长 (182行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\full_cross_ref_validator_v2.py

- **文件类型**: python
- **总行数**: 475
- **代码行**: 322
- **注释行**: 59
- **质量分数**: 18.0/100

**问题列表**:

- ⚠️ **import_order** (第465行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第18行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第43行): 函数 'scan_all_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第56行): 函数 'extract_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第56行): 函数 'extract_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第84行): 函数 'generate_anchor_from_text' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第84行): 函数 'generate_anchor_from_text' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第103行): 函数 'normalize_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第103行): 函数 'normalize_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第130行): 函数 'is_likely_code_content' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第130行): 函数 'is_likely_code_content' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第151行): 函数 'validate_all_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第160行): 函数 'validate_file_links' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第160行): 函数 'validate_file_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第185行): 函数 'validate_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第185行): 函数 'validate_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第250行): 函数 'check_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第250行): 函数 'check_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第273行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第302行): 函数 'generate_file_statistics' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第322行): 函数 'save_reports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第322行): 函数 'save_reports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第338行): 函数 'generate_markdown_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第338行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第426行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第17行): ClassDef 'CrossRefValidator' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第18行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第185行): 'validate_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第250行): 'check_anchor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第273行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第322行): 'save_reports' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第426行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第224行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第185行): 函数 'validate_link' 过长 (63行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第338行): 函数 'generate_markdown_report' 过长 (86行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\manage-doc-tiers.py

- **文件类型**: python
- **总行数**: 632
- **代码行**: 496
- **注释行**: 36
- **质量分数**: 18.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第27行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第386行): 函数 'cmd_scan' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第386行): 函数 'cmd_scan' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第403行): 函数 'cmd_tier' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第403行): 函数 'cmd_tier' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第422行): 函数 'cmd_apply_tier' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第422行): 函数 'cmd_apply_tier' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第446行): 函数 'cmd_check_review' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第446行): 函数 'cmd_check_review' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第483行): 函数 'cmd_stats' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第483行): 函数 'cmd_stats' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第535行): 函数 'cmd_validate' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第535行): 函数 'cmd_validate' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第565行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第216行): 'DocInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第274行): 'get_maintainers' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第284行): 'calculate_next_review' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第301行): 'scan_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第326行): 'scan_all_documents' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第386行): 'cmd_scan' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第403行): 'cmd_tier' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第422行): 'cmd_apply_tier' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第446行): 'cmd_check_review' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第483行): 'cmd_stats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第535行): 'cmd_validate' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第565行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **empty_except** (第467行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第498行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第498行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第529行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第565行): 函数 'main' 过长 (62行)
  - 建议: 考虑拆分函数

### ❌ scripts\audit-fictional-content.py

- **文件类型**: python
- **总行数**: 538
- **代码行**: 425
- **注释行**: 28
- **质量分数**: 18.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第449行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第76行): 函数名 '_load_config' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第85行): 函数名 '_compile_patterns' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第120行): 函数名 '_compile_exclusions' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第145行): 函数名 '_should_exclude_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第159行): 函数名 '_should_exclude_line' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第166行): 函数名 '_get_context' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第470行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第31行): 'Finding' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第63行): 'FictionalContentAuditor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第470行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第45行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第66行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第120行): '_compile_exclusions' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第166行): '_get_context' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第183行): 'scan_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第224行): 'scan_project' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第263行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第133行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第140行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第470行): 函数 'main' 过长 (63行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第263行): 函数 'generate_report' 过长 (182行)
  - 建议: 考虑拆分函数

### ❌ scripts\full_cross_ref_validator_v2.py

- **文件类型**: python
- **总行数**: 475
- **代码行**: 322
- **注释行**: 59
- **质量分数**: 18.0/100

**问题列表**:

- ⚠️ **import_order** (第465行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第18行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第43行): 函数 'scan_all_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第56行): 函数 'extract_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第56行): 函数 'extract_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第84行): 函数 'generate_anchor_from_text' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第84行): 函数 'generate_anchor_from_text' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第103行): 函数 'normalize_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第103行): 函数 'normalize_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第130行): 函数 'is_likely_code_content' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第130行): 函数 'is_likely_code_content' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第151行): 函数 'validate_all_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第160行): 函数 'validate_file_links' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第160行): 函数 'validate_file_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第185行): 函数 'validate_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第185行): 函数 'validate_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第250行): 函数 'check_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第250行): 函数 'check_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第273行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第302行): 函数 'generate_file_statistics' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第322行): 函数 'save_reports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第322行): 函数 'save_reports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第338行): 函数 'generate_markdown_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第338行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第426行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第17行): ClassDef 'CrossRefValidator' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第18行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第185行): 'validate_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第250行): 'check_anchor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第273行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第322行): 'save_reports' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第426行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第224行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第185行): 函数 'validate_link' 过长 (63行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第338行): 函数 'generate_markdown_report' 过长 (86行)
  - 建议: 考虑拆分函数

### ❌ scripts\manage-doc-tiers.py

- **文件类型**: python
- **总行数**: 632
- **代码行**: 496
- **注释行**: 36
- **质量分数**: 18.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第27行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第386行): 函数 'cmd_scan' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第386行): 函数 'cmd_scan' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第403行): 函数 'cmd_tier' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第403行): 函数 'cmd_tier' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第422行): 函数 'cmd_apply_tier' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第422行): 函数 'cmd_apply_tier' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第446行): 函数 'cmd_check_review' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第446行): 函数 'cmd_check_review' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第483行): 函数 'cmd_stats' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第483行): 函数 'cmd_stats' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第535行): 函数 'cmd_validate' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第535行): 函数 'cmd_validate' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第565行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第216行): 'DocInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第274行): 'get_maintainers' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第284行): 'calculate_next_review' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第301行): 'scan_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第326行): 'scan_all_documents' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第386行): 'cmd_scan' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第403行): 'cmd_tier' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第422行): 'cmd_apply_tier' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第446行): 'cmd_check_review' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第483行): 'cmd_stats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第535行): 'cmd_validate' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第565行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **empty_except** (第467行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第498行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第498行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第529行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第565行): 函数 'main' 过长 (62行)
  - 建议: 考虑拆分函数

### ❌ formal-methods\.scripts\pdf-export.py

- **文件类型**: python
- **总行数**: 902
- **代码行**: 663
- **注释行**: 66
- **质量分数**: 19.0/100

**问题列表**:

- ⚠️ **import_order** (第27行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第29行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第33行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第35行): 导入顺序问题: dataclasses
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第522行): 函数名 '_build_metadata' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_type_hints** (第387行): 函数 'replace_diagram' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_type_hints** (第441行): 函数 'replace_ref' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **short_docstring** (第46行): 'ExportConfig' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第120行): 'ExportResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第407行): 'CrossRefProcessor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第462行): 'PDFExporter' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第756行): 'create_parser' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第808行): 'setup_logging' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第818行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第91行): 'from_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第96行): 'from_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第329行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第421行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第426行): 'build_ref_map' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第465行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第475行): 'cleanup' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第480行): 'check_dependencies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第636行): 'export_single' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第671行): 'export_batch' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第693行): 'export_merge' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第735行): 'export_volume' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第387行): FunctionDef 'replace_diagram' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第441行): FunctionDef 'replace_ref' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第818行): 函数 'main' 过长 (79行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第562行): 函数 'run_pandoc' 过长 (72行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\docs\formal-methods\.scripts\pdf-export.py

- **文件类型**: python
- **总行数**: 902
- **代码行**: 663
- **注释行**: 66
- **质量分数**: 19.0/100

**问题列表**:

- ⚠️ **import_order** (第27行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第29行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第33行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第35行): 导入顺序问题: dataclasses
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第522行): 函数名 '_build_metadata' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_type_hints** (第387行): 函数 'replace_diagram' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_type_hints** (第441行): 函数 'replace_ref' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **short_docstring** (第46行): 'ExportConfig' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第120行): 'ExportResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第407行): 'CrossRefProcessor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第462行): 'PDFExporter' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第756行): 'create_parser' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第808行): 'setup_logging' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第818行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第91行): 'from_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第96行): 'from_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第329行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第421行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第426行): 'build_ref_map' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第465行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第475行): 'cleanup' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第480行): 'check_dependencies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第636行): 'export_single' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第671行): 'export_batch' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第693行): 'export_merge' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第735行): 'export_volume' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第387行): FunctionDef 'replace_diagram' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第441行): FunctionDef 'replace_ref' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第818行): 函数 'main' 过长 (79行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第562行): 函数 'run_pandoc' 过长 (72行)
  - 建议: 考虑拆分函数

### ❌ .scripts\ai-assistant\auto-translator.py

- **文件类型**: python
- **总行数**: 416
- **代码行**: 320
- **注释行**: 34
- **质量分数**: 20.0/100

**问题列表**:

- ⚠️ **import_order** (第20行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第42行): 函数名 '_load_config' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第55行): 函数名 '_build_terminology' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第67行): 函数名 '_compile_preserve_patterns' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第78行): 函数名 '_setup_logger' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第187行): 函数名 '_apply_zh_to_en_rules' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第237行): 函数名 '_apply_en_to_zh_rules' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第349行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第133行): 函数 'replace_with_placeholder' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第133行): 函数 'replace_with_placeholder' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第26行): 'TranslationBlock' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第33行): 'AutoTranslator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第349行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第36行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第42行): '_load_config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): '_build_terminology' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第78行): '_setup_logger' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第103行): 'split_into_blocks' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第285行): 'translate_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第310行): 'translate_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第334行): 'batch_translate' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第133行): FunctionDef 'replace_with_placeholder' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **empty_except** (第74行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第349行): 函数 'main' 过长 (62行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第103行): 函数 'split_into_blocks' 过长 (56行)
  - 建议: 考虑拆分函数

### ❌ .scripts\validate-cross-refs.py

- **文件类型**: python
- **总行数**: 352
- **代码行**: 290
- **注释行**: 21
- **质量分数**: 21.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第10行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第15行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_type_hints** (第96行): 函数 'should_ignore_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第96行): 函数 'should_ignore_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第118行): 函数 'get_all_markdown_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第128行): 函数 'extract_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第128行): 函数 'extract_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第139行): 函数 'generate_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第139行): 函数 'generate_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第146行): 函数 'get_file_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第146行): 函数 'get_file_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第157行): 函数 'find_similar_path' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第157行): 函数 'find_similar_path' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第165行): 函数 'validate_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第165行): 函数 'validate_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第247行): 函数 'validate_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第247行): 函数 'validate_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第266行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第14行): ClassDef 'CrossRefValidator' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第15行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第165行): 'validate_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第266行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第153行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **bare_except** (第209行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **bare_except** (第203行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第15行): 函数 '**init**' 过长 (79行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第165行): 函数 'validate_link' 过长 (80行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第266行): 函数 'run' 过长 (78行)
  - 建议: 考虑拆分函数

### ❌ scripts\final-zero-error-report.py

- **文件类型**: python
- **总行数**: 518
- **代码行**: 359
- **注释行**: 51
- **质量分数**: 22.0/100

**问题列表**:

- ℹ️ **missing_type_hints** (第17行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第33行): 函数 'scan_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第46行): 函数 'extract_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第46行): 函数 'extract_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第66行): 函数 'generate_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第66行): 函数 'generate_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第97行): 函数 'is_false_positive' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第97行): 函数 'is_false_positive' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第138行): 函数 'validate_all' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第203行): 函数 'validate_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第203行): 函数 'validate_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第257行): 函数 'generate_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第257行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第476行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第16行): ClassDef 'FinalZeroErrorReport' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第17行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第33行): 'scan_files' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第46行): 'extract_anchors' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第66行): 'generate_anchors' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第97行): 'is_false_positive' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第138行): 'validate_all' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第203行): 'validate_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第257行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第476行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第63行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第63行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第189行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第138行): 函数 'validate_all' 过长 (63行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第203行): 函数 'validate_link' 过长 (52行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第257行): 函数 'generate_report' 过长 (217行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\full_cross_ref_validator_v3.py

- **文件类型**: python
- **总行数**: 454
- **代码行**: 330
- **注释行**: 35
- **质量分数**: 23.0/100

**问题列表**:

- ℹ️ **missing_type_hints** (第17行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第41行): 函数 'scan_all_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第54行): 函数 'extract_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第54行): 函数 'extract_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第84行): 函数 'generate_anchor_variants' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第84行): 函数 'generate_anchor_variants' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第114行): 函数 'normalize_link_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第114行): 函数 'normalize_link_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第131行): 函数 'is_likely_code_content' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第131行): 函数 'is_likely_code_content' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第151行): 函数 'validate_all_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第160行): 函数 'validate_file_links' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第160行): 函数 'validate_file_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第184行): 函数 'validate_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第184行): 函数 'validate_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第242行): 函数 'check_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第242行): 函数 'check_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第265行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第293行): 函数 'generate_file_statistics' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第311行): 函数 'save_reports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第311行): 函数 'save_reports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第325行): 函数 'generate_markdown_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第325行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第414行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第16行): ClassDef 'CrossRefValidator' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第17行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第184行): 'validate_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第242行): 'check_anchor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第265行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第311行): 'save_reports' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第414行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第219行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第184行): 函数 'validate_link' 过长 (56行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第325行): 函数 'generate_markdown_report' 过长 (87行)
  - 建议: 考虑拆分函数

### ❌ scripts\full_cross_ref_validator_v3.py

- **文件类型**: python
- **总行数**: 454
- **代码行**: 330
- **注释行**: 35
- **质量分数**: 23.0/100

**问题列表**:

- ℹ️ **missing_type_hints** (第17行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第41行): 函数 'scan_all_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第54行): 函数 'extract_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第54行): 函数 'extract_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第84行): 函数 'generate_anchor_variants' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第84行): 函数 'generate_anchor_variants' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第114行): 函数 'normalize_link_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第114行): 函数 'normalize_link_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第131行): 函数 'is_likely_code_content' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第131行): 函数 'is_likely_code_content' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第151行): 函数 'validate_all_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第160行): 函数 'validate_file_links' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第160行): 函数 'validate_file_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第184行): 函数 'validate_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第184行): 函数 'validate_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第242行): 函数 'check_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第242行): 函数 'check_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第265行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第293行): 函数 'generate_file_statistics' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第311行): 函数 'save_reports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第311行): 函数 'save_reports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第325行): 函数 'generate_markdown_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第325行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第414行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第16行): ClassDef 'CrossRefValidator' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第17行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第184行): 'validate_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第242行): 'check_anchor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第265行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第311行): 'save_reports' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第414行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第219行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第184行): 函数 'validate_link' 过长 (56行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第325行): 函数 'generate_markdown_report' 过长 (87行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\generate-proof-chains-pdf.py

- **文件类型**: python
- **总行数**: 464
- **代码行**: 358
- **注释行**: 25
- **质量分数**: 24.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **naming_convention** (第53行): 函数名 '_setup_font' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第63行): 函数名 '_font' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第301行): 函数 'generate_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第364行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第47行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第53行): 函数 '_setup_font' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第63行): 函数 '_font' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第63行): 函数 '_font' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第70行): 函数 'header' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第78行): 函数 'footer' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第364行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第47行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第70行): FunctionDef 'header' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第78行): FunctionDef 'footer' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **bare_except** (第60行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第60行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第286行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第286行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第102行): 函数 'generate_pdf' 过长 (142行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第247行): 函数 'merge_pdfs' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第301行): 函数 'generate_index' 过长 (60行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第364行): 函数 'main' 过长 (95行)
  - 建议: 考虑拆分函数

### ❌ scripts\generate-proof-chains-pdf.py

- **文件类型**: python
- **总行数**: 464
- **代码行**: 358
- **注释行**: 25
- **质量分数**: 24.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **naming_convention** (第53行): 函数名 '_setup_font' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第63行): 函数名 '_font' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第301行): 函数 'generate_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第364行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第47行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第53行): 函数 '_setup_font' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第63行): 函数 '_font' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第63行): 函数 '_font' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第70行): 函数 'header' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第78行): 函数 'footer' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第364行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第47行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第70行): FunctionDef 'header' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第78行): FunctionDef 'footer' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **bare_except** (第60行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第60行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第286行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第286行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第102行): 函数 'generate_pdf' 过长 (142行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第247行): 函数 'merge_pdfs' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第301行): 函数 'generate_index' 过长 (60行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第364行): 函数 'main' 过长 (95行)
  - 建议: 考虑拆分函数

### ❌ formal-methods\.scripts\theorem-dependency-graph.py

- **文件类型**: python
- **总行数**: 824
- **代码行**: 633
- **注释行**: 53
- **质量分数**: 26.0/100

**问题列表**:

- ⚠️ **import_order** (第29行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第377行): 函数名 '_calculate_statistics' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第550行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第710行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第115行): 函数 '**repr**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第128行): 函数 'add_element' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第132行): 函数 'add_edge' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第146行): 函数 'dfs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第73行): 'FormalElement' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第119行): 'DependencyGraph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第497行): 'build_dependency_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第710行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第76行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第90行): 'id' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第95行): 'short_id' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第99行): 'to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第115行): FunctionDef '**repr**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第122行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第128行): 'add_element' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第139行): 'detect_cycles' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第252行): 'filter_by_topic' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第360行): 'to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第377行): '_calculate_statistics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第146行): FunctionDef 'dfs' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第416行): 函数 'extract_formal_elements' 过长 (54行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第550行): 函数 'generate_markdown_report' 过长 (157行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第710行): 函数 'main' 过长 (109行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第304行): 函数 'to_mermaid' 过长 (54行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\docs\formal-methods\.scripts\theorem-dependency-graph.py

- **文件类型**: python
- **总行数**: 824
- **代码行**: 633
- **注释行**: 53
- **质量分数**: 26.0/100

**问题列表**:

- ⚠️ **import_order** (第29行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第377行): 函数名 '_calculate_statistics' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第550行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第710行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第115行): 函数 '**repr**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第128行): 函数 'add_element' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第132行): 函数 'add_edge' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第146行): 函数 'dfs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第73行): 'FormalElement' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第119行): 'DependencyGraph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第497行): 'build_dependency_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第710行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第76行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第90行): 'id' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第95行): 'short_id' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第99行): 'to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第115行): FunctionDef '**repr**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第122行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第128行): 'add_element' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第139行): 'detect_cycles' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第252行): 'filter_by_topic' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第360行): 'to_dict' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第377行): '_calculate_statistics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第146行): FunctionDef 'dfs' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第416行): 函数 'extract_formal_elements' 过长 (54行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第550行): 函数 'generate_markdown_report' 过长 (157行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第710行): 函数 'main' 过长 (109行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第304行): 函数 'to_mermaid' 过长 (54行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\full_cross_ref_validator.py

- **文件类型**: python
- **总行数**: 396
- **代码行**: 273
- **注释行**: 44
- **质量分数**: 26.0/100

**问题列表**:

- ⚠️ **import_order** (第386行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第18行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第38行): 函数 'scan_all_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第51行): 函数 'extract_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第51行): 函数 'extract_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第79行): 函数 'generate_anchor_from_text' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第79行): 函数 'generate_anchor_from_text' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第96行): 函数 'validate_all_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第105行): 函数 'validate_file_links' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第105行): 函数 'validate_file_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第120行): 函数 'validate_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第120行): 函数 'validate_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第179行): 函数 'check_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第179行): 函数 'check_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第200行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第228行): 函数 'generate_file_statistics' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第248行): 函数 'save_reports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第248行): 函数 'save_reports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第264行): 函数 'generate_markdown_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第264行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第348行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第17行): ClassDef 'CrossRefValidator' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第18行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第120行): 'validate_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第179行): 'check_anchor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第200行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第248行): 'save_reports' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第348行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第153行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第120行): 函数 'validate_link' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第264行): 函数 'generate_markdown_report' 过长 (82行)
  - 建议: 考虑拆分函数

### ❌ scripts\full_cross_ref_validator.py

- **文件类型**: python
- **总行数**: 396
- **代码行**: 273
- **注释行**: 44
- **质量分数**: 26.0/100

**问题列表**:

- ⚠️ **import_order** (第386行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第18行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第38行): 函数 'scan_all_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第51行): 函数 'extract_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第51行): 函数 'extract_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第79行): 函数 'generate_anchor_from_text' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第79行): 函数 'generate_anchor_from_text' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第96行): 函数 'validate_all_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第105行): 函数 'validate_file_links' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第105行): 函数 'validate_file_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第120行): 函数 'validate_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第120行): 函数 'validate_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第179行): 函数 'check_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第179行): 函数 'check_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第200行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第228行): 函数 'generate_file_statistics' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第248行): 函数 'save_reports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第248行): 函数 'save_reports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第264行): 函数 'generate_markdown_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第264行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第348行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第17行): ClassDef 'CrossRefValidator' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第18行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第120行): 'validate_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第179行): 'check_anchor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第200行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第248行): 'save_reports' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第348行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第153行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第120行): 函数 'validate_link' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第264行): 函数 'generate_markdown_report' 过长 (82行)
  - 建议: 考虑拆分函数

### ❌ .scripts\ai-assistant\doc-summarizer.py

- **文件类型**: python
- **总行数**: 597
- **代码行**: 427
- **注释行**: 53
- **质量分数**: 27.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第55行): 函数名 '_load_config' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第68行): 函数名 '_compile_patterns' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第79行): 函数名 '_setup_logger' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第537行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第510行): 函数 'save_summary' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第30行): 'DocumentSummary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第47行): 'DocumentAnalyzer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第537行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第50行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第55行): '_load_config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第68行): '_compile_patterns' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第79行): '_setup_logger' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第92行): 'read_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第101行): 'extract_title' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第109行): 'extract_formal_level' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第117行): 'extract_sections' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第219行): 'extract_references' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第225行): 'extract_key_terms' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第247行): 'generate_content_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第279行): 'generate_suggestions' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第369行): 'analyze' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第510行): 'save_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第537行): 函数 'main' 过长 (55行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第313行): 函数 'suggest_mermaid_diagrams' 过长 (54行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第418行): 函数 'generate_markdown_summary' 过长 (90行)
  - 建议: 考虑拆分函数

### ❌ java-validator-core.py

- **文件类型**: python
- **总行数**: 464
- **代码行**: 383
- **注释行**: 13
- **质量分数**: 28.0/100

**问题列表**:

- ⚠️ **import_order** (第13行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第97行): 函数 'detect_missing_imports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第97行): 函数 'detect_missing_imports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第110行): 函数 'add_missing_imports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第110行): 函数 'add_missing_imports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第123行): 函数 'wrap_code_if_needed' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第123行): 函数 'wrap_code_if_needed' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第140行): 函数 'validate_java_code' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第140行): 函数 'validate_java_code' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第213行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第343行): 函数 'generate_markdown_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第343行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第97行): FunctionDef 'detect_missing_imports' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第110行): FunctionDef 'add_missing_imports' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第123行): FunctionDef 'wrap_code_if_needed' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第140行): FunctionDef 'validate_java_code' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第213行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **bare_except** (第266行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第266行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第202行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第202行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第140行): 函数 'validate_java_code' 过长 (70行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第213行): 函数 'main' 过长 (127行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第343行): 函数 'generate_markdown_report' 过长 (116行)
  - 建议: 考虑拆分函数

### ❌ .scripts\cross-ref-recommender.py

- **文件类型**: python
- **总行数**: 562
- **代码行**: 416
- **注释行**: 37
- **质量分数**: 29.0/100

**问题列表**:

- ⚠️ **import_order** (第17行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第99行): 函数名 '_parse_document' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第131行): 函数名 '_extract_keywords' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第153行): 函数名 '_extract_refs' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第170行): 函数名 '_resolve_ref_path' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第378行): 函数名 '_path_to_node_id' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第478行): 函数名 '_save_markdown_report' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第538行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第25行): 'Document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第47行): 'ReferenceRecommendation' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第56行): 'CrossRefRecommender' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第538行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第38行): FunctionDef 'filename' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第42行): FunctionDef 'dir_name' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第75行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第99行): '_parse_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第131行): '_extract_keywords' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第187行): 'build_reference_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第382行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第465行): 'save_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第382行): 函数 'generate_report' 过长 (81行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第478行): 函数 '_save_markdown_report' 过长 (57行)
  - 建议: 考虑拆分函数

### ❌ scripts\comprehensive-fix-and-validate.py

- **文件类型**: python
- **总行数**: 595
- **代码行**: 429
- **注释行**: 52
- **质量分数**: 29.0/100

**问题列表**:

- ℹ️ **missing_type_hints** (第19行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第38行): 函数 'scan_all_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第53行): 函数 'extract_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第53行): 函数 'extract_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第78行): 函数 'generate_anchor_variants' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第78行): 函数 'generate_anchor_variants' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第110行): 函数 'is_false_positive' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第110行): 函数 'is_false_positive' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第148行): 函数 'fix_critical_issues' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第204行): 函数 'validate_all' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第274行): 函数 'validate_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第274行): 函数 'validate_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第326行): 函数 'generate_final_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第326行): 函数 'generate_final_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第534行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第18行): ClassDef 'ComprehensiveFixAndValidate' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第19行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第78行): 'generate_anchor_variants' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第110行): 'is_false_positive' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第148行): 'fix_critical_issues' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第204行): 'validate_all' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第274行): 'validate_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第534行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第75行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第260行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第148行): 函数 'fix_critical_issues' 过长 (54行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第204行): 函数 'validate_all' 过长 (68行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第326行): 函数 'generate_final_report' 过长 (206行)
  - 建议: 考虑拆分函数

### ❌ scripts\zero-error-validator.py

- **文件类型**: python
- **总行数**: 476
- **代码行**: 330
- **注释行**: 48
- **质量分数**: 29.0/100

**问题列表**:

- ℹ️ **missing_type_hints** (第19行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第42行): 函数 'scan_all_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第56行): 函数 'extract_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第56行): 函数 'extract_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第82行): 函数 'generate_anchor_variants' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第82行): 函数 'generate_anchor_variants' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第111行): 函数 'is_code_or_math_fragment' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第111行): 函数 'is_code_or_math_fragment' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第143行): 函数 'is_external_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第143行): 函数 'is_external_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第148行): 函数 'validate_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第202行): 函数 'validate_single_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第202行): 函数 'validate_single_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第261行): 函数 'generate_zero_error_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第438行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第18行): ClassDef 'ZeroErrorValidator' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第19行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第82行): 'generate_anchor_variants' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第143行): 'is_external_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第148行): 'validate_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第202行): 'validate_single_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第261行): 'generate_zero_error_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第438行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第79行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第197行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第148行): 函数 'validate_links' 过长 (52行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第202行): 函数 'validate_single_link' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第261行): 函数 'generate_zero_error_report' 过长 (175行)
  - 建议: 考虑拆分函数

### ❌ neo4j\generate_import_v2.py

- **文件类型**: python
- **总行数**: 475
- **代码行**: 379
- **注释行**: 17
- **质量分数**: 32.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第36行): 函数 'extract_id_from_line' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第36行): 函数 'extract_id_from_line' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第45行): 函数 'parse_element_id' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第45行): 函数 'parse_element_id' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第60行): 函数 'parse_full_format_line' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第60行): 函数 'parse_full_format_line' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第84行): 函数 'parse_simple_format_line' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第84行): 函数 'parse_simple_format_line' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第105行): 函数 'parse_formal_level' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第105行): 函数 'parse_formal_level' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第116行): 函数 'extract_dependencies' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第116行): 函数 'extract_dependencies' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第123行): 函数 'sanitize_cypher_string' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第123行): 函数 'sanitize_cypher_string' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第134行): 函数 'parse_registry' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第170行): 函数 'generate_nodes_cypher' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第170行): 函数 'generate_nodes_cypher' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第262行): 函数 'generate_edges_cypher' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第262行): 函数 'generate_edges_cypher' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第405行): 函数 'generate_stats' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第405行): 函数 'generate_stats' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第432行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第36行): 'extract_id_from_line' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第105行): 'parse_formal_level' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第116行): 'extract_dependencies' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第134行): 'parse_registry' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第405行): 'generate_stats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第432行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第170行): 函数 'generate_nodes_cypher' 过长 (90行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第262行): 函数 'generate_edges_cypher' 过长 (141行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\ci-check-scripts.py

- **文件类型**: python
- **总行数**: 539
- **代码行**: 400
- **注释行**: 33
- **质量分数**: 32.0/100

**问题列表**:

- ⚠️ **import_order** (第18行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第37行): 函数 'log_info' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第41行): 函数 'log_success' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第45行): 函数 'log_warning' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第49行): 函数 'log_error' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第53行): 函数 'log_section' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第392行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第27行): 'Colors' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第37行): FunctionDef 'log_info' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第41行): FunctionDef 'log_success' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第45行): FunctionDef 'log_warning' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第49行): FunctionDef 'log_error' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第53行): FunctionDef 'log_section' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第347行): 'get_changed_files' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第392行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **empty_except** (第225行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第286行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第339行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第61行): 函数 'check_markdown_syntax' 过长 (56行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第169行): 函数 'check_mermaid_syntax' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第231行): 函数 'check_internal_links' 过长 (58行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第392行): 函数 'main' 过长 (142行)
  - 建议: 考虑拆分函数

### ❌ scripts\ci-check-scripts.py

- **文件类型**: python
- **总行数**: 539
- **代码行**: 400
- **注释行**: 33
- **质量分数**: 32.0/100

**问题列表**:

- ⚠️ **import_order** (第18行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第37行): 函数 'log_info' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第41行): 函数 'log_success' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第45行): 函数 'log_warning' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第49行): 函数 'log_error' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第53行): 函数 'log_section' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第392行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第27行): 'Colors' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第37行): FunctionDef 'log_info' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第41行): FunctionDef 'log_success' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第45行): FunctionDef 'log_warning' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第49行): FunctionDef 'log_error' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第53行): FunctionDef 'log_section' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第347行): 'get_changed_files' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第392行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **empty_except** (第225行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第286行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第339行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第61行): 函数 'check_markdown_syntax' 过长 (56行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第169行): 函数 'check_mermaid_syntax' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第231行): 函数 'check_internal_links' 过长 (58行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第392行): 函数 'main' 过长 (142行)
  - 建议: 考虑拆分函数

### ❌ .improvement-tracking\scripts\outdated-tech-check.py

- **文件类型**: python
- **总行数**: 528
- **代码行**: 376
- **注释行**: 30
- **质量分数**: 33.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_return_type** (第77行): 函数 'fetch_flink_latest_version' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第98行): 函数 'parse_version' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第98行): 函数 'parse_version' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第107行): 函数 'compare_versions' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第107行): 函数 'compare_versions' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第121行): 函数 'version_diff' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第121行): 函数 'version_diff' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第131行): 函数 'get_version_status' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第131行): 函数 'get_version_status' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第159行): 函数 'extract_versions_from_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第159行): 函数 'extract_versions_from_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第191行): 函数 'scan_documents' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第191行): 函数 'scan_documents' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第212行): 函数 'analyze_outdated_docs' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第212行): 函数 'analyze_outdated_docs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第246行): 函数 'categorize_findings' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第246行): 函数 'categorize_findings' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第274行): 函数 'generate_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第274行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第453行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第131行): 'get_version_status' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第212行): 'analyze_outdated_docs' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第246行): 'categorize_findings' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第274行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第453行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第103行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第274行): 函数 'generate_report' 过长 (176行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第453行): 函数 'main' 过长 (70行)
  - 建议: 考虑拆分函数

### ❌ .scripts\knowledge-search-system.py

- **文件类型**: python
- **总行数**: 525
- **代码行**: 397
- **注释行**: 29
- **质量分数**: 33.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第19行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第179行): 函数名 '_index_formal_elements' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第263行): 函数名 '_extract_highlights' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第369行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第179行): 函数 '_index_formal_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第346行): 函数 'save_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第27行): 'SearchResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第37行): 'SearchIndex' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第48行): 'KnowledgeSearchSystem' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第369行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第61行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第85行): 'tokenize' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第98行): 'extract_title' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第106行): 'extract_snippet' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第117行): 'build_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第179行): '_index_formal_elements' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第208行): 'bm25_score' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第227行): 'search' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第263行): '_extract_highlights' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第295行): 'search_concept' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第311行): 'search_formal_element' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第315行): 'suggest_related' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第346行): 'save_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第369行): 函数 'main' 过长 (151行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第117行): 函数 'build_index' 过长 (60行)
  - 建议: 考虑拆分函数

### ❌ Flink-IoT-Authority-Alignment\Phase-8-Wearables\project-skeleton\device-simulator\cgm_simulator.py

- **文件类型**: python
- **总行数**: 339
- **代码行**: 266
- **注释行**: 23
- **质量分数**: 35.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第16行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第81行): 函数名 '_signal_handler' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第86行): 函数名 '_get_trend_arrow' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第107行): 函数名 '_simulate_meal_effect' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第114行): 函数名 '_simulate_insulin_effect' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第121行): 函数名 '_simulate_circadian_rhythm' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第242行): 函数名 '_cleanup' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第254行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第81行): 函数 '_signal_handler' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第81行): 函数 '_signal_handler' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第188行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第242行): 函数 '_cleanup' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第254行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第38行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第81行): '_signal_handler' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第242行): '_cleanup' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第254行): 函数 'main' 过长 (80行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第188行): 函数 'run' 过长 (52行)
  - 建议: 考虑拆分函数

### ❌ .scripts\kg-v2\concept-embedding-generator.py

- **文件类型**: python
- **总行数**: 608
- **代码行**: 444
- **注释行**: 47
- **质量分数**: 36.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第26行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第283行): 函数名 '_parse_stage' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第521行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第386行): 函数 'save_embeddings_hdf5' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第412行): 函数 'save_embeddings_numpy' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第424行): 函数 'save_concepts_json' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第443行): 函数 'build_annoy_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第470行): 函数 'build_faiss_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第489行): 函数 'compute_similarity_pairs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第71行): 'Concept' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第94行): 'SimilarConcept' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第521行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第127行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第261行): 'extract_all' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第283行): '_parse_stage' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第301行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第318行): 'generate_embeddings' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第343行): 'compute_similarity_matrix' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第347行): 'find_similar_concepts' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第382行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第443行): 'build_annoy_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第470行): 'build_faiss_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第489行): 'compute_similarity_pairs' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第521行): 函数 'main' 过长 (82行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第131行): 函数 'extract_from_theorem_registry' 过长 (95行)
  - 建议: 考虑拆分函数

### ❌ scripts\fix-remaining-issues.py

- **文件类型**: python
- **总行数**: 238
- **代码行**: 168
- **注释行**: 19
- **质量分数**: 36.0/100

**问题列表**:

- ℹ️ **missing_type_hints** (第14行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第19行): 函数 'scan_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第29行): 函数 'fix_common_patterns' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第93行): 函数 'add_missing_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第147行): 函数 'fix_relative_paths' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第214行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第13行): ClassDef 'FixRemainingIssues' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第14行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第19行): 'scan_files' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第29行): 'fix_common_patterns' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第147行): 'fix_relative_paths' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第214行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第87行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第141行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **empty_except** (第208行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第200行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第200行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第29行): 函数 'fix_common_patterns' 过长 (62行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第93行): 函数 'add_missing_anchors' 过长 (52行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第147行): 函数 'fix_relative_paths' 过长 (65行)
  - 建议: 考虑拆分函数

### ❌ java-validator-quick.py

- **文件类型**: python
- **总行数**: 362
- **代码行**: 299
- **注释行**: 12
- **质量分数**: 37.0/100

**问题列表**:

- ⚠️ **import_order** (第12行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第62行): 函数 'detect_missing_imports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第62行): 函数 'detect_missing_imports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第72行): 函数 'add_missing_imports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第72行): 函数 'add_missing_imports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第84行): 函数 'wrap_code' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第84行): 函数 'wrap_code' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第96行): 函数 'validate' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第96行): 函数 'validate' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第151行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第62行): FunctionDef 'detect_missing_imports' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第72行): FunctionDef 'add_missing_imports' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第84行): FunctionDef 'wrap_code' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第96行): FunctionDef 'validate' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第151行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **bare_except** (第188行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第188行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第140行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第140行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第96行): 函数 'validate' 过长 (52行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第151行): 函数 'main' 过长 (206行)
  - 建议: 考虑拆分函数

### ❌ .scripts\quality-gates\mermaid-syntax-validator.py

- **文件类型**: python
- **总行数**: 497
- **代码行**: 379
- **注释行**: 30
- **质量分数**: 39.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第18行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第169行): 函数名 '_validate_graph' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第224行): 函数名 '_validate_sequence_diagram' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第259行): 函数名 '_validate_state_diagram' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第280行): 函数名 '_validate_class_diagram' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第433行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第306行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第433行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第38行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第224行): '_validate_sequence_diagram' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第259行): '_validate_state_diagram' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第280行): '_validate_class_diagram' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第306行): 函数 'generate_report' 过长 (124行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第433行): 函数 'main' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第87行): 函数 'validate_diagram' 过长 (80行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第169行): 函数 '_validate_graph' 过长 (53行)
  - 建议: 考虑拆分函数

### ❌ .improvement-tracking\generate-freshness-metadata.py

- **文件类型**: python
- **总行数**: 425
- **代码行**: 339
- **注释行**: 17
- **质量分数**: 40.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **naming_convention** (第47行): 函数名 '_detect_tech_version' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第92行): 函数名 '_count_references' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第97行): 函数名 '_determine_content_type' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第107行): 函数名 '_calculate_confidence' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第167行): 函数名 '_calculate_next_review' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第181行): 函数名 '_analyze_file' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第391行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第270行): 函数 'save_metadata' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第276行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第391行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第42行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第92行): '_count_references' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第181行): '_analyze_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第226行): 'scan_and_generate' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第276行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第107行): 函数 '_calculate_confidence' 过长 (58行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第276行): 函数 'generate_report' 过长 (112行)
  - 建议: 考虑拆分函数

### ❌ java-validator-fast.py

- **文件类型**: python
- **总行数**: 467
- **代码行**: 383
- **注释行**: 12
- **质量分数**: 40.0/100

**问题列表**:

- ⚠️ **import_order** (第13行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第107行): 函数 'detect_missing_imports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第107行): 函数 'detect_missing_imports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第121行): 函数 'add_missing_imports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第121行): 函数 'add_missing_imports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第137行): 函数 'wrap_code_if_needed' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第137行): 函数 'wrap_code_if_needed' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第155行): 函数 'validate_java_code' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第155行): 函数 'validate_java_code' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第209行): 函数 'process_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第209行): 函数 'process_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第250行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第349行): 函数 'generate_markdown_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第349行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第209行): 'process_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第250行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **bare_except** (第271行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第271行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第155行): 函数 'validate_java_code' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第250行): 函数 'main' 过长 (96行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第349行): 函数 'generate_markdown_report' 过长 (113行)
  - 建议: 考虑拆分函数

### ❌ scripts\fix-all-issues.py

- **文件类型**: python
- **总行数**: 321
- **代码行**: 233
- **注释行**: 28
- **质量分数**: 40.0/100

**问题列表**:

- ℹ️ **missing_type_hints** (第19行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第32行): 函数 'scan_all_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第41行): 函数 'fix_duplicate_theorem_ids' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第41行): 函数 'fix_duplicate_theorem_ids' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第92行): 函数 'fix_broken_anchors' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第92行): 函数 'fix_broken_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第169行): 函数 'generate_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第169行): 函数 'generate_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第182行): 函数 'resolve_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第182行): 函数 'resolve_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第198行): 函数 'find_best_anchor_match' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第198行): 函数 'find_best_anchor_match' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第215行): 函数 'fix_broken_links' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第215行): 函数 'fix_broken_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第259行): 函数 'try_fix_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第259行): 函数 'try_fix_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第286行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第18行): ClassDef 'ComprehensiveFixer' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第19行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第41行): 'fix_duplicate_theorem_ids' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第92行): 'fix_broken_anchors' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第169行): 'generate_anchor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第215行): 'fix_broken_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第259行): 'try_fix_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第286行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第281行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第92行): 函数 'fix_broken_anchors' 过长 (75行)
  - 建议: 考虑拆分函数

### ❌ .improvement-tracking\scripts\find-orphaned-docs.py

- **文件类型**: python
- **总行数**: 298
- **代码行**: 193
- **注释行**: 21
- **质量分数**: 41.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第11行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第21行): 函数 'get_file_age_days' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第21行): 函数 'get_file_age_days' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第30行): 函数 'get_file_mtime_str' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第30行): 函数 'get_file_mtime_str' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第39行): 函数 'should_check_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第39行): 函数 'should_check_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第56行): 函数 'is_in_core_layer' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第56行): 函数 'is_in_core_layer' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第65行): 函数 'analyze_document' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第65行): 函数 'analyze_document' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第80行): 函数 'scan_directory' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第80行): 函数 'scan_directory' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第97行): 函数 'categorize_documents' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第97行): 函数 'categorize_documents' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第114行): 函数 'generate_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第114行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第236行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第65行): 'analyze_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第97行): 'categorize_documents' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第114行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第236行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第114行): 函数 'generate_report' 过长 (119行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第236行): 函数 'main' 过长 (57行)
  - 建议: 考虑拆分函数

### ❌ Flink-IoT-Authority-Alignment\Phase-8-Wearables\project-skeleton\device-simulator\hr_simulator.py

- **文件类型**: python
- **总行数**: 326
- **代码行**: 256
- **注释行**: 18
- **质量分数**: 41.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第16行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第81行): 函数名 '_signal_handler' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第86行): 函数名 '_update_activity_state' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第100行): 函数名 '_get_activity_hr_offset' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第231行): 函数名 '_cleanup' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第243行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第81行): 函数 '_signal_handler' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第81行): 函数 '_signal_handler' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第86行): 函数 '_update_activity_state' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第180行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第231行): 函数 '_cleanup' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第243行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第38行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第81行): '_signal_handler' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第86行): '_update_activity_state' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第231行): '_cleanup' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第243行): 函数 'main' 过长 (78行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第110行): 函数 'generate_reading' 过长 (53行)
  - 建议: 考虑拆分函数

### ❌ java-validator-batch.py

- **文件类型**: python
- **总行数**: 482
- **代码行**: 396
- **注释行**: 15
- **质量分数**: 41.0/100

**问题列表**:

- ⚠️ **import_order** (第13行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第105行): 函数 'detect_missing_imports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第105行): 函数 'detect_missing_imports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第119行): 函数 'add_missing_imports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第119行): 函数 'add_missing_imports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第135行): 函数 'wrap_code_if_needed' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第135行): 函数 'wrap_code_if_needed' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第153行): 函数 'validate_java_code' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第153行): 函数 'validate_java_code' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第232行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第362行): 函数 'generate_markdown_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第362行): 函数 'generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第232行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **empty_except** (第285行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **bare_except** (第221行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第221行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第153行): 函数 'validate_java_code' 过长 (76行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第232行): 函数 'main' 过长 (127行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第362行): 函数 'generate_markdown_report' 过长 (115行)
  - 建议: 考虑拆分函数

### ❌ phase2-automation\link-checker\link_checker.py

- **文件类型**: python
- **总行数**: 273
- **代码行**: 213
- **注释行**: 13
- **质量分数**: 41.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第20行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第23行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第249行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第27行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_type_hints** (第35行): 函数 'extract_links' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第35行): 函数 'extract_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第56行): 函数 'check_internal_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第56行): 函数 'check_internal_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第91行): 函数 'check_external_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第91行): 函数 'check_external_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第154行): 函数 'check_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第154行): 函数 'check_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第170行): 函数 'scan_directory' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第186行): 函数 'check_all_links' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第186行): 函数 'check_all_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第203行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第219行): 函数 'save_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第219行): 函数 'save_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第226行): 函数 'print_summary' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第226行): 函数 'print_summary' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第26行): ClassDef 'LinkChecker' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第249行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第27行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第91行): 函数 'check_external_link' 过长 (61行)
  - 建议: 考虑拆分函数

### ❌ .scripts\quality-gates\template-structure-checker.py

- **文件类型**: python
- **总行数**: 529
- **代码行**: 404
- **注释行**: 32
- **质量分数**: 42.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第27行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第187行): 函数名 '_should_apply_six_section' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第212行): 函数名 '_check_metadata' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第236行): 函数名 '_find_sections' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第273行): 函数名 '_check_theorem_ids' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第308行): 函数名 '_check_citations' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第479行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第363行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第479行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第96行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第212行): '_check_metadata' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第236行): '_find_sections' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第308行): '_check_citations' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第340行): 'check_all' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第363行): 函数 'generate_report' 过长 (113行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第106行): 函数 'check_document' 过长 (79行)
  - 建议: 考虑拆分函数

### ❌ .scripts\theorem-dependency-analyzer.py

- **文件类型**: python
- **总行数**: 408
- **代码行**: 304
- **注释行**: 28
- **质量分数**: 43.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第18行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第333行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第133行): 函数 'scan_theorem_usage' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第183行): 函数 'build_dependency_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第303行): 函数 'export_dependency_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第204行): 函数 'dfs' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第204行): 函数 'dfs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第258行): 函数 'backtrack' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第258行): 函数 'backtrack' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第26行): 'Theorem' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第42行): 'DependencyCycle' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第49行): 'TheoremDependencyAnalyzer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第333行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第63行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第183行): 'build_dependency_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第196行): 'detect_cycles' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第235行): 'calculate_metrics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第254行): 'find_proof_chains' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第303行): 'export_dependency_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第204行): FunctionDef 'dfs' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第258行): FunctionDef 'backtrack' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第333行): 函数 'main' 过长 (70行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第70行): 函数 'parse_theorem_registry' 过长 (61行)
  - 建议: 考虑拆分函数

### ❌ .scripts\ai-assistant\cross-ref-suggester.py

- **文件类型**: python
- **总行数**: 529
- **代码行**: 388
- **注释行**: 40
- **质量分数**: 44.0/100

**问题列表**:

- ⚠️ **import_order** (第18行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第21行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第61行): 函数名 '_load_config' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第74行): 函数名 '_setup_logger' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第462行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第29行): 'Document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第42行): 'LinkSuggestion' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第51行): 'CrossRefSuggester' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第462行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第54行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第61行): '_load_config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第74行): '_setup_logger' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第87行): 'extract_keywords' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第117行): 'parse_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第155行): 'build_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第195行): 'suggest_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第345行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第462行): 函数 'main' 过长 (62行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第345行): 函数 'generate_report' 过长 (81行)
  - 建议: 考虑拆分函数

### ❌ .scripts\code-example-validator.py

- **文件类型**: python
- **总行数**: 723
- **代码行**: 531
- **注释行**: 65
- **质量分数**: 44.0/100

**问题列表**:

- ⚠️ **import_order** (第19行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第258行): 函数名 '_validate_java_relaxed' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第676行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第50行): 函数 '**hash**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第92行): 函数 'update' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第638行): 函数 'save_results' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第42行): 'CodeBlock' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): 'ValidationResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第82行): 'ValidationStats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第110行): 'CodeExampleValidator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第676行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第50行): FunctionDef '**hash**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第65行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第92行): FunctionDef 'update' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第115行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第351行): 'validate_sql' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第388行): 'validate_code_block' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第455行): 'run_validation' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第505行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第638行): 'save_results' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第180行): 函数 'validate_java' 过长 (76行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第505行): 函数 'generate_report' 过长 (131行)
  - 建议: 考虑拆分函数

### ❌ neo4j\verify_deployment.py

- **文件类型**: python
- **总行数**: 348
- **代码行**: 272
- **注释行**: 18
- **质量分数**: 44.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **naming_convention** (第113行): 函数名 '_check_schema_syntax' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第134行): 函数名 '_check_nodes_syntax' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第162行): 函数名 '_check_edges_syntax' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第317行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第25行): 函数 'verify_file_structure' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第45行): 函数 'parse_nodes_cypher' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第67行): 函数 'verify_data_integrity' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第103行): 函数 'verify_cypher_syntax' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第113行): 函数 '_check_schema_syntax' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第134行): 函数 '_check_nodes_syntax' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第162行): 函数 '_check_edges_syntax' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第182行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第293行): 函数 'run_all' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第13行): ClassDef 'Neo4jDeploymentVerifier' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第317行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第14行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第25行): 'verify_file_structure' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第67行): 'verify_data_integrity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第182行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第293行): 'run_all' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第182行): 函数 'generate_report' 过长 (109行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\link-auto-fix.py

- **文件类型**: python
- **总行数**: 585
- **代码行**: 438
- **注释行**: 36
- **质量分数**: 45.0/100

**问题列表**:

- ⚠️ **import_order** (第16行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第347行): 函数名 '_should_skip_domain' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第469行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第365行): 函数 'list_redirects' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第399行): 函数 'list_broken' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第434行): 函数 'generate_fix_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第31行): 'LinkFix' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第41行): 'LinkAutoFixer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第469行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第44行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第55行): 'load_check_results' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第142行): 'mark_broken_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第188行): 'fix_redirects' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第272行): 'mark_broken_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第365行): 'list_redirects' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第399行): 'list_broken' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第434行): 'generate_fix_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第469行): 函数 'main' 过长 (111行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第188行): 函数 'fix_redirects' 过长 (82行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第272行): 函数 'mark_broken_links' 过长 (73行)
  - 建议: 考虑拆分函数

### ❌ scripts\link-auto-fix.py

- **文件类型**: python
- **总行数**: 585
- **代码行**: 438
- **注释行**: 36
- **质量分数**: 45.0/100

**问题列表**:

- ⚠️ **import_order** (第16行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第347行): 函数名 '_should_skip_domain' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第469行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第365行): 函数 'list_redirects' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第399行): 函数 'list_broken' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第434行): 函数 'generate_fix_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第31行): 'LinkFix' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第41行): 'LinkAutoFixer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第469行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第44行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第55行): 'load_check_results' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第142行): 'mark_broken_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第188行): 'fix_redirects' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第272行): 'mark_broken_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第365行): 'list_redirects' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第399行): 'list_broken' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第434行): 'generate_fix_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第469行): 函数 'main' 过长 (111行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第188行): 函数 'fix_redirects' 过长 (82行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第272行): 函数 'mark_broken_links' 过长 (73行)
  - 建议: 考虑拆分函数

### ❌ .scripts\quality-score-dashboard.py

- **文件类型**: python
- **总行数**: 665
- **代码行**: 573
- **注释行**: 4
- **质量分数**: 46.0/100

**问题列表**:

- ⚠️ **naming_convention** (第534行): 函数名 '_get_score_class' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第545行): 函数名 '_get_issue_class' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第554行): 函数名 '_generate_breakdown_rows' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第581行): 函数名 '_generate_gap_list' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第594行): 函数名 '_generate_top_issues' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第653行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第25行): 函数 'load_data' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第639行): 函数 'save_dashboard' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第17行): 'QualityDashboardGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第653行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第20行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第25行): 'load_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第38行): 'generate_html' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第554行): '_generate_breakdown_rows' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第581行): '_generate_gap_list' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第594行): '_generate_top_issues' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第639行): 'save_dashboard' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第38行): 函数 'generate_html' 过长 (494行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\add-doc-status.py

- **文件类型**: python
- **总行数**: 612
- **代码行**: 460
- **注释行**: 41
- **质量分数**: 46.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第33行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第490行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第40行): 'DocStatus' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第61行): 'ConfidenceLevel' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第106行): 'ScanResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第128行): 'DocStatusMarker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第490行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第46行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第52行): 'from_string' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第67行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第72行): 'from_string' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第116行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第175行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第285行): 'scan_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第318行): 'scan_directory' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第335行): 'add_status_header' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第395行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第490行): 函数 'main' 过长 (117行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第335行): 函数 'add_status_header' 过长 (58行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第395行): 函数 'generate_report' 过长 (92行)
  - 建议: 考虑拆分函数

### ❌ scripts\add-doc-status.py

- **文件类型**: python
- **总行数**: 612
- **代码行**: 460
- **注释行**: 41
- **质量分数**: 46.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第33行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第490行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第40行): 'DocStatus' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第61行): 'ConfidenceLevel' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第106行): 'ScanResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第128行): 'DocStatusMarker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第490行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第46行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第52行): 'from_string' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第67行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第72行): 'from_string' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第116行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第175行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第285行): 'scan_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第318行): 'scan_directory' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第335行): 'add_status_header' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第395行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第490行): 函数 'main' 过长 (117行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第335行): 函数 'add_status_header' 过长 (58行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第395行): 函数 'generate_report' 过长 (92行)
  - 建议: 考虑拆分函数

### ❌ KNOWLEDGE-GRAPH\scripts\auto_update.py

- **文件类型**: python
- **总行数**: 249
- **代码行**: 188
- **注释行**: 11
- **质量分数**: 48.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第10行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第14行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第32行): 函数名 '_load_state' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第42行): 函数名 '_save_state' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第49行): 函数名 '_get_file_hash' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第54行): 函数名 '_find_changed_files' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第77行): 函数名 '_merge_graph_data' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第218行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第42行): 函数 '_save_state' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第171行): 函数 'export_all_formats' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第188行): 函数 'run_full_update' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第23行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第113行): 函数 'update_graph' 过长 (56行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\neo4j\KNOWLEDGE-GRAPH\scripts\auto_update.py

- **文件类型**: python
- **总行数**: 249
- **代码行**: 188
- **注释行**: 11
- **质量分数**: 48.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第10行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第14行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第32行): 函数名 '_load_state' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第42行): 函数名 '_save_state' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第49行): 函数名 '_get_file_hash' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第54行): 函数名 '_find_changed_files' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第77行): 函数名 '_merge_graph_data' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第218行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第42行): 函数 '_save_state' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第171行): 函数 'export_all_formats' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第188行): 函数 'run_full_update' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第23行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第113行): 函数 'update_graph' 过长 (56行)
  - 建议: 考虑拆分函数

### ❌ .scripts\doc-similarity-analyzer.py

- **文件类型**: python
- **总行数**: 414
- **代码行**: 300
- **注释行**: 31
- **质量分数**: 49.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第20行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第343行): 函数名 '_generate_recommendations' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第370行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第310行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第28行): 'SimilarityResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第38行): 'DuplicateBlock' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第49行): 'DocSimilarityAnalyzer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第370行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第58行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第82行): 'tokenize' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第94行): 'compute_tf' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第100行): 'compute_idf' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第117行): 'cosine_similarity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第140行): 'find_duplicate_blocks' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第183行): 'analyze_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第211行): 'run_analysis' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第298行): 'find_related_docs' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第310行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第343行): '_generate_recommendations' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第211行): 函数 'run_analysis' 过长 (85行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\generate-pdfs.py

- **文件类型**: python
- **总行数**: 671
- **代码行**: 554
- **注释行**: 19
- **质量分数**: 49.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第10行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第12行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第50行): 函数 'check_dependencies' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第163行): 函数 'preprocess_markdown' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第323行): 函数 'generate_download_page' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第566行): 函数 'generate_metadata' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第587行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第233行): 'generate_pdf' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第587行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第74行): 函数 'generate_cover_page' 过长 (86行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第163行): 函数 'preprocess_markdown' 过长 (67行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第233行): 函数 'generate_pdf' 过长 (87行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第323行): 函数 'generate_download_page' 过长 (240行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第587行): 函数 'main' 过长 (79行)
  - 建议: 考虑拆分函数

### ❌ scripts\generate-pdfs.py

- **文件类型**: python
- **总行数**: 671
- **代码行**: 554
- **注释行**: 19
- **质量分数**: 49.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第10行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第12行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第50行): 函数 'check_dependencies' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第163行): 函数 'preprocess_markdown' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第323行): 函数 'generate_download_page' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第566行): 函数 'generate_metadata' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第587行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第233行): 'generate_pdf' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第587行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第74行): 函数 'generate_cover_page' 过长 (86行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第163行): 函数 'preprocess_markdown' 过长 (67行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第233行): 函数 'generate_pdf' 过长 (87行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第323行): 函数 'generate_download_page' 过长 (240行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第587行): 函数 'main' 过长 (79行)
  - 建议: 考虑拆分函数

### ❌ .scripts\concept-graph-builder.py

- **文件类型**: python
- **总行数**: 426
- **代码行**: 335
- **注释行**: 28
- **质量分数**: 50.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第18行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第392行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第317行): 函数 'export_to_neo4j' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第373行): 函数 'export_to_json' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第26行): 'Concept' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第41行): 'ConceptRelation' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第51行): 'ConceptGraphBuilder' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第392行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第79行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第103行): 'generate_concept_id' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第110行): 'extract_concepts_from_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第183行): 'extract_relations' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第222行): 'infer_additional_relations' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第266行): 'build_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第373行): 'export_to_json' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第303行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第110行): 函数 'extract_concepts_from_file' 过长 (71行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第317行): 函数 'export_to_neo4j' 过长 (54行)
  - 建议: 考虑拆分函数

### ❌ .scripts\link-health-checker-v4.1.py

- **文件类型**: python
- **总行数**: 623
- **代码行**: 518
- **注释行**: 28
- **质量分数**: 50.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第13行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第17行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第22行): 导入顺序问题: collections
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第41行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第537行): 函数 'export_json' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第28行): 'LinkStatus' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第560行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第41行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第47行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第61行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第76行): 'is_external_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第84行): 'normalize_url' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第91行): 'init_session' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第108行): 'close_session' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第114行): 'check_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第212行): 'check_batch' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第299行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第299行): 函数 'generate_report' 过长 (236行)
  - 建议: 考虑拆分函数

### ❌ fix_java_code.py

- **文件类型**: python
- **总行数**: 400
- **代码行**: 289
- **注释行**: 35
- **质量分数**: 51.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第41行): 函数 'find_java_code_blocks' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第41行): 函数 'find_java_code_blocks' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第46行): 函数 'needs_import_fix' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第46行): 函数 'needs_import_fix' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第65行): 函数 'add_missing_imports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第65行): 函数 'add_missing_imports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第126行): 函数 'fix_deprecated_api' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第126行): 函数 'fix_deprecated_api' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第178行): 函数 'process_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第178行): 函数 'process_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第244行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第287行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第126行): 'fix_deprecated_api' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第178行): 'process_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第244行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第287行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第65行): 函数 'add_missing_imports' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第178行): 函数 'process_file' 过长 (64行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第287行): 函数 'generate_report' 过长 (109行)
  - 建议: 考虑拆分函数

### ❌ i18n\translation-workflow\quality-checker.py

- **文件类型**: python
- **总行数**: 483
- **代码行**: 363
- **注释行**: 32
- **质量分数**: 51.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第20行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第472行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第28行): 'CheckResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第39行): 'FileReport' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第47行): 'QualityChecker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第472行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第50行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第59行): 'load_terminology' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第77行): 'load_verification_rules' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第84行): 'check_term_consistency' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第177行): 'check_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第292行): 'check_prohibited_terms' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第309行): 'check_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第349行): 'check_all' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第367行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第432行): 'save_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第442行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第121行): 函数 'check_markdown_format' 过长 (54行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第367行): 函数 'generate_report' 过长 (63行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\docs\i18n\translation-workflow\quality-checker.py

- **文件类型**: python
- **总行数**: 483
- **代码行**: 363
- **注释行**: 32
- **质量分数**: 51.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第20行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第472行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第28行): 'CheckResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第39行): 'FileReport' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第47行): 'QualityChecker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第472行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第50行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第59行): 'load_terminology' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第77行): 'load_verification_rules' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第84行): 'check_term_consistency' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第177行): 'check_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第292行): 'check_prohibited_terms' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第309行): 'check_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第349行): 'check_all' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第367行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第432行): 'save_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第442行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第121行): 函数 'check_markdown_format' 过长 (54行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第367行): 函数 'generate_report' 过长 (63行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\formal_element_uniqueness_check.py

- **文件类型**: python
- **总行数**: 495
- **代码行**: 375
- **注释行**: 35
- **质量分数**: 52.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第49行): 函数 'get_all_md_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第62行): 函数 'extract_formal_elements' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第62行): 函数 'extract_formal_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第91行): 函数 'check_uniqueness' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第91行): 函数 'check_uniqueness' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第108行): 函数 'check_format_validity' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第108行): 函数 'check_format_validity' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第140行): 函数 'check_continuity' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第140行): 函数 'check_continuity' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第185行): 函数 'generate_statistics' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第185行): 函数 'generate_statistics' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第206行): 函数 'generate_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第206行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第407行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第108行): 'check_format_validity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第140行): 'check_continuity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第185行): 'generate_statistics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第206行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第407行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第206行): 函数 'generate_report' 过长 (198行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第407行): 函数 'main' 过长 (83行)
  - 建议: 考虑拆分函数

### ❌ scripts\formal_element_uniqueness_check.py

- **文件类型**: python
- **总行数**: 495
- **代码行**: 375
- **注释行**: 35
- **质量分数**: 52.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第49行): 函数 'get_all_md_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第62行): 函数 'extract_formal_elements' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第62行): 函数 'extract_formal_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第91行): 函数 'check_uniqueness' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第91行): 函数 'check_uniqueness' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第108行): 函数 'check_format_validity' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第108行): 函数 'check_format_validity' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第140行): 函数 'check_continuity' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第140行): 函数 'check_continuity' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第185行): 函数 'generate_statistics' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第185行): 函数 'generate_statistics' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第206行): 函数 'generate_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第206行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第407行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第108行): 'check_format_validity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第140行): 'check_continuity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第185行): 'generate_statistics' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第206行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第407行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第206行): 函数 'generate_report' 过长 (198行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第407行): 函数 'main' 过长 (83行)
  - 建议: 考虑拆分函数

### ❌ .scripts\automation\tests\test_cross_ref_validator.py

- **文件类型**: python
- **总行数**: 143
- **代码行**: 100
- **注释行**: 16
- **质量分数**: 53.0/100

**问题列表**:

- ⚠️ **import_order** (第9行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第18行): 函数名 'setUp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第23行): 函数名 'tearDown' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第18行): 函数 'setUp' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第23行): 函数 'tearDown' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第28行): 函数 'test_is_external_url' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第36行): 函数 'test_parse_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第53行): 函数 'test_extract_anchors' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第69行): 函数 'test_extract_references' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第82行): 函数 'test_scan_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第106行): 函数 'test_validate_internal_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第18行): 'setUp' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第23行): 'tearDown' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第28行): 'test_is_external_url' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第36行): 'test_parse_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第53行): 'test_extract_anchors' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第69行): 'test_extract_references' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第82行): 'test_scan_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第106行): 'test_validate_internal_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明

### ❌ .scripts\external-link-checker.py

- **文件类型**: python
- **总行数**: 610
- **代码行**: 483
- **注释行**: 34
- **质量分数**: 53.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第12行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第16行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第38行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第99行): 函数 'load_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第118行): 函数 'save_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第532行): 函数 'export_json' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第25行): 'LinkStatus' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第48行): 'ExternalLinkChecker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第546行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第38行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第44行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第99行): 'load_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第118行): 'save_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第128行): 'get_priority' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第139行): 'is_external_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第147行): 'init_session' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第164行): 'close_session' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第387行): 函数 'generate_report' 过长 (143行)
  - 建议: 考虑拆分函数

### ❌ .scripts\ai-assistant\code-comment-generator.py

- **文件类型**: python
- **总行数**: 506
- **代码行**: 386
- **注释行**: 27
- **质量分数**: 54.0/100

**问题列表**:

- ⚠️ **import_order** (第20行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第63行): 函数名 '_load_config' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第76行): 函数名 '_setup_logger' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第437行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第26行): ClassDef 'Language' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第37行): 'FunctionInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第47行): 'ClassInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): 'CodeCommentGenerator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第437行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第58行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第63行): '_load_config' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第76行): '_setup_logger' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第89行): 'detect_language' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第293行): 'generate_line_comments' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第391行): 'process_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第425行): 'save_processed' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第437行): 函数 'main' 过长 (64行)
  - 建议: 考虑拆分函数

### ❌ neo4j\generate_import.py

- **文件类型**: python
- **总行数**: 445
- **代码行**: 336
- **注释行**: 32
- **质量分数**: 54.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第51行): 函数 'parse_formal_level' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第51行): 函数 'parse_formal_level' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第64行): 函数 'extract_dependencies' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第64行): 函数 'extract_dependencies' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第79行): 函数 'sanitize_cypher_string' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第79行): 函数 'sanitize_cypher_string' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第92行): 函数 'parse_registry' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第138行): 函数 'generate_nodes_cypher' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第138行): 函数 'generate_nodes_cypher' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第233行): 函数 'generate_edges_cypher' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第233行): 函数 'generate_edges_cypher' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第367行): 函数 'generate_stats' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第367行): 函数 'generate_stats' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第394行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第92行): 'parse_registry' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第367行): 'generate_stats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第394行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第138行): 函数 'generate_nodes_cypher' 过长 (93行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第233行): 函数 'generate_edges_cypher' 过长 (132行)
  - 建议: 考虑拆分函数

### ❌ tools\fix-broken-links.py

- **文件类型**: python
- **总行数**: 563
- **代码行**: 423
- **注释行**: 46
- **质量分数**: 54.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_return_type** (第547行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第252行): 函数 'fix_specific_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第406行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第464行): 函数 'generate_reports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第88行): 'FixResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第99行): 'BrokenLinkFixer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第547行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第102行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第135行): 'is_anchor_only' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第160行): 'fix_external_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第406行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第464行): 'generate_reports' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第167行): 函数 'process_file' 过长 (83行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第252行): 函数 'fix_specific_files' 过长 (152行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第406行): 函数 'run' 过长 (56行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第464行): 函数 'generate_reports' 过长 (80行)
  - 建议: 考虑拆分函数

### ❌ .improvement-tracking\apply-freshness-tags.py

- **文件类型**: python
- **总行数**: 262
- **代码行**: 190
- **注释行**: 16
- **质量分数**: 55.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **naming_convention** (第22行): 函数名 '_load_metadata' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第27行): 函数名 '_generate_frontmatter' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第53行): 函数名 '_has_existing_frontmatter' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第57行): 函数名 '_has_freshness_tag' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第61行): 函数名 '_remove_old_frontmatter' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第206行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第206行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第17行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第162行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第206行): 函数 'main' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第72行): 函数 'apply_tag_to_file' 过长 (64行)
  - 建议: 考虑拆分函数

### ❌ .scripts\automation\tests\test_mermaid_checker.py

- **文件类型**: python
- **总行数**: 157
- **代码行**: 123
- **注释行**: 6
- **质量分数**: 55.0/100

**问题列表**:

- ⚠️ **import_order** (第9行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第18行): 函数名 'setUp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第23行): 函数名 'tearDown' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第18行): 函数 'setUp' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第23行): 函数 'tearDown' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第28行): 函数 'test_detect_diagram_type' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第51行): 函数 'test_parse_flowchart' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第74行): 函数 'test_parse_flowchart_with_undefined_nodes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第90行): 函数 'test_parse_sequence_diagram' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第105行): 函数 'test_scan_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第140行): 函数 'test_check_empty_diagram' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第18行): 'setUp' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第23行): 'tearDown' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第28行): 'test_detect_diagram_type' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第74行): 'test_parse_flowchart_with_undefined_nodes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第90行): 'test_parse_sequence_diagram' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第105行): 'test_scan_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第140行): 'test_check_empty_diagram' 的文档字符串过短
  - 建议: 提供更详细的文档说明

### ❌ i18n\translation-workflow\sync-tracker.py

- **文件类型**: python
- **总行数**: 356
- **代码行**: 270
- **注释行**: 20
- **质量分数**: 55.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第16行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第346行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第24行): 'SyncTracker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第346行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第38行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第43行): 'load_state' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): 'save_state' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第65行): 'compute_file_hash' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第73行): 'scan_source_files' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第102行): 'detect_changes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第166行): 'determine_priority' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第195行): 'generate_translation_queue' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第238行): 'save_queue' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第246行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第311行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第102行): 函数 'detect_changes' 过长 (62行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第246行): 函数 'generate_report' 过长 (63行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\docs\i18n\translation-workflow\sync-tracker.py

- **文件类型**: python
- **总行数**: 356
- **代码行**: 270
- **注释行**: 20
- **质量分数**: 55.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第16行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第346行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第24行): 'SyncTracker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第346行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第38行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第43行): 'load_state' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): 'save_state' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第65行): 'compute_file_hash' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第73行): 'scan_source_files' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第102行): 'detect_changes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第166行): 'determine_priority' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第195行): 'generate_translation_queue' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第238行): 'save_queue' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第246行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第311行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第102行): 函数 'detect_changes' 过长 (62行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第246行): 函数 'generate_report' 过长 (63行)
  - 建议: 考虑拆分函数

### ❌ .scripts\fix-external-links.py

- **文件类型**: python
- **总行数**: 403
- **代码行**: 320
- **注释行**: 12
- **质量分数**: 56.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第13行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第364行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第180行): 函数 'fix_all_redirects' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第223行): 函数 'mark_all_dead_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第271行): 函数 'generate_archive_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第348行): 函数 'print_summary' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第153行): 函数 'replace_with_marker' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第153行): 函数 'replace_with_marker' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第19行): 'ExternalLinkFixer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第364行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第348行): 'print_summary' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第153行): FunctionDef 'replace_with_marker' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第44行): 函数 'fix_redirects_in_file' 过长 (80行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第126行): 函数 'mark_dead_links' 过长 (52行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第271行): 函数 'generate_archive_report' 过长 (75行)
  - 建议: 考虑拆分函数

### ❌ .scripts\link-health-checker.py

- **文件类型**: python
- **总行数**: 600
- **代码行**: 472
- **注释行**: 40
- **质量分数**: 56.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第12行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第16行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第21行): 导入顺序问题: collections
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第39行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第522行): 函数 'export_json' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第27行): 'LinkStatus' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第49行): 'LinkHealthChecker' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第537行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第39行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第45行): FunctionDef 'to_dict' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第84行): 'is_external_link' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第101行): 'init_session' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第118行): 'close_session' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第317行): 'get_suggestion' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第346行): 函数 'generate_report' 过长 (174行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\link-quick-fix.py

- **文件类型**: python
- **总行数**: 418
- **代码行**: 311
- **注释行**: 20
- **质量分数**: 56.0/100

**问题列表**:

- ⚠️ **import_order** (第16行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第328行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第252行): 函数 'interactive_fix' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第22行): 'LinkQuickFixer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第328行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第25行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第67行): 'replace_url_in_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第252行): 'interactive_fix' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第328行): 函数 'main' 过长 (85行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第67行): 函数 'replace_url_in_file' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第120行): 函数 'find_and_replace_all' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第173行): 函数 'fix_specific_link' 过长 (77行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第252行): 函数 'interactive_fix' 过长 (73行)
  - 建议: 考虑拆分函数

### ❌ scripts\link-quick-fix.py

- **文件类型**: python
- **总行数**: 418
- **代码行**: 311
- **注释行**: 20
- **质量分数**: 56.0/100

**问题列表**:

- ⚠️ **import_order** (第16行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第328行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第252行): 函数 'interactive_fix' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第22行): 'LinkQuickFixer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第328行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第25行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第67行): 'replace_url_in_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第252行): 'interactive_fix' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第328行): 函数 'main' 过长 (85行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第67行): 函数 'replace_url_in_file' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第120行): 函数 'find_and_replace_all' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第173行): 函数 'fix_specific_link' 过长 (77行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第252行): 函数 'interactive_fix' 过长 (73行)
  - 建议: 考虑拆分函数

### ❌ .scripts\cross-ref-fixer.py

- **文件类型**: python
- **总行数**: 196
- **代码行**: 145
- **注释行**: 15
- **质量分数**: 57.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第10行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第14行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第51行): 函数 'get_all_markdown_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第58行): 函数 'find_broken_refs' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第58行): 函数 'find_broken_refs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第90行): 函数 'fix_file_ref' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第90行): 函数 'fix_file_ref' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第110行): 函数 'fix_anchor' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第110行): 函数 'fix_anchor' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第125行): 函数 'fix_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第125行): 函数 'fix_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第159行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第13行): ClassDef 'CrossRefFixer' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第14行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第58行): 'find_broken_refs' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第90行): 'fix_file_ref' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第110行): 'fix_anchor' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第125行): 'fix_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第159行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明

### ❌ .scripts\flink-version-tracking\check-new-releases.py

- **文件类型**: python
- **总行数**: 363
- **代码行**: 280
- **注释行**: 22
- **质量分数**: 57.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第17行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第21行): 导入顺序问题: dataclasses
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第130行): 函数名 '_parse_flip_table' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第153行): 函数名 '_parse_flip_content' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第280行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第54行): 'FLIPStatus' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第280行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第48行): FunctionDef '**str**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第62行): FunctionDef '**str**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第69行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第180行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第229行): 'update_version_tracking' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第280行): 函数 'main' 过长 (78行)
  - 建议: 考虑拆分函数

### ❌ .scripts\knowledge-graph\generate-sample-data.py

- **文件类型**: python
- **总行数**: 454
- **代码行**: 391
- **注释行**: 5
- **质量分数**: 57.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第10行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第17行): 函数 'generate_concept_graph' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第103行): 函数 'generate_cypher_script' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第146行): 函数 'generate_theorem_dependencies' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第251行): 函数 'generate_similarity_matrix' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第286行): 函数 'generate_clusters' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第335行): 函数 'generate_content_gaps' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第381行): 函数 'generate_search_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第422行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第17行): 'generate_concept_graph' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第251行): 'generate_similarity_matrix' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第286行): 'generate_clusters' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第381行): 'generate_search_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第422行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第17行): 函数 'generate_concept_graph' 过长 (83行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第146行): 函数 'generate_theorem_dependencies' 过长 (102行)
  - 建议: 考虑拆分函数

### ❌ .scripts\code-example-fixer.py

- **文件类型**: python
- **总行数**: 516
- **代码行**: 359
- **注释行**: 56
- **质量分数**: 58.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第469行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第310行): 函数 'run_fixer' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第450行): 函数 'save_fixes_log' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第274行): 函数 'replace_code_block' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第274行): 函数 'replace_code_block' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第24行): 'FixResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第34行): 'CodeExampleFixer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第469行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第37行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第161行): 'fix_yaml_issues' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第193行): 'fix_sql_issues' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第237行): 'fix_code_block' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第310行): 'run_fixer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第372行): 'generate_fix_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第450行): 'save_fixes_log' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第274行): FunctionDef 'replace_code_block' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第310行): 函数 'run_fixer' 过长 (60行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第372行): 函数 'generate_fix_report' 过长 (76行)
  - 建议: 考虑拆分函数

### ❌ .scripts\cross-ref-checker-v2.py

- **文件类型**: python
- **总行数**: 435
- **代码行**: 335
- **注释行**: 26
- **质量分数**: 58.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第20行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第396行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第112行): 函数 'build_anchor_cache' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第368行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第28行): 'CrossRefIssue' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第41行): 'CheckStats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第396行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第57行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第112行): 'build_anchor_cache' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第197行): 'check_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第295行): 'run_check' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **empty_except** (第170行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第197行): 函数 'check_file' 过长 (66行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第295行): 函数 'run_check' 过长 (71行)
  - 建议: 考虑拆分函数

### ❌ pdf-export.py

- **文件类型**: python
- **总行数**: 573
- **代码行**: 423
- **注释行**: 39
- **质量分数**: 58.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第26行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第28行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第460行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ⚠️ **high_complexity** (第78行): 函数 'get_latex_template' 过长 (71行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第190行): 函数 'export_single' 过长 (108行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第301行): 函数 'export_batch' 过长 (78行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第382行): 函数 'export_merge' 过长 (75行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第460行): 函数 'main' 过长 (108行)
  - 建议: 考虑拆分函数

### ❌ phase2-automation\theorem-checker\check_theorems.py

- **文件类型**: python
- **总行数**: 254
- **代码行**: 198
- **注释行**: 17
- **质量分数**: 58.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_return_type** (第215行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第30行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第37行): 函数 'scan_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第41行): 函数 'is_valid_theorem_id' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第41行): 函数 'is_valid_theorem_id' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第46行): 函数 'extract_theorems' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第46行): 函数 'extract_theorems' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第75行): 函数 'extract_refs' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第75行): 函数 'extract_refs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第98行): 函数 'check_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第98行): 函数 'check_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第130行): 函数 'check_duplicates' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第141行): 函数 'check_undefined_refs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第154行): 函数 'check_sequential' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第175行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第190行): 函数 'print_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第190行): 函数 'print_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第29行): ClassDef 'TheoremChecker' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第215行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第30行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串

### ❌ release\v3.0.0\tools\pdf-export.py

- **文件类型**: python
- **总行数**: 573
- **代码行**: 423
- **注释行**: 39
- **质量分数**: 58.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第26行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **import_order** (第28行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第460行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ⚠️ **high_complexity** (第78行): 函数 'get_latex_template' 过长 (71行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第190行): 函数 'export_single' 过长 (108行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第301行): 函数 'export_batch' 过长 (78行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第382行): 函数 'export_merge' 过长 (75行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第460行): 函数 'main' 过长 (108行)
  - 建议: 考虑拆分函数

### ❌ validate_python.py

- **文件类型**: python
- **总行数**: 117
- **代码行**: 107
- **注释行**: 1
- **质量分数**: 58.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第3行): 导入顺序问题: sys
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_type_hints** (第8行): 函数 'extract_python_blocks' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第8行): 函数 'extract_python_blocks' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第27行): 函数 'check_syntax' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第27行): 函数 'check_syntax' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第44行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第70行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第8行): FunctionDef 'extract_python_blocks' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第27行): FunctionDef 'check_syntax' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第44行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第70行): FunctionDef 'generate_report' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **bare_except** (第24行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **bare_except** (第42行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第42行): 空的异常处理块
  - 建议: 处理异常或记录日志

### ❌ .scripts\automation\tests\test_template_validator.py

- **文件类型**: python
- **总行数**: 153
- **代码行**: 100
- **注释行**: 13
- **质量分数**: 59.0/100

**问题列表**:

- ⚠️ **import_order** (第9行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第18行): 函数名 'setUp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第23行): 函数名 'tearDown' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第18行): 函数 'setUp' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第23行): 函数 'tearDown' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第28行): 函数 'test_classify_section' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第50行): 函数 'test_extract_formal_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第64行): 函数 'test_count_mermaid_diagrams' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第82行): 函数 'test_validate_file_valid' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第132行): 函数 'test_validate_file_invalid' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第18行): 'setUp' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第23行): 'tearDown' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第28行): 'test_classify_section' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第50行): 'test_extract_formal_elements' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第82行): 'test_validate_file_valid' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第132行): 'test_validate_file_invalid' 的文档字符串过短
  - 建议: 提供更详细的文档说明

### ❌ java-validator-static.py

- **文件类型**: python
- **总行数**: 387
- **代码行**: 306
- **注释行**: 25
- **质量分数**: 59.0/100

**问题列表**:

- ℹ️ **missing_type_hints** (第74行): 函数 'detect_missing_imports' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第74行): 函数 'detect_missing_imports' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第85行): 函数 'detect_deprecated_apis' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第85行): 函数 'detect_deprecated_apis' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第94行): 函数 'detect_syntax_issues' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第94行): 函数 'detect_syntax_issues' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第119行): 函数 'analyze_code' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第119行): 函数 'analyze_code' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第168行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第85行): 'detect_deprecated_apis' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第94行): 'detect_syntax_issues' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第119行): 'analyze_code' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第168行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **bare_except** (第201行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第201行): 空的异常处理块
  - 建议: 处理异常或记录日志
- ⚠️ **high_complexity** (第168行): 函数 'main' 过长 (214行)
  - 建议: 考虑拆分函数

### ❌ .scripts\six-section-validator.py

- **文件类型**: python
- **总行数**: 428
- **代码行**: 329
- **注释行**: 29
- **质量分数**: 60.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第19行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第387行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第367行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第27行): 'ValidationIssue' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第38行): 'ValidationStats' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第48行): 'SixSectionValidator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第387行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第76行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第100行): 'check_section_structure' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第131行): 'check_formal_elements' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第234行): 'check_header_metadata' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第268行): 'check_references_format' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第299行): 'validate_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第324行): 'run_validation' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第367行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第179行): 函数 'check_mermaid_diagrams' 过长 (53行)
  - 建议: 考虑拆分函数

### ❌ formal-methods\.scripts\fix-mermaid-syntax.py

- **文件类型**: python
- **总行数**: 449
- **代码行**: 317
- **注释行**: 44
- **质量分数**: 60.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第285行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第368行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第85行): 函数 'log' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第31行): 'FixRecord' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第41行): 'FileReport' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第285行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第368行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第78行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第85行): 'log' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第174行): 'process_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第242行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第285行): 函数 'generate_report' 过长 (80行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第368行): 函数 'main' 过长 (76行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第174行): 函数 'process_file' 过长 (59行)
  - 建议: 考虑拆分函数

### ❌ formal-methods\90-examples\stream\signal-processing.py

- **文件类型**: python
- **总行数**: 581
- **代码行**: 384
- **注释行**: 64
- **质量分数**: 60.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第26行): 导入顺序问题: typing
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第491行): 函数 'print_signal' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第497行): 函数 'write_wav' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第525行): 函数 'demo' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第60行): 'cosine_wave' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第86行): 'sawtooth_wave' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第95行): 'triangle_wave' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第108行): 'white_noise' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第115行): 'impulse_train' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第167行): 'take' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第172行): 'drop' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第434行): 'add_signals' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第440行): 'multiply_signals' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第525行): 'demo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第525行): 函数 'demo' 过长 (51行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\docs\formal-methods\.scripts\fix-mermaid-syntax.py

- **文件类型**: python
- **总行数**: 449
- **代码行**: 317
- **注释行**: 44
- **质量分数**: 60.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第285行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第368行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第85行): 函数 'log' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第31行): 'FixRecord' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第41行): 'FileReport' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第285行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第368行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第78行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第85行): 'log' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第174行): 'process_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **bare_except** (第242行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **high_complexity** (第285行): 函数 'generate_report' 过长 (80行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第368行): 函数 'main' 过长 (76行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第174行): 函数 'process_file' 过长 (59行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\docs\formal-methods\90-examples\stream\signal-processing.py

- **文件类型**: python
- **总行数**: 581
- **代码行**: 384
- **注释行**: 64
- **质量分数**: 60.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第26行): 导入顺序问题: typing
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第491行): 函数 'print_signal' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第497行): 函数 'write_wav' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第525行): 函数 'demo' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第60行): 'cosine_wave' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第86行): 'sawtooth_wave' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第95行): 'triangle_wave' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第108行): 'white_noise' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第115行): 'impulse_train' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第167行): 'take' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第172行): 'drop' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第434行): 'add_signals' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第440行): 'multiply_signals' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第525行): 'demo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第525行): 函数 'demo' 过长 (51行)
  - 建议: 考虑拆分函数

### ❌ .scripts\automation\tests\test_formal_element_tracker.py

- **文件类型**: python
- **总行数**: 116
- **代码行**: 77
- **注释行**: 8
- **质量分数**: 61.0/100

**问题列表**:

- ⚠️ **import_order** (第9行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第18行): 函数名 'setUp' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ⚠️ **naming_convention** (第23行): 函数名 'tearDown' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第18行): 函数 'setUp' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第23行): 函数 'tearDown' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第28行): 函数 'test_scan_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第62行): 函数 'test_type_mapping' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第78行): 函数 'test_analyze_conflicts_duplicate' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第97行): 函数 'test_suggest_new_id' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第18行): 'setUp' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第23行): 'tearDown' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第28行): 'test_scan_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第62行): 'test_type_mapping' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第78行): 'test_analyze_conflicts_duplicate' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第97行): 'test_suggest_new_id' 的文档字符串过短
  - 建议: 提供更详细的文档说明

### ❌ KNOWLEDGE-GRAPH\scripts\extract_entities.py

- **文件类型**: python
- **总行数**: 367
- **代码行**: 291
- **注释行**: 20
- **质量分数**: 61.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第10行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第162行): 函数名 '_doc_path_to_id' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第319行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第28行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第43行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第28行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第43行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第77行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第83行): 函数 'extract_from_file' 过长 (77行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第166行): 函数 'extract_from_directory' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第225行): 函数 'build_dependency_graph' 过长 (91行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\neo4j\KNOWLEDGE-GRAPH\scripts\extract_entities.py

- **文件类型**: python
- **总行数**: 367
- **代码行**: 291
- **注释行**: 20
- **质量分数**: 61.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第10行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第162行): 函数名 '_doc_path_to_id' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第319行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第28行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第43行): 函数 '**post_init**' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第28行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第43行): FunctionDef '**post_init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第77行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第83行): 函数 'extract_from_file' 过长 (77行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第166行): 函数 'extract_from_directory' 过长 (57行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第225行): 函数 'build_dependency_graph' 过长 (91行)
  - 建议: 考虑拆分函数

### ❌ .scripts\fix_external_links.py

- **文件类型**: python
- **总行数**: 344
- **代码行**: 255
- **注释行**: 30
- **质量分数**: 62.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第81行): 函数 'load_analysis' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第85行): 函数 'get_replacement' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第85行): 函数 'get_replacement' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第98行): 函数 'fix_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第98行): 函数 'fix_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第140行): 函数 'run_fix' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第241行): 函数 'generate_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第241行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第75行): ClassDef 'LinkFixer' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第76行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第81行): FunctionDef 'load_analysis' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第85行): 'get_replacement' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第140行): 'run_fix' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第241行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第140行): 函数 'run_fix' 过长 (99行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第241行): 函数 'generate_report' 过长 (91行)
  - 建议: 考虑拆分函数

### ❌ i18n\translation-workflow\auto-translate.py

- **文件类型**: python
- **总行数**: 416
- **代码行**: 279
- **注释行**: 42
- **质量分数**: 62.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第19行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第390行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第30行): 'TranslationTask' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第39行): 'AutoTranslator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第390行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第42行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第48行): 'load_terminology' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第76行): 'create_translation_prompt' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第209行): 'compute_file_hash' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第76行): 函数 'create_translation_prompt' 过长 (71行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第223行): 函数 'translate_file' 过长 (58行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第283行): 函数 'generate_ai_translation_template' 过长 (63行)
  - 建议: 考虑拆分函数

### ❌ phase2-automation\cross-ref-checker\check_refs.py

- **文件类型**: python
- **总行数**: 224
- **代码行**: 173
- **注释行**: 16
- **质量分数**: 62.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_return_type** (第190行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第25行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第32行): 函数 'scan_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第36行): 函数 'extract_defined_refs' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第36行): 函数 'extract_defined_refs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第64行): 函数 'extract_used_refs' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第64行): 函数 'extract_used_refs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第92行): 函数 'check_file_refs' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第92行): 函数 'check_file_refs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第122行): 函数 'validate_refs' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第135行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第160行): 函数 'save_report' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第160行): 函数 'save_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第166行): 函数 'print_summary' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第166行): 函数 'print_summary' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第24行): ClassDef 'CrossRefChecker' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第190行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第25行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串

### ❌ release\v3.0.0\docs\i18n\translation-workflow\auto-translate.py

- **文件类型**: python
- **总行数**: 416
- **代码行**: 279
- **注释行**: 42
- **质量分数**: 62.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第19行): 导入顺序问题: json
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第390行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第30行): 'TranslationTask' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第39行): 'AutoTranslator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第390行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第42行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第48行): 'load_terminology' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第76行): 'create_translation_prompt' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第209行): 'compute_file_hash' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第76行): 函数 'create_translation_prompt' 过长 (71行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第223行): 函数 'translate_file' 过长 (58行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第283行): 函数 'generate_ai_translation_template' 过长 (63行)
  - 建议: 考虑拆分函数

### ❌ .scripts\formal-element-checker.py

- **文件类型**: python
- **总行数**: 535
- **代码行**: 415
- **注释行**: 32
- **质量分数**: 63.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第24行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ⚠️ **naming_convention** (第281行): 函数名 '_should_check' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第475行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第329行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第475行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第83行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第309行): 'check_all' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第329行): 函数 'generate_report' 过长 (143行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第475行): 函数 'main' 过长 (55行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第148行): 函数 'check_document' 过长 (131行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\six_section_audit.py

- **文件类型**: python
- **总行数**: 421
- **代码行**: 327
- **注释行**: 19
- **质量分数**: 63.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第295行): 函数 'print_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第372行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第391行): 函数 'generate_fix_task_list' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第17行): 'SectionCheck' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第28行): 'DocumentAuditResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第372行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第391行): 'generate_fix_task_list' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第59行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第124行): 'audit_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第208行): 'run_audit' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第222行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第295行): 函数 'print_report' 过长 (74行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第124行): 函数 'audit_document' 过长 (82行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第222行): 函数 'generate_report' 过长 (70行)
  - 建议: 考虑拆分函数

### ❌ six_section_audit.py

- **文件类型**: python
- **总行数**: 421
- **代码行**: 327
- **注释行**: 19
- **质量分数**: 63.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第295行): 函数 'print_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第372行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第391行): 函数 'generate_fix_task_list' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第17行): 'SectionCheck' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第28行): 'DocumentAuditResult' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第372行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第391行): 'generate_fix_task_list' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第59行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第124行): 'audit_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第208行): 'run_audit' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第222行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第295行): 函数 'print_report' 过长 (74行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第124行): 函数 'audit_document' 过长 (82行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第222行): 函数 'generate_report' 过长 (70行)
  - 建议: 考虑拆分函数

### ❌ .scripts\formal-element-auto-number.py

- **文件类型**: python
- **总行数**: 435
- **代码行**: 338
- **注释行**: 22
- **质量分数**: 64.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第19行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第394行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第338行): 函数 'apply_fixes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第367行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第27行): 'FormalElement' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第41行): 'NumberingIssue' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第394行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第103行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第203行): 'check_duplicates' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第237行): 'analyze_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第290行): 'run_analysis' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第338行): 'apply_fixes' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第367行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第237行): 函数 'analyze_file' 过长 (51行)
  - 建议: 考虑拆分函数

### ❌ tools\fix-duplicate-ids.py

- **文件类型**: python
- **总行数**: 254
- **代码行**: 196
- **注释行**: 18
- **质量分数**: 64.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **naming_convention** (第185行): 函数名 '_generate_markdown_report' 不符合snake_case规范
  - 建议: 使用小写字母和下划线命名函数
- ℹ️ **missing_return_type** (第231行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第38行): 函数 'load_validation_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第134行): 函数 'run' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第163行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第185行): 函数 '_generate_markdown_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第17行): ClassDef 'DuplicateIDFixer' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第231行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第18行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第38行): 'load_validation_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第46行): 'group_issues_by_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第134行): 'run' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第163行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第64行): 函数 'fix_file' 过长 (68行)
  - 建议: 考虑拆分函数

### ❌ .scripts\fix-cross-refs-v2.py

- **文件类型**: python
- **总行数**: 174
- **代码行**: 123
- **注释行**: 16
- **质量分数**: 65.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第12行): 函数 'get_relative_path' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第12行): 函数 'get_relative_path' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第24行): 函数 'fix_links_in_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第24行): 函数 'fix_links_in_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第105行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第37行): 函数 'replace_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第37行): 函数 'replace_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第105行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第37行): FunctionDef 'replace_link' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第24行): 函数 'fix_links_in_file' 过长 (79行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第105行): 函数 'main' 过长 (65行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第37行): 函数 'replace_link' 过长 (53行)
  - 建议: 考虑拆分函数

### ❌ .scripts\kg-v2\generate-static-data.py

- **文件类型**: python
- **总行数**: 259
- **代码行**: 195
- **注释行**: 17
- **质量分数**: 65.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_return_type** (第19行): 函数 'ensure_output_dir' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第23行): 函数 'parse_theorem_registry' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第57行): 函数 'extract_nodes_from_html' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第121行): 函数 'generate_links' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第121行): 函数 'generate_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第167行): 函数 'generate_metadata' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第180行): 函数 'generate_graph_data' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第204行): 函数 'generate_chunked_data' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第235行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第19行): 'ensure_output_dir' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第121行): 'generate_links' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第167行): 'generate_metadata' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第180行): 'generate_graph_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第235行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第57行): 函数 'extract_nodes_from_html' 过长 (62行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\tools\scripts\add-prospective-banners.py

- **文件类型**: python
- **总行数**: 494
- **代码行**: 376
- **注释行**: 37
- **质量分数**: 65.0/100

**问题列表**:

- ⚠️ **import_order** (第18行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第305行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第411行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第63行): 'DocumentInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第76行): 'ProcessingReport' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第130行): 'generate_banner' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第177行): 'scan_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第216行): 'scan_all_documents' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第268行): 'add_banner_to_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第305行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第411行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第305行): 函数 'generate_report' 过长 (104行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第411行): 函数 'main' 过长 (79行)
  - 建议: 考虑拆分函数

### ❌ scripts\add-prospective-banners.py

- **文件类型**: python
- **总行数**: 494
- **代码行**: 376
- **注释行**: 37
- **质量分数**: 65.0/100

**问题列表**:

- ⚠️ **import_order** (第18行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第305行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第411行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第63行): 'DocumentInfo' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第76行): 'ProcessingReport' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第130行): 'generate_banner' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第177行): 'scan_document' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第216行): 'scan_all_documents' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第268行): 'add_banner_to_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第305行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第411行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第305行): 函数 'generate_report' 过长 (104行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第411行): 函数 'main' 过长 (79行)
  - 建议: 考虑拆分函数

### ❌ .scripts\mermaid-syntax-checker.py

- **文件类型**: python
- **总行数**: 416
- **代码行**: 317
- **注释行**: 23
- **质量分数**: 66.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第19行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第375行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第352行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第41行): 'SyntaxError' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第375行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第83行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **short_docstring** (第137行): 'detect_diagram_type' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第153行): 'count_nodes_and_edges' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第185行): 'validate_syntax_basic' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第261行): 'analyze_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第315行): 'run_check' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第352行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第261行): 函数 'analyze_file' 过长 (52行)
  - 建议: 考虑拆分函数

### ❌ .scripts\kg-v2\optimize-assets.py

- **文件类型**: python
- **总行数**: 332
- **代码行**: 269
- **注释行**: 12
- **质量分数**: 67.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第9行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第16行): 函数 'optimize_json_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第52行): 函数 'generate_service_worker' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第163行): 函数 'generate_manifest' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第204行): 函数 'copy_and_optimize_html' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第248行): 函数 'generate_404_page' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第306行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第248行): 'generate_404_page' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第306行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第52行): 函数 'generate_service_worker' 过长 (109行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第248行): 函数 'generate_404_page' 过长 (56行)
  - 建议: 考虑拆分函数

### ❌ phase2-automation\mermaid-renderer\render_mermaid.py

- **文件类型**: python
- **总行数**: 119
- **代码行**: 93
- **注释行**: 3
- **质量分数**: 67.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第21行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第97行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第25行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_type_hints** (第29行): 函数 'extract_mermaid_blocks' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第29行): 函数 'extract_mermaid_blocks' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第34行): 函数 'render_diagram' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第34行): 函数 'render_diagram' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第59行): 函数 'process_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第59行): 函数 'process_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第80行): 函数 'batch_process' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第80行): 函数 'batch_process' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第24行): ClassDef 'MermaidRenderer' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第97行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第25行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串

### ❌ release\v3.0.0\tools\scripts\formal_element_final_check.py

- **文件类型**: python
- **总行数**: 523
- **代码行**: 413
- **注释行**: 33
- **质量分数**: 67.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第37行): 函数 'get_all_md_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第50行): 函数 'extract_formal_elements' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第50行): 函数 'extract_formal_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第79行): 函数 'analyze_uniqueness' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第79行): 函数 'analyze_uniqueness' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第92行): 函数 'analyze_continuity' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第92行): 函数 'analyze_continuity' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第137行): 函数 'check_format_issues' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第137行): 函数 'check_format_issues' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第165行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第79行): 'analyze_uniqueness' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第92行): 'analyze_continuity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第137行): 'check_format_issues' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第165行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第165行): 函数 'main' 过长 (353行)
  - 建议: 考虑拆分函数

### ❌ scripts\formal_element_final_check.py

- **文件类型**: python
- **总行数**: 523
- **代码行**: 413
- **注释行**: 33
- **质量分数**: 67.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第37行): 函数 'get_all_md_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第50行): 函数 'extract_formal_elements' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第50行): 函数 'extract_formal_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第79行): 函数 'analyze_uniqueness' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第79行): 函数 'analyze_uniqueness' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第92行): 函数 'analyze_continuity' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第92行): 函数 'analyze_continuity' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第137行): 函数 'check_format_issues' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第137行): 函数 'check_format_issues' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第165行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第79行): 'analyze_uniqueness' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第92行): 'analyze_continuity' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第137行): 'check_format_issues' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第165行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第165行): 函数 'main' 过长 (353行)
  - 建议: 考虑拆分函数

### ❌ examples\python\table-api\table_api_example.py

- **文件类型**: python
- **总行数**: 351
- **代码行**: 279
- **注释行**: 19
- **质量分数**: 68.0/100

**问题列表**:

- ⚠️ **import_order** (第24行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第58行): 函数 'batch_processing_example' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第121行): 函数 'stream_processing_example' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第173行): 函数 'window_aggregation_example' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第235行): 函数 'table_join_example' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第316行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第316行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第58行): 函数 'batch_processing_example' 过长 (60行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第173行): 函数 'window_aggregation_example' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第235行): 函数 'table_join_example' 过长 (78行)
  - 建议: 考虑拆分函数

### ❌ release\v3.0.0\docs\examples\python\table-api\table_api_example.py

- **文件类型**: python
- **总行数**: 351
- **代码行**: 279
- **注释行**: 19
- **质量分数**: 68.0/100

**问题列表**:

- ⚠️ **import_order** (第24行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第58行): 函数 'batch_processing_example' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第121行): 函数 'stream_processing_example' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第173行): 函数 'window_aggregation_example' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第235行): 函数 'table_join_example' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第316行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第316行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第58行): 函数 'batch_processing_example' 过长 (60行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第173行): 函数 'window_aggregation_example' 过长 (59行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第235行): 函数 'table_join_example' 过长 (78行)
  - 建议: 考虑拆分函数

### ❌ .scripts\theorem-validator.py

- **文件类型**: python
- **总行数**: 424
- **代码行**: 344
- **注释行**: 15
- **质量分数**: 69.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_return_type** (第367行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第134行): 函数 'scan_all_documents' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第157行): 函数 'check_duplicates' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第180行): 函数 'check_continuity' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第213行): 函数 'check_format_consistency' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第235行): 函数 'compare_with_registry' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第307行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第327行): 函数 'print_summary' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第357行): 函数 'run_all_checks' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第28行): ClassDef 'Colors' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第72行): ClassDef 'TheoremValidator' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第73行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第367行): 函数 'main' 过长 (53行)
  - 建议: 考虑拆分函数

### ❌ KNOWLEDGE-GRAPH\scripts\export_formats.py

- **文件类型**: python
- **总行数**: 382
- **代码行**: 283
- **注释行**: 27
- **质量分数**: 69.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第10行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第319行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第18行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第319行): 函数 'main' 过长 (58行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第29行): 函数 'to_graphml' 过长 (65行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第96行): 函数 'to_cypher' 过长 (71行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第169行): 函数 'to_gexf' 过长 (77行)
  - 建议: 考虑拆分函数

### ❌ phase2-automation\doc-generator\generate_docs.py

- **文件类型**: python
- **总行数**: 88
- **代码行**: 70
- **注释行**: 1
- **质量分数**: 69.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第11行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第72行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第15行): 函数 '**init**' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第20行): 函数 'generate_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第45行): 函数 'generate_stats' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第14行): ClassDef 'DocumentationGenerator' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第72行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第15行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **bare_except** (第61行): 使用裸except:捕获所有异常
  - 建议: 指定具体的异常类型
- ⚠️ **empty_except** (第61行): 空的异常处理块
  - 建议: 处理异常或记录日志

### ❌ release\v3.0.0\neo4j\KNOWLEDGE-GRAPH\scripts\export_formats.py

- **文件类型**: python
- **总行数**: 382
- **代码行**: 283
- **注释行**: 27
- **质量分数**: 69.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第10行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第319行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第18行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第319行): 函数 'main' 过长 (58行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第29行): 函数 'to_graphml' 过长 (65行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第96行): 函数 'to_cypher' 过长 (71行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第169行): 函数 'to_gexf' 过长 (77行)
  - 建议: 考虑拆分函数

### ⚠️ .scripts\fix-cross-refs-batch.py

- **文件类型**: python
- **总行数**: 220
- **代码行**: 153
- **注释行**: 24
- **质量分数**: 70.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第92行): 函数 'find_best_match' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第92行): 函数 'find_best_match' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第106行): 函数 'fix_links_in_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第106行): 函数 'fix_links_in_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第159行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第119行): 函数 'replace_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第119行): 函数 'replace_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第159行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第119行): FunctionDef 'replace_link' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第106行): 函数 'fix_links_in_file' 过长 (51行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第159行): 函数 'main' 过长 (57行)
  - 建议: 考虑拆分函数

### ⚠️ .scripts\quality-gates\theorem-uniqueness-checker.py

- **文件类型**: python
- **总行数**: 303
- **代码行**: 234
- **注释行**: 11
- **质量分数**: 71.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第17行): 导入顺序问题: pathlib
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第112行): 函数 'generate_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第219行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第65行): 'find_duplicates' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第80行): 'check_sequential_gaps' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第112行): 'generate_report' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第219行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第112行): 函数 'generate_report' 过长 (104行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第219行): 函数 'main' 过长 (79行)
  - 建议: 考虑拆分函数

### ⚠️ release\v3.0.0\tools\scripts\theorem-validator.py

- **文件类型**: python
- **总行数**: 423
- **代码行**: 328
- **注释行**: 21
- **质量分数**: 73.0/100

**问题列表**:

- ⚠️ **import_order** (第17行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第200行): 函数 'generate_validation_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第282行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第27行): 'ValidationError' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第37行): 'ValidationReport' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第147行): 'check_duplicates' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第282行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第200行): 函数 'generate_validation_report' 过长 (79行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第282行): 函数 'main' 过长 (136行)
  - 建议: 考虑拆分函数

### ⚠️ scripts\theorem-validator.py

- **文件类型**: python
- **总行数**: 423
- **代码行**: 328
- **注释行**: 21
- **质量分数**: 73.0/100

**问题列表**:

- ⚠️ **import_order** (第17行): 导入顺序问题: re
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第200行): 函数 'generate_validation_report' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第282行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第27行): 'ValidationError' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第37行): 'ValidationReport' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第147行): 'check_duplicates' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第282行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第200行): 函数 'generate_validation_report' 过长 (79行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第282行): 函数 'main' 过长 (136行)
  - 建议: 考虑拆分函数

### ⚠️ .scripts\benchmarks\benchmark-data-synthesizer.py

- **文件类型**: python
- **总行数**: 509
- **代码行**: 458
- **注释行**: 13
- **质量分数**: 75.0/100

**问题列表**:

- ⚠️ **import_order** (第21行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第444行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第201行): 'add_realistic_variation' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第206行): 'generate_time_series_data' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第248行): 'generate_throughput_results' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第360行): 'generate_backpressure_results' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第386行): 函数 'generate_grafana_dashboard_data' 过长 (56行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第444行): 函数 'main' 过长 (61行)
  - 建议: 考虑拆分函数

### ⚠️ .scripts\fix-cross-refs-final.py

- **文件类型**: python
- **总行数**: 144
- **代码行**: 100
- **注释行**: 13
- **质量分数**: 77.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第37行): 函数 'fix_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第37行): 函数 'fix_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第88行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第49行): 函数 'replace_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第49行): 函数 'replace_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第37行): 'fix_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第88行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第49行): FunctionDef 'replace_link' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第88行): 函数 'main' 过长 (52行)
  - 建议: 考虑拆分函数

### ⚠️ patches\fix-formal-elements.py

- **文件类型**: python
- **总行数**: 194
- **代码行**: 143
- **注释行**: 22
- **质量分数**: 77.0/100

**问题列表**:

- ℹ️ **missing_type_hints** (第23行): 函数 'scan_formal_elements' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第23行): 函数 'scan_formal_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第41行): 函数 'fix_quick_start_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第85行): 函数 'fix_duplicate_in_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第85行): 函数 'fix_duplicate_in_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第138行): 函数 'process_directory' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第138行): 函数 'process_directory' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第152行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第152行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第85行): 函数 'fix_duplicate_in_file' 过长 (51行)
  - 建议: 考虑拆分函数

### ⚠️ USTM-F-Reconstruction\proof-assistant\coq\verify_proofs.py

- **文件类型**: python
- **总行数**: 230
- **代码行**: 173
- **注释行**: 13
- **质量分数**: 77.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_return_type** (第216行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第37行): 函数 'collect_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第102行): 函数 'verify' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第141行): 函数 'print_stats' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第17行): ClassDef 'FileStats' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第30行): ClassDef 'CoqVerifier' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第216行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第31行): FunctionDef '**init**' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第141行): 函数 'print_stats' 过长 (73行)
  - 建议: 考虑拆分函数

### ⚠️ .scripts\ai-assistant\demo.py

- **文件类型**: python
- **总行数**: 174
- **代码行**: 122
- **注释行**: 10
- **质量分数**: 78.0/100

**问题列表**:

- ℹ️ **missing_type_hints** (第14行): 函数 'import_from_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第14行): 函数 'import_from_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第24行): 函数 'demo_summarizer' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第55行): 函数 'demo_translator' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第88行): 函数 'demo_cross_ref' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第141行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第14行): 'import_from_file' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第24行): 'demo_summarizer' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第55行): 'demo_translator' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第88行): 'demo_cross_ref' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第141行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明

### ⚠️ examples\python\wordcount\wordcount.py

- **文件类型**: python
- **总行数**: 175
- **代码行**: 124
- **注释行**: 17
- **质量分数**: 80.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: typing
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第83行): 函数 'run_wordcount' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第138行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第44行): 函数 'flat_map' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第44行): 函数 'flat_map' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第138行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第83行): 函数 'run_wordcount' 过长 (52行)
  - 建议: 考虑拆分函数

### ⚠️ release\v3.0.0\docs\examples\python\wordcount\wordcount.py

- **文件类型**: python
- **总行数**: 175
- **代码行**: 124
- **注释行**: 17
- **质量分数**: 80.0/100

**问题列表**:

- ⚠️ **import_order** (第22行): 导入顺序问题: typing
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第83行): 函数 'run_wordcount' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第138行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第44行): 函数 'flat_map' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第44行): 函数 'flat_map' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第138行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第83行): 函数 'run_wordcount' 过长 (52行)
  - 建议: 考虑拆分函数

### ⚠️ .improvement-tracking\add-prospective-banners.py

- **文件类型**: python
- **总行数**: 388
- **代码行**: 294
- **注释行**: 24
- **质量分数**: 81.0/100

**问题列表**:

- ⚠️ **import_order** (第27行): 导入顺序问题: datetime
  - 建议: 标准库导入应该放在第三方库之前
- ℹ️ **missing_return_type** (第265行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第265行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第207行): 函数 'process_file' 过长 (55行)
  - 建议: 考虑拆分函数
- ⚠️ **high_complexity** (第265行): 函数 'main' 过长 (118行)
  - 建议: 考虑拆分函数

### ⚠️ .scripts\kg-v2\generate-search-index.py

- **文件类型**: python
- **总行数**: 201
- **代码行**: 166
- **注释行**: 9
- **质量分数**: 81.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_return_type** (第16行): 函数 'extract_searchable_content' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第114行): 函数 'generate_lunr_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第154行): 函数 'generate_suggestions' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第174行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第154行): 'generate_suggestions' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第174行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第16行): 函数 'extract_searchable_content' 过长 (96行)
  - 建议: 考虑拆分函数

### ⚠️ .scripts\kg-v2\push-to-algolia.py

- **文件类型**: python
- **总行数**: 128
- **代码行**: 97
- **注释行**: 10
- **质量分数**: 81.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_return_type** (第30行): 函数 'load_search_index' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第40行): 函数 'push_to_algolia' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第40行): 函数 'push_to_algolia' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第104行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第30行): 'load_search_index' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第104行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第40行): 函数 'push_to_algolia' 过长 (62行)
  - 建议: 考虑拆分函数

### ⚠️ .scripts\fix-cross-refs-complete.py

- **文件类型**: python
- **总行数**: 145
- **代码行**: 107
- **注释行**: 7
- **质量分数**: 82.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第50行): 函数 'fix_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第50行): 函数 'fix_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第95行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第59行): 函数 'replace_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第59行): 函数 'replace_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第50行): FunctionDef 'fix_file' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第95行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第59行): FunctionDef 'replace_link' 缺少文档字符串
  - 建议: 添加描述性的文档字符串

### ⚠️ .scripts\fix-cross-refs-last.py

- **文件类型**: python
- **总行数**: 145
- **代码行**: 108
- **注释行**: 7
- **质量分数**: 82.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第47行): 函数 'fix_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第47行): 函数 'fix_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第92行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第56行): 函数 'replace_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第56行): 函数 'replace_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第47行): FunctionDef 'fix_file' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第92行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第56行): FunctionDef 'replace_link' 缺少文档字符串
  - 建议: 添加描述性的文档字符串

### ⚠️ .scripts\fix-cross-refs-zero.py

- **文件类型**: python
- **总行数**: 125
- **代码行**: 90
- **注释行**: 6
- **质量分数**: 82.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第36行): 函数 'fix_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第36行): 函数 'fix_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第81行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第45行): 函数 'replace_link' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第45行): 函数 'replace_link' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第36行): FunctionDef 'fix_file' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第81行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ℹ️ **missing_docstring** (第45行): FunctionDef 'replace_link' 缺少文档字符串
  - 建议: 添加描述性的文档字符串

### ⚠️ .scripts\kg-v2\generate-learning-paths.py

- **文件类型**: python
- **总行数**: 264
- **代码行**: 246
- **注释行**: 3
- **质量分数**: 83.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_return_type** (第13行): 函数 'generate_learning_paths' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第193行): 函数 'generate_skill_tree' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第238行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第193行): 'generate_skill_tree' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **short_docstring** (第238行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第13行): 函数 'generate_learning_paths' 过长 (178行)
  - 建议: 考虑拆分函数

### ⚠️ patches\fix-links.py

- **文件类型**: python
- **总行数**: 156
- **代码行**: 123
- **注释行**: 13
- **质量分数**: 83.0/100

**问题列表**:

- ℹ️ **missing_type_hints** (第30行): 函数 'fix_links_in_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第30行): 函数 'fix_links_in_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第65行): 函数 'process_directory' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第65行): 函数 'process_directory' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第83行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第83行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第83行): 函数 'main' 过长 (69行)
  - 建议: 考虑拆分函数

### ⚠️ patches\fix-dependencies.py

- **文件类型**: python
- **总行数**: 156
- **代码行**: 116
- **注释行**: 15
- **质量分数**: 84.0/100

**问题列表**:

- ℹ️ **missing_type_hints** (第32行): 函数 'scan_missing_definitions' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第32行): 函数 'scan_missing_definitions' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第50行): 函数 'add_missing_definitions' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第50行): 函数 'add_missing_definitions' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第91行): 函数 'process_key_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第133行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第91行): 'process_key_files' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ℹ️ **missing_docstring** (第133行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串

### ⚠️ Flink-IoT-Authority-Alignment\Phase-12-Smart-Building\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 311
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 85.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 180, column 33:
              jobmanager.rpc.address: flink-jobmanager
                                    ^
  - 建议: 检查YAML缩进和语法
- ⚠️ **indentation** (第235行): 缩进应为2的倍数 (当前13个空格)
  - 建议: 使用2个空格作为缩进

### ⚠️ release\v3.0.0\tools\scripts\formal_element_advanced_check.py

- **文件类型**: python
- **总行数**: 349
- **代码行**: 275
- **注释行**: 17
- **质量分数**: 85.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第43行): 函数 'get_all_md_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第56行): 函数 'extract_formal_elements' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第56行): 函数 'extract_formal_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第99行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第99行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第99行): 函数 'main' 过长 (245行)
  - 建议: 考虑拆分函数

### ⚠️ scripts\formal_element_advanced_check.py

- **文件类型**: python
- **总行数**: 349
- **代码行**: 275
- **注释行**: 17
- **质量分数**: 85.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第43行): 函数 'get_all_md_files' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_type_hints** (第56行): 函数 'extract_formal_elements' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第56行): 函数 'extract_formal_elements' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_return_type** (第99行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **short_docstring** (第99行): 'main' 的文档字符串过短
  - 建议: 提供更详细的文档说明
- ⚠️ **high_complexity** (第99行): 函数 'main' 过长 (245行)
  - 建议: 考虑拆分函数

### ⚠️ fix_python_code.py

- **文件类型**: python
- **总行数**: 187
- **代码行**: 126
- **注释行**: 29
- **质量分数**: 87.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第31行): 函数 'fix_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第31行): 函数 'fix_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第31行): FunctionDef 'fix_file' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第31行): 函数 'fix_file' 过长 (132行)
  - 建议: 考虑拆分函数

### ⚠️ fix_python_remaining.py

- **文件类型**: python
- **总行数**: 198
- **代码行**: 142
- **注释行**: 21
- **质量分数**: 87.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_type_hints** (第27行): 函数 'fix_file' 缺少参数类型提示
  - 建议: 为函数参数添加类型注解
- ℹ️ **missing_return_type** (第27行): 函数 'fix_file' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第27行): FunctionDef 'fix_file' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第27行): 函数 'fix_file' 过长 (156行)
  - 建议: 考虑拆分函数

### ⚠️ .scripts\generate-link-report.py

- **文件类型**: python
- **总行数**: 363
- **代码行**: 317
- **注释行**: 17
- **质量分数**: 89.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ℹ️ **missing_return_type** (第17行): 函数 'main' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第17行): FunctionDef 'main' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第17行): 函数 'main' 过长 (341行)
  - 建议: 考虑拆分函数

### ✅ CONFIG-TEMPLATES\cloud-providers\aliyun-realtime-compute-config.yaml

- **文件类型**: yaml
- **总行数**: 374
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: while scanning a simple key
  in "<unicode string>", line 178, column 1:
    log4j.appender.sls=com.aliyun.op ...
    ^
could not find expected ':'
  in "<unicode string>", line 179, column 1:
    log4j.appender.sls.projectName=f ...
    ^
  - 建议: 检查YAML缩进和语法

### ✅ CONFIG-TEMPLATES\cloud-providers\aws-emr-config.yaml

- **文件类型**: yaml
- **总行数**: 228
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: expected '<document start>', but found '<block mapping start>'
  in "<unicode string>", line 67, column 1:
    fs.s3a.impl: org.apache.hadoop.f ...
    ^
  - 建议: 检查YAML缩进和语法

### ✅ CONFIG-TEMPLATES\cloud-providers\azure-hdinsight-config.yaml

- **文件类型**: yaml
- **总行数**: 263
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: while scanning a simple key
  in "<unicode string>", line 141, column 1:
    log4j.appender.azure=com.microso ...
    ^
could not find expected ':'
  in "<unicode string>", line 142, column 1:
    log4j.appender.azure.instrumenta ...
    ^
  - 建议: 检查YAML缩进和语法

### ✅ CONFIG-TEMPLATES\cloud-providers\gcp-dataproc-config.yaml

- **文件类型**: yaml
- **总行数**: 290
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: expected '<document start>', but found '<scalar>'
  in "<unicode string>", line 30, column 1:
    FLINK_VERSION=1.18.0
    ^
  - 建议: 检查YAML缩进和语法

### ✅ CONFIG-TEMPLATES\development\docker-compose-dev.yml

- **文件类型**: yaml
- **总行数**: 299
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 49, column 33:
              jobmanager.rpc.address: jobmanager
                                    ^
  - 建议: 检查YAML缩进和语法

### ✅ CONFIG-TEMPLATES\production\k8s-flink-production.yaml

- **文件类型**: yaml
- **总行数**: 755
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: expected a single document in the stream
  in "<unicode string>", line 11, column 1:
    apiVersion: v1
    ^
but found another document
  in "<unicode string>", line 21, column 1
    ---

    ^
  - 建议: 检查YAML缩进和语法

### ✅ CONFIG-TEMPLATES\testing\k8s-flink-test.yaml

- **文件类型**: yaml
- **总行数**: 570
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: expected a single document in the stream
  in "<unicode string>", line 12, column 1:
    apiVersion: v1
    ^
but found another document
  in "<unicode string>", line 21, column 1
    ---

    ^
  - 建议: 检查YAML缩进和语法

### ✅ examples\docker\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 200
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 31, column 33:
              jobmanager.rpc.address: jobmanager
                                    ^
  - 建议: 检查YAML缩进和语法

### ✅ Flink-IoT-Authority-Alignment\Phase-1-Architecture\project-skeleton\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 448
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 113, column 33:
              jobmanager.rpc.address: jobmanager
                                    ^
  - 建议: 检查YAML缩进和语法

### ✅ Flink-IoT-Authority-Alignment\Phase-10-Telecom\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 443
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 152, column 41:
     ...   jobmanager.memory.process.size: 4096m
                                         ^
  - 建议: 检查YAML缩进和语法

### ✅ Flink-IoT-Authority-Alignment\Phase-11-Mining-Oil-Gas\project-skeleton\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 311
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 169, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^
  - 建议: 检查YAML缩进和语法

### ✅ Flink-IoT-Authority-Alignment\Phase-13-Water-Management\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 319
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 134, column 39:
     ...   jobmanager.memory.process.size: 2048m
                                         ^
  - 建议: 检查YAML缩进和语法

### ✅ Flink-IoT-Authority-Alignment\Phase-5-Agriculture\project-skeleton\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 283
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 188, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^
  - 建议: 检查YAML缩进和语法

### ✅ Flink-IoT-Authority-Alignment\Phase-7-Smart-Retail\project-skeleton\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 262
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 89, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^
  - 建议: 检查YAML缩进和语法

### ✅ Flink-IoT-Authority-Alignment\Phase-8-Wearables\project-skeleton\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 210
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 68, column 33:
              jobmanager.rpc.address: jobmanager
                                    ^
  - 建议: 检查YAML缩进和语法

### ✅ Flink-IoT-Authority-Alignment\Phase-9-Smart-Home\project-skeleton\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 417
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 210, column 33:
              jobmanager.rpc.address: jobmanager
                                    ^
  - 建议: 检查YAML缩进和语法

### ✅ release\v3.0.0\docs\examples\docker\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 200
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 31, column 33:
              jobmanager.rpc.address: jobmanager
                                    ^
  - 建议: 检查YAML缩进和语法

### ✅ release\v3.0.0\docs\tutorials\interactive\flink-playground\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 219
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 19, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^
  - 建议: 检查YAML缩进和语法

### ✅ tutorials\interactive\flink-playground\docker-compose.yml

- **文件类型**: yaml
- **总行数**: 219
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 90.0/100

**问题列表**:

- ❌ **yaml_syntax** (第1行): YAML语法错误: mapping values are not allowed here
  in "<unicode string>", line 19, column 41:
     ...   jobmanager.memory.process.size: 2048m
                                         ^
  - 建议: 检查YAML缩进和语法

### ✅ .scripts\analyze_links.py

- **文件类型**: python
- **总行数**: 97
- **代码行**: 74
- **注释行**: 6
- **质量分数**: 91.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第9行): 函数 'analyze_links' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第9行): FunctionDef 'analyze_links' 缺少文档字符串
  - 建议: 添加描述性的文档字符串
- ⚠️ **high_complexity** (第9行): 函数 'analyze_links' 过长 (84行)
  - 建议: 考虑拆分函数

### ✅ check_syntax_direct.py

- **文件类型**: python
- **总行数**: 34
- **代码行**: 25
- **注释行**: 2
- **质量分数**: 91.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明
- ⚠️ **import_order** (第4行): 导入顺序问题: os
  - 建议: 标准库导入应该放在第三方库之前

### ✅ Flink-IoT-Authority-Alignment\Phase-1-Architecture\project-skeleton\flink-sql\02-ingestion.sql

- **文件类型**: sql
- **总行数**: 308
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 95.0/100

**问题列表**:

- ⚠️ **select_star** (第1行): 使用SELECT *
  - 建议: 显式指定需要的列

### ✅ Flink-IoT-Authority-Alignment\Phase-1-Architecture\project-skeleton\flink-sql\04-queries.sql

- **文件类型**: sql
- **总行数**: 439
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 95.0/100

**问题列表**:

- ⚠️ **select_star** (第1行): 使用SELECT *
  - 建议: 显式指定需要的列

### ✅ Flink-IoT-Authority-Alignment\Phase-10-Telecom\flink-sql\02_create_processing_jobs.sql

- **文件类型**: sql
- **总行数**: 504
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 95.0/100

**问题列表**:

- ⚠️ **select_star** (第1行): 使用SELECT *
  - 建议: 显式指定需要的列

### ✅ Flink-IoT-Authority-Alignment\Phase-5-Agriculture\project-skeleton\flink-sql\02-irrigation-rules.sql

- **文件类型**: sql
- **总行数**: 280
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 95.0/100

**问题列表**:

- ⚠️ **select_star** (第1行): 使用SELECT *
  - 建议: 显式指定需要的列

### ✅ Flink-IoT-Authority-Alignment\Phase-8-Wearables\project-skeleton\flink-sql\01_cgm_pipeline.sql

- **文件类型**: sql
- **总行数**: 376
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 95.0/100

**问题列表**:

- ⚠️ **select_star** (第1行): 使用SELECT *
  - 建议: 显式指定需要的列

### ✅ Flink-IoT-Authority-Alignment\Phase-8-Wearables\project-skeleton\flink-sql\02_hr_pipeline.sql

- **文件类型**: sql
- **总行数**: 293
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 95.0/100

**问题列表**:

- ⚠️ **select_star** (第1行): 使用SELECT *
  - 建议: 显式指定需要的列

### ✅ Flink-IoT-Authority-Alignment\Phase-8-Wearables\project-skeleton\flink-sql\03_alert_pipeline.sql

- **文件类型**: sql
- **总行数**: 253
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 95.0/100

**问题列表**:

- ⚠️ **select_star** (第1行): 使用SELECT *
  - 建议: 显式指定需要的列

### ✅ Flink-IoT-Authority-Alignment\Phase-8-Wearables\project-skeleton\flink-sql\04_activity_pipeline.sql

- **文件类型**: sql
- **总行数**: 218
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 95.0/100

**问题列表**:

- ⚠️ **select_star** (第1行): 使用SELECT *
  - 建议: 显式指定需要的列

### ✅ Knowledge\Flink-Scala-Rust-Comprehensive\performance-tests\nexmark\materialize\q0-passthrough.sql

- **文件类型**: sql
- **总行数**: 16
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 95.0/100

**问题列表**:

- ⚠️ **select_star** (第1行): 使用SELECT *
  - 建议: 显式指定需要的列

### ✅ Knowledge\Flink-Scala-Rust-Comprehensive\performance-tests\nexmark\risingwave\q0-passthrough.sql

- **文件类型**: sql
- **总行数**: 27
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 95.0/100

**问题列表**:

- ⚠️ **select_star** (第1行): 使用SELECT *
  - 建议: 显式指定需要的列

### ✅ release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\performance-tests\nexmark\materialize\q0-passthrough.sql

- **文件类型**: sql
- **总行数**: 16
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 95.0/100

**问题列表**:

- ⚠️ **select_star** (第1行): 使用SELECT *
  - 建议: 显式指定需要的列

### ✅ release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\performance-tests\nexmark\risingwave\q0-passthrough.sql

- **文件类型**: sql
- **总行数**: 27
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 95.0/100

**问题列表**:

- ⚠️ **select_star** (第1行): 使用SELECT *
  - 建议: 显式指定需要的列

### ✅ .scripts\automation\tests\_*init*_.py

- **文件类型**: python
- **总行数**: 2
- **代码行**: 0
- **注释行**: 1
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ analyze_block.py

- **文件类型**: python
- **总行数**: 15
- **代码行**: 14
- **注释行**: 0
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ analyze_broken_links.py

- **文件类型**: python
- **总行数**: 56
- **代码行**: 41
- **注释行**: 5
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ analyze_perf.py

- **文件类型**: python
- **总行数**: 14
- **代码行**: 13
- **注释行**: 0
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ analyze_perf2.py

- **文件类型**: python
- **总行数**: 12
- **代码行**: 11
- **注释行**: 0
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ analyze_remaining.py

- **文件类型**: python
- **总行数**: 19
- **代码行**: 13
- **注释行**: 1
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ check_block.py

- **文件类型**: python
- **总行数**: 11
- **代码行**: 10
- **注释行**: 0
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ fix_final.py

- **文件类型**: python
- **总行数**: 13
- **代码行**: 8
- **注释行**: 1
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ release\v3.0.0\docs\reports\apply-auto-fixes.py

- **文件类型**: python
- **总行数**: 79
- **代码行**: 54
- **注释行**: 9
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第25行): 函数 'apply_fixes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第25行): FunctionDef 'apply_fixes' 缺少文档字符串
  - 建议: 添加描述性的文档字符串

### ✅ release\v3.0.0\tools\analyze_broken_links.py

- **文件类型**: python
- **总行数**: 56
- **代码行**: 41
- **注释行**: 5
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ reports\apply-auto-fixes.py

- **文件类型**: python
- **总行数**: 79
- **代码行**: 54
- **注释行**: 9
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_return_type** (第25行): 函数 'apply_fixes' 缺少返回值类型提示
  - 建议: 为函数添加 -> 返回类型
- ℹ️ **missing_docstring** (第25行): FunctionDef 'apply_fixes' 缺少文档字符串
  - 建议: 添加描述性的文档字符串

### ✅ show_errors.py

- **文件类型**: python
- **总行数**: 9
- **代码行**: 8
- **注释行**: 0
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ show_errors2.py

- **文件类型**: python
- **总行数**: 10
- **代码行**: 9
- **注释行**: 0
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ show_final_errors.py

- **文件类型**: python
- **总行数**: 14
- **代码行**: 10
- **注释行**: 1
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ show_remaining.py

- **文件类型**: python
- **总行数**: 10
- **代码行**: 8
- **注释行**: 1
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ show_remaining2.py

- **文件类型**: python
- **总行数**: 10
- **代码行**: 9
- **注释行**: 0
- **质量分数**: 96.0/100

**问题列表**:

- ℹ️ **missing_shebang** (第1行): 缺少shebang (#!/usr/bin/env python3)
  - 建议: 在文件第一行添加shebang
- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ formal-methods\.scripts\verify-fix.py

- **文件类型**: python
- **总行数**: 56
- **代码行**: 44
- **注释行**: 3
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ phase2-automation\backup-automation\backup.yml

- **文件类型**: yaml
- **总行数**: 10
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_header_comment** (第1行): 缺少文件头注释
  - 建议: 在文件开头添加描述性注释

### ✅ phase2-automation\code-quality\linter.yml

- **文件类型**: yaml
- **总行数**: 10
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_header_comment** (第1行): 缺少文件头注释
  - 建议: 在文件开头添加描述性注释

### ✅ phase2-automation\notifier\notify.yml

- **文件类型**: yaml
- **总行数**: 8
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_header_comment** (第1行): 缺少文件头注释
  - 建议: 在文件开头添加描述性注释

### ✅ release\v3.0.0\docs\formal-methods\.scripts\verify-fix.py

- **文件类型**: python
- **总行数**: 56
- **代码行**: 44
- **注释行**: 3
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ release\v3.0.0\tools\scripts\add_dependencies.py

- **文件类型**: python
- **总行数**: 178
- **代码行**: 146
- **注释行**: 15
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ release\v3.0.0\tools\scripts\debug_registry.py

- **文件类型**: python
- **总行数**: 18
- **代码行**: 13
- **注释行**: 2
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ release\v3.0.0\tools\scripts\debug_registry2.py

- **文件类型**: python
- **总行数**: 19
- **代码行**: 13
- **注释行**: 2
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ release\v3.0.0\tools\scripts\debug_registry3.py

- **文件类型**: python
- **总行数**: 16
- **代码行**: 11
- **注释行**: 1
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ release\v3.0.0\tools\scripts\update_registry.py

- **文件类型**: python
- **总行数**: 120
- **代码行**: 90
- **注释行**: 14
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ release\v3.0.0\tools\scripts\update_registry_v2.py

- **文件类型**: python
- **总行数**: 142
- **代码行**: 103
- **注释行**: 21
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ release\v3.0.0\tools\scripts\update_registry_v3.py

- **文件类型**: python
- **总行数**: 131
- **代码行**: 93
- **注释行**: 20
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ release\v3.0.0\tools\scripts\update_registry_v4.py

- **文件类型**: python
- **总行数**: 121
- **代码行**: 86
- **注释行**: 19
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ scripts\add_dependencies.py

- **文件类型**: python
- **总行数**: 178
- **代码行**: 146
- **注释行**: 15
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ scripts\debug_registry.py

- **文件类型**: python
- **总行数**: 18
- **代码行**: 13
- **注释行**: 2
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ scripts\debug_registry2.py

- **文件类型**: python
- **总行数**: 19
- **代码行**: 13
- **注释行**: 2
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ scripts\debug_registry3.py

- **文件类型**: python
- **总行数**: 16
- **代码行**: 11
- **注释行**: 1
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ scripts\update_registry.py

- **文件类型**: python
- **总行数**: 120
- **代码行**: 90
- **注释行**: 14
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ scripts\update_registry_v2.py

- **文件类型**: python
- **总行数**: 142
- **代码行**: 103
- **注释行**: 21
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ scripts\update_registry_v3.py

- **文件类型**: python
- **总行数**: 131
- **代码行**: 93
- **注释行**: 20
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ scripts\update_registry_v4.py

- **文件类型**: python
- **总行数**: 121
- **代码行**: 86
- **注释行**: 19
- **质量分数**: 98.0/100

**问题列表**:

- ℹ️ **missing_encoding** (第1行): 缺少编码声明 (# -*- coding: utf-8 -*-)
  - 建议: 在shebang后添加编码声明

### ✅ .scripts\ai-assistant\config.yaml

- **文件类型**: yaml
- **总行数**: 331
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ _config.yml

- **文件类型**: yaml
- **总行数**: 157
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ CONFIG-TEMPLATES\development\flink-conf-dev.yaml

- **文件类型**: yaml
- **总行数**: 174
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ CONFIG-TEMPLATES\production\flink-conf-production.yaml

- **文件类型**: yaml
- **总行数**: 421
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ CONFIG-TEMPLATES\scenarios\high-throughput-config.yaml

- **文件类型**: yaml
- **总行数**: 196
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ CONFIG-TEMPLATES\scenarios\large-state-config.yaml

- **文件类型**: yaml
- **总行数**: 208
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ CONFIG-TEMPLATES\scenarios\low-latency-config.yaml

- **文件类型**: yaml
- **总行数**: 165
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ CONFIG-TEMPLATES\scenarios\multi-tenant-config.yaml

- **文件类型**: yaml
- **总行数**: 199
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ CONFIG-TEMPLATES\testing\flink-conf-test.yaml

- **文件类型**: yaml
- **总行数**: 316
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ create_telecom_doc.py

- **文件类型**: python
- **总行数**: 2348
- **代码行**: 1872
- **注释行**: 123
- **质量分数**: 100.0/100

### ✅ docker-compose.yml

- **文件类型**: yaml
- **总行数**: 101
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ docs\i18n\config\i18n-config.yaml

- **文件类型**: yaml
- **总行数**: 132
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Flink-IoT-Authority-Alignment\Phase-1-Architecture\project-skeleton\flink-sql\01-create-tables.sql

- **文件类型**: sql
- **总行数**: 231
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Flink-IoT-Authority-Alignment\Phase-1-Architecture\project-skeleton\flink-sql\03-watermark.sql

- **文件类型**: sql
- **总行数**: 357
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Flink-IoT-Authority-Alignment\Phase-1-Architecture\project-skeleton\prometheus\grafana-dashboards.yml

- **文件类型**: yaml
- **总行数**: 21
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Flink-IoT-Authority-Alignment\Phase-1-Architecture\project-skeleton\prometheus\grafana-datasources.yml

- **文件类型**: yaml
- **总行数**: 96
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Flink-IoT-Authority-Alignment\Phase-1-Architecture\project-skeleton\prometheus\prometheus.yml

- **文件类型**: yaml
- **总行数**: 128
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Flink-IoT-Authority-Alignment\Phase-10-Telecom\flink-sql\01_create_sources.sql

- **文件类型**: sql
- **总行数**: 266
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Flink-IoT-Authority-Alignment\Phase-10-Telecom\flink-sql\03_create_sinks.sql

- **文件类型**: sql
- **总行数**: 287
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Flink-IoT-Authority-Alignment\Phase-10-Telecom\flink-sql\04_deploy_pipelines.sql

- **文件类型**: sql
- **总行数**: 234
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Flink-IoT-Authority-Alignment\Phase-12-Smart-Building\flink-sql\01-source-tables.sql

- **文件类型**: sql
- **总行数**: 139
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Flink-IoT-Authority-Alignment\Phase-12-Smart-Building\flink-sql\02-cleaning-views.sql

- **文件类型**: sql
- **总行数**: 121
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Flink-IoT-Authority-Alignment\Phase-5-Agriculture\project-skeleton\flink-sql\01-create-tables.sql

- **文件类型**: sql
- **总行数**: 251
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ java-code-validator.py

- **文件类型**: python
- **总行数**: 715
- **代码行**: 539
- **注释行**: 59
- **质量分数**: 100.0/100

**问题列表**:

- ❌ **syntax_error** (第266行): 语法错误: invalid syntax
  - 建议: 修复语法错误

### ✅ Knowledge\Flink-Scala-Rust-Comprehensive\performance-tests\nexmark\materialize\q5-hot-items.sql

- **文件类型**: sql
- **总行数**: 29
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Knowledge\Flink-Scala-Rust-Comprehensive\performance-tests\nexmark\risingwave\q1-currency.sql

- **文件类型**: sql
- **总行数**: 25
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ Knowledge\Flink-Scala-Rust-Comprehensive\performance-tests\nexmark\risingwave\q5-hot-items.sql

- **文件类型**: sql
- **总行数**: 38
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ phase2-automation\ci-cd\documentation-check.yml

- **文件类型**: yaml
- **总行数**: 187
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ phase2-automation\ci-cd\github-workflows.yml

- **文件类型**: yaml
- **总行数**: 214
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ phase2-automation\ci-cd\performance-benchmark.yml

- **文件类型**: yaml
- **总行数**: 171
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ phase2-automation\dependency-checker\check_deps.py

- **文件类型**: python
- **总行数**: 12
- **代码行**: 9
- **注释行**: 0
- **质量分数**: 100.0/100

**问题列表**:

- ❌ **syntax_error** (第1行): 语法错误: invalid non-printable character U+FEFF
  - 建议: 修复语法错误

### ✅ phase2-automation\performance-profiler\profile.py

- **文件类型**: python
- **总行数**: 11
- **代码行**: 8
- **注释行**: 0
- **质量分数**: 100.0/100

**问题列表**:

- ❌ **syntax_error** (第1行): 语法错误: invalid non-printable character U+FEFF
  - 建议: 修复语法错误

### ✅ phase2-automation\release-automation\release.yml

- **文件类型**: yaml
- **总行数**: 25
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ phase2-automation\security-scanner\scan.py

- **文件类型**: python
- **总行数**: 12
- **代码行**: 9
- **注释行**: 0
- **质量分数**: 100.0/100

**问题列表**:

- ❌ **syntax_error** (第1行): 语法错误: invalid non-printable character U+FEFF
  - 建议: 修复语法错误

### ✅ release\v3.0.0\docs\docs\i18n\config\i18n-config.yaml

- **文件类型**: yaml
- **总行数**: 132
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\performance-tests\nexmark\materialize\q5-hot-items.sql

- **文件类型**: sql
- **总行数**: 29
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\performance-tests\nexmark\risingwave\q1-currency.sql

- **文件类型**: sql
- **总行数**: 25
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ release\v3.0.0\docs\Knowledge\Flink-Scala-Rust-Comprehensive\performance-tests\nexmark\risingwave\q5-hot-items.sql

- **文件类型**: sql
- **总行数**: 38
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ release\v3.0.0\docs\tutorials\interactive\flink-playground\conf\flink-conf.yaml

- **文件类型**: yaml
- **总行数**: 95
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ release\v3.0.0\docs\tutorials\interactive\flink-playground\sql\init.sql

- **文件类型**: sql
- **总行数**: 69
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ release\v3.0.0\tools\create_telecom_doc.py

- **文件类型**: python
- **总行数**: 2348
- **代码行**: 1872
- **注释行**: 123
- **质量分数**: 100.0/100

### ✅ release\v3.0.0\tools\scripts\check_results.py

- **文件类型**: python
- **总行数**: 61
- **代码行**: 46
- **注释行**: 5
- **质量分数**: 100.0/100

### ✅ release\v3.0.0\tools\scripts\config\fictional-patterns.yaml

- **文件类型**: yaml
- **总行数**: 260
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ scripts\check_results.py

- **文件类型**: python
- **总行数**: 61
- **代码行**: 46
- **注释行**: 5
- **质量分数**: 100.0/100

### ✅ scripts\config\fictional-patterns.yaml

- **文件类型**: yaml
- **总行数**: 260
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ tutorials\interactive\flink-playground\conf\flink-conf.yaml

- **文件类型**: yaml
- **总行数**: 95
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

### ✅ tutorials\interactive\flink-playground\sql\init.sql

- **文件类型**: sql
- **总行数**: 69
- **代码行**: 0
- **注释行**: 0
- **质量分数**: 100.0/100

## 改进建议

### 高优先级

1. 修复 24 个错误级别问题
2. 处理 1335 个警告级别问题

### 代码风格

1. 确保所有Python文件包含shebang和编码声明
2. 为所有公共函数和类添加文档字符串
3. 使用类型提示提高代码可读性
4. 遵循PEP 8命名规范

### 配置文件

1. YAML文件使用2个空格缩进
2. 添加描述性注释说明配置用途
3. SQL文件显式指定查询列
