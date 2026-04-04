#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统计更新系统主运行脚本 (Main Runner)

功能:
    - 协调执行所有统计更新任务
    - 支持命令行参数控制
    - 支持定时执行
    - 支持Git自动提交
    - 错误处理和日志记录

作者: AnalysisDataFlow Project
版本: 1.0.0

用法:
    python run.py [options]

选项:
    --full              执行完整更新流程（默认）
    --collect-only      仅收集统计
    --dashboard-only    仅生成仪表盘
    --readme-only       仅更新README
    --tracking-only     仅更新PROJECT-TRACKING
    --weekly-only       仅生成周报
    --git-commit        自动提交变更到Git
    --help              显示帮助信息

示例:
    python run.py                           # 执行完整更新
    python run.py --collect-only            # 仅收集统计
    python run.py --full --git-commit       # 完整更新并提交
"""

import sys
import argparse
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# 导入各模块
sys.path.insert(0, str(Path(__file__).parent))


class StatsUpdateRunner:
    """统计更新运行器"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化运行器
        
        Args:
            config_path: 配置文件路径
        """
        self.script_dir = Path(__file__).parent
        self.config = self._load_config(config_path)
        self.root_dir = Path(self.config["project"]["root_dir"]).resolve()
        self.stats_dir = self.root_dir / ".stats"
        
        # 确保统计目录存在
        self.stats_dir.mkdir(exist_ok=True)
        
        # 日志记录
        self.log_file = self.stats_dir / "update.log"
        
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        try:
            with open(self.script_dir / config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "project": {"root_dir": "../.."},
                "git": {"enable_commit": False, "commit_message_template": "📊 自动更新项目统计 - {timestamp}"}
            }
    
    def log(self, message: str, level: str = "INFO"):
        """
        记录日志
        
        Args:
            message: 日志消息
            level: 日志级别
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # 输出到控制台
        print(log_entry)
        
        # 写入日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def run_script(self, script_name: str, description: str) -> bool:
        """
        运行指定的Python脚本
        
        Args:
            script_name: 脚本文件名
            description: 任务描述
            
        Returns:
            bool: 是否成功
        """
        script_path = self.script_dir / script_name
        
        if not script_path.exists():
            self.log(f"脚本不存在: {script_path}", "ERROR")
            return False
        
        self.log(f"开始执行: {description}")
        
        try:
            # 使用subprocess运行脚本
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=self.script_dir,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            # 输出脚本输出
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        print(f"  {line}")
            
            if result.stderr:
                for line in result.stderr.strip().split('\n'):
                    if line.strip():
                        print(f"  [ERR] {line}")
            
            if result.returncode == 0:
                self.log(f"✅ 完成: {description}")
                return True
            else:
                self.log(f"❌ 失败: {description} (返回码: {result.returncode})", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ 异常: {description} - {str(e)}", "ERROR")
            return False
    
    def run_full_update(self, git_commit: bool = False) -> bool:
        """
        执行完整更新流程
        
        Args:
            git_commit: 是否自动提交到Git
            
        Returns:
            bool: 是否全部成功
        """
        self.log("=" * 60)
        self.log("🚀 启动完整统计更新流程")
        self.log("=" * 60)
        
        results = []
        
        # 1. 收集统计
        results.append(("统计收集", self.run_script("stats-collector.py", "收集项目统计")))
        
        # 2. 生成仪表盘
        results.append(("仪表盘生成", self.run_script("dashboard-generator.py", "生成统计仪表盘")))
        
        # 3. 更新README
        results.append(("README更新", self.run_script("readme-updater.py", "更新README.md")))
        
        # 4. 更新PROJECT-TRACKING
        results.append(("跟踪文档更新", self.run_script("tracking-updater.py", "更新PROJECT-TRACKING.md")))
        
        # 5. 生成周报（如果是周日或手动执行）
        today = datetime.now()
        if today.weekday() == 6:  # 周日
            results.append(("周报生成", self.run_script("weekly-report.py", "生成周报")))
        
        # 汇总结果
        self.log("=" * 60)
        self.log("📊 执行结果汇总")
        self.log("=" * 60)
        
        all_success = True
        for task_name, success in results:
            status = "✅ 成功" if success else "❌ 失败"
            self.log(f"  {task_name}: {status}")
            if not success:
                all_success = False
        
        # Git提交
        if git_commit and all_success:
            self.git_commit_changes()
        
        self.log("=" * 60)
        self.log("✅ 完整更新流程结束" if all_success else "⚠️ 部分任务失败")
        self.log("=" * 60)
        
        return all_success
    
    def git_commit_changes(self) -> bool:
        """
        提交变更到Git
        
        Returns:
            bool: 是否成功
        """
        git_config = self.config.get("git", {})
        if not git_config.get("enable_commit", False):
            self.log("Git自动提交已禁用", "WARN")
            return False
        
        self.log("📝 开始Git提交流程")
        
        try:
            # 检查是否有变更
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.root_dir,
                capture_output=True,
                text=True
            )
            
            if not status_result.stdout.strip():
                self.log("ℹ️ 没有需要提交的变更")
                return True
            
            # 添加变更
            add_result = subprocess.run(
                ["git", "add", "."],
                cwd=self.root_dir,
                capture_output=True,
                text=True
            )
            
            if add_result.returncode != 0:
                self.log(f"Git add 失败: {add_result.stderr}", "ERROR")
                return False
            
            # 提交变更
            template = git_config.get("commit_message_template", "📊 自动更新项目统计 - {timestamp}")
            commit_message = template.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"))
            
            commit_result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.root_dir,
                capture_output=True,
                text=True
            )
            
            if commit_result.returncode == 0:
                self.log(f"✅ Git提交成功: {commit_message}")
                
                # 可选：推送到远程
                # push_result = subprocess.run(
                #     ["git", "push"],
                #     cwd=self.root_dir,
                #     capture_output=True,
                #     text=True
                # )
                
                return True
            else:
                self.log(f"Git commit 失败: {commit_result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"Git提交异常: {str(e)}", "ERROR")
            return False
    
    def show_status(self):
        """显示当前状态"""
        self.log("=" * 60)
        self.log("📊 项目统计更新系统状态")
        self.log("=" * 60)
        
        # 检查各脚本是否存在
        scripts = [
            "stats-collector.py",
            "dashboard-generator.py",
            "readme-updater.py",
            "tracking-updater.py",
            "weekly-report.py",
        ]
        
        self.log("\n脚本状态:")
        for script in scripts:
            exists = (self.script_dir / script).exists()
            status = "✅ 就绪" if exists else "❌ 缺失"
            self.log(f"  {script}: {status}")
        
        # 检查统计数据
        self.log("\n统计数据:")
        stats_file = self.stats_dir / "project-stats.json"
        if stats_file.exists():
            try:
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                summary = stats.get("summary", {})
                self.log(f"  文档数: {summary.get('total_docs', 0)}")
                self.log(f"  形式化元素: {summary.get('formal_elements', {}).get('total', 0)}")
                self.log(f"  最后更新: {stats.get('timestamp', '未知')}")
            except Exception as e:
                self.log(f"  读取统计失败: {e}", "ERROR")
        else:
            self.log("  暂无统计数据")
        
        # 检查日志
        if self.log_file.exists():
            log_size = self.log_file.stat().st_size
            self.log(f"\n日志文件: {self.log_file} ({log_size} bytes)")
        
        self.log("=" * 60)


def print_help():
    """打印帮助信息"""
    help_text = """
╔══════════════════════════════════════════════════════════════╗
║     AnalysisDataFlow 项目统计自动更新系统 v1.0.0              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  用法: python run.py [选项]                                   ║
║                                                              ║
║  选项:                                                        ║
║    --full              执行完整更新流程（默认）                ║
║    --collect-only      仅收集统计                             ║
║    --dashboard-only    仅生成仪表盘                           ║
║    --readme-only       仅更新README                           ║
║    --tracking-only     仅更新PROJECT-TRACKING                 ║
║    --weekly-only       仅生成周报                             ║
║    --git-commit        自动提交变更到Git                      ║
║    --status            显示系统状态                           ║
║    --help              显示此帮助信息                         ║
║                                                              ║
║  示例:                                                        ║
║    python run.py                           # 完整更新         ║
║    python run.py --collect-only            # 仅收集统计       ║
║    python run.py --full --git-commit       # 完整更新并提交   ║
║    python run.py --status                  # 查看状态         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(help_text)


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="项目统计自动更新系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python run.py                           # 执行完整更新
  python run.py --collect-only            # 仅收集统计
  python run.py --full --git-commit       # 完整更新并提交到Git
        """
    )
    
    parser.add_argument("--full", action="store_true", help="执行完整更新流程（默认）")
    parser.add_argument("--collect-only", action="store_true", help="仅收集统计")
    parser.add_argument("--dashboard-only", action="store_true", help="仅生成仪表盘")
    parser.add_argument("--readme-only", action="store_true", help="仅更新README")
    parser.add_argument("--tracking-only", action="store_true", help="仅更新PROJECT-TRACKING")
    parser.add_argument("--weekly-only", action="store_true", help="仅生成周报")
    parser.add_argument("--git-commit", action="store_true", help="自动提交变更到Git")
    parser.add_argument("--status", action="store_true", help="显示系统状态")
    
    args = parser.parse_args()
    
    # 如果没有指定任何选项，默认执行完整更新
    if not any([args.collect_only, args.dashboard_only, args.readme_only, 
                args.tracking_only, args.weekly_only, args.status]):
        args.full = True
    
    # 获取脚本目录
    script_dir = Path(__file__).parent
    config_path = script_dir / "config.json"
    
    # 创建运行器
    runner = StatsUpdateRunner(str(config_path))
    
    # 处理状态查询
    if args.status:
        runner.show_status()
        return 0
    
    # 执行相应任务
    success = True
    
    if args.full:
        success = runner.run_full_update(git_commit=args.git_commit)
    elif args.collect_only:
        success = runner.run_script("stats-collector.py", "收集项目统计")
    elif args.dashboard_only:
        success = runner.run_script("dashboard-generator.py", "生成统计仪表盘")
    elif args.readme_only:
        success = runner.run_script("readme-updater.py", "更新README.md")
    elif args.tracking_only:
        success = runner.run_script("tracking-updater.py", "更新PROJECT-TRACKING.md")
    elif args.weekly_only:
        success = runner.run_script("weekly-report.py", "生成周报")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
