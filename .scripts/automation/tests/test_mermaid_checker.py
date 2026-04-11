#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaid语法检查器单元测试
"""

import unittest
import tempfile
from pathlib import Path
from scripts.automation.mermaid_syntax_checker import (
    MermaidSyntaxChecker, DiagramType, SyntaxErrorType
)


class TestMermaidSyntaxChecker(unittest.TestCase):
    """测试MermaidSyntaxChecker类"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.checker = MermaidSyntaxChecker(root_dir=Path(self.temp_dir))
        
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir)
        
    def test_detect_diagram_type(self):
        """测试图表类型检测"""
        self.assertEqual(
            self.checker._detect_diagram_type("flowchart TD\nA --> B"),
            DiagramType.FLOWCHART
        )
        self.assertEqual(
            self.checker._detect_diagram_type("graph LR\nA --> B"),
            DiagramType.GRAPH
        )
        self.assertEqual(
            self.checker._detect_diagram_type("sequenceDiagram\nA->>B: msg"),
            DiagramType.SEQUENCE
        )
        self.assertEqual(
            self.checker._detect_diagram_type("classDiagram\nclass A"),
            DiagramType.CLASS
        )
        self.assertEqual(
            self.checker._detect_diagram_type("unknown syntax"),
            DiagramType.UNKNOWN
        )
        
    def test_parse_flowchart(self):
        """测试Flowchart解析"""
        content = """
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
"""
        info = self.checker._parse_flowchart(content)
        
        self.assertEqual(info.diagram_type, DiagramType.FLOWCHART)
        self.assertEqual(len(info.nodes), 5)
        self.assertEqual(len(info.edges), 5)
        
        node_ids = [n.node_id for n in info.nodes]
        self.assertIn("A", node_ids)
        self.assertIn("B", node_ids)
        self.assertIn("C", node_ids)
        self.assertIn("D", node_ids)
        self.assertIn("E", node_ids)
        
    def test_parse_flowchart_with_undefined_nodes(self):
        """测试检测未定义节点"""
        content = """
graph TD
    A[Start] --> B[End]
    C --> D  // C and D are not defined
"""
        info = self.checker._parse_flowchart(content)
        
        # 应该有未定义节点的错误
        undefined_errors = [
            e for e in info.errors 
            if e.error_type == SyntaxErrorType.UNDEFINED_NODE
        ]
        self.assertEqual(len(undefined_errors), 2)
        
    def test_parse_sequence_diagram(self):
        """测试序列图解析"""
        content = """
sequenceDiagram
    participant A as Alice
    participant B as Bob
    A->>B: Hello
    B->>A: Hi
"""
        info = self.checker._parse_sequence_diagram(content)
        
        self.assertEqual(info.diagram_type, DiagramType.SEQUENCE)
        self.assertEqual(len(info.nodes), 2)
        self.assertEqual(len(info.edges), 2)
        
    def test_scan_file(self):
        """测试文件扫描"""
        test_file = Path(self.temp_dir) / "test.md"
        test_file.write_text("""# Test Document

## Diagram 1

```mermaid
graph TD
    A --> B
```

## Diagram 2

```mermaid
sequenceDiagram
    A->>B: message
```

Not a diagram.

```mermaid
invalid syntax here
```
""", encoding='utf-8')
        
        blocks = self.checker.scan_file(test_file)
        
        self.assertEqual(len(blocks), 3)
        
        # 检查类型
        types = [b.diagram_info.diagram_type for b in blocks if b.diagram_info]
        self.assertIn(DiagramType.GRAPH, types)
        self.assertIn(DiagramType.SEQUENCE, types)
        
    def test_check_empty_diagram(self):
        """测试空图表检测"""
        content = """
graph TD
    %% Just a comment
"""
        block = self.checker.check_block(content)
        
        empty_errors = [
            e for e in block.diagram_info.errors 
            if e.error_type == SyntaxErrorType.EMPTY_DIAGRAM
        ]
        self.assertEqual(len(empty_errors), 1)
        

if __name__ == '__main__':
    unittest.main()
