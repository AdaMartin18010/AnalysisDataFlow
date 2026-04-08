# Flink可运行示例集合

本项目将AnalysisDataFlow文档中的Flink代码示例改造为完全可运行的项目，包含Java、Python和Docker Compose环境。

## 📁 项目结构

```
examples/
├── java/
│   ├── wordcount/      # WordCount - DataStream API入门
│   ├── windowing/      # 窗口操作 - 滚动/滑动/会话窗口
│   └── stateful/       # 状态管理 - Value/List/MapState
├── python/
│   ├── wordcount/      # Python WordCount
│   └── table-api/      # Table API & SQL
├── docker/
│   └── docker-compose.yml  # 一键启动Flink集群
└── README.md           # 本文件
```

## 🚀 快速开始

### 方式1: Docker Compose（推荐）

```bash
cd examples/docker
docker-compose up -d

# 访问Flink Web UI
open http://localhost:8081
```

### 方式2: 本地运行Java示例

```bash
# 进入项目目录
cd examples/java/wordcount

# 编译并运行
mvn clean compile exec:java -Dexec.mainClass="com.example.flink.WordCount" -Plocal
```

### 方式3: 本地运行Python示例

```bash
# 安装依赖
cd examples/python/wordcount
pip install -r requirements.txt

# 运行
python wordcount.py
```

## 📊 示例概览

| 示例 | 类型 | 核心概念 | 状态 |
|-----|------|---------|------|
| WordCount (Java) | DataStream | flatMap, keyBy, window, sum | ✅ 可运行 |
| Windowing (Java) | DataStream | Tumbling/Sliding/Session窗口 | ✅ 可运行 |
| Stateful (Java) | DataStream | Value/List/MapState | ✅ 可运行 |
| WordCount (Python) | DataStream | PyFlink基础 | ✅ 可运行 |
| Table API (Python) | Table/SQL | SQL查询、窗口聚合 | ✅ 可运行 |
| Docker Compose | 环境 | 完整Flink集群 | ✅ 可运行 |

## 🔧 环境要求

### Java示例
- JDK 11+
- Apache Maven 3.6+
- (可选) Flink 1.20+

### Python示例
- Python 3.8+
- Java 11+ (Flink依赖)
- pip

### Docker环境
- Docker 20.10+
- Docker Compose 2.0+

## 📖 详细文档

每个示例目录下都有独立的README.md：

- [Java WordCount](./java/wordcount/README.md)
- [Java Windowing](./java/windowing/README.md)
- [Java Stateful](./java/stateful/README.md)
- [Python WordCount](./python/wordcount/README.md)
- [Python Table API](./python/table-api/README.md)
- [Docker环境](./docker/README.md)

## 🧪 CI测试

所有示例都配置了GitHub Actions CI流程：

```yaml
# 触发条件
- Push到main分支
- Pull Request
- 每日定时任务

# 测试内容
- Java项目编译和打包
- Python语法检查
- Docker Compose验证
- 代码质量检查
```

查看CI配置: [`.github/workflows/examples-ci.yml`](../.github/workflows/examples-ci.yml)

## 📝 验证清单

运行以下命令验证所有示例：

```bash
# 验证脚本
./scripts/verify-examples.sh
```

或手动验证：

```bash
# 1. 验证目录结构
ls -la examples/java/
ls -la examples/python/
ls -la examples/docker/

# 2. 验证Java项目
for dir in wordcount windowing stateful; do
    echo "验证: examples/java/$dir"
    cd examples/java/$dir && mvn validate && cd ../../..
done

# 3. 验证Python项目
for dir in wordcount table-api; do
    echo "验证: examples/python/$dir"
    cd examples/python/$dir && python -m py_compile *.py && cd ../../..
done

# 4. 验证Docker配置
cd examples/docker && docker-compose config
cd ../..
```

## 🔄 与文档的关联

这些可运行示例与项目文档中的代码片段对应：

| 文档 | 对应示例 |
|-----|---------|
| `Flink/01.*-datastream-api.md` | `examples/java/wordcount/` |
| `Flink/03.*-windowing.md` | `examples/java/windowing/` |
| `Flink/04.*-state-management.md` | `examples/java/stateful/` |
| `Flink/05.*-table-api.md` | `examples/python/table-api/` |

## 🤝 贡献指南

添加新示例时，请确保：

1. ✅ 完整的README.md说明
2. ✅ 可独立运行的构建配置
3. ✅ 通过CI验证
4. ✅ 与文档中的代码片段保持一致

## 📜 许可证

与主项目相同，遵循项目根目录的LICENSE文件。
