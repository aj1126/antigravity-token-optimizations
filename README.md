# AntiGravity Token & Budget Optimizations

This repository contains optimized templates, configuration files, and automation scripts designed for the **AntiGravity AI coding assistant** (and similar LLM-based agent ecosystems). 

The primary goal of these optimizations is to **minimize prompt/context size** (input tokens) and **limit verbosity in responses** (output tokens) to conserve your plan usage cap and budget without losing functional capability.

## Project Structure

```
.
├── scripts/
│   ├── compress_all_skills.py   # Script to compress science/tool SKILL.md files
│   └── compress_mcp_schemas.py  # Script to recursively compress MCP JSON schemas
├── templates/
│   ├── rules/
│   │   └── AGENTS.md            # Highly optimized global system rules
│   └── skills/                  # Hand-crafted global pipeline skills
│       ├── autonomous-dev-planning/SKILL.md
│       ├── autonomous-dev-implementation/SKILL.md
│       ├── autonomous-dev-review/SKILL.md
│       ├── document-driven-design/SKILL.md
│       ├── document-driven-design-only/SKILL.md
│       ├── git-check-commit-push/SKILL.md
│       ├── workspace-onboarding-planning/SKILL.md
│       ├── workspace-onboarding-development/SKILL.md
│       └── workspace-onboarding-review/SKILL.md
```

## Optimization Concepts & Intentions

### 1. Context Size Minimization
By default, AntiGravity loads the contents of active system rules (`AGENTS.md`), triggered skill instructions (`SKILL.md`), and registered MCP tool schemas (`*.json`) into the model's prompt on every turn. In large projects, this startup overhead can consume **50,000+ tokens** per message. 

* **Pruning Verbal Fluff**: Removing lengthy background explanations, common mistakes lists, and verbose workflows from skills.
* **Structural Filtering**: Eliminating empty headings and sections that do not contain actionable commands or parameters.
* **Rules Condensation**: Shortening system rules (Node.js worker thread management, PDF.js ingestion invariants, PowerShell constraints) to direct imperatives.

### 2. Output Verbosity Controls
Generating verbose text is the most expensive part of LLM usage (in terms of time and API budget).
* **Strict Constraints**: Adding explicit limits (e.g., maximum line limits for plans, bullet point constraints, code-only outputs, removing conversational padding) directly in the skills' instructions.
* **Narration-Free Execution**: Enforcing that code implementation phases output pure code/tests with zero explanations.

### 3. Minification of JSON Schemas
Tool definitions are loaded as JSON structures.
* Minifying schema JSON files (removing pretty-print spacing and indentation).
* Compressing description and parameter description texts while preserving schemas (like GraphQL schema syntax) to keep tools fully functional.

## Metrics & Combined Savings

* **Skill Files**: ~164,000 characters saved (**49.3%** size reduction).
* **MCP Schemas & Rules**: ~18,500 characters saved (**10.5%** size reduction).
* **Total Savings**: **~183,000 characters** (equivalent to **~45,000 tokens** saved on **every single message turn**).

## Installation & Usage

### Prerequisites
- Python 3.8+

### Step 1: Apply Hand-Crafted Global Skills & Rules
Copy the optimized global templates directly into your global configuration directory:
- Copy `templates/rules/AGENTS.md` to `~/.gemini/config/AGENTS.md`.
- Copy `templates/skills/*` folders to `~/.gemini/config/skills/`.

### Step 2: Compress Dynamic Tool Skills
Run the script to automatically parse and compress the science and Android-specific tool skills:
```bash
python scripts/compress_all_skills.py --execute
```

### Step 3: Compress MCP Tool JSON Schemas
Run the schema minification script to compress descriptions and remove spacing:
```bash
python scripts/compress_mcp_schemas.py --execute
```
