#!/usr/bin/env python3
"""
Iron Functions 版本跟踪脚本

功能：
1. 检查官网版本信息
2. 对比本地文档版本
3. 生成同步建议和报告
4. 自动创建更新提醒

使用：
    python iron-functions-tracker.py [--check] [--sync-advice] [--update] [--report]
"""

import argparse
import json
import re
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

try:
    import requests
except ImportError:
    print("警告: 未安装 requests 库，将使用模拟数据")
    requests = None


class SyncStatus(Enum):
    """同步状态"""
    SYNCED = "synced"          # 已同步
    NEEDS_UPDATE = "needs_update"  # 需要更新
    CHECKING = "checking"      # 检查中
    UNKNOWN = "unknown"        # 未知


@dataclass
class ComponentVersion:
    """组件版本信息"""
    name: str
    current_version: str
    latest_version: str
    last_checked: str
    status: SyncStatus
    release_date: str = ""
    changelog_url: str = ""
    priority: str = "medium"  # high, medium, low


@dataclass
class VersionReport:
    """版本报告"""
    timestamp: str
    overall_status: SyncStatus
    components: List[ComponentVersion]
    sync_advice: List[str]
    action_items: List[str]


class IronFunctionsTracker:
    """Iron Functions 版本跟踪器"""
    
    # 项目配置
    PROJECT_URL = "https://irontools.dev"
    DOCS_URL = "https://irontools.dev/docs"
    GITHUB_API = "https://api.github.com/repos/irontools/iron-functions"
    
    # 本地文件路径
    VERSION_TRACKING_FILE = Path("Flink/14-rust-assembly-ecosystem/iron-functions/VERSION-TRACKING.md")
    MAIN_DOC_FILE = Path("Flink/14-rust-assembly-ecosystem/iron-functions/01-iron-functions-complete-guide.md")
    STATE_FILE = Path(".scripts/iron-functions-state.json")
    
    def __init__(self):
        self.state = self._load_state()
        self.report = None
    
    def _load_state(self) -> Dict:
        """加载状态文件"""
        if self.STATE_FILE.exists():
            try:
                with open(self.STATE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {
            "last_check": None,
            "versions": {},
            "check_count": 0
        }
    
    def _save_state(self):
        """保存状态文件"""
        self.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)
    
    def _fetch_latest_version(self) -> Optional[str]:
        """从 GitHub API 获取最新版本"""
        if requests is None:
            return None
        
        try:
            response = requests.get(
                f"{self.GITHUB_API}/releases/latest",
                headers={"Accept": "application/vnd.github.v3+json"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("tag_name", "unknown")
        except Exception as e:
            print(f"获取最新版本失败: {e}")
        
        return None
    
    def _check_website_version(self) -> Dict:
        """检查官网版本信息（模拟/占位）"""
        # 实际实现需要爬取 irontools.dev
        # 这里返回占位数据
        return {
            "cli_version": "0.1.0",
            "sdk_versions": {
                "rust": "0.2.0",
                "go": "0.1.5",
                "typescript": "0.1.3"
            },
            "docs_version": "2025-06",
            "flink_compatibility": ["1.18", "1.19"]
        }
    
    def _extract_doc_version(self) -> str:
        """从文档中提取版本信息"""
        if not self.MAIN_DOC_FILE.exists():
            return "unknown"
        
        try:
            content = self.MAIN_DOC_FILE.read_text(encoding='utf-8')
            # 查找版本声明
            version_match = re.search(r'版本[:：]\s*v?(\d+\.\d+(?:\.\d+)?)', content)
            if version_match:
                return version_match.group(1)
            
            # 查找基于日期
            date_match = re.search(r'基于\s*(\d{4}-\d{2})', content)
            if date_match:
                return date_match.group(1)
        except Exception:
            pass
        
        return "unknown"
    
    def check_versions(self) -> List[ComponentVersion]:
        """检查所有组件版本"""
        components = []
        now = datetime.now().isoformat()
        
        # 检查 Core 版本
        latest = self._fetch_latest_version()
        current = self.state.get("versions", {}).get("core", "unknown")
        
        components.append(ComponentVersion(
            name="Iron Functions Core",
            current_version=current,
            latest_version=latest or "unknown",
            last_checked=now,
            status=SyncStatus.NEEDS_UPDATE if latest and latest != current else SyncStatus.SYNCED,
            changelog_url=f"{self.GITHUB_API}/releases",
            priority="high"
        ))
        
        # 检查 CLI 版本
        website_info = self._check_website_version()
        cli_current = self.state.get("versions", {}).get("cli", "unknown")
        cli_latest = website_info.get("cli_version", "unknown")
        
        components.append(ComponentVersion(
            name="ironfun CLI",
            current_version=cli_current,
            latest_version=cli_latest,
            last_checked=now,
            status=SyncStatus.NEEDS_UPDATE if cli_latest != cli_current else SyncStatus.SYNCED,
            priority="high"
        ))
        
        # 检查 SDK 版本
        for lang, version in website_info.get("sdk_versions", {}).items():
            current_sdk = self.state.get("versions", {}).get(f"sdk_{lang}", "unknown")
            components.append(ComponentVersion(
                name=f"{lang.title()} SDK",
                current_version=current_sdk,
                latest_version=version,
                last_checked=now,
                status=SyncStatus.NEEDS_UPDATE if version != current_sdk else SyncStatus.SYNCED,
                priority="medium"
            ))
        
        # 更新状态
        self.state["last_check"] = now
        self.state["check_count"] = self.state.get("check_count", 0) + 1
        self._save_state()
        
        return components
    
    def generate_sync_advice(self, components: List[ComponentVersion]) -> Tuple[List[str], List[str]]:
        """生成同步建议和行动项"""
        advice = []
        actions = []
        
        needs_update = [c for c in components if c.status == SyncStatus.NEEDS_UPDATE]
        
        if not needs_update:
            advice.append("✅ 所有组件版本已同步，无需更新")
            return advice, actions
        
        advice.append(f"⚠️ 检测到 {len(needs_update)} 个组件需要更新：")
        
        for comp in needs_update:
            advice.append(f"  - {comp.name}: {comp.current_version} → {comp.latest_version}")
            
            if comp.priority == "high":
                actions.append(f"[高优先级] 更新 {comp.name} 文档")
                actions.append(f"  - 检查 {comp.name} 的兼容性变更")
                actions.append(f"  - 更新代码示例")
            else:
                actions.append(f"[中优先级] 检查 {comp.name} 更新")
        
        # 添加通用建议
        advice.append("\n📋 通用同步步骤：")
        advice.append("  1. 查看官方 Changelog")
        advice.append("  2. 更新 VERSION-TRACKING.md")
        advice.append("  3. 更新主文档版本声明")
        advice.append("  4. 验证示例代码兼容性")
        advice.append("  5. 运行验证示例测试")
        
        return advice, actions
    
    def generate_report(self, components: List[ComponentVersion]) -> VersionReport:
        """生成完整报告"""
        advice, actions = self.generate_sync_advice(components)
        
        # 确定整体状态
        statuses = [c.status for c in components]
        if all(s == SyncStatus.SYNCED for s in statuses):
            overall = SyncStatus.SYNCED
        elif any(s == SyncStatus.NEEDS_UPDATE for s in statuses):
            overall = SyncStatus.NEEDS_UPDATE
        else:
            overall = SyncStatus.CHECKING
        
        return VersionReport(
            timestamp=datetime.now().isoformat(),
            overall_status=overall,
            components=components,
            sync_advice=advice,
            action_items=actions
        )
    
    def print_report(self, report: VersionReport, format_type: str = "text"):
        """打印报告"""
        if format_type == "json":
            print(json.dumps({
                "timestamp": report.timestamp,
                "overall_status": report.overall_status.value,
                "components": [asdict(c) for c in report.components],
                "sync_advice": report.sync_advice,
                "action_items": report.action_items
            }, indent=2, ensure_ascii=False))
        else:
            print("=" * 60)
            print("Iron Functions 版本跟踪报告")
            print("=" * 60)
            print(f"检查时间: {report.timestamp}")
            print(f"整体状态: {report.overall_status.value.upper()}")
            print()
            
            print("组件版本：")
            print("-" * 60)
            for comp in report.components:
                status_icon = "✅" if comp.status == SyncStatus.SYNCED else "⚠️"
                print(f"{status_icon} {comp.name}")
                print(f"   当前: {comp.current_version} | 最新: {comp.latest_version}")
                print()
            
            print("同步建议：")
            print("-" * 60)
            for item in report.sync_advice:
                print(item)
            print()
            
            if report.action_items:
                print("行动项：")
                print("-" * 60)
                for item in report.action_items:
                    print(item)
    
    def update_tracking_file(self, report: VersionReport) -> bool:
        """更新版本跟踪文件"""
        if not self.VERSION_TRACKING_FILE.exists():
            print(f"警告: 跟踪文件不存在 {self.VERSION_TRACKING_FILE}")
            return False
        
        try:
            content = self.VERSION_TRACKING_FILE.read_text(encoding='utf-8')
            
            # 更新最后检查时间
            content = re.sub(
                r'最后检查[:：]\s*\d{4}-\d{2}-\d{2}',
                f'最后检查: {datetime.now().strftime("%Y-%m-%d")}',
                content
            )
            
            # 更新状态
            status = "✅ 同步" if report.overall_status == SyncStatus.SYNCED else "⚠️ 需更新"
            content = re.sub(
                r'状态[:：]\s*[✅⚠️]\s*\S+',
                f'状态: {status}',
                content
            )
            
            # 更新最新版本（从 Core 组件获取）
            core_comp = next((c for c in report.components if c.name == "Iron Functions Core"), None)
            if core_comp and core_comp.latest_version != "unknown":
                content = re.sub(
                    r'最新版本[:：]\s*\S+',
                    f'最新版本: {core_comp.latest_version}',
                    content
                )
            
            self.VERSION_TRACKING_FILE.write_text(content, encoding='utf-8')
            print(f"✅ 已更新 {self.VERSION_TRACKING_FILE}")
            return True
            
        except Exception as e:
            print(f"更新跟踪文件失败: {e}")
            return False
    
    def check_and_report(self, output_format: str = "text") -> VersionReport:
        """执行检查并生成报告"""
        components = self.check_versions()
        report = self.generate_report(components)
        self.report = report
        self.print_report(report, output_format)
        return report


def main():
    parser = argparse.ArgumentParser(
        description="Iron Functions 版本跟踪工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --check                    # 检查版本并显示报告
  %(prog)s --check --format json      # 以 JSON 格式输出
  %(prog)s --sync-advice              # 显示同步建议
  %(prog)s --update                   # 更新跟踪文件
  %(prog)s --report                   # 生成完整报告
        """
    )
    
    parser.add_argument('--check', action='store_true',
                        help='检查版本状态')
    parser.add_argument('--sync-advice', action='store_true',
                        help='生成同步建议')
    parser.add_argument('--update', action='store_true',
                        help='更新版本跟踪文件')
    parser.add_argument('--report', action='store_true',
                        help='生成完整报告')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='输出格式 (默认: text)')
    parser.add_argument('--create-issue', action='store_true',
                        help='创建 GitHub Issue（需要 GITHUB_TOKEN）')
    
    args = parser.parse_args()
    
    # 如果没有指定任何操作，默认执行 check
    if not any([args.check, args.sync_advice, args.update, args.report]):
        args.check = True
    
    tracker = IronFunctionsTracker()
    
    if args.check or args.report:
        report = tracker.check_and_report(args.format)
        
        if args.update:
            tracker.update_tracking_file(report)
        
        # 返回码：需要更新时返回 1
        if report.overall_status == SyncStatus.NEEDS_UPDATE:
            sys.exit(1)
    
    elif args.sync_advice:
        components = tracker.check_versions()
        advice, actions = tracker.generate_sync_advice(components)
        print("\n".join(advice))
        print("\n行动项：")
        print("\n".join(actions))
    
    elif args.update:
        components = tracker.check_versions()
        report = tracker.generate_report(components)
        tracker.update_tracking_file(report)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
