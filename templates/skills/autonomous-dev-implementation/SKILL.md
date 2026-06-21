---
name: autonomous-dev-implementation
description: >
  Use to autonomously execute an approved implementation plan. Writes production
  code, creates tests, and modifies files in strict sequence. No explanations,
  no architectural discussion — pure high-density code execution.
---
# Autonomous Development - Implementation
Execute approved plan with full autonomy.

## CRITICAL CONSTRAINT: HIGH-DENSITY CODE ONLY
Do not narrate, explain, or state plans. Every token must produce code, tests, or configs. Run silently.

## Instructions
1. Protocol: Execute steps sequentially. Update `task.md` checkbox status. Write complete code without placeholders.
2. Quality: Add error handling, match planned signatures, preserve unrelated comments.
3. Tests: Write runnable tests (imports, fixtures) covering planned edge cases.
4. Verification: Run tests and linters after each group. Fix failures before proceeding.

## Output
Update `task.md`. Create a 3-line `walkthrough.md` list of changes and test results.
