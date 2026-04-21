#!/usr/bin/env python3
"""
AnalysisDataFlow Content Freshness Tracker

扩展 Flink 版本跟踪能力，监控以下外部信息源的变更：
- Apache Flink FLIP 提案仓库
- MCP / A2A 协议规范发布
- NIST / NCCoE AI Agent 身份治理标准

使用方式:
    python .scripts/content-freshness-tracker.py --check
    python .scripts/content-freshness-tracker.py --report
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin

# Optional dependencies
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Optional: pip install feedparser for RSS monitoring
try:
    import feedparser
    HAS_FEEDPARSER = True
except ImportError:
    HAS_FEEDPARSER = False


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CONFIG = {
    "flink_flips": {
        "name": "Apache Flink FLIPs",
        "source_type": "github_api",
        "url": "https://api.github.com/repos/apache/flink/contents/docs/content/docs/flips",
        "check_interval_hours": 168,  # weekly
    },
    "mcp_spec": {
        "name": "Model Context Protocol (MCP) Spec",
        "source_type": "github_releases",
        "url": "https://api.github.com/repos/modelcontextprotocol/specification/releases/latest",
        "check_interval_hours": 168,
    },
    "a2a_spec": {
        "name": "Agent-to-Agent (A2A) Protocol",
        "source_type": "github_releases",
        "url": "https://api.github.com/repos/google/A2A/releases/latest",
        "check_interval_hours": 168,
    },
    "nist_ai_rmf": {
        "name": "NIST AI Risk Management Framework",
        "source_type": "rss",
        "url": "https://www.nist.gov/news-events/cybersecurity-and-privacy-news/rss.xml",
        "keywords": ["AI", "agent", "identity", "governance", "risk management"],
        "check_interval_hours": 336,  # bi-weekly
    },
    "nist_nccoe": {
        "name": "NIST NCCoE Software & AI Agent Identity",
        "source_type": "web_page",
        "url": "https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity",
        "check_interval_hours": 336,
    },
}

STATE_FILE = Path(__file__).parent / ".content-freshness-state.json"


# ---------------------------------------------------------------------------
# State Management
# ---------------------------------------------------------------------------

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_state(state: dict) -> None:
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"[WARN] Failed to save state: {e}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Checkers
# ---------------------------------------------------------------------------

def check_github_api(name: str, url: str) -> dict:
    """Fetch directory listing from GitHub API."""
    if not HAS_REQUESTS:
        return {"status": "skipped", "reason": "requests not installed"}
    try:
        resp = requests.get(url, timeout=30, headers={"Accept": "application/vnd.github.v3+json"})
        resp.raise_for_status()
        data = resp.json()
        flip_files = [item["name"] for item in data if isinstance(item, dict) and item.get("name", "").startswith("FLIP-")]
        return {
            "status": "ok",
            "flip_count": len(flip_files),
            "latest_flips": sorted(flip_files)[-10:],
            "checked_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def check_github_releases(name: str, url: str) -> dict:
    """Fetch latest release from GitHub API."""
    if not HAS_REQUESTS:
        return {"status": "skipped", "reason": "requests not installed"}
    try:
        resp = requests.get(url, timeout=30, headers={"Accept": "application/vnd.github.v3+json"})
        if resp.status_code == 404:
            return {"status": "not_found", "reason": "No releases found yet"}
        resp.raise_for_status()
        data = resp.json()
        return {
            "status": "ok",
            "tag_name": data.get("tag_name"),
            "published_at": data.get("published_at"),
            "html_url": data.get("html_url"),
            "checked_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def check_rss(name: str, url: str, keywords: list) -> dict:
    """Check RSS feed for keyword matches."""
    if not HAS_FEEDPARSER:
        return {"status": "skipped", "reason": "feedparser not installed"}
    try:
        feed = feedparser.parse(url)
        matches = []
        for entry in feed.entries[:20]:
            text = f"{entry.get('title', '')} {entry.get('summary', '')}".lower()
            if any(kw.lower() in text for kw in keywords):
                matches.append({
                    "title": entry.get("title"),
                    "link": entry.get("link"),
                    "published": entry.get("published"),
                })
        return {
            "status": "ok",
            "match_count": len(matches),
            "matches": matches,
            "checked_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)}


def check_web_page(name: str, url: str) -> dict:
    """Fetch web page and compute a simple content hash."""
    if not HAS_REQUESTS:
        return {"status": "skipped", "reason": "requests not installed"}
    try:
        resp = requests.get(url, timeout=30, headers={"User-Agent": "AnalysisDataFlow-ContentTracker/1.0"})
        resp.raise_for_status()
        content = resp.text
        # Simple hash of first 8KB
        content_hash = hash(content[:8192])
        return {
            "status": "ok",
            "content_hash": content_hash,
            "content_length": len(content),
            "checked_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        return {"status": "error", "reason": str(e)}


# ---------------------------------------------------------------------------
# Main Logic
# ---------------------------------------------------------------------------

def should_check(source_key: str, config: dict, state: dict) -> bool:
    last_check = state.get(source_key, {}).get("checked_at")
    if not last_check:
        return True
    try:
        last_dt = datetime.fromisoformat(last_check.replace("Z", "+00:00"))
    except ValueError:
        return True
    interval = timedelta(hours=config["check_interval_hours"])
    return datetime.utcnow() - last_dt >= interval


def run_check(source_key: str, config: dict) -> dict:
    source_type = config["source_type"]
    if source_type == "github_api":
        return check_github_api(config["name"], config["url"])
    elif source_type == "github_releases":
        return check_github_releases(config["name"], config["url"])
    elif source_type == "rss":
        return check_rss(config["name"], config["url"], config.get("keywords", []))
    elif source_type == "web_page":
        return check_web_page(config["name"], config["url"])
    else:
        return {"status": "unknown_type", "reason": f"Unsupported source_type: {source_type}"}


def detect_changes(source_key: str, old_result: dict, new_result: dict) -> list:
    """Compare old and new check results to surface meaningful changes."""
    changes = []
    if old_result.get("status") != new_result.get("status"):
        changes.append(f"Status changed from '{old_result.get('status')}' to '{new_result.get('status')}'")

    # FLIP count changes
    old_count = old_result.get("flip_count")
    new_count = new_result.get("flip_count")
    if old_count is not None and new_count is not None and old_count != new_count:
        changes.append(f"FLIP count changed: {old_count} -> {new_count}")
        old_flips = set(old_result.get("latest_flips", []))
        new_flips = set(new_result.get("latest_flips", []))
        added = new_flips - old_flips
        if added:
            changes.append(f"New FLIPs detected: {', '.join(sorted(added))}")

    # Release tag changes
    old_tag = old_result.get("tag_name")
    new_tag = new_result.get("tag_name")
    if old_tag is not None and new_tag is not None and old_tag != new_tag:
        changes.append(f"New release: {old_tag} -> {new_tag}")

    # RSS match count changes
    old_matches = old_result.get("match_count", 0)
    new_matches = new_result.get("match_count", 0)
    if new_matches > old_matches:
        changes.append(f"New RSS matches: {old_matches} -> {new_matches}")

    # Web page hash changes
    old_hash = old_result.get("content_hash")
    new_hash = new_result.get("content_hash")
    if old_hash is not None and new_hash is not None and old_hash != new_hash:
        changes.append("Web page content changed")

    return changes


def cmd_check(args):
    state = load_state()
    any_change = False
    for key, cfg in CONFIG.items():
        if not should_check(key, cfg, state):
            print(f"[SKIP] {cfg['name']} - checked recently")
            continue

        print(f"[CHECK] {cfg['name']} ...")
        result = run_check(key, cfg)
        old_result = state.get(key, {})
        changes = detect_changes(key, old_result, result)

        state[key] = result
        save_state(state)

        if result.get("status") in ("error", "skipped", "not_found"):
            print(f"  -> {result['status'].upper()}: {result.get('reason', 'N/A')}")
        elif changes:
            any_change = True
            print(f"  -> CHANGES DETECTED:")
            for c in changes:
                print(f"     - {c}")
        else:
            print(f"  -> No changes detected")

    if any_change:
        print("\n[INFO] Changes detected. Run with --report to generate a detailed report.")
        return 1
    else:
        print("\n[INFO] All sources up to date.")
        return 0


def cmd_report(args):
    state = load_state()
    print("# AnalysisDataFlow Content Freshness Report\n")
    print(f"**Generated**: {datetime.utcnow().isoformat()}Z\n")
    for key, cfg in CONFIG.items():
        result = state.get(key, {})
        print(f"## {cfg['name']}")
        print(f"- **Type**: {cfg['source_type']}")
        print(f"- **URL**: {cfg['url']}")
        print(f"- **Status**: {result.get('status', 'never_checked')}")
        if 'checked_at' in result:
            print(f"- **Last Checked**: {result['checked_at']}")
        if 'tag_name' in result:
            print(f"- **Latest Tag**: {result['tag_name']} (published {result.get('published_at', 'N/A')})")
        if 'flip_count' in result:
            print(f"- **FLIP Count**: {result['flip_count']}")
        if 'match_count' in result:
            print(f"- **RSS Matches**: {result['match_count']}")
        if result.get("status") in ("error", "skipped"):
            print(f"- **Note**: {result.get('reason', '')}")
        print()


def main():
    parser = argparse.ArgumentParser(description="AnalysisDataFlow Content Freshness Tracker")
    subparsers = parser.add_subparsers(dest="command")

    check_parser = subparsers.add_parser("check", help="Check all configured sources for updates")
    report_parser = subparsers.add_parser("report", help="Generate a freshness report")

    args = parser.parse_args()

    if args.command == "check":
        sys.exit(cmd_check(args))
    elif args.command == "report":
        sys.exit(cmd_report(args))
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()

