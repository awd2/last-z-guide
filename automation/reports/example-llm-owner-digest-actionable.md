# LLM Owner Digest - Fixture

## Summary

- State: `owner_review_needed`
- Recommended next action: Review the listed topics and approve only if the player value and claims are valid.
- Queue: `automation/reports/llm-auto-review-queue/llm-auto-review-queue.json`
- Candidate topics: `2`
- Needs owner review: `2`
- Ready for intake: `1`
- Blocked or failed: `0`
- Resolved by decision: `0`
- Safety: fixture only; no content, backlog, manifest, PR, or production files were modified.

## Needs Owner Review

- `fixture-codes-first-screen-review`: target `codes.html`, priority `high`, risk `medium`, action `approve_for_intake_if_player_value_and_claims_are_valid`
  - Chain: `automation/reports/llm-worker-chain-fixture-codes-first-screen-review.md`
  - Intake command:
    ```bash
    python3 automation/pipeline.py llm-intake-latest --chain automation/reports/llm-worker-chain-fixture-codes-first-screen-review.json --approved-by OWNER_NAME --note "Approved owner scope for fixture-codes-first-screen-review: validate Gift Center route clarity only" --resolve-reviewer-blockers --json
    ```
- `fixture-research-cross-check`: target `research.html`, priority `medium`, risk `high`, action `answer_owner_questions_before_intake`
  - Chain: `automation/reports/llm-worker-chain-fixture-research-cross-check.md`

## Policy

- This fixture does not approve public copy.
- Public content still requires exact proposed text, owner approval, apply-preview, apply-approved, and strict QA.
- Use this fixture only to preview the GitHub owner handoff issue body.
