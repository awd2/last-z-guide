import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta
from statistics import median

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


def pick_insights(queries: list[dict], pages: list[dict], min_impr: int = 50) -> dict:
    q_rows = []
    for r in queries:
        q = r.get("keys", [""])[0]
        q_rows.append(
            {
                "query": q,
                "clicks": r.get("clicks", 0.0),
                "impr": r.get("impressions", 0.0),
                "ctr": r.get("ctr", 0.0),
                "pos": r.get("position", 0.0),
            }
        )
    p_rows = []
    for r in pages:
        p = r.get("keys", [""])[0]
        p_rows.append(
            {
                "page": p,
                "clicks": r.get("clicks", 0.0),
                "impr": r.get("impressions", 0.0),
                "ctr": r.get("ctr", 0.0),
                "pos": r.get("position", 0.0),
            }
        )

    ctr_values = [r["ctr"] for r in q_rows if r["impr"] >= min_impr]
    ctr_median = median(ctr_values) if ctr_values else 0.0

    def potential(row: dict) -> float:
        pos = row.get("pos", 0.0)
        pos_factor = 1.2 if 4 <= pos <= 10 else 1.0
        return row.get("impr", 0.0) * (1 - row.get("ctr", 0.0)) * pos_factor

    low_ctr_good_pos = [
        r
        for r in q_rows
        if 4 <= r["pos"] <= 10 and r["impr"] >= min_impr and r["ctr"] <= ctr_median
    ]
    low_ctr_good_pos.sort(key=potential, reverse=True)

    high_impr_low_clicks = [
        r for r in q_rows if r["impr"] >= 200 and r["clicks"] <= 5
    ]
    high_impr_low_clicks.sort(key=lambda r: r["impr"], reverse=True)

    quick_wins = [
        r for r in q_rows if 11 <= r["pos"] <= 20 and r["impr"] >= min_impr
    ]
    quick_wins.sort(key=potential, reverse=True)

    page_underperform = [
        r for r in p_rows if r["impr"] >= 200 and r["ctr"] <= ctr_median
    ]
    page_underperform.sort(key=lambda r: r["impr"], reverse=True)

    return {
        "ctr_median": ctr_median,
        "low_ctr_good_pos": low_ctr_good_pos[:15],
        "high_impr_low_clicks": high_impr_low_clicks[:15],
        "quick_wins": quick_wins[:15],
        "page_underperform": page_underperform[:15],
    }


def render_insight_list(rows: list[dict], kind: str) -> list[str]:
    lines = []
    if not rows:
        lines.append("- (no items)")
        return lines
    for r in rows:
        label = r.get("query") if kind == "query" else r.get("page")
        clicks = f'{r.get("clicks", 0):.0f}'
        impr = f'{r.get("impr", 0):.0f}'
        ctr = f'{r.get("ctr", 0) * 100:.2f}%'
        pos = f'{r.get("pos", 0):.2f}'
        lines.append(f"- {label} — {impr} impr, {clicks} clicks, {ctr} CTR, pos {pos}")
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

    insights = pick_insights(queries, pages)
    lines.append("## Insights (auto)")
    lines.append("")
    lines.append(
        f"- CTR median for queries (impr ≥ 50): {insights['ctr_median'] * 100:.2f}%"
    )
    lines.append("")

    lines.append("### Low CTR, good positions (4–10)")
    lines += render_insight_list(insights["low_ctr_good_pos"], "query")
    lines.append("")

    lines.append("### High impressions, low clicks")
    lines += render_insight_list(insights["high_impr_low_clicks"], "query")
    lines.append("")

    lines.append("### Quick wins (positions 11–20)")
    lines += render_insight_list(insights["quick_wins"], "query")
    lines.append("")

    lines.append("### Pages underperforming (high impressions, low CTR)")
    lines += render_insight_list(insights["page_underperform"], "page")
    lines.append("")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # Keep only the latest report file
    for name in os.listdir(OUT_DIR):
        if not name.endswith("-gsc-report.md"):
            continue
        path = os.path.join(OUT_DIR, name)
        if os.path.abspath(path) == os.path.abspath(out_path):
            continue
        os.remove(path)

    print(f"Wrote {out_path} with {len(queries)} queries and {len(pages)} pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
