---
name: document-driven-design-only
description: Run the research and planning phase of development to produce a functional architecture, design spec, and checklist without modifying code or writing implementation files.
---
# Document-Driven Design Only (No Code)
Research, design, and plan without executing implementation code.

## Workflow
1. Research: Trace flow, explore boundaries/dependencies, understand constraints.
2. Architecture (`design_spec.md`): Mermaid diagram, API/data contracts, risks/pitfalls, execution context file list.
3. Tasks (`task.md`): Checkbox list of sequential tasks grouped by layer.

## CRITICAL CONSTRAINT: NO CODE
Do not modify workspace files or write tests. Stop immediately after writing `design_spec.md` and `task.md` to wait for approval.
