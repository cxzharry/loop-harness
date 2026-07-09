#!/usr/bin/env python3
"""Render and serve the human review gate for loop-harness contracts."""

from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any


DEFAULT_ARTIFACT_DIR = ".loop-harness"
REVIEW_DIR = "review"
GROUPS = [
    ("metrics", "Metrics"),
    ("criteria", "Criteria"),
    ("benchmark", "Benchmark"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def artifact_root(repo: Path, artifact_dir: str = DEFAULT_ARTIFACT_DIR) -> Path:
    root = repo.resolve()
    if (root / "PRODUCT_LOOP.md").exists() and (root / "criteria").is_dir():
        return root
    return root / artifact_dir


def review_root(repo: Path, artifact_dir: str = DEFAULT_ARTIFACT_DIR) -> Path:
    return artifact_root(repo, artifact_dir) / REVIEW_DIR


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected object JSON: {path}")
    return data


def normalize_candidates(data: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {
        "surface": str(data.get("surface", "")),
        "intent": str(data.get("intent", "")),
        "profiles": [str(item) for item in data.get("profiles", [])],
    }
    for group, _label in GROUPS:
        items: list[dict[str, Any]] = []
        for raw in data.get(group, []):
            if not isinstance(raw, dict):
                continue
            item_id = str(raw.get("id", "")).strip()
            title = str(raw.get("title", "")).strip()
            if not item_id or not title:
                continue
            items.append(
                {
                    "id": item_id,
                    "title": title,
                    "description": str(raw.get("description", "")).strip(),
                    "recommended": bool(raw.get("recommended", False)),
                }
            )
        normalized[group] = items
    return normalized


def write_candidates(repo: Path, candidates_path: Path, artifact_dir: str) -> dict[str, Any]:
    candidates = normalize_candidates(read_json(candidates_path))
    root = review_root(repo, artifact_dir)
    root.mkdir(parents=True, exist_ok=True)
    (root / "evaluation-contract-candidates.json").write_text(
        json.dumps(candidates, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return candidates


def load_saved_candidates(root: Path) -> dict[str, Any]:
    path = root / "evaluation-contract-candidates.json"
    return normalize_candidates(read_json(path))


def row_html(group: str, item: dict[str, Any]) -> str:
    title = str(item["title"])
    display_title = f"{title} (Recommended)" if item["recommended"] else title
    choice = "yes" if item["recommended"] else "no"
    yes_active = " active" if choice == "yes" else ""
    no_active = " active" if choice == "no" else ""
    recommended_class = " recommended" if item["recommended"] else ""
    return f"""
        <div class="item" data-group="{html.escape(group)}" data-id="{html.escape(str(item['id']))}" data-recommended="{str(item['recommended']).lower()}" data-choice="{choice}">
          <div>
            <div class="title{recommended_class}">{html.escape(display_title)}</div>
            <div class="description">{html.escape(str(item.get('description', '')))}</div>
          </div>
          <div class="switch" role="group" aria-label="{html.escape(display_title)}">
            <button class="no{no_active}" type="button">No</button><button class="yes{yes_active}" type="button">Yes</button>
          </div>
        </div>
    """


def group_html(group: str, label: str, candidates: dict[str, Any]) -> str:
    items = candidates.get(group, [])
    selected = sum(1 for item in items if item.get("recommended"))
    rows = "\n".join(row_html(group, item) for item in items)
    return f"""
      <article class="group" data-group="{group}">
        <div class="group-head">
          <div class="group-title">{label}</div>
          <div class="group-count" data-count-for="{group}">{selected} selected</div>
        </div>
        {rows}
      </article>
    """


def render_html(candidates: dict[str, Any]) -> str:
    total = sum(len(candidates.get(group, [])) for group, _label in GROUPS)
    accepted = sum(
        1
        for group, _label in GROUPS
        for item in candidates.get(group, [])
        if item.get("recommended")
    )
    groups = "\n".join(group_html(group, label, candidates) for group, label in GROUPS)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Loop Harness Contract Review</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f3f5f8;
      --panel: #ffffff;
      --panel-soft: #f9fafc;
      --text: #111827;
      --muted: #465363;
      --line: #d8e0ea;
      --line-strong: #c6d0dd;
      --blue: #2557d6;
      --blue-soft: #e7efff;
      --green: #137047;
      --green-soft: #dcf7e9;
      --red: #a43a3a;
      --red-soft: #fde9e9;
      --shadow: 0 18px 40px rgb(20 28 40 / 0.10);
      --radius: 14px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100dvh;
      color: var(--text);
      background: linear-gradient(180deg, #eaf0f7 0, var(--bg) 230px), var(--bg);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }}
    button {{ font: inherit; }}
    .shell {{
      width: min(1220px, calc(100vw - 32px));
      margin: 0 auto;
      padding: 20px 0 84px;
    }}
    .topbar {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 18px;
      align-items: end;
      margin-bottom: 14px;
    }}
    h1 {{
      margin: 0;
      color: #0f1724;
      font-size: 24px;
      line-height: 1.08;
      font-weight: 850;
    }}
    .subtitle {{
      margin: 6px 0 0;
      max-width: 760px;
      color: var(--muted);
      font-size: 14px;
      line-height: 1.35;
    }}
    .meta {{
      display: flex;
      gap: 8px;
      justify-content: flex-end;
      flex-wrap: wrap;
    }}
    .pill {{
      min-height: 30px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 11px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(255, 255, 255, .74);
      color: #273244;
      font-size: 12px;
      font-weight: 780;
      white-space: nowrap;
    }}
    .pill.primary {{
      border-color: #b8c9f7;
      background: var(--blue-soft);
      color: #173f9d;
    }}
    .board {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 12px;
    }}
    .group {{
      overflow: hidden;
      border: 1px solid var(--line-strong);
      border-radius: var(--radius);
      background: var(--panel);
      box-shadow: var(--shadow);
    }}
    .group-head {{
      min-height: 48px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      background: #eef3f8;
    }}
    .group-title {{
      color: #152033;
      font-size: 14px;
      font-weight: 860;
    }}
    .group-count {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 760;
    }}
    .item {{
      display: grid;
      grid-template-columns: 1fr 124px;
      gap: 10px;
      align-items: center;
      min-height: 104px;
      padding: 10px 12px;
      border-bottom: 1px solid #ecf0f4;
      background: var(--panel);
    }}
    .item:last-child {{ border-bottom: 0; }}
    .item:nth-child(odd) {{ background: var(--panel-soft); }}
    .title {{
      color: #111827;
      font-size: 14px;
      line-height: 1.25;
      font-weight: 820;
    }}
    .title.recommended {{ color: #153f9f; }}
    .description {{
      margin-top: 5px;
      color: var(--muted);
      font-size: 12.5px;
      line-height: 1.35;
    }}
    .switch {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      width: 124px;
      height: 48px;
      padding: 4px;
      border: 1px solid var(--line-strong);
      border-radius: 999px;
      background: #edf2f7;
    }}
    .switch button {{
      border: 0;
      border-radius: 999px;
      background: transparent;
      color: #384557;
      font-size: 14px;
      font-weight: 880;
      cursor: pointer;
      transition: background .16s ease, color .16s ease, transform .12s ease;
    }}
    .switch button:focus-visible {{
      outline: 3px solid rgb(37 87 214 / .30);
      outline-offset: 2px;
    }}
    .switch button:active {{ transform: scale(.96); }}
    .switch button.no.active {{
      background: var(--red-soft);
      color: var(--red);
      box-shadow: inset 0 0 0 1px rgb(164 58 58 / .18);
    }}
    .switch button.yes.active {{
      background: var(--green-soft);
      color: var(--green);
      box-shadow: inset 0 0 0 1px rgb(19 112 71 / .18);
    }}
    .footer {{
      position: fixed;
      right: 0;
      bottom: 0;
      left: 0;
      border-top: 1px solid var(--line-strong);
      background: rgb(251 252 253 / .94);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
    }}
    .footer-inner {{
      width: min(1220px, calc(100vw - 32px));
      min-height: 66px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1fr auto;
      align-items: center;
      gap: 14px;
    }}
    .summary {{
      color: var(--muted);
      font-size: 13px;
      font-weight: 680;
    }}
    .summary strong {{ color: var(--text); }}
    .save {{
      min-width: 154px;
      min-height: 46px;
      border: 0;
      border-radius: 999px;
      background: var(--blue);
      color: #fff;
      font-size: 14px;
      font-weight: 880;
      cursor: pointer;
      box-shadow: 0 12px 24px rgb(37 87 214 / .25);
      transition: transform .12s ease, filter .16s ease;
    }}
    .save:hover {{ filter: brightness(.96); }}
    .save:active {{ transform: scale(.98); }}
    @media (max-width: 920px) {{
      .shell {{
        width: min(100vw - 24px, 720px);
        padding-top: 14px;
        padding-bottom: 132px;
      }}
      .topbar,
      .footer-inner {{
        grid-template-columns: 1fr;
        align-items: start;
      }}
      .meta {{ justify-content: flex-start; }}
      .board {{ grid-template-columns: 1fr; }}
      .item {{ min-height: 90px; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <header class="topbar">
      <div>
        <h1>Evaluation contract review</h1>
        <p class="subtitle">Select the Metrics, Criteria, and Benchmark entries that should define the loop before it runs.</p>
      </div>
      <div class="meta" aria-label="Review status">
        <span class="pill primary">A-lite gate</span>
        <span class="pill" id="accepted-pill">{accepted} accepted</span>
        <span class="pill" id="reviewed-pill">{total} reviewed</span>
      </div>
    </header>
    <section class="board" aria-label="Evaluation contract candidates">
      {groups}
    </section>
  </main>
  <footer class="footer">
    <div class="footer-inner">
      <div class="summary" id="summary"><strong>{accepted} accepted</strong> across Metrics, Criteria, and Benchmark. Save before CLI confirmation.</div>
      <button class="save" id="save" type="button">Save selection</button>
    </div>
  </footer>
  <script>
    const rows = Array.from(document.querySelectorAll('.item'));
    function groupName(row) {{
      return row.closest('.group').dataset.group;
    }}
    function updateSummary() {{
      const accepted = rows.filter(row => row.dataset.choice === 'yes').length;
      ['metrics', 'criteria', 'benchmark'].forEach(group => {{
        const groupRows = rows.filter(row => groupName(row) === group);
        const count = groupRows.filter(row => row.dataset.choice === 'yes').length;
        document.querySelector(`[data-count-for="${{group}}"]`).textContent = `${{count}} selected`;
      }});
      document.getElementById('accepted-pill').textContent = `${{accepted}} accepted`;
      document.getElementById('reviewed-pill').textContent = `${{rows.length}} reviewed`;
      document.getElementById('summary').innerHTML =
        `<strong>${{accepted}} accepted</strong> across Metrics, Criteria, and Benchmark. Save before CLI confirmation.`;
    }}
    function selectedItems() {{
      return rows.map(row => ({{
        group: row.dataset.group,
        id: row.dataset.id,
        accepted: row.dataset.choice === 'yes'
      }}));
    }}
    rows.forEach(row => {{
      row.querySelectorAll('button').forEach(button => {{
        button.addEventListener('click', () => {{
          const choice = button.classList.contains('yes') ? 'yes' : 'no';
          row.dataset.choice = choice;
          row.querySelectorAll('button').forEach(item => item.classList.remove('active'));
          button.classList.add('active');
          updateSummary();
        }});
      }});
    }});
    document.getElementById('save').addEventListener('click', async () => {{
      const button = document.getElementById('save');
      button.disabled = true;
      button.textContent = 'Saving';
      try {{
        const response = await fetch('/selection', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ items: selectedItems() }})
        }});
        if (!response.ok) throw new Error(`HTTP ${{response.status}}`);
        button.dataset.saved = 'true';
        button.textContent = 'Saved';
      }} catch (error) {{
        button.textContent = 'Save failed';
        button.dataset.error = String(error);
      }} finally {{
        setTimeout(() => {{
          button.disabled = false;
          if (button.textContent === 'Saved') button.textContent = 'Save selection';
        }}, 900);
      }}
    }});
    updateSummary();
  </script>
</body>
</html>
"""


def render(repo: Path, candidates_path: Path, artifact_dir: str) -> Path:
    candidates = write_candidates(repo, candidates_path, artifact_dir)
    root = review_root(repo, artifact_dir)
    html_path = root / "evaluation-contract.html"
    html_path.write_text(render_html(candidates), encoding="utf-8")
    return html_path


def enrich_selection(root: Path, submitted: dict[str, Any]) -> dict[str, Any]:
    candidates = load_saved_candidates(root)
    choices = {
        (str(item.get("group", "")), str(item.get("id", ""))): bool(item.get("accepted", False))
        for item in submitted.get("items", [])
        if isinstance(item, dict)
    }
    enriched_items: list[dict[str, Any]] = []
    for group, label in GROUPS:
        for item in candidates.get(group, []):
            key = (group, item["id"])
            accepted = choices.get(key, bool(item["recommended"]))
            enriched_items.append(
                {
                    "group": group,
                    "group_label": label,
                    "id": item["id"],
                    "title": item["title"],
                    "description": item["description"],
                    "recommended": item["recommended"],
                    "accepted": accepted,
                }
            )
    return {
        "saved_at": utc_now(),
        "surface": candidates.get("surface", ""),
        "intent": candidates.get("intent", ""),
        "profiles": candidates.get("profiles", []),
        "items": enriched_items,
    }


def save_selection(root: Path, submitted: dict[str, Any]) -> Path:
    selection = enrich_selection(root, submitted)
    path = root / "evaluation-contract-selection.json"
    path.write_text(json.dumps(selection, indent=2, sort_keys=True), encoding="utf-8")
    return path


class ReviewServer(HTTPServer):
    def __init__(self, server_address: tuple[str, int], handler_class: type[BaseHTTPRequestHandler], root: Path):
        super().__init__(server_address, handler_class)
        self.root = root
        self.selection_saved = False


class ReviewHandler(BaseHTTPRequestHandler):
    server: ReviewServer

    def log_message(self, format: str, *args: object) -> None:
        return

    def send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        path = self.server.root / "evaluation-contract.html"
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/selection":
            self.send_json(404, {"ok": False, "error": "unknown endpoint"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        try:
            submitted = json.loads(raw)
            if not isinstance(submitted, dict):
                raise ValueError("selection payload must be a JSON object")
            path = save_selection(self.server.root, submitted)
        except Exception as error:  # pragma: no cover - defensive response
            self.send_json(400, {"ok": False, "error": str(error)})
            return
        self.server.selection_saved = True
        self.send_json(200, {"ok": True, "selection": str(path)})


def serve(repo: Path, candidates_path: Path, artifact_dir: str, host: str, port: int, once: bool) -> int:
    html_path = render(repo, candidates_path, artifact_dir)
    root = html_path.parent
    server = ReviewServer((host, port), ReviewHandler, root)
    actual_host, actual_port = server.server_address
    info = {
        "url": f"http://{actual_host}:{actual_port}",
        "html": str(html_path),
        "selection": str(root / "evaluation-contract-selection.json"),
    }
    (root / "server-info.json").write_text(json.dumps(info, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(info), flush=True)
    try:
        if once:
            while not server.selection_saved:
                server.handle_request()
        else:
            server.serve_forever()
    finally:
        server.server_close()
    return 0


def accepted_by_group(selection: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    grouped = {group: [] for group, _label in GROUPS}
    for item in selection.get("items", []):
        if isinstance(item, dict) and item.get("accepted") and item.get("group") in grouped:
            grouped[str(item["group"])].append(item)
    return grouped


def contract_markdown(selection: dict[str, Any]) -> str:
    grouped = accepted_by_group(selection)
    missing = [label for group, label in GROUPS if not grouped[group]]
    if missing:
        raise ValueError(f"selection must accept at least one item in: {', '.join(missing)}")

    def lines_for(group: str, label: str) -> str:
        lines = []
        for item in grouped[group]:
            lines.append(f"- {label} id: {item['id']}")
            lines.append(f"  - Title: {item['title']}")
            lines.append(f"  - Purpose: {item.get('description', '')}")
        return "\n".join(lines)

    metrics = lines_for("metrics", "Metric")
    criteria = lines_for("criteria", "Criterion")
    benchmarks = lines_for("benchmark", "Seed")
    profiles = ", ".join(selection.get("profiles", []))
    reviewed = utc_now()
    return f"""# Evaluation Contract

Use this file to lock the metric, criteria, benchmark seeds, and verification surface before actioning.

Contract status: locked

## Product Surface

- Surface: {selection.get('surface', '')}
- User flow: human-confirmed evaluation contract review
- Intent: {selection.get('intent', '')}
- Profiles: {profiles}

## Metric

{metrics}

## Acceptance Criteria

{criteria}

## Benchmark seeds

{benchmarks}
- Activation rule: activate selected seeds only after this CLI confirmation; promote durable failures after repo-local evidence.

## Browser Verification

- Playwright required for app verification: yes when the selected surface is browser-visible
- URL or route:
- Viewports:
- Flow steps:
- Assertions:
- Screenshot/trace expectation:

## User Confirmations

- Selection source: review/evaluation-contract-selection.json
- CLI confirmed: yes
- Human gates: actioning work remains blocked until this file is locked from the saved review selection
- Non-goals:
- Last reviewed: {reviewed}
"""


def confirm(repo: Path, artifact_dir: str, yes: bool) -> int:
    root = review_root(repo, artifact_dir)
    selection_path = root / "evaluation-contract-selection.json"
    if not selection_path.is_file():
        print(f"Missing selection: {selection_path}", file=sys.stderr)
        return 2
    selection = read_json(selection_path)
    grouped = accepted_by_group(selection)
    summary = {
        label: [item["title"] for item in grouped[group]]
        for group, label in GROUPS
    }
    print(json.dumps({"accepted": summary}, indent=2, sort_keys=True))
    if not yes:
        print("Re-run with --yes after the user confirms this selection in CLI.")
        return 2
    criteria_path = artifact_root(repo, artifact_dir) / "criteria" / "current.md"
    criteria_path.parent.mkdir(parents=True, exist_ok=True)
    criteria_path.write_text(contract_markdown(selection), encoding="utf-8")
    confirmed_path = root / "evaluation-contract-confirmed.json"
    confirmed = dict(selection)
    confirmed["cli_confirmed"] = True
    confirmed["confirmed_at"] = utc_now()
    confirmed_path.write_text(json.dumps(confirmed, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Locked criteria: {criteria_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-dir", default=DEFAULT_ARTIFACT_DIR)
    subparsers = parser.add_subparsers(dest="command", required=True)

    render_parser = subparsers.add_parser("render")
    render_parser.add_argument("--repo", required=True)
    render_parser.add_argument("--candidates", required=True)

    serve_parser = subparsers.add_parser("serve")
    serve_parser.add_argument("--repo", required=True)
    serve_parser.add_argument("--candidates", required=True)
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=0)
    serve_parser.add_argument("--once", action="store_true")

    confirm_parser = subparsers.add_parser("confirm")
    confirm_parser.add_argument("--repo", required=True)
    confirm_parser.add_argument("--yes", action="store_true")

    args = parser.parse_args()
    artifact_dir = args.artifact_dir
    if args.command == "render":
        path = render(Path(args.repo), Path(args.candidates), artifact_dir)
        print(f"Rendered review page: {path}")
        return 0
    if args.command == "serve":
        return serve(Path(args.repo), Path(args.candidates), artifact_dir, args.host, args.port, args.once)
    if args.command == "confirm":
        return confirm(Path(args.repo), artifact_dir, args.yes)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
