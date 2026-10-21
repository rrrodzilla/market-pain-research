# Native runtime capabilities

This package works from its own installed folder. References and scripts belong to this package; do not look for a sibling Claude installation. Resolve resource paths from the skill folder and working paths from the chosen run folder. Quote filesystem paths in shell commands.

## Capability routing

| Capability | Use | If unavailable |
|---|---|---|
| Native web search and source retrieval | Find sources and read evidence | Explain that live collection is blocked; offer analysis of supplied evidence or a research plan |
| Python 3.9+ through shell or code execution | Run the bundled index script and retain deterministic counts | Offer collection or planning only; do not claim a completed, script-verified report |
| Writable files | Raw findings, coding, checkpoint, and exports | Explain that a full reproducible run cannot be saved; offer a bounded chat response |
| Native delegation | Independent collectors with exclusive raw files | Collect sequentially, or queue slices within available slots |
| Browser tools | Inspect permitted pages needing rendering | Skip unreadable pages and record the gap; respect existing access blocks |
| Existing source connectors | Read communities explicitly named by the user | Skip those sources and disclose missing access |
| Native document or Pages tools | Present a requested document | Return Markdown files and SVG instead |
| Image or browser preview | Inspect the generated chart | Use an available SVG converter when needed, or mark visual inspection unverified |

Tool availability differs by ChatGPT surface, Codex runtime, and account. Discover actual capabilities rather than assuming that an app name guarantees a tool. Native search, shell, Python, and connectors need no custom API layer for this workflow. Do not silently substitute an API-based research service.

## Web evidence and citations

Read pages before asserting their contents. Search snippets may identify candidate sites; title-only findings are limited to the explicit exception in the method and must be labeled. Retain source URLs, publication dates where available, speaker roles, and access limitations in the raw findings. Host citation IDs are useful in chat but are not stable source links for downloaded evidence files.

The 15-word limit is a per-quote ceiling, not permission to exceed the host's total quotation or source-use allowance by recording many quotes from one page. Paraphrase where needed. Existing authenticated connectors can read sources within the user's request; the research never opens a login flow or asks for credentials.

## Execution and continuation

In Codex, use the available shell tool to run the script. In ChatGPT with suitable code execution, execute the packaged Python file against the run folder. Do not assume web tools and code execution share paths or network access: pass the retrieved evidence into raw files explicitly and keep browsing in the tools intended for it.

Do not spawn collectors when current instructions prohibit delegation. With delegation, tell each collector its file ownership and that other collectors share the workspace. The main session audits all findings and applies one consistent coding scheme. If a collector returns evidence rather than writing files directly, save it in the required raw format before coding, preserving URLs and limitations.

Use `status.md` as a checkpoint, following collection-brief section 7. Do not claim work continues after the turn ends unless the host actually provides and starts a background task. If interrupted, preserve partial work and state the next action.

## Deliverable handling

Markdown and SVG are the portable baseline. Use local clickable paths in Codex and downloadable attachment links where supported by ChatGPT. Do not return an inaccessible sandbox path as if it were a download. Link the Findings and Evidence index files to each other using relative paths and keep source links as ordinary URLs.

When producing a requested native document, follow the selected document tool's skill and keep the local evidence files. Do not assume a particular tab API, dropdown schema, first-call skeleton rule, or visualization component exists. A rendered SVG or a PNG converted from that SVG is sufficient; generated art is unsuitable for a chart whose values must be exact.

Document creation does not establish its privacy state. Verify sharing through the selected tool if possible; otherwise report that it was not verified. An HTML output can remain a local or downloadable file. Public hosting and changes to sharing require authorization beyond merely asking for a research report.
