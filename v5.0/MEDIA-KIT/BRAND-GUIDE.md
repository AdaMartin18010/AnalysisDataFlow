# AnalysisDataFlow 品牌使用规范

> **版本**: v2.0 | **生效日期**: 2027-01-15 | **适用范围**: v5.0+

---

## 1. 品牌理念

### 品牌定位

**AnalysisDataFlow** 是流计算领域最全面的知识生态系统，致力于为开发者、架构师和研究者提供严格、完整、可导航的流计算知识库。

### 品牌个性

- 🔬 **专业严谨** - 形式化分析与严格论证
- 🚀 **前沿创新** - 紧跟技术发展趋势
- 🌐 **开放共享** - 开源协作与知识传播
- 💡 **实用导向** - 理论与实践相结合

### 品牌口号

> **"让流计算知识触手可及"**

英文: "Making Stream Computing Knowledge Accessible"

---

## 2. Logo规范

### Logo变体

#### 完整Logo (Full Logo)

```
[图标] AnalysisDataFlow
```

**使用场景**:

- 网站头部
- 演示文稿封面
- 宣传材料

#### 图标Logo (Icon)

```
[图标]
```

**使用场景**:

- Favicon
- 应用图标
- 社交媒体头像
- 小尺寸展示

#### 文字Logo (Wordmark)

```
AnalysisDataFlow
```

**使用场景**:

- 文章标题
- 水印
- 空间受限时

### Logo颜色变体

| 变体 | 浅色背景 | 深色背景 |
|------|----------|----------|
| 彩色 | 蓝色Logo | 白色Logo |
| 单色 | 黑色Logo | 白色Logo |

### 安全空间

Logo周围必须保留足够的空白空间：

```
┌─────────────────────────────┐
│                             │
│        [安全空间]            │
│                             │
│      [    Logo    ]         │
│                             │
│        [安全空间]            │
│                             │
└─────────────────────────────┘
```

最小安全空间 = Logo高度的 1/4

### 最小尺寸

| Logo类型 | 最小宽度 | 用途 |
|----------|----------|------|
| 完整Logo | 120px | 网页、印刷 |
| 图标Logo | 16px | Favicon |
| 图标Logo | 32px | 应用图标 |

---

## 3. 色彩系统

### 主色调

#### 品牌蓝 (Brand Blue)

```css
/* Primary Blue */
--color-primary: #0066CC;
--color-primary-light: #3385D6;
--color-primary-dark: #0052A3;
```

**使用场景**:

- Logo
- 主按钮
- 链接
- 重点强调

#### 科技青 (Tech Cyan)

```css
/* Secondary Cyan */
--color-secondary: #00A3E0;
--color-secondary-light: #33B5E6;
--color-secondary-dark: #0082B3;
```

**使用场景**:

- 辅助元素
- 高亮
- 图表
- 渐变

### 功能色

| 颜色 | 色值 | 用途 |
|------|------|------|
| 成功绿 | `#28A745` | 成功状态、正向数据 |
| 警告黄 | `#FFC107` | 警告、注意事项 |
| 错误红 | `#DC3545` | 错误、危险操作 |
| 信息蓝 | `#17A2B8` | 提示信息 |

### 中性色

```css
/* Dark Theme */
--color-bg-dark: #1A1A2E;
--color-surface-dark: #252541;
--color-text-primary-dark: #FFFFFF;
--color-text-secondary-dark: #B0B0C0;

/* Light Theme */
--color-bg-light: #FFFFFF;
--color-surface-light: #F5F5F7;
--color-text-primary-light: #1A1A2E;
--color-text-secondary-light: #6B6B7B;
```

### 渐变色

```css
/* Brand Gradient */
--gradient-primary: linear-gradient(135deg, #0066CC 0%, #00A3E0 100%);
--gradient-hero: linear-gradient(135deg, #1A1A2E 0%, #252541 50%, #0066CC 100%);
```

---

## 4. 字体规范

### 字体家族

```css
/* Primary Font */
font-family: 'Inter', system-ui, -apple-system, sans-serif;

/* Code Font */
font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace;

/* Chinese Font */
font-family: 'Inter', 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

### 字体层级

| 层级 | 大小 | 字重 | 用途 |
|------|------|------|------|
| H1 | 48px / 3rem | 700 | 页面主标题 |
| H2 | 36px / 2.25rem | 600 | 章节标题 |
| H3 | 24px / 1.5rem | 600 | 小节标题 |
| H4 | 20px / 1.25rem | 600 | 卡片标题 |
| Body | 16px / 1rem | 400 | 正文 |
| Small | 14px / 0.875rem | 400 | 辅助文字 |
| Caption | 12px / 0.75rem | 400 | 注释 |

### 代码字体

```css
code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  background: #F5F5F7;
  padding: 2px 6px;
  border-radius: 4px;
}
```

---

## 5. 视觉元素

### 图标风格

- **风格**: 线性图标 (Outline)
- **描边**: 2px
- **端点**: 圆角
- **尺寸**: 16px, 20px, 24px, 32px

### 图片风格

- **摄影**: 科技感、现代办公环境
- **插图**: 扁平化、品牌色点缀
- **图表**: 简洁清晰、品牌配色

### 圆角规范

| 元素 | 圆角 |
|------|------|
| 卡片 | 8px |
| 按钮 | 6px |
| 输入框 | 4px |
| 标签 | 16px (全圆角) |
| 头像 | 50% (圆形) |

### 阴影规范

```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
--shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
--shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
--shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1);
```

---

## 6. 应用场景

### 网站

- 使用品牌蓝作为主色
- Inter字体优先
- 深色/浅色主题可选
- 保持充足留白

### 演示文稿

- 封面使用品牌渐变背景
- 标题使用H1层级
- 每页不超过3个要点
- 使用品牌模板

### 社交媒体

- 头像使用图标Logo
- 封面使用品牌渐变
- 内容图使用品牌色点缀
- 保持视觉一致性

### 印刷品

- 使用CMYK色彩模式
- 300DPI分辨率
- 保留出血位
- 使用矢量Logo

---

## 7. 禁止使用

### Logo禁止

❌ **不要**:

- 改变Logo颜色
- 拉伸或压缩Logo
- 旋转Logo
- 添加阴影或效果
- 在复杂背景上使用
- 与其他Logo组合

### 色彩禁止

❌ **不要**:

- 使用非品牌色作为主色
- 将品牌色与冲突色搭配
- 降低品牌色对比度
- 使用过多颜色

---

## 8. 资源下载

- **Logo包**: [logo-pack.zip](./LOGO/logo-pack.zip)
- **色彩规范**: [color-palette.ase](./color-palette.ase)
- **字体**: [Google Fonts - Inter](https://fonts.google.com/specimen/Inter)
- **PPT模板**: [presentation-templates.zip](./PRESENTATION/templates.zip)

---

## 9. 联系方式

如有品牌使用相关问题，请联系：

- 📧 **邮箱**: <brand@analysisdataflow.org>
- 💬 **Slack**: #brand 频道

---

## 10. 更新记录

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v2.0 | 2027-01-15 | v5.0品牌升级，新增色彩系统 |
| v1.0 | 2026-04-01 | 初始版本 |

---

*AnalysisDataFlow Brand Guidelines v2.0*
