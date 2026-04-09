# 形式化验证指南

## 如何运行 TLA+ 证明

### 安装 TLC

```bash
# 下载 TLA+ Toolbox
wget https://github.com/tlaplus/tlaplus/releases/download/v1.7.1/TLAToolbox-1.7.1-linux.gtk.x86_64.zip

# 解压
unzip TLAToolbox-1.7.1-linux.gtk.x86_64.zip
```

### 验证证明

```bash
# 使用命令行
cd phase2-formal-proofs
tlc2 WatermarkMonotonicity.tla

# 或使用 Toolbox GUI
./toolbox
```

## 如何运行 Coq 证明

### 安装 Coq

```bash
# Ubuntu/Debian
sudo apt-get install coq

# macOS
brew install coq
```

### 编译证明

```bash
cd phase2-formal-proofs
coqc WatermarkAlgebra.v
```

## 常见问题

### Q: TLC 报错 "Module not found"

A: 检查文件名和模块名是否一致

### Q: Coq 编译失败

A: 检查依赖是否已编译

---

*Verification Guide*
