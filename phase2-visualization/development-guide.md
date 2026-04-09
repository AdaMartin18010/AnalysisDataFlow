# 可视化组件开发指南

## 开发环境

### 基本要求

- 现代浏览器 (Chrome, Firefox, Safari)
- 文本编辑器 (VS Code 推荐)
- 基本 HTML/CSS/JavaScript 知识

### 项目结构

```
phase2-visualization/
├── component-name/
│   ├── index.html
│   ├── style.css
│   └── script.js
```

## 开发规范

### HTML 规范

- 使用语义化标签
- 添加适当的 ARIA 属性
- 确保可访问性

### CSS 规范

- 使用 CSS 变量定义主题色
- 支持深色/浅色模式
- 响应式设计

### JavaScript 规范

- 使用现代 ES6+ 语法
- 添加错误处理
- 避免全局变量

## 示例组件

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Component</title>
    <style>
        :root {
            --primary-color: #3b82f6;
        }
        body {
            background: var(--bg-color, #fff);
        }
    </style>
</head>
<body>
    <h1>My Component</h1>
    <script>
        // Component logic
    </script>
</body>
</html>
```

---

*Development Guide*
