---
name: autonomous-dev-planning
description: >
  Use when starting autonomous development on a feature, bug fix, or refactor.
  Performs deep codebase research, dependency analysis, and creates a structured
  implementation plan without writing any code. Designed for token-efficient
  autonomous workflows.
---
# Autonomous Development - Planning
Prepare an implementation plan for autonomous execution.

## CRITICAL CONSTRAINT: RESEARCH & PLANNING ONLY
Do not modify files or run test/build commands. Sole output is `implementation_plan.md`. Every token must reduce execution risk.

## Instructions
1. Reconnaissance: Identify affected modules, map dependencies, find existing tests and conventions.
2. Impact: List all files to create/modify/delete, flag risks/regressions, clarify ambiguities, estimate unit complexity.
3. Sequence: Order atomic, verifiable steps. Define functions/API contracts.
4. Verification: List exact test commands and acceptance criteria.

## Output Format
Create `implementation_plan.md` using the standard format. Keep descriptions/bullets <10 words. Request feedback.
