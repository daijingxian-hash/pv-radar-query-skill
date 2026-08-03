from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone


DEFAULT_BASE_URL = os.getenv("PV_RADAR_BASE_URL", "http://172.26.198.15:8787")


def shanghai_today() -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=8)).date().isoformat()


def request_json(base_url: str, path: str, *, method: str = "GET", payload: dict | None = None) -> object:
    body = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json; charset=utf-8"
    request = urllib.request.Request(base_url.rstrip("/") + path, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def get_today_report(base_url: str, report_date: str, generate: bool) -> dict | None:
    if report_date == shanghai_today():
        value = request_json(base_url, "/api/reports/today")
    else:
        reports = request_json(base_url, "/api/reports?limit=30")
        value = next((item for item in reports if isinstance(item, dict) and str(item.get("report_date") or "") == report_date), None) if isinstance(reports, list) else None
    if isinstance(value, dict) and value.get("report"):
        return value
    if not generate:
        return None
    value = request_json(
        base_url,
        "/api/reports/generate",
        method="POST",
        payload={"date": report_date, "force": False},
    )
    return value if isinstance(value, dict) and value.get("report") else None


def confirmed_label(item: dict, *keys: str) -> str:
    for key in keys:
        value = str(item.get(key) or "").strip()
        if value:
            return value
    return ""


def format_digest(record: dict, max_items: int) -> str:
    report = record.get("report") if isinstance(record.get("report"), dict) else record
    report_date = str(report.get("date") or record.get("report_date") or shanghai_today())
    lines = [f"PV RADAR｜日报｜{report_date}"]
    overview = str(report.get("overview") or "").strip()
    if overview:
        lines += ["", overview]
    items = report.get("items") if isinstance(report.get("items"), list) else []
    if not items:
        game_items = report.get("gameItems") if isinstance(report.get("gameItems"), list) else []
        non_game_items = report.get("nonGameItems") if isinstance(report.get("nonGameItems"), list) else []
        items = game_items + non_game_items
    for index, item in enumerate(items[: max(1, max_items)], 1):
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or "未命名素材").strip()
        kind = "非游戏" if item.get("contentKind") == "non_game" else "游戏"
        lines += ["", f"{index}. [{kind}] {title}"]
        game = confirmed_label(item, "gameName", "game")
        developer = confirmed_label(item, "developerName", "developer")
        publisher = confirmed_label(item, "publisherName", "publisher")
        if game:
            lines.append(f"游戏：{game}")
        if developer:
            lines.append(f"开发商：{developer}")
        if publisher:
            lines.append(f"发行商：{publisher}")
        why = str(item.get("why") or item.get("summary") or "").strip()
        watch_point = str(item.get("watchPoint") or "").strip()
        if why:
            lines.append(f"评价：{why}")
        if watch_point:
            lines.append(f"高光：{watch_point}")
        url = str(item.get("url") or "").strip()
        if url:
            lines.append(f"原页面：{url}")
    if len(lines) == 1:
        lines.append("\n今日暂无可推送的已完成日报。")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the PV Radar daily digest for OpenClaw delivery.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--date", default=shanghai_today())
    parser.add_argument("--max-items", type=int, default=5)
    parser.add_argument("--no-generate", action="store_true", help="Do not ask Radar to generate the report when today's report is missing")
    args = parser.parse_args()
    try:
        record = get_today_report(args.base_url, args.date, not args.no_generate)
        if not record:
            print(f"PV RADAR｜日报｜{args.date}\n\n今日暂无可推送的已完成日报。")
            return 0
        print(format_digest(record, args.max_items))
        return 0
    except (OSError, urllib.error.URLError, json.JSONDecodeError, ValueError) as exc:
        print(f"PV RADAR 日报暂时无法生成：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
