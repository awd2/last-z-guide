#!/usr/bin/env python3
"""Deterministic contract tests for the Worker chain."""

from __future__ import annotations

import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from automation.io import load_json, write_json
from automation.reports import llm_approved_handoffs, llm_review_latest, llm_topic_decisions
from automation import close_run
from automation.workers import editor, intake, intake_to_run, llm_adapter, llm_editor, llm_intake, llm_reviewer, llm_scout, llm_topic_decision, llm_topic_discovery, llm_worker_chain, reviewer, run_chain, scout, write_manifest
from scripts import bing_weekly


ROOT = Path(__file__).resolve().parents[2]


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
            self.assertEqual(pending_intake["proposed_backlog_item"]["cluster"], "Economy")
            self.assertEqual(pending_intake["proposed_backlog_item"]["recommended_action"], "update_existing")

            approved_intake = llm_intake.build_intake(chain_path, approved_by="fixture", note="contract test")
            self.assertEqual(approved_intake["state"], "approved_for_intake")
            self.assertEqual(approved_intake["approved_by"], "fixture")
            run_plan = intake_to_run.build_proposal(approved_intake, tmp_path / "llm-intake.json")
            self.assertEqual(run_plan["state"], "run_plan_ready")
            self.assertEqual(run_plan["proposed_manifest"]["status"], "planned")
            self.assertEqual(run_plan["proposed_manifest"]["changed_files"], [])

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
