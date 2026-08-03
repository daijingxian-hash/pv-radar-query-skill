# 每日 17:00 日报

日报由 OpenClaw 的持久化 cron 任务触发，时区固定为 `Asia/Shanghai`，表达式为 `0 17 * * *`。

安装 Skill 后执行一次：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_daily_digest.ps1
```

如果需要明确投递到某个飞书群：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_daily_digest.ps1 `
  -Channel feishu `
  -To "<chat_id>"
```

脚本创建的是原 OpenClaw 机器人的定时任务，不创建新的机器人、长连接或会话；`--announce` 会把脚本输出投递到原机器人当前配置的目标渠道。

日报脚本只读取 PV Radar 已完成的日报证据；当天没有完成日报时，会发送“暂无可推送的已完成日报”，不会拿旧日期内容冒充当天日报。
