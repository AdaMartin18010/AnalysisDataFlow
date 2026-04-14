---
title: "Streaming Data Security & Compliance Quick Reference Card"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Streaming Data Security & Compliance Quick Reference Card

> **Quick Reference**: Compliance framework mapping, security configuration checklists, privacy protection technology decisions
>
> **Full Document**: [streaming-security-compliance.md](../08-standards/streaming-security-compliance.md)

---

## 🏛️ Compliance Framework Mapping Quick Reference

### GDPR/SOC2/PCI-DSS Requirement Comparison

| Regulatory Requirement | Technical Control | Verification Method | Stream Data Implementation Example |
|------------------------|-------------------|---------------------|-----------------------------------|
| **GDPR Art.32** Secure Processing | Encryption, Access Control, Anonymization | Technical Audit | Field-level encryption + ABAC |
| **GDPR Art.17** Right to Erasure | Data marking deletion, TTL | Deletion Verification | Kafka Log Compaction |
| **SOC2 CC6.1** Logical Access | MFA, Least Privilege | Access Review | RBAC + Periodic Re-review |
| **SOC2 CC6.6** Encryption in Transit | TLS 1.2+, Certificate Management | Config Scan | End-to-end mTLS |
| **PCI-DSS Req 3** Storage Protection | AES-256, Tokenization | QSA Audit | PAN encryption + Tokenization |
| **PCI-DSS Req 4** Transmission Protection | TLS 1.2+, Disable Weak Protocols | Vulnerability Scan | Disable SSLv3/TLS1.0 |
| **HIPAA §164.312** Technical Safeguards | Audit Controls, Integrity | Compliance Assessment | Immutable Audit Logs |

### Compliance Checklist Matrix

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Streaming Data Compliance Control Matrix             │
├─────────────────┬───────────────────────────────────────────────────────┤
│ Regulation      │ Key Control Points                                    │
├─────────────────┼───────────────────────────────────────────────────────┤
│                 │ □ Personal data pseudonymization (field-level encryption)│
│  GDPR           │ □ Processing system confidentiality (TLS 1.3 + mTLS)  │
│                 │ □ Processing system integrity (audit logs + hash chain)│
│                 │ □ Data subject rights support (deletion, export)      │
├─────────────────┼───────────────────────────────────────────────────────┤
│                 │ □ Logical access control (RBAC/ABAC)                  │
│  SOC2 Type II   │ □ Multi-factor authentication (MFA)                   │
│                 │ □ Encryption in transit (TLS 1.2+)                    │
│                 │ □ Audit log integrity                                 │
├─────────────────┼───────────────────────────────────────────────────────┤
│                 │ □ Cardholder data encryption (AES-256)                │
│  PCI-DSS        │ □ Transmission encryption (TLS 1.2+)                  │
│                 │ □ Access control (Need-to-know)                       │
│                 │ □ Network security (Firewall/IDS)                     │
├─────────────────┼───────────────────────────────────────────────────────┤
│                 │ □ Access control (Unique User ID)                     │
│  HIPAA          │ □ Audit controls (immutable logs)                     │
│                 │ □ Integrity controls (digital signatures)             │
│                 │ □ Transmission security (encrypted transport)         │
└─────────────────┴───────────────────────────────────────────────────────┘
```

---

## 🔒 Security Configuration Checklist

### Kafka Security Checklist

```bash
# □ 1. Enable SSL/TLS transport encryption
listeners=SASL_SSL://:9093
security.inter.broker.protocol=SASL_SSL
ssl.enabled.protocols=TLSv1.3

# □ 2. Configure client certificate authentication
ssl.client.auth=required

# □ 3. Enable strong cipher suites
ssl.cipher.suites=TLS_AES_256_GCM_SHA384,TLS_CHACHA20_POLY1305_SHA256

# □ 4. Configure SASL authentication
sasl.enabled.mechanisms=GSSAPI,PLAIN,SCRAM-SHA-512

# □ 5. Set ACLs
# Producer permissions
kafka-acls --add --allow-principal User:service \
  --producer --topic orders

# Consumer permissions
kafka-acls --add --allow-principal User:consumer \
  --consumer --topic orders --group analytics

# □ 6. Enable audit logs
log4j.logger.kafka.authorizer.logger=INFO, authorizerAppender
```

### Flink Security Checklist

```yaml
# flink-conf.yaml

# □ 1. Enable internal SSL
security.ssl.internal.enabled: true
security.ssl.rest.enabled: true

# □ 2. Configure keystore
security.ssl.internal.keystore: /path/to/internal.keystore
security.ssl.internal.keystore-password: ${KEYSTORE_PASSWORD}
security.ssl.internal.truststore: /path/to/internal.truststore

# □ 3. Enable strong cipher suites
security.ssl.algorithms: TLS_AES_256_GCM_SHA384,TLS_CHACHA20_POLY1305_SHA256
security.ssl.protocol: TLSv1.3

# □ 4. Enable Kerberos authentication
security.kerberos.login.use-ticket-cache: false
security.kerberos.login.keytab: /etc/security/keytabs/flink.keytab
security.kerberos.login.principal: flink@EXAMPLE.COM

# □ 5. Enable hostname verification
security.ssl.rest.verify-hostname: true

# □ 6. Configure ZooKeeper security
high-availability.zookeeper.client.acl: creator
```

### Data Encryption Layer Checklist

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Stream Encryption Layer Architecture│
├──────────────┬───────────────────┬──────────────────────────┤
│    Layer     │     Technology    │         Checklist        │
├──────────────┼───────────────────┼──────────────────────────┤
│ Transport (L4)│ TLS 1.3 / mTLS   │ □ Disable TLS 1.0/1.1   │
│              │                   │ □ Enable PFS             │
│              │                   │ □ Certificate expiry monitoring│
├──────────────┼───────────────────┼──────────────────────────┤
│ Message (L7) │ SASL_SSL          │ □ Strong cipher algorithms│
│              │                   │ □ Mutual authentication  │
├──────────────┼───────────────────┼──────────────────────────┤
│ Application  │ AES-256-GCM       │ □ Key rotation           │
│              │                   │ □ HSM protection         │
├──────────────┼───────────────────┼──────────────────────────┤
│ Storage (Disk)│ LUKS / BitLocker │ □ Full disk encryption   │
│              │                   │ □ Key escrow             │
├──────────────┼───────────────────┼──────────────────────────┤
│ Backup (Bak) │ Client-side encryption│ □ Offsite encrypted storage│
│              │                   │ □ Access logs            │
└──────────────┴───────────────────┴──────────────────────────┘
```

---

## 🛡️ Privacy Protection Technology Selection Decision Tree

### Data Sensitivity Assessment

```
┌─────────────────────────────────────────────────────────────────┐
│                    Privacy Protection Technology Decision Tree   │
└─────────────────────────────────────────────────────────────────┘

Data Classification Assessment
│
├── Public Data ──────────────────────────────► No protection needed
│   └─ Example: Product catalog, public news
│
├── Internal Data ────────────────────────────► Transport encryption (TLS)
│   └─ Example: Internal logs, non-sensitive metrics
│
├── Confidential Data ────────────────────────► End-to-end encryption
│   │
│   ├── Need retrieval? ──YES──► Format-Preserving Encryption (FPE)
│   │   └─ Example: Query by last 4 digits of phone number
│   │
│   ├── Need analytics? ──YES──► Differential Privacy / Secure Multi-Party Computation
│   │   └─ Example: Aggregate statistics, federated learning
│   │
│   └── Others ───────────► Application-layer AES-256 encryption
│       └─ Example: Personally Identifiable Information (PII)
│
└── Highly Sensitive ─────────────────────────► Application-layer encryption + TEE
    │
    ├── Compliance: PCI-DSS ──► Tokenization + HSM
    │
    ├── Compliance: GDPR ─────► Field-level encryption + Key separation
    │
    ├── Compliance: National crypto ──► SM4/SM2 + Domestic algorithms
    │
    └── General ──────────────► ChaCha20-Poly1305 (high performance)

Key Management Strategy
│
├── □ HSM protection (FIPS 140-2 Level 3+)
├── □ Regular rotation (90-day cycle)
└── □ Access audit (who/when/which key accessed)
```

### De-identification Strategy Selection

| Data Type | Static Masking | Dynamic Masking | FPE | k-Anonymity |
|-----------|----------------|-----------------|-----|-------------|
| **Phone Number** | ***-***-1234 | Permission-based display | ✅ | - |
| **Email** | j***@example.com | Permission-based display | ✅ | - |
| **ID Number** | ***********1234 | Partial display | ✅ | ✅ |
| **Credit Card** | ****-****-****-1234 | Show last 4 digits only | ✅ | - |
| **Name** | Zhang** | Permission-based display | - | ✅ |
| **Location** | Region-level blur | Precision downgrade | - | ✅ |

### Privacy Protection Technology Comparison

| Technology | Protection Level | Performance Impact | Applicable Scenario |
|------------|------------------|--------------------|---------------------|
| **TLS 1.3** | Transport Security | +0.5ms | All communications |
| **mTLS** | Mutual Authentication | +1.2ms | Service-to-service communication |
| **AES-256-GCM** | Application Encryption | +0.8ms | Field-level encryption |
| **FPE** | Format-Preserving | +1ms | Searchable PII |
| **k-Anonymity** | Identity Hiding | Medium | Data publishing |
| **Differential Privacy** | Statistical Security | High | Aggregate queries |
| **TEE** | Memory Security | High | Key processing |

---

## 📝 Audit Log Specification

### Audit Entry Structure

```java
public class AuditEntry {
    private long timestamp;        // T: Timestamp (milliseconds)
    private String action;         // A: READ/WRITE/DELETE/ADMIN
    private String userId;         // U: Subject
    private String resource;       // R: Topic/Table/Schema
    private String operation;      // O: Operation details
    private String result;         // Rst: Success/Failure/Denied
    private String previousHash;   // Previous entry hash
    private String currentHash;    // Current entry hash
}
```

### Mandatory Logging Operations

| Operation Type | Required Fields | Retention Period |
|----------------|-----------------|------------------|
| **Data Access** | User, Time, Resource, Query Conditions | 7 years |
| **Permission Change** | Changer, Changed, Old Value, New Value | Permanent |
| **Key Operation** | Operation Type, Key ID, Executor | Permanent |
| **Config Change** | Change Content, Changer, Time | 3 years |
| **Abnormal Access** | Denial Reason, Attempt Count, Source IP | 2 years |

---

## 🔐 Access Control Quick Reference

### RBAC vs ABAC Selection

| Dimension | RBAC | ABAC |
|-----------|------|------|
| **Granularity** | Role-level | Fine-grained (field/row-level) |
| **Applicable Scenario** | Stable organizational structure | Dynamic/complex environments |
| **Stream Data Applicability** | Topic-level ACL | Row-level security, PII control |
| **Performance** | High (table lookup) | Medium (policy evaluation) |
| **Complexity** | Low | High |

### Stream Data Access Control Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Access Control Layer Architecture         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 4: Compliance Governance Layer                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Compliance Policy Engine (GDPR/CCPA/PCI-DSS)       │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │ Policy Distribution                 │
│  Layer 3: Data Protection Layer ▼                          │
│  ┌─────────────┐  ┌─────────────┐  ┌───────────────────┐   │
│  │ Encryption  │  │ Masking     │  │ Privacy Computing │   │
│  │ (Transport/ │  │ (Dynamic    │  │ (DP/MPC/TEE)      │   │
│  │  Static)    │  │  Masking)   │  │                   │   │
│  └──────┬──────┘  └──────┬──────┘  └─────────┬─────────┘   │
│         │                │                    │              │
│  Layer 2: Access Control Layer │                    │              │
│  ┌─────────────┐  ┌──────▼──────┐  ┌──────────▼──────────┐  │
│  │ Identity    │  │ RBAC        │  │ ABAC                │  │
│  │ Management  │──│ Role-based  │──│ Attribute-based     │  │
│  │ (IAM/IdP)   │  │ Permissions │  │ Permissions         │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                    │              │
│         └────────────────┴────────────────────┘              │
│                          │ ACL/Policy                        │
│  Layer 1: Resource Layer  ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Kafka Topic  │  Flink Table  │  Schema Registry    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Configuration Templates

### Flink Row-Level Security Policy

```java
// Create table with row-level security
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

// Create row-level security view
tEnv.executeSql("""
    CREATE VIEW user_events_secure AS
    SELECT * FROM user_events
    WHERE
        -- Users can only view data from their own region
        region = CURRENT_USER_REGION()
        -- Or user has global view permission
        OR HAS_ROLE('data_admin')
""")
```

### PII Dynamic Masking UDF

```java
public class PiiMaskFunction extends ScalarFunction {

    public static final int LEVEL_FULL = 0;      // Full masking
    public static final int LEVEL_PARTIAL = 1;   // Partial masking
    public static final int LEVEL_MASKED = 2;    // Format-preserving
    public static final int LEVEL_RAW = 3;       // Raw data

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

## 📚 Further Reading

| Document | Content |
|----------|---------|
| [streaming-security-compliance.md](../08-standards/streaming-security-compliance.md) | Complete security and compliance guide |
| [streaming-data-governance.md](../08-standards/streaming-data-governance.md) | Data governance specifications |
| [streaming-access-control.md](../06-frontier/streaming-access-control.md) | Detailed access control design |
| [02.08-differential-privacy-streaming.md](../../Struct/02-properties/02.08-differential-privacy-streaming.md) | Differential privacy formal analysis |

---

*Quick Reference Card v1.0 | Last Updated: 2026-04-03*
