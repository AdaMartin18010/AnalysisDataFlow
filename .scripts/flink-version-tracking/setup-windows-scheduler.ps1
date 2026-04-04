#Requires -RunAsAdministrator
<#
.SYNOPSIS
    Flink Version Tracker - Windows 任务计划程序设置脚本

.DESCRIPTION
    此脚本在 Windows 任务计划程序中创建 Flink 版本跟踪的定时任务

.EXAMPLE
    .\setup-windows-scheduler.ps1

.NOTES
    需要管理员权限运行
    作者: Flink Version Tracker
    版本: 1.0.0
#>

[CmdletBinding()]
param(
    [string]$ScriptPath = "E:\_src\AnalysisDataFlow\.scripts\flink-version-tracking",
    [string]$PythonPath = "python",
    [string]$TaskPrefix = "FlinkTracker"
)

# 检查管理员权限
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "此脚本需要管理员权限运行。请以管理员身份运行 PowerShell。"
    exit 1
}

# 验证路径
if (-not (Test-Path $ScriptPath)) {
    Write-Error "脚本路径不存在: $ScriptPath"
    exit 1
}

# 验证 Python
$pythonExe = Get-Command $PythonPath -ErrorAction SilentlyContinue
if (-not $pythonExe) {
    # 尝试常见路径
    $possiblePaths = @(
        "C:\Python311\python.exe",
        "C:\Python310\python.exe",
        "C:\Python39\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $PythonPath = $path
            Write-Host "找到 Python: $PythonPath" -ForegroundColor Green
            break
        }
    }
}

Write-Host "Flink Version Tracker - Windows 任务计划程序设置" -ForegroundColor Cyan
Write-Host "=" * 60
Write-Host "脚本路径: $ScriptPath"
Write-Host "Python 路径: $PythonPath"
Write-Host "任务前缀: $TaskPrefix"
Write-Host ""

# 创建任务函数
function New-FlinkTrackerTask {
    param(
        [Parameter(Mandatory = $true)]
        [string]$TaskName,
        
        [Parameter(Mandatory = $true)]
        [string]$ScriptName,
        
        [Parameter(Mandatory = $true)]
        [ValidateSet("Hourly", "Daily", "Weekly", "AtLogon")]
        [string]$Schedule,
        
        [Parameter(Mandatory = $false)]
        [int]$Interval = 1,
        
        [Parameter(Mandatory = $false)]
        [string]$AtTime = "09:00",
        
        [Parameter(Mandatory = $false)]
        [string]$DaysOfWeek = "Monday",
        
        [Parameter(Mandatory = $false)]
        [string]$Description = ""
    )
    
    $fullTaskName = "$TaskPrefix-$TaskName"
    $scriptFullPath = Join-Path $ScriptPath $ScriptName
    
    # 检查脚本是否存在
    if (-not (Test-Path $scriptFullPath)) {
        Write-Warning "脚本不存在: $scriptFullPath"
        return
    }
    
    # 删除现有任务
    $existingTask = Get-ScheduledTask -TaskName $fullTaskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "删除现有任务: $fullTaskName" -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $fullTaskName -Confirm:$false
    }
    
    # 创建操作
    $action = New-ScheduledTaskAction `
        -Execute $PythonPath `
        -Argument $scriptFullPath `
        -WorkingDirectory $ScriptPath
    
    # 创建触发器
    switch ($Schedule) {
        "Hourly" {
            $trigger = New-ScheduledTaskTrigger `
                -Once -At (Get-Date) `
                -RepetitionInterval (New-TimeSpan -Hours $Interval) `
                -RepetitionDuration ([System.TimeSpan]::MaxValue)
        }
        "Daily" {
            $trigger = New-ScheduledTaskTrigger -Daily -At $AtTime
        }
        "Weekly" {
            $dayMap = @{
                "Monday" = 1; "Tuesday" = 2; "Wednesday" = 3; "Thursday" = 4
                "Friday" = 5; "Saturday" = 6; "Sunday" = 0
            }
            $dayValue = $dayMap[$DaysOfWeek]
            $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $dayValue -At $AtTime
        }
        "AtLogon" {
            $trigger = New-ScheduledTaskTrigger -AtLogon
        }
    }
    
    # 任务设置
    $settings = New-ScheduledTaskSettingsSet `
        -AllowStartIfOnBatteries `
        -DontStopIfGoingOnBatteries `
        -StartWhenAvailable `
        -RunOnlyIfNetworkAvailable `
        -WakeToRun:$false `
        -MultipleInstances IgnoreNew
    
    # 任务主体 (以最高权限运行)
    $principal = New-ScheduledTaskPrincipal `
        -UserId $env:USERNAME `
        -LogonType Interactive `
        -RunLevel Highest
    
    # 注册任务
    try {
        Register-ScheduledTask `
            -TaskName $fullTaskName `
            -Action $action `
            -Trigger $trigger `
            -Settings $settings `
            -Principal $principal `
            -Description ($Description -or "Flink Version Tracking - $TaskName") `
            -Force
        
        Write-Host "✅ 已创建任务: $fullTaskName" -ForegroundColor Green
        
        # 显示下次运行时间
        $task = Get-ScheduledTask -TaskName $fullTaskName
        $nextRun = (Get-ScheduledTaskInfo -TaskName $fullTaskName).NextRunTime
        if ($nextRun) {
            Write-Host "   下次运行: $nextRun" -ForegroundColor Gray
        }
    }
    catch {
        Write-Error "创建任务失败 ${fullTaskName}: $_"
    }
    
    Write-Host ""
}

# 创建日志目录
$logDir = Join-Path $ScriptPath "logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    Write-Host "创建日志目录: $logDir" -ForegroundColor Green
}

# ==================== 创建定时任务 ====================

# 任务 1: 检查 FLIP 状态 (每 6 小时)
New-FlinkTrackerTask `
    -TaskName "CheckFLIP" `
    -ScriptName "fetch-flip-status.py" `
    -Schedule "Hourly" `
    -Interval 6 `
    -Description "每 6 小时检查 Flink FLIP 状态更新"

# 任务 2: 检查新版本 (每 12 小时)
New-FlinkTrackerTask `
    -TaskName "CheckReleases" `
    -ScriptName "check-new-releases.py" `
    -Schedule "Hourly" `
    -Interval 12 `
    -Description "每 12 小时检查 Flink 新版本发布"

# 任务 3: 更新文档 (每日 08:00)
New-FlinkTrackerTask `
    -TaskName "UpdateDocs" `
    -ScriptName "update-version-docs.py" `
    -Schedule "Daily" `
    -AtTime "08:00" `
    -Description "每日 08:00 自动更新版本跟踪文档"

# 任务 4: 发送通知 (每日 09:00)
New-FlinkTrackerTask `
    -TaskName "SendNotification" `
    -ScriptName "notify-changes.py" `
    -Schedule "Daily" `
    -AtTime "09:00" `
    -Description "每日 09:00 发送变更通知摘要"

# ==================== 完成 ====================

Write-Host "=" * 60
Write-Host "所有任务已创建完成!" -ForegroundColor Cyan
Write-Host ""
Write-Host "管理命令:" -ForegroundColor Yellow
Write-Host "  查看所有任务:"
Write-Host "    Get-ScheduledTask | Where-Object { `$_.TaskName -like '${TaskPrefix}-*' }"
Write-Host ""
Write-Host "  手动运行任务:"
Write-Host "    Start-ScheduledTask -TaskName '${TaskPrefix}-CheckFLIP'"
Write-Host ""
Write-Host "  停止任务:"
Write-Host "    Stop-ScheduledTask -TaskName '${TaskPrefix}-CheckFLIP'"
Write-Host ""
Write-Host "  删除所有任务:"
Write-Host "    Get-ScheduledTask | Where-Object { `$_.TaskName -like '${TaskPrefix}-*' } | Unregister-ScheduledTask -Confirm:`$false"
Write-Host ""
Write-Host "  查看任务详情:"
Write-Host "    Get-ScheduledTaskInfo -TaskName '${TaskPrefix}-CheckFLIP'"
Write-Host ""

# 显示已创建的任务
Write-Host "已创建的任务列表:" -ForegroundColor Green
Get-ScheduledTask | Where-Object { $_.TaskName -like "${TaskPrefix}-*" } | 
    Select-Object TaskName, State, NextRunTime | 
    Format-Table -AutoSize
