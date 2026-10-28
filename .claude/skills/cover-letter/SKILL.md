---
name: cover-letter
description: Draft a cover letter for one job from the user's facts and house style in context/, self-review it in three passes with different jobs, rate it, and save the draft in the job's folder. Use when asked to write or revise a cover letter. Draft only; the final copy is cover-letter-final.
---

# Draft a cover letter

Produces a **rated draft**, not a finished letter. The final copy belongs to
`cover-letter-final`, after the user has revised and approved.

## Read these first, every time

- `context/career-facts.md`: the facts. Nothing in the letter may assert anything this file
  or the current résumé does not support.
- `context/house-style.md`: the craft. Structure, prose rules, the closing, length, and the
  rating scale. If it names a reference letter the user wrote or approved, read it and write
  toward it.
- `context/profile.md`: the user's name and contact details for the letter, and how they
  produce documents.
- The job folder: `posting.md`, the fit review, and the tailored résumé if there is one, so the
  letter matches what the employer will already see.

If a file is missing, stop and say so.

**When you run as a subagent you cannot talk to the user.** Any question goes in your final
message for the manager to relay.

## 1. Read the posting for its stated requirements

Pull out the stack, the seniority bar, and anything named as required rather than preferred.
That decides what each paragraph leads with. Note every requirement the facts cannot support,
so the report can name the gaps. If there is no posting text, ask for it; do not write from
the title alone.

Do not research the company or write about its product unless `house-style.md` or the user asks
for it. A paragraph of generated opinion about a product, in the user's voice, is a claim the
user cannot defend in an interview unless they actually hold that view.

## 2. Draft

Follow the structure in `house-style.md`. If it gives none, use three short body paragraphs
(the fit, scale and leadership, craft and tooling) and a two-sentence closing that offers a
conversation, not a deliverable. A reader who only reads first sentences should still get the
case. Lead with the user's experience; never paraphrase the posting back at the employer, and
never copy its sentences.

## 3. Three revision passes, before showing anything

Each pass has a **different job**. Three identical passes converge on blandness and start
inventing nitpicks.

1. **Fact check.** Trace every claim to `career-facts.md` or the résumé. Watch especially for
   employer structure (a client is not an employer), "most recent" claims, dates and titles.
2. **Substance.** Cut tie-backs, character claims, epigrams and filler. Rewrite "I did X rather
   than Y" contrasts as the plain claim. Read each sentence aloud: if it sounds like a line
   rather than a remark, flatten it. Apply every prose rule in `house-style.md`.
3. **Compression.** Repeated points and overstuffed paragraphs. The last body paragraph must
   not sit directly on the signature. Count anything `house-style.md` bans outright (for
   example em dashes); the count must be zero, and the fix is to rewrite the sentence.

**The table-stakes test.** For every sentence, ask whether every competent person in the
user's role could say the same thing. If so, cut it, however well it matches a requirement.
Leaving a requirement unanswered and naming the gap beats inflating routine work to cover it.

**Length is a ceiling, not a target.** When the strong material runs out, the letter ends.
Never pad to reach a count, and never report a short letter as a defect.

**Never invent a fact or a metric to close a gap.** Report the gap instead. A self-revision
loop that fabricates is worse than no loop.

## 4. Save

Save in `<job folder>/cover-letter/`:

- `draft.md`: the letter as plain text, with date, salutation, body, closing and name
- `posting.md`: the trimmed posting text, if it is not already in the job folder
- `versions/`: if a draft already exists, move it here first, named `<date>_<what-changed>.md`

Do not produce a PDF or any other final document here.

## 5. Report

- The letter as text
- A **rating out of 10** and what it still lacks, using the scale in `house-style.md`. Be
  honest that the rating is not independent, since the same process wrote the letter. If a
  higher score would need facts that do not exist (for example outcome metrics), say so
  rather than inflating the score.
- Any facts you could not verify
- Requirements left unanswered

## Revising

The user will ask for changes; that is where the letter improves. Revise, move the previous
draft into `versions/`, and report the new text and rating. Once three or four rounds have
passed and the changes are small, **say the letter is done.** Rereading always surfaces
something; that is a property of rereading, not evidence of remaining defects.
