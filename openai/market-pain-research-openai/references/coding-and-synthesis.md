# Coding and synthesis

This file turns the raw findings into themes, counts and the material the deliverable needs. The orchestrator (the main session) does this work, not the collectors, because themes must be coded consistently across every source type.

## Contents

1. Merge, deduplicate and check
2. Audit the vendor tags
3. Code themes
4. Build and renumber
5. Confidence and evidence groups
6. Synthesis notes
7. Rules that keep the analysis neutral

## 1. Merge, deduplicate and check

Run the script once before coding:

```bash
python3 <skill>/scripts/research_index.py <run folder>
```

Read `build/checks.md` and fix each problem in the raw files (missing URLs, long phrases, wrong ID letters, missing vendor fields). Then read every finding (`build/findings.json` is the easiest view) and look for duplicates: the same person making the same remark in two places, or two collectors recording the same post. Keep the richer one and drop the other in `coding.json`:

```json
{"F17": {"drop": "duplicate of P04: same CFO, same remark"}}
```

Never drop a finding because it is inconvenient. Drop only duplicates and findings outside the market definition, and give the reason.

## 2. Audit the vendor tags

Collectors tag vendors inconsistently, so re-check every finding. A finding is vendor (†) when any of these is true:

- the speaker's employer sells a product or service that addresses the pain they describe
- the speaker is a consultant, advisor, agency or fractional executive whose clients buy help with that pain
- the statistic comes from a survey or report that such a company sponsored
- the speaker promotes their own product, course or service in the same post

A finding is not vendor merely because the speaker works at a software company: a CFO of a software company describing their own finance team's pain is a practitioner. Look up the speaker's employer when the role is ambiguous.

Record corrections in `coding.json`, always with a reason:

```json
{"N25": {"vendor": "yes (survey sponsored by a reporting-software vendor)"},
 "P11": {"vendor": "no (CFO describing their own team; employer sells unrelated products)"}}
```

## 3. Code themes

A theme is a recurring obstacle to the market's job, described as a problem. Build themes from the findings, not from a list prepared in advance.

1. **Read everything first.** Skim all findings across source types before naming any theme.
2. **Draft 10 to 16 themes.** Fewer hides real differences; more spreads the evidence too thin for any theme to reach high confidence.
3. **Name each theme as the obstacle,** in at most 34 characters (the chart's label width): "Numbers arrive late", "Manual work around systems", "Automation stops at exceptions". Do not name a solution ("Need better AI"), a product, or a vendor category.
4. **Assign each finding to one to three themes.** Most findings support one. A finding that fits no theme stays out only if it is truly isolated: mark it `{"uncoded": "<reason>"}` in `coding.json`. `totals.md` reports how many findings sit outside every theme, and the deliverable states that number in Confidence and gaps.
5. **Write a one-sentence pain statement** per theme in `synthesis.md`: who struggles with what, in which situation. Key these notes by theme name, not number, because renumbering (section 4) changes the numbers.
6. **Merge or split** after the first count: merge two themes whose findings describe the same obstacle in different words; split a theme whose findings describe two different obstacles.

Write the results. `themes.json`:

```json
[{"n": 1, "name": "Manual work around systems"},
 {"n": 2, "name": "Multi-entity and intercompany"}]
```

`coding.json`, one entry per finding, merged with any drop and vendor entries:

```json
{"F01": {"themes": [12]}, "F02": {"themes": [1, 9]}, "F33": {"uncoded": "isolated remark about payroll tax"}, "N25": {"themes": [7], "vendor": "yes (survey sponsored by a reporting-software vendor)"}}
```

## 4. Build and renumber

When coding is stable, renumber so that theme 1 has the most findings:

```bash
python3 <skill>/scripts/research_index.py <run folder> --renumber
```

Renumbering rewrites `themes.json` and `coding.json`. Run it once, after the last merge or split; theme numbers then stay fixed for the deliverable. Then read `theme-stats.md` and `totals.md`, choose the chart title (below), and rebuild:

```bash
python3 <skill>/scripts/research_index.py <run folder> --chart-title "<the finding, as a sentence with its numbers>"
```

The build writes `build/`. Every number in the deliverable comes from these files:

| File | Use |
|---|---|
| `totals.md` | Evidence base table; group totals for the executive summary; findings outside every theme; findings by job area (for gaps); sites read |
| `theme-stats.md` / `.json` | Theme table, confidence, limits, evidence IDs, value counts and value |
| `vocabulary.md` | Word and force tallies |
| `evidence-index.md` | The index tab, as is |
| `theme-chart.svg` | The portable chart; `chart-module.jsx` is a compatibility output and is not used by this version |
| `checks.md` | Must say "No problems found", or list only drops you have confirmed, before writing |

The chart title states the main finding with its numbers, for example "Four themes are well supported; seven lean on vendor voices". Until it is set, `checks.md` flags the placeholder.

## 5. Confidence and evidence groups

The script applies these rules. Do not override them by judgment; if a rule produces a result that seems wrong, say why in the deliverable's "Confidence and gaps" section instead.

**Confidence per theme**

| Level | Rule |
|---|---|
| High | At least 15 findings, from at least four source types (or from every type collected, if fewer than four), and vendors supply under a third |
| Low | Fewer than 8 findings, or vendors supply half or more |
| Medium | Everything else |

**Value per theme.** A finding marked `both` counts toward each kind. A kind qualifies when its findings make up at least a third of the theme's findings that have a value. The theme is Both when both kinds qualify; otherwise it takes the one kind that does: Relieves pain, or Saves or makes money.

**Evidence groups.** Every theme falls into exactly one group. The groups, not a product lens, organize the executive summary.

| Group | Rule | What it means for the reader |
|---|---|---|
| Well supported | High confidence | Treat as established for planning |
| Vendor-heavy | Not high, and vendors supply a third or more | Treat as unvalidated: the people describing it have a reason to |
| Independent but limited | The rest | Credible voices, but too few or from too few source types |

A finding counts once under each theme it supports, so theme totals add up to more than the number of findings. Say so wherever totals appear.

## 6. Synthesis notes

Write `synthesis.md` before drafting the deliverable. It is a working file for you, not for the reader, and it holds:

1. **Theme sheet.** For each theme: number, name, pain statement, value (the `value` that `theme-stats.md` reports, from the rule in section 5), confidence, group, limit, and three to five representative finding IDs with their phrases.
2. **Vocabulary.** From `vocabulary.md`: the ten most frequent terms with counts, and any contrast that shows how the market frames its problems (for example control and evidence words against speed and ease words). Report counts, not interpretations the counts do not support.
3. **Reported numbers.** Every quantified cost, time, headcount or rate in the findings: the number, what it measures, the finding ID, and whether it is vendor-sourced. These are reported, not verified; the deliverable says so.
4. **Job stories.** At least one for every high- and medium-confidence theme, in the form "When…, I want to…, so I can…", each citing the finding IDs it rests on. Build them from the findings' situations and words; do not invent circumstances.
5. **Adoption risks.** Patterns in the anxiety and habit tags (see `force_counts` in `theme-stats.json`): what makes the market hesitate to change, and the workarounds a new approach would have to beat. Cite IDs.
6. **Gaps.** Blocked or skipped sources, roles or segments the sample under-represents, source types that came back thin, job areas with few findings (`totals.md`, "Findings by job area"), findings left outside every theme, and the date window. Take source gaps from the coverage sections of the raw files.
7. **Decisions.** Two to four decisions the reader can make from this evidence (see `deliverable.md`, "Decisions for this review").

## 7. Rules that keep the analysis neutral

The research exists to show where the market's pain is, so that a decision about where to focus can follow from the evidence. These rules protect that:

- **Rank and group by evidence alone.** Theme order comes from finding counts; groups come from the confidence rule.
- **No product or company lens unless the user asked for one in this request.** Do not infer a product, company or goal from context such as the user's email domain, employer, past projects or files on disk. If you think a comparison with a specific offer would help, ask the user; do not build it in and label it optional.
- **Describe pains, not solutions.** Theme names, pain statements and job stories leave the solution open.
- **Report vendor share everywhere it matters,** including for themes that look attractive.
- **Keep negative and null results.** A theme with little support, a source type that produced nothing, or a hypothesis the user mentioned that the evidence does not support all belong in the deliverable.
