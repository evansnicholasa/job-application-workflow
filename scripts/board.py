#!/usr/bin/env python3
"""Show every job from jobs/*/state.json.

    python scripts/board.py          one text line per job
    python scripts/board.py --html   write board.html (open it in a browser; it refreshes itself)
    python scripts/board.py --watch  keep board.html current: regenerate whenever a state.json changes

The board is generated, never edited. The manager keeps each state.json current, so the board
always shows the same facts the manager works from. Only the Python standard library is used.
"""

import html
import json
import pathlib
import sys
import time
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
JOBS = ROOT / "jobs"
OUT = ROOT / "board.html"

STEPS = ["Original posting", "Fit review", "Your decision", "Résumé", "Apply", "Cover letter", "Finished"]

# stage -> (step index, who holds the ball: "you", "agents" or "done")
STAGES = {
    "intake": (0, "agents"),
    "finding-original": (0, "agents"),
    "fit-review": (1, "agents"),
    "awaiting-gate-1": (2, "you"),
    "skipped": (2, "done"),
    "tailoring": (3, "agents"),
    "awaiting-tailor-input": (3, "you"),
    "awaiting-resume-approval": (3, "you"),
    "applying": (4, "you"),
    "awaiting-gate-3": (4, "you"),
    "cover-drafting": (5, "agents"),
    "awaiting-cover-feedback": (5, "you"),
    "awaiting-finalize-ok": (5, "you"),
    "finalizing": (5, "agents"),
    "no-cover-letter": (6, "done"),
    "finalized": (6, "done"),
    "done": (6, "done"),
    # Work that is not a job application (for example updating the master résumé).
    # Set "kind": "task" in its state.json.
    "task-you": (0, "you"),
    "task-agents": (0, "agents"),
    "task-done": (0, "done"),
}

LABELS = {
    "intake": "Starting",
    "finding-original": "Finding the original posting",
    "fit-review": "Reviewing fit",
    "awaiting-gate-1": "Waiting for your apply or skip decision",
    "skipped": "Skipped",
    "tailoring": "Tailoring the résumé",
    "awaiting-tailor-input": "Waiting for your answers or approval on the résumé",
    "awaiting-resume-approval": "Waiting for you to review the résumé",
    "applying": "You are applying",
    "awaiting-gate-3": "Does it need a cover letter?",
    "cover-drafting": "Drafting the cover letter",
    "awaiting-cover-feedback": "Waiting for your feedback on the cover letter",
    "awaiting-finalize-ok": "Waiting for your word to finalize the letter",
    "finalizing": "Preparing the final letter",
    "no-cover-letter": "Applied, no cover letter",
    "finalized": "Letter finalized",
    "done": "Done",
    "task-you": "Waiting for you",
    "task-agents": "Agents working",
    "task-done": "Done",
}

# files key in state.json -> link label on the card, in display order
FILE_LINKS = [
    ("source", "Source report"),
    ("fit_review", "Fit review"),
    ("resume_changes", "Résumé changes"),
    ("resume_folder", "Résumé folder"),
    ("resume_file", "Résumé"),
    ("cover_draft", "Cover letter draft"),
    ("cover_final", "Final cover letter"),
]


def load_jobs():
    jobs = []
    for f in sorted(JOBS.glob("*/state.json")):
        try:
            s = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            s = {"slug": f.parent.name, "company": f.parent.name, "role": f"unreadable state.json ({e})", "stage": "?"}
        jobs.append(s)
    return jobs


def open_questions(s):
    qs = [q for q in s.get("questions", []) if q.get("status", "open") == "open"]
    if not qs and s.get("pending_for_user"):
        qs = [{"id": "", "text": s["pending_for_user"]}]
    return qs


def holder(s):
    return STAGES.get(s.get("stage"), (0, "agents"))[1]


def text_board(jobs):
    if not jobs:
        print("No jobs yet.")
        return
    order = {"you": 0, "agents": 1, "done": 2}
    for s in sorted(jobs, key=lambda j: order[holder(j)]):
        line = f"{s.get('company', '?')} - {s.get('role', '?')} [{s.get('stage', '?')}]"
        for q in open_questions(s):
            line += f"\n    needs you: {(q.get('id') + ': ') if q.get('id') else ''}{q['text']}"
        print(line)


def href(path):
    """Link to a file. Paths inside the project become relative links, so the board works
    wherever the folder lives; other paths become file:// links."""
    p = pathlib.Path(path)
    if not p.is_absolute():
        p = ROOT / p
    try:
        rel = p.resolve().relative_to(ROOT)
        return urllib.parse.quote(rel.as_posix())
    except ValueError:
        return p.as_uri()


def links(s):
    items = []
    if s.get("original_url"):
        items.append(("Posting", s["original_url"]))
    elif s.get("url"):
        items.append(("Posting", s["url"]))
    f = s.get("files") or {}
    for key, label in FILE_LINKS:
        if f.get(key):
            items.append((label, href(f[key])))
    return items


def steps_html(s):
    if s.get("kind") == "task":
        return ""
    idx, who = STAGES.get(s.get("stage"), (0, "agents"))
    out = []
    for i, name in enumerate(STEPS):
        if who == "done" and idx == len(STEPS) - 1:
            cls = "done"
        elif i < idx:
            cls = "done"
        elif i == idx:
            cls = "now-" + who
        else:
            cls = ""
        out.append(f'<li class="{cls}">{html.escape(name)}</li>')
    return "<ol class='steps'>" + "".join(out) + "</ol>"


def card(s):
    who = holder(s)
    qs = open_questions(s)
    esc = html.escape
    q_html = ""
    if qs:
        q_html = "<ul class='qs'>" + "".join(
            f"<li>{('<b>' + esc(q['id']) + '.</b> ') if q.get('id') else ''}{esc(q['text'])}</li>" for q in qs) + "</ul>"
    link_html = " ".join(f'<a href="{esc(u)}">{esc(l)}</a>' for l, u in links(s))
    meta = []
    if s.get("kind") == "task":
        meta.append("Task, not a job application")
    if s.get("track"):
        meta.append(f"{s['track']} résumé")
    if s.get("verdict"):
        meta.append(f"Review: {s['verdict']}")
    return (
        f'<article class="card {who}">'
        f'<h3>{esc(str(s.get("company", "?")))}</h3>'
        f'<p class="role">{esc(str(s.get("role", "")))}</p>'
        f'<p class="state">{esc(LABELS.get(s.get("stage"), str(s.get("stage"))))}</p>'
        f'{steps_html(s)}{q_html}'
        f'<p class="meta">{esc(" · ".join(meta))}</p>'
        f'<p class="links">{link_html}</p></article>'
    )


def html_board(jobs):
    groups = {"you": [], "agents": [], "done": []}
    for s in jobs:
        groups[holder(s)].append(s)
    n_q = sum(len(open_questions(s)) for s in groups["you"])
    sections = [
        ("you", "Waiting on you", f"{len(groups['you'])} job(s), {n_q} open item(s)"),
        ("agents", "Agents working", f"{len(groups['agents'])} job(s)"),
        ("done", "Finished", f"{len(groups['done'])} job(s)"),
    ]
    body = ""
    for key, title, sub in sections:
        cards = "".join(card(s) for s in groups[key]) or '<p class="empty">Nothing here.</p>'
        body += (f'<details class="sec" data-key="{key}" open><summary><h2>{title} <span>{sub}</span></h2></summary>'
                 f'<div class="grid">{cards}</div></details>')
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    return TEMPLATE.replace("{{BODY}}", body).replace("{{STAMP}}", stamp)


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="20">
<title>Job Board</title>
<style>
:root{--bg:#f6f6f4;--card:#fff;--ink:#1c1c1a;--mute:#6b6b66;--line:#dcdcd6;--you:#b45309;--youbg:#fff7e6;--agent:#1d4ed8;--agentbg:#eef3ff;--ok:#15803d;--okbg:#eef8f1}
@media (prefers-color-scheme:dark){:root{--bg:#161614;--card:#20201d;--ink:#ecece8;--mute:#9a9a92;--line:#34342f;--you:#f59e0b;--youbg:#2b2210;--agent:#7aa2ff;--agentbg:#172036;--ok:#4ade80;--okbg:#14261b}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.45 system-ui,Segoe UI,Arial,sans-serif;padding:20px 16px 40px}
main{max-width:1100px;margin:0 auto}header{display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px;margin-bottom:8px}
h1{font-size:22px;margin:0}header small{color:var(--mute)}
details.sec{margin-top:26px}summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:8px;margin:0 0 10px;user-select:none}summary::-webkit-details-marker{display:none}
summary::before{content:"\\25BE";color:var(--mute);font-size:16px;transition:transform .15s}details.sec:not([open]) summary::before{transform:rotate(-90deg)}
summary:hover h2{color:var(--ink)}h2{font-size:15px;text-transform:uppercase;letter-spacing:.06em;margin:0;color:var(--mute)}h2 span{text-transform:none;letter-spacing:0;font-weight:400;margin-left:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-left:5px solid var(--line);border-radius:8px;padding:12px 14px}
.card.you{border-left-color:var(--you);background:var(--youbg)}.card.agents{border-left-color:var(--agent);background:var(--agentbg)}.card.done{border-left-color:var(--ok)}
.card h3{margin:0;font-size:17px}.role{margin:2px 0 6px;color:var(--mute)}.state{margin:0 0 8px;font-weight:600}
.card.you .state{color:var(--you)}.card.agents .state{color:var(--agent)}.card.done .state{color:var(--ok)}
.steps{list-style:none;display:flex;flex-wrap:wrap;gap:4px;padding:0;margin:0 0 8px}.steps li{font-size:11px;padding:2px 7px;border-radius:99px;border:1px solid var(--line);color:var(--mute)}
.steps li.done{background:var(--okbg);color:var(--ok);border-color:transparent}.steps li.now-you{background:var(--you);color:#fff;border-color:transparent;font-weight:600}.steps li.now-agents{background:var(--agent);color:#fff;border-color:transparent;font-weight:600}
.qs{margin:6px 0 8px;padding-left:0;list-style:none}.qs li{margin:3px 0}.meta{margin:4px 0;color:var(--mute);font-size:13px}.links{margin:6px 0 0;display:flex;flex-wrap:wrap;gap:6px 12px;font-size:13px}.links a{color:var(--agent)}
.empty{color:var(--mute);margin:0}
</style></head><body><main>
<header><h1>Job Board</h1><small>Updated {{STAMP}} · refreshes every 20 seconds</small></header>
{{BODY}}
</main>
<script>
// Remember which sections are collapsed across the 20-second refresh and across visits.
(function(){
  var KEY="jobboard-collapsed", saved={};
  try{saved=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}
  document.querySelectorAll("details.sec").forEach(function(d){
    var k=d.getAttribute("data-key");
    if(saved[k]) d.removeAttribute("open");
    d.addEventListener("toggle",function(){
      saved[k]=!d.open;
      try{localStorage.setItem(KEY,JSON.stringify(saved))}catch(e){}
    });
  });
})();
</script></body></html>
"""


def write_html():
    OUT.write_text(html_board(load_jobs()), encoding="utf-8")


def watch():
    """Regenerate board.html whenever any state.json changes (checked every 3 seconds)."""
    print(f"Watching {JOBS} and writing {OUT}. Press Ctrl+C to stop.")
    last = None
    try:
        while True:
            stamp = sorted((str(f), f.stat().st_mtime_ns) for f in JOBS.glob("*/state.json"))
            if stamp != last:
                write_html()
                last = stamp
            time.sleep(3)
    except KeyboardInterrupt:
        pass


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    if "--watch" in sys.argv:
        watch()
        return
    if "--html" in sys.argv:
        write_html()
        print(f"Wrote {OUT}")
    else:
        text_board(load_jobs())


if __name__ == "__main__":
    main()
