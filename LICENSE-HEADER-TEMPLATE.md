# 文档头部许可证声明模板

> 本文档提供 AnalysisDataFlow 项目文档头部的标准许可证声明格式

---

## 推荐格式

### 简短格式 (推荐用于大多数文档)

在每篇 Markdown 文档的 YAML Front Matter 或首行注释中添加：

```markdown
---
# 在 YAML Front Matter 中添加 (如果文档使用 YAML 头部)
license: "Apache-2.0"
copyright: "Copyright 2026 AdaMartin18010"
---

<!-- 或在文档开头添加简短注释 -->
<!--
  Copyright 2026 AdaMartin18010
  Licensed under Apache License 2.0
  See LICENSE and LICENSE-NOTICE.md for details
-->
```

### 完整格式 (可选)

```markdown
<!--
  AnalysisDataFlow - 统一流计算理论模型与工程实践知识库

  Copyright 2026 AdaMartin18010

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

  Third-party attributions: See THIRD-PARTY-NOTICES.md
-->
```

---

## 按文档类型的建议

### Struct/ 目录 (形式理论文档)

建议添加简短版权声明在文档头部：

```markdown
<!--
  Copyright 2026 AdaMartin18010 | Apache-2.0
  Part of AnalysisDataFlow: https://github.com/luyanfeng/AnalysisDataFlow
-->

# 文档标题
...
```

### Knowledge/ 目录 (工程实践文档)

```markdown
<!--
  Copyright 2026 AdaMartin18010 | Apache-2.0
  AnalysisDataFlow Project - 流计算知识库
-->

# 文档标题
...
```

### Flink/ 目录 (Flink 专项文档)

```markdown
<!--
  Copyright 2026 AdaMartin18010 | Apache-2.0
  AnalysisDataFlow - Flink 技术分析
  部分内容基于 Apache Flink (Apache-2.0)
-->

# 文档标题
...
```

---

## 批量添加脚本

### 使用 PowerShell 批量添加

```powershell
# 为所有 Markdown 文件添加简短许可证头
$licenseHeader = @"<!-- Copyright 2026 AdaMartin18010 | Apache-2.0 | AnalysisDataFlow -->

"@

Get-ChildItem -Path "Struct", "Knowledge", "Flink" -Recurse -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    if (-not $content.StartsWith("<!-- Copyright")) {
        $newContent = $licenseHeader + $content
        Set-Content -Path $_.FullName -Value $newContent -NoNewline
        Write-Host "Updated: $($_.FullName)"
    }
}
```

### 使用 Python 批量添加

```python
import os

LICENSE_HEADER = """<!-- Copyright 2026 AdaMartin18010 | Apache-2.0 | AnalysisDataFlow -->

"""

def add_license_to_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已有版权声明
    if content.startswith("<!-- Copyright"):
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(LICENSE_HEADER + content)
    return True

# 遍历目录
dirs = ['Struct', 'Knowledge', 'Flink']
for dir_name in dirs:
    for root, dirs, files in os.walk(dir_name):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if add_license_to_file(filepath):
                    print(f"Updated: {filepath}")
```

---

## 注意事项

1. **不要修改已有版权声明的文档** - 如果文档已有版权声明，请勿覆盖
2. **保持格式一致** - 使用统一格式便于识别
3. **引用第三方内容时** - 请在文档中明确标注引用来源
4. **代码示例** - 代码块内的示例代码不需要添加版权声明

---

**最后更新**: 2026-04-03
**文档版本**: v1.0
