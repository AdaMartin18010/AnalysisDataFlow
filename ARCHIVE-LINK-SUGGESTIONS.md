# Archive.org 备份链接建议

> 生成时间: 2026-04-08 15:19:54
> 失效链接数: 1

## 失效链接及Archive备份

| 失效链接 | 错误信息 | Archive查询 | 源文件 |
|----------|----------|-------------|--------|
| [https://gist.github.com/sindresorhus/a39789f98801d...](https://gist.github.com/sindresorhus) | 连接超时 | [查看备份](https://web.archive.org/web/*/https://gist.github.com/sindresorhus/a39789f98801d908bbc7ff3ecc99d99c) | learning-platform\node_modules\rehype-re |

## 批量替换脚本

可以使用以下Python脚本批量替换失效链接为Archive备份：

```python
import re

# 定义替换映射
replace_map = {
    "https://gist.github.com/sindresorhus": "https://web.archive.org/web/20240000000000*/https://gist.github.com/sindresorhus",
}

# 读取文件并替换
with open('your-file.md', 'r', encoding='utf-8') as f:
    content = f.read()

for old, new in replace_map.items():
    content = content.replace(old, new)

with open('your-file.md', 'w', encoding='utf-8') as f:
    f.write(content)
```
