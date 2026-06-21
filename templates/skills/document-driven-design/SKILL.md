---
name: document-driven-design
description: >
  Provides a structured workflow for Document-Driven Design (DocDD) and development.
  Guides the agent to design functional architectures, identify technical pitfalls,
  and write token-efficient specs suitable for local models (e.g. Ollama) before coding.
---
# Document-Driven Design (DocDD)
Design functional architecture and assess risks before coding.

## Philosophy
1. Design Before Dev.
2. Context Minimization: Keep specs concise, using Mermaid/tables.
3. Explicit Gates: Obtain approval on design/plan first.

## Workflow
- Phase 1: Research: Trace target flow. Use targeted grep/view on line ranges.
- Phase 2: Design (`design_spec.md`): Create Mermaid diagram, API contracts, risk/pitfall list, and minimal context file list. Wait for approval.
- Phase 3: Plan (`implementation_plan.md` & `task.md`): Create checkbox checklist. Wait for approval.
- Phase 4: Execution: Sequential precise replacements. Update `task.md`.
- Phase 5: Verification: Run tests, trace requirements to test cases in `walkthrough.md`.
