#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
形式化元素追踪器单元测试
"""

import unittest
import tempfile
from pathlib import Path
from scripts.automation.formal_element_tracker import (
    FormalElementTracker, ElementType, Stage
)


class TestFormalElementTracker(unittest.TestCase):
    """测试FormalElementTracker类"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.tracker = FormalElementTracker(root_dir=Path(self.temp_dir))
        
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_scan_file(self):
        """测试文件扫描"""
        test_file = Path(self.temp_dir) / "test.md"
        test_file.write_text("""# Test Document

## 概念定义

定义 `Def-S-01-01`: 第一定义。

定义 `Def-S-01-02`: 第二定义。

## 定理

定理 `Thm-S-01-01`: 重要定理。

引理 `Lemma-S-01-01`: 辅助引理。

命题 `Prop-K-02-01`: 一般命题。

推论 `Cor-S-01-01`: 直接推论。
""", encoding='utf-8')
        
        elements = self.tracker.scan_file(test_file)
        
        element_ids = [e.full_id for e in elements]
        self.assertIn("Def-S-01-01", element_ids)
        self.assertIn("Def-S-01-02", element_ids)
        self.assertIn("Thm-S-01-01", element_ids)
        self.assertIn("Lemma-S-01-01", element_ids)
        self.assertIn("Prop-K-02-01", element_ids)
        self.assertIn("Cor-S-01-01", element_ids)
        
        self.assertEqual(len(elements), 6)
        
    def test_type_mapping(self):
        """测试类型映射"""
        test_file = Path(self.temp_dir) / "test.md"
        test_file.write_text("""
`Theorem-S-01-01` should map to `Thm-S-01-01`.
`Proposition-K-01-01` should map to `Prop-K-01-01`.
`Corollary-F-01-01` should map to `Cor-F-01-01`.
""", encoding='utf-8')
        
        elements = self.tracker.scan_file(test_file)
        element_ids = [e.full_id for e in elements]
        
        self.assertIn("Thm-S-01-01", element_ids)
        self.assertIn("Prop-K-01-01", element_ids)
        self.assertIn("Cor-F-01-01", element_ids)
        
    def test_analyze_conflicts_duplicate(self):
        """测试重复检测"""
        # 创建两个文件，包含重复的定义
        file1 = Path(self.temp_dir) / "file1.md"
        file1.write_text("定义 `Def-S-01-01`: 定义1。", encoding='utf-8')
        
        file2 = Path(self.temp_dir) / "file2.md"
        file2.write_text("定义 `Def-S-01-01`: 定义1重复。", encoding='utf-8')
        
        result = self.tracker.scan_directory()
        
        # 检查是否有重复冲突
        duplicate_conflicts = [
            c for c in result.conflicts 
            if c.conflict_type == "duplicate"
        ]
        
        self.assertTrue(len(duplicate_conflicts) > 0)
        
    def test_suggest_new_id(self):
        """测试新ID建议"""
        # 创建包含一些元素的文件
        test_file = Path(self.temp_dir) / "test.md"
        test_file.write_text("""
`Def-S-01-01`
`Def-S-01-02`
`Def-S-01-03`
""", encoding='utf-8')
        
        result = self.tracker.scan_directory()
        
        # 建议新ID
        suggested_id = self.tracker.suggest_new_id("Def", "S", "01", result)
        self.assertEqual(suggested_id, "Def-S-01-04")
        

if __name__ == '__main__':
    unittest.main()
