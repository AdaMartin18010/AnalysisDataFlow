# AnalysisDataFlow Logo 使用指南

> **版本**: v2.0 | **生效日期**: 2027-01-15

---

## Logo 设计说明

### 设计概念

AnalysisDataFlow Logo 融合了以下元素：

- **数据流**: 抽象的流动线条代表数据流
- **分析**: 几何结构体现分析的思维
- **连接**: 节点间的连线表示知识的关联
- **无限**: 环形结构象征持续学习的循环

### 设计理念

```
简约、现代、科技感
可识别、可记忆、可扩展
```

---

## Logo 变体

### 1. 完整Logo (Full Logo)

**描述**: 图标 + 文字组合

**适用场景**:

- 网站头部
- 演示文稿封面
- 宣传海报
- 社交媒体封面

**最小尺寸**: 120px 宽度

### 2. 图标Logo (Icon Mark)

**描述**: 纯图标，无文字

**适用场景**:

- Favicon
- 应用图标
- 社交媒体头像
- 小尺寸展示
- 水印

**尺寸规格**:

- 16x16px (Favicon)
- 32x32px (App Icon)
- 64x64px (Avatar)
- 128x128px (High-res)
- 256x256px (App Store)
- 512x512px (Play Store)

### 3. 文字Logo (Wordmark)

**描述**: 纯文字 "AnalysisDataFlow"

**适用场景**:

- 文章标题
- 水印
- 空间受限时
- 纯文字环境

---

## 颜色规范

### 主色 Logo

**背景**: 浅色/白色背景

```
图标: 品牌蓝 #0066CC
文字: 深灰 #1A1A2E
```

### 反色 Logo

**背景**: 深色/品牌蓝背景

```
图标: 白色 #FFFFFF
文字: 白色 #FFFFFF
```

### 单色 Logo

**用途**: 特殊印刷、水印

```
深色背景: 白色
浅色背景: 黑色 #1A1A2E
```

---

## 安全空间

### 安全空间定义

Logo 周围必须保留的最小空白区域：

```
安全空间 = Logo 高度的 1/4
```

### 示例

```
        [安全空间]
            ↓
    ┌─────────────────┐
    │   [安全空间]    │
    │                 │
    │   [   Logo   ]  │ ← [安全空间]
    │                 │
    │   [安全空间]    │
    └─────────────────┘
            ↑
        [安全空间]
```

---

## 使用示例

### 正确用法 ✅

| 场景 | 使用变体 | 背景 | 尺寸 |
|------|----------|------|------|
| 网站头部 | 完整Logo | 白色 | 高度 40px |
| Favicon | 图标Logo | - | 16x16px |
| App图标 | 图标Logo | 品牌蓝 | 512x512px |
| 深色海报 | 反色Logo | 深蓝 | 高度 100px |
| 水印 | 单色Logo | 任意 | 高度 20px |

### 错误用法 ❌

| 错误类型 | 示例 | 后果 |
|----------|------|------|
| 改变颜色 | 将蓝色改为红色 | 品牌识别混乱 |
| 拉伸变形 | 宽度拉伸150% | 失去比例美感 |
| 添加效果 | 添加阴影/发光 | 视觉混乱 |
| 低对比度 | 蓝色Logo放蓝色背景 | 无法识别 |
| 与其他元素重叠 | Logo压在图片上 | 可读性差 |

---

## 文件格式

### 矢量格式 (推荐)

| 格式 | 用途 | 优点 |
|------|------|------|
| SVG | 网页、大屏 | 无限缩放、体积小 |
| AI | 设计编辑 | 可编辑源文件 |
| EPS | 印刷 | 广泛兼容 |
| PDF | 通用 | 跨平台 |

### 位图格式

| 格式 | 用途 | 背景 |
|------|------|------|
| PNG | 网页、App | 透明背景 |
| JPG | 摄影背景 | 白色背景 |
| WebP | 现代网页 | 透明/不透明 |
| ICO | Windows图标 | 多尺寸 |
| ICNS | macOS图标 | 多尺寸 |

---

## 下载包内容

### logo-pack.zip

```
logo-pack/
├── svg/
│   ├── logo-full.svg
│   ├── logo-icon.svg
│   └── logo-wordmark.svg
├── png/
│   ├── logo-full-dark.png
│   ├── logo-full-light.png
│   ├── logo-icon-512.png
│   ├── logo-icon-256.png
│   ├── logo-icon-128.png
│   ├── logo-icon-64.png
│   ├── logo-icon-32.png
│   └── logo-icon-16.png
├── ico/
│   ├── favicon.ico
│   └── favicon-32.ico
└── source/
    ├── logo-master.ai
    └── logo-master.fig
```

---

## 实际应用示例

### 网站应用

```html
<!-- 网站头部 -->
<header>
  <img src="logo-full.svg" height="40" alt="AnalysisDataFlow">
</header>

<!-- Favicon -->
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="logo-icon-32.png">
```

### 社交媒体

| 平台 | 图片 | 尺寸 |
|------|------|------|
| Twitter/X | 头像 | 400x400px |
| Twitter/X | Header | 1500x500px |
| GitHub | Avatar | 500x500px |
| LinkedIn | Logo | 300x300px |
| 微信 | 头像 | 200x200px |

### 印刷品

| 物品 | Logo变体 | 建议尺寸 |
|------|----------|----------|
| 名片 | 图标Logo | 20x20mm |
| 宣传册 | 完整Logo | 宽度 40mm |
| 海报 | 完整Logo | 宽度 100mm |
| 易拉宝 | 完整Logo | 宽度 200mm |
| T恤 | 图标Logo | 宽度 100mm |

---

## 常见问题

**Q: 可以在深色背景上使用主色Logo吗？**
A: 不可以。深色背景请使用反色Logo（白色）。

**Q: 可以改变Logo的颜色以匹配活动主题吗？**
A: 不可以。必须使用官方提供的颜色变体。

**Q: 可以在Logo周围添加边框吗？**
A: 不可以。Logo周围必须保持安全空间。

**Q: 可以将Logo用于商业用途吗？**
A: 遵循 Apache 2.0 许可证，可以商业使用，但需注明来源。

---

## 联系我们

如有Logo使用相关问题，请联系：

- 📧 **邮箱**: <brand@analysisdataflow.org>
- 💬 **Slack**: #brand 频道

---

*AnalysisDataFlow Logo Usage Guide v2.0*
