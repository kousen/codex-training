# Codex Training Exercises

This directory contains hands-on exercises for learning OpenAI Codex.

## Available Exercises

### Lab 0: Planning and Steering Warm-Up
- `plan-mode-warmup/` - Learn planning, steering, permissions, and key slash commands (15 min)

### Lab 1: Generate from Scratch
- `java-spring-boot/` - Build a complete REST API with Spring Boot

### Lab 2: Refactor Existing Code
- `python-refactoring/` - Improve legacy Python code quality

### Lab 3: Frontend Development
- `react-forms/` - Build production-ready React TypeScript forms

### Lab 4: Multi-Language Projects
- `microservices/` - Build an event-driven microservices architecture

### Lab 5: Agent Skills
- `skills-creation/` - Create a custom Codex skill for commit messages

### Lab 6: MCP Servers
- `mcp-context7/` - Connect Codex to live library documentation via MCP

## Getting Started

Each exercise directory contains:
- `README.md` - Exercise instructions and Codex prompt progression
- `starter/` - Initial code to work with (most exercises)
- `AGENTS.md` - Project context for Codex (most exercises)

Note: These are hands-on exercises where you build the solution using Codex. Reference implementations are not provided—the goal is to practice using Codex to generate and refactor code.

## Recommended Order

0. **Lab 0** - Planning and Steering Warm-Up (interaction model, 15 min)
1. **Lab 1** - Java Spring Boot (generation)
2. **Lab 2** - Python Refactoring (code improvement)
3. **Lab 3** - React Forms (frontend development)
4. **Lab 4** - Microservices (multi-language, advanced)
5. **Lab 5** - Skills Creation (extending Codex)
6. **Lab 6** - MCP Servers (connecting external data sources)

## Using Codex for Exercises

### Basic Workflow

```bash
# Navigate to exercise directory
cd java-spring-boot

# Review the AGENTS.md file
cat AGENTS.md

# Start Codex
codex

# Follow exercise instructions
```

### Tips for Success

1. **Read AGENTS.md first** - Provides context to Codex
2. **Use appropriate profiles** - Development vs production
3. **Start with conservative permissions** - Prefer `workspace-write` with `on-request`
4. **Review generated code** - Never blindly accept
5. **Use MCP for current docs** - Especially for fast-moving libraries
6. **Run tests frequently** - Ensure correctness

## Exercise Completion Checklist

- [ ] Code compiles/runs without errors
- [ ] All tests pass
- [ ] Code follows project conventions
- [ ] Documentation is complete
- [ ] Security best practices followed
- [ ] Performance is acceptable

## Need Help?

- Review the main slides for concept explanations
- Use `codex "explain this error"` for debugging
- Check the exercise README for step-by-step Codex prompts
- Ask in the workshop chat or discussions
