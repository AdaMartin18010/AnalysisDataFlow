# 链接健康检查器 v2.0

用于扫描 Markdown 文件中外部链接的健康状态检查工具。

## 功能特性

- 🔍 **全面扫描**: 递归扫描所有 Markdown 文件中的外部链接
- 🌐 **HTTP状态检查**: 检测 200/404/500/重定向/超时
- 📝 **Markdown报告**: 生成结构化的 Markdown 格式检查报告
- 🏷️ **状态分类**: 正常/警告/错误三级分类
- ⚡ **性能优化**: 
  - 并发请求控制（限制并发数）
  - 缓存机制避免重复检查
  - 支持断点续查
- ⚙️ **灵活配置**: 排除特定域名、设置超时时间、重试次数

## 快速开始

### 安装依赖

```bash
cd .scripts/link-checker
pip install -r requirements.txt
```

### 基本使用

```bash
# 检查当前目录下的所有 Markdown 文件
python link-checker.py

# 指定检查目录
python link-checker.py --path ../../

# 生成报告
python link-checker.py --path ../../ --output link-report.md
```

## 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--path` | `-p` | 要扫描的基础目录 | `.` |
| `--config` | `-c` | 配置文件路径 | `config.yaml` |
| `--output` | `-o` | Markdown 报告输出路径 | `link-check-report.md` |
| `--json` | `-j` | JSON 结果输出路径（可选） | - |
| `--timeout` | `-t` | 请求超时时间(秒) | `30` |
| `--retries` | `-r` | 重试次数 | `3` |
| `--concurrent` | - | 最大并发数 | `50` |
| `--exclude` | `-e` | 额外排除的域名模式 | - |
| `--no-resume` | - | 不从断点续查 | `False` |
| `--clear-cache` | - | 清除缓存后运行 | `False` |
| `--verbose` | `-v` | 启用详细日志 | `False` |

## 使用示例

### 生成 Markdown 和 JSON 两种报告

```bash
python link-checker.py \
  --path ../../ \
  --output link-report.md \
  --json link-results.json
```

### 排除特定域名

```bash
python link-checker.py \
  --path ../../ \
  --exclude "example\.com" "internal\.company\.com"
```

### 断点续查

检查过程中按 Ctrl+C 中断后，重新运行命令会自动从断点继续：

```bash
python link-checker.py --path ../../
# 中断...
python link-checker.py --path ../../  # 自动续查
```

如需重新开始：

```bash
python link-checker.py --path ../../ --no-resume
```

### 清除缓存

```bash
python link-checker.py --clear-cache --path ../../
```

## 报告输出

生成的 Markdown 报告包含以下部分：

1. **执行摘要**: 总体统计信息
2. **状态概览**: HTTP状态码分布
3. **错误链接**: 需要修复的链接列表
4. **警告链接**: 建议优化的链接（如重定向）
5. **按文件统计**: 每个文件的链接状态
6. **建议操作**: 优先级修复建议

## 配置文件

`config.yaml` 用于配置检查行为：

```yaml
# 排除列表 - 匹配的URL将跳过检查
exclude:
  - '^https?://localhost'
  - '^https?://127\.'
  - '^https?://example\.com'

# 超时设置
timeout:
  total: 30      # 总超时
  connect: 10    # 连接超时

# 重试策略
retry:
  max_retries: 3
  delay: 1

# 并发控制
max_concurrent: 50
max_per_host: 10

# 缓存设置
cache:
  enabled: true
  cache_dir: ".link-checker-cache"
  ttl: 24        # 缓存有效期(小时)

# 速率限制
rate_limit:
  domain_delay: 0.5
  domains:
    github.com:
      delay: 1.0
```

## 退出码

- `0`: 所有链接检查通过
- `1`: 发现失效链接

## 缓存机制

- 缓存文件存储在 `.link-checker-cache/` 目录
- 默认缓存有效期 24 小时
- 检查点文件支持断点续查

## 日志

检查过程中的详细日志写入 `link-checker.log` 文件。
