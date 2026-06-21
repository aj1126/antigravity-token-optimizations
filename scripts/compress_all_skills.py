import os
import re

class Section:
    def __init__(self, heading_line, level):
        self.heading_line = heading_line
        self.level = level
        self.content = []  # list of strings (lines), dicts (code blocks), or Section objects

def parse_markdown_to_tree(body_lines):
    root = Section("", 0)
    stack = [root]
    
    in_code_block = False
    code_block_lines = []
    
    for line in body_lines:
        stripped = line.strip()
        
        # Handle code blocks
        if stripped.startswith('```'):
            if in_code_block:
                code_block_lines.append(line)
                stack[-1].content.append({'type': 'code_block', 'lines': code_block_lines})
                code_block_lines = []
                in_code_block = False
            else:
                in_code_block = True
                code_block_lines.append(line)
            continue
            
        if in_code_block:
            code_block_lines.append(line)
            continue
            
        # Handle headings
        m = re.match(r'^(#+)\s+(.*)$', line)
        if m:
            level = len(m.group(1))
            new_sec = Section(line, level)
            
            while len(stack) > 1 and stack[-1].level >= level:
                stack.pop()
                
            stack[-1].content.append(new_sec)
            stack.append(new_sec)
            continue
            
        # Normal content line
        stack[-1].content.append(line)
        
    return root

def has_code_block(node):
    if isinstance(node, dict) and node.get('type') == 'code_block':
        return True
    if isinstance(node, Section):
        return any(has_code_block(child) for child in node.content)
    return False

def is_rule_heading(heading_line):
    h = heading_line.lower()
    return any(x in h for x in ['prerequisite', 'setup', 'rule', 'constraint', 'install', 'hook'])

def section_has_actual_content(node):
    if not isinstance(node, Section):
        return False
    for child in node.content:
        if isinstance(child, dict) and child.get('type') == 'code_block':
            return True
        elif isinstance(child, Section):
            if section_has_actual_content(child):
                return True
        elif isinstance(child, str):
            if child.strip():
                return True
    return False

def filter_and_clean_tree(node, parent_is_rule=False):
    if not isinstance(node, Section):
        return node
        
    current_is_rule = parent_is_rule or is_rule_heading(node.heading_line)
    new_content = []
    
    for child in node.content:
        if isinstance(child, Section):
            cleaned_child = filter_and_clean_tree(child, current_is_rule)
            if cleaned_child and section_has_actual_content(cleaned_child):
                new_content.append(cleaned_child)
        elif isinstance(child, dict) and child.get('type') == 'code_block':
            new_content.append(child)
        else:
            new_content.append(child)
            
    filtered_content = []
    n = len(new_content)
    
    is_near_code = [False] * n
    for i in range(n):
        c = new_content[i]
        if isinstance(c, dict) and c.get('type') == 'code_block':
            for j in range(max(0, i-2), i):
                if isinstance(new_content[j], str):
                    is_near_code[j] = True
                    
    for i in range(n):
        c = new_content[i]
        if isinstance(c, Section) or (isinstance(c, dict) and c.get('type') == 'code_block'):
            filtered_content.append(c)
        elif isinstance(c, str):
            stripped = c.strip()
            if not stripped:
                filtered_content.append(c)
                continue
                
            if current_is_rule:
                filtered_content.append(c)
            elif is_near_code[i] or stripped.startswith(('>', '[!', 'Warning:', 'Note:', 'CRITICAL:')) or 'scripts/' in stripped or 'uv run' in stripped:
                filtered_content.append(c)

                
    cleaned_filtered = []
    for c in filtered_content:
        if isinstance(c, str) and not c.strip():
            if cleaned_filtered and isinstance(cleaned_filtered[-1], str) and not cleaned_filtered[-1].strip():
                continue
        cleaned_filtered.append(c)
        
    node.content = cleaned_filtered
    return node

def write_tree_to_markdown(node):
    lines = []
    if node.heading_line:
        lines.append(node.heading_line)
        
    for child in node.content:
        if isinstance(child, Section):
            lines.append(write_tree_to_markdown(child))
        elif isinstance(child, dict) and child.get('type') == 'code_block':
            lines.extend(child['lines'])
        else:
            lines.append(child)
            
    return '\n'.join(lines)

def compress_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    parts = content.split('---')
    if len(parts) < 3:
        return content
        
    frontmatter = parts[1]
    body = '---'.join(parts[2:])
    
    frontmatter_lines = [line.strip() for line in frontmatter.strip().split('\n') if line.strip()]
    compressed_frontmatter = '\n'.join(frontmatter_lines)
    
    body_lines = body.split('\n')
    tree = parse_markdown_to_tree(body_lines)
    filtered_tree = filter_and_clean_tree(tree)
    compressed_body = write_tree_to_markdown(filtered_tree)
    
    compressed_body = compressed_body.strip()
    compressed_body = re.sub(r'\n{3,}', '\n\n', compressed_body)
    
    return f"---\n{compressed_frontmatter}\n---\n\n{compressed_body}\n"

# Hand-crafted compressed versions for the 9 global skills
GLOBAL_SKILLS_DATA = {
    "autonomous-dev-planning": """---
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
""",

    "autonomous-dev-implementation": """---
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
""",

    "autonomous-dev-review": """---
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
""",

    "document-driven-design": """---
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
""",

    "document-driven-design-only": """---
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
""",

    "git-check-commit-push": """---
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
""",

    "workspace-onboarding-planning": """---
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
""",

    "workspace-onboarding-development": """---
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
""",

    "workspace-onboarding-review": """---
name: workspace-onboarding-review
description: >
  Use to audit, evaluate, and verify workspace configuration compliance and inheritance
  integrity against universal workstation standards.
---
# Workspace Onboarding - Review
Audit workspace configuration compliance.

## CRITICAL CONSTRAINT: COMPACT EVALUATION ONLY
Use bulleted fragments, checklists, or tables. No code blocks or file rewrites.
1. Inheritance: Verify local configs properly cascade without duplication or redundant rules.
2. Boundaries: Check local hooks/formatters scope.
3. Discrepancies: Flag legacy drift violating workstation standards.
Output health check report.
"""
}

def run_compression(dry_run=True):
    total_original_bytes = 0
    total_compressed_bytes = 0
    files_processed = []

    # 1. Global skills
    global_dir = r"C:\Users\ajjuk\.gemini\config\skills"
    if os.path.exists(global_dir):
        for name, new_content in GLOBAL_SKILLS_DATA.items():
            filepath = os.path.join(global_dir, name, "SKILL.md")
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    orig_content = f.read()
                orig_len = len(orig_content)
                new_len = len(new_content)
                total_original_bytes += orig_len
                total_compressed_bytes += new_len
                files_processed.append((filepath, orig_len, new_len))
                if not dry_run:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

    # 2. Built-in science skills
    science_skills_dir = r"C:\Users\ajjuk\.gemini\config\plugins\science\skills"
    if os.path.exists(science_skills_dir):
        for entry in os.listdir(science_skills_dir):
            entry_path = os.path.join(science_skills_dir, entry)
            if os.path.isdir(entry_path):
                filepath = os.path.join(entry_path, "SKILL.md")
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        orig_content = f.read()
                    orig_len = len(orig_content)
                    
                    try:
                        compressed = compress_file(filepath)
                        new_len = len(compressed)
                        total_original_bytes += orig_len
                        total_compressed_bytes += new_len
                        files_processed.append((filepath, orig_len, new_len))
                        if not dry_run:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(compressed)
                    except Exception as e:
                        print(f"Error compressing {filepath}: {e}")

    # 3. Built-in android-cli skill
    android_cli_path = r"C:\Users\ajjuk\.gemini\config\plugins\android-cli-plugin\skills\SKILL.md"
    if os.path.exists(android_cli_path):
        with open(android_cli_path, 'r', encoding='utf-8') as f:
            orig_content = f.read()
        orig_len = len(orig_content)
        try:
            compressed = compress_file(android_cli_path)
            new_len = len(compressed)
            total_original_bytes += orig_len
            total_compressed_bytes += new_len
            files_processed.append((android_cli_path, orig_len, new_len))
            if not dry_run:
                with open(android_cli_path, 'w', encoding='utf-8') as f:
                    f.write(compressed)
        except Exception as e:
            print(f"Error compressing {android_cli_path}: {e}")

    print(f"Mode: {'DRY RUN' if dry_run else 'EXECUTION'}")
    print(f"Total files processed: {len(files_processed)}")
    print(f"Total original size: {total_original_bytes} bytes")
    print(f"Total compressed size: {total_compressed_bytes} bytes")
    print(f"Reduction: {(total_original_bytes - total_compressed_bytes) / total_original_bytes * 100:.2f}%")
    print(f"Saved: {total_original_bytes - total_compressed_bytes} bytes")

if __name__ == '__main__':
    # Default is dry run
    import sys
    dry = True
    if len(sys.argv) > 1 and sys.argv[1] == '--execute':
        dry = False
    run_compression(dry_run=dry)
