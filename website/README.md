# AnalysisDataFlow 交互式导航网站

## 项目结构

```
website/
├── index.html              # 主页
├── chains/
│   ├── index.html          # 推导链列表
│   ├── checkpoint.html     # Checkpoint 推导链
│   └── exactly-once.html   # Exactly-Once 推导链
├── graph/
│   └── index.html          # 交互式依赖图 (D3.js)
├── search/
│   └── index.html          # 全文搜索 (Fuse.js)
├── assets/
│   ├── css/
│   │   └── main.css        # 主样式表
│   ├── js/
│   │   └── main.js         # 主脚本
│   └── images/             # 图片资源
└── data/
    ├── search-index.json   # 搜索索引数据
    └── graph-data.json     # 图谱数据
```

## 功能特性

### 1. 响应式设计

- 支持桌面端和移动端
- 自适应侧边栏导航
- 流畅的过渡动画

### 2. 主题切换

- 支持暗色/亮色主题
- 本地存储主题偏好
- GitHub 风格界面

### 3. 推导链可视化

- 4层结构展示：基础定义 → 性质推导 → 关系建立 → 形式证明
- Checkpoint 正确性证明链
- Exactly-Once 端到端正确性证明链

### 4. 交互式依赖图 (D3.js)

- 可缩放、可拖拽的力导向图
- 5,200+ 关系边可视化
- 分层筛选 (Struct/Knowledge/Flink)

### 5. 全文搜索 (Fuse.js)

- 模糊匹配搜索
- 按类型筛选 (定理/定义/引理/命题/推论)
- 40+ 形式化元素索引

## 技术栈

- **HTML5** + **CSS3** + **JavaScript**
- **D3.js** v7 - 数据可视化
- **Fuse.js** v6 - 模糊搜索
- **Prism.js** - 代码高亮
- **Font Awesome** - 图标

## 使用说明

1. 打开 `index.html` 进入主页
2. 点击左侧导航或使用汉堡菜单切换页面
3. 在搜索页面输入关键词查找定理/定义
4. 在图谱页面拖拽节点、滚轮缩放

## 页面统计

- 总页面数: 6 个
- CSS 代码: ~600 行
- JavaScript 代码: ~400 行
- 数据文件: 2 个 (搜索索引 + 图谱数据)

## 浏览器支持

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
