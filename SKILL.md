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

After installing this Skill into the existing OpenClaw/Feishu bot, configure the persistent daily digest job once:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_daily_digest.ps1
```

The job runs at 17:00 in `Asia/Shanghai`, reads the current day's completed Radar report, and announces the formatted digest through the existing bot route. If the bot uses a specific Feishu group, pass `-Channel feishu -To "<chat_id>"`. Keep the existing bot session and memory; this Skill must not start a replacement WebSocket bot or create a second conversation.

The installer is idempotent and will not create a duplicate job with the same name. Read [references/daily_digest.md](references/daily_digest.md) for the delivery behavior and troubleshooting notes.
