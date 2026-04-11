# 视频教程脚本：第一次贡献

> 时长: 15-20 分钟 | 目标受众: 新贡献者

---

## 开场 (1 分钟)

### 画面

- 项目 Logo 和标题
- 主持人出镜

### 脚本

```
大家好！欢迎观看 AnalysisDataFlow 项目贡献指南系列教程。

我是本期的讲解员。今天，我将带你完成第一次贡献，
从 Fork 项目到提交 Pull Request，一步一步，零基础也能学会。

无论你是想修正一个拼写错误，还是想添加新的内容，
这个视频都能帮助你快速上手。

让我们开始吧！
```

---

## 第一部分：项目概览 (2 分钟)

### 画面

- 项目仓库首页
- 目录结构展示

### 脚本

```
首先，让我们快速了解一下 AnalysisDataFlow 项目。

这是一个关于流计算的综合知识库，涵盖三个主要领域：

第一，Struct 目录，包含形式理论和严格证明；
第二，Knowledge 目录，包含设计模式和最佳实践；
第三，Flink 目录，专注于 Apache Flink 的架构和机制。

项目的一个特色是严格的形式化体系。
每个核心概念都有编号定义和定理证明。

比如这个 Watermark 的定义，有唯一的编号 Def-F-03-01。
这种编号系统确保了整个知识库的严谨性和可追溯性。
```

### 屏幕操作

```
1. 展示 GitHub 仓库首页
2. 逐个展示 Struct/、Knowledge/、Flink/ 目录
3. 打开一个文档，展示定理编号示例
```

---

## 第二部分：准备工作 (3 分钟)

### 画面

- Git 安装页面
- VS Code 界面
- Node.js 下载页面

### 脚本

```
在开始之前，我们需要准备以下工具：

第一，Git，用于版本控制；
第二，VS Code，作为我们的编辑器；
第三，Node.js，用于运行本地验证工具。

对于 VS Code，我推荐安装这几个扩展：
Markdown All in One 提供 Markdown 编辑支持；
Markdown Preview Mermaid Support 可以预览 Mermaid 图表；
markdownlint 帮助我们检查 Markdown 语法。

安装完成后，我们还需要安装一些命令行工具。
打开终端，运行以下命令：

npm install -g markdownlint-cli
npm install -g markdown-link-check

这些工具可以帮助我们在提交前检查文档质量。
```

### 屏幕操作

```
1. 展示 Git 官网下载页面
2. 展示 VS Code 扩展安装
3. 终端中运行 npm install 命令
```

---

## 第三部分：Fork 和克隆 (3 分钟)

### 画面

- GitHub Fork 界面
- 终端操作

### 脚本

```
现在让我们 Fork 项目。

Fork 就是在你的账号下创建一个项目的副本，
你可以自由修改，不会影响原项目。

点击右上角的 Fork 按钮，等待几秒钟，
你的 Fork 就创建好了。

接下来，我们需要将项目克隆到本地。
在你的 Fork 页面，点击 Code 按钮，复制 HTTPS 地址。

然后打开终端，运行：
git clone https://github.com/YOUR_USERNAME/AnalysisDataFlow.git

进入项目目录：
cd AnalysisDataFlow

为了保持与原项目的同步，我们需要添加上游仓库：
git remote add upstream https://github.com/your-org/AnalysisDataFlow.git

git fetch upstream

现在，你的本地仓库就配置好了。
```

### 屏幕操作

```
1. 点击 Fork 按钮
2. 等待 Fork 完成
3. 复制仓库地址
4. 终端中运行 git clone
5. 运行 git remote add upstream
```

---

## 第四部分：创建分支 (2 分钟)

### 画面

- 终端操作
- 分支命名说明

### 脚本

```
在修改之前，我们需要创建一个新的分支。

分支就像一个独立的工作空间，
你的修改不会影响主分支。

首先，同步主分支的最新代码：
git checkout main
git pull upstream main

然后创建功能分支：
git checkout -b docs/fix-typo-in-watermark

分支命名遵循这样的规范：
类型前缀，如 docs、fix、feat；
然后是斜杠；
最后是简短的描述。

常用前缀有：
docs 用于文档改进；
fix 用于修复错误；
feat 用于新功能。

好的分支命名可以让其他人快速了解你的工作内容。
```

### 屏幕操作

```
1. 终端中运行 git checkout main
2. 运行 git pull upstream main
3. 运行 git checkout -b
4. 展示分支命名规范的表格
```

---

## 第五部分：进行修改 (3 分钟)

### 画面

- VS Code 编辑界面
- 文档修改示例

### 脚本

```
现在让我们进行实际的修改。

假设我们在 Watermark 文档中发现了一个拼写错误，
"checkpoint" 被写成了 "chekcpoint"。

在 VS Code 中打开文件，找到错误位置，
进行修改。

保存文件后，我们可以使用 markdownlint 检查语法：
npx markdownlint-cli Flink/1.1-watermark-mechanism.md

如果没有错误，说明语法是正确的。

接下来检查链接：
npx markdown-link-check Flink/1.1-watermark-mechanism.md

如果所有链接都是有效的，就可以提交了。
```

### 屏幕操作

```
1. VS Code 中打开文件
2. 定位并修改拼写错误
3. 保存文件
4. 终端运行 markdownlint
5. 终端运行 markdown-link-check
```

---

## 第六部分：提交更改 (3 分钟)

### 画面

- 终端 git 操作
- Commit 信息说明

### 脚本

```
修改完成后，我们需要提交更改。

首先，查看修改的文件：
git status

然后，将文件添加到暂存区：
git add Flink/1.1-watermark-mechanism.md

接下来，提交更改：
git commit -m "fix(flink): 修正 Watermark 文档中的拼写错误

将 'chekcpoint' 修正为 'checkpoint'"

提交信息遵循规范格式：
类型、范围、主题，然后是详细描述。

类型可以是：
feat 表示新功能；
fix 表示修复；
docs 表示文档；
refactor 表示重构。

一个好的提交信息应该：
主题简洁明了，不超过 50 个字符；
详细说明变更原因和内容；
如果有相关的 Issue，可以在最后引用。
```

### 屏幕操作

```
1. 运行 git status
2. 运行 git add
3. 运行 git commit
4. 展示提交信息规范的示例
```

---

## 第七部分：推送和创建 PR (3 分钟)

### 画面

- git push 操作
- GitHub PR 界面

### 脚本

```
提交完成后，将更改推送到你的 Fork：
git push origin docs/fix-typo-in-watermark

然后，访问你的 Fork 页面，
GitHub 会显示一个提示，询问是否创建 Pull Request。

点击 "Compare & pull request" 按钮。

在 PR 页面，填写标题和描述：
标题应该简洁描述变更；
描述中可以详细说明修改内容；
选择相关的 Issue（如果有）。

检查清单可以帮助你确认：
- 拼写错误已修正
- Markdown 语法检查通过
- 本地验证通过

最后，点击 "Create pull request"。

恭喜！你的第一个 Pull Request 已经提交了！
```

### 屏幕操作

```
1. 运行 git push
2. 刷新 GitHub 页面
3. 点击 Compare & pull request
4. 填写 PR 标题和描述
5. 勾选检查清单
6. 点击 Create pull request
```

---

## 结尾 (1 分钟)

### 画面

- 项目 Logo
- 资源链接
- 主持人出镜

### 脚本

```
恭喜你完成了第一次贡献！

回顾我们今天学到的：
- 了解了项目的结构和特色
- 配置了开发环境
- Fork 并克隆了项目
- 创建了功能分支
- 进行了修改和本地验证
- 提交了更改并创建了 PR

更多学习资源：
- 完整贡献指南：CONTRIBUTING.md
- 写作风格指南：docs/contributing/writing-guide.md
- 审核清单：docs/contributing/review-checklist.md

在下一个视频中，我们将学习如何编写形式化定理。

感谢观看，期待你的贡献！
```

---

## 补充说明

### 录制提示

1. **屏幕分辨率**：建议 1920x1080 或更高
2. **字体大小**：确保代码和文字清晰可见
3. **鼠标高亮**：使用鼠标高亮工具突出重点
4. **语速控制**：保持适中语速，关键步骤放慢

### 剪辑建议

1. **开头**：添加项目 Logo 动画
2. **过渡**：使用简洁的转场效果
3. **重点**：对关键操作添加文字提示
4. **结尾**：显示资源链接卡片

### 字幕文件

建议在录制后添加中文字幕，方便观看。
