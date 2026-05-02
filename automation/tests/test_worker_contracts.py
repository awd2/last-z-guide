#!/usr/bin/env python3
"""Deterministic contract tests for the Worker chain."""

from __future__ import annotations

import argparse
import json
import tempfile
import unittest
from pathlib import Path

from automation.io import load_json, write_json
from automation.workers import editor, intake, intake_to_run, llm_adapter, reviewer, run_chain, scout, write_manifest


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


if __name__ == "__main__":
    unittest.main()
