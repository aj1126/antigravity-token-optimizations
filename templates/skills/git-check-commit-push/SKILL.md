---
name: git-check-commit-push
description: Check for untracked/modified changes in the workspace, draft a descriptive commit message, commit them, and push the commit.
---
# Git Check, Commit, and Push
Automate staging, committing, and pushing workspace changes.

## Workflow
1. Status: Run `git status`. If clean, stop and notify user.
2. Stage: Run `git add -A`.
3. Message: Run `git diff --cached --stat` to view changes. Draft a concise conventional commit message (max 50 chars).
4. Commit: Run `git commit -m "<message>"`.
5. Push: Run `git push`.
