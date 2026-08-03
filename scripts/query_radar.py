from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def main() -> int:
    parser = argparse.ArgumentParser(description="Query PV Radar evidence without taking over assistant memory.")
    parser.add_argument("--question", required=True)
    parser.add_argument("--base-url", default=os.getenv("PV_RADAR_BASE_URL", "http://172.26.198.15:8787"))
    args = parser.parse_args()
    payload = json.dumps({"question": args.question}, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        args.base_url.rstrip("/") + "/api/assistant/query",
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": f"PV Radar unavailable: {exc}"}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
