# market-pain-research

A market research skill with separate Claude and OpenAI versions that finds out what a market struggles with, in its own words, and delivers a review document you can decide from. You name a market, for example "small window cleaning businesses" or "independent veterinary clinic owners". The skill reads where that market already talks, codes 100 to 200 findings into ranked themes, and reports how well the evidence supports each theme, including how much of it comes from people who sell into the problem.

The research is passive. It reads public forums, podcasts, trade press and product reviews, plus any communities you name (such as Slack channels you belong to), without posting, registering or contacting anyone.

The original Claude package stays at the repository root. The self-contained OpenAI package lives in [`openai/market-pain-research-openai/`](openai/market-pain-research-openai/SKILL.md). It uses available ChatGPT or Codex tools, retains Markdown and SVG outputs, and uses sequential collection when delegation is unavailable or prohibited.

## What you get

One document with two parts:

- **Findings.** A one-page executive summary with a table of decisions for the reader, then the evidence base, a ranked chart of themes, theme detail with confidence ratings, the market's own vocabulary, reported numbers for sizing, job stories to test in interviews, adoption risks, gaps and next steps.
- **Evidence index.** Every finding ID with its title, speaker role and source link, so any claim traces back to its source in one click.

The Claude version uses one doc with two tabs when its Docs connector is available, with HTML and Markdown fallbacks. The OpenAI version retains `findings.md`, `evidence-index.md`, and the generated SVG, and uses available native document tools for requested documents.

Every count, percentage and confidence rating comes from a bundled script, not from the model's arithmetic.

## How a run works

1. **Plan.** Sharpen the market definition, fix the list of job areas, and pick candidate sites for four source types: expert voices (podcasts and interviews), newsletters and trade press, peer forums, and reviews of the market's tools.
2. **Collect.** Four or five research agents run in parallel, one per source type. Each records 25 to 40 findings in a strict format: source link, speaker role, vendor flag, a short quote, context, value, forces, the speaker's own terms, and job area.
3. **Check.** The script flags format problems. Duplicates are dropped with a reason, and every vendor flag is audited again.
4. **Code.** Findings are grouped into 10 to 16 themes, each named as a problem. The script ranks the themes and applies a fixed confidence rule.
5. **Write.** The deliverable follows a strict plain-language standard, and every number in it is checked against the script's output.

The Claude workflow estimates 30 to 60 minutes for a full parallel run. The OpenAI version reports its actual collection mode; duration depends on source access and available tools.

## Install

### Claude Code

For Claude Code, at the user level:

```bash
git clone https://github.com/rrrodzilla/market-pain-research.git ~/.claude/skills/market-pain-research
```

For a single project, clone it into `.claude/skills/market-pain-research` inside that project instead. The root package is the original Claude version. Its runtime files and relative paths are preserved. The OpenAI package has a distinct skill name to avoid name collisions; install the specific package for the client you use.

### Codex

From a checkout of this repository, link only the OpenAI package into the current user skill directory:

```bash
mkdir -p ~/.agents/skills
ln -s "$PWD/openai/market-pain-research-openai" ~/.agents/skills/market-pain-research-openai
```

Run these commands from the repository root. The link requires the checkout to remain at that path; copy the complete `openai/market-pain-research-openai` folder instead for an independent installation. An existing destination must be reviewed before replacing it. For repository-scoped use, place the package under `.agents/skills/market-pain-research-openai` in the target project.

Once this change is available in the remote repository, Codex's skill installer can also install `openai/market-pain-research-openai` specifically from `rrrodzilla/market-pain-research`. Do not install the repository root as the OpenAI skill.

### ChatGPT

The same OpenAI skill folder contains the instructions and resources for a ChatGPT environment that supports skills, web retrieval, Python execution, and working files. Use the skill installation or plugin packaging mechanism available in your workspace. Local Codex installation does not install it into ChatGPT. A chat with no skill loader is not an equivalent installation, and uploading only `SKILL.md` leaves out required resources.

For broader distribution, OpenAI recommends packaging reusable skills as plugins. This repository currently supplies the skill folder, not a published plugin. See the [official skills guide](https://learn.chatgpt.com/docs/build-skills) and [plugin skill packaging guide](https://developers.openai.com/plugins/build/skills).

## Use

For Codex, invoke the new version explicitly:

```text
$market-pain-research-openai research the pains of independent veterinary clinic owners
```

In ChatGPT with the skill installed, select it with an `@` mention. Tool availability depends on the host. The OpenAI version checks capabilities before collection and does not claim a verified full run without web retrieval, Python, and writable files. It retains `findings.md`, `evidence-index.md`, and `build/theme-chart.svg`, and can also create a requested document through an available native document tool. Document sharing state is reported only when verified.

For the original Claude version, invoke it by name or describe the research you want:

```text
/market-pain-research find the pains for small window cleaning businesses
```

```text
What do residential HVAC contractors complain about most? Dig through forums and reviews and give me a findings writeup with sources.
```

```text
Research mid-market supply chain planners. Also include the #general and #planning channels of a Slack I'm in.
```

| Input | Required | Default |
|---|---|---|
| Target market | Yes | A rough description is enough; the skill sharpens it in its plan |
| Specific sources (Slack groups, Discord servers, forums, publications) | No | The four default source types |
| Purpose or decision context | No | A neutral purpose: which problems the market reports most, and how well the evidence supports each |
| Where to save working files | No | `research/pain-<market>-<date>/` in the working directory |

## Requirements

The table below describes the original Claude package. The OpenAI capability matrix is in [`references/runtime.md`](openai/market-pain-research-openai/references/runtime.md); it requires Python for verified counts and does not use the manual-count fallback.

| Capability | Used for | If missing |
|---|---|---|
| Web search and fetch | Finding and reading sources | Required |
| Sub-agents | Parallel collection | Source types are collected one after another |
| Python 3.9+ (standard library only) | Counts, tables and the chart | The skill computes the tables by hand from the same rules |
| Claude Docs connector | The two-tab document | An HTML page, otherwise Markdown files |
| Connectors for named sources (for example Slack) | Reading communities you belong to | That source is skipped |
| Browser automation | Pages that need rendering | Optional |

## Research rules

Every collector prompt includes these rules:

- Read only. Never post, comment, register, log in to read, or message anyone.
- Read through the research tools (web retrieval, or a browser for pages that need rendering), never with shell downloads.
- Never get around a block: no proxies, caches, archive mirrors or retries through another tool. Blocked sites are recorded as gaps. Licensed syndication, such as a partner site republishing the same article, is fine.
- Skip communities whose rules forbid research.
- Record forum, review and community speakers by role, never by name or handle. Keep quotes to 15 words.
- Flag vendor voices. A finding is flagged when the speaker sells into the pain, advises buyers on it, cites a vendor-sponsored survey, or promotes their own offer in the same piece.
- Stay neutral. The analysis never assumes a product or goal that the user did not state.

## Confidence rule

| Level | Rule |
|---|---|
| High | 15 or more findings, from at least four source types (or every type collected, if fewer), with under a third from vendors or consultants |
| Low | Fewer than 8 findings, or half or more from vendors or consultants |
| Medium | Everything else |

## Repository layout

| Path | Contents |
|---|---|
| `SKILL.md` | The original Claude workflow |
| `openai/market-pain-research-openai/` | Standalone OpenAI skill, references, copied engine and chart template |
| `openai/evals/evals.json` | OpenAI behavior scenarios, including missing tools and interrupted runs |
| `compatibility/claude-baseline.json` | SHA-256 baseline of original Claude runtime and eval files |
| `tests/test_versions.py` | Baseline, standalone execution, output parity, and confidence checks |
| `references/method.md` | Market definition, where to look, what counts as a finding, access and privacy rules |
| `references/frameworks.md` | The reasoning behind job areas, forces, job stories and buyer interviews |
| `references/collection-brief.md` | Record format and the collector prompt template |
| `references/coding-and-synthesis.md` | Deduplication, vendor audit, theme coding, confidence rule, synthesis notes |
| `references/deliverable.md` | Outline and section specifications for both parts, build notes, fallbacks, final checks |
| `references/writing-standard.md` | The plain-language writing standard and its revision rubric |
| `scripts/research_index.py` | Parses findings, applies coding, and writes every count, table and chart |
| `assets/chart-module.jsx` | The chart template that the script fills for Claude Docs |
| `evals/evals.json` | Test prompts for evaluating the skill |

The script also runs on its own:

```bash
python3 scripts/research_index.py --selftest
python3 scripts/research_index.py <run folder> [--renumber] [--chart-title "The main finding, as a sentence"]
```

## Compatibility and maintenance

Run the compatibility suite with Python 3.9 or newer:

```bash
python3 -m unittest discover -s tests -v
```

The suite checks that the Claude runtime matches the baseline, that shared method and engine files remain identical, and that the OpenAI package runs after being copied outside the repository. A four-source fixture checks counts, vendor shares, confidence groups, evidence URLs, theme renumbering, chart output, and repeat builds. Both engines must produce byte-identical build files. The GitHub Actions workflow is configured to run these checks on Python 3.9 and 3.14.

The OpenAI copies of `method.md`, `frameworks.md`, `writing-standard.md`, `research_index.py`, and `chart-module.jsx` are intentionally identical to their root counterparts. The entrypoint, collection brief, coding reference, and deliverable reference are platform-specific; `runtime.md` is OpenAI-only. Review deliberate shared-method changes in both versions. Do not regenerate the Claude baseline just to make a failure disappear; update it only when an intentional Claude change has been reviewed and verified. The original baseline is commit `0826271`; the baseline file's `revisions` list records each reviewed change since.

The legacy chart template remains in the OpenAI package because the shared engine's self-test checks its JSX output. OpenAI presentation uses the generated SVG and does not execute the Claude component.

The engine and the compatibility tests pass Ruff under the development machine's lint configuration without suppressions.

Automated checks verify packaging and calculations. They do not establish live ChatGPT or Claude behavior, account-specific tool availability, or full research quality. The scenarios in `openai/evals/evals.json` are behavioral test specifications, not recorded passing results. Run them in each target host before claiming end-to-end support. No full live market study is included in the compatibility suite.

## Limits

- The research shows where a market reports pain, not who will pay to remove it. The job stories are hypotheses for buyer interviews; the deliverable plans those interviews, but the skill does not run them.
- Coverage depends on what is public and readable by research tools. Some large communities, such as Reddit and closed Facebook groups, are often out of reach, and the report lists them as gaps.
- Numbers quoted in findings are self-reported by individual speakers and are not verified.

## Acknowledgements

The method condenses ideas from these works, summarized in the skill's own words in `references/`:

- Amy Hoy, Sales Safari (taught in 30x500 with Alex Hillman)
- Jim Kalbach, *The Jobs To Be Done Playbook*
- Superfounder, *Jobs to Be Done: How to Find Painkillers and Money Multipliers*
- Alexander Osterwalder, Yves Pigneur, Greg Bernarda and Alan Smith, *Value Proposition Design*
- Alex Hormozi, *$100M Offers*
- Jean-luc Doumont, *Trees, Maps, and Theorems*

## License

MIT. See [LICENSE](LICENSE).
