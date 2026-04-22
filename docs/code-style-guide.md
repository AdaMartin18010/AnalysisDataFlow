# AnalysisDataFlow 代码风格指南

> 版本: 1.0 | 最后更新: 2026-04-12

本指南定义了 AnalysisDataFlow 项目中所有代码（Python、YAML、SQL、Java）的编写规范，确保代码一致性、可读性和可维护性。

---

## 目录

- [AnalysisDataFlow 代码风格指南](#analysisdataflow-代码风格指南)
  - [目录](#目录)
  - [通用原则](#通用原则)
    - [1.1 代码可读性优先](#11-代码可读性优先)
    - [1.2 注释与文档](#12-注释与文档)
    - [1.3 错误处理](#13-错误处理)
  - [Python 代码规范](#python-代码规范)
    - [2.1 文件结构](#21-文件结构)
    - [2.2 命名规范](#22-命名规范)
    - [2.3 类型提示](#23-类型提示)
    - [2.4 导入排序](#24-导入排序)
    - [2.5 异常处理](#25-异常处理)
    - [2.6 代码格式化](#26-代码格式化)
  - [YAML 配置规范](#yaml-配置规范)
    - [3.1 基本格式](#31-基本格式)
    - [3.2 命名规范](#32-命名规范)
    - [3.3 Docker Compose 示例](#33-docker-compose-示例)
  - [SQL 查询规范](#sql-查询规范)
    - [4.1 格式化规则](#41-格式化规则)
    - [4.2 命名规范](#42-命名规范)
    - [4.3 查询优化原则](#43-查询优化原则)
  - [Java 代码规范](#java-代码规范)
    - [5.1 文件结构](#51-文件结构)
    - [5.2 命名规范](#52-命名规范)
  - [文档字符串规范](#文档字符串规范)
    - [6.1 Python 文档字符串](#61-python-文档字符串)
    - [6.2 类文档字符串](#62-类文档字符串)
  - [代码审查清单](#代码审查清单)
    - [7.1 提交前自检](#71-提交前自检)
    - [7.2 审查关注点](#72-审查关注点)
  - [工具配置](#工具配置)
    - [8.1 推荐工具](#81-推荐工具)
    - [8.2 pre-commit 配置](#82-pre-commit-配置)
  - [总结](#总结)

---

## 通用原则

### 1.1 代码可读性优先

- **清晰胜于简洁**: 使用描述性变量名，即使较长
- **避免过度优化**: 优先保证代码可读性
- **一致的格式**: 使用统一的代码风格

### 1.2 注释与文档

- 所有公共 API 必须包含文档字符串
- 复杂逻辑需要内联注释说明
- 保持注释与代码同步更新

### 1.3 错误处理

- 永远不要忽略异常
- 使用具体的异常类型，避免裸 `except:`
- 提供有意义的错误信息

---

## Python 代码规范

### 2.1 文件结构

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模块标题
========

简短描述模块功能。

详细说明模块的用途、主要功能和用法示例。

用法:
    python module.py [options]

示例:
    >>> from module import MyClass
    >>> obj = MyClass()
    >>> obj.process()
"""

# 标准库导入
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 第三方库导入
import requests
import yaml

# 本地模块导入
from .utils import helper_function

# 常量定义(UPPER_SNAKE_CASE)
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30

# 类定义(PascalCase)
class MyClass:
    """类文档字符串"""
    pass

# 函数定义(snake_case)
def process_data(input_data: Dict) -> List:
    """函数文档字符串"""
    pass

# 主函数
if __name__ == "__main__":
    main()
```

### 2.2 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 模块 | `snake_case` | `data_processor.py` |
| 包 | `snake_case` | `my_package` |
| 类 | `PascalCase` | `DataProcessor` |
| 函数 | `snake_case` | `process_data()` |
| 变量 | `snake_case` | `data_list` |
| 常量 | `UPPER_SNAKE_CASE` | `MAX_COUNT` |
| 私有 | `_leading_underscore` | `_internal_var` |

### 2.3 类型提示

所有函数必须添加类型提示：

```python
# 伪代码示意，非完整可编译代码
def calculate_metrics(
    data: List[Dict[str, Any]],
    threshold: float = 0.5,
    verbose: bool = False
) -> Tuple[float, float, float]:
    """
    计算数据指标

    Args:
        data: 输入数据列表
        threshold: 阈值,默认为0.5
        verbose: 是否打印详细信息

    Returns:
        Tuple包含 (准确率, 召回率, F1分数)

    Raises:
        ValueError: 当数据为空时
    """
    if not data:
        raise ValueError("数据不能为空")
    # ...
```

### 2.4 导入排序

```python
# 1. 标准库
import os
import sys
from pathlib import Path
from typing import Dict, List

# 2. 第三方库(按字母顺序)
import numpy as np
import pandas as pd
import requests

# 3. 本地模块
from .config import settings
from .utils import helper
```

### 2.5 异常处理

```python
def safe_operation():
    """安全的操作示例"""
    try:
        result = risky_call()
    except FileNotFoundError as e:
        # 处理特定异常
        logger.error(f"文件未找到: {e}")
        return None
    except PermissionError:
        # 处理权限错误
        logger.error("权限不足")
        raise  # 重新抛出
    except Exception as e:
        # 捕获其他异常但记录日志
        logger.exception(f"未预期的错误: {e}")
        raise
    else:
        # 没有异常时执行
        logger.info("操作成功")
    finally:
        # 清理资源
        cleanup()
```

### 2.6 代码格式化

使用 `black` 和 `isort` 自动格式化：

```bash
# 格式化代码
black src/ tests/

# 排序导入
isort src/ tests/

# 类型检查
mypy src/
```

---

## YAML 配置规范

### 3.1 基本格式

```yaml
# 文件头注释
document_title.yaml
# ================
# 简要描述配置文件用途

# 使用2个空格缩进
version: "3.8"

# 键值对
key: value

# 列表
items:
  - item1
  - item2
  - item3

# 嵌套对象
config:
  database:
    host: localhost
    port: 5432
    name: mydb
```

### 3.2 命名规范

- 键名使用 `snake_case`
- 布尔值使用 `true`/`false`（非 `yes`/`no`）
- 字符串值加引号（可选但建议）

### 3.3 Docker Compose 示例

```yaml
# docker-compose.yml
# 开发环境服务配置

version: "3.8"

services:
  # 应用服务
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: my-app
    ports:
      - "8080:8080"
    environment:
      - DEBUG=true
      - LOG_LEVEL=info
    volumes:
      - ./data:/app/data:ro
    depends_on:
      - database
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # 数据库服务
  database:
    image: postgres:14
    container_name: my-db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  db_data:
```

---

## SQL 查询规范

### 4.1 格式化规则

```sql
-- 查询名称: 获取用户订单统计
-- 描述: 计算每个用户的订单数量和总金额
-- 参数: start_date, end_date

SELECT
    u.user_id,
    u.user_name,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS total_amount,
    AVG(o.total_amount) AS avg_amount,
    MAX(o.created_at) AS last_order_date
FROM
    users u
LEFT JOIN
    orders o ON u.user_id = o.user_id
WHERE
    o.created_at >= :start_date
    AND o.created_at < :end_date
    AND o.status IN ('completed', 'shipped')
GROUP BY
    u.user_id, u.user_name
HAVING
    COUNT(o.order_id) > 0
ORDER BY
    total_amount DESC
LIMIT 100;
```

### 4.2 命名规范

| 对象 | 规范 | 示例 |
|------|------|------|
| 表名 | `snake_case` | `user_profiles` |
| 列名 | `snake_case` | `created_at` |
| 索引 | `idx_<table>_<column>` | `idx_users_email` |
| 约束 | `pk_<table>`, `fk_<table>_<ref>` | `pk_users` |

### 4.3 查询优化原则

1. **避免 SELECT ***: 明确指定需要的列
2. **使用索引**: 在 WHERE、JOIN、ORDER BY 列上建立索引
3. **限制结果集**: 使用 LIMIT 避免大数据量查询
4. **避免子查询**: 优先使用 JOIN

```sql
-- ✅ 推荐
SELECT user_id, user_name
FROM users
WHERE created_at > '2024-01-01'
LIMIT 100;

-- ❌ 避免
SELECT * FROM users;
```

---

## Java 代码规范

### 5.1 文件结构

```java
package com.analysisdataflow.utils;

import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 类描述
 *
 * 详细说明类的用途和功能
 *
 * @author Author Name
 * @version 1.0
 * @since 2024-01-01
 */
public class DataProcessor {

    private static final Logger LOG = LoggerFactory.getLogger(DataProcessor.class);

    // 常量
    private static final int MAX_BATCH_SIZE = 1000;

    // 实例变量
    private final String configPath;

    /**
     * 构造函数
     *
     * @param configPath 配置文件路径
     */
    public DataProcessor(String configPath) {
        this.configPath = configPath;
    }

    /**
     * 处理方法
     *
     * @param data 输入数据
     * @return 处理结果
     * @throws IllegalArgumentException 当数据无效时
     */
    public Result process(Data data) throws IllegalArgumentException {
        // 实现
    }
}
```

### 5.2 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类 | `PascalCase` | `DataProcessor` |
| 接口 | `PascalCase`（形容词） | `Serializable` |
| 方法 | `camelCase`（动词） | `processData()` |
| 变量 | `camelCase` | `dataList` |
| 常量 | `UPPER_SNAKE_CASE` | `MAX_COUNT` |
| 包 | `com.company.module` | `com.analysis.utils` |

---

## 文档字符串规范

### 6.1 Python 文档字符串

使用 Google 风格或 NumPy 风格的文档字符串：

```python
def process_data(data, threshold=0.5):
    """
    处理数据并返回过滤后的结果

    这是一个更详细的描述,说明函数的具体行为、
    算法复杂度、副作用等。

    Args:
        data (List[Dict]): 输入数据列表,每个字典包含:
            - id: 唯一标识符
            - value: 数值
            - timestamp: 时间戳
        threshold (float, optional): 过滤阈值,默认为0.5
            小于此值的记录将被过滤掉

    Returns:
        List[Dict]: 过滤后的数据列表
        返回的列表按 timestamp 降序排列

    Raises:
        ValueError: 当数据格式不正确或 threshold 为负数
        TypeError: 当 data 不是列表类型

    Examples:
        >>> data = [{"id": 1, "value": 0.8}]
        >>> result = process_data(data, threshold=0.5)
        >>> len(result)
        1
    """
    pass
```

### 6.2 类文档字符串

```python
class DataValidator:
    """
    数据验证器

    提供数据格式验证、类型检查和值范围验证功能。

    Attributes:
        schema (Dict): 验证模式定义
        strict_mode (bool): 是否启用严格模式

    Example:
        >>> validator = DataValidator(schema={"name": str})
        >>> validator.validate({"name": "test"})
        True
    """

    def __init__(self, schema, strict_mode=False):
        """初始化验证器"""
        self.schema = schema
        self.strict_mode = strict_mode
```

---

## 代码审查清单

### 7.1 提交前自检

- [ ] 代码通过所有单元测试
- [ ] 新增代码有对应的测试用例
- [ ] 文档字符串完整
- [ ] 类型提示正确
- [ ] 无硬编码敏感信息
- [ ] 异常处理完善
- [ ] 代码格式化通过 (black/isort)
- [ ] 静态检查无错误 (flake8/mypy)

### 7.2 审查关注点

**可读性**

- 变量名是否清晰描述用途？
- 函数是否单一职责？
- 是否有过多嵌套（建议不超过3层）？

**健壮性**

- 是否处理了边界情况？
- 输入参数是否经过验证？
- 是否有适当的错误处理？

**性能**

- 是否存在明显的性能问题？
- 是否有不必要的循环或重复计算？
- 大对象是否有及时释放？

---

## 工具配置

### 8.1 推荐工具

```bash
# 代码格式化
pip install black isort

# 代码检查
pip install flake8 pylint mypy

# 提交前检查
pip install pre-commit
```

### 8.2 pre-commit 配置

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88']
```

---

## 总结

遵循本指南可以：

1. **提高代码质量**: 统一的规范使代码更易读、易维护
2. **减少错误**: 类型提示和异常处理减少运行时错误
3. **促进协作**: 团队成员可以快速理解和修改代码
4. **便于自动化**: 格式化工具可以自动处理大部分风格问题

如有疑问或建议，请提交 Issue 或 PR。
