# PV Radar Query Skill

为现有 OpenClaw／飞书机器人附加 PV Radar 素材库查询能力。该 Skill 只读取素材证据，不接管机器人身份、对话上下文或长期记忆。

> This skill adds read-only PV Radar evidence lookup to an existing assistant without replacing its identity, conversation context, or memory.

## 能做什么

- 查询近期游戏品牌向 PV、宣传片及每日摘要
- 按厂商、开发商、发行商、游戏或时间范围检索素材
- 返回视频画面高光与视频评价证据
- 比较不同视频的信息传达、视觉搭配和音画协调
- 提供原始素材标题与平台链接，便于机器人组织回答

PV Radar 当前会排除竖屏、角色／英雄 PV、采访、幕后花絮、普通短切版及纯实机内容。

## 工作方式

```text
用户问题
   ↓
原 OpenClaw／飞书机器人（保留原有记忆）
   ↓ 需要素材证据时调用
pv-radar-query Skill
   ↓ HTTP，只读
PV Radar 素材库
```

这个仓库仅包含查询 Skill，不包含 PV Radar 服务端、数据库、素材文件、模型密钥或飞书凭证。

## 安装

将本仓库克隆或下载到原 OpenClaw 实例可识别的 Skills 目录中，仓库根目录必须保留 `SKILL.md`：

```bash
git clone https://github.com/daijingxian-hash/pv-radar-query-skill.git pv-radar-query
```

随后按当前 OpenClaw 版本的方式重新加载 Skills。请把它安装到原机器人，而不是新建一个独立机器人；原机器人的提示词、记忆和飞书 WebSocket 配置应保持不变。

## 网络配置

Skill 默认连接当前内部 PV Radar 服务。OpenClaw 所在设备需要能够访问运行 Radar 的电脑和 `8787` 端口。

如服务地址发生变化，可通过环境变量覆盖：

### PowerShell

```powershell
$env:PV_RADAR_BASE_URL = "http://host:8787"
```

### Bash

```bash
export PV_RADAR_BASE_URL="http://host:8787"
```

不要把 API Key、飞书 App Secret 或其他凭证提交到本仓库。

## 测试

Skill 只使用 Python 标准库，无需安装额外依赖：

```bash
python scripts/query_radar.py --question "最近有哪些 HoYoverse 品牌向素材？"
```

也可以显式指定地址：

```bash
python scripts/query_radar.py \
  --base-url "http://host:8787" \
  --question "查询最近一周已完成分析的品牌向视频"
```

成功时脚本会输出 JSON 证据；如果显示 `PV Radar unavailable`，请检查 Radar 服务是否运行、设备是否处于可互通网络，以及 Windows 防火墙是否允许 `8787` 端口。

## 示例问题

- 最近一周有哪些值得关注的品牌向素材？
- 最近有哪些 HoYoverse 发布的视频？
- 对比这两支视频的信息传达和音画协调。
- 今天的日报里有哪些高质量素材？
- 某支视频有哪些值得关注的画面高光？

## 仓库结构

```text
pv-radar-query/
├── SKILL.md                    # Skill 触发条件和回答规则
├── agents/openai.yaml          # Skill 界面元数据
├── scripts/query_radar.py      # 只读查询客户端
└── references/evidence.md      # 返回字段解释
```

## 更新

```bash
git pull --ff-only
```

更新后按 OpenClaw 当前版本的方式重新加载 Skills。

## Daily 17:00 digest

The skill includes an idempotent installer for a persistent OpenClaw cron job. Run it once after installing the skill into the existing bot:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install_daily_digest.ps1
```

It schedules `scripts/daily_digest.py` for 17:00 in `Asia/Shanghai` and announces the current day's completed PV Radar report through the bot's existing delivery route. To target a specific Feishu group, pass `-Channel feishu -To "<chat_id>"`.
