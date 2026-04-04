#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务调度器 (Scheduler)

功能:
    - 支持定时执行统计更新任务
    - 支持Daily/Weekly调度
    - 支持后台运行
    - 支持Windows任务计划集成

作者: AnalysisDataFlow Project
版本: 1.0.0

用法:
    python scheduler.py [command]

命令:
    run         启动调度器（前台运行）
    run-daemon  启动调度器（后台运行）
    daily       立即执行每日任务
    weekly      立即执行每周任务
    install     安装Windows任务计划
    uninstall   卸载Windows任务计划
    status      显示调度器状态
"""

import sys
import time
import subprocess
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# 尝试导入schedule库，如果没有则使用简单实现
try:
    import schedule
    HAS_SCHEDULE = True
except ImportError:
    HAS_SCHEDULE = False
    print("⚠️  schedule库未安装，使用内置简单调度器")
    print("   安装命令: pip install schedule")


class TaskScheduler:
    """任务调度器"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化调度器
        
        Args:
            config_path: 配置文件路径
        """
        self.script_dir = Path(__file__).parent
        self.config = self._load_config(config_path)
        self.running = False
        
        # 调度配置
        schedule_config = self.config.get("schedule", {})
        self.daily_time = schedule_config.get("daily_stats_time", "06:00")
        self.weekly_day = schedule_config.get("weekly_report_day", "Sunday")
        self.weekly_time = schedule_config.get("weekly_report_time", "23:00")
        
    def _load_config(self, config_path: str) -> dict:
        """加载配置文件"""
        try:
            with open(self.script_dir / config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "schedule": {
                    "daily_stats_time": "06:00",
                    "weekly_report_day": "Sunday",
                    "weekly_report_time": "23:00"
                }
            }
    
    def run_daily_task(self):
        """运行每日任务"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🌅 执行每日统计更新")
        
        # 运行主更新脚本
        result = subprocess.run(
            [sys.executable, str(self.script_dir / "run.py"), "--full"],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print("✅ 每日任务完成")
        else:
            print(f"❌ 每日任务失败: {result.stderr}")
        
        return result.returncode == 0
    
    def run_weekly_task(self):
        """运行每周任务"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📅 执行周报生成")
        
        # 先生成周报
        result1 = subprocess.run(
            [sys.executable, str(self.script_dir / "weekly-report.py")],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # 然后执行完整更新
        result2 = subprocess.run(
            [sys.executable, str(self.script_dir / "run.py"), "--full"],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result1.returncode == 0 and result2.returncode == 0:
            print("✅ 每周任务完成")
        else:
            print(f"❌ 每周任务部分失败")
        
        return result1.returncode == 0 and result2.returncode == 0
    
    def setup_schedule(self):
        """设置调度计划"""
        if not HAS_SCHEDULE:
            print("⚠️  schedule库未安装，无法使用高级调度功能")
            print("   请运行: pip install schedule")
            return False
        
        # 每日任务
        schedule.every().day.at(self.daily_time).do(self.run_daily_task)
        print(f"📅 已设置每日任务: {self.daily_time}")
        
        # 每周任务
        day_map = {
            "Monday": schedule.every().monday,
            "Tuesday": schedule.every().tuesday,
            "Wednesday": schedule.every().wednesday,
            "Thursday": schedule.every().thursday,
            "Friday": schedule.every().friday,
            "Saturday": schedule.every().saturday,
            "Sunday": schedule.every().sunday,
        }
        
        if self.weekly_day in day_map:
            day_map[self.weekly_day].at(self.weekly_time).do(self.run_weekly_task)
            print(f"📅 已设置每周任务: {self.weekly_day} {self.weekly_time}")
        
        return True
    
    def run_forever(self):
        """持续运行调度器"""
        if not HAS_SCHEDULE:
            self.run_simple_scheduler()
            return
        
        if not self.setup_schedule():
            return
        
        self.running = True
        print(f"\n🚀 调度器已启动，按 Ctrl+C 停止")
        print(f"   每日任务: {self.daily_time}")
        print(f"   每周任务: {self.weekly_day} {self.weekly_time}\n")
        
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # 每分钟检查一次
        except KeyboardInterrupt:
            print("\n👋 调度器已停止")
            self.running = False
    
    def run_simple_scheduler(self):
        """简单调度器（无schedule库时使用）"""
        self.running = True
        print(f"\n🚀 简单调度器已启动")
        print(f"   注意: 安装schedule库可获得更精确的调度")
        print(f"   每日任务: {self.daily_time}")
        print(f"   每周任务: {self.weekly_day} {self.weekly_time}\n")
        
        # 解析时间
        daily_hour, daily_minute = map(int, self.daily_time.split(':'))
        weekly_hour, weekly_minute = map(int, self.weekly_time.split(':'))
        
        last_daily_date = None
        last_weekly_week = None
        
        try:
            while self.running:
                now = datetime.now()
                
                # 检查每日任务
                if (now.hour == daily_hour and now.minute == daily_minute and 
                    last_daily_date != now.date()):
                    self.run_daily_task()
                    last_daily_date = now.date()
                
                # 检查每周任务
                current_week = now.isocalendar()[1]
                if (now.strftime("%A") == self.weekly_day and 
                    now.hour == weekly_hour and now.minute == weekly_minute and
                    last_weekly_week != current_week):
                    self.run_weekly_task()
                    last_weekly_week = current_week
                
                time.sleep(30)  # 每30秒检查一次
                
        except KeyboardInterrupt:
            print("\n👋 调度器已停止")
            self.running = False
    
    def install_windows_task(self):
        """安装Windows任务计划"""
        if sys.platform != "win32":
            print("❌ Windows任务计划仅在Windows平台可用")
            return False
        
        try:
            import win32com.client
            
            # 创建调度任务
            scheduler = win32com.client.Dispatch("Schedule.Service")
            scheduler.Connect()
            root_folder = scheduler.GetFolder("\\")
            
            task_def = scheduler.NewTask(0)
            
            # 设置任务信息
            col_tasks = root_folder.GetTasks(0)
            for task in col_tasks:
                if task.Name == "AnalysisDataFlow Stats Update":
                    root_folder.DeleteTask("AnalysisDataFlow Stats Update", 0)
                    print("🗑️  已删除旧任务")
            
            # 创建触发器（每日）
            trigger = task_def.Triggers.Create(2)  # 每日触发器
            trigger.StartBoundary = datetime.now().strftime("%Y-%m-%dT") + self.daily_time + ":00"
            trigger.Enabled = True
            
            # 设置操作
            action = task_def.Actions.Create(0)  # 执行操作
            action.Path = sys.executable
            action.Arguments = f'"{self.script_dir / "run.py"}" --full'
            action.WorkingDirectory = str(self.script_dir)
            
            # 设置任务设置
            task_def.RegistrationInfo.Description = "AnalysisDataFlow项目统计自动更新"
            task_def.Settings.Enabled = True
            task_def.Settings.AllowDemandStart = True
            
            # 注册任务
            root_folder.RegisterTaskDefinition(
                "AnalysisDataFlow Stats Update",
                task_def,
                6,  # CREATE_OR_UPDATE
                None,  # 当前用户
                None,  # 无密码
                3,  # 使用当前用户登录
                None
            )
            
            print("✅ Windows任务计划已安装")
            print("   任务名称: AnalysisDataFlow Stats Update")
            print(f"   执行时间: 每日 {self.daily_time}")
            return True
            
        except ImportError:
            print("❌ 需要安装pywin32库: pip install pywin32")
            return False
        except Exception as e:
            print(f"❌ 安装失败: {e}")
            return False
    
    def uninstall_windows_task(self):
        """卸载Windows任务计划"""
        if sys.platform != "win32":
            print("❌ Windows任务计划仅在Windows平台可用")
            return False
        
        try:
            import win32com.client
            
            scheduler = win32com.client.Dispatch("Schedule.Service")
            scheduler.Connect()
            root_folder = scheduler.GetFolder("\\")
            
            root_folder.DeleteTask("AnalysisDataFlow Stats Update", 0)
            print("✅ Windows任务计划已卸载")
            return True
            
        except Exception as e:
            print(f"❌ 卸载失败: {e}")
            return False
    
    def show_status(self):
        """显示调度器状态"""
        print("=" * 60)
        print("📅 任务调度器状态")
        print("=" * 60)
        print(f"\n调度配置:")
        print(f"  每日任务时间: {self.daily_time}")
        print(f"  每周任务时间: {self.weekly_day} {self.weekly_time}")
        print(f"  schedule库: {'✅ 已安装' if HAS_SCHEDULE else '⚠️ 未安装'}")
        
        # 检查Windows任务
        if sys.platform == "win32":
            try:
                import win32com.client
                scheduler = win32com.client.Dispatch("Schedule.Service")
                scheduler.Connect()
                root_folder = scheduler.GetFolder("\\")
                
                col_tasks = root_folder.GetTasks(0)
                task_exists = any(task.Name == "AnalysisDataFlow Stats Update" for task in col_tasks)
                
                print(f"\nWindows任务计划:")
                print(f"  状态: {'✅ 已安装' if task_exists else '❌ 未安装'}")
            except:
                print(f"\nWindows任务计划: 无法检测")
        
        print("\n下次执行时间:")
        
        # 计算下次执行时间
        now = datetime.now()
        daily_hour, daily_minute = map(int, self.daily_time.split(':'))
        next_daily = now.replace(hour=daily_hour, minute=daily_minute, second=0, microsecond=0)
        if next_daily <= now:
            next_daily += timedelta(days=1)
        print(f"  每日任务: {next_daily.strftime('%Y-%m-%d %H:%M')}")
        
        # 计算下次周任务
        days_ahead = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                      "Friday", "Saturday", "Sunday"].index(self.weekly_day) - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        next_weekly = now + timedelta(days=days_ahead)
        weekly_hour, weekly_minute = map(int, self.weekly_time.split(':'))
        next_weekly = next_weekly.replace(hour=weekly_hour, minute=weekly_minute)
        print(f"  每周任务: {next_weekly.strftime('%Y-%m-%d %H:%M')}")
        
        print("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="任务调度器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scheduler.py run          # 启动调度器（前台）
  python scheduler.py daily        # 立即执行每日任务
  python scheduler.py weekly       # 立即执行每周任务
  python scheduler.py install      # 安装Windows任务计划
  python scheduler.py uninstall    # 卸载Windows任务计划
  python scheduler.py status       # 显示状态
        """
    )
    
    parser.add_argument(
        "command",
        choices=["run", "run-daemon", "daily", "weekly", "install", "uninstall", "status"],
        nargs="?",
        default="status",
        help="要执行的命令"
    )
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent
    config_path = script_dir / "config.json"
    
    scheduler = TaskScheduler(str(config_path))
    
    if args.command == "run":
        scheduler.run_forever()
    elif args.command == "run-daemon":
        print("🚀 启动后台调度器...")
        print("   提示: 在Windows上建议使用 'install' 命令创建系统任务")
        scheduler.run_forever()
    elif args.command == "daily":
        scheduler.run_daily_task()
    elif args.command == "weekly":
        scheduler.run_weekly_task()
    elif args.command == "install":
        scheduler.install_windows_task()
    elif args.command == "uninstall":
        scheduler.uninstall_windows_task()
    elif args.command == "status":
        scheduler.show_status()
    
    return 0


if __name__ == "__main__":
    exit(main())
