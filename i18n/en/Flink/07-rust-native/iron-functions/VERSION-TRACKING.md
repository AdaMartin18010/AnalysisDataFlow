---
title: "Iron Functions Version Tracking"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# Iron Functions Version Tracking

> **Project Homepage**: <https://irontools.dev>
> **Docs**: <https://irontools.dev/docs/>
> **GitHub**: <https://github.com/iron-io/functions>
> **Last Checked**: 2026-04-05

## Current Version

- **Latest Version**: Checking...
- **Doc Version**: Based on 2025-06 release
- **Status**: ✅ Synced / ⚠️ Update Needed

## Version History

| Version | Release Date | Major Changes | Doc Impact |
|---------|--------------|---------------|------------|
| v0.x | 2025-06 | Initial release | Baseline |

## Tracking Checklist

Monthly checks:

- [ ] Official website version updates
- [ ] CLI tool new features
- [ ] SDK API changes
- [ ] Supported language extensions
- [ ] Performance optimization announcements

## Pending Sync Items

- [ ] Verify current documentation accuracy
- [ ] Track WASM runtime updates
- [ ] Track Flink compatibility updates

---

## Detailed Version Information

### Iron Functions Core

| Component | Current Version | Latest Version | Status |
|-----------|-----------------|----------------|--------|
| ironfun CLI | - | - | ⏳ Pending Check |
| Rust SDK | - | - | ⏳ Pending Check |
| Go SDK | - | - | ⏳ Pending Check |
| TypeScript SDK | - | - | ⏳ Pending Check |
| Flink Runtime Integration | - | - | ⏳ Pending Check |

### Dependencies

| Dependency | Current Version | Latest Version | Impact Level |
|------------|-----------------|----------------|--------------|
| Extism PDK | 0.3.x | - | High |
| WebAssembly Runtime | - | - | High |
| Apache Flink | 1.18.x | - | Medium |

## Automated Checks

```bash
# Manual version check
python .scripts/iron-functions-tracker.py --check

# Generate sync advice
python .scripts/iron-functions-tracker.py --sync-advice

# Update version record
python .scripts/iron-functions-tracker.py --update
```

## Change Notifications

When a new version is detected, a GitHub Issue is created automatically:

- Labels: `external-dependency`, `iron-functions`
- Priority is determined by the impact level of the changes

## Reference Links

- [Iron Functions Documentation](https://irontools.dev/docs/)
- [GitHub Releases](https://github.com/iron-io/functions/releases)
- [Flink Compatibility Matrix](../00-MASTER-INDEX.md)
