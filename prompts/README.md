# Codex Custom Prompts

This directory contains custom prompt templates for use with OpenAI Codex CLI.

## Installation

Copy these files to your Codex prompts directory:

```bash
cp -r prompts/* ~/.codex/prompts/
```

## Available Prompts

### `/refactor`
Refactors code following clean code principles.

### `/security-audit`
Performs comprehensive security analysis with severity ratings.

### `/test-gen`
Generates unit tests with 80% coverage target.

### `/pr-review`
Reviews code like a senior engineer would.

### `/api-upgrade`
Migrates code to use latest API versions.

### `/perf-fix`
Analyzes and optimizes performance bottlenecks.

## Usage

After installing, use these prompts in Codex:

```bash
# Interactive mode
codex
> /security-audit

# Non-interactive mode
codex exec "Run /security-audit on the UserService class"
```

## Creating Your Own

1. Create a new `.md` file in `~/.codex/prompts/`
2. Name it after your command (e.g., `deploy-check.md` for `/deploy-check`)
3. Write clear instructions in markdown format

## Note on Arguments

Codex doesn't currently support parameterized prompts like Claude Code's `$ARGUMENTS`.
See `scripts/review-file.sh` for a workaround using shell scripts.