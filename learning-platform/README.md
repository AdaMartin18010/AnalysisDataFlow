# Flink 学习平台

一个基于静态网站技术的在线学习平台，专注于 Apache Flink 流处理技术教育。

## 功能特性

- **系统课程**: 3门完整课程，17个课时，涵盖基础到高级
- **编程挑战**: 20个实战编程挑战，巩固学习成果
- **代码编辑器**: 集成 Monaco Editor，支持语法高亮
- **进度跟踪**: LocalStorage 本地存储学习进度
- **证书生成**: PDF 证书导出功能
- **响应式设计**: 适配桌面和移动设备

## 技术栈

- **框架**: Next.js 14 (App Router)
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **组件**: shadcn/ui
- **编辑器**: Monaco Editor (@monaco-editor/react)
- **图表**: Mermaid
- **PDF导出**: jsPDF + html2canvas
- **图标**: Lucide React

## 课程大纲

### 课程1: Flink基础入门 (8课时)

1. 流处理概念介绍
2. Flink架构概览
3. DataStream API入门
4. 状态管理基础
5. Checkpoint机制
6. Window操作详解
7. 连接器使用
8. 部署实践

### 课程2: 流处理原理 (5课时)

1. Watermark机制
2. 时间语义详解
3. 一致性模型
4. 背压处理
5. 性能调优

### 课程3: 生产实践 (4课时)

1. 监控告警系统
2. 故障排查指南
3. 集群运维
4. 升级迁移

## 编程挑战列表

| 编号 | 标题 | 难度 | 分类 |
|------|------|------|------|
| 01 | Hello DataStream | 简单 | 基础API |
| 02 | Map转换操作 | 简单 | 基础API |
| 03 | Filter过滤 | 简单 | 基础API |
| 04 | KeyBy分组 | 中等 | 基础API |
| 05 | Tumbling Window | 中等 | Window |
| 06 | Watermark生成 | 中等 | 时间语义 |
| 07 | 状态编程 | 中等 | 状态管理 |
| 08 | Checkpoint配置 | 中等 | 容错机制 |
| 09 | Kafka Source | 中等 | 连接器 |
| 10 | Side Output | 困难 | 高级特性 |
| 11 | Async IO | 困难 | 高级特性 |
| 12 | Session Window | 中等 | Window |
| 13 | Table API基础 | 简单 | Table API |
| 14 | ProcessFunction计时器 | 困难 | 高级特性 |
| 15 | CEP模式匹配 | 困难 | 高级特性 |
| 16 | 广播状态 | 困难 | 高级特性 |
| 17 | Flink SQL | 简单 | Table API |
| 18 | Savepoint管理 | 中等 | 容错机制 |
| 19 | Metrics监控 | 中等 | 监控 |
| 20 | 端到端Exactly-Once | 困难 | 容错机制 |

## 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建静态导出
npm run build
```

## 部署到GitHub Pages

1. Fork 本仓库到你的 GitHub 账号
2. 进入仓库 Settings > Pages
3. Source 选择 "GitHub Actions"
4. 推送代码到 main 分支，自动触发部署

## 项目结构

```
learning-platform/
├── .github/workflows/    # GitHub Actions 配置
├── src/
│   ├── app/             # Next.js App Router
│   │   ├── courses/     # 课程相关页面
│   │   ├── challenges/  # 挑战相关页面
│   │   ├── certificates/# 证书页面
│   │   ├── page.tsx     # 首页
│   │   ├── layout.tsx   # 根布局
│   │   └── globals.css  # 全局样式
│   ├── components/      # React 组件
│   │   ├── ui/          # UI 组件
│   │   ├── CodeEditor.tsx
│   │   ├── CourseCard.tsx
│   │   ├── CoursePlayer.tsx
│   │   ├── CertificateGenerator.tsx
│   │   ├── ChallengeCard.tsx
│   │   ├── ProgressTracker.tsx
│   │   ├── Navbar.tsx
│   │   └── Mermaid.tsx
│   ├── hooks/           # 自定义 Hooks
│   │   └── useProgress.ts
│   ├── lib/             # 工具函数和数据
│   │   ├── utils.ts
│   │   ├── courses.ts   # 课程数据
│   │   ├── challenges.ts# 挑战数据
│   │   └── progress.ts  # 进度管理
│   └── types/           # TypeScript 类型
├── public/              # 静态资源
├── next.config.js       # Next.js 配置
├── tailwind.config.ts   # Tailwind 配置
└── package.json
```

## 数据存储

- 学习进度保存在浏览器 LocalStorage 中
- 证书数据也存储在本地
- 清除浏览器数据会丢失进度

## 浏览器兼容性

- Chrome 90+
- Firefox 90+
- Safari 14+
- Edge 90+

## 许可证

MIT License

## 致谢

- [Next.js](https://nextjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Monaco Editor](https://microsoft.github.io/monaco-editor/)
- [Apache Flink](https://flink.apache.org/)
