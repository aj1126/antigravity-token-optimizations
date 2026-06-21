---
name: autonomous-dev-review
description: >
  Use after autonomous development is complete to self-audit code changes,
  verify test coverage, check for regressions, and produce a compact
  diagnostic report. No code rewrites unless a critical defect is found.
---
# Autonomous Development - Review
Audit changes and verify correctness.

## CRITICAL CONSTRAINT: COMPACT DIAGNOSTICS ONLY
Do not rewrite code or explain architecture. Use checklists, brief tables, and verdict.

## Instructions
1. Audit: Verify changes match plan. Confirm no placeholders/TODOs. Check error handling.
2. Test: Run full suite. Report pass/fail counts. Verify acceptance criteria coverage.
3. Regression: Confirm legacy tests pass, check for new warnings, ensure no unintended edits.
4. Summary: List changed files with line deltas. Verdict: ✅ PASS, ⚠️ PASS WITH NOTES, or ❌ FAIL.

## Output
Terse markdown table of files, checklist, and overall verdict.
