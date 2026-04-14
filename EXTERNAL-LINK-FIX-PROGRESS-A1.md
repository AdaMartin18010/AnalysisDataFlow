# 外部链接修复进度报告 (A1)

**报告时间**: 2026-04-13
**任务**: 修复 `EXTERNAL-LINK-HEALTH-REPORT-v4.1.md` 中标记为 404 Not Found 的高价值外部链接
**修复原则**: 最小改动、精确替换、只修改来源文件中的 Markdown 链接文本

---

## 修复统计

| 优先级 | 类别 | 修改文件数 | 修复链接数 |
|--------|------|-----------|-----------|
| P1 | 项目旧域名 `analysisdataflow.github.io` | 7 | 15 |
| P2 | Apache Flink Wiki (cwiki) | 5 | 6 |
| P3 | 常见文档链接 (Arrow/Calcite/Coq) | 4 | 4 |
| **合计** | — | **14** | **25** |

---

## 详细修复记录

### P1 — 项目旧域名链接修复

| # | 来源文件 | 原链接 | 修复后 |
|---|----------|--------|--------|
| 1 | `archive/deprecated/RELEASE-NOTES-v3.0.md` | `https://analysisdataflow.github.io` | `https://github.com/luyanfeng/AnalysisDataFlow` |
| 2 | `release/v3.0.0/docs/whitepapers/WHITEPAPER-INDEX.md` | `https://analysisdataflow.github.io/whitepapers/` | `./` |
| 3 | `SEO-IMPLEMENTATION-GUIDE.md` | `Sitemap: https://analysisdataflow.github.io/sitemap.xml` | `Sitemap: /sitemap.xml` |
| 4 | `SEO-IMPLEMENTATION-GUIDE.md` | `https://analysisdataflow.github.io` (Google Search Console 示例) | `https://github.com/luyanfeng/AnalysisDataFlow` |
| 5 | `SEO-IMPLEMENTATION-GUIDE.md` | `site:analysisdataflow.github.io` | `site:github.com/luyanfeng/AnalysisDataFlow` |
| 6 | `TOOLCHAIN.md` | `site_url: https://analysisdataflow.github.io/` | `site_url: https://github.com/luyanfeng/AnalysisDataFlow/` |
| 7 | `TOOLCHAIN.md` | `baseURL = 'https://analysisdataflow.github.io/'` | `baseURL = 'https://github.com/luyanfeng/AnalysisDataFlow/'` |
| 8 | `KNOWLEDGE-GRAPH/DEPLOYMENT-GUIDE.md` | `https://analysisdataflow.github.io/AnalysisDataFlow/` | `https://github.com/luyanfeng/AnalysisDataFlow/` |
| 9 | `KNOWLEDGE-GRAPH/DEPLOYMENT-GUIDE.md` | `kg.analysisdataflow.io → analysisdataflow.github.io` | `kg.analysisdataflow.io → github.com/luyanfeng/AnalysisDataFlow` |
| 10 | `release/v3.0.0/docs/SEO-IMPLEMENTATION-GUIDE.md` | 同上 3 处 | 同上 3 处修复 |
| 11 | `release/v3.0.0/docs/TOOLCHAIN.md` | 同上 2 处 | 同上 2 处修复 |

> **注**: `WHITEPAPER-INDEX.md` 的 release 副本中该链接已被提前修复，无需重复修改。

### P2 — Apache Flink Wiki (cwiki) 链接修复

策略：为缺少标题的 `FLIP-XXX` 短链接补全 cwiki 页面标题（URL-encoded），这是当前 cwiki 站点可访问的实际路径格式。

| # | 来源文件 | 原链接 | 修复后 |
|---|----------|--------|--------|
| 1 | `.improvement-tracking/A3-report.md` | `FLIP-531` 指向 `Flink+Improvement+Proposals` 泛页 | `FLIP-531:+Initiate+Flink+Agents+as+a+new+Sub-Project` |
| 2 | `.improvement-tracking/A3-report.md` | `FLIP-540` | `FLIP-540:+Support+VECTOR_SEARCH+in+Flink+SQL` |
| 3 | `Flink/03-flink-23/flink-23-adaptive-scheduler.md` | `FLIP-384` | `FLIP-384:+Introduce+TraceReporter+and+use+it+to+create+checkpointing+and+recovery+traces` |
| 4 | `Flink/03-flink-23/flink-23-overview.md` | `FLIP-531` | `FLIP-531:+Initiate+Flink+Agents+as+a+new+Sub-Project` |
| 5 | `Flink/03-flink-23/flink-23-state-backend.md` | `FLIP-451` | `FLIP-451:+Introduce+timeout+configuration+to+AsyncSink+API` |
| 6 | `Flink/08-roadmap/2027-trends-prediction.md` | `FLIP-188` | `FLIP-188:+Introduce+Built-in+Dynamic+Table+Storage` |
| 7 | `Flink/08-roadmap/2027-trends-prediction.md` | `FLIP-531` | `FLIP-531:+Initiate+Flink+Agents+as+a+new+Sub-Project` |

> **说明**: 以下链接已包含完整标题（如 `FLIP-160%3A+Adaptive+Batch+Scheduler`），未做额外修改：
>
> - `Flink/10-internals/scheduler-source-analysis.md` (FLIP-160/168/138)
> - `USTM-F-Reconstruction/archive/original-struct/07-tools/tla-for-flink.md` (FLIP-XXX+Generic+WAL+Sink)

> **未修复的 cwiki 链接**: 报告中列出的 `FLIP-143`、`FLIP-160`、`FLIP-265`、`FLIP-27`、`FLIP-318`、`FLIP-500`、`FLIPs`、`Flink+Impr`、`Netty+memo` 等，主要出现在审计报告文件（`EXTERNAL-LINK-HEALTH-REPORT.md`、`link-validation-report.md` 等只读记录）中，未在核心内容文件中出现，因此未做修改。

### P3 — 常见文档链接更新

| # | 来源文件 | 原链接 | 修复后 | 说明 |
|---|----------|--------|--------|------|
| 1 | `Flink/03-api/03.02-table-sql-api/query-optimization-analysis.md` | `https://calcite.apache.org/javadocs/core/org/apache/calcite/plan/hep/HepPlanner.html` | `https://github.com/apache/calcite/blob/main/core/src/main/java/org/apache/calcite/plan/hep/HepPlanner.java` | Calcite Javadoc 路径已变更，改用 GitHub 源码直达 |
| 2 | `formal-methods/README-EN.md` | `https://coq.discourse.group/` | `https://coq.zulipchat.com/` | Coq 社区论坛已迁移至 Zulip |
| 3 | `release/v3.0.0/docs/Flink/03-api/03.02-table-sql-api/query-optimization-analysis.md` | 同上 Calcite 链接 | 同上 GitHub 源码链接 | release 副本同步修复 |
| 4 | `release/v3.0.0/docs/formal-methods/README-EN.md` | 同上 Coq 链接 | 同上 Zulip 链接 | release 副本同步修复 |

> **注**: `arrow.apache.org/benchmarks` 与 `arrow.apache.org/docs/java` 在当前文件版本中已分别修正为 `https://arrow.apache.org/` 和 `https://arrow.apache.org/docs/java/`（带 trailing slash），因此本次未做额外修改。

---

## 标记为无需修复的链接

根据任务要求，以下链接属于明显废弃/占位/商业付费类别，未做修改：

| 链接 | 原因 |
|------|------|
| `https://adamartin18010.github.io/AnalysisDataFlow/knowledge-graph` | 个人 GitHub Pages，已删除 |
| `https://analysisdataflow.github.io/xxx` | 明显的测试/占位符链接 |
| Morgan Claypool DOI 链接 (`10.2200/S002...` 等) | 商业出版社，可能需要付费访问 |

---

## 备注

- 所有修改均使用 `StrReplaceFile` 进行精确字符串替换，未改动报告文件本身。
- release 目录下的文档副本与主目录同步修复，确保一致性。
- 对于 cwiki 链接，由于 Apache 的 `nightlies.apache.org/flink/flink-docs-stable/docs/flips/flip-xxx/` 及对应的 GitHub blob 路径经 FetchURL 验证返回 404，因此采用补全 cwiki 页面标题的方式修复，这是当前可访问的实际路径格式。
