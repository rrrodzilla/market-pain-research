# Research method: listen before you ask

This file explains the method behind the skill: where to look, what counts as evidence, and which rules keep the research honest. Read it once at the start of a run. The collector briefs in `collection-brief.md` apply it slice by slice.

## Contents

1. Why passive research comes first
2. Define the market
3. Find the watering holes
4. Choose four vantage points
5. What counts as a finding
6. Classify the value: pain relief or money
7. Capture the market's own words
8. Separate vendor voices
9. Access, privacy and quotation rules
10. When to stop

## 1. Why passive research comes first

People describe their problems most honestly to each other, in places where nobody is selling to them. A forum question, a complaint in a review, or a CFO's aside on a podcast is unprompted: the speaker chose the topic, the words and the emphasis. Interviews and surveys, by contrast, frame the problem for the respondent.

So this method reads first and asks later. It never posts, never joins to read, never contacts anyone. The output is a map of where the pain is and how the market talks about it. It cannot show willingness to pay; buyer interviews test that afterwards (see `frameworks.md`, "Buyer interviews").

The approach follows the "sales safari" practice of reading a market's watering holes, combined with jobs-to-be-done coding. Those names belong in this skill's references only. The deliverable describes what was done in plain words and never names methods, authors or books.

## 2. Define the market

Before searching, write a one-paragraph market definition:

- **Who performs the job:** roles and seniority (for example "controllers, assistant controllers and accounting managers").
- **Where they work:** company size, industry, region, if the user gave them.
- **Who decides and who pays:** these can differ from the job performer; note both.
- **Exclusions:** neighbours who look similar but have different jobs (for example small-business bookkeepers when the market is enterprise finance).

Then derive 8 to 13 **job areas**: the main stages or domains of the work. They come from the market's own job, not from any product. A useful way to find them is to walk the job from start to finish (plan, gather inputs, prepare, execute, check, fix, report, conclude) and name the domains where the work happens. Add `team/skills`, `tools/data` and `other` if the market needs them. Collectors tag each finding with one job area, so the list must be fixed before collection.

Example for enterprise finance: close/consolidation, reconciliation, AP/payments, AR/collections, treasury/cash, FP&A/forecasting, reporting/board, audit/controls/compliance, systems/ERP/data, AI/automation, team/talent, strategy/capital, other.

## 3. Find the watering holes

A watering hole is any place where the market talks among itself. Find candidates by searching the market's role names and job areas with these patterns:

> `[market or role] + forum | community | subreddit | Q&A | mailing list | Slack | Discord | meetup | user group | conference | podcast | newsletter | blog | awards | reviews | "how do I" | "is there a tool" | "anyone else" | template | workaround`

Also search the names of the tools the market uses, followed by "community", "reviews", "alternatives" and "vs". Tool communities and review pages are dense with pain.

Sort what you find into three tiers and record the tier in the coverage notes:

| Tier | What it is | What to do |
|---|---|---|
| 1. Open | Public pages readable without an account: forums, Q&A sites, review sites, podcast pages and transcripts, newsletters and their comments, public social posts | Read them. |
| 2. Joinable | Communities that need a free account or application: Slack and Discord groups, membership forums | Do not join on the user's behalf. If the user is already a member and names it as a source, read it through an available connector only after checking its rules (section 9). |
| 3. Closed | Paid or vetted peer networks, private groups | Record their existence as a coverage gap. Do not try to get in. |

Many joinable communities explicitly ban research, recruiting or vendor activity. Check the community's rules or code of conduct before reading. If the rules forbid it, skip the community and tell the user.

## 4. Choose four vantage points

Different places reveal different layers of the same market. Collect from four distinct source types so that no single layer dominates. Default prefixes, which also become finding-ID letters:

| Prefix | Source type | What it reveals | Typical bias |
|---|---|---|---|
| P | Expert voices: podcasts, recorded interviews, conference talks | Senior perspective, strategy, the "why" behind a pain, numbers on record | Skews senior; hosts and guests often work for vendors |
| N | Newsletters and trade press, including reader comments | Trends, survey results, and in the comments, candid practitioner pushback | Surveys are often vendor-sponsored |
| F | Peer forums and Q&A sites | The most candid layer: real problems in the asker's own words, workarounds, unanswered questions | Skews junior and hands-on; tool-specific |
| R | Reviews of the tools the market uses | What tools fail to do, what buyers wish for, what made them switch | Reviews are about tools, so pains outside tools are missing |
| S | Sources the user names (for example Slack groups) | Whatever that community discusses | Depends on the community |

Adapt the four types to the market. A consumer market might use app-store reviews instead of software review sites and video comments instead of podcasts. A trade with no software might use supplier reviews. Keep the principle: four vantage points that differ in who is speaking and why.

User-named sources become a fifth type (`S`) or replace the closest default type. They do not reduce the other three or four, because the confidence rule (see `coding-and-synthesis.md`) rewards breadth across types.

## 5. What counts as a finding

A finding is one speaker expressing one pain, desire, fear, workaround or cost, at one source. If a speaker raises two separate pains, record two findings. If two speakers in one thread raise the same pain, record two findings.

Strong signals:

- a question that asks for help or for a tool ("how do I…", "is there a way…", "anyone else…")
- a workaround they built: spreadsheets, scripts, extra staff, manual checks
- something they want to stop doing, or keep putting off
- a fear: of an error, an audit finding, a breach, blame, a failed project
- a quantified cost: hours, days, headcount, money, error rates
- a tool switch, and what triggered it
- an unanswered forum question (no one could help, which is itself a signal)

Skip general opinions with no pain behind them, marketing copy, and posts from outside the market definition.

## 6. Classify the value: pain relief or money

Tag each finding with what removing the problem would deliver:

- **Relieves pain:** less anxiety, stress, risk, fear, uncertainty, guilt or frustration.
- **Saves or makes money:** more revenue, more customers, lower cost, higher prices, or time saved.
- **Both:** common, for example a manual process that is both slow and risky.

Guide questions help the collector notice findings they would otherwise skip:

- For pain relief: What do they struggle to do well? What skills do they want? What are they afraid of? What should they be doing but avoid?
- For money: What costs them money or time? What is inefficient? What could be optimized? What do they ignore because fixing it seems too hard?

## 7. Capture the market's own words

Record the words the speaker actually uses for the pain: their jargon, their verbs, their adjectives. These words become the vocabulary tally, which shows how the market frames its problems.

Generic "signal words" (easier, faster, finally, relief) often fail to appear in professional markets. In enterprise finance, for example, speakers said "manual", "control", "visibility", "trust" and "audit" far more than "faster" or "easier". So do not seed collectors with a fixed word list. Ask them to record the speaker's own one-to-three-word terms, then count what emerges.

## 8. Separate vendor voices

Much of what is published about any market comes from people who sell to it. Their accounts of pain may be accurate, but they are not independent: a vendor has a reason to describe the pain its product removes.

Tag a finding as **vendor** (shown as † in the deliverable) when any of these is true. This list is the single definition; `collection-brief.md` and `coding-and-synthesis.md` use it unchanged.

- the speaker's employer sells a product or service that addresses the pain they describe
- the speaker is a consultant, advisor, agency or fractional executive whose clients buy help with that pain
- the statistic comes from a survey or report that such a company sponsored
- the speaker promotes their own product, course or service in the same piece

A speaker who merely works at a software company is not a vendor when they describe their own team's pain. Record the tag as `yes (<reason>)` or `no`, for example `yes (CFO of a close-software vendor)`. The vendor share per theme is one of the main outputs, so this tag must be applied consistently. The orchestrator re-audits every tag after collection.

## 9. Access, privacy and quotation rules

These rules are part of the method, not an add-on. A run that breaks them produces evidence the user cannot use.

- **Read only.** Never post, comment, vote, message, register, or log in to read. Never recruit.
- **One access path.** Read pages with the web retrieval tool, or with a browser tool when a page needs rendering. Do not read sources with shell downloads (curl, wget) or scripts. One path keeps the access record honest: each page was either read or blocked.
- **Respect blocks.** If a site returns a block (such as a 403), a login wall, a rate limit or a bot challenge, pause once and retry once; then skip it and record it as blocked. A block from any tool is a block for that page: do not request the page again through another tool to get past it. Do not use proxies, cache or archive mirrors, or other workarounds. Official syndication is fine: a marketplace that displays a review site's reviews under licence, or a licensed partner that republishes the same article (a news portal carrying a broadcaster's story). Cite the page you read.
- **Respect tool and platform policy.** If a site is off limits to your tools, skip it and record the gap.
- **Respect community rules.** Skip any community whose rules forbid research or recruiting, even if the user has access.
- **Browser automation is optional.** If you use it, open your own tab, decline non-essential cookies, and never enter credentials.
- **Roles, not names, for ordinary people.** Record forum, review and community speakers by role and context ("asker, staff accountant at a 12-entity group"), never by username or real name. People speaking on record in published interviews or press can be named with role and employer, because the employer matters for the vendor test.
- **Short quotes only.** Verbatim phrases are at most 15 words. If no short phrase captures the point, paraphrase and mark it "(paraphrase)". Never copy long passages; summarize in your own words.
- **Private communities are more sensitive.** Quotes from Slack or similar groups are paraphrased by default, with no identifying detail, even when the user is a member.

## 10. When to stop

Each source type aims for 25 to 40 findings, preferring the last two to three years. Stop a slice early when new findings only repeat what is already recorded; that repetition is evidence of saturation, and the coverage notes should say so. Keep going past 40 only if a source type is clearly producing new pains.

A full run usually lands between 100 and 200 findings. Fewer than about 80 makes most themes fall below the confidence thresholds.
