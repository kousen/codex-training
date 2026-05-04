# Codex CLI Training Materials

This repository contains training materials for a 5-hour hands-on workshop on OpenAI Codex CLI.

## Project Context

- **Purpose**: Professional training course for developers learning Codex CLI
- **Audience**: Developers with command-line experience, basic programming knowledge
- **Format**: Slidev presentation + hands-on exercises
- **Current Codex Version**: v0.114 (March 2026)

## Key Files

| File | Purpose |
|------|---------|
| `slides.md` | Main Slidev presentation (160+ slides) |
| `exercises/*/README.md` | Lab instructions for each exercise |
| `exercises/*/starter/` | Starting code for students |
| `exercises/*/AGENTS.md` | Project context for Codex |
| `config-examples/*.toml` | Sample configuration files |
| `docs/TROUBLESHOOTING.md` | Common issues and solutions |
| `docs/MODEL-SELECTION.md` | Model cost/performance guide |

## Technology Stack

- **Slides**: Slidev (Vue-based presentation framework)
- **Lab 1**: Java 17, Spring Boot 3.2, Maven
- **Lab 2**: Python 3.11+, pytest, mypy
- **Lab 3**: React 18, TypeScript, Vite, React Hook Form, Zod
- **Lab 4**: Docker, RabbitMQ, PostgreSQL, MongoDB
- **Lab 5**: Codex Skills (SKILL.md format)
- **Lab 6**: MCP Servers (Context7, live documentation)

## Important Notes

### Model Names (March 2026)
- `gpt-5.4` - Latest frontier model, default
- `gpt-5.3-codex` - Frontier agentic coding model
- `gpt-5.2-codex` - Strong long-horizon coding model
- `gpt-5.1-codex-max` - Deep reasoning, long sessions

### Installation
```bash
brew install --cask codex  # NOT 'brew install codex'
```

### Exercise Vulnerabilities
The Dependabot alerts for this repo are **intentional** - they exist in the exercise starter code so students can practice fixing them with Codex.

## When Modifying

1. **Slides**: Keep model names current, verify installation commands
2. **Exercises**: Each has its own AGENTS.md - update if requirements change
3. **Config examples**: Must use current TOML syntax and model names
4. **Exports**: Run `slidev export` after slide changes

## Commands

```bash
# Start slides locally
npm run dev

# Export slides
slidev export slides.md --output exports/slides.pdf --format pdf

# Run specific exercise
cd exercises/java-spring-boot/starter
./mvnw spring-boot:run
```
