#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用验证器单元测试
"""

import unittest
import tempfile
from pathlib import Path
from scripts.automation.cross_ref_validator import (
    CrossRefValidator, LinkInfo, LinkType, LinkStatus
)


class TestCrossRefValidator(unittest.TestCase):
    """测试CrossRefValidator类"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.validator = CrossRefValidator(root_dir=Path(self.temp_dir))
        
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_is_external_url(self):
        """测试外部URL识别"""
        self.assertTrue(self.validator._is_external_url("https://example.com"))
        self.assertTrue(self.validator._is_external_url("http://test.org/page"))
        self.assertFalse(self.validator._is_external_url("./relative/path.md"))
        self.assertFalse(self.validator._is_external_url("/absolute/path.md"))
        self.assertFalse(self.validator._is_external_url("path/to/file.md#anchor"))
        
    def test_parse_link(self):
        """测试链接解析"""
        # 文件+锚点
        file_path, anchor = self.validator._parse_link("path/to/file.md#section")
        self.assertEqual(file_path, "path/to/file.md")
        self.assertEqual(anchor, "section")
        
        # 仅锚点
        file_path, anchor = self.validator._parse_link("#anchor")
        self.assertEqual(file_path, "")
        self.assertEqual(anchor, "anchor")
        
        # 仅文件
        file_path, anchor = self.validator._parse_link("path/to/file.md")
        self.assertEqual(file_path, "path/to/file.md")
        self.assertIsNone(anchor)
        
    def test_extract_anchors(self):
        """测试锚点提取"""
        content = """
# Main Title
## Section 1
### Subsection A
## Section 2
<a id="custom-anchor"></a>
"""
        anchors = self.validator._extract_anchors(content)
        
        self.assertIn("main-title", anchors)
        self.assertIn("section-1", anchors)
        self.assertIn("subsection-a", anchors)
        self.assertIn("custom-anchor", anchors)
        
    def test_extract_references(self):
        """测试引用提取"""
        content = """
Some text with reference[^1] and another[^2].

[^1]: First reference
[^2]: Second reference with https://example.com
"""
        refs = self.validator._extract_references(content)
        
        self.assertEqual(refs.get("1"), "First reference")
        self.assertIn("Second reference", refs.get("2", ""))
        
    def test_scan_file(self):
        """测试文件扫描"""
        # 创建测试文件
        test_file = Path(self.temp_dir) / "test.md"
        test_file.write_text("""
# Test Document

This is a [link to external](https://example.com) site.
Here is an [internal link](./other.md) and [another with anchor](./other.md#section).

Reference test[^1].

[^1]: Reference content
""", encoding='utf-8')
        
        links = self.validator.scan_file(test_file)
        
        # 检查是否找到所有链接
        link_types = [l.link_type for l in links]
        self.assertIn(LinkType.EXTERNAL_URL, link_types)
        self.assertIn(LinkType.INTERNAL_FILE, link_types)
        self.assertIn(LinkType.INTERNAL_ANCHOR, link_types)
        self.assertIn(LinkType.REFERENCE, link_types)
        
    def test_validate_internal_link(self):
        """测试内部链接验证"""
        # 创建目标文件
        target_file = Path(self.temp_dir) / "target.md"
        target_file.write_text("# Target\n## Section 1", encoding='utf-8')
        
        # 创建源文件
        source_file = Path(self.temp_dir) / "source.md"
        source_file.write_text("# Source", encoding='utf-8')
        
        # 测试有效链接
        valid_link = LinkInfo(
            source_file="source.md",
            link_text="Valid Link",
            link_target="target.md",
            link_type=LinkType.INTERNAL_FILE,
            line_number=1,
            column_number=1
        )
        result = self.validator.validate_internal_link(valid_link)
        self.assertEqual(result.status, LinkStatus.VALID)
        
        # 测试无效链接
        invalid_link = LinkInfo(
            source_file="source.md",
            link_text="Invalid Link",
            link_target="nonexistent.md",
            link_type=LinkType.INTERNAL_FILE,
            line_number=1,
            column_number=1
        )
        result = self.validator.validate_internal_link(invalid_link)
        self.assertEqual(result.status, LinkStatus.INVALID)
        

if __name__ == '__main__':
    unittest.main()
