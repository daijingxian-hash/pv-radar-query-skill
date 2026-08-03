[CmdletBinding()]
param(
    [string]$BaseUrl = "http://172.26.198.15:8787",
    [string]$Channel = "",
    [string]$To = ""
)

$ErrorActionPreference = "Stop"
$skillRoot = Split-Path -Parent $PSScriptRoot
$jobName = "PV Radar 每日17:00日报"

if (-not (Get-Command openclaw -ErrorAction SilentlyContinue)) {
    throw "未找到 openclaw 命令。请先确认 OpenClaw CLI 已加入 PATH。"
}

# Keep installation idempotent: do not create a second copy of the same digest job.
$existing = @()
try {
    $raw = (& openclaw cron list --json 2>$null | Out-String).Trim()
    if ($raw) {
        $parsed = $raw | ConvertFrom-Json
        if ($parsed -is [array]) { $existing = @($parsed) }
        elseif ($parsed.jobs) { $existing = @($parsed.jobs) }
        else { $existing = @($parsed) }
    }
} catch { }
if ($existing | Where-Object { $_.name -eq $jobName }) {
    Write-Output "日报定时任务已存在：$jobName"
    exit 0
}

$command = "python scripts/daily_digest.py --base-url `"$BaseUrl`""
$args = @(
    "cron", "add", "0 17 * * *",
    "--name", $jobName,
    "--command", $command,
    "--command-cwd", $skillRoot,
    "--session", "isolated",
    "--announce",
    "--tz", "Asia/Shanghai"
)
if ($Channel) { $args += @("--channel", $Channel) }
if ($To) { $args += @("--to", $To) }

& openclaw @args
if ($LASTEXITCODE -ne 0) { throw "创建 PV Radar 日报定时任务失败。" }
Write-Output "已创建：每天 17:00（Asia/Shanghai）推送 PV Radar 日报。"
