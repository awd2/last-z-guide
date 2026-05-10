#!/usr/bin/env python3
"""Apply approved Patch Spec v1 entries with conservative deterministic templates."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from automation.io import load_run_manifest, write_json, write_run_manifest
from automation.proposal_renderer import REPORTS_DIR, md_list, resolve_manifest_path


TARGET_CARDS = {
    "codes.html": {"href": "codes.html", "label": "Redeem Codes"},
    "gift-center-uid.html": {"href": "gift-center-uid.html", "label": "Gift Center UID Setup"},
    "redeem-code-not-working.html": {"href": "redeem-code-not-working.html", "label": "Code Not Working"},
    "research-costs.html": {"href": "research-costs.html", "label": "Research Costs Atlas"},
}

TARGET_OPERATION_SUPPORT = {
    "codes.html": {
        "first_screen_update",
        "internal_link_addition",
    },
    "research-costs.html": {
        "meta_refresh",
        "first_screen_update",
        "internal_link_addition",
        "atlas_card_update",
    },
    "gift-center-uid.html": {
        "meta_refresh",
        "first_screen_update",
        "internal_link_addition",
    },
    "redeem-code-not-working.html": {
        "first_screen_update",
        "internal_link_addition",
    },
    "start.html": {
        "first_screen_update",
    },
}

SAFE_EXACT_REPLACE_OPERATION = "safe_exact_replace"

GENERIC_HTML_RELATED_CARD_SUPPORT = {
    ("alliance-recognition-cost.html", "research-costs.html"),
    ("diamond-reserve.html", "codes.html"),
    ("diamond-reserve.html", "gift-center-uid.html"),
    ("f2p.html", "gift-center-uid.html"),
    ("farm-account.html", "codes.html"),
    ("farm-account.html", "gift-center-uid.html"),
}

GENERATED_RESEARCH_RELATED_GUIDE_TARGETS = {
    "research-costs.html",
}

START_SEASON_NOTE = """                    <p class="qa-callout qa-callout--note">
                        <span class="qa-icon" aria-hidden="true">i</span>
                        <span class="qa-callout-text"><strong>Season naming note:</strong> on newer servers, Season 2 is Winter. Older guides may call Season 2 Desert, but Desert was canceled or skipped for current servers, so follow Winter naming when planning your early timeline.</span>
                    </p>"""

CODES_GUIDE_VERIFIED_OLD = '<p class="guide-verified">Use the official Last Z Gift Center to redeem active codes. This page gives you the current verified codes, the official login page, the fastest UID steps, and the main reasons redemption fails.</p>'
CODES_GUIDE_VERIFIED_NEW = '<p class="guide-verified">Use this page for active Last Z codes first, then redeem them through the official Gift Center. Copy your UID from Avatar &gt; Settings &gt; Copy ID, paste the code exactly, and check your in-game mailbox for rewards.</p>'

CODES_ROUTING_OLD = """            <p><strong>Need setup only?</strong> Use the <a href="gift-center-uid.html">Gift Center &amp; UID Guide</a>. <strong>Need troubleshooting?</strong> Use <a href="redeem-code-not-working.html">Code Not Working?</a>.</p>
            <p>If you want the full troubleshooting flow, use the <a href="redeem-code-not-working.html">Last Z Code Not Working?</a> guide.</p>"""
CODES_ROUTING_NEW = '            <p><strong>Need setup only?</strong> Use the <a href="gift-center-uid.html">Gift Center &amp; UID Guide</a>. <strong>Code failed?</strong> Use the <a href="redeem-code-not-working.html">Last Z Code Not Working?</a> guide.</p>'

REDEEM_MAILBOX_CALLOUT = """                    <p class="qa-callout qa-callout--tip">
                        <span class="qa-icon" aria-hidden="true">📬</span>
                        <span class="qa-callout-text"><strong>Check your mailbox:</strong> rewards go to in-game mail, not the Gift Center screen.</span>
                    </p>"""

REDEEM_FAILURE_SORTING_CALLOUT = """                    <p class="qa-callout qa-callout--note">
                        <span class="qa-icon" aria-hidden="true">i</span>
                        <span class="qa-callout-text"><strong>Sort the failure first:</strong> wrong UID or typo means the redemption failed, expired or already-used means the code is no longer claimable for that account, and missing rewards means you should check mailbox timing before retrying.</span>
                    </p>"""

REDEEM_RELATED_CODES_CARD = '                <a href="codes.html" class="related-card">Redeem Codes</a>'
REDEEM_RELATED_UID_CARD = '                <a href="gift-center-uid.html" class="related-card">Gift Center UID Setup</a>'


def approved_specs(manifest) -> list[dict[str, Any]]:
    patch_plan = (manifest.artifacts or {}).get("patch_plan", {})
    return [
        spec
        for spec in patch_plan.get("patch_specs", [])
        if spec.get("approval_state") == "approved"
    ]


def replace_once(text: str, old: str, new: str, applied: list[str], label: str) -> str:
    if old not in text:
        return text
    applied.append(label)
    return text.replace(old, new, 1)


def exact_replace_texts(spec: dict[str, Any]) -> tuple[str, str]:
    old = spec.get("exact_old")
    new = spec.get("exact_new")
    if not isinstance(old, str) or not old:
        raise ValueError("safe_exact_replace requires a non-empty `exact_old` string.")
    if not isinstance(new, str) or not new:
        raise ValueError("safe_exact_replace requires a non-empty `exact_new` string.")
    if old == new:
        raise ValueError("safe_exact_replace requires different `exact_old` and `exact_new` strings.")
    return old, new


def source_path(source_file: str) -> Path:
    path = Path(source_file)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Unsafe source path for safe_exact_replace: {source_file}")
    resolved = (ROOT / path).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"Source path escapes repository root: {source_file}") from exc
    return resolved


def validate_safe_exact_replace_spec(source_file: str, spec: dict[str, Any]) -> None:
    exact_replace_texts(spec)
    if spec.get("is_generated"):
        raise ValueError(f"safe_exact_replace refuses generated source files: {source_file}")
    if spec.get("source_type") != "html_file":
        raise ValueError(f"safe_exact_replace only supports html_file sources: {source_file}")
    if Path(source_file).suffix != ".html":
        raise ValueError(f"safe_exact_replace only supports HTML files: {source_file}")
    output_file = str(spec.get("output_file") or "")
    target_file = str(spec.get("target_file") or "")
    if output_file != source_file or target_file != source_file:
        raise ValueError(
            "safe_exact_replace requires target_file, source_of_truth_file, and output_file "
            f"to match for {source_file}."
        )
    source_path(source_file)


def apply_safe_exact_replace(source_file: str, spec: dict[str, Any]) -> tuple[list[str], list[str]]:
    old, new = exact_replace_texts(spec)
    path = source_path(source_file)
    if not path.exists():
        raise ValueError(f"safe_exact_replace source file not found: {source_file}")

    text = path.read_text(encoding="utf-8")
    old_count = text.count(old)
    new_count = text.count(new)
    selector = str(spec.get("selector_or_anchor") or "exact")
    label = f"{source_file}:safe_exact_replace:{selector}"

    if old_count == 1:
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        return [label], []
    if old_count == 0 and new_count == 1:
        return [], [f"{label}:already_applied"]
    if old_count == 0:
        raise ValueError(f"safe_exact_replace old text not found in {source_file}: {selector}")
    raise ValueError(f"safe_exact_replace old text is ambiguous in {source_file}: {selector} ({old_count} matches)")


def target_card(target_page: str) -> dict[str, str]:
    return TARGET_CARDS.get(target_page, {"href": target_page, "label": target_page})


def validate_supported_specs(grouped: dict[str, list[dict[str, Any]]], target_page: str) -> None:
    for source_file, source_specs in grouped.items():
        non_exact_specs = []
        for spec in source_specs:
            if spec.get("operation_type") == SAFE_EXACT_REPLACE_OPERATION:
                validate_safe_exact_replace_spec(source_file, spec)
            else:
                non_exact_specs.append(spec)

        if not non_exact_specs:
            continue

        supported = TARGET_OPERATION_SUPPORT.get(source_file)
        if supported is not None:
            unsupported = [
                str(spec.get("operation_type"))
                for spec in non_exact_specs
                if spec.get("operation_type") not in supported
            ]
            if unsupported:
                raise ValueError(
                    f"Unsupported approved operation(s) for {source_file}: "
                    f"{', '.join(sorted(set(unsupported)))}"
                )
            continue

        for spec in non_exact_specs:
            operation = spec.get("operation_type")
            source_type = spec.get("source_type")
            if operation != "internal_link_addition":
                raise ValueError(f"Unsupported approved operation for {source_file}: {operation}")
            if source_type == "generated_research_branch":
                if target_page not in GENERATED_RESEARCH_RELATED_GUIDE_TARGETS:
                    raise ValueError(
                        "Unsupported generated research related-guide target for "
                        f"{source_file}: {target_page}"
                    )
                continue
            if source_type == "html_file":
                if (source_file, target_page) not in GENERIC_HTML_RELATED_CARD_SUPPORT:
                    raise ValueError(
                        "Unsupported generic HTML related-card route for "
                        f"{source_file} -> {target_page}"
                    )
                continue
            raise ValueError(f"Unsupported source type for {source_file}: {source_type}")


def apply_research_costs(specs: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    path = ROOT / "research-costs.html"
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []
    skipped: list[str] = []
    operations = {spec.get("operation_type") for spec in specs}

    if "meta_refresh" in operations:
        replacements = [
            (
                "<title>Last Z Research Costs Atlas (2026) — All Research Trees, Badge Totals, and Unlock Paths</title>",
                "<title>Last Z Research Costs Atlas (2026) — Branch Comparison, Badge Totals, and Unlock Paths</title>",
                "title",
            ),
            (
                '<meta name="description" content="All major Last Z research trees in one place: total badge costs, unlock requirements, best stopping points, and links to every exact node-cost tree.">',
                '<meta name="description" content="Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page before spending badges.">',
                "meta_description",
            ),
            (
                '<meta property="og:title" content="Last Z Research Costs Atlas — All Research Trees, Badge Totals, and Unlock Paths">',
                '<meta property="og:title" content="Last Z Research Costs Atlas — Branch Comparison, Badge Totals, and Unlock Paths">',
                "og_title",
            ),
            (
                '<meta property="og:description" content="Compare all major Last Z research trees by total badges, unlock requirements, and exact node-cost pages.">',
                '<meta property="og:description" content="Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page.">',
                "og_description",
            ),
            (
                '<meta name="twitter:title" content="Last Z Research Costs Atlas — All Research Trees, Badge Totals, and Unlock Paths">',
                '<meta name="twitter:title" content="Last Z Research Costs Atlas — Branch Comparison, Badge Totals, and Unlock Paths">',
                "twitter_title",
            ),
            (
                '<meta name="twitter:description" content="Compare all major Last Z research trees by total badges, unlock requirements, and exact node-cost pages.">',
                '<meta name="twitter:description" content="Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page.">',
                "twitter_description",
            ),
            (
                '"headline": "Last Z Research Costs Atlas — All Research Trees, Badge Totals, and Unlock Paths"',
                '"headline": "Last Z Research Costs Atlas — Branch Comparison, Badge Totals, and Unlock Paths"',
                "article_headline",
            ),
            (
                '"description": "All major Last Z research trees in one place: total badge costs, unlock requirements, best stopping points, and links to every exact node-cost tree."',
                '"description": "Compare Last Z research branches by badge total, unlock path, priority role, and exact node-cost page before spending badges."',
                "article_description",
            ),
            (
                "<h1>Last Z Research Costs Atlas — All Research Trees, Badge Totals, and Unlock Paths</h1>",
                "<h1>Last Z Research Costs Atlas — Branch Comparison, Badge Totals, and Unlock Paths</h1>",
                "h1",
            ),
        ]
        for old, new, label in replacements:
            text = replace_once(text, old, new, applied, f"research-costs:{label}")

    if "first_screen_update" in operations:
        text = replace_once(
            text,
            '<p class="guide-verified">This atlas is the fastest way to compare all major badge-heavy research trees in Last Z. Use it when you want to see total branch cost, unlock requirements, and the exact tree page for each branch without jumping through the whole site blindly.</p>',
            '<p class="guide-verified">This atlas is the branch router for Last Z research costs: compare badge totals and unlock paths here, then open the exact branch page for node-by-node costs before spending badges.</p>',
            applied,
            "research-costs:guide_verified",
        )
        text = replace_once(
            text,
            '<p class="data-lede">Use this page to compare every major research branch by total badge cost, unlock path, and practical value. It is the main entry point for exact node trees and badge planning across the whole research cluster.</p>',
            '<p class="data-lede">Use this page to compare every major research branch by badge total, unlock path, and priority role. The main route for most players is Hero Training to Cockpit, Military Strategies, Peace Shield, Siege to Seize, then Field Research.</p>',
            applied,
            "research-costs:data_lede",
        )
        text = replace_once(
            text,
            '<p class="qa-lede"><strong>Best way to use the research atlas:</strong> start with Hero Training to Cockpit, move into Military Strategies and Peace Shield for efficient mid-game value, and treat Unit Special Training as the biggest late-game badge sink rather than an early goal.</p>',
            '<p class="qa-lede"><strong>Best way to use the research atlas:</strong> use this page as the branch router, then open the exact cost page for node totals. For most players, the main route is Hero Training to Cockpit, Military Strategies, Peace Shield, Siege to Seize, then Field Research.</p>',
            applied,
            "research-costs:qa_lede",
        )

    if {"internal_link_addition", "atlas_card_update"} & operations:
        count = text.count('<span class="atlas-link">View tree →</span>')
        if count:
            text = text.replace(
                '<span class="atlas-link">View tree →</span>',
                '<span class="atlas-link">View exact cost tree →</span>',
            )
            applied.append(f"research-costs:atlas_link_copy:{count}")

    if "internal_link_addition" in operations:
        skipped.append("research-costs.html:self_link_skipped")

    path.write_text(text, encoding="utf-8")
    return applied, skipped


def apply_gift_center_uid(specs: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    path = ROOT / "gift-center-uid.html"
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []
    skipped: list[str] = []
    operations = {spec.get("operation_type") for spec in specs}

    if "meta_refresh" in operations:
        replacements = [
            (
                "<title>Last Z Gift Center Login & UID Guide (2026) — Official Redeem Page</title>",
                "<title>Last Z Gift Center Login and UID Setup (2026) — Official Redeem Page</title>",
                "title",
            ),
            (
                '<meta name="description" content="Official Last Z Gift Center login, how to find and copy your UID, how to redeem codes on iPhone or Android, and where rewards appear after redemption.">',
                '<meta name="description" content="Official Last Z Gift Center login setup: how to copy your UID from Avatar > Settings > Copy ID, redeem in a browser, and collect rewards from mailbox.">',
                "meta_description",
            ),
            (
                '<meta property="og:title" content="Last Z Gift Center Login & UID Guide — Official Redeem Page">',
                '<meta property="og:title" content="Last Z Gift Center Login and UID Setup — Official Redeem Page">',
                "og_title",
            ),
            (
                '<meta property="og:description" content="Official Last Z Gift Center login, how to copy your UID, redeem codes on iPhone or Android, and where rewards appear after redemption.">',
                '<meta property="og:description" content="Official Last Z Gift Center login setup, UID copying path, browser redemption flow, and mailbox reward delivery.">',
                "og_description",
            ),
            (
                '<meta name="twitter:title" content="Last Z Gift Center Login & UID Guide — Official Redeem Page">',
                '<meta name="twitter:title" content="Last Z Gift Center Login and UID Setup — Official Redeem Page">',
                "twitter_title",
            ),
            (
                '<meta name="twitter:description" content="Official Last Z Gift Center login, how to copy your UID, redeem codes on iPhone or Android, and where rewards appear after redemption.">',
                '<meta name="twitter:description" content="Official Last Z Gift Center login setup, UID copying path, browser redemption flow, and mailbox reward delivery.">',
                "twitter_description",
            ),
            (
                '"headline": "Last Z Gift Center Login & UID Guide — Official Redeem Page"',
                '"headline": "Last Z Gift Center Login and UID Setup — Official Redeem Page"',
                "article_headline",
            ),
            (
                '"description": "Setup guide for Last Z Gift Center login, UID copying, mobile redemption flow, and mailbox reward delivery"',
                '"description": "Official Last Z Gift Center login setup, UID copying path, browser redemption flow, and mailbox reward delivery"',
                "article_description",
            ),
            (
                "<h1>Last Z Gift Center Login &amp; UID Guide — Official Redeem Page</h1>",
                "<h1>Last Z Gift Center Login and UID Setup — Official Redeem Page</h1>",
                "h1",
            ),
        ]
        for old, new, label in replacements:
            text = replace_once(text, old, new, applied, f"gift-center-uid:{label}")

    if "first_screen_update" in operations:
        text = replace_once(
            text,
            '<p class="guide-verified">The official Last Z Gift Center login page is the only place where codes are redeemed. Copy your UID from Avatar → Settings → Copy ID, redeem in a browser, and collect rewards from your mailbox.</p>',
            '<p class="guide-verified">Use the official Last Z Gift Center in a browser, copy your UID from Avatar → Settings → Copy ID, redeem outside the game client, and collect rewards from your in-game mailbox.</p>',
            applied,
            "gift-center-uid:guide_verified",
        )
        text = replace_once(
            text,
            '<p class="qa-lede"><strong>Official Last Z Gift Center setup:</strong> open the redeem website, copy your UID from Settings, paste the code in your browser on iPhone or Android, and check your in-game mailbox for rewards.</p>',
            '<p class="qa-lede"><strong>Official Last Z Gift Center setup:</strong> open the Gift Center in a browser, copy your UID from Avatar → Settings → Copy ID, paste the code outside the game, and collect rewards from your in-game mailbox.</p>',
            applied,
            "gift-center-uid:qa_lede",
        )

    if "internal_link_addition" in operations:
        if 'href="codes.html"' in text and 'href="redeem-code-not-working.html"' in text:
            skipped.append("gift-center-uid.html:self_link_skipped_outbound_routing_already_present")
        else:
            skipped.append("gift-center-uid.html:self_link_skipped_manual_outbound_review")

    path.write_text(text, encoding="utf-8")
    return applied, skipped


def apply_start(specs: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    path = ROOT / "start.html"
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []
    skipped: list[str] = []
    operations = {spec.get("operation_type") for spec in specs}

    if "first_screen_update" in operations:
        if "Season naming note:" in text:
            skipped.append("start.html:season_note_already_present")
        else:
            anchor = """                    <p class="qa-callout qa-callout--tip">
                        <span class="qa-icon" aria-hidden="true">💡</span>
                        <span class="qa-callout-text"><strong>Core rule:</strong> early progress is mostly about avoiding waste, not trying to do everything at once.</span>
                    </p>"""
            replacement = anchor + "\n" + START_SEASON_NOTE
            text = replace_once(text, anchor, replacement, applied, "start.html:season_note_callout")
            if not applied:
                skipped.append("start.html:season_note_anchor_not_found")

    path.write_text(text, encoding="utf-8")
    return applied, skipped


def apply_codes(specs: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    path = ROOT / "codes.html"
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []
    skipped: list[str] = []
    operations = {spec.get("operation_type") for spec in specs}

    if "first_screen_update" in operations:
        text = replace_once(
            text,
            CODES_GUIDE_VERIFIED_OLD,
            CODES_GUIDE_VERIFIED_NEW,
            applied,
            "codes.html:guide_verified",
        )
        if "codes.html:guide_verified" not in applied:
            if CODES_GUIDE_VERIFIED_NEW in text:
                skipped.append("codes.html:guide_verified_already_updated")
            else:
                skipped.append("codes.html:guide_verified_anchor_not_found")

    if "internal_link_addition" in operations:
        text = replace_once(
            text,
            CODES_ROUTING_OLD,
            CODES_ROUTING_NEW,
            applied,
            "codes.html:dedupe_setup_troubleshooting_routing",
        )
        if "codes.html:dedupe_setup_troubleshooting_routing" not in applied:
            if CODES_ROUTING_NEW in text:
                skipped.append("codes.html:routing_already_deduped")
            else:
                skipped.append("codes.html:routing_anchor_not_found")

    path.write_text(text, encoding="utf-8")
    return applied, skipped


def apply_redeem_code_not_working(specs: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    path = ROOT / "redeem-code-not-working.html"
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []
    skipped: list[str] = []
    operations = {spec.get("operation_type") for spec in specs}

    if "first_screen_update" in operations:
        if "Sort the failure first:" in text:
            skipped.append("redeem-code-not-working.html:failure_sorting_callout_already_present")
        elif REDEEM_MAILBOX_CALLOUT in text:
            text = replace_once(
                text,
                REDEEM_MAILBOX_CALLOUT,
                REDEEM_MAILBOX_CALLOUT + "\n" + REDEEM_FAILURE_SORTING_CALLOUT,
                applied,
                "redeem-code-not-working.html:failure_sorting_callout",
            )
        else:
            skipped.append("redeem-code-not-working.html:mailbox_callout_anchor_not_found")

    if "internal_link_addition" in operations:
        related_match = re.search(
            r'(<div class="related-grid">\n)(?P<body>.*?)(\n\s*</div>)',
            text,
            flags=re.S,
        )
        if not related_match:
            skipped.append("redeem-code-not-working.html:related_grid_not_found")
        elif 'href="gift-center-uid.html"' in related_match.group("body"):
            skipped.append("redeem-code-not-working.html:uid_related_card_already_present")
        elif REDEEM_RELATED_CODES_CARD in related_match.group("body"):
            text = replace_once(
                text,
                REDEEM_RELATED_CODES_CARD,
                REDEEM_RELATED_CODES_CARD + "\n" + REDEEM_RELATED_UID_CARD,
                applied,
                "redeem-code-not-working.html:uid_related_card",
            )
        else:
            skipped.append("redeem-code-not-working.html:related_codes_card_anchor_not_found")

    path.write_text(text, encoding="utf-8")
    return applied, skipped


def add_html_related_card(source_file: str, target_page: str) -> tuple[list[str], list[str]]:
    path = ROOT / source_file
    text = path.read_text(encoding="utf-8")
    card = target_card(target_page)

    match = re.search(
        r'(<div class="related-grid">\n)(?P<body>.*?)(\n\s*</div>)',
        text,
        flags=re.S,
    )
    if not match:
        return [], [f"{source_file}:related_grid_not_found"]

    if f'href="{target_page}"' in match.group("body"):
        return [], [f"{source_file}:related_card_duplicate_skipped"]

    new_card = f'                <a href="{card["href"]}" class="related-card">{card["label"]}</a>'
    body = match.group("body")
    if source_file == "diamond-reserve.html" and target_page == "codes.html":
        anchor = '                <a href="resources.html" class="related-card">Resources Guide</a>'
        if anchor in body:
            replacement_body = body.replace(anchor, anchor + "\n" + new_card, 1)
        else:
            replacement_body = body + "\n" + new_card
    elif source_file == "farm-account.html" and target_page == "codes.html":
        anchor = '                <a href="gift-center-uid.html" class="related-card">Gift Center UID Setup</a>'
        if anchor in body:
            replacement_body = body.replace(anchor, anchor + "\n" + new_card, 1)
        else:
            replacement_body = body + "\n" + new_card
    else:
        replacement_body = body + "\n" + new_card
    replacement = match.group(1) + replacement_body + match.group(3)
    text = text[: match.start()] + replacement + text[match.end() :]
    path.write_text(text, encoding="utf-8")
    return [f"{source_file}:related_card:{target_page}"], []


def add_json_related_guide(source_file: str, target_page: str) -> tuple[list[str], list[str]]:
    path = ROOT / source_file
    payload = json.loads(path.read_text(encoding="utf-8"))
    related = payload.setdefault("related_guides", [])
    if any(item.get("href") == target_page for item in related if isinstance(item, dict)):
        return [], [f"{source_file}:related_guides_duplicate_skipped"]

    insert_at = len(related)
    for index, item in enumerate(related):
        if isinstance(item, dict) and item.get("href") == "research.html":
            insert_at = index + 1
            break
    related.insert(insert_at, dict(target_card(target_page)))
    write_json(path, payload)
    return [f"{source_file}:related_guides:{target_page}"], []


def run_generators(specs: list[dict[str, Any]]) -> list[str]:
    commands = []
    for spec in specs:
        command = spec.get("generator_command")
        if command and command not in commands:
            commands.append(command)

    ran: list[str] = []
    for command in commands:
        subprocess.run(command.split(), cwd=ROOT, check=True)
        ran.append(command)
    return ran


SPECIALIZED_APPLY_HANDLERS = {
    "codes.html": apply_codes,
    "gift-center-uid.html": apply_gift_center_uid,
    "redeem-code-not-working.html": apply_redeem_code_not_working,
    "research-costs.html": apply_research_costs,
    "start.html": apply_start,
}


def render_report(manifest, applied: list[str], skipped: list[str], generators: list[str], applied_at: str) -> str:
    return f"""# Apply Result: {manifest.run_id}

## Overview

- Summary: {manifest.summary}
- Applied at: `{applied_at}`
- Applied operations: {len(applied)}
- Skipped operations: {len(skipped)}
- Generator commands: {len(generators)}
- Status after apply: `applied_pending_qa`

## Safety Rule

- Only approved Patch Spec v1 entries were considered.
- `safe_exact_replace` specs replace exact owner-approved before/after snippets only.
- Generated research pages were changed through JSON source files and regenerated.
- This is still not a production publish step.

## Applied Operations

{md_list(applied)}

## Skipped Operations

{md_list(skipped)}

## Generator Commands

{md_list(generators)}
"""


def apply_approved(path: Path):
    manifest = load_run_manifest(path)
    specs = approved_specs(manifest)
    if not specs:
        raise ValueError("No approved Patch Spec v1 entries found.")

    grouped: dict[str, list[dict[str, Any]]] = {}
    for spec in specs:
        grouped.setdefault(str(spec.get("source_of_truth_file")), []).append(spec)

    applied: list[str] = []
    skipped: list[str] = []
    generated_specs: list[dict[str, Any]] = []
    target_page = str((manifest.plan or {}).get("target_page_or_slug", ""))
    validate_supported_specs(grouped, target_page)

    for source_file, source_specs in grouped.items():
        exact_specs = [
            spec for spec in source_specs if spec.get("operation_type") == SAFE_EXACT_REPLACE_OPERATION
        ]
        for spec in exact_specs:
            source_applied, source_skipped = apply_safe_exact_replace(source_file, spec)
            applied.extend(source_applied)
            skipped.extend(source_skipped)

        remaining_specs = [
            spec for spec in source_specs if spec.get("operation_type") != SAFE_EXACT_REPLACE_OPERATION
        ]
        if not remaining_specs:
            continue

        handler = SPECIALIZED_APPLY_HANDLERS.get(source_file)
        if handler is not None:
            source_applied, source_skipped = handler(remaining_specs)
            applied.extend(source_applied)
            skipped.extend(source_skipped)
            continue

        for spec in remaining_specs:
            operation = spec.get("operation_type")
            source_type = spec.get("source_type")
            if operation != "internal_link_addition":
                raise ValueError(f"Unsupported approved operation for {source_file}: {operation}")
            if source_type == "generated_research_branch":
                source_applied, source_skipped = add_json_related_guide(source_file, target_page)
                applied.extend(source_applied)
                skipped.extend(source_skipped)
                generated_specs.append(spec)
            elif source_type == "html_file":
                source_applied, source_skipped = add_html_related_card(source_file, target_page)
                applied.extend(source_applied)
                skipped.extend(source_skipped)
            else:
                raise ValueError(f"Unsupported source type for {source_file}: {source_type}")

    generators = run_generators(generated_specs)
    applied_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    out_path = REPORTS_DIR / f"{manifest.run_id}.apply-result.md"
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_report(manifest, applied, skipped, generators, applied_at), encoding="utf-8")

    manifest.artifacts.setdefault("apply_result", {})
    manifest.artifacts["apply_result"] = {
        "report_path": str(out_path.relative_to(ROOT)),
        "applied_at": applied_at,
        "applied_operations": applied,
        "skipped_operations": skipped,
        "generator_commands": generators,
    }
    manifest.status = "applied_pending_qa"
    write_run_manifest(path, manifest)
    return out_path, applied, skipped, generators


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply approved Patch Spec v1 entries with safe templates.")
    parser.add_argument("manifest", help="Manifest path or basename without .json")
    args = parser.parse_args()

    manifest_path = resolve_manifest_path(args.manifest)
    try:
        out_path, applied, skipped, generators = apply_approved(manifest_path)
    except ValueError as exc:
        print(str(exc))
        return 1

    print(f"Wrote {out_path.relative_to(ROOT)}")
    print(f"Applied operations: {len(applied)}")
    print(f"Skipped operations: {len(skipped)}")
    print(f"Generator commands: {len(generators)}")
    print(f"Updated {manifest_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
