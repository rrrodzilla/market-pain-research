---
name: market-pain-research
description: Run passive pain-point research on any target market and deliver a review document with two parts, Findings (opening with a one-page executive summary) and an Evidence index that links every finding to its source. Reads where the market already talks (practitioner forums, podcasts, newsletters and their comments, product reviews, plus any communities the user names, such as Slack groups) without posting or contacting anyone. Then codes 100-200 findings into themes, with vendor share and confidence for each. Use this skill whenever the user wants to research a market's pain points, find out what a market struggles with or complains about, find problems worth solving, choose where (or whether) to focus or pivot based on market evidence, do customer discovery or jobs-to-be-done research from public sources, or run a "sales safari", even if they don't name this skill. Not for running live interviews or surveys.
---

# Market pain research

Find out what a market struggles with, in its own words, and how well the evidence supports each struggle, so that a decision about where to focus can follow from the evidence rather than from anyone's existing plans.

The output is one document with two parts:

1. **Findings**: a one-page executive summary with a decisions table, then the evidence base, a ranked chart of themes, theme detail, the market's vocabulary, reported numbers, job stories to test, adoption risks, gaps and next steps.
2. **Evidence index**: every finding ID with its title, speaker and source link.

## Inputs

| Input | Required | Default |
|---|---|---|
| Target market | Yes | Ask if missing. Accept a rough description and sharpen it in the plan. |
| Specific sources (Slack groups, Discord servers, forums, publications) | No | Four default source types only |
| Purpose or decision context | No | The neutral purpose in `references/deliverable.md` section 1 |
| Where to save working files | No | `research/pain-<market-slug>-<YYYY-MM-DD>/` in the working directory |

Do not ask more questions than you need. If the market is clear, state your defaults in one line and start.

## The rules that matter most

These come from the skill owner's corrections. Keep them in mind at every step.

- **Neutral by default.** The research describes the market's pains, ranked by evidence. Never infer a product, company or goal from context (an email domain, an employer, prior projects, files on disk) and never frame the analysis around one. Use a product lens only if the user asks for one in the current request; if one seems useful, ask.
- **Passive and polite.** Read only. Never post, register, log in to read, message, or get around a block. Skip communities whose rules forbid research. Record ordinary people by role, never by name or handle. Keep quotes to 15 words.
- **Evidence you can trace.** Every finding has a source link and an ID; every number in the deliverable comes from the script's outputs.
- **Vendor voices are labelled.** People who sell into a pain describe it differently. Every finding records whether the speaker is a vendor or consultant, and every theme reports its vendor share.
- **Plain words in the deliverable.** No method, author or book names, and none of the method's jargon. The reader needs the findings, not the scaffolding.

## Workflow

Tell the user at the start that a full run sends four or five parallel research agents and usually takes 30-60 minutes.

### 1. Open the document (if Claude Docs is available)

This skill's deliverable is a document, so invoking it counts as asking for one, unless the user asked for a different format (a file, a chat summary). If a Claude Docs connector is present, follow its instructions, which take precedence: at the time of writing they ask that a requested doc be created as the first call, as a skeleton with a pending block for each section. Create "<Market> Pain Research" with a byline (date and author) and one pending block for each of: Executive summary (with Decisions for this review), Evidence base, Ranked problems, Theme detail, How buyers describe the problem, Reported numbers for sizing, Job stories to test, Adoption risks, Confidence and gaps, Next steps, Sources. Open it, then continue. Without the connector, skip this step; the deliverable is built at step 7.

### 2. Plan

Read `references/method.md` (sections 2-4 and 9 at least). Then write `plan.md` in the run folder with:

- **Market definition:** who performs the job, where they work, who decides and pays, exclusions.
- **Purpose:** the user's words, or the neutral default.
- **Job areas:** 8-13 domains of the market's work, derived from the job itself (method.md section 2). Collectors tag every finding with one, so fix the list now.
- **Source plan:** for each of the four source types (P expert voices, N newsletters and trade press, F peer forums, R reviews), adapted to the market, five to ten candidate sites found by quick searches using the watering-hole patterns. Add an S slice for user-named sources.
- **User-named sources:** for each, the access path (an available connector, or none) and the result of reading its rules. Drop any whose rules forbid research, or that you cannot read without new credentials, and tell the user.
- **Recency window:** the last three years unless the market moves faster or slower.

### 3. Collect

Read `references/collection-brief.md`. Fill its collector prompt once per source type and launch all collectors in a single message so they run in parallel. Give each its own raw file, with the run folder as an absolute path. Use the S-slice variant for user-named sources.

While they run, do not edit their files. When each finishes, note its count and blocked sites. If a slice comes back with fewer than about 15 findings, consider one follow-up collector for the same type with different sites; it writes `raw/<letter>-<slug>-2.md` and continues the IDs from the first file's last one.

Without a sub-agent tool, run the slices one after another yourself (collection-brief.md section 7).

### 4. Check, deduplicate, audit vendors

Read `references/coding-and-synthesis.md` sections 1-2. Run the script:

```bash
python3 <this skill's folder>/scripts/research_index.py <run folder>
```

Fix the problems listed in `build/checks.md`, drop duplicates in `coding.json` with a reason, and re-audit every vendor tag. Run `python3 <this skill's folder>/scripts/research_index.py --selftest` if you suspect the script itself.

### 5. Code themes and build

Follow coding-and-synthesis.md sections 3-5: read all findings, draft 10-16 problem-named themes (34 characters at most), assign each finding to one to three themes (or mark it uncoded with a reason), merge or split. When coding is final, renumber once so theme 1 has the most findings:

```bash
python3 <this skill's folder>/scripts/research_index.py <run folder> --renumber
```

Read `build/theme-stats.md` and `build/totals.md`, write the main finding as a sentence with its numbers, and rebuild with it as the chart title:

```bash
python3 <this skill's folder>/scripts/research_index.py <run folder> --chart-title "<the main finding, with its numbers>"
```

The build applies the confidence rule and evidence groups; do not override them by judgment. `build/checks.md` must be clean (or list only confirmed drops) before you write.

If Python is unavailable, compute the same tables by hand from the rules in coding-and-synthesis.md and double-check every count.

### 6. Synthesize

Write `synthesis.md` (coding-and-synthesis.md section 6): theme sheet, vocabulary, reported numbers, job stories (at least one per high- and medium-confidence theme), adoption risks, gaps, and two to four decisions. Plan the writing with the five questions in `references/writing-standard.md` section 2 and write the main message as one sentence.

### 7. Write the deliverable

Follow `references/deliverable.md` for every section, and `references/writing-standard.md` for every sentence. In Claude Docs, fill one section per call, build the chart from `build/chart-module.jsx`, look at a screenshot of it, add the Evidence index tab from `build/evidence-index.md`, and rename the main tab "Findings". Without Claude Docs, use the fallbacks in deliverable.md section 6.

### 8. Revise and verify

Run the final checks in deliverable.md section 7 and the revision pass in writing-standard.md section 6. Fix everything marked "revise". Re-read the summary as if you were the reviewer seeing it for the first time.

### 9. Report back

In chat, keep it short: the link or file paths, the main message in two or three sentences, the counts (findings, themes, vendor share), the most important gaps, and that the doc is private until shared. Offer the next step (buyer interviews) without starting it.

## Reference files

| File | Read when |
|---|---|
| `references/method.md` | Step 2: market definition, watering holes, source types, what counts as a finding, access and privacy rules |
| `references/frameworks.md` | When you need the reasoning behind job areas, forces, job stories, buyer interviews or sizing |
| `references/collection-brief.md` | Step 3: run folder, record format, collector prompts, user-named sources |
| `references/coding-and-synthesis.md` | Steps 4-6: dedupe, vendor audit, theme coding, confidence rule, groups, synthesis notes, neutrality rules |
| `references/deliverable.md` | Steps 1 and 7-8: outline, section specs, Evidence index, Claude Docs notes, fallbacks, final checks |
| `references/writing-standard.md` | Steps 6-8: planning, structure, sentences, revision rubric |
| `scripts/research_index.py` | Steps 4-5: parses raw files, applies coding, writes every count, table and chart |
| `assets/chart-module.jsx` | Used by the script to produce the Claude Docs chart; edit only to change the chart's design |

## Tools and fallbacks

| Capability | Used for | If missing |
|---|---|---|
| Web search and fetch | Finding and reading sources | Required; stop and tell the user |
| Sub-agents | Parallel collection | Run slices sequentially |
| Browser automation | Pages that need rendering | Optional; skip those pages and note them |
| Connectors for user-named sources (for example Slack) | Reading those communities | Skip the source and tell the user |
| Claude Docs | The two-tab document | HTML page via an Artifact tool, else two Markdown files |
| Python 3.9+ | The index script | Compute by hand from the rules |
