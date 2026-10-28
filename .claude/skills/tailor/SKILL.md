---
name: tailor
description: Tailor the user's résumé to one job posting by surfacing real, relevant experience from context/, or report that no change is needed. Asks about any requirement the context files cannot support instead of skipping it or assuming. Use when asked to tailor or customize a résumé for a posting. Works on a copy; never edits the master résumé.
---

# Tailor a résumé to one posting

Produces a **tailored résumé** for one posting, or a clear statement that the master résumé
already fits and needs no change. "No change" is a valid and common outcome. Do not edit for
the sake of editing.

## Read these first, every time

- `context/career-facts.md`: the facts, including the "known gaps" and "always wrong" lists.
  Nothing on the résumé may assert anything this file or the master résumé does not support.
- `context/profile.md`: where the master résumé (or résumés) live, which one to use for which
  kind of role, page limits, and how the user produces documents.
- `context/house-style.md`: the prose rules and any résumé conventions (fixed wording,
  headline rules, terms to avoid). Its cover-letter rules do not apply here.

If a file is missing, stop and say so.

**When you run as a subagent you cannot talk to the user.** Every "ask the user" and "wait for
approval" point below means: stop, and make your final message the questions or the summary.
The manager relays them and resumes you with the answers.

## 1. Get the posting

Use the job folder's `posting.md` if it exists, otherwise the URL or text the manager gave you.
Job-board pages often carry other companies' listings, "people also viewed" rails and salary
estimates after the posting itself. Cut the text where the posting ends; other companies'
requirements and pay must never reach the résumé.

If there is no usable posting text, ask for it. Do not proceed on the title alone.

## 2. Pick the master résumé

Use the master résumé `profile.md` names for this kind of role. If the user keeps more than
one and the posting could fit either, **ask the user**. State which file you used in every
report. Never modify it.

## 3. Map requirements to evidence

List the posting's stated requirements (stack, tools, domain, seniority, leadership, required
or preferred). Classify each one:

| Class | Meaning | Action |
|---|---|---|
| Already prominent | On the résumé and easy to see | Nothing |
| Supported but buried or absent | In `career-facts.md` or the résumé, but not surfaced | Candidate edit |
| Unknown | Not in the context files or the résumé | **Ask the user** |
| Known gap | Listed under known gaps or "always wrong" | Leave out, report the gap |

**Ask about every unknown requirement in one batch, before any editing.** Phrase each as a
yes or no plus "where and roughly how", so the answer is defensible: "The posting asks for
Kafka. I have no record of it. Do you have hands-on experience, and on which project?" Never
silently skip an unknown, and never assume yes.

If the user confirms new experience, use it, and report it so the manager can offer to record
it in `career-facts.md` with the date and any limits the user put on the claim. Do not write to
that file yourself.

## 4. Decide what may change

Allowed, when supported: reorder or regroup the skills section; reword or reorder bullets to
lead with what the posting names; add a skill or tool the user has confirmed; adjust the
summary's emphasis. Keep to the page limit in `profile.md`; nothing is added as filler, and
the first page must stand on its own with the strongest material.

Not allowed: invent or inflate anything; add metrics the facts do not record; change dates,
titles or employer structure; claim anything on the "always wrong" list; change anything
`house-style.md` marks as fixed (for example the headline under the name); write the target
company or role anywhere it reads as a label.

**Defensibility outranks keyword matching.** If the user could not back a line up out loud in
an interview, it does not go on the résumé, even if the posting asks for it.

**Keyword coverage.** Automated screens and recruiter searches look for the posting's terms,
soft skills included. After drafting, list the posting's technical terms and soft skills (for
example collaboration, mentoring, ownership, working independently) and make sure each one
the user can defend appears at least once, as a short term in the summary, a bullet or the
skills line. Back soft skills with the evidence in `career-facts.md`, and use two or three,
not a list.

**Never copy a posting's sentences.** Verbatim matches can get an application flagged as
generated and filtered out. Name the tools and skills the posting asks for, but write the
sentences in the user's own wording from `career-facts.md`.

## 5. Show the change summary and wait

Before producing anything, return:

- The master résumé used
- The requirement map (short)
- Proposed edits as **before and after** pairs, each with the fact it rests on
- Gaps left unanswered
- If nothing is worth changing: **"No changes needed"**, with the reasoning. Stop there and
  create no file.

Save the summary to `<job folder>/resume-changes.md`. Wait for approval or edits.

## 6. Produce the résumé

Only after the summary is approved:

1. Save the tailored résumé text to `<job folder>/resume/resume.md`: the full résumé as it
   should read, so the user can review it without opening a document.
2. **Verbatim check.** Compare the tailored text with the posting for runs of four or more
   consecutive shared words. Rewrite any that are not just a tool name, a job title or a
   standard term. Record the result in the notes.
3. Produce the document the user sends with the tooling `profile.md` describes (for example
   editing a copy of the master document and exporting a PDF). Work on a copy, keep the master's
   styles, and check the page count against the limit. If `profile.md` describes no tooling,
   do not invent a build: report that the text is ready and the document needs producing.
4. Name the document as `profile.md` says. If it gives no rule, use the user's name and today's
   date, never the date of the master file and never the company name (the folder tells
   versions apart; the file goes to the employer).
5. If the folder already holds a résumé, move it into `versions/` first, named
   `<date>_<what-changed>`.
6. Save `<job folder>/resume/tailor-notes.md`: requirement map, edits made, gaps, questions and
   answers, verbatim-check result.

## 7. Report

- Master résumé used
- The edits made, or "no changes needed"
- Gaps left unanswered, stated plainly
- Paths of everything produced, and anything the user still has to do by hand
- New facts the user confirmed, for the manager to offer to record

If the master résumé itself should change because of something that surfaced (a skill the user
has that is missing everywhere), say so as a separate suggestion. Do not apply it.
