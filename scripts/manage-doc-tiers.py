#!/usr/bin/env python3
"""
AnalysisDataFlow 文档分级标签管理脚本

功能:
1. 批量添加/更新文档的 YAML frontmatter 标签
2. 扫描并验证文档分级状态
3. 生成分级统计报告
4. 检查审查到期文档
5. 升级/降级文档层级

用法:
    python manage-doc-tiers.py scan                          # 扫描所有文档
    python manage-doc-tiers.py tier --file path/to/doc.md    # 查看文档分级
    python manage-doc-tiers.py apply-core                    # 为核心层文档添加标签
    python manage-doc-tiers.py apply-advanced                # 为进阶层文档添加标签
    python manage-doc-tiers.py check-review                  # 检查待审查文档
    python manage-doc-tiers.py stats                         # 生成统计报告
    python manage-doc-tiers.py validate                      # 验证标签完整性
"""

import os
import re
import sys
import yaml
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

# 项目根目录
PROJECT_ROOT = Path("e:/_src/AnalysisDataFlow")

# 文档分级定义 - 核心层 (50篇)
CORE_TIER_DOCS = {
    # Struct/ 16篇
    "Struct/01-foundation/01.01-unified-streaming-theory.md",
    "Struct/01-foundation/01.02-process-calculus-primer.md",
    "Struct/01-foundation/01.03-actor-model-formalization.md",
    "Struct/01-foundation/01.04-dataflow-model-formalization.md",
    "Struct/01-foundation/01.05-csp-formalization.md",
    "Struct/01-foundation/01.06-petri-net-formalization.md",
    "Struct/01-foundation/01.07-session-types.md",
    "Struct/01-foundation/stream-processing-semantics-formalization.md",
    "Struct/02-properties/02.01-determinism-in-streaming.md",
    "Struct/02-properties/02.02-consistency-hierarchy.md",
    "Struct/02-properties/02.03-watermark-monotonicity.md",
    "Struct/02-properties/02.04-liveness-and-safety.md",
    "Struct/02-properties/02.05-type-safety-derivation.md",
    "Struct/02-properties/02.06-calm-theorem.md",
    "Struct/02-properties/02.07-encrypted-stream-processing.md",
    "Struct/02-properties/02.08-differential-privacy-streaming.md",
    
    # Knowledge/ 12篇
    "Knowledge/01-concept-atlas/concurrency-paradigms-matrix.md",
    "Knowledge/01-concept-atlas/data-streaming-landscape-2026-complete.md",
    "Knowledge/01-concept-atlas/streaming-models-mindmap.md",
    "Knowledge/02-design-patterns/pattern-event-time-processing.md",
    "Knowledge/02-design-patterns/pattern-windowed-aggregation.md",
    "Knowledge/02-design-patterns/pattern-stateful-computation.md",
    "Knowledge/02-design-patterns/pattern-async-io-enrichment.md",
    "Knowledge/02-design-patterns/pattern-side-output.md",
    "Knowledge/02-design-patterns/pattern-cep-complex-event.md",
    "Knowledge/02-design-patterns/pattern-checkpoint-recovery.md",
    "Knowledge/02-design-patterns/pattern-realtime-feature-engineering.md",
    "Knowledge/02-design-patterns/pattern-log-analysis.md",
    
    # Flink/ 22篇
    "Flink/02-core/checkpoint-mechanism-deep-dive.md",
    "Flink/02-core/exactly-once-semantics-deep-dive.md",
    "Flink/02-core/exactly-once-end-to-end.md",
    "Flink/02-core/flink-state-management-complete-guide.md",
    "Flink/02-core/time-semantics-and-watermark.md",
    "Flink/02-core/backpressure-and-flow-control.md",
    "Flink/02-core/state-backends-deep-comparison.md",
    "Flink/02-core/forst-state-backend.md",
    "Flink/02-core/flink-2.0-forst-state-backend.md",
    "Flink/02-core/flink-state-ttl-best-practices.md",
    "Flink/02-core/async-execution-model.md",
    "Flink/02-core/flink-2.0-async-execution-model.md",
    "Flink/02-core/adaptive-execution-engine-v2.md",
    "Flink/02-core/smart-checkpointing-strategies.md",
    "Flink/02-core/delta-join.md",
    "Flink/02-core/delta-join-production-guide.md",
    "Flink/02-core/multi-way-join-optimization.md",
    "Flink/02-core/streaming-etl-best-practices.md",
    "Flink/02-core/flink-2.2-frontier-features.md",
    "Flink/3.9-state-backends-deep-comparison.md",
    "Flink/flink-state-backends-comparison.md",
    "Flink/state-backends-comparison.md",
}

# 进阶层文档定义 (102篇)
ADVANCED_TIER_DOCS = {
    # Struct/ 15篇
    "Struct/03-relationships/03.01-actor-to-csp-encoding.md",
    "Struct/03-relationships/03.02-flink-to-process-calculus.md",
    "Struct/03-relationships/03.03-expressiveness-hierarchy.md",
    "Struct/03-relationships/03.04-bisimulation-equivalences.md",
    "Struct/03-relationships/03.05-cross-model-mappings.md",
    "Struct/04-proofs/04.01-flink-checkpoint-correctness.md",
    "Struct/04-proofs/04.02-flink-exactly-once-correctness.md",
    "Struct/04-proofs/04.03-chandy-lamport-consistency.md",
    "Struct/04-proofs/04.04-watermark-algebra-formal-proof.md",
    "Struct/04-proofs/04.05-type-safety-fg-fgg.md",
    "Struct/04-proofs/04.06-dot-subtyping-completeness.md",
    "Struct/04-proofs/04.07-deadlock-freedom-choreographic.md",
    "Struct/07-tools/coq-mechanization.md",
    "Struct/07-tools/tla-for-flink.md",
    "Struct/07-tools/smart-casual-verification.md",
    
    # Knowledge/ 35篇 - 业务场景
    "Knowledge/03-business-patterns/fintech-realtime-risk-control.md",
    "Knowledge/03-business-patterns/real-time-recommendation.md",
    "Knowledge/03-business-patterns/iot-stream-processing.md",
    "Knowledge/03-business-patterns/log-monitoring.md",
    "Knowledge/03-business-patterns/alibaba-double11-flink.md",
    "Knowledge/03-business-patterns/netflix-streaming-pipeline.md",
    "Knowledge/03-business-patterns/uber-realtime-platform.md",
    "Knowledge/03-business-patterns/spotify-music-recommendation.md",
    "Knowledge/03-business-patterns/stripe-payment-processing.md",
    "Knowledge/03-business-patterns/gaming-analytics.md",
    "Knowledge/03-business-patterns/airbnb-marketplace-dynamics.md",
    "Knowledge/03-business-patterns/data-mesh-streaming-architecture-2026.md",
    "Knowledge/03-business-patterns/streaming-data-product-economics.md",
    # 技术选型
    "Knowledge/04-technology-selection/paradigm-selection-guide.md",
    "Knowledge/04-technology-selection/engine-selection-guide.md",
    "Knowledge/04-technology-selection/streaming-database-guide.md",
    "Knowledge/04-technology-selection/storage-selection-guide.md",
    "Knowledge/04-technology-selection/flink-vs-risingwave.md",
    # 映射指南
    "Knowledge/05-mapping-guides/struct-to-flink-mapping.md",
    "Knowledge/05-mapping-guides/theory-to-code-patterns.md",
    "Knowledge/05-mapping-guides/migration-guides/05.1-spark-streaming-to-flink-migration.md",
    "Knowledge/05-mapping-guides/migration-guides/05.2-kafka-streams-to-flink-migration.md",
    "Knowledge/05-mapping-guides/migration-guides/05.3-storm-to-flink-migration.md",
    "Knowledge/05-mapping-guides/migration-guides/05.4-flink-1x-to-2x-migration.md",
    "Knowledge/05-mapping-guides/migration-guides/05.5-batch-to-streaming-migration.md",
    # 最佳实践
    "Knowledge/07-best-practices/07.01-flink-production-checklist.md",
    "Knowledge/07-best-practices/07.02-performance-tuning-patterns.md",
    "Knowledge/07-best-practices/07.03-troubleshooting-guide.md",
    "Knowledge/07-best-practices/07.04-cost-optimization-patterns.md",
    "Knowledge/07-best-practices/07.05-security-hardening-guide.md",
    "Knowledge/07-best-practices/07.06-high-availability-patterns.md",
    "Knowledge/07-best-practices/07.07-testing-strategies-complete.md",
    # 反模式
    "Knowledge/09-anti-patterns/README.md",
    "Knowledge/09-anti-patterns/anti-pattern-checklist.md",
    "Knowledge/09-anti-patterns/streaming-anti-patterns.md",
    
    # Flink/ 52篇
    "Flink/03-api/03.02-table-sql-api/flink-table-sql-complete-guide.md",
    "Flink/03-api/03.02-table-sql-api/flink-sql-window-functions-deep-dive.md",
    "Flink/03-api/03.02-table-sql-api/flink-sql-calcite-optimizer-deep-dive.md",
    "Flink/03-api/03.02-table-sql-api/flink-cep-complete-guide.md",
    "Flink/03-api/03.02-table-sql-api/flink-materialized-table-deep-dive.md",
    "Flink/03-api/03.02-table-sql-api/materialized-tables.md",
    "Flink/03-api/03.02-table-sql-api/ansi-sql-2023-compliance-guide.md",
    "Flink/03-api/03.02-table-sql-api/flink-sql-hints-optimization.md",
    "Flink/03-api/03.02-table-sql-api/flink-process-table-functions.md",
    "Flink/03-api/03.02-table-sql-api/built-in-functions-complete-list.md",
    "Flink/03-api/03.02-table-sql-api/data-types-complete-reference.md",
    "Flink/03-api/03.02-table-sql-api/flink-python-udf.md",
    "Flink/03-api/03.02-table-sql-api/vector-search.md",
    "Flink/03-api/03.02-table-sql-api/flink-vector-search-rag.md",
    "Flink/data-types-complete-reference.md",
    "Flink/flink-data-types-reference.md",
    "Flink/flink-built-in-functions-reference.md",
    "Flink/built-in-functions-reference.md",
    # 部署
    "Flink/04-runtime/04.01-deployment/flink-deployment-ops-complete-guide.md",
    "Flink/04-runtime/04.01-deployment/kubernetes-deployment.md",
    "Flink/04-runtime/04.01-deployment/kubernetes-deployment-production-guide.md",
    "Flink/04-runtime/04.01-deployment/flink-kubernetes-operator-deep-dive.md",
    "Flink/04-runtime/04.01-deployment/flink-kubernetes-autoscaler-deep-dive.md",
    "Flink/04-runtime/04.01-deployment/flink-serverless-architecture.md",
    "Flink/04-runtime/04.01-deployment/serverless-flink-ga-guide.md",
    "Flink/04-runtime/04.01-deployment/multi-cloud-deployment-templates.md",
    "Flink/04-runtime/04.01-deployment/flink-24-deployment-improvements.md",
    "Flink/04-runtime/04.01-deployment/cost-optimization-calculator.md",
    # 可观测性
    "Flink/04-runtime/04.03-observability/flink-observability-complete-guide.md",
    "Flink/04-runtime/04.03-observability/metrics-and-monitoring.md",
    "Flink/04-runtime/04.03-observability/distributed-tracing.md",
    "Flink/04-runtime/04.03-observability/flink-opentelemetry-observability.md",
    "Flink/04-runtime/04.03-observability/opentelemetry-streaming-observability.md",
    "Flink/04-runtime/04.03-observability/realtime-data-quality-monitoring.md",
    "Flink/04-runtime/04.03-observability/split-level-watermark-metrics.md",
    "Flink/04-runtime/04.03-observability/streaming-metrics-monitoring-slo.md",
    "Flink/04-runtime/04.03-observability/event-reporting.md",
    # 连接器
    "Flink/05-ecosystem/05.01-connectors/flink-connectors-ecosystem-complete-guide.md",
    "Flink/05-ecosystem/05.01-connectors/kafka-integration-patterns.md",
    "Flink/05-ecosystem/05.01-connectors/flink-cdc-3.0-data-integration.md",
    "Flink/05-ecosystem/05.01-connectors/jdbc-connector-complete-guide.md",
    "Flink/05-ecosystem/05.01-connectors/elasticsearch-connector-complete-guide.md",
    "Flink/05-ecosystem/05.01-connectors/mongodb-connector-complete-guide.md",
    "Flink/05-ecosystem/05.01-connectors/flink-delta-lake-integration.md",
    "Flink/05-ecosystem/05.01-connectors/flink-iceberg-integration.md",
    # AI/ML
    "Flink/06-ai-ml/flink-ai-ml-integration-complete-guide.md",
    "Flink/06-ai-ml/flink-ml-architecture.md",
    "Flink/06-ai-ml/flink-realtime-ml-inference.md",
    "Flink/06-ai-ml/realtime-feature-engineering-feature-store.md",
    "Flink/06-ai-ml/flink-llm-integration.md",
    "Flink/06-ai-ml/flink-llm-realtime-rag-architecture.md",
    "Flink/06-ai-ml/vector-database-integration.md",
}


@dataclass
class DocInfo:
    """文档信息"""
    path: Path
    tier: Optional[str] = None
    review_cycle: Optional[str] = None
    last_reviewed: Optional[str] = None
    next_review: Optional[str] = None
    formal_level: Optional[str] = None
    has_frontmatter: bool = False
    raw_frontmatter: Optional[str] = None


def extract_frontmatter(content: str) -> Tuple[Optional[Dict], str, str]:
    """
    提取 YAML frontmatter
    返回: (frontmatter_dict, content_without_frontmatter, raw_frontmatter)
    """
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        try:
            raw_fm = match.group(1)
            fm = yaml.safe_load(raw_fm)
            rest_content = content[match.end():]
            return fm, rest_content, raw_fm
        except yaml.YAMLError:
            return None, content, None
    
    return None, content, None


def get_tier_from_path(rel_path: str) -> Optional[str]:
    """根据路径确定文档层级"""
    # 规范化路径
    rel_path = rel_path.replace("\\", "/")
    
    if rel_path in CORE_TIER_DOCS:
        return "core"
    elif rel_path in ADVANCED_TIER_DOCS:
        return "advanced"
    else:
        # 检查是否在三大目录下
        if rel_path.startswith(("Struct/", "Knowledge/", "Flink/")):
            return "reference"
    return None


def get_review_cycle(tier: str) -> str:
    """根据层级获取审查周期"""
    cycles = {
        "core": "monthly",
        "advanced": "quarterly",
        "reference": "biannual"
    }
    return cycles.get(tier, "biannual")


def get_maintainers(tier: str) -> List[str]:
    """根据层级获取维护者"""
    maintainers = {
        "core": ["core-team"],
        "advanced": ["domain-experts"],
        "reference": ["community"]
    }
    return maintainers.get(tier, ["community"])


def calculate_next_review(last_reviewed: str, review_cycle: str) -> str:
    """计算下次审查日期"""
    try:
        last = datetime.strptime(last_reviewed, "%Y-%m-%d")
    except (ValueError, TypeError):
        last = datetime.now()
    
    deltas = {
        "monthly": timedelta(days=30),
        "quarterly": timedelta(days=90),
        "biannual": timedelta(days=180)
    }
    
    next_date = last + deltas.get(review_cycle, timedelta(days=180))
    return next_date.strftime("%Y-%m-%d")


def scan_document(doc_path: Path) -> DocInfo:
    """扫描单个文档"""
    rel_path = doc_path.relative_to(PROJECT_ROOT).as_posix()
    
    info = DocInfo(path=doc_path)
    info.tier = get_tier_from_path(rel_path)
    
    try:
        content = doc_path.read_text(encoding='utf-8')
        fm, _, raw_fm = extract_frontmatter(content)
        
        if fm:
            info.has_frontmatter = True
            info.raw_frontmatter = raw_fm
            info.tier = fm.get("tier", info.tier)
            info.review_cycle = fm.get("review-cycle")
            info.last_reviewed = fm.get("last-reviewed")
            info.next_review = fm.get("next-review")
            info.formal_level = fm.get("formal-level")
    except Exception as e:
        print(f"警告: 无法读取 {rel_path}: {e}")
    
    return info


def scan_all_documents() -> List[DocInfo]:
    """扫描所有文档"""
    docs = []
    
    for dir_name in ["Struct", "Knowledge", "Flink"]:
        dir_path = PROJECT_ROOT / dir_name
        if dir_path.exists():
            for md_file in dir_path.rglob("*.md"):
                # 排除隐藏目录
                if "/." not in str(md_file) and "\\." not in str(md_file):
                    docs.append(scan_document(md_file))
    
    return docs


def apply_frontmatter(doc_path: Path, tier: str, dry_run: bool = False) -> bool:
    """
    为文档添加/更新 frontmatter
    返回: 是否成功
    """
    try:
        content = doc_path.read_text(encoding='utf-8')
        rel_path = doc_path.relative_to(PROJECT_ROOT).as_posix().replace("\\", "/")
        
        fm, rest_content, _ = extract_frontmatter(content)
        
        # 构建新的 frontmatter
        new_fm = {
            "tier": tier,
            "review-cycle": get_review_cycle(tier),
            "maintainers": get_maintainers(tier),
            "created": datetime.now().strftime("%Y-%m-%d") if not fm or "created" not in fm else fm.get("created"),
            "last-reviewed": datetime.now().strftime("%Y-%m-%d"),
            "next-review": calculate_next_review(datetime.now().strftime("%Y-%m-%d"), get_review_cycle(tier)),
            "status": "stable"
        }
        
        # 保留现有字段
        if fm:
            for key in ["formal-level", "version", "dependencies", "tags"]:
                if key in fm:
                    new_fm[key] = fm[key]
        
        # 生成 YAML
        yaml_content = yaml.dump(new_fm, allow_unicode=True, sort_keys=False)
        new_content = f"---\n{yaml_content}---\n\n{rest_content.lstrip()}"
        
        if dry_run:
            print(f"[DRY RUN] 将更新: {rel_path}")
            return True
        
        doc_path.write_text(new_content, encoding='utf-8')
        print(f"已更新: {rel_path}")
        return True
        
    except Exception as e:
        print(f"错误: 无法更新 {rel_path}: {e}")
        return False


def cmd_scan(args):
    """扫描命令"""
    print("正在扫描所有文档...")
    docs = scan_all_documents()
    
    stats = defaultdict(int)
    for doc in docs:
        tier = doc.tier or "unclassified"
        stats[tier] += 1
    
    print(f"\n扫描完成! 共发现 {len(docs)} 篇文档:")
    print(f"  核心层 (core): {stats.get('core', 0)} 篇")
    print(f"  进阶层 (advanced): {stats.get('advanced', 0)} 篇")
    print(f"  参考层 (reference): {stats.get('reference', 0)} 篇")
    print(f"  未分类 (unclassified): {stats.get('unclassified', 0)} 篇")


def cmd_tier(args):
    """查看文档分级命令"""
    doc_path = PROJECT_ROOT / args.file
    if not doc_path.exists():
        print(f"错误: 文件不存在: {args.file}")
        return
    
    info = scan_document(doc_path)
    
    print(f"\n文档: {args.file}")
    print(f"{'='*50}")
    print(f"层级 (tier): {info.tier or '未设置'}")
    print(f"审查周期: {info.review_cycle or '未设置'}")
    print(f"最后审查: {info.last_reviewed or '未设置'}")
    print(f"下次审查: {info.next_review or '未设置'}")
    print(f"形式化等级: {info.formal_level or '未设置'}")
    print(f"已有 frontmatter: {'是' if info.has_frontmatter else '否'}")


def cmd_apply_tier(args, tier: str):
    """应用指定层级的标签"""
    target_docs = CORE_TIER_DOCS if tier == "core" else ADVANCED_TIER_DOCS
    
    print(f"正在为 {tier} 层文档应用标签...")
    print(f"目标文档数: {len(target_docs)}")
    
    success = 0
    failed = 0
    
    for rel_path in sorted(target_docs):
        doc_path = PROJECT_ROOT / rel_path
        if doc_path.exists():
            if apply_frontmatter(doc_path, tier, args.dry_run):
                success += 1
            else:
                failed += 1
        else:
            print(f"警告: 文件不存在: {rel_path}")
            failed += 1
    
    print(f"\n完成: 成功 {success}, 失败 {failed}")


def cmd_check_review(args):
    """检查待审查文档"""
    print("正在检查待审查文档...")
    docs = scan_all_documents()
    
    today = datetime.now()
    overdue = []
    upcoming = []
    
    for doc in docs:
        if not doc.next_review:
            continue
        
        try:
            next_date = datetime.strptime(doc.next_review, "%Y-%m-%d")
            days_diff = (next_date - today).days
            
            if days_diff < 0:
                overdue.append((doc, abs(days_diff)))
            elif days_diff <= 7:
                upcoming.append((doc, days_diff))
        except ValueError:
            pass
    
    print(f"\n已逾期文档 ({len(overdue)}):")
    for doc, days in sorted(overdue, key=lambda x: x[1], reverse=True)[:20]:
        rel_path = doc.path.relative_to(PROJECT_ROOT).as_posix()
        print(f"  - {rel_path} (逾期 {days} 天)")
    if len(overdue) > 20:
        print(f"  ... 还有 {len(overdue) - 20} 篇")
    
    print(f"\n即将到期文档 ({len(upcoming)}):")
    for doc, days in sorted(upcoming, key=lambda x: x[1]):
        rel_path = doc.path.relative_to(PROJECT_ROOT).as_posix()
        print(f"  - {rel_path} (还有 {days} 天)")


def cmd_stats(args):
    """生成统计报告"""
    print("正在生成统计报告...")
    docs = scan_all_documents()
    
    # 按层级统计
    tier_stats = defaultdict(lambda: {"count": 0, "with_fm": 0, "size": 0})
    
    for doc in docs:
        tier = doc.tier or "unclassified"
        tier_stats[tier]["count"] += 1
        if doc.has_frontmatter:
            tier_stats[tier]["with_fm"] += 1
        try:
            tier_stats[tier]["size"] += doc.path.stat().st_size
        except:
            pass
    
    print("\n" + "="*60)
    print("文档分级统计报告")
    print("="*60)
    
    total = len(docs)
    for tier in ["core", "advanced", "reference", "unclassified"]:
        if tier in tier_stats:
            stats = tier_stats[tier]
            pct = stats["count"] / total * 100
            size_mb = stats["size"] / (1024 * 1024)
            fm_pct = stats["with_fm"] / stats["count"] * 100 if stats["count"] > 0 else 0
            
            print(f"\n{tier.upper()} 层:")
            print(f"  文档数: {stats['count']} ({pct:.1f}%)")
            print(f"  已标注: {stats['with_fm']} ({fm_pct:.1f}%)")
            print(f"  总大小: {size_mb:.2f} MB")
    
    print(f"\n总计: {total} 篇文档")
    
    # 审查状态
    today = datetime.now()
    needs_review = 0
    for doc in docs:
        if doc.next_review:
            try:
                next_date = datetime.strptime(doc.next_review, "%Y-%m-%d")
                if next_date <= today:
                    needs_review += 1
            except ValueError:
                pass
    
    print(f"\n待审查文档: {needs_review} 篇")


def cmd_validate(args):
    """验证标签完整性"""
    print("正在验证文档标签...")
    docs = scan_all_documents()
    
    issues = []
    
    for doc in docs:
        rel_path = doc.path.relative_to(PROJECT_ROOT).as_posix()
        
        # 检查必需字段
        if doc.has_frontmatter:
            if not doc.tier:
                issues.append(f"{rel_path}: 缺少 tier 字段")
            if not doc.review_cycle:
                issues.append(f"{rel_path}: 缺少 review-cycle 字段")
            if not doc.last_reviewed:
                issues.append(f"{rel_path}: 缺少 last-reviewed 字段")
        else:
            # 未分类文档应该有 frontmatter
            if doc.tier in ["core", "advanced"]:
                issues.append(f"{rel_path}: 核心/进阶层文档缺少 frontmatter")
    
    print(f"\n发现 {len(issues)} 个问题:")
    for issue in issues[:30]:
        print(f"  - {issue}")
    if len(issues) > 30:
        print(f"  ... 还有 {len(issues) - 30} 个问题")


def main():
    parser = argparse.ArgumentParser(
        description="AnalysisDataFlow 文档分级标签管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s scan                           # 扫描所有文档
  %(prog)s tier --file Struct/01-foundation/01.01-unified-streaming-theory.md
  %(prog)s apply-core --dry-run          # 预览核心层标签应用
  %(prog)s apply-core                    # 应用核心层标签
  %(prog)s check-review                  # 检查待审查文档
  %(prog)s stats                         # 生成统计报告
  %(prog)s validate                      # 验证标签完整性
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # scan 命令
    subparsers.add_parser("scan", help="扫描所有文档")
    
    # tier 命令
    tier_parser = subparsers.add_parser("tier", help="查看文档分级")
    tier_parser.add_argument("--file", required=True, help="文档路径")
    
    # apply-core 命令
    apply_core = subparsers.add_parser("apply-core", help="为核心层文档添加标签")
    apply_core.add_argument("--dry-run", action="store_true", help="仅预览，不实际修改")
    
    # apply-advanced 命令
    apply_advanced = subparsers.add_parser("apply-advanced", help="为进阶层文档添加标签")
    apply_advanced.add_argument("--dry-run", action="store_true", help="仅预览，不实际修改")
    
    # check-review 命令
    subparsers.add_parser("check-review", help="检查待审查文档")
    
    # stats 命令
    subparsers.add_parser("stats", help="生成统计报告")
    
    # validate 命令
    subparsers.add_parser("validate", help="验证标签完整性")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # 执行命令
    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "tier":
        cmd_tier(args)
    elif args.command == "apply-core":
        cmd_apply_tier(args, "core")
    elif args.command == "apply-advanced":
        cmd_apply_tier(args, "advanced")
    elif args.command == "check-review":
        cmd_check_review(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "validate":
        cmd_validate(args)


if __name__ == "__main__":
    main()
