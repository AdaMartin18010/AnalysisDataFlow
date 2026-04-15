# Archive.org 备份链接建议

> 生成时间: 2026-04-16 00:05:03
> 失效链接数: 5

## 失效链接及Archive备份

| 失效链接 | 错误信息 | Archive查询 | 源文件 |
|----------|----------|-------------|--------|
| [https://archive.org/web/*/https://nightlies.apache...](https://archive.org/web/*/https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/dev/datastream/fault-tolerance/queryable_state/) | 连接超时 | [查看备份](https://web.archive.org/web/*/https://archive.org/web/*/https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/dev/datastream/fault-tolerance/queryable_state/) | Flink\02-core\flink-state-management-com |
| [https://github.com/your-org/AnalysisDataFlow...](https://github.com/your-org/AnalysisDataFlow) | HTTP 404 | [查看备份](https://web.archive.org/web/*/https://github.com/your-org/AnalysisDataFlow) | RELEASE-NOTES-v5.0.0-DRAFT.md, archive\d |
| [https://github.com/luyanfeng/AnalysisDataFlow/acti...](https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/pr-quality-gate.yml/badge.svg) | HTTP 404 | [查看备份](https://web.archive.org/web/*/https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/pr-quality-gate.yml/badge.svg) | release\v3.0.0\docs\i18n\ja\README-ja.md |
| [https://en.wikipedia.org/wiki/Category_theory...](https://en.wikipedia.org/wiki/Category_theory) | 连接超时 | [查看备份](https://web.archive.org/web/*/https://en.wikipedia.org/wiki/Category_theory) | formal-methods\98-appendices\wikipedia-c |
| [https://cert.analysisdataflow.org/verify...](https://cert.analysisdataflow.org/verify) | 客户端错误: Cannot connect to host  | [查看备份](https://web.archive.org/web/*/https://cert.analysisdataflow.org/verify) | docs\certification\csa\exam-guide-csa.md |

## 批量替换脚本

可以使用以下Python脚本批量替换失效链接为Archive备份：

```python
import re

# 定义替换映射
replace_map = {
    "https://archive.org/web/*/https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/dev/datastream/fault-tolerance/queryable_state/": "https://web.archive.org/web/20240000000000*/https://archive.org/web/*/https://nightlies.apache.org/flink/flink-docs-release-1.16/docs/dev/datastream/fault-tolerance/queryable_state/",
    "https://github.com/your-org/AnalysisDataFlow": "https://web.archive.org/web/20240000000000*/https://github.com/your-org/AnalysisDataFlow",
    "https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/pr-quality-gate.yml/badge.svg": "https://web.archive.org/web/20240000000000*/https://github.com/luyanfeng/AnalysisDataFlow/actions/workflows/pr-quality-gate.yml/badge.svg",
    "https://en.wikipedia.org/wiki/Category_theory": "https://web.archive.org/web/20240000000000*/https://en.wikipedia.org/wiki/Category_theory",
    "https://cert.analysisdataflow.org/verify": "https://web.archive.org/web/20240000000000*/https://cert.analysisdataflow.org/verify",
}

# 读取文件并替换
with open('your-file.md', 'r', encoding='utf-8') as f:
    content = f.read()

for old, new in replace_map.items():
    content = content.replace(old, new)

with open('your-file.md', 'w', encoding='utf-8') as f:
    f.write(content)
```
