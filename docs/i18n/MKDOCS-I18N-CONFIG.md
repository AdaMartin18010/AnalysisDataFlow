# MkDocs Material 多语言配置参考

> **用途**: 为 AnalysisDataFlow 文档站点部署提供 MkDocs Material + i18n 插件的配置参考
>
> **关联文档**: [ARCHITECTURE.md](./ARCHITECTURE.md)、[../i18n/TRANSLATION-STRATEGY.md]

---

## 1. 推荐的 `mkdocs.yml` 配置

以下配置基于项目统一后的目录结构（`docs/i18n/en/` 作为英文站点源）：

```yaml
site_name: AnalysisDataFlow
site_url: https://your-domain.com/
repo_url: https://github.com/luyanfeng/AnalysisDataFlow

# 主题配置
theme:
  name: material
  language: zh
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.suggest
    - search.highlight
    - content.tabs.link
    - content.code.annotation
    - content.code.copy
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode

# 插件配置
plugins:
  - search:
      lang:
        - zh
        - en
      # MkDocs Material 内置搜索支持多语言索引
      # 但每个语言版本构建时会生成独立的搜索索引

  - i18n:
      docs_structure: folder
      fallback_to_default: true
      languages:
        - locale: zh
          name: 中文
          default: true
          build: true
          site_name: AnalysisDataFlow
          # 中文源文档位于项目根目录
          # 若使用 docs/i18n/ 作为多语言根,需通过 extra 或 hooks 映射
        - locale: en
          name: English
          build: true
          site_name: AnalysisDataFlow
          # 英文文档源: docs/i18n/en/
          # 构建后路径: /en/

# 扩展
markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - tables
  - attr_list
  - md_in_html
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - pymdownx.arithmatex:
      generic: true
  - def_list
  - pymdownx.tasklist:
      custom_checkbox: true

extra_javascript:
  - javascripts/mathjax.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js

# 额外配置
extra:
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/luyanfeng/AnalysisDataFlow
  version:
    provider: mike
```

---

## 2. 语言回退 (Fallback) 配置

MkDocs Material 的 `mkdocs-static-i18n` 插件支持 `fallback_to_default`：

```yaml
plugins:
  - i18n:
      fallback_to_default: true
      languages:
        - locale: zh
          default: true
        - locale: en
```

**行为说明**:

- 当用户访问英文版页面（如 `/en/flink/overview/`），但该页面尚未翻译时，插件会自动回退到默认语言（中文）的对应页面。
- 若回退页面也不存在，则显示 404 页面。

**项目当前状态**:

- `docs/i18n/config/i18n-config.yaml` 中已启用 `fallback_to_default: true`
- 实际部署时需在 `mkdocs.yml` 中确认该配置生效

---

## 3. 多语言搜索配置

### 3.1 独立语言索引

MkDocs Material 的搜索插件会在每次构建时为当前语言生成独立的搜索索引。这意味着：

- 中文站点 (`/`) 的搜索只索引中文内容
- 英文站点 (`/en/`) 的搜索只索引英文内容

这是推荐做法，可避免中英文术语混排导致的搜索质量下降。

### 3.2 搜索语言支持

确保 `plugins.search.lang` 包含对应的语言代码：

```yaml
plugins:
  - search:
      lang:
        - zh        # 中文(支持简体和繁体)
        - en        # 英文
```

> **注意**: `zh` 搜索支持需要 MkDocs Material 版本 >= 8.2.0。

### 3.3 缺失语言页面的搜索行为

如果某篇文档只有中文版本，用户通过英文版搜索时：

- 若该文档已被翻译（存在于 `docs/i18n/en/`），则英文搜索可命中
- 若未翻译，由于 `fallback_to_default: true`，用户可能通过中文搜索命中，但英文搜索不会索引该文档

**建议**: 对于重要的导航页和指南，优先保证英文翻译，以提升英文搜索覆盖率。

---

## 4. 目录挂载示例

当前实际目录结构与 MkDocs `docs_structure: folder` 模式的映射：

```
docs/
├── i18n/
│   ├── en/          # 英文文档(构建为 /en/)
│   ├── de/          # 德文文档(构建为 /de/)
│   ├── fr/          # 法文文档(构建为 /fr/)
│   ├── ja/          # 日文文档(构建为 /ja/)
│   └── zh/          # 中文指针(可选)
└── ...              # 其他站点页面
```

中文源文档实际位于项目根目录（`Struct/`、`Knowledge/`、`Flink/`、`README.md` 等）。若要将这些根目录内容也纳入 MkDocs 构建，可使用 `mkdocs.yml` 中的 `extra` 配置或预构建脚本将它们复制到 `docs/zh/` 下。

**更简单的方案**（推荐）:

在构建前运行同步脚本：

```bash
# 将根目录中文文档复制到 docs/zh/ 作为 MkDocs 源
mkdir -p docs/zh
cp -r Struct Knowledge Flink docs/zh/
cp README.md QUICK-START.md ARCHITECTURE.md GLOSSARY.md docs/zh/
```

然后在 `mkdocs.yml` 中配置：

```yaml
plugins:
  - i18n:
      docs_structure: folder
      languages:
        - locale: zh
          name: 中文
          default: true
          # docs/zh/ 作为中文源
        - locale: en
          name: English
          # docs/i18n/en/ 作为英文源
```

---

## 5. 部署检查清单

在将多语言站点部署到 GitHub Pages / Vercel / Netlify 前，请确认：

- [ ] `mkdocs.yml` 中 `plugins.i18n.fallback_to_default` 设置为 `true`
- [ ] `plugins.search.lang` 包含 `zh` 和 `en`
- [ ] 英文文档已统一放入 `docs/i18n/en/`（根目录 `en/` 仅保留 redirect）
- [ ] 中文文档已同步到 `docs/` 下的适当位置（或构建脚本已配置）
- [ ] 语言切换器在页眉或页脚可见
- [ ] 测试从英文页面切换到中文页面时，链接能正确映射
- [ ] 测试访问未翻译的英文页面时，能正确回退到中文版本
- [ ] 英文搜索能命中 `docs/i18n/en/` 中的内容

---

## 6. 参考链接

- [MkDocs Material i18n Plugin Documentation](https://ultrabug.github.io/mkdocs-static-i18n/)
- [MkDocs Material Search Configuration](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/)
- [Doks Multilingual Guide](https://getdoks.org/docs/guides/i18n/)

---

> **Last Updated**: 2026-04-15
