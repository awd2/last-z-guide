import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

OUT_DIR = "content/gsc"
API_URL = "https://searchconsole.googleapis.com/webmasters/v3"
TOKEN_URL = "https://oauth2.googleapis.com/token"


def get_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing env var: {name}")
    return value


def post_json(url: str, data: dict, headers: dict | None = None) -> dict:
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers or {}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def exchange_refresh_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    payload = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        TOKEN_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    access_token = data.get("access_token")
    if not access_token:
        raise RuntimeError(f"Failed to refresh token: {data}")
    return access_token


def query_search_analytics(site_url: str, access_token: str, dimensions: list[str], rows: int) -> list[dict]:
    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=27)
    payload = {
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "dimensions": dimensions,
        "rowLimit": rows,
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    url = f"{API_URL}/sites/{urllib.parse.quote(site_url, safe='')}/searchAnalytics/query"
    data = post_json(url, payload, headers)
    return data.get("rows", [])


def render_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return lines


def main() -> int:
    client_id = get_env("GSC_CLIENT_ID")
    client_secret = get_env("GSC_CLIENT_SECRET")
    refresh_token = get_env("GSC_REFRESH_TOKEN")
    site_url = get_env("GSC_PROPERTY")
    rows_limit = int(os.getenv("GSC_ROWS", "100"))

    access_token = exchange_refresh_token(client_id, client_secret, refresh_token)

    queries = query_search_analytics(site_url, access_token, ["query"], rows_limit)
    pages = query_search_analytics(site_url, access_token, ["page"], rows_limit)

    end_date = date.today() - timedelta(days=1)
    start_date = end_date - timedelta(days=27)

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"{end_date.isoformat()}-gsc-report.md")

    lines = []
    lines.append(f"# GSC Daily Report — {end_date.isoformat()}")
    lines.append("")
    lines.append(f"- Property: `{site_url}`")
    lines.append(f"- Date range: {start_date.isoformat()} → {end_date.isoformat()}")
    lines.append(f"- Rows: {rows_limit}")
    lines.append("")

    lines.append("## Queries (top by impressions)")
    lines.append("")
    q_rows = []
    for r in queries:
        q = r.get("keys", [""])[0]
        clicks = f'{r.get("clicks", 0):.0f}'
        impressions = f'{r.get("impressions", 0):.0f}'
        ctr = f'{r.get("ctr", 0) * 100:.2f}%'
        position = f'{r.get("position", 0):.2f}'
        q_rows.append([q, clicks, impressions, ctr, position])
    lines += render_table(["Query", "Clicks", "Impr.", "CTR", "Pos."], q_rows)
    lines.append("")

    lines.append("## Pages (top by impressions)")
    lines.append("")
    p_rows = []
    for r in pages:
        p = r.get("keys", [""])[0]
        clicks = f'{r.get("clicks", 0):.0f}'
        impressions = f'{r.get("impressions", 0):.0f}'
        ctr = f'{r.get("ctr", 0) * 100:.2f}%'
        position = f'{r.get("position", 0):.2f}'
        p_rows.append([p, clicks, impressions, ctr, position])
    lines += render_table(["Page", "Clicks", "Impr.", "CTR", "Pos."], p_rows)
    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Wrote {out_path} with {len(queries)} queries and {len(pages)} pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
