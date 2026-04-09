# 案例研究贡献指南

## 如何贡献新案例

### 1. 选择行业

从以下行业中选择：

- 金融、电商、物流
- 医疗、制造、能源
- 互联网、媒体、教育

### 2. 准备内容

参考 Case-Study-Template.md 准备：

- 执行摘要
- 业务背景
- 技术架构
- 效果指标

### 3. 提交案例

```bash
# Fork 项目
git clone https://github.com/your-fork/AnalysisDataFlow.git

# 创建分支
git checkout -b case-study/your-case

# 添加文件
cp your-case.md phase2-case-studies/industry/

# 提交
git add .
git commit -m "Add case study: your-case"
git push origin case-study/your-case
```

### 4. 创建 PR

在 GitHub 上创建 Pull Request

## 案例审查标准

- [ ] 内容真实可信
- [ ] 技术方案清晰
- [ ] 效果指标量化
- [ ] 格式符合模板

---

*Case Study Contribution Guide*
