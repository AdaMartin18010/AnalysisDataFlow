#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板验证器单元测试
"""

import unittest
import tempfile
from pathlib import Path
from scripts.automation.template_validator import (
    TemplateValidator, ValidationLevel, SectionType
)


class TestTemplateValidator(unittest.TestCase):
    """测试TemplateValidator类"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.validator = TemplateValidator()
        
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_classify_section(self):
        """测试章节分类"""
        self.assertEqual(
            self.validator._classify_section("概念定义"),
            SectionType.DEFINITIONS
        )
        self.assertEqual(
            self.validator._classify_section("Definitions"),
            SectionType.DEFINITIONS
        )
        self.assertEqual(
            self.validator._classify_section("属性推导"),
            SectionType.PROPERTIES
        )
        self.assertEqual(
            self.validator._classify_section("形式证明"),
            SectionType.PROOF
        )
        self.assertIsNone(
            self.validator._classify_section("Random Section")
        )
        
    def test_extract_formal_elements(self):
        """测试形式化元素提取"""
        content = """
这是一个定义 `Def-S-01-01`。
这是定理 `Thm-S-01-02` 的引用。
还有引理 `Lemma-K-02-03`。
"""
        elements = self.validator._extract_formal_elements(content)
        
        element_ids = [e.full_id for e in elements]
        self.assertIn("Def-S-01-01", element_ids)
        self.assertIn("Thm-S-01-02", element_ids)
        self.assertIn("Lemma-K-02-03", element_ids)
        
    def test_count_mermaid_diagrams(self):
        """测试Mermaid图表计数"""
        content = """
```mermaid
graph TD
    A --> B
```

Some text.

```mermaid
sequenceDiagram
    A->>B: message
```
"""
        count = self.validator._count_mermaid_diagrams(content)
        self.assertEqual(count, 2)
        
    def test_validate_file_valid(self):
        """测试有效文件验证"""
        test_file = Path(self.temp_dir) / "valid.md"
        test_file.write_text("""# Valid Document

> 所属阶段: Struct/ | 形式化等级: L3

## 1. 概念定义 (Definitions)

定义 `Def-S-01-01`: 这是一个定义。

## 2. 属性推导 (Properties)

引理 `Lemma-S-01-01`: 这是一个引理。

## 3. 关系建立 (Relations)

关系描述。

## 4. 论证过程 (Argumentation)

论证内容。

## 5. 形式证明 (Proof)

证明过程。

## 6. 实例验证 (Examples)

示例内容。

## 7. 可视化 (Visualizations)

```mermaid
graph TD
    A --> B
```

## 8. 引用参考 (References)

[^1]: Reference content
""", encoding='utf-8')
        
        result = self.validator.validate_file(test_file)
        
        # 应该有效
        self.assertTrue(result.score >= 80)
        self.assertTrue(result.has_header)
        self.assertEqual(result.formalization_level, "L3")
        
    def test_validate_file_invalid(self):
        """测试无效文件验证"""
        test_file = Path(self.temp_dir) / "invalid.md"
        test_file.write_text("""# Invalid Document

Missing header metadata.

## Some Random Section

Content without proper structure.
""", encoding='utf-8')
        
        result = self.validator.validate_file(test_file)
        
        # 应该有警告/错误
        self.assertTrue(len(result.issues) > 0)
        self.assertFalse(result.has_header)
        

if __name__ == '__main__':
    unittest.main()
