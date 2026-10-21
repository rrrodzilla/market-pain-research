# Deliverable: the Findings and Evidence index artifacts

The run produces one document with two parts:

- **Findings**: a review document that a senior reader (for example a principal product manager or an executive) can decide from. It opens with a one-page executive summary.
- **Evidence index**: every finding ID with its title, speaker and source link, so any claim can be traced in one click.

In Claude Docs these are two tabs of one doc. Without that connector, see section 6 for fallbacks.

## Contents

1. Rules that apply to every sentence
2. Findings tab: outline
3. Findings tab: section specifications
4. Evidence index tab
5. Building it in Claude Docs
6. Fallbacks
7. Final checks

## 1. Rules that apply to every sentence

These rules come from corrections by the skill's owner. Breaking any of them makes the deliverable unusable.

- **Purpose comes only from the user.** State the purpose the user gave, in their terms. If they gave none, use: "This research asks which problems [market] report most, and how well the evidence supports each, to inform a decision about where, if anywhere, to focus." Never infer a product, company, or goal from context (an email domain, an employer, earlier projects, files on disk) and never frame findings around one.
- **No product lens unless asked in this request.** No section mapping themes to a product, no "fit" or "opportunity for us" language. If such a comparison seems useful, ask the user first.
- **No method, author or book names in the prose.** Describe what was done in plain words ("we read N posts, episodes, articles and reviews without contacting anyone; each finding is tagged by theme, source type, and whether the speaker sells into the pain"). Avoid the method's jargon too: write "relieves pain" and "saves or makes money", not the method's names for them; write "buyer interviews", not a named interview technique.
- **Every number comes from `build/`.** Totals, percentages, counts and IDs are copied from the script's outputs, never computed in your head. After writing, check each number against its file.
- **Theme numbers are stable identifiers.** Refer to themes by number and short name the same way in the summary, decisions table, chart, theme table and job stories.
- **Vendor share travels with every claim.** Whenever a theme is presented as important, its vendor share is visible nearby.
- **Quotes stay short.** At most 15 words, attributed by role. No usernames.
- **House style.** No em dashes; use commas, colons, parentheses or separate sentences. Sentence-case headings. Follow `writing-standard.md`.

## 2. Findings tab: outline

Title: "<Market> Pain Research" (for example "Enterprise Finance Pain Research"). Under the title, a byline line with the date and the author.

1. Executive summary
   - Decisions for this review (third-level heading inside the summary)
2. Evidence base
3. Ranked problems (the chart)
4. Theme detail
5. How buyers describe the problem
6. Reported numbers for sizing
7. Job stories to test
8. Adoption risks
9. Confidence and gaps
10. Next steps
11. Sources

Keep this order: it moves from the decision (summary) to the evidence that supports it, then to what to do next. The summary and decisions table must fit on about one page.

## 3. Findings tab: section specifications

### Executive summary

Four parts, in this order:

1. **Purpose and scope** (one paragraph, two sentences): the purpose (section 1 rule), then what was read: "We read N accounts on YYYY-MM-DD from [source types in plain words]." Say "public accounts" only if there is no user-named private source.
2. **Main message** (one paragraph, two or three sentences): which pains are well supported, named; how many themes lean on vendor voices; and the limit that matters most to the decision. A good closing sentence, when it is true: "The research shows where the pain is, not who will pay to remove it."
3. **Bullets** (three to five), one per evidence group plus at most one on vocabulary, each opening with a bold sentence that carries the message. The wording below is an example from a past run; replace every number and theme with this run's values from `build/`:
   - "**Themes 1-4 are well supported.**" Name them with finding counts; say how many source types they appear in; give the vendor share for the group.
   - "**Seven themes are vendor-heavy.**" List their numbers and the vendor share; name any notable ones with their percentages.
   - "**Themes 7, 9, 11 and 12 are independent but limited.**" Name them with counts; say what limits them (volume or source-type breadth, not vendor influence).
   - Optional: "**Buyers describe a [X] problem more than a [Y] problem.**" With the word counts from `vocabulary.md`, only if the contrast is clear.
   Leave out a group that has no themes, and say so in one clause instead.
4. **Gaps** (one sentence): the coverage gaps most likely to change the picture.

Then **Decisions for this review**: one sentence ("This review should make N calls. Record each in the Decision column, and comment on any cell you challenge."), then a table. The rows below are an example from a past run; write this run's calls and numbers:

| Call | Basis | Decision |
|---|---|---|
| Treat themes 1-4 as established pains when deciding where to focus | 104 findings across all four source types; 13% from vendors or consultants | Open |
| Treat the seven vendor-heavy themes (…) as unvalidated until interviews | 68 findings; 47% from vendors or consultants | Open |
| Approve 5-10 buyer interviews, as planned in Next steps | Interviews are the only planned test of willingness to pay, the job stories and the vendor-heavy themes | Open |

Two to four calls, each a decision the evidence can inform, each with its basis in numbers. The Decision column is a choice field (Open, Accepted, Changed, Rejected) when the medium supports it, else the word "Open".

### Evidence base

One paragraph: how many findings, the date, that no one was contacted, how findings are tagged, and which source types are the candid layer and which carry the vendor voices (from `totals.md`). Then a table:

| Source type | What was read | Findings | Vendor or consultant findings | Whose voice |
|---|---|---|---|---|

with a Total row. Then one paragraph: finding IDs use the letter in the first column (give an example ID); a dagger (†) marks a speaker whose employer sells into the pain, a consultant, or a vendor-paid survey; every ID is listed with its source in the Evidence index.

### Ranked problems

The chart (from `build/chart-module.jsx` or `build/theme-chart.svg`), then one or two sentences on what the picture shows that the summary did not already say, for example the minimum independent share of the well-supported themes. Do not restate the bar values. The chart's title states the finding with its numbers; its caption names the source: "Source: Evidence index tab, N findings collected YYYY-MM-DD."

### Theme detail

One paragraph naming the high-confidence themes and which themes rate low and why (count or vendor share). One paragraph stating the confidence rule in plain words (High = 15+ findings from at least four source types, or every type collected if fewer, with under a third from vendors or consultants; Low = fewer than 8, or half or more from vendors or consultants; Medium = the rest), and any surprise the rule produces (for example a theme ranked lower by count but higher by confidence). Then the table:

| # | Theme | The pain | Value | Confidence | Key evidence |
|---|---|---|---|---|---|

- **The pain:** the one-sentence pain statement from `synthesis.md`, concrete and solution-free.
- **Value:** Relieves pain, Saves or makes money, or Both (choice field when supported).
- **Confidence:** High, Medium or Low from `theme-stats.md` (choice field when supported).
- **Key evidence:** three to six IDs, independent voices first, then vendor voices with †.

End with one sentence: "Key evidence lists independent voices first, then vendor or consultant voices (†)."

### How buyers describe the problem

One paragraph. Lead with the message the vocabulary supports; follow with the counts from `vocabulary.md`. Report counts, not inferences beyond them.

### Reported numbers for sizing

One paragraph with the main message about the numbers and their reliability (for example "each comes from one user of one product, so treat them as ranges, not benchmarks"). Then a table:

| Measure | Reported value | Source | Source type |
|---|---|---|---|

Source = finding ID with † where it applies, plus role and context. End with a sentence on what is unaudited or vendor-sourced.

### Job stories to test

One paragraph: the stories are hypotheses no buyer has tested; every high- and medium-confidence theme has at least one story; name any story that rests only on low-confidence themes. Then:

| # | Job story | Themes | What would confirm it in interviews |
|---|---|---|---|

Each story follows "When…, I want…, so I can…". The confirmation column names a concrete past event or artifact an interviewee could describe.

### Adoption risks

One paragraph with the single objection most likely to stall a change, with its evidence and how many sources support it. Then bullets, each opening with a short bold label for a risk the anxiety and habit tags actually show (labels from a past run, for example: tool skepticism, implementation cost, abandonment after launch, staff fear). Include only risks with tagged evidence. Cite IDs; mark single-source risks as such.

### Confidence and gaps

One paragraph: what the sample can and cannot show, and whose voices are strong or thin. Then bullets: blocked or skipped sources by name, under-represented roles or segments, skews (polished on-record speakers, vendor-leaning commenters), and the counting caveat (one finding can support several themes).

### Next steps

A checklist. Lead with buyer interviews: how many, with whom (roles and company size that match the market), anchored on a recent purchase or switch, what to ask, how to recruit (asking moderators first, and naming communities whose rules ban research). Then: test each job story against its confirmation signal; probe the vendor-heavy themes; fill the named coverage gaps; and "If a focus is chosen, write a measurable target for it and size it with the reported numbers."

### Sources

One sentence linking to the Evidence index tab, then the sites read with finding counts per source type (from the "Sites read" section of `totals.md`).

## 4. Evidence index tab

Tab name: "Evidence index". Content:

1. A lead paragraph: what the tab holds, how IDs are formed, what † means, and that links open the original page (links into private communities open only for their members). Mention that forum, review and community speakers are recorded by role only.
2. For each source type, a second-level heading with the source type's name, then its table from `build/evidence-index.md` (ID | Finding | Speaker | Source). Paste the tables as generated; do not retype them.

## 5. Building it in Claude Docs

When a Claude Docs connector is available, its own instructions take precedence over this section. Load its docs skill if the client lists one, otherwise call its `guide` tool for `topic.index`, then `topic.tabs` and `topic.charts` before the steps that need them. At the time of writing, the connector expected the following, which fits this skill's flow:

1. **Skeleton first.** This skill's deliverable is a document, so invoking it is a request for one, unless the user asked for another format. The connector asks that a requested doc be born as the first call of the turn: the title, a byline (a date block and a mention of the current user), and one `pending` block per section of the outline in section 2, each with an intent such as "Theme detail: filled after coding". So create it at the start of the run, before research, and open it with the Artifact tool's `open` action (or give the link). Tell the user in one line that sections fill as research completes.
2. **Fill one section per call** by replacing its pending block with the heading and body. Keep a short chat line between calls about what is being filled.
3. **Choice fields.** Create each choice list once (Decision, Value, Confidence) as an `enum` object in a `batch`, then place `dropdown` blocks in table cells (`{"type": "dropdown", "enum": "<enum id>", "index": <option index>}` referenced by `<?claude block id?>` tokens in the markdown).
4. **Chart.** Create the widget from `build/chart-module.jsx` (it is already a single `<claude.Visualize>` tag with inline rows, `datum` stamps, named groups and text ids) and embed it in the Ranked problems section with the caption from section 3. Then take a screenshot through the connector's `read` of the widget and fix any clipped or overlapping labels; long theme names are the usual cause.
5. **Evidence index tab.** Add a second tab named "Evidence index" ordered after the main tab, fill it, and put a mention chip to it in the Sources section. Rename the main tab "Findings".
6. **Privacy.** The doc is private to the user until they share it. Say so in the closing message.

## 6. Fallbacks

- **No Claude Docs, but an Artifact or HTML publishing tool is available:** build one HTML page with two tab buttons, "Findings" and "Evidence index", following that tool's design rules. Inline `build/theme-chart.svg` in Ranked problems. Use plain text "Open" in the Decision column.
- **No publishing tool:** write `findings.md` and `evidence-index.md` into the run folder, embed or link `build/theme-chart.svg` from `findings.md`, and give the user the paths.
- **Any medium:** the content and rules above do not change.

## 7. Final checks

Before telling the user the work is done:

1. Read only the headings and first sentences of each section: the argument must hold on its own.
2. Check every number in the summary, decisions table and chart caption against `build/` files.
3. Search the text for terms that must not appear, and remove them: "sales safari", "watering hole", "jobs to be done", "JTBD", "painkiller", "money multiplier", "switch interview", "forces of progress", "value proposition canvas", "value equation", any author or book name, the em dash character, and any product or company framing the user did not request.
4. Confirm the theme numbers match across summary, decisions, chart and tables.
5. Confirm every high- and medium-confidence theme has a job story.
6. Look at the chart as rendered, if the medium allows; if no picture is available, say so rather than claiming it was checked.
7. Run the revision pass in `writing-standard.md`.
