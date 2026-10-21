"""Compatibility and standalone packaging checks. Standard library only."""

import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
OPENAI = ROOT / "openai" / "market-pain-research-openai"
SHARED = (
    "references/method.md",
    "references/frameworks.md",
    "references/writing-standard.md",
    "scripts/research_index.py",
    "assets/chart-module.jsx",
)


def run_script(skill, *arguments, cwd=None):
    """Run a packaged script through its public CLI."""
    return subprocess.run(
        [
            sys.executable,
            str(skill / "scripts/research_index.py"),
            *map(str, arguments),
        ],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )


def write_fixture(run):
    """A four-source corpus covering confidence groups, overlap, and exclusions."""
    (run / "raw").mkdir(parents=True)
    coding = {}
    for prefix in "PNFR":
        records = [f"# Source {prefix}\n\n## Findings\n"]
        for number in range(1, 11):
            finding_id = f"{prefix}{number:02}"
            vendor = number in (5, 6, 7)
            theme = 2 if number <= 5 else 1 if number <= 8 else 3 if number == 9 else 4
            themes = [theme, 3] if number == 1 else [theme]
            coding[finding_id] = {"themes": themes}
            records.append(
                f"### {finding_id}. Records arrive late\n"
                f"- source: https://example.org/{prefix}/{number} | Source {prefix} | 2026-10-01\n"
                "- speaker: practitioner, small business owner\n"
                f"- vendor: {'yes (advises buyers)' if vendor else 'no'}\n"
                '- phrase: "Records arrive too late"\n'
                "- context: Delayed records cause manual follow-up.\n"
                "- value: both\n"
                "- forces: push, workaround\n"
                "- words: manual, follow-up\n"
                "- job area: operations\n"
            )
        if prefix == "P":
            records.append(records[1].replace("### P01.", "### P11."))
            coding["P11"] = {"drop": "duplicate of P01: same speaker and remark"}
        (run / "raw" / f"{prefix}-fixture.md").write_text(
            "\n".join(records), encoding="utf-8"
        )
    themes = [
        {"n": 1, "name": "Handoffs fail"},
        {"n": 2, "name": "Records arrive late"},
        {"n": 3, "name": "Follow-up takes time"},
        {"n": 4, "name": "Missing context"},
    ]
    (run / "themes.json").write_text(json.dumps(themes), encoding="utf-8")
    (run / "coding.json").write_text(json.dumps(coding), encoding="utf-8")


class VersionCompatibility(unittest.TestCase):
    def test_claude_runtime_matches_frozen_baseline(self):
        baseline = json.loads((ROOT / "compatibility/claude-baseline.json").read_text())
        for relative, digest in baseline["sha256"].items():
            with self.subTest(path=relative):
                self.assertEqual(
                    hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), digest
                )

    def test_shared_method_and_engine_have_not_drifted(self):
        for relative in SHARED:
            with self.subTest(path=relative):
                self.assertEqual(
                    (ROOT / relative).read_bytes(), (OPENAI / relative).read_bytes()
                )

    def test_existing_claude_selftest(self):
        self.assertIn("selftest passed", run_script(ROOT, "--selftest").stdout)

    def test_standalone_package_and_output_parity(self):
        with tempfile.TemporaryDirectory(prefix="pain research ") as temporary:
            sandbox = Path(temporary)
            installed = sandbox / "installed skill"
            shutil.copytree(
                OPENAI, installed, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
            )
            self.assertFalse(any(path.is_symlink() for path in installed.rglob("*")))
            self.assertIn(
                "selftest passed",
                run_script(installed, "--selftest", cwd=sandbox).stdout,
            )
            original_run, portable_run = sandbox / "claude run", sandbox / "openai run"
            write_fixture(original_run)
            shutil.copytree(original_run, portable_run)
            title = "One theme has high confidence across four source types"
            for skill, run in ((ROOT, original_run), (installed, portable_run)):
                run_script(skill, run, "--renumber", cwd=sandbox)
                result = json.loads(
                    run_script(skill, run, "--chart-title", title, cwd=sandbox).stdout
                )
                self.assertEqual(result["findings"], 40)
                self.assertEqual(result["vendor"], 12)
                self.assertEqual(result["dropped"], 1)
                self.assertEqual(result["themes"], 4)
            original_files = {
                path.name: path.read_bytes()
                for path in (original_run / "build").iterdir()
            }
            portable_files = {
                path.name: path.read_bytes()
                for path in (portable_run / "build").iterdir()
            }
            self.assertEqual(original_files, portable_files)
            self.assertEqual(
                (original_run / "themes.json").read_bytes(),
                (portable_run / "themes.json").read_bytes(),
            )
            self.assertEqual(
                (original_run / "coding.json").read_bytes(),
                (portable_run / "coding.json").read_bytes(),
            )
            stats = json.loads(portable_files["theme-stats.json"])["themes"]
            by_name = {theme["name"]: theme for theme in stats}
            self.assertEqual(by_name["Records arrive late"]["n"], 1)
            self.assertEqual(by_name["Records arrive late"]["total"], 20)
            self.assertEqual(by_name["Records arrive late"]["vendor"], 4)
            self.assertEqual(by_name["Records arrive late"]["confidence"], "High")
            self.assertEqual(by_name["Records arrive late"]["value"], "Both")
            self.assertEqual(by_name["Handoffs fail"]["group"], "vendor-heavy")
            self.assertEqual(by_name["Follow-up takes time"]["confidence"], "Medium")
            self.assertEqual(by_name["Missing context"]["confidence"], "Low")
            self.assertEqual(
                by_name["Missing context"]["group"], "independent but limited"
            )
            index = portable_files["evidence-index.md"].decode()
            self.assertIn("https://example.org/P/1", index)
            self.assertNotIn("P11", index)
            self.assertTrue(
                all(
                    "dropped (" in line
                    for line in portable_files["checks.md"].decode().splitlines()
                )
            )
            svg = ElementTree.fromstring(portable_files["theme-chart.svg"])
            self.assertEqual(svg.tag, "{http://www.w3.org/2000/svg}svg")
            self.assertIn(title, "".join(svg.itertext()))
            # Rebuilding after a paused run must preserve completed evidence and IDs.
            before = {
                path.name: path.read_bytes()
                for path in (portable_run / "raw").iterdir()
            }
            run_script(installed, portable_run, "--chart-title", title, cwd=sandbox)
            self.assertEqual(
                portable_files,
                {
                    path.name: path.read_bytes()
                    for path in (portable_run / "build").iterdir()
                },
            )
            self.assertEqual(
                before,
                {
                    path.name: path.read_bytes()
                    for path in (portable_run / "raw").iterdir()
                },
            )

    def test_skill_reference_links_stay_inside_package(self):
        for document in [
            OPENAI / "SKILL.md",
            *sorted((OPENAI / "references").glob("*.md")),
        ]:
            for target in re.findall(r"\]\(([^)]+)\)", document.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                path = (document.parent / target.split("#", 1)[0]).resolve()
                with self.subTest(document=document.name, link=target):
                    self.assertTrue(path.is_relative_to(OPENAI.resolve()))
                    self.assertTrue(path.is_file())

    def test_confidence_boundaries_in_portable_engine(self):
        spec = importlib.util.spec_from_file_location(
            "portable_index", OPENAI / "scripts/research_index.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for arguments, expected in (
            ((15, 4, 4, 4), "High"),
            ((15, 5, 4, 4), "Medium"),
            ((20, 10, 4, 4), "Low"),
            ((15, 0, 3, 4), "Medium"),
            ((15, 0, 2, 2), "High"),
            ((7, 0, 4, 4), "Low"),
        ):
            with self.subTest(arguments=arguments):
                self.assertEqual(module.confidence(*arguments), expected)


if __name__ == "__main__":
    unittest.main()
