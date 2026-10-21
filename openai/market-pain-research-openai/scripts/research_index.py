#!/usr/bin/env python3
"""Build the evidence index and theme statistics for a market pain research run.

Standard library only; runs on any machine with Python 3.9+.

Usage:
    python3 research_index.py RUN_DIR [--renumber] [--chart-title "The finding, as a sentence"]
    python3 research_index.py --selftest

RUN_DIR layout (references/collection-brief.md defines the record format):
    raw/<PREFIX>-<slug>.md   one file per source type, e.g. raw/P-podcasts.md.
                             PREFIX is one capital letter; finding IDs start with
                             it. The file's first "# " heading is the source
                             type's display name. Tables follow PREFIX_ORDER.
    themes.json              written at coding time:
                             [{"n": 1, "name": "Manual work around systems"}, ...]
    coding.json              written at coding time, keyed by finding ID:
                             {"P02": {"themes": [1, 2], "vendor": "yes (sells X)"},
                              "F07": {"drop": "duplicate of F03"}}
                             "themes" and "vendor" override the raw file;
                             "drop" removes the finding from every output;
                             "uncoded" (with a reason) marks a finding that
                             fits no theme, so checks stop flagging it.

Writes RUN_DIR/build/:
    findings.json      every kept finding, after coding
    evidence-index.md  one table per source type, for the index tab
    totals.md          counts by source type, vendor counts, group totals
    theme-stats.md     per-theme counts, vendor share, confidence, group
    theme-stats.json   the same, machine-readable
    vocabulary.md      tallies of the `words:` and `forces:` fields
    chart-rows.json    rows for the chart
    chart-module.jsx   Claude Docs widget module with rows, title, total filled in
    theme-chart.svg    static chart for HTML or Markdown deliverables
    checks.md          problems to fix before writing the deliverable

Every number the deliverable states should come from these files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

# Confidence rule. Keep in sync with references/coding-and-synthesis.md.
HIGH_MIN_FINDINGS = 15  # High needs at least this many findings ...
LOW_BELOW_FINDINGS = 8  # ... and fewer than this many is Low.
MAX_PHRASE_WORDS = 15  # Verbatim phrases stay short (copyright and privacy).
MAX_CHART_NAME = 34  # Longer theme names collide with the chart's bars.

DEFAULT_TITLE = "CHART TITLE: state the finding as a sentence"
VENDOR_RE = re.compile(r"^(yes|no|y|n|true|false|†)\b", re.I)

# Display order of source types; unknown prefixes follow alphabetically.
PREFIX_ORDER = "PNFRS"

URL_RE = re.compile(r"https?://[^\s|,;)\]>]+")
HEADER_RE = re.compile(r"^([A-Z])(\d+)\.?\s*(.*)$")
FIELD_RE = re.compile(r"^-\s*\*{0,2}([A-Za-z][A-Za-z ]*?)\*{0,2}\s*:\s*\*{0,2}\s*(.*)$")
VALUE_KINDS = ("pain", "money", "both")
FORCE_KINDS = ("push", "pull", "anxiety", "habit", "workaround")


# ---------------------------------------------------------------------------
# Parsing (pure functions)
# ---------------------------------------------------------------------------


def parse_fields(block: str) -> dict:
    """Return the `- key: value` fields of one finding block, keys lowercased."""
    fields = {}
    for line in block.splitlines():
        m = FIELD_RE.match(line.strip())
        if m:
            fields[m.group(1).strip().lower()] = m.group(2).strip()
    return fields


def parse_vendor(value: str) -> tuple[bool, str]:
    """`yes (sells close software)` -> (True, 'sells close software')."""
    v = (value or "").strip()
    is_vendor = bool(re.match(r"^(yes|y|true|†)\b", v, re.I))
    reason = re.sub(r"^(yes|no|y|n|true|false|†)\W*", "", v, flags=re.I).strip(" ()-")
    return is_vendor, reason


def parse_themes(value) -> list[int]:
    if isinstance(value, list):
        return sorted({int(x) for x in value})
    return sorted({int(x) for x in re.findall(r"\d+", value or "")})


def parse_list(value: str) -> list[str]:
    out = []
    for w in re.split(r"[,;]", value or ""):
        w = w.strip().strip("\"'()[]").strip().lower()
        if w and not w.startswith(("none", "n/a")) and w != "-":
            out.append(w)
    return out


def parse_value(value: str) -> str:
    """Normalize the value field to pain, money, both or ''."""
    v = (value or "").lower()
    if "both" in v:
        return "both"
    has_pain = "pain" in v
    has_money = any(k in v for k in ("money", "saves", "save", "revenue", "cost"))
    if has_pain and has_money:
        return "both"
    return "pain" if has_pain else "money" if has_money else ""


def parse_source(value: str) -> tuple[str | None, str, str]:
    """`URL | Site name | date` -> (url, site, date). Missing parts are ''."""
    url_m = URL_RE.search(value or "")
    url = url_m.group(0) if url_m else None
    parts = [p.strip() for p in (value or "").split("|")]
    site = parts[1] if len(parts) > 1 else ""
    date = parts[2] if len(parts) > 2 else ""
    return url, site, date


def host(url: str | None) -> str:
    if not url:
        return ""
    name = url.split("/")[2]
    return name[4:] if name.startswith("www.") else name


def display_name(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def parse_raw_file(text: str, file_prefix: str) -> list[dict]:
    """Parse one raw file into finding dicts. A `same` source inherits the previous URL."""
    findings = []
    last = (None, "", "")
    for part in re.split(r"^### ", text, flags=re.M)[1:]:
        head, _, body = part.partition("\n")
        m = HEADER_RE.match(head.strip())
        if not m:
            continue
        letter, num, title = m.group(1), int(m.group(2)), m.group(3).strip()
        f = parse_fields(body)
        url, site, date = parse_source(f.get("source", ""))
        if not url and f.get("source", "").lower().startswith("same"):
            url, site, date = last
        if url:
            last = (url, site, date)
        is_vendor, vendor_reason = parse_vendor(f.get("vendor", ""))
        findings.append(
            {
                "id": f"{letter}{num:02d}",
                "prefix": letter,
                "file_prefix": file_prefix,
                "title": title,
                "url": url,
                "site": site or host(url),
                "date": date,
                "speaker": f.get("speaker", ""),
                "vendor": is_vendor,
                "vendor_field": f.get("vendor"),
                "vendor_reason": vendor_reason,
                "phrase": f.get("phrase", "").strip(),
                "context": f.get("context", ""),
                "value": parse_value(f.get("value", "")),
                "forces": [x for x in parse_list(f.get("forces", "")) if x in FORCE_KINDS],
                "unknown_forces": [x for x in parse_list(f.get("forces", "")) if x not in FORCE_KINDS],
                "job_area": f.get("job area", ""),
                "words": parse_list(f.get("words", "")),
                "themes": parse_themes(f.get("themes", "")),
                "drop": "",
                "uncoded": "",
            }
        )
    return findings


def apply_coding(findings: list[dict], coding: dict) -> list[dict]:
    """Return copies of the findings with coding.json overrides applied."""
    out = []
    for f in findings:
        c = coding.get(f["id"], {})
        g = dict(f)
        if "themes" in c:
            g["themes"] = parse_themes(c["themes"])
        if "vendor" in c:
            g["vendor_field"] = str(c["vendor"])
            g["vendor"], g["vendor_reason"] = parse_vendor(str(c["vendor"]))
        g["drop"] = str(c.get("drop", ""))
        g["uncoded"] = str(c.get("uncoded", ""))
        out.append(g)
    return out


def prefix_key(prefix: str) -> tuple[int, str]:
    i = PREFIX_ORDER.find(prefix)
    return (i if i >= 0 else len(PREFIX_ORDER), prefix)


# ---------------------------------------------------------------------------
# Statistics (pure functions)
# ---------------------------------------------------------------------------


def confidence(total: int, vendor: int, n_types: int, min_types: int) -> str:
    if total < LOW_BELOW_FINDINGS or vendor * 2 >= total:
        return "Low"
    if total >= HIGH_MIN_FINDINGS and n_types >= min_types and vendor * 3 < total:
        return "High"
    return "Medium"


def group_for(conf: str, total: int, vendor: int) -> str:
    """Partition every theme into exactly one evidence group."""
    if conf == "High":
        return "well supported"
    if total and vendor * 3 >= total:
        return "vendor-heavy"
    return "independent but limited"


def limit_reason(total: int, vendor: int, n_types: int, min_types: int) -> str:
    reasons = []
    if total < HIGH_MIN_FINDINGS:
        reasons.append(f"{total} findings (High needs {HIGH_MIN_FINDINGS}+)")
    if n_types < min_types:
        reasons.append(f"{n_types} of {min_types} source types")
    if total and vendor * 3 >= total:
        reasons.append(f"{vendor} of {total} from vendors")
    return "; ".join(reasons)


def theme_stats(findings: list[dict], themes: list[dict], prefixes: list[str]) -> list[dict]:
    """Per-theme counts. A finding counts once under each theme it supports."""
    min_types = min(4, len(prefixes)) or 1
    names = {t["n"]: t for t in themes}
    numbers = sorted(set(names) | {n for f in findings for n in f["themes"]})
    out = []
    for n in numbers:
        members = [f for f in findings if n in f["themes"]]
        vendor = sum(1 for f in members if f["vendor"])
        total = len(members)
        by_type = {p: sum(1 for f in members if f["prefix"] == p) for p in prefixes}
        n_types = sum(1 for c in by_type.values() if c)
        conf = confidence(total, vendor, n_types, min_types)
        t = names.get(n, {})
        out.append(
            {
                "n": n,
                "name": t.get("name", f"Theme {n}"),
                "total": total,
                "independent": total - vendor,
                "vendor": vendor,
                "vendor_pct": round(100 * vendor / total) if total else 0,
                "by_type": by_type,
                "source_types": n_types,
                "min_types": min_types,
                "confidence": conf,
                "group": group_for(conf, total, vendor),
                "limit": "" if conf == "High" else limit_reason(total, vendor, n_types, min_types),
                "value_counts": {k: sum(1 for f in members if f["value"] == k) for k in VALUE_KINDS},
                "force_counts": {k: sum(1 for f in members if k in f["forces"]) for k in FORCE_KINDS},
                "evidence_ids": [f["id"] for f in members if not f["vendor"]]
                + [f["id"] + "†" for f in members if f["vendor"]],
            }
        )
    return out


def renumber_map(stats: list[dict]) -> dict[int, int]:
    """Map old theme numbers to new ones so that 1 has the most findings."""
    ranked = sorted(stats, key=lambda s: (-s["total"], s["n"]))
    return {s["n"]: i for i, s in enumerate(ranked, start=1)}


def renumber(themes: list[dict], coding: dict, mapping: dict[int, int]) -> tuple[list[dict], dict]:
    new_themes = sorted(({**t, "n": mapping.get(t["n"], t["n"])} for t in themes), key=lambda t: t["n"])
    new_coding = {}
    for fid, c in coding.items():
        c = dict(c)
        if "themes" in c:
            c["themes"] = sorted(mapping.get(n, n) for n in parse_themes(c["themes"]))
        new_coding[fid] = c
    return new_themes, new_coding


def group_totals(stats: list[dict]) -> list[dict]:
    out = []
    for g in ("well supported", "vendor-heavy", "independent but limited"):
        members = [s for s in stats if s["group"] == g]
        total = sum(s["total"] for s in members)
        vendor = sum(s["vendor"] for s in members)
        out.append(
            {
                "group": g,
                "themes": [s["n"] for s in members],
                "total": total,
                "vendor": vendor,
                "vendor_pct": round(100 * vendor / total) if total else 0,
            }
        )
    return out


def tally(items: list[list[str]]) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for words in items:
        for w in set(words):
            counts[w] = counts.get(w, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def checks(findings: list[dict], themes: list[dict], dropped: list[dict], chart_title: str = "") -> list[str]:
    problems = []
    if themes and chart_title in ("", DEFAULT_TITLE):
        problems.append("chart: title is still the placeholder; rebuild with --chart-title \"<the finding>\"")
    seen = set()
    defined = {t["n"] for t in themes}
    used = set()
    for t in themes:
        if len(t.get("name", "")) > MAX_CHART_NAME:
            problems.append(f"theme {t['n']}: name over {MAX_CHART_NAME} characters; shorten it for the chart")
    for f in findings:
        fid = f["id"]
        if fid in seen:
            problems.append(f"{fid}: duplicate ID")
        seen.add(fid)
        if f["prefix"] != f["file_prefix"]:
            problems.append(f"{fid}: ID letter does not match its file prefix {f['file_prefix']}")
        if not f["url"]:
            problems.append(f"{fid}: no source URL")
        if not f["context"]:
            problems.append(f"{fid}: no context")
        if f["vendor_field"] is None:
            problems.append(f"{fid}: no vendor field (run the vendor audit)")
        elif not VENDOR_RE.match(f["vendor_field"].strip()):
            problems.append(f"{fid}: vendor must start with yes or no, not {f['vendor_field']!r}")
        elif f["vendor"] and not f["vendor_reason"]:
            problems.append(f"{fid}: vendor=yes needs a reason (employer, sponsor or client base)")
        phrase = f["phrase"]
        words = len(re.findall(r"\w+", phrase.replace("(paraphrase)", "")))
        if words > MAX_PHRASE_WORDS and "(paraphrase)" not in phrase:
            problems.append(f"{fid}: phrase is {words} words; trim to {MAX_PHRASE_WORDS} or mark (paraphrase)")
        if not f["value"]:
            problems.append(f"{fid}: value is not pain, money or both")
        long_words = [w for w in f["words"] if len(w.split()) > 3]
        if long_words:
            problems.append(f"{fid}: words should be the speaker's own 1-3 word terms, not {long_words[0]!r}")
        if f["unknown_forces"]:
            problems.append(f"{fid}: unknown forces {f['unknown_forces']}; use {', '.join(FORCE_KINDS)}")
        if themes and not f["themes"] and not f["uncoded"]:
            problems.append(f"{fid}: no themes coded (code it, or mark it uncoded with a reason)")
        used.update(f["themes"])
    for n in sorted(defined - used):
        problems.append(f"theme {n}: defined in themes.json but no finding supports it")
    for n in sorted(used - defined) if themes else []:
        problems.append(f"theme {n}: used by findings but missing from themes.json")
    for f in dropped:
        problems.append(f"{f['id']}: dropped ({f['drop']}); confirm before writing")
    return problems


# ---------------------------------------------------------------------------
# Rendering (pure functions)
# ---------------------------------------------------------------------------


def cell(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def truncate(text: str, n: int = 70) -> str:
    text = text or ""
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def render_index(findings: list[dict], names: dict) -> str:
    lines = []
    for p in sorted({f["prefix"] for f in findings}, key=prefix_key):
        lines += [f"## {names.get(p, p)}", "", "| ID | Finding | Speaker | Source |", "| --- | --- | --- | --- |"]
        for f in [f for f in findings if f["prefix"] == p]:
            fid = f["id"] + ("†" if f["vendor"] else "")
            src = f"[{cell(f['site']) or 'link'}]({f['url']})" if f["url"] else "no link"
            lines.append(f"| {fid} | {cell(f['title'])} | {cell(truncate(f['speaker']))} | {src} |")
        lines.append("")
    return "\n".join(lines)


def render_totals(findings: list[dict], names: dict, groups: list[dict]) -> str:
    lines = ["| Source type | Findings | Vendor or consultant |", "| --- | --- | --- |"]
    for p in sorted(names, key=prefix_key):
        fs = [f for f in findings if f["prefix"] == p]
        lines.append(f"| {names[p]} ({p}) | {len(fs)} | {sum(f['vendor'] for f in fs)} |")
    lines.append(f"| Total | {len(findings)} | {sum(f['vendor'] for f in findings)} |")
    lines += ["", "| Group | Themes | Theme findings | Vendor | Vendor share |", "| --- | --- | --- | --- | --- |"]
    for g in groups:
        themes = ", ".join(str(n) for n in g["themes"]) or "none"
        lines.append(f"| {g['group']} | {themes} | {g['total']} | {g['vendor']} | {g['vendor_pct']}% |")
    lines += ["", "Theme findings count a finding once under each theme it supports, so they can exceed the total."]
    uncoded = [f["id"] for f in findings if not f["themes"]]
    lines += ["", f"Findings outside every theme: {len(uncoded)}" + (f" ({', '.join(uncoded)})" if uncoded else "")]
    lines += ["", "## Findings by job area", "", "| Job area | Findings | Vendor |", "| --- | --- | --- |"]
    for area, count in tally([[f["job_area"].lower() or "not tagged"] for f in findings]):
        vendor = sum(1 for f in findings if (f["job_area"].lower() or "not tagged") == area and f["vendor"])
        lines.append(f"| {cell(area)} | {count} | {vendor} |")
    lines += ["", "## Sites read, with findings from each", ""]
    for p in sorted(names, key=prefix_key):
        sites = tally([[f["site"] or "unknown"] for f in findings if f["prefix"] == p])
        lines.append(f"- {names[p]}: " + ", ".join(f"{s} ({c})" for s, c in sites))
    return "\n".join(lines)


def render_stats(stats: list[dict]) -> str:
    lines = [
        "| # | Theme | Findings | Indep. | Vendor | Vendor % | Source types | Confidence | Group "
        "| Pain/money/both | Limit | Evidence |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for s in stats:
        v = s["value_counts"]
        lines.append(
            f"| {s['n']} | {cell(s['name'])} | {s['total']} | {s['independent']} | {s['vendor']} | "
            f"{s['vendor_pct']}% | {s['source_types']}/{s['min_types']} | {s['confidence']} | {s['group']} | "
            f"{v['pain']}/{v['money']}/{v['both']} | {cell(s['limit'])} | {', '.join(s['evidence_ids'])} |"
        )
    return "\n".join(lines)


def render_tally(rows: list[tuple[str, int]], label: str) -> str:
    return f"| {label} | Findings |\n| --- | --- |\n" + "\n".join(f"| {w} | {c} |" for w, c in rows)


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:40] or "theme"


def chart_rows(stats: list[dict]) -> list[dict]:
    return [
        {
            "n": s["n"],
            "slug": slugify(s["name"]),
            "theme": s["name"],
            "ind": s["independent"],
            "ven": s["vendor"],
            "conf": s["confidence"],
        }
        for s in stats
        if s["total"]
    ]


def js_literal(value) -> str:
    if isinstance(value, str):
        return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"
    return json.dumps(value)


def js_rows(rows: list[dict]) -> str:
    return "[" + ", ".join("{" + ", ".join(f"{k}:{js_literal(v)}" for k, v in r.items()) + "}" for r in rows) + "]"


def jsx_text(text: str) -> str:
    """Make typed words safe inside a JSX attribute or text node."""
    return text.replace("'", "’").replace("{", "(").replace("}", ")").replace("<", "‹").replace(">", "›")


def render_module(template: str, rows: list[dict], title: str, total: int) -> str:
    return (
        template.replace("__ROWS__", js_rows(rows))
        .replace("__TITLE__", jsx_text(title))
        .replace("__TOTAL__", str(total))
    )


def render_svg(rows: list[dict], title: str, total: int) -> str:
    """Static version of the chart for HTML or Markdown deliverables."""
    rows = sorted(rows, key=lambda r: (-(r["ind"] + r["ven"]), r["n"]))
    max_total = max((r["ind"] + r["ven"] for r in rows), default=1) or 1
    x0, width, y0, rh = 268, 360, 104, 26
    w = width / max_total
    height = y0 + rh * len(rows) + 30
    grey, blue, ink, quiet = "#b9b8ae", "#2a78d6", "#1f1f1f", "#5e5e5e"

    def esc(s: str) -> str:
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&#39;")

    out = [
        f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 760 {height}' role='img' "
        f"aria-label='{esc(title)}' font-family='system-ui, sans-serif' font-size='12'>",
        f"<text x='16' y='28' font-size='16' font-weight='600' fill='{ink}'>{esc(title)}</text>",
        f"<text x='16' y='52' font-size='13' fill='{quiet}'>Bold: themes where vendors or consultants "
        f"supply a third or more of the findings.</text>",
        f"<rect x='16' y='68' width='12' height='12' fill='{grey}'/>"
        f"<text x='34' y='78' fill='{quiet}'>Independent voices</text>",
        f"<rect x='246' y='68' width='12' height='12' fill='{blue}'/>"
        f"<text x='264' y='78' fill='{quiet}'>Vendor or consultant voices</text>",
    ]
    for i, r in enumerate(rows):
        y = y0 + i * rh
        tot = r["ind"] + r["ven"]
        heavy = 3 * r["ven"] >= tot
        weight, color = ("600", ink) if heavy else ("400", quiet)
        label = f"{tot} · {round(100 * r['ven'] / tot)}% vendor" if heavy else str(tot)
        out.append(
            f"<text x='{x0 - 10}' y='{y + 13}' text-anchor='end' fill='{color}' font-weight='{weight}'>"
            f"{r['n']}. {esc(r['theme'])}</text>"
        )
        out.append(f"<rect x='{x0}' y='{y}' width='{r['ind'] * w:.1f}' height='18' fill='{grey}'/>")
        if r["ven"]:
            out.append(
                f"<rect x='{x0 + r['ind'] * w:.1f}' y='{y}' width='{r['ven'] * w:.1f}' height='18' "
                f"fill='{blue}' fill-opacity='{1 if heavy else 0.4}'/>"
            )
        out.append(
            f"<text x='{x0 + tot * w + 6:.1f}' y='{y + 13}' fill='{color}' font-weight='{weight}'>{label}</text>"
        )
    out.append(
        f"<text x='16' y='{height - 10}' font-size='11' fill='{quiet}'>One finding can support several "
        f"themes, so the bars add up to more than {total}.</text></svg>"
    )
    return "\n".join(out)


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------


def read_json(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def load_run(run_dir: Path) -> tuple[list[dict], list[dict], dict, list[dict]]:
    """Return (kept findings, dropped findings, source-type names, themes)."""
    # The original file sorts before its follow-ups (F-forums.md before F-forums-2.md), so its heading names the type.
    raw_files = sorted((run_dir / "raw").glob("[A-Z]-*.md"), key=lambda p: (prefix_key(p.name[0]), len(p.name), p.name))
    if not raw_files:
        raise SystemExit(f"No raw/<PREFIX>-<slug>.md files under {run_dir}")
    parsed, names = [], {}
    for path in raw_files:
        prefix = path.name[0]
        text = path.read_text(encoding="utf-8")
        names.setdefault(prefix, display_name(text, path.stem[2:].replace("-", " ").title()))
        parsed += parse_raw_file(text, prefix)
    parsed.sort(key=lambda f: (prefix_key(f["prefix"]), int(f["id"][1:])))
    coded = apply_coding(parsed, read_json(run_dir / "coding.json", {}))
    themes = read_json(run_dir / "themes.json", [])
    kept = [f for f in coded if not f["drop"]]
    dropped = [f for f in coded if f["drop"]]
    return kept, dropped, names, themes


def renumber_run(run_dir: Path) -> dict[int, int]:
    """Rewrite themes.json and coding.json so theme numbers follow rank by findings."""
    findings, _, names, themes = load_run(run_dir)
    mapping = renumber_map(theme_stats(findings, themes, sorted(names, key=prefix_key)))
    new_themes, new_coding = renumber(themes, read_json(run_dir / "coding.json", {}), mapping)
    (run_dir / "themes.json").write_text(json.dumps(new_themes, indent=1, ensure_ascii=False), encoding="utf-8")
    (run_dir / "coding.json").write_text(json.dumps(new_coding, indent=1, ensure_ascii=False), encoding="utf-8")
    return mapping


def build(run_dir: Path, chart_title: str) -> dict:
    findings, dropped, names, themes = load_run(run_dir)
    prefixes = sorted(names, key=prefix_key)
    coded = any(f["themes"] for f in findings)
    stats = theme_stats(findings, themes, prefixes) if coded else []
    groups = group_totals(stats)
    rows = chart_rows(stats)
    out = run_dir / "build"
    out.mkdir(exist_ok=True)

    def write(name: str, text: str) -> None:
        (out / name).write_text(text, encoding="utf-8")

    write("findings.json", json.dumps(findings, indent=1, ensure_ascii=False))
    write("evidence-index.md", render_index(findings, names))
    write("totals.md", render_totals(findings, names, groups))
    write("theme-stats.md", render_stats(stats))
    write("theme-stats.json", json.dumps({"themes": stats, "groups": groups}, indent=1, ensure_ascii=False))
    write(
        "vocabulary.md",
        render_tally(tally([f["words"] for f in findings]), "Word")
        + "\n\n"
        + render_tally(tally([f["forces"] for f in findings]), "Force"),
    )
    write("chart-rows.json", json.dumps(rows, indent=1, ensure_ascii=False))
    template = Path(__file__).resolve().parent.parent / "assets" / "chart-module.jsx"
    if rows and template.exists():
        write("chart-module.jsx", render_module(template.read_text(encoding="utf-8").strip(), rows,
                                                chart_title, len(findings)))
    if rows:
        write("theme-chart.svg", render_svg(rows, chart_title, len(findings)))
    problems = checks(findings, themes, dropped, chart_title)
    write("checks.md", "\n".join(f"- {p}" for p in problems) if problems else "No problems found.")
    return {
        "findings": len(findings),
        "vendor": sum(f["vendor"] for f in findings),
        "dropped": len(dropped),
        "themes": len(stats),
        "problems": len(problems),
        "out": str(out),
    }


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

SAMPLE_P = """# Expert podcasts and interviews

### P01. Close still runs in spreadsheets
- source: https://example.com/ep1 | Example Show | 2026-01-05
- speaker: CFO, mid-size manufacturer
- vendor: no
- phrase: "we still close in Excel"
- context: Describes a manual close.
- value: relieves pain
- forces: push, habit
- words: manual, spreadsheet
- job area: close

### P02. Vendor CFO on audit trails
- source: same
- speaker: CFO of a close-software vendor
- vendor: no
- phrase: "auditors want the trail"
- context: Pitches audit evidence.
- value: both
- forces: anxiety
- words: audit, control
- job area: audit

### P03. Repeat of P01 from a clip
- source: https://example.com/clip | Example Show | 2026-01-06
- speaker: same CFO as P01
- vendor: no
- phrase: "we still close in Excel"
- context: Same remark, reposted.
- value: relieves pain
- words: manual
"""

SAMPLE_F = """# Practitioner forums

### F01. Intercompany will not balance
- source: https://www.forum.example.org/q/1 ; no pipes here
- speaker: asker, staff accountant at a 12-entity group
- vendor: no
- phrase: "intercompany never ties out and I rebuild the eliminations every single month from scratch by hand again"
- context: Manual eliminations every month.
- value: relieves pain
- words: manual

### F02. Consultant on vendor sprawl
- source: https://www.forum.example.org/q/2 | Example Forum | 2025-11-02
- speaker: fractional controller
- vendor: vendor (advises buyers)
- phrase: "too many tools"
- context: Says clients run too many tools.
- value: saves or makes money
- forces: negative job
- words: sprawl
- job area: tools
"""


SAMPLE_F2 = """# Follow-up forum collection

### F03. Follow-up finding
- source: https://other.example.net/t/9 | Other Forum | 2026-03-03
- speaker: controller
- vendor: no
- phrase: "still reconciling by hand"
- context: Manual reconciliation.
- value: relieves pain
- words: manual
- job area: close
"""


def selftest() -> None:
    with tempfile.TemporaryDirectory() as d:
        run = Path(d)
        (run / "raw").mkdir()
        (run / "raw" / "P-podcasts.md").write_text(SAMPLE_P, encoding="utf-8")
        (run / "raw" / "F-forums.md").write_text(SAMPLE_F, encoding="utf-8")
        (run / "raw" / "F-forums-2.md").write_text(SAMPLE_F2, encoding="utf-8")
        (run / "themes.json").write_text(
            json.dumps([{"n": 1, "name": "Manual close"}, {"n": 2, "name": "Intercompany"},
                        {"n": 3, "name": "Unused"}]),
            encoding="utf-8",
        )
        (run / "coding.json").write_text(
            json.dumps({"P01": {"themes": [1]}, "P02": {"themes": [1, 2], "vendor": "yes (sells close software)"},
                        "P03": {"drop": "duplicate of P01"}, "F01": {"themes": "2"},
                        "F02": {"uncoded": "isolated remark"}, "F03": {"themes": [1]}}),
            encoding="utf-8",
        )
        result = build(run, "Test title {with} 'quotes'")
        findings, dropped, names, themes = load_run(run)
        byid = {f["id"]: f for f in findings}
        assert result["findings"] == 5 and result["vendor"] == 1 and result["dropped"] == 1, result
        assert list(names) == ["P", "F"], "source types must follow PREFIX_ORDER"
        assert names["F"] == "Practitioner forums", "the original file's heading must name the type"
        assert [f["id"] for f in findings if f["prefix"] == "F"] == ["F01", "F02", "F03"]
        assert byid["P02"]["url"] == "https://example.com/ep1", "same-source inheritance failed"
        assert byid["P02"]["site"] == "Example Show"
        assert byid["P02"]["vendor"] and byid["P02"]["vendor_reason"] == "sells close software"
        assert byid["F01"]["site"] == "forum.example.org"
        assert byid["F01"]["themes"] == [2]
        assert byid["P01"]["forces"] == ["push", "habit"]
        assert [d["id"] for d in dropped] == ["P03"]

        stats = {s["n"]: s for s in theme_stats(findings, themes, list(names))}
        assert stats[1]["total"] == 3 and stats[1]["vendor"] == 1 and stats[1]["group"] == "vendor-heavy"
        assert stats[2]["confidence"] == "Low", "fewer than 8 findings must be Low"
        assert stats[3]["total"] == 0
        assert confidence(15, 4, 4, 4) == "High"
        assert confidence(15, 5, 4, 4) == "Medium"  # exactly a third is not under a third
        assert confidence(20, 10, 4, 4) == "Low"  # half or more from vendors
        assert confidence(20, 0, 3, 4) == "Medium"  # a source type is missing
        assert confidence(7, 0, 4, 4) == "Low"
        assert group_for("Medium", 6, 2) == "vendor-heavy"  # 2 of 6 is a third
        assert group_for("Medium", 14, 1) == "independent but limited"

        problems = (run / "build" / "checks.md").read_text(encoding="utf-8")
        assert "theme 3: defined in themes.json but no finding supports it" in problems
        assert "F01: phrase is 17 words" in problems
        assert "F02: vendor must start with yes or no" in problems
        assert "F02: unknown forces ['negative job']" in problems
        assert "F02: no themes coded" not in problems, "uncoded findings must not be flagged"
        assert "chart: title" not in problems
        assert any(p.startswith("chart: title") for p in checks(findings, themes, [], DEFAULT_TITLE))
        assert "P03: dropped (duplicate of P01)" in problems
        index = (run / "build" / "evidence-index.md").read_text(encoding="utf-8")
        assert index.index("## Expert podcasts") < index.index("## Practitioner forums")
        assert "| P02† |" in index and "P03" not in index
        totals = (run / "build" / "totals.md").read_text(encoding="utf-8")
        assert "- Expert podcasts and interviews: Example Show (2)" in totals, totals
        assert "Findings outside every theme: 1 (F02)" in totals and "| tools | 1 | 0 |" in totals, totals
        module = (run / "build" / "chart-module.jsx").read_text(encoding="utf-8")
        assert "__" not in module, "a placeholder was left in the chart module"
        assert "Test title (with) ’quotes’" in module and "more than 5" in module
        svg = (run / "build" / "theme-chart.svg").read_text(encoding="utf-8")
        assert svg.startswith("<svg") and "more than 5" in svg
        mapping = renumber_run(run)
        assert mapping == {1: 1, 2: 2, 3: 3}, mapping
        (run / "coding.json").write_text(json.dumps({"P01": {"themes": [2]}, "P02": {"themes": [2, 1]},
                                                     "F01": {"themes": [2]}}), encoding="utf-8")
        assert renumber_run(run) == {2: 1, 1: 2, 3: 3}
        renamed = {t["n"]: t["name"] for t in read_json(run / "themes.json", [])}
        assert renamed[1] == "Intercompany" and renamed[2] == "Manual close"
        assert read_json(run / "coding.json", {})["P02"]["themes"] == [1, 2]
        assert parse_list("manual, 'control'; none") == ["manual", "control"]
        assert parse_list("(none explicit); (cost effective)") == ["cost effective"]
        assert parse_vendor("no") == (False, "")
        assert parse_value("Saves or makes money") == "money" and parse_value("relieves pain") == "pain"
    print("selftest passed")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir", nargs="?", type=Path)
    ap.add_argument("--chart-title", default=DEFAULT_TITLE,
                    help="the chart's finding, as a sentence")
    ap.add_argument("--renumber", action="store_true",
                    help="first renumber themes so 1 has the most findings (rewrites themes.json and coding.json)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        selftest()
        return 0
    if not args.run_dir:
        ap.error("RUN_DIR is required")
    if args.renumber:
        changed = {old: new for old, new in renumber_run(args.run_dir).items() if old != new}
        print("renumbered themes (old -> new):", changed or "no change")
    print(json.dumps(build(args.run_dir, args.chart_title), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
