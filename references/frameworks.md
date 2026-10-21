# Frameworks used for coding and synthesis

This file summarizes, in this skill's own words, the ideas that shape how findings are tagged and how themes are written up. Use it to understand why fields exist; you do not need to cite any of it. The deliverable never names these frameworks, their authors or their books; it describes what was done in plain language ("we tagged each finding by what removing the problem would deliver").

## Contents

1. Jobs to be done
2. Forces that drive or block change
3. Desired outcomes
4. Job stories
5. Buyer interviews
6. Fit between offer and need
7. What makes relief valuable
8. Where each idea shows up in the run

## 1. Jobs to be done

People do not want a product; they want to make progress on a job in their circumstances. A job has a **performer** (who does it), a **goal** (what "done" looks like), and a **process** (the stages they go through). Jobs have three layers:

- **Functional:** the task itself (close the books, reconcile accounts, file a return).
- **Emotional:** how the performer wants to feel or avoid feeling (confident in the numbers, not blamed for an error).
- **Social:** how they want to be seen (a strategic partner rather than a scorekeeper).

The job is stable over time even as tools change. That is why the research codes pains against the job, not against products. Two consequences for the run:

- Job areas come from walking the job's stages: define and plan, gather inputs, prepare, execute, check, fix, report, conclude. Name the domains where the work happens; those become the job-area list.
- A pain is something that makes the job slower, riskier, costlier or less certain than the performer wants. A theme groups findings that describe the same obstacle to the same job, regardless of which tool they use.

## 2. Forces that drive or block change

Whether someone changes how they do a job depends on four forces:

- **Push:** frustration with the current way ("we close in spreadsheets and it takes ten days").
- **Pull:** attraction to a better way ("I wish it matched payments automatically").
- **Anxiety:** fear about the new way (will it be accurate, will the auditors accept it, will the project fail).
- **Habit:** comfort with the current way, including sunk cost in workarounds that already work well enough.

Change happens only when push and pull outweigh anxiety and habit. One further tag helps:

- **Workaround:** the performer built a fix (spreadsheets, scripts, extra headcount). A workaround proves the pain is real enough to spend effort on, and it is the incumbent any new approach must beat.

Something the performer wants to stop doing altogether is a strong signal too, but it is recorded as a push, not as a separate tag. Collectors tag each finding with any of `push, pull, anxiety, habit, workaround`; the script flags any other value. The anxiety and habit tags feed the "Adoption risks" section.

## 3. Desired outcomes

A desired outcome is a measurable statement of what the performer wants from a stage of the job, written as **direction + metric + object + qualifier**: "minimize the time it takes to reconcile intercompany balances at month end." Outcomes avoid naming solutions, so they stay valid across products.

The run uses outcomes in two places: to keep theme names about the problem rather than a solution, and to suggest the measurable target for each theme in "Next steps" (for example "a five-day close").

## 4. Job stories

A job story states a need in its situation:

> **When** [situation and trigger], **I want to** [motivation], **so I can** [expected outcome].

Job stories differ from user stories because they describe the circumstance, not a persona, and they leave the solution open. In the deliverable, each high- or medium-confidence theme gets at least one job story built from its findings. Each story cites the finding IDs it rests on. Stories are hypotheses to test in interviews, and the deliverable says so.

## 5. Buyer interviews

Passive research shows where pain is; it does not show who will pay to remove it. The recommended next step is a small set (5 to 10) of buyer interviews per candidate theme. They work best when anchored on a real, recent event rather than opinions:

- Pick someone who recently bought, switched or abandoned a tool or service for the job (or tried to).
- Reconstruct the timeline: what first made them look for something new, what they did in the meantime, what they compared, what nearly stopped them, what finally made them decide, and how they knew it worked.
- Ask open questions (what, how, tell me about the last time…). Do not pitch, do not describe an idea and ask if they would buy it. Opinions about the future are weak evidence; past behaviour is strong evidence.
- Listen for the four forces, the workaround being replaced, and who else had to approve the purchase.

The "Next steps" section of the deliverable proposes these interviews and lists what each should test (willingness to pay, the job stories, the vendor-heavy themes).

## 6. Fit between offer and need

An offer fits a market when it addresses jobs the market cares about, relieves pains they rank as severe, and creates gains they want. This research covers only the market side of that fit: jobs, pains and desired gains, each with evidence. It deliberately says nothing about any particular offer unless the user explicitly asks for that comparison (see the neutrality rules in `deliverable.md`).

## 7. What makes relief valuable

The perceived value of removing a problem rises with the size of the outcome and the buyer's belief that it will really happen, and falls with the time it takes to arrive and the effort or sacrifice it demands. In short: value ≈ (outcome × likelihood) ÷ (time × effort).

Use this as a lens when writing "Reported numbers for sizing" and "Next steps": a pain with large reported costs, repeated failed attempts (low belief that any tool will fix it), long delays and heavy manual effort is a stronger candidate than one that is merely common. Do not score themes with it in the deliverable; the evidence grouping stays the primary ranking.

## 8. Where each idea shows up in the run

| Idea | Field or section |
|---|---|
| Job areas from the job's stages | `job area:` field; defined in the plan |
| Pain relief versus money | `value:` field; Value column of the theme table |
| Forces and workarounds | `forces:` field; Adoption risks section |
| Market's own words | `words:` field; How buyers describe the problem |
| Desired outcomes | Theme names stay solution-free; measurable targets in Next steps |
| Job stories | Job stories to test |
| Buyer interviews | Next steps and the decisions table |
| What makes relief valuable | Reported numbers for sizing; Next steps |
