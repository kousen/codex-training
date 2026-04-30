# Lab 5: Skills Creation

## Objective
Use Codex to create a custom skill that generates conventional commit messages following team standards.

## Background

Agent Skills are reusable instruction bundles that extend Codex's capabilities. They can include instructions, scripts, references, and assets. Codex loads only the name and description at startup, then reads the full `SKILL.md` when the skill is selected.

Skills can be invoked explicitly with `$skill-name` or selected implicitly based on the description. Use `/skills` in an interactive session to inspect what is available.

## Requirements

Build a skill that:

1. **Analyzes Git Changes**
   - Reads staged files and their diffs
   - Understands the scope of changes
   - Identifies file types and patterns

2. **Generates Conventional Commits**
   - Follows the [Conventional Commits](https://conventionalcommits.org) specification
   - Suggests appropriate type: feat, fix, docs, style, refactor, test, chore
   - Includes scope when applicable
   - Writes clear, concise descriptions

3. **Team Customization**
   - Configurable commit types
   - Custom scopes for your project
   - Optional issue/ticket number integration

## Starting Point

Use `$skill-creator` to bootstrap your skill:

```bash
$skill-creator Create a skill for generating conventional commit messages
```

## Skill Structure

Your completed skill should have this structure:

```
~/.agents/skills/commit-gen/
├── SKILL.md          # Required: YAML frontmatter + instructions
├── agents/           # Optional: Codex metadata and dependencies
│   └── openai.yaml
├── scripts/          # Optional: executable helpers
├── references/       # Optional: commit examples
│   └── conventions.md
└── assets/           # Optional: templates
    └── template.txt
```

## Step-by-Step Guide

### Step 1: Create the Skill Skeleton

```bash
$skill-creator Create a skill called commit-gen that helps generate conventional commit messages by analyzing staged changes
```

Review the generated SKILL.md and customize as needed.

### Step 2: Define the Skill Metadata

Edit `~/.agents/skills/commit-gen/SKILL.md`:

```yaml
---
name: commit-gen
description: >
  Generate conventional commit messages. Use when asked to write a
  commit message, create a commit, or when user runs git commit.
  Triggers: "commit message", "write commit", "generate commit".
---

# Commit Message Generator

Generate conventional commit messages following project standards.

## Workflow

1. **Analyze Changes**: Run `git diff --staged` to see what's staged
2. **Identify Type**: Determine the commit type from the changes
3. **Extract Scope**: Identify the component/module affected
4. **Generate Message**: Create a clear, concise commit message

## Commit Types

- **feat**: New feature for the user
- **fix**: Bug fix for the user
- **docs**: Documentation changes
- **style**: Formatting, no code change
- **refactor**: Code restructuring, no behavior change
- **test**: Adding or updating tests
- **chore**: Build process, dependencies

## Output Format

```
<type>(<scope>): <description>

<optional body>

<optional footer>
```
```

### Step 3: Add Reference Material

Create `~/.agents/skills/commit-gen/references/conventions.md`:

```markdown
# Conventional Commits Quick Reference

## Examples

### Feature
```
feat(auth): add OAuth2 login support

Implements Google and GitHub OAuth providers with
automatic account linking for existing users.

Closes #123
```

### Bug Fix
```
fix(api): handle null response from payment gateway

Check for null before accessing response properties
to prevent 500 errors during checkout.

Fixes #456
```

### Refactor
```
refactor(database): migrate to connection pooling

Replace individual connections with HikariCP pool
for improved performance under load.
```

## Scope Guidelines

Use lowercase, typically matching:
- Directory names (api, web, cli)
- Feature areas (auth, payment, search)
- Component names (button, modal, form)
```

### Step 4: Test Your Skill

1. Stage some changes in a Git repository:
   ```bash
   git add .
   ```

2. Invoke the skill:
   ```bash
   $commit-gen
   ```

3. Alternatively, test implicit invocation:
   ```bash
   Write a commit message for my staged changes
   ```

## Success Criteria

- [ ] Skill created at `~/.agents/skills/commit-gen/`
- [ ] SKILL.md has valid YAML frontmatter
- [ ] Description triggers match commit-related queries
- [ ] Skill correctly analyzes staged changes
- [ ] Generated messages follow conventional format
- [ ] Messages are clear and accurate

## Advanced Challenges

1. **Issue Integration**: Add support for extracting issue numbers from branch names
2. **Multi-language Support**: Generate commit messages in different languages
3. **Breaking Changes**: Automatically detect and flag breaking changes
4. **Changelog Integration**: Generate changelog entries alongside commits
5. **Team Templates**: Support multiple commit templates for different projects

## Sharing Your Skill

### Project-Level Sharing

Copy your skill to the project's `.agents/skills/` directory. Codex scans repo
skills from the current directory up to the repository root, so this is the
right location for team-shared workflows.

```bash
cp -r ~/.agents/skills/commit-gen .agents/skills/
git add .agents/skills/commit-gen
git commit -m "chore: add commit-gen skill for team"
```

### Skill Catalog Submission

For wider distribution, package the skill in a plugin or contribute it to a
shared skills catalog.

## Tips

- **Keep instructions focused**: Skills work best with clear, specific workflows
- **Write precise descriptions**: The description is what Codex sees before loading the full skill
- **Test implicit invocation**: Verify your description matches user intent
- **Add examples**: Reference files with examples improve output quality
- **Use scripts for repeatable work**: Put deterministic commands in `scripts/` instead of re-describing them
- **Iterate**: Refine your skill based on real usage

## Comparison: Skills vs Custom Prompts

| Aspect | Skills | Custom Prompts |
|--------|--------|----------------|
| Structure | Directory with SKILL.md + resources | Single text file |
| Invocation | `$skill-name` or implicit | Manual copy/paste |
| Sharing | Git-friendly, team-distributable | Single file |
| Resources | Can include scripts, templates, docs | Text only |
| Best for | Complex workflows | Simple templates |
