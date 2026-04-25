#!/usr/bin/env python3
"""Resolve editable source-of-truth files for automation patch planning."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RESEARCH_BRANCH_DIR = ROOT / "data" / "research_branches"
RESEARCH_GENERATOR = "scripts/generate_research_branch.py"


@dataclass(slots=True)
class SourceResolution:
    target_file: str
    source_of_truth_file: str
    output_file: str
    source_type: str
    is_generated: bool
    generator_command: str | None
    edit_policy: str

    def to_dict(self) -> dict:
        return asdict(self)


def research_branch_slug_map() -> dict[str, str]:
    mapping: dict[str, str] = {}
    if not RESEARCH_BRANCH_DIR.exists():
        return mapping

    for path in sorted(RESEARCH_BRANCH_DIR.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        slug = payload.get("page", {}).get("slug")
        if not slug:
            continue
        mapping[f"{slug}.html"] = str(path.relative_to(ROOT))
    return mapping


def resolve_source(target_file: str) -> SourceResolution:
    filename = Path(target_file).name
    research_sources = research_branch_slug_map()

    if filename in research_sources:
        source = research_sources[filename]
        return SourceResolution(
            target_file=target_file,
            source_of_truth_file=source,
            output_file=filename,
            source_type="generated_research_branch",
            is_generated=True,
            generator_command=f"python3 {RESEARCH_GENERATOR} {source}",
            edit_policy="Edit the JSON source first, then regenerate the HTML output.",
        )

    return SourceResolution(
        target_file=target_file,
        source_of_truth_file=target_file,
        output_file=filename,
        source_type="html_file",
        is_generated=False,
        generator_command=None,
        edit_policy="Edit the target file directly.",
    )
