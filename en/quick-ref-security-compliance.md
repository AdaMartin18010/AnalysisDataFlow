# Streaming Security & Compliance Quick Reference

> **Language**: English | **Source**: [Knowledge/98-exercises/quick-ref-security-compliance.md](../Knowledge/98-exercises/quick-ref-security-compliance.md) | **Last Updated**: 2026-04-21

---

## Regulatory Framework Mapping

### GDPR / SOC2 / PCI-DSS Requirements

| Regulation | Technical Control | Verification | Streaming Example |
|------------|-------------------|--------------|-------------------|
| **GDPR Art.32** Secure processing | Encryption, access control, anonymization | Technical audit | Field-level encryption + ABAC |
| **GDPR Art.17** Right to erasure | Data marking, TTL | Deletion verification | Kafka Log Compaction |
| **SOC2 CC6.1** Logical access | MFA, least privilege | Access review | RBAC + periodic recertification |
| **SOC2 CC6.6** Encrypted transmission | TLS 1.2+, certificate management | Config scan | End-to-end mTLS |
| **PCI-DSS Req 3** Storage protection | AES-256, tokenization | QSA audit | PAN encryption + tokenization |
| **PCI-DSS Req 4** Transmission protection | TLS 1.2+, disable weak protocols | Vulnerability scan | Disable SSLv3/TLS1.0 |
| **HIPAA §164.312** Technical safeguards | Audit controls, integrity | Compliance assessment | Immutable audit logs |

### Compliance Checklist Matrix

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Streaming Data Compliance Control Matrix              │
├─────────────────┬───────────────────────────────────────────────────────┤
│ Regulation      │ Key Control Points                                    │
├─────────────────┼───────────────────────────────────────────────────────┤
│                 │ □ Pseudonymization (field-level encryption)           │
│  GDPR           │ □ Processing confidentiality (TLS 1.3 + mTLS)         │
│                 │ □ Processing integrity (audit logs + hash chain)      │
│                 │ □ Data subject rights support (deletion, export)      │
├─────────────────┼───────────────────────────────────────────────────────┤
│                 │ □ Logical access control (RBAC/ABAC)                  │
│  SOC2 Type II   │ □ Multi-factor authentication (MFA)                   │
│                 │ □ Encrypted transmission (TLS 1.2+)                   │
│                 │ □ Audit log integrity                                 │
├─────────────────┼───────────────────────────────────────────────────────┤
│                 │ □ Cardholder data encryption (AES-256)                │
│  PCI-DSS        │ □ Transmission encryption (TLS 1.2+)                  │
│                 │ □ Access control (Need-to-know)                       │
│                 │ □ Network security (firewall/IDS)                     │
├─────────────────┼───────────────────────────────────────────────────────┤
│                 │ □ Access control (Unique User ID)                     │
│  HIPAA          │ □ Audit controls (immutable logs)                     │
│                 │ □ Integrity controls (digital signatures)             │
│                 □ Transmission security (encryption)                    │
└─────────────────┴───────────────────────────────────────────────────────┘
```

---

## Kafka Security Checklist

```bash
# □ 1. Enable SSL/TLS encryption listeners=SASL_SSL://:9093
# □ 2. Configure SASL authentication (SCRAM-SHA-512 or Kerberos)
# □ 3. Enable ACLs for topic-level authorization
# □ 4. Enable log.cleanup.policy=compact for GDPR deletion
# □ 5. Encrypt data at rest (EBS encryption or filesystem-level)
# □ 6. Enable audit logging (authorizer.log4j.logger)
# □ 7. Rotate TLS certificates before expiry
# □ 8. Disable plaintext listener in production
```

## Flink Security Checklist

| Layer | Control | Configuration |
|-------|---------|---------------|
| **Network** | mTLS between TaskManagers | `security.ssl.internal.enabled: true` |
| **Authentication** | Kerberos / OAuth2 | `security.kerberos.login.*` |
| **Authorization** | ACL on state backends | Custom `StateBackend` with ACL checks |
| **Audit** | Log all savepoint operations | `state.backend.incremental: true` + audit hook |
| **Encryption** | Encrypt checkpoints at rest | S3 SSE-KMS or HDFS encryption zones |

## Privacy-Preserving Techniques

| Technique | Use Case | Overhead |
|-----------|----------|----------|
| **Field-level encryption** | PII protection in transit & at rest | Low (AES-NI) |
| **Tokenization** | PCI-DSS PAN handling | Medium (token vault) |
| **Differential privacy** | Aggregate analytics without individual exposure | High (noise injection) |
| **K-anonymity** | De-identification before downstream processing | Medium (generalization) |

## References
