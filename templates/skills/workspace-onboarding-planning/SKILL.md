---
name: workspace-onboarding-planning
description: >
  Use when onboarding an existing project workspace into our hierarchical workstation
  ecosystem. This skill performs gap analysis, local override mapping, and refactoring
  planning without generating code.
---
# Workspace Onboarding - Planning
Plan project onboarding into hierarchical workstation rulesets.

## CRITICAL CONSTRAINT: PLANNING ONLY
Do not generate code, configs, or scripts. Deliver a plan covering:
1. Gap Analysis: Identify local config conflicts with global user configuration. Plan deprecation/removal.
2. Local Mapping: Map minimal local `.vscode/settings.json` and `.cursorrules` (overrides only).
3. Migration: Provide step-by-step sequence list to migrate safely.
