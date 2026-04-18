# 流数据安全与合规快速参考卡片

> **快速查阅**: 合规框架映射、安全配置检查清单、隐私保护技术决策
>
> **完整文档**: [streaming-security-compliance.md](../08-standards/streaming-security-compliance.md)

---

## 🏛️ 合规框架映射速查

### GDPR/SOC2/PCI-DSS 要求对照

| 法规要求 | 技术控制 | 验证方法 | 流数据实现示例 |
|----------|----------|----------|----------------|
| **GDPR Art.32** 安全处理 | 加密、访问控制、匿名化 | 技术审计 | 字段级加密 + ABAC |
| **GDPR Art.17** 删除权 | 数据标记删除、TTL | 删除验证 | Kafka Log Compaction |
| **SOC2 CC6.1** 逻辑访问 | MFA、最小权限 | 访问评审 | RBAC + 定期复核 |
| **SOC2 CC6.6** 加密传输 | TLS 1.2+、证书管理 | 配置扫描 | mTLS全链路 |
| **PCI-DSS Req 3** 存储保护 | AES-256、Tokenization | QSA审计 | PAN加密 + 令牌化 |
| **PCI-DSS Req 4** 传输保护 | TLS 1.2+、禁用弱协议 | 漏洞扫描 | 禁用SSLv3/TLS1.0 |
| **HIPAA §164.312** 技术保障 | 审计控制、完整性 | 合规评估 | 不可变审计日志 |

### 合规检查清单矩阵

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    流数据合规控制矩阵                                    │
├─────────────────┬───────────────────────────────────────────────────────┤
│ 法规            │ 关键控制点                                             │
├─────────────────┼───────────────────────────────────────────────────────┤
│                 │ □ 个人数据假名化 (字段级加密)                          │
│  GDPR           │ □ 处理系统保密性 (TLS 1.3 + mTLS)                      │
│                 │ □ 处理系统完整性 (审计日志 + 哈希链)                   │
│                 │ □ 数据主体权利支持 (删除、导出)                        │
├─────────────────┼───────────────────────────────────────────────────────┤
│                 │ □ 逻辑访问控制 (RBAC/ABAC)                             │
│  SOC2 Type II   │ □ 多因素认证 (MFA)                                     │
│                 │ □ 加密传输 (TLS 1.2+)                                  │
│                 │ □ 审计日志完整性                                       │
├─────────────────┼───────────────────────────────────────────────────────┤
│                 │ □ 持卡人数据加密 (AES-256)                             │
│  PCI-DSS        │ □ 传输加密 (TLS 1.2+)                                  │
│                 │ □ 访问控制 (Need-to-know)                              │
│                 │ □ 网络安全 (防火墙/IDS)                                │
├─────────────────┼───────────────────────────────────────────────────────┤
│                 │ □ 访问控制 (Unique User ID)                            │
│  HIPAA          │ □ 审计控制 (不可变日志)                                │
│                 │ □ 完整性控制 (数字签名)                                │
│                 │ □ 传输安全 (加密传输)                                  │
└─────────────────┴───────────────────────────────────────────────────────┘
```

---

## 🔒 安全配置检查清单

### Kafka安全清单

```bash
# □ 1. 启用SSL/TLS传输加密 listeners=SASL_SSL://:9093
security.inter.broker.protocol=SASL_SSL
ssl.enabled.protocols=TLSv1.3

# □ 2. 配置客户端证书认证 ssl.client.auth=required

# □ 3. 启用强密码套件 ssl.cipher.suites=TLS_AES_256_GCM_SHA384,TLS_CHACHA20_POLY1305_SHA256

# □ 4. 配置SASL认证 sasl.enabled.mechanisms=GSSAPI,PLAIN,SCRAM-SHA-512

# □ 5. 设置ACL
# 生产者权限 kafka-acls --add --allow-principal User:service \
  --producer --topic orders

# 消费者权限 kafka-acls --add --allow-principal User:consumer \
  --consumer --topic orders --group analytics

# □ 6. 启用审计日志 log4j.logger.kafka.authorizer.logger=INFO, authorizerAppender
```

### Flink安全清单

```yaml
# flink-conf.yaml

# □ 1. 启用内部SSL security.ssl.internal.enabled: true
security.ssl.rest.enabled: true

# □ 2. 配置密钥库 security.ssl.internal.keystore: /path/to/internal.keystore
security.ssl.internal.keystore-password: ${KEYSTORE_PASSWORD}
security.ssl.internal.truststore: /path/to/internal.truststore

# □ 3. 启用强密码套件 security.ssl.algorithms: TLS_AES_256_GCM_SHA384,TLS_CHACHA20_POLY1305_SHA256
security.ssl.protocol: TLSv1.3

# □ 4. 启用Kerberos认证 security.kerberos.login.use-ticket-cache: false
security.kerberos.login.keytab: /etc/security/keytabs/flink.keytab
security.kerberos.login.principal: flink@EXAMPLE.COM

# □ 5. 启用主机名验证 security.ssl.rest.verify-hostname: true

# □ 6. 配置ZooKeeper安全 high-availability.zookeeper.client.acl: creator
```

### 数据加密层次清单

```
┌─────────────────────────────────────────────────────────────┐
│                    数据流加密层次架构                        │
├──────────────┬───────────────────┬──────────────────────────┤
│    层次       │     技术           │         检查项          │
├──────────────┼───────────────────┼──────────────────────────┤
│ 传输层 (L4)   │ TLS 1.3 / mTLS    │ □ 禁用TLS 1.0/1.1       │
│              │                   │ □ 启用前向保密 (PFS)     │
│              │                   │ □ 证书有效期监控         │
├──────────────┼───────────────────┼──────────────────────────┤
│ 消息层 (L7)   │ SASL_SSL          │ □ 强密码算法             │
│              │                   │ □ 双向认证               │
├──────────────┼───────────────────┼──────────────────────────┤
│ 应用层 (App)  │ AES-256-GCM       │ □ 密钥轮换               │
│              │                   │ □ HSM保护                │
├──────────────┼───────────────────┼──────────────────────────┤
│ 存储层 (Disk) │ LUKS / BitLocker  │ □ 全盘加密               │
│              │                   │ □ 密钥托管               │
├──────────────┼───────────────────┼──────────────────────────┤
│ 备份层 (Bak)  │ 客户端加密         │ □ 异地加密存储           │
│              │                   │ □ 访问日志               │
└──────────────┴───────────────────┴──────────────────────────┘
```

---

## 🛡️ 隐私保护技术选择决策树

### 数据敏感度评估

```
┌─────────────────────────────────────────────────────────────────┐
│                    隐私保护技术决策树                            │
└─────────────────────────────────────────────────────────────────┘

数据分类评估
│
├── 公开数据 ──────────────────────────────► 无需保护
│   └─ 例:产品目录、公开新闻
│
├── 内部数据 ──────────────────────────────► 传输加密 (TLS)
│   └─ 例:内部日志、非敏感指标
│
├── 机密数据 ──────────────────────────────► 端到端加密
│   │
│   ├── 需要检索? ──YES──► 格式保留加密 (FPE)
│   │   └─ 例:手机号后四位查询
│   │
│   ├── 需要分析? ──YES──► 差分隐私 / 安全多方计算
│   │   └─ 例:聚合统计、联邦学习
│   │
│   └── 其他 ────────────► 应用层AES-256加密
│       └─ 例:个人身份信息 (PII)
│
└── 高度敏感 ──────────────────────────────► 应用层加密 + TEE
    │
    ├── 合规要求: PCI-DSS ──► Tokenization + HSM
    │
    ├── 合规要求: GDPR ─────► 字段级加密 + 密钥分离
    │
    ├── 合规要求: 国密 ─────► SM4/SM2 + 国产算法
    │
    └── 通用 ───────────────► ChaCha20-Poly1305 (高性能)

密钥管理策略
│
├── □ HSM保护 (FIPS 140-2 Level 3+)
├── □ 定期轮换 (90天周期)
└── □ 访问审计 (谁/何时/访问了什么密钥)
```

### 脱敏策略选择

| 数据类型 | 静态脱敏 | 动态脱敏 | FPE | k-匿名 |
|----------|----------|----------|-----|--------|
| **手机号** | ***-***-1234 | 根据权限显示 | ✅ | - |
| **邮箱** | j***@example.com | 根据权限显示 | ✅ | - |
| **身份证号** | ***********1234 | 部分显示 | ✅ | ✅ |
| **信用卡** | ****-****-****-1234 | 仅显示后四位 | ✅ | - |
| **姓名** | 张** | 根据权限显示 | - | ✅ |
| **位置** | 区域级模糊 | 精度降级 | - | ✅ |

### 隐私保护技术对比

| 技术 | 保护级别 | 性能影响 | 适用场景 |
|------|----------|----------|----------|
| **TLS 1.3** | 传输安全 | +0.5ms | 所有通信 |
| **mTLS** | 双向认证 | +1.2ms | 服务间通信 |
| **AES-256-GCM** | 应用加密 | +0.8ms | 字段级加密 |
| **FPE** | 格式保留 | +1ms | 需要检索的PII |
| **k-匿名** | 身份隐藏 | 中 | 数据发布 |
| **差分隐私** | 统计安全 | 高 | 聚合查询 |
| **TEE** | 内存安全 | 高 | 密钥处理 |

---

## 📝 审计日志规范

### 审计条目结构

```java
public class AuditEntry {
    private long timestamp;        // T: 时间戳(毫秒)
    private String action;         // A: READ/WRITE/DELETE/ADMIN
    private String userId;         // U: 执行主体
    private String resource;       // R: Topic/Table/Schema
    private String operation;      // O: 操作详情
    private String result;         // Rst: Success/Failure/Denied
    private String previousHash;   // 前一个条目哈希
    private String currentHash;    // 当前条目哈希
}
```

### 必须记录的操作

| 操作类型 | 必须记录字段 | 保留期限 |
|----------|--------------|----------|
| **数据访问** | 用户、时间、资源、查询条件 | 7年 |
| **权限变更** | 变更者、被变更者、旧值、新值 | 永久 |
| **密钥操作** | 操作类型、密钥ID、执行者 | 永久 |
| **配置变更** | 变更内容、变更者、时间 | 3年 |
| **异常访问** | 拒绝原因、尝试次数、来源IP | 2年 |

---

## 🔐 访问控制速查

### RBAC vs ABAC 选择

| 维度 | RBAC | ABAC |
|------|------|------|
| **粒度** | 角色级 | 细粒度（字段/行级） |
| **适用场景** | 组织架构稳定 | 动态/复杂环境 |
| **流数据适用** | Topic级ACL | 行级安全、PII控制 |
| **性能** | 高（查表） | 中（策略评估） |
| **复杂度** | 低 | 高 |

### 流数据访问控制层次

```
┌─────────────────────────────────────────────────────────────┐
│                    访问控制层次架构                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 4: 合规治理层                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  合规策略引擎 (GDPR/CCPA/PCI-DSS)                   │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │ 策略下发                          │
│  Layer 3: 数据保护层     ▼                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────────────┐   │
│  │ 加密服务    │  │ 脱敏服务    │  │ 隐私计算          │   │
│  │ (传输/静态) │  │ (动态脱敏)  │  │ (DP/MPC/TEE)      │   │
│  └──────┬──────┘  └──────┬──────┘  └─────────┬─────────┘   │
│         │                │                    │              │
│  Layer 2: 访问控制层      │                    │              │
│  ┌─────────────┐  ┌──────▼──────┐  ┌──────────▼──────────┐  │
│  │ 身份管理    │  │ RBAC        │  │ ABAC                │  │
│  │ (IAM/IdP)   │──│ 角色权限    │──│ 属性权限            │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                    │              │
│         └────────────────┴────────────────────┘              │
│                          │ ACL/Policy                        │
│  Layer 1: 资源层          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Kafka Topic  │  Flink Table  │  Schema Registry    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速配置模板

### Flink行级安全策略

```java
// 创建带行级安全的表
tEnv.executeSql("""
    CREATE TABLE user_events (
        user_id STRING,
        event_type STRING,
        region STRING,
        payload STRING,
        acl_mask STRING METADATA FROM 'acl_mask'
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'user-events',
        'properties.security.protocol' = 'SASL_SSL',
        'properties.sasl.mechanism' = 'GSSAPI',
        'format' = 'json'
    )
""")

// 创建行级安全视图
tEnv.executeSql("""
    CREATE VIEW user_events_secure AS
    SELECT * FROM user_events
    WHERE
        -- 用户只能查看自己所在区域的数据
        region = CURRENT_USER_REGION()
        -- 或用户有全局查看权限
        OR HAS_ROLE('data_admin')
""")
```

### PII动态脱敏UDF

```java
public class PiiMaskFunction extends ScalarFunction {

    public static final int LEVEL_FULL = 0;      // 完全脱敏
    public static final int LEVEL_PARTIAL = 1;   // 部分脱敏
    public static final int LEVEL_MASKED = 2;    // 格式保留
    public static final int LEVEL_RAW = 3;       // 原始数据

    public String eval(String value, String piiType, int accessLevel) {
        if (value == null || accessLevel >= LEVEL_RAW) {
            return value;
        }

        return switch (piiType.toUpperCase()) {
            case "EMAIL" -> maskEmail(value, accessLevel);
            case "PHONE" -> maskPhone(value, accessLevel);
            case "CREDIT_CARD" -> maskCreditCard(value, accessLevel);
            default -> maskGeneric(value, accessLevel);
        };
    }

    private String maskEmail(String email, int level) {
        if (level <= LEVEL_FULL) return "***@***.com";
        int atIndex = email.indexOf('@');
        return email.substring(0, 2) + "***" + email.substring(atIndex);
    }

    private String maskPhone(String phone, int level) {
        String digits = phone.replaceAll("\\D", "");
        if (level <= LEVEL_FULL) return "***-***-****";
        return "***-***-" + digits.substring(digits.length() - 4);
    }

    private String maskCreditCard(String cc, int level) {
        String digits = cc.replaceAll("\\D", "");
        return digits.substring(0, 6) + "-****-****-" +
               digits.substring(digits.length() - 4);
    }
}
```

---

## 📚 延伸阅读

| 文档 | 内容 |
|------|------|
| [streaming-security-compliance.md](../08-standards/streaming-security-compliance.md) | 完整安全与合规指南 |
| [streaming-data-governance.md](../08-standards/streaming-data-governance.md) | 数据治理规范 |
| [streaming-access-control.md](../06-frontier/streaming-access-control.md) | 访问控制详细设计 |
| [02.08-differential-privacy-streaming.md](../../Struct/02-properties/02.08-differential-privacy-streaming.md) | 差分隐私形式化分析 |

---

*快速参考卡片 v1.0 | 最后更新: 2026-04-03*
