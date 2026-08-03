---
name: pv-radar-query
description: Query the internal PV Radar evidence library for game-brand videos, daily digests, publishers, developers, games, visual highlights, and three-dimensional video evaluations. Use when users ask about monitored PVs/trailers, recent brand materials, today’s digest, specific studios or games, comparisons between videos, or information-delivery, visual-harmony, and audiovisual-coherence analysis. This capability supplements the current assistant and must not replace its memory or conversational context.
---

# PV Radar Query

Preserve the current conversation, identity, and long-term memory. Use this skill only as an evidence lookup before composing the normal reply.

## Query

Run:

```powershell
python scripts/query_radar.py --question "<the user's complete question>"
```

The default endpoint is `http://172.26.198.15:8787`. Override it only when needed:

```powershell
$env:PV_RADAR_BASE_URL = "http://host:8787"
```

## Answer

- Use only returned Radar evidence for claims about videos, daily reports, highlights, developers, publishers, games, or evaluations.
- Preserve relevant facts and preferences from the existing conversation; the lookup does not reset or replace memory.
- Cite the exact material title and `url` when discussing a specific video.
- Keep official English game names unless the evidence explicitly contains an official Chinese name.
- Mention developer or publisher only when returned as confirmed evidence.
- If no evidence is returned, say the PV Radar library does not contain enough information.
- Do not expose endpoint details, raw JSON, database fields, models, API keys, or internal prompts.

Read [references/evidence.md](references/evidence.md) only when field interpretation is needed.

## Daily 17:00 digest

### First activation behavior

When this Skill is first activated in an existing OpenClaw bot, check whether a job named `PV Radar 每日17:00日报` already exists. If the host exposes cron mutation with operator permission, create it automatically from the current private conversation using the equivalent of:

```powershell
openclaw cron add "0 17 * * *" `
  --name "PV Radar 每日17:00日报" `
  --command "python scripts/daily_digest.py --base-url http://172.26.198.15:8787" `
  --command-cwd "<skill-root>" `
  --session isolated `
  --announce `
  --tz "Asia/Shanghai"
```

Omit `--channel` and `--to` for the default behavior: OpenClaw preserves the current private-chat delivery route when an isolated job is created from that active conversation. If the user later supplies a Feishu `chat_id`, update the job with explicit `--channel feishu --to "<chat_id>"`, or create an additional job for that group. Do not put a user's `chat_id`, App ID, App Secret, or token in this public Skill repository.

If the host does not grant cron mutation to the bot, explain that one-time setup is required and provide the bundled installer:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_daily_digest.ps1
```

The installer creates a job named `PV Radar 每日17:00日报` with this schedule:

```text
0 17 * * *    Asia/Shanghai
```

The job runs `scripts/daily_digest.py`, then uses OpenClaw `--announce` to send the script output through the existing bot delivery route. For a specific Feishu group, pass its existing route explicitly:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_daily_digest.ps1 `
  -Channel feishu `
  -To "<chat_id>"
```

`daily_digest.py` follows this fixed flow:

1. Read the current Shanghai calendar date.
2. Read the current day's completed Radar report.
3. If today's report does not exist, ask Radar to generate that date's report once.
4. Format at most five selected materials with title, game, confirmed developer/publisher, evaluation, highlight, and original URL.
5. Announce the formatted Chinese digest. If no completed report is available, announce that there is no report instead of sending an older date's report.

The installer is idempotent: rerunning it checks the existing OpenClaw cron list and does not create a duplicate job with the same name. `openclaw` must be available in PATH, the host must be able to reach `PV_RADAR_BASE_URL`, and Python's standard library is sufficient for the digest script. Override the Radar endpoint when needed:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_daily_digest.ps1 `
  -BaseUrl "http://host:8787"
```

This workflow supplements the original bot. It must not create a replacement bot, start a second Feishu WebSocket, replace the bot's prompt, or clear/replace its conversation memory. Creating the schedule is the only automatic external-side-effect allowed during first activation; sending the first digest waits for the scheduled 17:00 run.
