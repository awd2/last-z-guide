#!/usr/bin/env python3
"""Deterministic contract tests for the Worker chain."""

from __future__ import annotations

import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from automation.io import load_json, load_run_manifest, write_json, write_run_manifest
from automation.reports import llm_approved_handoffs, llm_auto_review_latest, llm_owner_digest, llm_owner_issue, llm_review_latest, llm_topic_decisions
from automation import apply_approved, apply_preview, approval, close_run, exact_proposals, patch_planner, pipeline, proposal_renderer
from automation.source_resolver import SourceResolution
from automation.workers import editor, external_evidence_collect, external_evidence_refresh, external_scout, external_search_collect, intake, intake_to_run, llm_adapter, llm_auto_review_queue, llm_candidate_refresh, llm_editor, llm_intake, llm_reviewer, llm_run_approved_handoffs, llm_scout, llm_topic_decision, llm_topic_discovery, llm_worker_chain, reviewer, run_chain, scout, write_manifest
from scripts import bing_weekly


ROOT = Path(__file__).resolve().parents[2]


def fixture_codes_guide_verified_snippet() -> str:
    return editor.html_context("codes.html")["source_snippets"]["guide_verified"]


def fixture_signals() -> dict:
    return {
        "report_type": "gsc_weekly_agent_signals",
        "generated_for": "fixture-window",
        "page_opportunities": [
            {
                "page": "https://lastzguides.com/codes.html",
                "local_page": "codes.html",
                "impressions": 6400,
                "clicks": 96,
                "ctr": 0.015,
                "position": 4.2,
            }
        ],
        "query_page_pairs": [
            {
                "query": "last z codes",
                "page": "https://lastzguides.com/codes.html",
                "local_page": "codes.html",
                "impressions": 4000,
                "clicks": 70,
                "ctr": 0.0175,
                "position": 3.8,
            },
            {
                "query": "last z survival shooter codes",
                "page": "https://lastzguides.com/codes.html",
                "local_page": "codes.html",
                "impressions": 1800,
                "clicks": 20,
                "ctr": 0.0111,
                "position": 5.1,
            },
        ],
        "query_opportunities": {
            "low_ctr_good_positions": [
                {
                    "query": "last z codes",
                    "impressions": 4000,
                    "clicks": 70,
                    "ctr": 0.0175,
                    "position": 3.8,
                }
            ]
        },
        "trend_signals": {
            "rising_queries_last_7_vs_previous_7": [
                {
                    "query": "last z codes",
                    "delta_impressions": 350,
                }
            ]
        },
    }


def fixture_bing_signals() -> dict:
    payload = fixture_signals()
    payload["report_type"] = "bing_weekly_agent_signals"
    return payload


def fixture_llm_scout_response() -> dict:
    return {
        "response_json": {
            "overview": "Codes has enough search signal for human review, but Scout should keep the page role narrow.",
            "selected_opportunities": [
                {
                    "topic_id": "codes-gsc-opportunity",
                    "decision": "update_existing",
                    "rationale": "The deterministic signal points to CTR and query-fit review for the existing codes hub.",
                    "player_value": "Make the first-screen answer and Gift Center route clearer for players searching active codes.",
                    "duplication_risk": "Low if the update stays on codes.html and does not absorb Gift Center setup troubleshooting.",
                    "priority": "high",
                    "risk_level": "high",
                    "next_step": "Run the deterministic Editor brief and require owner approval before content changes.",
                    "claims_to_verify": ["gift_center_cluster_roles"],
                }
            ],
            "rejected_or_monitor": [],
            "global_risks": ["Analytics can identify opportunity, but it must not force a broad rewrite."],
            "next_actions": ["Review the selected opportunity with the existing worker-chain command."],
        }
    }


def fixture_external_source_registry() -> dict:
    return {
        "schema_version": 1,
        "updated_at": "2026-05-12",
        "policy": {
            "purpose": "Fixture external sources.",
            "forbidden_uses": ["copy_visible_text"],
        },
        "sources": [
            {
                "id": "fixture-lastz-reference",
                "name": "Fixture Last Z Reference",
                "base_url": "https://example.com",
                "status": "approved",
                "source_type": "competitor_reference",
                "trust_level": "medium",
                "allowed_uses": ["topic_discovery", "cross_validation"],
                "disallowed_uses": ["copy_visible_text", "single_source_fact_claims"],
                "crawl_policy": "explicit_url_only",
                "freshness_window_days": 30,
                "notes": "Fixture only.",
                "discovery_queries": [],
                "topic_seeds": [
                    {
                        "topic_id": "hq-upgrade-requirements",
                        "title": "External opportunity: HQ upgrade requirements",
                        "cluster": "Progression",
                        "recommended_action": "update_existing",
                        "archetype_suggestion": "support-guide",
                        "target_page_or_slug": "hq.html",
                        "priority": "high",
                        "confidence": "medium",
                        "risk_level": "high",
                        "source_urls": ["https://example.com/last-z/hq"],
                        "evidence": ["Competitor coverage suggests players compare HQ upgrade requirements."],
                        "claims_to_verify": ["hq_upgrade_requirements"],
                    }
                ],
                "discovery_queries": ["site:example.com Last Z HQ requirements"],
            }
        ],
    }


def fixture_external_llm_scout_response() -> dict:
    return {
        "response_json": {
            "overview": "External source signal is worth human review only as a verification-backed update.",
            "selected_opportunities": [
                {
                    "topic_id": "external-hq-upgrade-requirements",
                    "decision": "update_existing",
                    "rationale": "The source indicates a player job around HQ upgrade requirements that can be reviewed against existing site structure.",
                    "player_value": "Players can avoid misleading HQ upgrade planning if requirements are clearer.",
                    "duplication_risk": "Medium; keep it on the existing HQ page if that page owns the intent.",
                    "priority": "high",
                    "risk_level": "high",
                    "next_step": "Run no-write Editor/Reviewer and verify claims before public copy.",
                    "claims_to_verify": ["hq_upgrade_requirements"],
                }
            ],
            "rejected_or_monitor": [],
            "global_risks": ["External sources are discovery signals, not proof."],
            "next_actions": ["Require owner approval before any public content proposal."],
        }
    }


def fixture_llm_editor_response() -> dict:
    return {
        "response_json": {
            "brief_summary": "Plan a narrow codes.html first-screen and route review without writing final page copy.",
            "target_page_or_slug": "codes.html",
            "page_role": "cornerstone-guide",
            "primary_user_job": "Help players redeem Last Z codes through the correct Gift Center route.",
            "first_screen_plan": "Clarify the redeem path and UID/mailbox expectations without merging setup or troubleshooting pages.",
            "section_plan": [
                {
                    "section": "Quick Answer",
                    "action": "Review whether the first screen directly answers active-code and Gift Center intent.",
                    "reason": "The page is the Economy hub for code redemption.",
                }
            ],
            "internal_link_plan": [
                {
                    "page": "gift-center-uid.html",
                    "role": "downstream",
                    "reason": "Route UID/setup details to the dedicated support page.",
                }
            ],
            "protected_claims": ["gift-center-only-redeem-flow"],
            "do_not_change": ["Do not absorb redeem-code-not-working.html troubleshooting into codes.html."],
            "owner_questions": ["Has the prior Gift Center CTR pass already covered this first-screen issue?"],
            "required_context_before_patch": [
                "AGENTS.md",
                "automation/memory/site_style_guide.md",
                "automation/memory/page_archetypes.md",
                "automation/memory/seo_llm_optimization.md",
                "automation/memory/canonical_claims.json",
                "automation/memory/content_index.json",
                "automation/memory/entities.json",
                "automation/memory/release_checklist.md",
                "codes.html",
            ],
            "acceptance_checks": [
                "python3 scripts/prepublish_check.py",
                "python3 automation/pipeline.py checks --strict",
            ],
            "exact_replacements": [],
            "next_step": "Run deterministic Reviewer before any patch plan.",
        }
    }


def fixture_llm_reviewer_response() -> dict:
    return {
        "response_json": {
            "target_page_or_slug": "codes.html",
            "page_role": "cornerstone-guide",
            "verdict": "needs_human_review",
            "risk_level": "high",
            "approved_next_stage": "proposal",
            "blocking_issues": [],
            "warnings": [
                "codes.html is a cornerstone page; owner approval is required before any content proposal."
            ],
            "duplicate_intent_review": "The brief keeps Gift Center setup and troubleshooting on adjacent support pages.",
            "cluster_role_review": "The plan preserves codes.html as the redeem-codes hub.",
            "canonical_claim_review": "The official Gift Center, UID, and mailbox claims remain protected.",
            "template_safety_review": "The brief does not request template, schema, or navigation replacement.",
            "exact_replacement_review": "The Editor did not include exact replacement candidates.",
            "owner_approval_required": True,
            "owner_questions": ["Should this move to a human-reviewed proposal artifact?"],
            "required_context_before_edit": [
                "AGENTS.md",
                "automation/memory/site_style_guide.md",
                "automation/memory/page_archetypes.md",
                "automation/memory/seo_llm_optimization.md",
                "automation/memory/canonical_claims.json",
                "codes.html",
            ],
            "required_checks": [
                "python3 scripts/prepublish_check.py",
                "python3 automation/pipeline.py checks --strict",
            ],
            "next_step": "Ask the owner to approve or reject moving this planning brief into a proposal-only content artifact.",
        }
    }


def fixture_approved_topic_decision() -> dict:
    proposal = {
        "topic_id": "codes-gsc-opportunity",
        "title": "GSC opportunity review: Last Z Redeem Codes",
        "cluster": "Economy",
        "recommended_action": "update_existing",
        "archetype_suggestion": "cornerstone-guide",
        "target_page_or_slug": "codes.html",
        "source_type": "analytics",
        "source_reference": "GSC weekly fixture",
        "confidence": "high",
        "priority": "high",
        "risk_level": "high",
        "status": "candidate",
        "notes": "Codes has enough signal for a no-write worker-chain pass.",
        "evidence": ["GSC page signal fixture."],
        "site_fit": {
            "primary_user_job": "Help players redeem Last Z codes through the correct Gift Center route.",
            "cluster_owner": "Economy",
            "expected_internal_route": ["index.html", "codes.html"],
            "archetype_reason": "Existing codes hub owns code redemption intent.",
        },
        "constraints": ["Use existing page template."],
        "reject_if": ["The query intent is already served."],
        "claims_to_verify": ["gift-center-only-redeem-flow"],
    }
    return {
        "schema_version": 1,
        "report_type": "llm_topic_decision",
        "generated_at": "2026-05-05T00:00:00Z",
        "state": "decision_recorded",
        "topic_id": "codes-gsc-opportunity",
        "decision_state": "approved_for_chain",
        "decided_by": "fixture",
        "decision_note": "Approved for a no-write worker-chain pass only.",
        "source_discovery": "automation/reports/llm-topic-discovery.json",
        "topic_snapshot": proposal,
        "allows_worker_chain": True,
        "allows_content_edit": False,
        "next_actions": ["Run no-write chain from decision."],
        "errors": [],
    }


class WorkerContractTests(unittest.TestCase):
    def test_patch_planner_emits_safe_exact_replace_spec_from_exact_proposal(self) -> None:
        source = SourceResolution(
            target_file="sample.html",
            source_of_truth_file="sample.html",
            output_file="sample.html",
            source_type="html_file",
            is_generated=False,
            generator_command=None,
            edit_policy="Edit the target file directly.",
        )
        proposal = {
            "file": "sample.html",
            "change_type": "first_screen_update",
            "reason": "Apply owner-reviewed exact text.",
            "selector_or_anchor": ".guide-verified",
            "exact_old": "<p>Old approved-before copy.</p>",
            "exact_new": "<p>New owner-approved copy.</p>",
        }

        with patch.object(patch_planner, "resolve_source", return_value=source):
            specs = patch_planner.build_patch_specs(
                [proposal],
                canonical_ids=[],
                deterministic_checks=["python3 scripts/prepublish_check.py"],
            )

        self.assertEqual(len(specs), 1)
        spec = specs[0]
        self.assertEqual(spec["operation_type"], "safe_exact_replace")
        self.assertEqual(spec["selector_or_anchor"], ".guide-verified")
        self.assertEqual(spec["exact_old"], "<p>Old approved-before copy.</p>")
        self.assertEqual(spec["exact_new"], "<p>New owner-approved copy.</p>")
        self.assertTrue(spec["human_approval_required"])

    def test_patch_planner_uses_manifest_exact_replacements_without_generic_noise(self) -> None:
        manifest = type(
            "ManifestFixture",
            (),
            {
                "plan": {
                    "target_page_or_slug": "sample.html",
                    "archetype_suggestion": "support-guide",
                    "exact_replacements": [
                        {
                            "file": "sample.html",
                            "change_type": "first_screen_update",
                            "selector_or_anchor": ".guide-verified",
                            "exact_old": "<p>Old approved-before copy.</p>",
                            "exact_new": "<p>New owner-approved copy.</p>",
                        }
                    ],
                },
                "inputs": {},
                "artifacts": {},
            },
        )()

        proposals = patch_planner.propose_change_types(manifest)

        matching = [
            proposal
            for proposal in proposals
            if proposal["file"] == "sample.html" and proposal["change_type"] == "first_screen_update"
        ]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0]["exact_old"], "<p>Old approved-before copy.</p>")
        self.assertEqual([proposal["change_type"] for proposal in proposals], ["first_screen_update"])

    def test_worker_run_plan_preserves_exact_replacements_from_intake(self) -> None:
        intake = {
            "state": "approved_for_intake",
            "source_topic_id": "sample-topic",
            "target_page_or_slug": "sample.html",
            "risk_level": "medium",
            "approved_by": "fixture",
            "approval_note": "Approved for run-plan only.",
            "proposed_backlog_item": {
                "topic_id": "sample-topic",
                "title": "Sample exact proposal",
                "cluster": "Site",
                "recommended_action": "update_existing",
                "archetype_suggestion": "support-guide",
                "target_page_or_slug": "sample.html",
                "source_type": "fixture",
                "source_reference": "fixture",
                "confidence": "high",
                "priority": "medium",
                "status": "candidate",
                "notes": "Fixture exact replacement.",
            },
            "exact_replacements": [
                {
                    "file": "sample.html",
                    "change_type": "first_screen_update",
                    "selector_or_anchor": ".guide-verified",
                    "exact_old": "<p>Old approved-before copy.</p>",
                    "exact_new": "<p>New owner-approved copy.</p>",
                }
            ],
        }

        proposal = intake_to_run.build_proposal(intake, Path("automation/reports/fixture-intake.json"))

        self.assertEqual(proposal["state"], "run_plan_ready")
        exact = proposal["proposed_manifest"]["plan"]["exact_replacements"]
        self.assertEqual(len(exact), 1)
        self.assertEqual(exact[0]["exact_new"], "<p>New owner-approved copy.</p>")

    def test_llm_editor_request_prefers_exact_replacements_for_existing_html(self) -> None:
        proposal = {
            "topic_id": "research-route-clarity",
            "title": "Research route clarity",
            "cluster": "Research",
            "recommended_action": "update_existing",
            "archetype_suggestion": "atlas-page",
            "target_page_or_slug": "research-costs.html",
            "site_fit": {
                "primary_user_job": "Clarify the post-Peace Shield route choice without broadening the atlas page.",
                "expected_internal_route": ["research.html", "research-costs.html"],
            },
            "constraints": ["Protect `research-best-mainline`."],
            "evidence": ["query: `last z research costs`"],
        }
        selected = {
            "topic_id": "research-route-clarity",
            "decision": "update_existing",
            "priority": "high",
            "risk_level": "high",
        }

        brief = editor.build_editor_brief(proposal, Path("automation/reports/fixture-scout.json"))
        request = llm_editor.build_request(
            selected=selected,
            proposal=proposal,
            deterministic_brief=brief,
            request_id="llm-editor-request-fixture",
            scout_result_path=Path("automation/reports/fixture-scout-result.json"),
            scout_request_path=Path("automation/reports/fixture-scout-request.json"),
        )

        snippets = request["inputs"]["deterministic_editor_brief"]["current_page_snapshot"]["source_snippets"]
        guardrails = " ".join(request["inputs"]["guardrails"])
        self.assertIn("recommended_route_section", snippets)
        self.assertIn("quick_answer_section", snippets)
        self.assertIn("prefer narrow exact_replacements", request["prompt"])
        self.assertIn("recommended_route_section", guardrails)

    def test_llm_exact_replacement_full_lifecycle_on_temp_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            reports_dir = tmp_path / "reports"
            page_path = tmp_path / "sample.html"
            page_path.write_text(
                "<html><head><title>Old exact title</title></head><body><p class=\"guide-verified\">Old exact copy.</p></body></html>",
                encoding="utf-8",
            )
            intake = {
                "state": "approved_for_intake",
                "source_topic_id": "sample-topic",
                "target_page_or_slug": "sample.html",
                "risk_level": "medium",
                "approved_by": "fixture",
                "approval_note": "Approved for run-plan only.",
                "proposed_backlog_item": {
                    "topic_id": "sample-topic",
                    "title": "Sample exact lifecycle proposal",
                    "cluster": "Site",
                    "recommended_action": "update_existing",
                    "archetype_suggestion": "support-guide",
                    "target_page_or_slug": "sample.html",
                    "source_type": "fixture",
                    "source_reference": "fixture",
                    "confidence": "high",
                    "priority": "medium",
                    "status": "candidate",
                    "notes": "Fixture exact replacement.",
                },
                "exact_replacements": [
                    {
                        "file": "sample.html",
                        "change_type": "meta_refresh",
                        "selector_or_anchor": "<title>",
                        "exact_old": "<title>Old exact title</title>",
                        "exact_new": "<title>New exact title</title>",
                        "reason": "Fixture exact lifecycle title replacement.",
                        "owner_approval_required": True,
                    },
                    {
                        "file": "sample.html",
                        "change_type": "first_screen_update",
                        "selector_or_anchor": ".guide-verified",
                        "exact_old": '<p class="guide-verified">Old exact copy.</p>',
                        "exact_new": '<p class="guide-verified">New exact copy.</p>',
                        "reason": "Fixture exact lifecycle replacement.",
                        "owner_approval_required": True,
                    }
                ],
            }
            run_plan = intake_to_run.build_proposal(intake, tmp_path / "llm-intake.json")
            manifest_payload = run_plan["proposed_manifest"]
            manifest_path = tmp_path / "manifest.json"
            write_json(manifest_path, manifest_payload)

            source = SourceResolution(
                target_file="sample.html",
                source_of_truth_file="sample.html",
                output_file="sample.html",
                source_type="html_file",
                is_generated=False,
                generator_command=None,
                edit_policy="Edit the target file directly.",
            )
            with patch.object(patch_planner, "resolve_source", return_value=source):
                manifest = load_run_manifest(manifest_path)
                manifest.status = "draft_brief_ready"
                patch_plan, markdown = patch_planner.build_patch_plan(manifest)
                patch_report = reports_dir / f"{manifest.run_id}.patch.md"
                reports_dir.mkdir(parents=True, exist_ok=True)
                patch_report.write_text(markdown, encoding="utf-8")
                manifest.status = "patch_plan_ready"
                manifest.artifacts.setdefault("patch_plan", {})
                manifest.artifacts["patch_plan"] = patch_plan
                manifest.artifacts["patch_plan"]["report_path"] = str(patch_report)
                manifest.changed_files = list(patch_plan["changed_files"])
                write_run_manifest(manifest_path, manifest)

            proposal_path, rendered_specs = proposal_renderer.render_proposal(manifest_path, reports_dir)
            self.assertEqual(len(rendered_specs), 2)
            self.assertTrue(all(spec["operation_type"] == "safe_exact_replace" for spec in rendered_specs))
            self.assertIn("New exact copy", proposal_path.read_text(encoding="utf-8"))

            with patch.object(
                approval,
                "render_proposal",
                lambda path: proposal_renderer.render_proposal(path, reports_dir),
            ), patch.object(approval, "ROOT", tmp_path):
                code = approval.cmd_approval(
                    argparse.Namespace(
                        run_id=str(manifest_path),
                        state="approved",
                        source=None,
                        target=None,
                        operation=None,
                        all=True,
                        note="Owner approved temp fixture exact replacement.",
                        dry_run=False,
                    )
                )
            self.assertEqual(code, 0)
            self.assertEqual(load_json(manifest_path)["status"], "approved_for_apply")

            with patch.object(apply_preview, "ROOT", tmp_path), patch.object(apply_preview, "REPORTS_DIR", reports_dir):
                preview_path, preview_items = apply_preview.render_apply_preview(manifest_path)
            self.assertTrue(preview_path.exists())
            self.assertEqual(preview_items[0]["preview_action"], "safe_exact_replace")
            self.assertEqual(preview_items[0]["warnings"], [])

            with patch.object(apply_approved, "ROOT", tmp_path), patch.object(apply_approved, "REPORTS_DIR", reports_dir):
                result_path, applied, skipped, generators = apply_approved.apply_approved(manifest_path)
            self.assertTrue(result_path.exists())
            self.assertEqual(
                applied,
                [
                    "sample.html:safe_exact_replace:<title>",
                    "sample.html:safe_exact_replace:.guide-verified",
                ],
            )
            self.assertEqual(skipped, [])
            self.assertEqual(generators, [])
            self.assertIn("New exact title", page_path.read_text(encoding="utf-8"))
            self.assertIn("New exact copy", page_path.read_text(encoding="utf-8"))
            self.assertEqual(load_json(manifest_path)["status"], "applied_pending_qa")

    def test_proposal_renderer_shows_exact_replace_candidate(self) -> None:
        manifest = type(
            "ManifestFixture",
            (),
            {
                "artifacts": {
                    "patch_plan": {
                        "target_page_or_slug": "sample.html",
                        "patch_specs": [
                            {
                                "target_file": "sample.html",
                                "source_of_truth_file": "sample.html",
                                "output_file": "sample.html",
                                "source_type": "html_file",
                                "is_generated": False,
                                "generator_command": None,
                                "operation_type": "safe_exact_replace",
                                "selector_or_anchor": ".guide-verified",
                                "required_preconditions": [],
                                "proposed_change_summary": "Apply exact approved copy.",
                                "canonical_claims_to_protect": [],
                                "validation_commands": [],
                                "human_approval_required": True,
                                "exact_old": "<p>Old approved-before copy.</p>",
                                "exact_new": "<p>New owner-approved copy.</p>",
                            }
                        ],
                    }
                },
                "plan": {"target_page_or_slug": "sample.html"},
            },
        )()

        rendered = proposal_renderer.build_rendered_specs(manifest)

        self.assertEqual(rendered[0]["operation_type"], "safe_exact_replace")
        self.assertEqual(rendered[0]["selector_or_anchor"], ".guide-verified")
        self.assertIn("Exact approved replacement candidate", rendered[0]["suggested_content"])
        self.assertIn("<p>Old approved-before copy.</p>", rendered[0]["suggested_content"])
        self.assertIn("<p>New owner-approved copy.</p>", rendered[0]["suggested_content"])

    def test_exact_proposals_render_compact_before_after_only(self) -> None:
        manifest = type(
            "ManifestFixture",
            (),
            {
                "run_id": "fixture-exact-review",
                "status": "proposal_ready",
                "summary": "Fixture exact owner review.",
                "risk_level": "medium",
                "artifacts": {
                    "proposal": {
                        "rendered_specs": [
                            {
                                "target_file": "sample.html",
                                "source_of_truth_file": "sample.html",
                                "output_file": "sample.html",
                                "operation_type": "safe_exact_replace",
                                "selector_or_anchor": ".guide-verified",
                                "risk_level": "medium",
                                "approval_state": "proposed",
                                "human_approval_required": True,
                                "proposed_change_summary": "Apply exact owner-reviewed copy.",
                                "exact_old": "<p>Old approved-before copy.</p>",
                                "exact_new": "<p>New owner-approved copy.</p>",
                                "validation_commands": ["python3 scripts/prepublish_check.py"],
                            },
                            {
                                "target_file": "sample.html",
                                "source_of_truth_file": "sample.html",
                                "output_file": "sample.html",
                                "operation_type": "meta_refresh",
                                "selector_or_anchor": "<title>",
                            },
                        ]
                    }
                },
                "plan": {"target_page_or_slug": "sample.html"},
            },
        )()

        review = exact_proposals.build_exact_review(manifest)
        markdown = exact_proposals.render_markdown(review)

        self.assertEqual(review["exact_proposal_count"], 1)
        self.assertEqual(review["non_exact_proposal_count"], 1)
        self.assertIn("Before:", markdown)
        self.assertIn("After:", markdown)
        self.assertIn("<p>Old approved-before copy.</p>", markdown)
        self.assertIn("<p>New owner-approved copy.</p>", markdown)
        self.assertNotIn("meta_refresh", markdown)

    def test_pipeline_propose_renders_exact_proposals_after_proposal_report(self) -> None:
        calls: list[tuple[str, list[str]]] = []

        def fake_run_step(name: str, command: list[str]) -> int:
            calls.append((name, command))
            return 0

        with patch.object(pipeline, "run_step", fake_run_step):
            code = pipeline.cmd_propose("fixture-run", "/tmp/proposal-output")

        self.assertEqual(code, 0)
        self.assertEqual([name for name, _command in calls], ["Proposal Renderer", "Exact Proposal Review"])
        self.assertIn("proposal_renderer.py", calls[0][1][1])
        self.assertIn("exact_proposals.py", calls[1][1][1])
        self.assertEqual(calls[0][1][-2:], ["--output-dir", "/tmp/proposal-output"])
        self.assertEqual(calls[1][1][-2:], ["--output-dir", "/tmp/proposal-output"])

    def test_safe_exact_replace_apply_and_preview(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            page_path = tmp_path / "sample.html"
            manifest_path = tmp_path / "manifest.json"
            reports_dir = tmp_path / "reports"
            page_path.write_text("<html><title>Old Title</title><h1>Old Title</h1></html>", encoding="utf-8")
            write_json(
                manifest_path,
                {
                    "run_id": "fixture-safe-exact-replace",
                    "created_at": "2026-05-10T00:00:00Z",
                    "run_type": "update_existing",
                    "status": "approved_for_apply",
                    "risk_level": "medium",
                    "summary": "Fixture exact replacement.",
                    "inputs": {},
                    "plan": {"target_page_or_slug": "sample.html"},
                    "artifacts": {
                        "patch_plan": {
                            "patch_specs": [
                                {
                                    "target_file": "sample.html",
                                    "source_of_truth_file": "sample.html",
                                    "output_file": "sample.html",
                                    "source_type": "html_file",
                                    "is_generated": False,
                                    "operation_type": "safe_exact_replace",
                                    "selector_or_anchor": "<title>",
                                    "approval_state": "approved",
                                    "exact_old": "<title>Old Title</title>",
                                    "exact_new": "<title>New Title</title>",
                                    "validation_commands": ["python3 scripts/prepublish_check.py"],
                                }
                            ]
                        }
                    },
                    "changed_files": ["sample.html"],
                    "checks": {},
                    "review": {
                        "verdict": "needs_human_review",
                        "open_questions": [],
                        "next_action": "apply",
                        "reviewer_notes": "",
                    },
                },
            )

            with patch.object(apply_preview, "ROOT", tmp_path), patch.object(apply_preview, "REPORTS_DIR", reports_dir):
                preview_path, preview_items = apply_preview.render_apply_preview(manifest_path)
            self.assertTrue(preview_path.exists())
            self.assertEqual(preview_items[0]["preview_action"], "safe_exact_replace")
            self.assertEqual(preview_items[0]["warnings"], [])

            with patch.object(apply_approved, "ROOT", tmp_path), patch.object(apply_approved, "REPORTS_DIR", reports_dir):
                result_path, applied, skipped, generators = apply_approved.apply_approved(manifest_path)

            self.assertTrue(result_path.exists())
            self.assertIn("<title>New Title</title>", page_path.read_text(encoding="utf-8"))
            self.assertEqual(applied, ["sample.html:safe_exact_replace:<title>"])
            self.assertEqual(skipped, [])
            self.assertEqual(generators, [])
            manifest = load_json(manifest_path)
            self.assertEqual(manifest["status"], "applied_pending_qa")

    def test_safe_exact_replace_fails_on_ambiguous_old_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            page_path = tmp_path / "sample.html"
            manifest_path = tmp_path / "manifest.json"
            page_path.write_text("<p>Repeat me</p><p>Repeat me</p>", encoding="utf-8")
            write_json(
                manifest_path,
                {
                    "run_id": "fixture-safe-exact-replace-ambiguous",
                    "created_at": "2026-05-10T00:00:00Z",
                    "run_type": "update_existing",
                    "status": "approved_for_apply",
                    "risk_level": "medium",
                    "summary": "Fixture ambiguous exact replacement.",
                    "inputs": {},
                    "plan": {"target_page_or_slug": "sample.html"},
                    "artifacts": {
                        "patch_plan": {
                            "patch_specs": [
                                {
                                    "target_file": "sample.html",
                                    "source_of_truth_file": "sample.html",
                                    "output_file": "sample.html",
                                    "source_type": "html_file",
                                    "is_generated": False,
                                    "operation_type": "safe_exact_replace",
                                    "selector_or_anchor": "paragraph",
                                    "approval_state": "approved",
                                    "exact_old": "<p>Repeat me</p>",
                                    "exact_new": "<p>Replace me</p>",
                                }
                            ]
                        }
                    },
                    "changed_files": ["sample.html"],
                    "checks": {},
                },
            )

            with patch.object(apply_approved, "ROOT", tmp_path):
                with self.assertRaisesRegex(ValueError, "ambiguous"):
                    apply_approved.apply_approved(manifest_path)

    def test_llm_adapter_fail_closed_and_fixture_provider(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            request = {
                "schema_version": 1,
                "request_id": "fixture-editor-brief",
                "worker_role": "editor",
                "task": "Return a structured draft note for an approved topic.",
                "prompt": "Use the supplied site memory and return JSON only.",
                "inputs": {
                    "target_page_or_slug": "codes.html",
                    "cluster": "Economy",
                },
                "expected_response_keys": ["summary", "risk_level", "next_action"],
            }
            fixture_response = {
                "response_json": {
                    "summary": "Keep the Gift Center page role narrow.",
                    "risk_level": "medium",
                    "next_action": "review",
                }
            }
            request_path = tmp_path / "request.json"
            fixture_path = tmp_path / "response.json"
            output_path = tmp_path / "llm-result.json"
            write_json(request_path, request)
            write_json(fixture_path, fixture_response)

            code, blocked = llm_adapter.run_adapter(request_path, "disabled", None)
            self.assertEqual(code, 1)
            self.assertEqual(blocked["state"], "blocked")
            self.assertIsNone(blocked["response_json"])

            code, completed = llm_adapter.run_adapter(request_path, "fixture", fixture_path)
            self.assertEqual(code, 0)
            self.assertEqual(completed["state"], "completed")
            self.assertEqual(completed["response_json"]["risk_level"], "medium")
            self.assertEqual(completed["errors"], [])
            written = llm_adapter.write_output(completed, str(output_path))
            self.assertEqual(written, output_path)
            self.assertTrue(output_path.exists())

            bad_fixture_path = tmp_path / "bad-response.json"
            write_json(bad_fixture_path, {"response_json": {"summary": "Incomplete"}})
            code, bad = llm_adapter.run_adapter(request_path, "fixture", bad_fixture_path)
            self.assertEqual(code, 1)
            self.assertEqual(bad["state"], "blocked")
            self.assertIn("Response is missing expected key `risk_level`.", bad["errors"])

            non_ascii_fixture_path = tmp_path / "non-ascii-response.json"
            write_json(
                non_ascii_fixture_path,
                {
                    "response_json": {
                        "summary": "Use HQ30->35 planning, but avoid odd glyphs like →.",
                        "risk_level": "medium",
                        "next_action": "review",
                    }
                },
            )
            code, non_ascii = llm_adapter.run_adapter(request_path, "fixture", non_ascii_fixture_path)
            self.assertEqual(code, 1)
            self.assertEqual(non_ascii["state"], "blocked")
            self.assertTrue(any("plain ASCII English" in error for error in non_ascii["errors"]))

            exempt_request_path = tmp_path / "exempt-request.json"
            write_json(
                exempt_request_path,
                {
                    **load_json(request_path),
                    "ascii_validation_exempt_paths": ["response_json.exact_replacements"],
                    "expected_response_keys": ["summary", "risk_level", "next_action", "exact_replacements"],
                },
            )
            exempt_fixture_path = tmp_path / "exempt-response.json"
            write_json(
                exempt_fixture_path,
                {
                    "response_json": {
                        "summary": "ASCII planning text remains enforced.",
                        "risk_level": "medium",
                        "next_action": "review",
                        "exact_replacements": [{"exact_new": "Unsafe arrow → should be sanitized by caller."}],
                    }
                },
            )
            code, exempt = llm_adapter.run_adapter(exempt_request_path, "fixture", exempt_fixture_path)
            self.assertEqual(code, 0)
            self.assertEqual(exempt["state"], "completed")

    def test_llm_adapter_openai_provider_blocks_without_key(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            request_path = Path(tmp) / "request.json"
            write_json(
                request_path,
                {
                    "schema_version": 1,
                    "request_id": "fixture-editor-brief",
                    "worker_role": "editor",
                    "task": "Return a structured draft note for an approved topic.",
                    "prompt": "Use the supplied site memory and return JSON only.",
                    "inputs": {"target_page_or_slug": "codes.html"},
                    "expected_response_keys": ["summary", "risk_level", "next_action"],
                },
            )
            with patch.dict("os.environ", {"OPENAI_API_KEY": ""}, clear=False):
                code, blocked = llm_adapter.run_adapter(request_path, "openai", None)
            self.assertEqual(code, 1)
            self.assertEqual(blocked["state"], "blocked")
            self.assertEqual(blocked["provider"], "openai")
            self.assertTrue(any("OPENAI_API_KEY" in error for error in blocked["errors"]))

    def test_llm_adapter_openai_body_and_response_extraction(self) -> None:
        request = {
            "schema_version": 1,
            "request_id": "fixture-editor-brief",
            "worker_role": "editor",
            "task": "Return a structured draft note for an approved topic.",
            "prompt": "Use the supplied site memory and return JSON only.",
            "inputs": {"target_page_or_slug": "codes.html"},
            "expected_response_keys": ["summary", "risk_level", "next_action"],
        }
        with patch.dict(
            "os.environ",
            {"OPENAI_MODEL": "gpt-5.4-mini", "OPENAI_MAX_OUTPUT_TOKENS": "500"},
            clear=False,
        ):
            body = llm_adapter.openai_request_body(request)
        self.assertEqual(body["model"], "gpt-5.4-mini")
        self.assertEqual(body["max_output_tokens"], 500)
        self.assertEqual(body["text"]["format"]["type"], "json_schema")
        self.assertTrue(body["text"]["format"]["strict"])
        self.assertEqual(body["text"]["format"]["schema"]["required"], ["summary", "risk_level", "next_action"])

        request["max_output_tokens"] = 1200
        body = llm_adapter.openai_request_body(request)
        self.assertEqual(body["max_output_tokens"], 1200)

        payload = {
            "id": "resp_fixture",
            "model": "gpt-5.4-mini",
            "output": [
                {
                    "type": "message",
                    "content": [
                        {
                            "type": "output_text",
                            "text": json.dumps(
                                {
                                    "summary": "Keep the page role narrow.",
                                    "risk_level": "medium",
                                    "next_action": "review",
                                }
                            ),
                        }
                    ],
                }
            ],
        }
        self.assertEqual(llm_adapter.openai_response_json(payload)["next_action"], "review")

    def test_llm_scout_builds_request_and_runs_fixture_provider(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            fixture_path = tmp_path / "llm-scout-response.json"
            write_json(signals_path, fixture_signals())
            write_json(fixture_path, fixture_llm_scout_response())

            code, payload = llm_scout.run_llm_scout(
                signal_paths=[signals_path],
                external_proposal_paths=[],
                output_dir=tmp_path,
                basename="llm-scout-fixture",
                provider="fixture",
                fixture_path=fixture_path,
                limit=4,
                min_impressions=200,
            )
            self.assertEqual(code, 0)
            self.assertEqual(payload["report_type"], "llm_scout_review")
            self.assertEqual(payload["adapter_result"]["state"], "completed")
            self.assertEqual(payload["source_proposal_count"], 1)
            self.assertEqual(payload["adapter_result"]["response_json"]["selected_opportunities"][0]["topic_id"], "codes-gsc-opportunity")
            self.assertTrue((tmp_path / "llm-scout-fixture-request.json").exists())
            self.assertTrue((tmp_path / "llm-scout-fixture-result.json").exists())
            self.assertTrue((tmp_path / "llm-scout-fixture.md").exists())

    def test_llm_scout_blocks_monitor_decision_in_selected_opportunities(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            fixture_path = tmp_path / "llm-scout-response.json"
            response = fixture_llm_scout_response()
            response["response_json"]["selected_opportunities"][0]["decision"] = "monitor"
            write_json(signals_path, fixture_signals())
            write_json(fixture_path, response)

            code, payload = llm_scout.run_llm_scout(
                signal_paths=[signals_path],
                external_proposal_paths=[],
                output_dir=tmp_path,
                basename="llm-scout-fixture",
                provider="fixture",
                fixture_path=fixture_path,
                limit=4,
                min_impressions=200,
            )

            self.assertEqual(code, 1)
            self.assertEqual(payload["adapter_result"]["state"], "blocked")
            self.assertTrue(any("move it to rejected_or_monitor" in error for error in payload["adapter_result"]["errors"]))

    def test_external_scout_writes_no_write_candidate_proposals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            registry_path = tmp_path / "source-registry.json"
            write_json(registry_path, fixture_external_source_registry())

            code, payload = external_scout.build_external_scout(
                registry_path=registry_path,
                output_dir=tmp_path,
                basename="external-scout-fixture",
                include_proposed=False,
                limit=4,
            )

            self.assertEqual(code, 0)
            self.assertEqual(payload["report_type"], "external_scout")
            self.assertEqual(payload["state"], "external_scout_ready")
            self.assertEqual(payload["candidate_proposal_count"], 1)
            self.assertEqual(payload["source_query_task_count"], 1)
            proposal = payload["candidate_proposals"][0]
            self.assertEqual(proposal["topic_id"], "external-hq-upgrade-requirements")
            self.assertEqual(proposal["source_type"], "external")
            self.assertEqual(proposal["cross_validation_status"], "needs_second_source")
            self.assertFalse(payload["allows_content_edit"])
            self.assertTrue((tmp_path / "external-scout-fixture.json").exists())
            self.assertTrue((tmp_path / "external-scout-fixture.md").exists())

    def test_external_evidence_refresh_writes_no_write_evidence_queue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            registry_path = tmp_path / "source-registry.json"
            external_path = tmp_path / "external-scout-fixture.json"
            write_json(registry_path, fixture_external_source_registry())
            external_scout.build_external_scout(
                registry_path=registry_path,
                output_dir=tmp_path,
                basename="external-scout-fixture",
                include_proposed=False,
                limit=4,
            )

            code, payload = external_evidence_refresh.build_external_evidence_refresh(
                external_scout_path=external_path,
                output_dir=tmp_path,
                basename="external-evidence-fixture",
                limit=4,
            )

            self.assertEqual(code, 0)
            self.assertEqual(payload["report_type"], "external_evidence_refresh")
            self.assertEqual(payload["state"], "evidence_queue_ready")
            self.assertEqual(payload["source_query_task_count"], 1)
            self.assertEqual(payload["url_evidence_lead_count"], 1)
            self.assertEqual(payload["claim_review_count"], 1)
            self.assertFalse(payload["url_evidence_leads"][0]["public_claim_ready"])
            self.assertFalse(payload["allows_content_edit"])
            self.assertTrue((tmp_path / "external-evidence-fixture.json").exists())
            self.assertTrue((tmp_path / "external-evidence-fixture.md").exists())

    def test_external_evidence_collect_fixture_collects_no_write_url_leads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            registry_path = tmp_path / "source-registry.json"
            external_path = tmp_path / "external-scout-fixture.json"
            refresh_path = tmp_path / "external-evidence-fixture.json"
            write_json(registry_path, fixture_external_source_registry())
            external_scout.build_external_scout(
                registry_path=registry_path,
                output_dir=tmp_path,
                basename="external-scout-fixture",
                include_proposed=False,
                limit=4,
            )
            external_evidence_refresh.build_external_evidence_refresh(
                external_scout_path=external_path,
                output_dir=tmp_path,
                basename="external-evidence-fixture",
                limit=4,
            )

            code, payload = external_evidence_collect.build_external_evidence_collect(
                evidence_refresh_path=refresh_path,
                output_dir=tmp_path,
                basename="external-evidence-collect-fixture",
                provider="fixture",
                limit=4,
                timeout=1.0,
                max_bytes=10000,
            )

            self.assertEqual(code, 0)
            self.assertEqual(payload["report_type"], "external_evidence_collect")
            self.assertEqual(payload["state"], "evidence_collected")
            self.assertEqual(payload["provider"], "fixture")
            self.assertEqual(payload["url_lead_count"], 1)
            self.assertEqual(payload["collected_count"], 1)
            self.assertEqual(payload["failed_count"], 0)
            self.assertEqual(payload["query_task_count"], 1)
            self.assertFalse(payload["collected_evidence"][0]["public_claim_ready"])
            self.assertFalse(payload["allows_content_edit"])
            self.assertTrue((tmp_path / "external-evidence-collect-fixture.json").exists())
            self.assertTrue((tmp_path / "external-evidence-collect-fixture.md").exists())

    def test_external_search_collect_fixture_emits_no_write_candidate_proposals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            registry_path = tmp_path / "source-registry.json"
            external_path = tmp_path / "external-scout-fixture.json"
            refresh_path = tmp_path / "external-evidence-fixture.json"
            write_json(registry_path, fixture_external_source_registry())
            external_scout.build_external_scout(
                registry_path=registry_path,
                output_dir=tmp_path,
                basename="external-scout-fixture",
                include_proposed=False,
                limit=4,
            )
            external_evidence_refresh.build_external_evidence_refresh(
                external_scout_path=external_path,
                output_dir=tmp_path,
                basename="external-evidence-fixture",
                limit=4,
            )

            code, payload = external_search_collect.build_external_search_collect(
                evidence_refresh_path=refresh_path,
                output_dir=tmp_path,
                basename="external-search-collect-fixture",
                provider="fixture",
                limit=4,
                per_query_results=2,
                proposal_limit=4,
            )

            self.assertEqual(code, 0)
            self.assertEqual(payload["report_type"], "external_search_collect")
            self.assertEqual(payload["state"], "search_collected")
            self.assertEqual(payload["provider"], "fixture")
            self.assertEqual(payload["search_task_count"], 1)
            self.assertEqual(payload["searched_count"], 1)
            self.assertEqual(payload["failed_count"], 0)
            self.assertEqual(payload["candidate_proposal_count"], 1)
            self.assertEqual(payload["candidate_proposals"][0]["source_type"], "external_search")
            self.assertFalse(payload["allows_content_edit"])
            self.assertTrue((tmp_path / "external-search-collect-fixture.json").exists())
            self.assertTrue((tmp_path / "external-search-collect-fixture.md").exists())

    def test_external_search_collect_normalizes_clusters_and_targets(self) -> None:
        records = [
            {
                "search_status": "searched",
                "source_id": "fixture-source",
                "source_name": "Fixture Source",
                "trust_level": "high",
                "query": "site:fixture.example Last Z heroes",
                "results": [
                    {
                        "url": "https://fixture.example/en/heroes.html",
                        "title": "Heroes - Last Z Wiki | Tier List and Character Guide",
                        "evidence_summary": "Hero roster and tier-list page useful for entity coverage checks.",
                        "topic_fit": "high",
                        "suggested_cluster": "heroes_core",
                        "recommended_action": "update_existing",
                        "target_page_or_slug": "/en/heroes.html",
                        "primary_user_job": "Check hero roster and naming coverage.",
                        "claims_to_verify": ["hero_names"],
                        "public_claim_ready": False,
                    },
                    {
                        "url": "https://fixture.example/en/index.html",
                        "title": "Home",
                        "evidence_summary": "Generic homepage.",
                        "topic_fit": "high",
                        "suggested_cluster": "home",
                        "recommended_action": "update_existing",
                        "target_page_or_slug": "/en/index.html",
                        "primary_user_job": "Generic homepage.",
                        "claims_to_verify": [],
                        "public_claim_ready": False,
                    },
                ],
            }
        ]

        proposals = external_search_collect.build_candidate_proposals(records, limit=4)

        self.assertEqual(len(proposals), 2)
        self.assertEqual(proposals[0]["cluster"], "Heroes")
        self.assertEqual(proposals[0]["target_page_or_slug"], "heroes.html")
        self.assertEqual(proposals[0]["recommended_action"], "update_existing")
        self.assertEqual(proposals[0]["status"], "candidate")
        self.assertEqual(proposals[0]["deterministic_mapping"]["raw_suggested_cluster"], "heroes_core")
        self.assertEqual(proposals[1]["cluster"], "Home")
        self.assertEqual(proposals[1]["target_page_or_slug"], "index.html")
        self.assertEqual(proposals[1]["recommended_action"], "monitor")
        self.assertTrue(proposals[1]["deterministic_mapping"]["noise_result"])

    def test_llm_scout_accepts_external_scout_proposals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            registry_path = tmp_path / "source-registry.json"
            external_path = tmp_path / "external-scout-fixture.json"
            fixture_path = tmp_path / "llm-scout-response.json"
            write_json(registry_path, fixture_external_source_registry())
            write_json(fixture_path, fixture_external_llm_scout_response())
            external_scout.build_external_scout(
                registry_path=registry_path,
                output_dir=tmp_path,
                basename="external-scout-fixture",
                include_proposed=False,
                limit=4,
            )

            code, payload = llm_scout.run_llm_scout(
                signal_paths=[],
                external_proposal_paths=[external_path],
                output_dir=tmp_path,
                basename="llm-scout-external-fixture",
                provider="fixture",
                fixture_path=fixture_path,
                limit=4,
                min_impressions=200,
            )

            self.assertEqual(code, 0)
            self.assertEqual(payload["source_proposal_count"], 1)
            self.assertEqual(payload["external_proposal_count"], 1)
            self.assertEqual(payload["ready_topic_ids"], ["external-hq-upgrade-requirements"])

    def test_llm_topic_discovery_creates_backlog_shaped_no_write_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            scout_request_path = tmp_path / "llm-scout-review-request.json"
            scout_result_path = tmp_path / "llm-scout-review-result.json"
            write_json(
                scout_request_path,
                {
                    "inputs": {
                        "proposals": [
                            {
                                "topic_id": "codes-gsc-opportunity",
                                "title": "GSC opportunity review: Last Z Redeem Codes",
                                "cluster": "Economy",
                                "recommended_action": "update_existing",
                                "archetype_suggestion": "cornerstone-guide",
                                "target_page_or_slug": "codes.html",
                                "source_reference": "GSC weekly fixture",
                                "confidence": "high",
                                "priority": "high",
                                "risk_level": "high",
                                "evidence": ["GSC page signal fixture."],
                                "site_fit": {"expected_internal_route": ["index.html", "codes.html"]},
                                "constraints": ["Use existing page template."],
                                "reject_if": ["The query intent is already served."],
                            }
                        ]
                    }
                },
            )
            write_json(scout_result_path, {"state": "completed", **fixture_llm_scout_response()})

            with patch.object(llm_topic_discovery, "MANIFESTS_DIR", tmp_path / "manifests"):
                code, payload = llm_topic_discovery.run_topic_discovery(
                    scout_result_path=scout_result_path,
                    scout_request_path=scout_request_path,
                    output_dir=tmp_path,
                    basename="topic-discovery-fixture",
                )

            self.assertEqual(code, 0)
            self.assertEqual(payload["state"], "topic_discovery_ready")
            self.assertEqual(payload["topic_count"], 1)
            topic = payload["topics"][0]
            self.assertEqual(topic["topic_id"], "codes-gsc-opportunity")
            self.assertEqual(topic["backlog_row_preview"]["target_page_or_slug"], "codes.html")
            self.assertTrue(topic["human_approval_required"])
            self.assertTrue((tmp_path / "topic-discovery-fixture.json").exists())
            self.assertTrue((tmp_path / "topic-discovery-fixture.md").exists())

    def test_llm_candidate_refresh_runs_scout_and_topic_discovery_no_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            fixture_path = tmp_path / "llm-scout-response.json"
            write_json(signals_path, fixture_signals())
            write_json(fixture_path, fixture_llm_scout_response())

            with patch.object(llm_topic_discovery, "MANIFESTS_DIR", tmp_path / "manifests"):
                code, payload = llm_candidate_refresh.run_candidate_refresh(
                    signal_paths=[signals_path],
                    external_proposal_paths=[],
                    output_dir=tmp_path,
                    basename="llm-candidate-refresh-fixture",
                    scout_basename="llm-candidate-refresh-scout",
                    discovery_basename="llm-candidate-refresh-topic-discovery",
                    provider="fixture",
                    fixture_path=fixture_path,
                    limit=4,
                    min_impressions=200,
                )

            self.assertEqual(code, 0)
            self.assertEqual(payload["report_type"], "llm_candidate_refresh")
            self.assertEqual(payload["state"], "candidate_refresh_ready")
            self.assertEqual(payload["candidate_topic_ids"], ["codes-gsc-opportunity"])
            self.assertFalse(payload["allows_content_edit"])
            self.assertFalse(payload["allows_backlog_mutation"])
            self.assertFalse(payload["allows_manifest_mutation"])
            self.assertFalse(payload["allows_pr_or_deploy"])
            self.assertTrue((tmp_path / "llm-candidate-refresh-fixture.json").exists())
            self.assertTrue((tmp_path / "llm-candidate-refresh-fixture.md").exists())
            self.assertTrue((tmp_path / "llm-candidate-refresh-scout-result.json").exists())
            self.assertTrue((tmp_path / "llm-candidate-refresh-topic-discovery.json").exists())

    def test_llm_topic_discovery_includes_monitor_topics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            scout_request_path = tmp_path / "llm-scout-review-request.json"
            scout_result_path = tmp_path / "llm-scout-review-result.json"
            write_json(
                scout_request_path,
                {
                    "inputs": {
                        "proposals": [
                            {
                                "topic_id": "index-bing-opportunity",
                                "title": "Bing opportunity review: Last Z Guides",
                                "cluster": "Home",
                                "recommended_action": "update_existing",
                                "archetype_suggestion": "home-hub",
                                "target_page_or_slug": "index.html",
                                "source_reference": "Bing weekly fixture",
                                "confidence": "high",
                                "priority": "high",
                                "risk_level": "high",
                                "evidence": ["Bing page signal fixture."],
                                "site_fit": {"expected_internal_route": ["index.html"]},
                                "constraints": ["Use existing page template."],
                                "reject_if": ["The query intent is too broad."],
                            }
                        ]
                    }
                },
            )
            write_json(
                scout_result_path,
                {
                    "state": "completed",
                    "response_json": {
                        "overview": "Monitor homepage for now.",
                        "selected_opportunities": [],
                        "rejected_or_monitor": [
                            {
                                "topic_id": "index-bing-opportunity",
                                "reason": "Homepage signal is useful but too broad for a rewrite.",
                                "future_trigger": "Promote if repeated Bing/GSC signals stay stable.",
                            }
                        ],
                        "global_risks": [],
                        "next_actions": [],
                    },
                },
            )

            with patch.object(llm_topic_discovery, "MANIFESTS_DIR", tmp_path / "manifests"):
                code, payload = llm_topic_discovery.run_topic_discovery(
                    scout_result_path=scout_result_path,
                    scout_request_path=scout_request_path,
                    output_dir=tmp_path,
                    basename="topic-discovery-fixture",
                )

            self.assertEqual(code, 0)
            self.assertEqual(payload["topic_count"], 1)
            topic = payload["topics"][0]
            self.assertEqual(topic["topic_id"], "index-bing-opportunity")
            self.assertEqual(topic["status"], "monitor")
            self.assertEqual(topic["recommended_action"], "monitor")
            self.assertFalse(topic["human_approval_required"])
            self.assertIn("Homepage signal is useful", topic["notes"])

    def test_llm_topic_decision_records_owner_monitor_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            discovery_path = tmp_path / "topic-discovery-fixture.json"
            write_json(
                discovery_path,
                {
                    "schema_version": 1,
                    "report_type": "llm_topic_discovery",
                    "state": "topic_discovery_ready",
                    "topics": [
                        {
                            "topic_id": "research-gsc-opportunity",
                            "title": "GSC opportunity review: Last Z Research Guide",
                            "cluster": "Research",
                            "recommended_action": "update_existing",
                            "target_page_or_slug": "research.html",
                            "priority": "high",
                            "risk_level": "high",
                            "status": "candidate",
                            "notes": "Owner scope review required.",
                        }
                    ],
                },
            )

            code, payload = llm_topic_decision.run_topic_decision(
                discovery_path=discovery_path,
                topic_id="research-gsc-opportunity",
                decision_state="monitor",
                decided_by="fixture",
                note="Current cornerstone page already satisfies the opportunity.",
                output_dir=tmp_path,
                basename=None,
            )

            self.assertEqual(code, 0)
            self.assertEqual(payload["report_type"], "llm_topic_decision")
            self.assertEqual(payload["state"], "decision_recorded")
            self.assertEqual(payload["decision_state"], "monitor")
            self.assertFalse(payload["allows_worker_chain"])
            self.assertFalse(payload["allows_content_edit"])
            self.assertTrue((tmp_path / "llm-topic-decision-research-gsc-opportunity.json").exists())
            self.assertTrue((tmp_path / "llm-topic-decision-research-gsc-opportunity.md").exists())

    def test_llm_topic_decision_rerecords_from_prior_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            discovery_path = tmp_path / "topic-discovery-fixture.json"
            write_json(
                discovery_path,
                {
                    "schema_version": 1,
                    "report_type": "llm_topic_discovery",
                    "state": "topic_discovery_ready",
                    "topics": [
                        {
                            "topic_id": "research-gsc-opportunity",
                            "title": "GSC opportunity review: Last Z Research Guide",
                            "cluster": "Research",
                            "recommended_action": "update_existing",
                            "target_page_or_slug": "research.html",
                            "priority": "high",
                            "risk_level": "high",
                            "status": "candidate",
                            "notes": "Owner scope review required.",
                        }
                    ],
                },
            )
            monitor_code, monitor_payload = llm_topic_decision.run_topic_decision(
                discovery_path=discovery_path,
                topic_id="research-gsc-opportunity",
                decision_state="monitor",
                decided_by="fixture",
                note="Monitor first.",
                output_dir=tmp_path,
                basename=None,
            )
            self.assertEqual(monitor_code, 0)
            prior_path = tmp_path / "llm-topic-decision-research-gsc-opportunity.json"
            self.assertTrue(prior_path.exists())

            approve_code, approve_payload = llm_topic_decision.run_topic_decision(
                discovery_path=discovery_path,
                topic_id=None,
                decision_state="approved_for_chain",
                decided_by="fixture",
                note="Owner approved no-write chain replay.",
                output_dir=tmp_path,
                basename=None,
                from_decision_path=prior_path,
            )

            self.assertEqual(approve_code, 0)
            self.assertEqual(approve_payload["decision_state"], "approved_for_chain")
            self.assertTrue(approve_payload["allows_worker_chain"])
            self.assertFalse(approve_payload["allows_content_edit"])
            self.assertEqual(approve_payload["previous_decision"]["decision_state"], "monitor")
            self.assertEqual(approve_payload["topic_snapshot"], monitor_payload["topic_snapshot"])
            self.assertIn("--from-decision", approve_payload["next_actions"][0])
            written = load_json(prior_path)
            self.assertEqual(written["decision_state"], "approved_for_chain")
            self.assertEqual(written["previous_decision"]["decision_state"], "monitor")

    def test_llm_topic_decisions_summary_reports_allowed_topics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            write_json(
                tmp_path / "llm-topic-decision-a.json",
                {
                    "report_type": "llm_topic_decision",
                    "topic_id": "a",
                    "decision_state": "monitor",
                    "decided_by": "fixture",
                    "generated_at": "2026-05-05T00:00:00Z",
                    "allows_worker_chain": False,
                    "allows_content_edit": False,
                    "decision_note": "Monitor only.",
                    "next_actions": ["Do not edit content."],
                    "source_discovery": "fixture.json",
                    "markdown_path": "a.md",
                    "topic_snapshot": {
                        "target_page_or_slug": "a.html",
                        "cluster": "A",
                        "risk_level": "high",
                        "priority": "low",
                    },
                },
            )
            write_json(
                tmp_path / "llm-topic-decision-b.json",
                {
                    "report_type": "llm_topic_decision",
                    "topic_id": "b",
                    "decision_state": "approved_for_chain",
                    "decided_by": "fixture",
                    "generated_at": "2026-05-05T00:00:00Z",
                    "allows_worker_chain": True,
                    "allows_content_edit": False,
                    "decision_note": "No-write chain only.",
                    "next_actions": ["Run no-write chain."],
                    "source_discovery": "fixture.json",
                    "markdown_path": "b.md",
                    "topic_snapshot": {
                        "target_page_or_slug": "b.html",
                        "cluster": "B",
                        "risk_level": "high",
                        "priority": "high",
                    },
                },
            )

            report = llm_topic_decisions.build_report(tmp_path)
            self.assertEqual(report["decision_count"], 2)
            self.assertEqual(report["counts_by_state"]["monitor"], 1)
            self.assertEqual(report["counts_by_state"]["approved_for_chain"], 1)
            self.assertEqual(report["allowed_worker_chain_topics"], ["b"])
            self.assertEqual(report["content_edit_allowed_count"], 0)
            json_path, markdown_path = llm_topic_decisions.write_report(
                report,
                tmp_path / "llm-topic-decisions.json",
                tmp_path / "llm-topic-decisions.md",
            )
            self.assertTrue(json_path.exists())
            self.assertTrue(markdown_path.exists())
            self.assertIn("LLM Topic Decisions", markdown_path.read_text())

    def test_llm_approved_handoffs_lists_replay_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            write_json(
                tmp_path / "llm-topic-decision-a.json",
                {
                    "report_type": "llm_topic_decision",
                    "topic_id": "a",
                    "decision_state": "monitor",
                    "decided_by": "fixture",
                    "generated_at": "2026-05-05T00:00:00Z",
                    "allows_worker_chain": False,
                    "allows_content_edit": False,
                    "decision_note": "Monitor only.",
                    "next_actions": ["Do not edit content."],
                    "source_discovery": "fixture.json",
                    "markdown_path": "a.md",
                    "topic_snapshot": {
                        "target_page_or_slug": "a.html",
                        "cluster": "A",
                        "risk_level": "high",
                        "priority": "low",
                    },
                },
            )
            write_json(
                tmp_path / "llm-topic-decision-b.json",
                {
                    "report_type": "llm_topic_decision",
                    "topic_id": "b",
                    "decision_state": "approved_for_chain",
                    "decided_by": "fixture",
                    "generated_at": "2026-05-05T00:00:00Z",
                    "allows_worker_chain": True,
                    "allows_content_edit": False,
                    "decision_note": "No-write chain only.",
                    "next_actions": ["Run no-write chain."],
                    "source_discovery": "fixture.json",
                    "markdown_path": "b.md",
                    "topic_snapshot": {
                        "target_page_or_slug": "b.html",
                        "cluster": "B",
                        "risk_level": "high",
                        "priority": "high",
                    },
                },
            )

            view = llm_approved_handoffs.build_view(tmp_path, provider="fixture")
            self.assertEqual(view["approved_handoff_count"], 1)
            self.assertEqual(view["handoffs"][0]["topic_id"], "b")
            self.assertIn("--from-decision", view["handoffs"][0]["worker_chain_command"])
            self.assertIn("--provider fixture", view["handoffs"][0]["worker_chain_command"])
            self.assertIn("llm-topic-decision-b.json", view["handoffs"][0]["worker_chain_command"])
            markdown = llm_approved_handoffs.render_markdown(view)
            self.assertIn("LLM Approved Handoffs", markdown)
            self.assertIn("llm-worker-chain", markdown)

    def test_llm_auto_review_latest_builds_owner_decision_view(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            editor_result = tmp_path / "editor-result.json"
            reviewer_result = tmp_path / "reviewer-result.json"
            chain_path = tmp_path / "llm-worker-chain-fixture-topic.json"
            queue_path = tmp_path / "llm-auto-review-queue.json"
            write_json(
                editor_result,
                {
                    "response_json": {
                        "brief_summary": "Keep the target page narrow and useful.",
                        "primary_user_job": "Help players validate a specific task.",
                        "first_screen_plan": "Answer the player job immediately.",
                        "exact_replacements": [],
                    }
                },
            )
            write_json(
                reviewer_result,
                {
                    "response_json": {
                        "verdict": "needs_human_review",
                        "approved_next_stage": "brief",
                        "owner_approval_required": True,
                        "blocking_issues": [
                            {
                                "severity": "medium",
                                "issue": "Owner must confirm the player job.",
                                "required_fix": "Confirm the scope before intake.",
                            }
                        ],
                        "warnings": ["No public copy is approved."],
                        "owner_questions": ["Is this useful enough for players?"],
                        "required_checks": ["python3 automation/pipeline.py checks --strict"],
                    }
                },
            )
            write_json(
                chain_path,
                {
                    "state": "completed",
                    "provider": "fixture",
                    "source_topic_id": "fixture-topic",
                    "target_page_or_slug": "gift-center-uid.html",
                    "page_role": "support-guide",
                    "review_verdict": "needs_human_review",
                    "risk_level": "medium",
                    "approved_next_stage": "brief",
                    "owner_approval_required": True,
                    "errors": [],
                    "stages": {
                        "llm_editor": {"result_path": str(editor_result)},
                        "llm_reviewer": {"result_path": str(reviewer_result)},
                    },
                    "artifacts": {
                        "chain_json": str(chain_path),
                        "chain_markdown": str(tmp_path / "chain.md"),
                    },
                },
            )
            write_json(
                queue_path,
                {
                    "state": "queue_ready",
                    "provider": "fixture",
                    "candidate_topic_count": 1,
                    "queued_topic_count": 1,
                    "completed_item_count": 1,
                    "failed_item_count": 0,
                    "skipped_existing_count": 0,
                    "queue_items": [
                        {
                            "topic_id": "fixture-topic",
                            "target_page_or_slug": "gift-center-uid.html",
                            "cluster": "Economy",
                            "priority": "high",
                            "risk_level": "medium",
                            "score": 91,
                            "status": "completed",
                            "review_verdict": "needs_human_review",
                            "approved_next_stage": "brief",
                            "owner_approval_required": True,
                            "chain_json": str(chain_path),
                            "chain_markdown": str(tmp_path / "chain.md"),
                            "errors": [],
                        }
                    ],
                },
            )

            view = llm_auto_review_latest.build_view(queue_path)
            markdown = llm_auto_review_latest.render_markdown(view)

            self.assertEqual(view["needs_owner_decision_count"], 1)
            self.assertEqual(view["items"][0]["topic_id"], "fixture-topic")
            self.assertEqual(view["items"][0]["recommended_owner_action"], "answer_owner_questions_before_intake")
            self.assertIn("llm-intake-latest", view["items"][0]["approve_for_intake_command"])
            self.assertIn("LLM Auto Review Latest", markdown)

    def test_llm_auto_review_latest_includes_skipped_existing_chains(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            editor_result = tmp_path / "editor-result.json"
            reviewer_result = tmp_path / "reviewer-result.json"
            chain_path = tmp_path / "llm-worker-chain-fixture-topic.json"
            queue_path = tmp_path / "llm-auto-review-queue.json"
            write_json(
                editor_result,
                {
                    "response_json": {
                        "brief_summary": "Existing chain still needs owner review.",
                        "primary_user_job": "Validate a skipped existing topic.",
                        "first_screen_plan": "Keep it narrow.",
                        "exact_replacements": [],
                    }
                },
            )
            write_json(
                reviewer_result,
                {
                    "response_json": {
                        "verdict": "needs_human_review",
                        "approved_next_stage": "brief",
                        "owner_approval_required": True,
                        "blocking_issues": [],
                        "warnings": [],
                        "owner_questions": ["Should this existing chain move forward?"],
                        "required_checks": [],
                    }
                },
            )
            write_json(
                chain_path,
                {
                    "state": "completed",
                    "source_topic_id": "fixture-topic",
                    "review_verdict": "needs_human_review",
                    "approved_next_stage": "brief",
                    "owner_approval_required": True,
                    "stages": {
                        "llm_editor": {"result_path": str(editor_result)},
                        "llm_reviewer": {"result_path": str(reviewer_result)},
                    },
                },
            )
            write_json(
                queue_path,
                {
                    "state": "current",
                    "provider": "fixture",
                    "candidate_topic_count": 1,
                    "queued_topic_count": 0,
                    "completed_item_count": 0,
                    "failed_item_count": 0,
                    "skipped_existing_count": 1,
                    "queue_items": [],
                    "skipped_topics": [
                        {
                            "topic_id": "fixture-topic",
                            "target_page_or_slug": "gift-center-uid.html",
                            "cluster": "Economy",
                            "priority": "high",
                            "risk_level": "medium",
                            "score": 91,
                            "status": "skipped_existing_chain",
                            "existing_chain": str(chain_path),
                        }
                    ],
                },
            )

            view = llm_auto_review_latest.build_view(queue_path)

            self.assertEqual(view["needs_owner_decision_count"], 1)
            self.assertEqual(view["items"][0]["topic_id"], "fixture-topic")
            self.assertEqual(view["items"][0]["chain_json"], str(chain_path))

    def test_llm_auto_review_latest_respects_recorded_monitor_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            editor_result = tmp_path / "editor-result.json"
            reviewer_result = tmp_path / "reviewer-result.json"
            chain_path = tmp_path / "llm-worker-chain-fixture-topic.json"
            queue_path = tmp_path / "llm-auto-review-queue.json"
            decision_path = tmp_path / "llm-topic-decision-fixture-topic.json"
            write_json(
                editor_result,
                {
                    "response_json": {
                        "brief_summary": "Existing topic has already been owner-reviewed.",
                        "primary_user_job": "Validate a narrow support task.",
                        "first_screen_plan": "Keep the page unchanged.",
                        "exact_replacements": [],
                    }
                },
            )
            write_json(
                reviewer_result,
                {
                    "response_json": {
                        "verdict": "needs_human_review",
                        "approved_next_stage": "brief",
                        "owner_approval_required": True,
                        "blocking_issues": [
                            {
                                "severity": "medium",
                                "issue": "Owner must decide whether the topic is worth intake.",
                                "required_fix": "Record a topic decision.",
                            }
                        ],
                        "warnings": [],
                        "owner_questions": ["Should this move forward?"],
                        "required_checks": [],
                    }
                },
            )
            write_json(
                chain_path,
                {
                    "state": "completed",
                    "source_topic_id": "fixture-topic",
                    "review_verdict": "needs_human_review",
                    "approved_next_stage": "brief",
                    "owner_approval_required": True,
                    "stages": {
                        "llm_editor": {"result_path": str(editor_result)},
                        "llm_reviewer": {"result_path": str(reviewer_result)},
                    },
                },
            )
            write_json(
                queue_path,
                {
                    "state": "queue_ready",
                    "provider": "fixture",
                    "candidate_topic_count": 1,
                    "queued_topic_count": 1,
                    "completed_item_count": 1,
                    "failed_item_count": 0,
                    "skipped_existing_count": 0,
                    "queue_items": [
                        {
                            "topic_id": "fixture-topic",
                            "target_page_or_slug": "gift-center-uid.html",
                            "cluster": "Economy",
                            "priority": "high",
                            "risk_level": "medium",
                            "score": 91,
                            "status": "completed",
                            "owner_approval_required": True,
                            "chain_json": str(chain_path),
                        }
                    ],
                },
            )
            write_json(
                decision_path,
                {
                    "report_type": "llm_topic_decision",
                    "topic_id": "fixture-topic",
                    "decision_state": "monitor",
                    "decision_note": "Resolved by owner review; keep monitoring only.",
                    "allows_worker_chain": False,
                    "allows_content_edit": False,
                    "markdown_path": str(tmp_path / "llm-topic-decision-fixture-topic.md"),
                },
            )

            view = llm_auto_review_latest.build_view(queue_path)
            markdown = llm_auto_review_latest.render_markdown(view)

            self.assertEqual(view["needs_owner_decision_count"], 0)
            self.assertEqual(view["resolved_by_owner_decision_count"], 1)
            self.assertTrue(view["items"][0]["owner_decision_resolved"])
            self.assertEqual(view["items"][0]["recommended_owner_action"], "decision_recorded_monitor")
            self.assertEqual(view["items"][0]["approve_for_intake_command"], "")
            self.assertIn("Resolved by owner review", markdown)

    def test_llm_owner_digest_summarizes_resolved_only_queue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            queue_path = tmp_path / "llm-auto-review-queue.json"
            decision_path = tmp_path / "llm-topic-decision-fixture-topic.json"
            write_json(
                queue_path,
                {
                    "state": "current",
                    "provider": "fixture",
                    "candidate_topic_count": 1,
                    "queued_topic_count": 0,
                    "completed_item_count": 0,
                    "failed_item_count": 0,
                    "skipped_existing_count": 0,
                    "queue_items": [],
                    "skipped_topics": [],
                    "resolved_by_decision": [
                        {
                            "topic_id": "fixture-topic",
                            "target_page_or_slug": "gift-center-uid.html",
                            "cluster": "Economy",
                            "priority": "high",
                            "risk_level": "medium",
                            "score": 91,
                            "status": "resolved_by_decision_monitor",
                        }
                    ],
                },
            )
            write_json(
                decision_path,
                {
                    "report_type": "llm_topic_decision",
                    "topic_id": "fixture-topic",
                    "decision_state": "monitor",
                    "decision_note": "Already handled by owner.",
                    "allows_worker_chain": False,
                    "allows_content_edit": False,
                    "markdown_path": str(tmp_path / "llm-topic-decision-fixture-topic.md"),
                },
            )

            digest = llm_owner_digest.build_digest(queue_path)
            markdown = llm_owner_digest.render_markdown(digest)
            json_path, markdown_path = llm_owner_digest.write_digest(
                digest,
                tmp_path / "llm-owner-digest.json",
                tmp_path / "llm-owner-digest.md",
            )

            self.assertEqual(digest["state"], "no_action_needed")
            self.assertEqual(digest["counts"]["digest_needs_review"], 0)
            self.assertEqual(digest["counts"]["resolved_by_owner_decision"], 1)
            self.assertEqual(digest["recommended_next_action"], "No owner action needed; wait for new GSC/Bing/external-source signals.")
            self.assertIn("No owner action needed", markdown)
            self.assertTrue(json_path.exists())
            self.assertTrue(markdown_path.exists())

    def test_llm_owner_issue_skips_non_actionable_digest_without_token(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            digest_path = tmp_path / "llm-owner-digest.json"
            markdown_path = tmp_path / "llm-owner-digest.md"
            write_json(
                digest_path,
                {
                    "state": "no_candidates",
                    "generated_at": "2026-05-17T00:00:00Z",
                    "recommended_next_action": "No candidate topics are ready; wait for new signals.",
                    "counts": {},
                },
            )
            markdown_path.write_text("# Digest\n\nNo candidates.\n", encoding="utf-8")

            summary = llm_owner_issue.build_summary(
                digest_path=digest_path,
                markdown_path=markdown_path,
                repository="",
                token="",
                api_url="https://api.github.com",
                server_url="https://github.com",
                title="LLM Owner Digest: Action Needed",
                explicit_run_url=None,
                dry_run=False,
            )

            self.assertFalse(summary["actionable"])
            self.assertEqual(summary["action"], "skipped_non_actionable")
            self.assertIsNone(summary["issue_number"])

    def test_llm_owner_issue_renders_actionable_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            digest_path = tmp_path / "llm-owner-digest.json"
            markdown_path = tmp_path / "llm-owner-digest.md"
            write_json(
                digest_path,
                {
                    "state": "owner_review_needed",
                    "generated_at": "2026-05-17T00:00:00Z",
                    "recommended_next_action": "Review the listed topics and approve only if the player value and claims are valid.",
                    "counts": {
                        "candidate_topics": 2,
                        "digest_needs_review": 1,
                        "digest_ready_for_intake": 1,
                        "digest_failed": 0,
                        "resolved_by_owner_decision": 0,
                    },
                },
            )
            markdown_path.write_text("# Digest\n\n- `fixture-topic`\n", encoding="utf-8")

            summary = llm_owner_issue.build_summary(
                digest_path=digest_path,
                markdown_path=markdown_path,
                repository="awd2/last-z-guide",
                token="",
                api_url="https://api.github.com",
                server_url="https://github.com",
                title="LLM Owner Digest: Action Needed",
                explicit_run_url="https://github.com/awd2/last-z-guide/actions/runs/1",
                dry_run=True,
            )

            self.assertTrue(summary["actionable"])
            self.assertEqual(summary["action"], "dry_run")
            self.assertIn("LLM Owner Digest: Action Needed", summary["issue_body"])
            self.assertIn("owner_review_needed", summary["issue_body"])
            self.assertIn("https://github.com/awd2/last-z-guide/actions/runs/1", summary["issue_body"])

    def test_llm_owner_issue_closes_existing_issue_when_digest_resolved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            digest_path = tmp_path / "llm-owner-digest.json"
            markdown_path = tmp_path / "llm-owner-digest.md"
            write_json(
                digest_path,
                {
                    "state": "no_action_needed",
                    "generated_at": "2026-05-17T00:00:00Z",
                    "recommended_next_action": "No owner action needed; wait for new GSC/Bing/external-source signals.",
                    "counts": {
                        "candidate_topics": 1,
                        "digest_needs_review": 0,
                        "digest_ready_for_intake": 0,
                        "digest_failed": 0,
                        "resolved_by_owner_decision": 1,
                    },
                },
            )
            markdown_path.write_text("# Digest\n\nResolved.\n", encoding="utf-8")

            with patch(
                "automation.reports.llm_owner_issue.find_open_issue",
                return_value={"number": 42, "html_url": "https://github.com/awd2/last-z-guide/issues/42"},
            ), patch(
                "automation.reports.llm_owner_issue.github_request",
                return_value={"number": 42, "html_url": "https://github.com/awd2/last-z-guide/issues/42"},
            ) as request:
                summary = llm_owner_issue.build_summary(
                    digest_path=digest_path,
                    markdown_path=markdown_path,
                    repository="awd2/last-z-guide",
                    token="token",
                    api_url="https://api.github.com",
                    server_url="https://github.com",
                    title="LLM Owner Digest: Action Needed",
                    explicit_run_url="https://github.com/awd2/last-z-guide/actions/runs/1",
                    dry_run=False,
                )

            self.assertFalse(summary["actionable"])
            self.assertEqual(summary["action"], "closed_resolved")
            self.assertEqual(summary["issue_number"], 42)
            payload = request.call_args.args[4]
            self.assertEqual(payload["state"], "closed")
            self.assertEqual(payload["state_reason"], "completed")
            self.assertIn("LLM Owner Digest: Resolved", payload["body"])

    def test_llm_run_approved_handoffs_runs_pending_decision_and_skips_current(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            decision_path = tmp_path / "llm-topic-decision-codes-gsc-opportunity.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            reviewer_fixture_path = tmp_path / "llm-reviewer-response.json"
            write_json(decision_path, fixture_approved_topic_decision())
            write_json(editor_fixture_path, fixture_llm_editor_response())
            write_json(reviewer_fixture_path, fixture_llm_reviewer_response())

            code, summary = llm_run_approved_handoffs.run_approved_handoffs(
                reports_dir=tmp_path,
                output_dir=tmp_path,
                provider="fixture",
                max_handoffs=3,
                include_current=False,
                basename="llm-approved-handoff-run-fixture",
                editor_fixture_path=editor_fixture_path,
                reviewer_fixture_path=reviewer_fixture_path,
            )

            self.assertEqual(code, 0)
            self.assertEqual(summary["state"], "completed")
            self.assertEqual(summary["approved_handoff_count"], 1)
            self.assertEqual(summary["run_count"], 1)
            self.assertEqual(summary["success_count"], 1)
            self.assertTrue((tmp_path / "llm-worker-chain-codes-gsc-opportunity.json").exists())
            self.assertTrue((tmp_path / "llm-approved-handoff-run-fixture.json").exists())

            second_code, second_summary = llm_run_approved_handoffs.run_approved_handoffs(
                reports_dir=tmp_path,
                output_dir=tmp_path / "second-run",
                provider="fixture",
                max_handoffs=3,
                include_current=False,
                basename="llm-approved-handoff-run-fixture",
                editor_fixture_path=editor_fixture_path,
                reviewer_fixture_path=reviewer_fixture_path,
            )

            self.assertEqual(second_code, 0)
            self.assertEqual(second_summary["state"], "current")
            self.assertEqual(second_summary["run_count"], 0)
            self.assertEqual(second_summary["skipped_current_count"], 1)

    def test_llm_auto_review_queue_runs_top_candidate_and_skips_existing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            reviewer_fixture_path = tmp_path / "llm-reviewer-response.json"
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, fixture_llm_editor_response())
            write_json(reviewer_fixture_path, fixture_llm_reviewer_response())

            with patch.object(llm_topic_discovery, "existing_topic_review", return_value=None), patch.object(
                llm_auto_review_queue,
                "REPORTS_DIR",
                tmp_path / "global-reports",
            ):
                code, summary = llm_auto_review_queue.run_auto_review_queue(
                    signal_paths=[signals_path],
                    external_proposal_paths=[],
                    output_dir=tmp_path,
                    basename="llm-auto-review-queue-fixture",
                    provider="fixture",
                    scout_fixture_path=scout_fixture_path,
                    editor_fixture_path=editor_fixture_path,
                    reviewer_fixture_path=reviewer_fixture_path,
                    limit=4,
                    min_impressions=200,
                    max_chains=2,
                    include_existing=False,
                )

            self.assertEqual(code, 0)
            self.assertEqual(summary["state"], "queue_ready")
            self.assertEqual(summary["candidate_topic_count"], 1)
            self.assertEqual(summary["queued_topic_count"], 1)
            self.assertEqual(summary["completed_item_count"], 1)
            self.assertEqual(summary["queue_items"][0]["topic_id"], "codes-gsc-opportunity")
            self.assertTrue((tmp_path / "llm-worker-chain-codes-gsc-opportunity.json").exists())
            self.assertTrue((tmp_path / "llm-auto-review-queue-fixture.json").exists())

            with patch.object(llm_topic_discovery, "existing_topic_review", return_value=None), patch.object(
                llm_auto_review_queue,
                "REPORTS_DIR",
                tmp_path / "global-reports",
            ):
                second_code, second_summary = llm_auto_review_queue.run_auto_review_queue(
                    signal_paths=[signals_path],
                    external_proposal_paths=[],
                    output_dir=tmp_path,
                    basename="llm-auto-review-queue-fixture-2",
                    provider="fixture",
                    scout_fixture_path=scout_fixture_path,
                    editor_fixture_path=editor_fixture_path,
                    reviewer_fixture_path=reviewer_fixture_path,
                    limit=4,
                    min_impressions=200,
                    max_chains=2,
                    include_existing=False,
                )

            self.assertEqual(second_code, 0)
            self.assertEqual(second_summary["state"], "current")
            self.assertEqual(second_summary["queued_topic_count"], 0)
            self.assertEqual(second_summary["skipped_existing_count"], 1)

    def test_llm_auto_review_queue_resolves_recorded_topic_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            discovery_path = tmp_path / "discovery.json"
            decision_path = tmp_path / "llm-topic-decision-fixture-topic.json"
            write_json(signals_path, fixture_signals())
            write_json(
                discovery_path,
                {
                    "topics": [
                        {
                            "topic_id": "fixture-topic",
                            "target_page_or_slug": "gift-center-uid.html",
                            "cluster": "Economy",
                            "priority": "high",
                            "confidence": "high",
                            "risk_level": "medium",
                            "recommended_action": "update_existing",
                            "status": "candidate",
                        }
                    ]
                },
            )
            write_json(
                decision_path,
                {
                    "report_type": "llm_topic_decision",
                    "topic_id": "fixture-topic",
                    "decision_state": "monitor",
                    "decision_note": "Already reviewed by owner.",
                    "allows_worker_chain": False,
                    "allows_content_edit": False,
                    "markdown_path": str(tmp_path / "llm-topic-decision-fixture-topic.md"),
                },
            )
            refresh_payload = {
                "output_path": str(tmp_path / "refresh.json"),
                "markdown_path": str(tmp_path / "refresh.md"),
                "topic_discovery_path": str(discovery_path),
                "topic_discovery_markdown": str(tmp_path / "discovery.md"),
                "stages": [],
            }

            with patch.object(
                llm_candidate_refresh,
                "run_candidate_refresh",
                return_value=(0, refresh_payload),
            ), patch.object(llm_auto_review_queue, "run_queue_item") as run_queue_item:
                code, summary = llm_auto_review_queue.run_auto_review_queue(
                    signal_paths=[signals_path],
                    external_proposal_paths=[],
                    output_dir=tmp_path,
                    basename="llm-auto-review-queue-fixture",
                    provider="fixture",
                    scout_fixture_path=None,
                    editor_fixture_path=None,
                    reviewer_fixture_path=None,
                    limit=4,
                    min_impressions=200,
                    max_chains=1,
                    include_existing=False,
                )

            self.assertEqual(code, 0)
            self.assertEqual(summary["state"], "current")
            self.assertEqual(summary["queued_topic_count"], 0)
            self.assertEqual(summary["skipped_existing_count"], 0)
            self.assertEqual(summary["resolved_by_decision_count"], 1)
            self.assertEqual(summary["resolved_by_decision"][0]["topic_id"], "fixture-topic")
            self.assertEqual(summary["resolved_by_decision"][0]["decision_state"], "monitor")
            self.assertTrue(any("No owner action needed" in action for action in summary["next_actions"]))
            self.assertTrue(any("recorded owner decisions" in action for action in summary["next_actions"]))
            run_queue_item.assert_not_called()

    def test_llm_auto_review_queue_reruns_stale_existing_chain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            reviewer_fixture_path = tmp_path / "llm-reviewer-response.json"
            stale_chain_path = tmp_path / "llm-worker-chain-codes-gsc-opportunity.json"
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, fixture_llm_editor_response())
            write_json(reviewer_fixture_path, fixture_llm_reviewer_response())
            write_json(
                stale_chain_path,
                {
                    "schema_version": 1,
                    "report_type": "llm_worker_chain_summary",
                    "state": "completed",
                    "source_topic_id": "codes-gsc-opportunity",
                    "target_page_or_slug": "codes.html",
                    "errors": [],
                },
            )

            with patch.object(llm_topic_discovery, "existing_topic_review", return_value=None), patch.object(
                llm_auto_review_queue,
                "REPORTS_DIR",
                tmp_path / "global-reports",
            ):
                code, summary = llm_auto_review_queue.run_auto_review_queue(
                    signal_paths=[signals_path],
                    external_proposal_paths=[],
                    output_dir=tmp_path,
                    basename="llm-auto-review-queue-fixture",
                    provider="fixture",
                    scout_fixture_path=scout_fixture_path,
                    editor_fixture_path=editor_fixture_path,
                    reviewer_fixture_path=reviewer_fixture_path,
                    limit=4,
                    min_impressions=200,
                    max_chains=2,
                    include_existing=False,
                )

            refreshed_chain = load_json(stale_chain_path)
            self.assertEqual(code, 0)
            self.assertEqual(summary["state"], "queue_ready")
            self.assertEqual(summary["queued_topic_count"], 1)
            self.assertEqual(summary["skipped_existing_count"], 0)
            self.assertEqual(summary["stale_existing_count"], 1)
            self.assertTrue(summary["queue_items"][0]["stale_existing_chain"])
            self.assertEqual(
                refreshed_chain["worker_chain_contract_version"],
                llm_worker_chain.WORKER_CHAIN_CONTRACT_VERSION,
            )

    def test_llm_auto_review_queue_keeps_success_exit_for_item_failures(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            discovery_path = tmp_path / "discovery.json"
            write_json(signals_path, fixture_signals())
            write_json(
                discovery_path,
                {
                    "topics": [
                        {
                            "topic_id": "fixture-topic",
                            "target_page_or_slug": "gift-center-uid.html",
                            "cluster": "Economy",
                            "priority": "high",
                            "confidence": "medium",
                            "risk_level": "medium",
                            "recommended_action": "update_existing",
                            "status": "candidate",
                        }
                    ]
                },
            )
            refresh_payload = {
                "output_path": str(tmp_path / "refresh.json"),
                "markdown_path": str(tmp_path / "refresh.md"),
                "topic_discovery_path": str(discovery_path),
                "topic_discovery_markdown": str(tmp_path / "discovery.md"),
                "stages": [
                    {
                        "stage": "llm_scout",
                        "request_path": str(tmp_path / "scout-request.json"),
                        "result_path": str(tmp_path / "scout-result.json"),
                        "markdown_path": str(tmp_path / "scout.md"),
                    }
                ],
            }
            failed_item = {
                "topic_id": "fixture-topic",
                "target_page_or_slug": "gift-center-uid.html",
                "cluster": "Economy",
                "priority": "high",
                "risk_level": "medium",
                "status": "failed",
                "chain_json": str(tmp_path / "llm-worker-chain-fixture-topic.json"),
                "chain_markdown": str(tmp_path / "llm-worker-chain-fixture-topic.md"),
                "errors": ["LLM Editor stage failed; Reviewer was not run."],
            }

            with patch.object(
                llm_candidate_refresh,
                "run_candidate_refresh",
                return_value=(0, refresh_payload),
            ), patch.object(llm_auto_review_queue, "run_queue_item", return_value=failed_item):
                code, summary = llm_auto_review_queue.run_auto_review_queue(
                    signal_paths=[signals_path],
                    external_proposal_paths=[],
                    output_dir=tmp_path,
                    basename="llm-auto-review-queue-fixture",
                    provider="fixture",
                    scout_fixture_path=None,
                    editor_fixture_path=None,
                    reviewer_fixture_path=None,
                    limit=4,
                    min_impressions=200,
                    max_chains=1,
                    include_existing=False,
                )

            self.assertEqual(code, 0)
            self.assertEqual(summary["state"], "completed_with_failures")
            self.assertEqual(summary["failed_item_count"], 1)
            self.assertIn("LLM Editor stage failed", summary["errors"][0])

    def test_llm_editor_builds_brief_from_llm_scout_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, fixture_llm_editor_response())

            scout_code, scout_payload = llm_scout.run_llm_scout(
                signal_paths=[signals_path],
                external_proposal_paths=[],
                output_dir=tmp_path,
                basename="llm-scout-fixture",
                provider="fixture",
                fixture_path=scout_fixture_path,
                limit=4,
                min_impressions=200,
            )
            self.assertEqual(scout_code, 0)

            editor_code, editor_payload = llm_editor.run_llm_editor(
                scout_result_path=Path(scout_payload["result_path"]),
                scout_request_path=Path(scout_payload["request_path"]),
                topic_id="codes-gsc-opportunity",
                output_dir=tmp_path,
                basename="llm-editor-fixture",
                provider="fixture",
                fixture_path=editor_fixture_path,
            )
            self.assertEqual(editor_code, 0)
            self.assertEqual(editor_payload["report_type"], "llm_editor_brief")
            self.assertEqual(editor_payload["adapter_result"]["state"], "completed")
            self.assertEqual(editor_payload["target_page_or_slug"], "codes.html")
            self.assertEqual(editor_payload["adapter_result"]["response_json"]["page_role"], "cornerstone-guide")
            self.assertTrue((tmp_path / "llm-editor-fixture-request.json").exists())
            self.assertTrue((tmp_path / "llm-editor-fixture-result.json").exists())
            self.assertTrue((tmp_path / "llm-editor-fixture.md").exists())

    def test_llm_reviewer_gates_llm_editor_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            reviewer_fixture_path = tmp_path / "llm-reviewer-response.json"
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, fixture_llm_editor_response())
            write_json(reviewer_fixture_path, fixture_llm_reviewer_response())

            scout_code, scout_payload = llm_scout.run_llm_scout(
                signal_paths=[signals_path],
                external_proposal_paths=[],
                output_dir=tmp_path,
                basename="llm-scout-fixture",
                provider="fixture",
                fixture_path=scout_fixture_path,
                limit=4,
                min_impressions=200,
            )
            self.assertEqual(scout_code, 0)
            editor_code, editor_payload = llm_editor.run_llm_editor(
                scout_result_path=Path(scout_payload["result_path"]),
                scout_request_path=Path(scout_payload["request_path"]),
                topic_id="codes-gsc-opportunity",
                output_dir=tmp_path,
                basename="llm-editor-fixture",
                provider="fixture",
                fixture_path=editor_fixture_path,
            )
            self.assertEqual(editor_code, 0)

            reviewer_code, reviewer_payload = llm_reviewer.run_llm_reviewer(
                editor_result_path=Path(editor_payload["result_path"]),
                editor_request_path=Path(editor_payload["request_path"]),
                output_dir=tmp_path,
                basename="llm-reviewer-fixture",
                provider="fixture",
                fixture_path=reviewer_fixture_path,
            )
            self.assertEqual(reviewer_code, 0)
            self.assertEqual(reviewer_payload["report_type"], "llm_reviewer_gate")
            self.assertEqual(reviewer_payload["adapter_result"]["state"], "completed")
            self.assertEqual(reviewer_payload["adapter_result"]["response_json"]["verdict"], "needs_human_review")
            self.assertEqual(reviewer_payload["target_page_or_slug"], "codes.html")
            self.assertTrue((tmp_path / "llm-reviewer-fixture-request.json").exists())
            self.assertTrue((tmp_path / "llm-reviewer-fixture-result.json").exists())
            self.assertTrue((tmp_path / "llm-reviewer-fixture.md").exists())

    def test_llm_editor_drops_unapproved_exact_replacement_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            editor_response = fixture_llm_editor_response()
            editor_response["response_json"]["exact_replacements"] = [
                {
                    "file": "codes.html",
                    "change_type": "first_screen_update",
                    "selector_or_anchor": ".guide-verified",
                    "exact_old": fixture_codes_guide_verified_snippet(),
                    "exact_new": "<p>Draft replacement copy.</p>",
                    "reason": "Test proposal-only exact replacement.",
                    "owner_approval_required": False,
                }
            ]
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, editor_response)

            scout_code, scout_payload = llm_scout.run_llm_scout(
                signal_paths=[signals_path],
                external_proposal_paths=[],
                output_dir=tmp_path,
                basename="llm-scout-fixture",
                provider="fixture",
                fixture_path=scout_fixture_path,
                limit=4,
                min_impressions=200,
            )
            self.assertEqual(scout_code, 0)

            editor_code, editor_payload = llm_editor.run_llm_editor(
                scout_result_path=Path(scout_payload["result_path"]),
                scout_request_path=Path(scout_payload["request_path"]),
                topic_id="codes-gsc-opportunity",
                output_dir=tmp_path,
                basename="llm-editor-fixture",
                provider="fixture",
                fixture_path=editor_fixture_path,
            )
            self.assertEqual(editor_code, 0)
            self.assertEqual(editor_payload["adapter_result"]["state"], "completed")
            self.assertEqual(editor_payload["adapter_result"]["response_json"]["exact_replacements"], [])
            self.assertTrue(
                any("owner_approval_required" in warning for warning in editor_payload["adapter_result"].get("warnings", []))
            )

    def test_llm_editor_rejects_nonliteral_exact_old_candidate(self) -> None:
        response = {
            "exact_replacements": [
                {
                    "file": "codes.html",
                    "change_type": "first_screen_update",
                    "selector_or_anchor": ".guide-verified",
                    "exact_old": "<p>This text is not in the current target file.</p>",
                    "exact_new": "<p>Draft replacement copy.</p>",
                    "reason": "Test nonliteral exact replacement.",
                    "owner_approval_required": True,
                }
            ]
        }

        errors = llm_editor.validate_exact_replacements(response, "codes.html")

        self.assertTrue(any("exactly once" in error for error in errors))

    def test_llm_editor_drops_noop_exact_replacements_without_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            noop_snippet = fixture_codes_guide_verified_snippet()
            editor_response = fixture_llm_editor_response()
            editor_response["response_json"]["exact_replacements"] = [
                {
                    "file": "codes.html",
                    "change_type": "first_screen_update",
                    "selector_or_anchor": ".guide-verified",
                    "exact_old": noop_snippet,
                    "exact_new": noop_snippet,
                    "reason": "No-op exact replacement should be dropped, not block the planning brief.",
                    "owner_approval_required": True,
                }
            ]
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, editor_response)

            scout_code, scout_payload = llm_scout.run_llm_scout(
                signal_paths=[signals_path],
                external_proposal_paths=[],
                output_dir=tmp_path,
                basename="llm-scout-fixture",
                provider="fixture",
                fixture_path=scout_fixture_path,
                limit=4,
                min_impressions=200,
            )
            self.assertEqual(scout_code, 0)

            editor_code, editor_payload = llm_editor.run_llm_editor(
                scout_result_path=Path(scout_payload["result_path"]),
                scout_request_path=Path(scout_payload["request_path"]),
                topic_id="codes-gsc-opportunity",
                output_dir=tmp_path,
                basename="llm-editor-fixture",
                provider="fixture",
                fixture_path=editor_fixture_path,
            )

            self.assertEqual(editor_code, 0)
            self.assertEqual(editor_payload["adapter_result"]["state"], "completed")
            self.assertEqual(editor_payload["adapter_result"]["response_json"]["exact_replacements"], [])
            self.assertTrue(
                any("Dropped no-op" in warning for warning in editor_payload["adapter_result"].get("warnings", []))
            )

    def test_llm_editor_drops_non_ascii_exact_replacements_without_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            editor_response = fixture_llm_editor_response()
            editor_response["response_json"]["exact_replacements"] = [
                {
                    "file": "codes.html",
                    "change_type": "first_screen_update",
                    "selector_or_anchor": ".guide-verified",
                    "exact_old": fixture_codes_guide_verified_snippet(),
                    "exact_new": "<p>Draft replacement with an unsafe arrow →.</p>",
                    "reason": "Non-ASCII exact replacement should be dropped, not block the planning brief.",
                    "owner_approval_required": True,
                }
            ]
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, editor_response)

            scout_code, scout_payload = llm_scout.run_llm_scout(
                signal_paths=[signals_path],
                external_proposal_paths=[],
                output_dir=tmp_path,
                basename="llm-scout-fixture",
                provider="fixture",
                fixture_path=scout_fixture_path,
                limit=4,
                min_impressions=200,
            )
            self.assertEqual(scout_code, 0)

            editor_code, editor_payload = llm_editor.run_llm_editor(
                scout_result_path=Path(scout_payload["result_path"]),
                scout_request_path=Path(scout_payload["request_path"]),
                topic_id="codes-gsc-opportunity",
                output_dir=tmp_path,
                basename="llm-editor-fixture",
                provider="fixture",
                fixture_path=editor_fixture_path,
            )

            self.assertEqual(editor_code, 0)
            self.assertEqual(editor_payload["adapter_result"]["state"], "completed")
            self.assertEqual(editor_payload["adapter_result"]["response_json"]["exact_replacements"], [])
            self.assertTrue(
                any("plain ASCII English" in warning for warning in editor_payload["adapter_result"].get("warnings", []))
            )

    def test_llm_exact_replacements_reach_intake_as_proposal_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            reviewer_fixture_path = tmp_path / "llm-reviewer-response.json"
            editor_response = fixture_llm_editor_response()
            editor_response["response_json"]["exact_replacements"] = [
                {
                    "file": "codes.html",
                    "change_type": "first_screen_update",
                    "selector_or_anchor": ".guide-verified",
                    "exact_old": fixture_codes_guide_verified_snippet(),
                    "exact_new": "<p>Draft replacement copy.</p>",
                    "reason": "Test proposal-only exact replacement.",
                    "owner_approval_required": True,
                }
            ]
            reviewer_response = fixture_llm_reviewer_response()
            reviewer_response["response_json"]["exact_replacement_review"] = (
                "One narrow target-only candidate is present and still requires proposal and owner approval."
            )
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, editor_response)
            write_json(reviewer_fixture_path, reviewer_response)

            code, summary = llm_worker_chain.run_llm_worker_chain(
                signal_paths=[signals_path],
                output_dir=tmp_path,
                provider="fixture",
                topic_id="codes-gsc-opportunity",
                basename="llm-worker-chain-fixture",
                scout_basename="llm-worker-chain-scout-fixture",
                editor_basename="llm-worker-chain-editor-fixture",
                reviewer_basename="llm-worker-chain-reviewer-fixture",
                scout_fixture_path=scout_fixture_path,
                editor_fixture_path=editor_fixture_path,
                reviewer_fixture_path=reviewer_fixture_path,
                limit=4,
                min_impressions=200,
            )
            self.assertEqual(code, 0)
            self.assertEqual(summary["exact_replacements_count"], 1)
            chain_path = Path(summary["artifacts"]["chain_json"])
            review = llm_review_latest.build_review(chain_path)
            self.assertEqual(review["exact_replacements_count"], 1)

            approved_intake = llm_intake.build_intake(chain_path, approved_by="fixture", note="contract test")
            self.assertEqual(approved_intake["state"], "approved_for_intake")
            self.assertFalse(approved_intake["content_edit_approved"])
            self.assertEqual(approved_intake["exact_replacements_count"], 1)
            run_plan = intake_to_run.build_proposal(approved_intake, tmp_path / "llm-intake.json")
            self.assertEqual(len(run_plan["proposed_manifest"]["plan"]["exact_replacements"]), 1)

    def test_llm_worker_chain_runs_fixture_stages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            reviewer_fixture_path = tmp_path / "llm-reviewer-response.json"
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, fixture_llm_editor_response())
            write_json(reviewer_fixture_path, fixture_llm_reviewer_response())

            code, summary = llm_worker_chain.run_llm_worker_chain(
                signal_paths=[signals_path],
                output_dir=tmp_path,
                provider="fixture",
                topic_id="codes-gsc-opportunity",
                basename="llm-worker-chain-fixture",
                scout_basename="llm-worker-chain-scout-fixture",
                editor_basename="llm-worker-chain-editor-fixture",
                reviewer_basename="llm-worker-chain-reviewer-fixture",
                scout_fixture_path=scout_fixture_path,
                editor_fixture_path=editor_fixture_path,
                reviewer_fixture_path=reviewer_fixture_path,
                limit=4,
                min_impressions=200,
            )
            self.assertEqual(code, 0)
            self.assertEqual(summary["report_type"], "llm_worker_chain_summary")
            self.assertEqual(summary["state"], "completed")
            self.assertEqual(summary["source_topic_id"], "codes-gsc-opportunity")
            self.assertEqual(summary["target_page_or_slug"], "codes.html")
            self.assertEqual(summary["review_verdict"], "needs_human_review")
            self.assertEqual(summary["stages"]["llm_scout"]["state"], "completed")
            self.assertEqual(summary["stages"]["llm_editor"]["state"], "completed")
            self.assertEqual(summary["stages"]["llm_reviewer"]["state"], "completed")
            self.assertTrue((tmp_path / "llm-worker-chain-fixture.json").exists())
            self.assertTrue((tmp_path / "llm-worker-chain-fixture.md").exists())

    def test_llm_worker_chain_replays_approved_topic_decision_without_scout_rerank(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            decision_path = tmp_path / "llm-topic-decision-codes-gsc-opportunity.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            reviewer_fixture_path = tmp_path / "llm-reviewer-response.json"
            write_json(decision_path, fixture_approved_topic_decision())
            write_json(editor_fixture_path, fixture_llm_editor_response())
            write_json(reviewer_fixture_path, fixture_llm_reviewer_response())

            code, summary = llm_worker_chain.run_llm_worker_chain(
                signal_paths=[],
                output_dir=tmp_path,
                provider="fixture",
                topic_id=None,
                basename="llm-worker-chain-fixture",
                scout_basename="llm-worker-chain-scout-fixture",
                editor_basename="llm-worker-chain-editor-fixture",
                reviewer_basename="llm-worker-chain-reviewer-fixture",
                scout_fixture_path=None,
                editor_fixture_path=editor_fixture_path,
                reviewer_fixture_path=reviewer_fixture_path,
                limit=4,
                min_impressions=200,
                decision_path=decision_path,
            )

            self.assertEqual(code, 0)
            self.assertEqual(summary["state"], "completed")
            self.assertEqual(summary["handoff_source"], "topic_decision")
            self.assertEqual(summary["source_topic_id"], "codes-gsc-opportunity")
            self.assertEqual(summary["stages"]["llm_scout"]["provider"], "decision_replay")
            self.assertEqual(summary["stages"]["llm_editor"]["state"], "completed")
            self.assertEqual(summary["stages"]["llm_reviewer"]["state"], "completed")
            self.assertTrue((tmp_path / "llm-worker-chain-scout-fixture-request.json").exists())
            self.assertTrue((tmp_path / "llm-worker-chain-scout-fixture-result.json").exists())
            self.assertTrue((tmp_path / "llm-worker-chain-fixture.json").exists())

    def test_llm_worker_chain_blocks_monitor_topic_decision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            decision_path = tmp_path / "llm-topic-decision-codes-gsc-opportunity.json"
            decision = fixture_approved_topic_decision()
            decision["decision_state"] = "monitor"
            decision["allows_worker_chain"] = False
            write_json(decision_path, decision)

            code, summary = llm_worker_chain.run_llm_worker_chain(
                signal_paths=[],
                output_dir=tmp_path,
                provider="fixture",
                topic_id=None,
                basename="llm-worker-chain-fixture",
                scout_basename="llm-worker-chain-scout-fixture",
                editor_basename=None,
                reviewer_basename=None,
                scout_fixture_path=None,
                editor_fixture_path=None,
                reviewer_fixture_path=None,
                limit=4,
                min_impressions=200,
                decision_path=decision_path,
            )

            self.assertEqual(code, 1)
            self.assertEqual(summary["state"], "blocked")
            self.assertEqual(summary["handoff_source"], "topic_decision")
            self.assertEqual(summary["stages"]["llm_scout"]["state"], "not_run")
            self.assertTrue(any("not approved_for_chain" in error for error in summary["errors"]))
            self.assertTrue((tmp_path / "llm-worker-chain-fixture.json").exists())

    def test_llm_worker_chain_blocks_when_requested_topic_is_not_selected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            reviewer_fixture_path = tmp_path / "llm-reviewer-response.json"
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, fixture_llm_editor_response())
            write_json(reviewer_fixture_path, fixture_llm_reviewer_response())

            code, summary = llm_worker_chain.run_llm_worker_chain(
                signal_paths=[signals_path],
                output_dir=tmp_path,
                provider="fixture",
                topic_id="heroes-gsc-opportunity",
                basename="llm-worker-chain-fixture",
                scout_basename="llm-worker-chain-scout-fixture",
                editor_basename="llm-worker-chain-editor-fixture",
                reviewer_basename="llm-worker-chain-reviewer-fixture",
                scout_fixture_path=scout_fixture_path,
                editor_fixture_path=editor_fixture_path,
                reviewer_fixture_path=reviewer_fixture_path,
                limit=4,
                min_impressions=200,
            )

            self.assertEqual(code, 1)
            self.assertEqual(summary["state"], "blocked")
            self.assertEqual(summary["source_topic_id"], "heroes-gsc-opportunity")
            self.assertEqual(summary["stages"]["llm_scout"]["state"], "completed")
            self.assertEqual(summary["stages"]["llm_editor"]["state"], "not_run")
            self.assertTrue(any("was not selected by LLM Scout" in error for error in summary["errors"]))
            self.assertTrue((tmp_path / "llm-worker-chain-fixture.json").exists())
            self.assertTrue((tmp_path / "llm-worker-chain-fixture.md").exists())

    def test_llm_worker_chain_blocks_low_priority_selected_topic_before_editor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            reviewer_fixture_path = tmp_path / "llm-reviewer-response.json"
            scout_response = fixture_llm_scout_response()
            scout_response["response_json"]["selected_opportunities"][0]["priority"] = "low"
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, scout_response)
            write_json(editor_fixture_path, fixture_llm_editor_response())
            write_json(reviewer_fixture_path, fixture_llm_reviewer_response())

            code, summary = llm_worker_chain.run_llm_worker_chain(
                signal_paths=[signals_path],
                output_dir=tmp_path,
                provider="fixture",
                topic_id=None,
                basename="llm-worker-chain-fixture",
                scout_basename="llm-worker-chain-scout-fixture",
                editor_basename="llm-worker-chain-editor-fixture",
                reviewer_basename="llm-worker-chain-reviewer-fixture",
                scout_fixture_path=scout_fixture_path,
                editor_fixture_path=editor_fixture_path,
                reviewer_fixture_path=reviewer_fixture_path,
                limit=4,
                min_impressions=200,
            )

            self.assertEqual(code, 1)
            self.assertEqual(summary["state"], "blocked")
            self.assertEqual(summary["stages"]["llm_scout"]["state"], "completed")
            self.assertEqual(summary["stages"]["llm_editor"]["state"], "not_run")
            self.assertTrue(any("no ready-for-chain opportunities" in error for error in summary["errors"]))

    def test_llm_review_latest_reads_chain_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            reviewer_fixture_path = tmp_path / "llm-reviewer-response.json"
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, fixture_llm_editor_response())
            write_json(reviewer_fixture_path, fixture_llm_reviewer_response())
            code, summary = llm_worker_chain.run_llm_worker_chain(
                signal_paths=[signals_path],
                output_dir=tmp_path,
                provider="fixture",
                topic_id="codes-gsc-opportunity",
                basename="llm-worker-chain-fixture",
                scout_basename="llm-worker-chain-scout-fixture",
                editor_basename="llm-worker-chain-editor-fixture",
                reviewer_basename="llm-worker-chain-reviewer-fixture",
                scout_fixture_path=scout_fixture_path,
                editor_fixture_path=editor_fixture_path,
                reviewer_fixture_path=reviewer_fixture_path,
                limit=4,
                min_impressions=200,
            )
            self.assertEqual(code, 0)
            chain_path = Path(summary["artifacts"]["chain_json"])
            review = llm_review_latest.build_review(chain_path)
            self.assertEqual(review["report_type"], "llm_latest_owner_review")
            self.assertEqual(review["source_topic_id"], "codes-gsc-opportunity")
            self.assertEqual(review["target_page_or_slug"], "codes.html")
            self.assertEqual(review["review_verdict"], "needs_human_review")
            self.assertEqual(review["recommended_operator_action"], "owner_review_required")
            markdown = llm_review_latest.render_markdown(review)
            self.assertIn("LLM Latest Owner Review", markdown)

    def test_llm_intake_latest_bridges_to_run_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            reviewer_fixture_path = tmp_path / "llm-reviewer-response.json"
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, fixture_llm_editor_response())
            write_json(reviewer_fixture_path, fixture_llm_reviewer_response())
            code, summary = llm_worker_chain.run_llm_worker_chain(
                signal_paths=[signals_path],
                output_dir=tmp_path,
                provider="fixture",
                topic_id="codes-gsc-opportunity",
                basename="llm-worker-chain-fixture",
                scout_basename="llm-worker-chain-scout-fixture",
                editor_basename="llm-worker-chain-editor-fixture",
                reviewer_basename="llm-worker-chain-reviewer-fixture",
                scout_fixture_path=scout_fixture_path,
                editor_fixture_path=editor_fixture_path,
                reviewer_fixture_path=reviewer_fixture_path,
                limit=4,
                min_impressions=200,
            )
            self.assertEqual(code, 0)
            chain_path = Path(summary["artifacts"]["chain_json"])

            pending_intake = llm_intake.build_intake(chain_path, approved_by=None, note=None)
            self.assertEqual(pending_intake["report_type"], "llm_worker_proposal_intake")
            self.assertEqual(pending_intake["state"], "approval_required")
            self.assertEqual(pending_intake["approval_scope"], "none")
            self.assertFalse(pending_intake["content_edit_approved"])
            self.assertFalse(pending_intake["public_content_change_allowed"])
            self.assertEqual(pending_intake["proposed_backlog_item"]["cluster"], "Economy")
            self.assertEqual(pending_intake["proposed_backlog_item"]["recommended_action"], "update_existing")

            incomplete_approval = llm_intake.build_intake(chain_path, approved_by="fixture", note=None)
            self.assertEqual(incomplete_approval["state"], "approval_required")
            self.assertIn(
                "Approval note is required when the LLM Reviewer left owner questions.",
                incomplete_approval["warnings"],
            )

            approved_intake = llm_intake.build_intake(chain_path, approved_by="fixture", note="contract test")
            self.assertEqual(approved_intake["state"], "approved_for_intake")
            self.assertEqual(approved_intake["approved_by"], "fixture")
            self.assertEqual(approved_intake["approval_scope"], "intake_only_no_content_edits")
            self.assertFalse(approved_intake["content_edit_approved"])
            self.assertFalse(approved_intake["public_content_change_allowed"])
            self.assertTrue(approved_intake["requires_owner_answers"])
            self.assertTrue(approved_intake["owner_answers_recorded"])
            self.assertTrue(any("Approval is intake-only" in item for item in approved_intake["approval_guardrails"]))
            run_plan = intake_to_run.build_proposal(approved_intake, tmp_path / "llm-intake.json")
            self.assertEqual(run_plan["state"], "run_plan_ready")
            self.assertEqual(run_plan["proposed_manifest"]["status"], "planned")
            self.assertEqual(run_plan["proposed_manifest"]["changed_files"], [])

    def test_llm_intake_blocks_reviewer_blocking_issues(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            scout_fixture_path = tmp_path / "llm-scout-response.json"
            editor_fixture_path = tmp_path / "llm-editor-response.json"
            reviewer_fixture_path = tmp_path / "llm-reviewer-response.json"
            reviewer_response = fixture_llm_reviewer_response()
            reviewer_response["response_json"]["blocking_issues"] = [
                {
                    "severity": "high",
                    "issue": "The plan needs source verification before intake.",
                    "required_fix": "Resolve the source gap before owner intake approval.",
                }
            ]
            write_json(signals_path, fixture_signals())
            write_json(scout_fixture_path, fixture_llm_scout_response())
            write_json(editor_fixture_path, fixture_llm_editor_response())
            write_json(reviewer_fixture_path, reviewer_response)
            code, summary = llm_worker_chain.run_llm_worker_chain(
                signal_paths=[signals_path],
                output_dir=tmp_path,
                provider="fixture",
                topic_id="codes-gsc-opportunity",
                basename="llm-worker-chain-fixture",
                scout_basename="llm-worker-chain-scout-fixture",
                editor_basename="llm-worker-chain-editor-fixture",
                reviewer_basename="llm-worker-chain-reviewer-fixture",
                scout_fixture_path=scout_fixture_path,
                editor_fixture_path=editor_fixture_path,
                reviewer_fixture_path=reviewer_fixture_path,
                limit=4,
                min_impressions=200,
            )
            self.assertEqual(code, 0)
            chain_path = Path(summary["artifacts"]["chain_json"])

            approved_intake = llm_intake.build_intake(chain_path, approved_by="fixture", note="contract test")
            self.assertEqual(approved_intake["state"], "blocked")
            self.assertIn("LLM Reviewer returned blocking issues; resolve them before LLM intake.", approved_intake["blockers"])

            resolved_intake = llm_intake.build_intake(
                chain_path,
                approved_by="fixture",
                note="Owner resolved source verification for intake only.",
                resolve_reviewer_blockers=True,
            )
            self.assertEqual(resolved_intake["state"], "approved_for_intake")
            self.assertTrue(resolved_intake["reviewer_blockers_resolved_by_owner"])
            self.assertFalse(resolved_intake["content_edit_approved"])
            self.assertTrue(any("owner-resolved for intake only" in item for item in resolved_intake["warnings"]))

    def test_scout_editor_reviewer_contract_shapes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            write_json(signals_path, fixture_signals())

            scout_payload = scout.build_payload(signals_path, limit=4, min_impressions=200)
            self.assertEqual(scout_payload["report_type"], "scout_topic_proposals")
            self.assertGreaterEqual(scout_payload["proposal_count"], 1)

            proposal = scout_payload["proposals"][0]
            self.assertEqual(proposal["topic_id"], "codes-gsc-opportunity")
            self.assertEqual(proposal["target_page_or_slug"], "codes.html")
            self.assertEqual(proposal["recommended_action"], "update_existing")
            self.assertIn("site_fit", proposal)
            self.assertIn("expected_internal_route", proposal["site_fit"])

            scout_json, _ = scout.write_outputs(scout_payload, tmp_path, "scout-topic-proposals")
            brief = editor.build_editor_brief(proposal, scout_json)
            self.assertEqual(brief["report_type"], "editor_brief")
            self.assertEqual(brief["source_topic_id"], "codes-gsc-opportunity")
            self.assertEqual(brief["target_page_or_slug"], "codes.html")
            self.assertEqual(brief["template_reference"], "codes.html")
            self.assertIn("AGENTS.md", brief["required_context_before_patch"])
            self.assertIn("python3 scripts/prepublish_check.py", brief["acceptance_checks"])
            snippets = brief["current_page_snapshot"]["source_snippets"]
            self.assertIn("guide_verified", snippets)
            self.assertIn('class="guide-verified"', snippets["guide_verified"])
            self.assertIn("title_tag", snippets)
            self.assertTrue(snippets["title_tag"].startswith("<title>"))

            index_context = editor.html_context("index.html")
            index_snippets = index_context["source_snippets"]
            self.assertIn("home_hero_block", index_snippets)
            self.assertIn('<header class="hero">', index_snippets["home_hero_block"])
            self.assertIn("home_featured_header", index_snippets)

            editor_json, _ = editor.write_outputs(brief, tmp_path, None)
            review = reviewer.build_review(brief, proposal, editor_json, scout_json)
            self.assertEqual(review["report_type"], "worker_review")
            self.assertEqual(review["target_page_or_slug"], "codes.html")
            self.assertIn(review["verdict"], {"pass", "needs_human_review", "revise", "reject"})
            self.assertIn("python3 automation/pipeline.py checks --strict", review["required_checks"])
            self.assertTrue(review["human_approval_required"])

    def test_scout_accepts_bing_agent_signal_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            signals_path = Path(tmp) / "bing-signals.json"
            write_json(signals_path, fixture_bing_signals())

            scout_payload = scout.build_payload(signals_path, limit=4, min_impressions=200)
            self.assertEqual(scout_payload["report_type"], "scout_topic_proposals")
            self.assertGreaterEqual(scout_payload["proposal_count"], 1)
            proposal = scout_payload["proposals"][0]
            self.assertEqual(proposal["topic_id"], "codes-bing-opportunity")
            self.assertIn("Bing opportunity review", proposal["title"])
            self.assertIn("Bing weekly", proposal["source_reference"])
            self.assertTrue(any("Treat Bing data as a signal" in item for item in proposal["constraints"]))

    def test_bing_date_and_local_page_helpers(self) -> None:
        self.assertEqual(bing_weekly.parse_bing_date("/Date(1316156400000-0700)/"), "2011-09-16")
        self.assertEqual(bing_weekly.local_page_path("https://lastzguides.com/resources.html"), "resources.html")
        self.assertEqual(bing_weekly.local_page_path("https://lastzguides.com/"), "index.html")

    def test_bing_insights_use_separate_page_ctr_baseline(self) -> None:
        queries = [
            {"query": "last z", "impressions": 300, "clicks": 1, "ctr": 0.003, "position": 7},
            {"query": "last z guide", "impressions": 100, "clicks": 30, "ctr": 0.3, "position": 4},
        ]
        pages = [
            {"page": "https://lastzguides.com/", "impressions": 900, "clicks": 18, "ctr": 0.02, "position": 6},
            {"page": "https://lastzguides.com/hq.html", "impressions": 300, "clicks": 30, "ctr": 0.1, "position": 4},
            {"page": "https://lastzguides.com/research.html", "impressions": 200, "clicks": 30, "ctr": 0.15, "position": 3},
        ]

        insights = bing_weekly.pick_insights(queries, pages)
        self.assertAlmostEqual(insights["query_ctr_median"], 0.1515)
        self.assertAlmostEqual(insights["page_ctr_median"], 0.1)
        self.assertEqual(insights["page_underperform"][0]["page"], "https://lastzguides.com/")

    def test_bing_query_page_rows_keep_undated_page_query_details(self) -> None:
        rows = bing_weekly.query_page_rows(
            {
                "https://lastzguides.com/hq.html": [
                    {"query": "last z hq", "date": "", "impressions": 42, "clicks": 4, "ctr": 0.095, "position": 3},
                    {
                        "query": "old hq",
                        "date": "2026-04-24",
                        "impressions": 100,
                        "clicks": 1,
                        "ctr": 0.01,
                        "position": 11,
                    },
                ]
            },
            "2026-05-01",
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["query"], "last z hq")
        self.assertEqual(rows[0]["date_scope"], "page_query_detail_no_date")

    def test_run_chain_writes_only_requested_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            signals_path = tmp_path / "signals.json"
            write_json(signals_path, fixture_signals())

            args = argparse.Namespace(
                topic_id="codes-gsc-opportunity",
                target=None,
                signals=str(signals_path),
                output_dir=str(tmp_path),
                limit=4,
                min_impressions=200,
                scout_basename="scout-topic-proposals",
                editor_basename=None,
                reviewer_basename=None,
                basename=None,
            )
            summary = run_chain.run_chain(args)
            self.assertEqual(summary["report_type"], "worker_chain_summary")
            self.assertEqual(summary["source_topic_id"], "codes-gsc-opportunity")
            self.assertEqual(summary["target_page_or_slug"], "codes.html")

            for artifact_path in summary["artifacts"].values():
                self.assertTrue((ROOT / artifact_path if not Path(artifact_path).is_absolute() else Path(artifact_path)).exists())

            self.assertFalse((tmp_path / "automation" / "manifests").exists())

    def test_intake_run_plan_and_manifest_writer_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            chain = {
                "schema_version": 1,
                "report_type": "worker_chain_summary",
                "source_topic_id": "codes-gsc-opportunity",
                "target_page_or_slug": "codes.html",
                "cluster": "Economy",
                "recommended_action": "update_existing",
                "page_role": "cornerstone-guide",
                "review_verdict": "needs_human_review",
                "risk_level": "high",
                "approved_next_stage": "patch_plan",
                "human_approval_required": True,
                "blocking_issue_count": 0,
                "artifacts": {},
            }
            chain_path = tmp_path / "worker-chain-codes-gsc-opportunity.json"
            write_json(chain_path, chain)

            pending_intake = intake.build_intake(chain, chain_path, approved_by=None, note=None)
            self.assertEqual(pending_intake["state"], "approval_required")
            blocked_plan = intake_to_run.build_proposal(pending_intake, tmp_path / "worker-intake.json")
            self.assertEqual(blocked_plan["state"], "blocked")
            self.assertIsNone(blocked_plan["proposed_manifest"])

            approved_intake = intake.build_intake(chain, chain_path, approved_by="fixture", note="contract test")
            self.assertEqual(approved_intake["state"], "approved_for_intake")
            run_plan = intake_to_run.build_proposal(approved_intake, tmp_path / "worker-intake.json")
            self.assertEqual(run_plan["state"], "run_plan_ready")
            self.assertEqual(run_plan["proposed_manifest"]["status"], "planned")
            self.assertEqual(run_plan["proposed_manifest"]["changed_files"], [])

            run_plan_path = tmp_path / "worker-run-plan.json"
            write_json(run_plan_path, run_plan)
            manifest_dir = tmp_path / "manifests"

            code, dry_summary = write_manifest.write_manifest(run_plan_path, manifest_dir, "fixture", dry_run=True)
            self.assertEqual(code, 0)
            self.assertEqual(dry_summary["state"], "dry_run_ready")
            self.assertFalse(manifest_dir.exists())

            code, created_summary = write_manifest.write_manifest(run_plan_path, manifest_dir, "fixture", dry_run=False)
            self.assertEqual(code, 0)
            self.assertEqual(created_summary["state"], "manifest_created")
            manifest_path = Path(created_summary["manifest_path"])
            self.assertTrue(manifest_path.exists())
            manifest = load_json(manifest_path)
            self.assertEqual(manifest["status"], "planned")
            self.assertEqual(manifest["changed_files"], [])
            self.assertIn("worker_manifest_writer", manifest["artifacts"])

            code, duplicate_summary = write_manifest.write_manifest(run_plan_path, manifest_dir, "fixture", dry_run=False)
            self.assertEqual(code, 1)
            self.assertEqual(duplicate_summary["state"], "blocked")

    def test_close_run_allows_rejected_no_content_change_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            manifest_path = tmp_path / "rejected-run.json"
            write_json(
                manifest_path,
                {
                    "run_id": "rejected-run",
                    "created_at": "2026-05-05T00:00:00Z",
                    "run_type": "update_existing",
                    "status": "rejected",
                    "risk_level": "high",
                    "summary": "Proposal reviewed; no content change needed.",
                    "inputs": {},
                    "plan": {},
                    "artifacts": {
                        "proposal": {
                            "report_path": "automation/reports/rejected-run.proposed.md",
                        }
                    },
                    "changed_files": ["codes.html"],
                    "checks": {},
                },
            )

            with patch.object(close_run, "REPORTS_DIR", tmp_path / "reports"):
                report_path = close_run.close_run(manifest_path, "No content change needed.")

            manifest = load_json(manifest_path)
            self.assertEqual(manifest["status"], "closed")
            self.assertTrue(manifest["artifacts"]["closeout"]["report_path"].endswith("reports/rejected-run.closed.md"))
            report = report_path.read_text(encoding="utf-8")
            self.assertIn("Closeout type: `rejected_no_content_change`", report)
            self.assertIn("No site files were edited by this run.", report)


if __name__ == "__main__":
    unittest.main()
