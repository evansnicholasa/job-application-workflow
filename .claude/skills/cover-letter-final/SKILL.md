---
name: cover-letter-final
description: Prepare the final copy of a cover letter once the user has approved the draft. Runs final checks and produces the copy the user will send, using the user's own document tooling if context/profile.md describes it. Use only when the user says the letter is done.
---

# Finalize a cover letter

The draft step (`cover-letter`) never produces a final copy. This step does, and it runs
**only when the user says the letter is done**. Keeping the two apart means a file called
final is always the letter the user approved, never some draft from some point.

## 1. Confirm what is being finalized

Never run on your own initiative. The current draft is `<job folder>/cover-letter/draft.md`;
anything in `versions/` is not current. If there is any doubt about which text the user
approved, stop and ask.

## 2. Check the approved text

Read `context/house-style.md` and `context/profile.md`, then check the draft:

- The company name and role title match the posting exactly.
- The date is today's date, and the name and contact details match `profile.md`.
- Nothing the house style bans outright is present (for example em dashes). Count, do not skim.
- No leftover markers from drafting: brackets, notes to self, "insert", repeated words.
- The length is within the house-style limit.

Do not reword the letter. If a check fails, stop and report it; the fix goes back through the
user.

## 3. Produce the final copy

Copy the approved text to `<job folder>/cover-letter/final.md`. Then produce the document the
user sends with the tooling `profile.md` describes (for example a word-processor file built
from their résumé's styles, exported to PDF). Check what you can about the result, such as the
page count. If `profile.md` describes no tooling, stop at `final.md` and say the document
still needs producing.

Name the document as `profile.md` says. If it gives no rule, use the user's name and today's
date. Never put internal ids or notes in a filename that goes to an employer.

## 4. Report

- Path of `final.md` and of any document produced
- The result of each check
- What the user still has to do by hand

Do not send, upload, attach or submit anything, and do not contact anyone.
