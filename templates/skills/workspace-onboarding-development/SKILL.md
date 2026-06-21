---
name: workspace-onboarding-development
description: >
  Use to execute the implementation phase of onboarding an existing project
  workspace. Generates localized overrides, configuration snippets, and pre-commit
  hooks.
---
# Workspace Onboarding - Development
Execute onboarding implementation.

## CRITICAL CONSTRAINT: HIGH-DENSITY IMPLEMENTATION ONLY
Skip introductions and explanations. Output only functional configs.
1. Local Overrides: Minimal `.vscode/settings.json` and `.cursorrules` linking to `~/.global_ai_rules.md`.
2. Hooks: Shell code block for `.git/hooks/pre-commit.local` if validation gates are needed.
No structural placeholders.
