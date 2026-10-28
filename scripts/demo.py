#!/usr/bin/env python3
"""Create a demo jobs/ folder with fictional jobs at every stage, then write board.html.

    python scripts/demo.py           create or refresh the demo jobs and write board.html
    python scripts/demo.py --clean   remove the demo jobs and rewrite board.html

Every company, person and posting here is fictional. Demo jobs live in jobs/demo-*/ and are the
only folders this script creates or removes, so it never touches your real jobs.
Only the Python standard library is used.
"""

import json
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
JOBS = ROOT / "jobs"

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import board  # noqa: E402

NOTE = "Demo data. Every company and person in this file is fictional.\n\n"


def q(i, text, status="open"):
    return {"id": str(i), "text": text, "status": status}


DEMO = [
    {
        "slug": "demo-woodgrove-senior-qa-automation",
        "company": "Woodgrove Bank",
        "role": "Senior QA Automation Engineer",
        "url": "https://aggregator.example.net/jobs/88213",
        "original_url": "https://jobs.example.com/woodgrove/senior-qa-automation-engineer",
        "stage": "awaiting-gate-1",
        "verdict": "Apply",
        "user_decision": None,
        "questions": [q(1, "Fit review says Apply (strong fit on Playwright and API testing). Apply or skip?")],
        "docs": {
            "source": "# Source report\n\nResult: Confirmed.\nOriginal: the employer's own careers page.\n"
                      "Matched on the benefits list, the tool list and the team description.\n",
            "fit_review": "# Woodgrove Bank - Senior QA Automation Engineer\n\nApply: yes.\n"
                          "Strong fit on Playwright, TypeScript and REST API testing.\n"
                          "Main gap: the posting prefers performance testing with k6, which is unconfirmed.\n",
        },
    },
    {
        "slug": "demo-contoso-sdet",
        "company": "Contoso Labs",
        "role": "Software Development Engineer in Test",
        "url": "https://jobs.example.com/contoso/sdet-2291",
        "original_url": None,
        "stage": "awaiting-tailor-input",
        "verdict": "Apply",
        "user_decision": "Apply",
        "questions": [
            q(1, "The posting asks for contract testing with Pact. I have no record of it. Have you used it, and on which project?"),
            q(2, "It names Azure DevOps Pipelines. Your facts mention GitHub Actions and Jenkins only. Have you worked with Azure DevOps, and where?"),
            q(3, "Approve the change summary (summary reordered, skills regrouped, two bullets reworded)?"),
        ],
        "docs": {
            "fit_review": "# Contoso Labs - SDET\n\nApply: yes.\nGood skills fit. Contract testing is unconfirmed.\n",
            "resume_changes": "# Proposed résumé changes\n\nBefore: Built UI tests in Selenium and Java.\n"
                              "After: Built UI and API test suites in Java, with Selenium for the browser layer.\n"
                              "Evidence: career-facts.md, Northwind Systems role.\n",
        },
    },
    {
        "slug": "demo-fabrikam-qa-engineer-ii",
        "company": "Fabrikam",
        "role": "QA Engineer II",
        "url": "https://jobs.example.com/fabrikam/qa-engineer-ii",
        "original_url": None,
        "stage": "awaiting-gate-3",
        "verdict": "Apply",
        "user_decision": "Apply",
        "track": "QA",
        "questions": [q(1, "Résumé is approved. Tell me once you have applied, and whether this application takes a cover letter.")],
        "docs": {
            "fit_review": "# Fabrikam - QA Engineer II\n\nApply: yes.\nSolid fit, slightly junior for your experience.\n",
            "resume_changes": "# Résumé changes (approved)\n\nSkills line reordered to lead with Cypress and SQL.\n",
        },
    },
    {
        "slug": "demo-tailspin-test-automation-lead",
        "company": "Tailspin Toys",
        "role": "Test Automation Lead",
        "url": "https://jobs.example.com/tailspin/test-automation-lead",
        "original_url": None,
        "stage": "awaiting-cover-feedback",
        "verdict": "Worthwhile stretch",
        "user_decision": "Apply",
        "track": "QA",
        "questions": [q(1, "Cover letter draft is ready, rated 7 out of 10 (it does not name an outcome metric). Feedback or approve?")],
        "docs": {
            "fit_review": "# Tailspin Toys - Test Automation Lead\n\nApply: yes, as a stretch.\n"
                          "The lead role is broader than your mentoring experience.\n",
            "cover_draft": "Dear Tailspin Toys Hiring Team,\n\n"
                           "A shortened demo draft. A real draft has three short paragraphs and a closing.\n",
        },
    },
    {
        "slug": "demo-wideworld-quality-engineer",
        "company": "Wide World Importers",
        "role": "Quality Engineer",
        "url": "https://aggregator.example.net/jobs/90417",
        "original_url": None,
        "stage": "finding-original",
        "verdict": None,
        "user_decision": None,
        "questions": [],
        "docs": {},
    },
    {
        "slug": "demo-adventureworks-software-engineer-in-test",
        "company": "Adventure Works",
        "role": "Software Engineer in Test",
        "url": "https://jobs.example.com/adventureworks/set-417",
        "original_url": None,
        "stage": "tailoring",
        "verdict": "Apply",
        "user_decision": "Apply",
        "track": "QA",
        "questions": [q(1, "Do you have experience with Appium?", "answered")],
        "docs": {
            "fit_review": "# Adventure Works - Software Engineer in Test\n\nApply: yes.\n",
        },
    },
    {
        "slug": "demo-litware-senior-sdet",
        "company": "Litware",
        "role": "Senior SDET",
        "url": "https://jobs.example.com/litware/senior-sdet",
        "original_url": None,
        "stage": "finalized",
        "verdict": "Apply",
        "user_decision": "Apply",
        "track": "QA",
        "questions": [],
        "docs": {
            "fit_review": "# Litware - Senior SDET\n\nApply: yes.\n",
            "cover_final": "Dear Litware Hiring Team,\n\nA shortened demo of an approved final letter.\n",
        },
    },
    {
        "slug": "demo-proseware-qa-analyst",
        "company": "Proseware",
        "role": "Quality Assurance Analyst (Manufacturing)",
        "url": "https://jobs.example.com/proseware/qa-analyst",
        "original_url": None,
        "stage": "skipped",
        "verdict": "Skip",
        "user_decision": "Skip",
        "questions": [],
        "docs": {
            "fit_review": "# Proseware - Quality Assurance Analyst\n\nApply: no.\n"
                          "This is manufacturing quality control, not software testing.\n",
        },
    },
]

FILENAMES = {
    "source": "source.md",
    "fit_review": "fit-review.md",
    "resume_changes": "resume-changes.md",
    "cover_draft": "cover-letter/draft.md",
    "cover_final": "cover-letter/final.md",
}


def clean():
    for d in JOBS.glob("demo-*"):
        if d.is_dir():
            shutil.rmtree(d)


def create():
    clean()
    for job in DEMO:
        folder = JOBS / job["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        files = {}
        for key, text in job["docs"].items():
            name = FILENAMES[key]
            (folder / name).parent.mkdir(parents=True, exist_ok=True)
            (folder / name).write_text(NOTE + text, encoding="utf-8")
            files[key] = f"jobs/{job['slug']}/{name}"
        state = {k: v for k, v in job.items() if k != "docs"}
        state.setdefault("track", None)
        state["agent_ids"] = {"source": None, "fit": None, "tailor": None, "cover": None}
        state["files"] = files
        open_qs = [x for x in state["questions"] if x["status"] == "open"]
        state["pending_for_user"] = open_qs[0]["text"] if open_qs else None
        state["notes"] = "Demo job. Fictional."
        (folder / "state.json").write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Created {len(DEMO)} demo jobs in {JOBS}")


def main():
    if "--clean" in sys.argv:
        clean()
        print("Removed the demo jobs.")
    else:
        create()
    board.write_html()
    print(f"Wrote {board.OUT}")
    if "--clean" not in sys.argv:
        print("Open board.html in a browser to see the board.")


if __name__ == "__main__":
    main()
