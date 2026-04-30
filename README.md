# OpenAI Codex Training

A hands-on training course for using OpenAI Codex across the CLI, app, IDE extensions, and cloud workflows.

## Course Overview

This 5-hour hands-on workshop covers installation, authentication, safe agent workflows, configuration, MCP servers, skills, cloud tasks, and practical development labs.

### What You'll Learn

- 🚀 **Installation & Setup**: CLI, app, IDE, ChatGPT login, and API-key authentication
- 🛡️ **Safety & Security**: Sandbox modes, approval policies, trusted projects, and reviews
- 🎯 **Core Features**: AGENTS.md guidance, custom prompts, profiles, and session resumption
- ⚡ **Agent Skills**: Reusable workflow bundles with scripts, references, and assets
- 🔧 **Advanced Capabilities**: MCP integration, Codex Cloud, local OSS models, and CI/CD workflows
- 💻 **Practical Skills**: Real-world exercises in Java, Python, and TypeScript

## Prerequisites

- Command-line experience
- Basic programming knowledge in at least one language
- Git familiarity
- Docker (for advanced exercises)

## Repository Structure

```
codex-training/
├── slides.md                     # Slidev presentation (160+ slides)
├── exercises/                    # Hands-on labs with starter code
│   ├── plan-mode-warmup/        # Lab 0: Plan mode and steering warm-up
│   ├── java-spring-boot/        # Lab 1: Spring Boot REST API
│   ├── python-refactoring/      # Lab 2: Legacy code refactoring
│   ├── react-forms/             # Lab 3: React TypeScript forms
│   ├── microservices/           # Lab 4: Multi-language microservices
│   ├── skills-creation/         # Lab 5: Create custom Codex skills
│   └── mcp-context7/            # Lab 6: Connect current docs through MCP
├── config-examples/              # Sample configurations
│   ├── basic-config.toml        # Minimal setup for beginners
│   └── advanced-config.toml     # Full features with MCP, profiles
├── prompts/                      # Custom prompt templates
│   └── *.md                     # security-audit, test-gen, etc.
├── docs/                         # Reference documentation
│   ├── TROUBLESHOOTING.md       # Common issues and solutions
│   └── MODEL-SELECTION.md       # Cost/performance guide
├── .github/workflows/            # CI/CD examples
│   └── codex-review.yml         # Automated PR review with Codex
└── exports/                      # Slide exports (PDF)
```

## Quick Start

### 1. Install Codex

```bash
# Via npm (recommended)
npm install -g @openai/codex

# Via Homebrew (macOS/Linux)
brew install codex

# Verify installation
codex --version
```

### 2. Authenticate

```bash
# ChatGPT account (recommended)
codex login

# Or store an API key with Codex
printenv OPENAI_API_KEY | codex login --with-api-key
```

### 3. Run Your First Command

```bash
codex "Create a hello world function in Python"
```

### 4. Start the Training

```bash
# Clone this repository
git clone https://github.com/kousen/codex-training
cd codex-training

# Install dependencies for slides
npm install

# Start the presentation
npm run dev

# Open browser to http://localhost:3030
```

## Exercises

### Lab 0: Planning and Steering Warm-Up
Learn the current Codex interaction model before the larger labs:
- Ask Codex to propose a plan before editing
- Steer an in-flight task with follow-up messages
- Inspect permissions, model choice, and diffs with slash commands

**Time**: 15-20 minutes

### Lab 1: Spring Boot REST API
Build a complete task management API with Spring Boot, including:
- CRUD operations with validation
- H2 database integration
- OpenAPI documentation
- Comprehensive test suite

**Time**: 60-90 minutes

### Lab 2: Python Code Refactoring
Transform legacy Python code using modern best practices:
- Add type hints and documentation
- Implement design patterns
- Create pytest test suite
- Setup code quality tools

**Time**: 45-60 minutes

### Lab 3: React TypeScript Forms
Create a production-ready registration form with:
- React Hook Form + Zod validation
- Accessibility compliance
- Multi-step workflow
- Full test coverage

**Time**: 45-60 minutes

### Lab 4: Microservices Architecture
Build an event-driven microservices system with:
- Multiple languages (Node.js, Python, Go, Java)
- RabbitMQ message queue
- Docker orchestration
- API gateway

**Time**: 90-120 minutes

### Lab 5: Skills Creation
Create a custom Codex skill using `$skill-creator`:
- SKILL.md format with YAML frontmatter
- Conventional commit message generator
- Team sharing via repository

**Time**: 30 minutes

### Lab 6: MCP Servers with Context7
Connect Codex to current library documentation:
- Add Context7 as an MCP server
- Inspect configured MCP tools
- Use current React Hook Form, Zod, pytest, and Spring docs in prompts

**Time**: 15-20 minutes

## Key Codex Features Covered

### Core Features
- ✅ Terminal UI navigation
- ✅ Sandbox modes and approval policies
- ✅ Project memory with AGENTS.md
- ✅ Custom prompts and profiles
- ✅ Session management and resumption

### Agent Skills
- ✅ Creating reusable skill bundles
- ✅ SKILL.md format and structure
- ✅ Explicit (`$skill-name`) and implicit invocation
- ✅ Built-in skills: `$skill-creator`, `$skill-installer`
- ✅ Skills vs prompts comparison

### Advanced Features
- ✅ Model Context Protocol (MCP)
- ✅ OpenAI models plus local OSS providers through Ollama or LM Studio
- ✅ Running as MCP server
- ✅ Codex App, IDE extensions, and Codex Cloud workflows
- ✅ CI/CD integration
- ✅ Non-interactive execution

### Configuration
- ✅ TOML configuration files
- ✅ Project-local config (`.codex/config.toml`)
- ✅ Environment variables
- ✅ Shell environment policies
- ✅ Notification systems

## Tips for Success

1. **Start Conservatively**: Use `workspace-write` with `on-request`, or `read-only` for review-only tasks
2. **Use AGENTS.md**: Provide context for better results
3. **Create Profiles**: Separate development/production configurations
4. **Review Generated Code**: Never blindly accept AI suggestions
5. **Leverage MCP**: Pull current documentation and project data into prompts
6. **Test Thoroughly**: Always verify generated code works correctly

## Useful Commands Reference

```bash
# Basic usage
codex                          # Interactive mode
codex "prompt"                 # Start with initial prompt
codex exec "prompt"            # Execute and exit
codex resume                   # Resume session picker
codex resume --last            # Resume most recent session
codex update                   # Update the CLI

# Configuration
codex --profile development    # Use specific profile
codex --sandbox read-only      # Set sandbox mode
codex --model gpt-5.5          # Select model when available
codex --model gpt-5.4          # Fallback for API-key auth or availability
codex --search "latest docs"   # Enable live web search for that run

# Advanced
codex mcp list                 # List configured MCP servers
codex mcp login server-name    # OAuth login for supported MCP servers
codex mcp-server               # Expose Codex itself as an MCP server
codex cloud exec "prompt"      # Launch a cloud task
codex cloud diff               # Inspect cloud task changes
codex cloud apply              # Apply cloud task changes locally
codex login --device-auth      # Device-auth flow for remote/headless environments
codex review --uncommitted     # Review local changes
```

Inside an interactive Codex session, you can also invoke skills directly:

```text
$skill-creator
$skill-installer linear
$create-plan
```

## Resources

### Course Materials
- [Course Slides](./slides.md) - Full Slidev presentation
- [Exercises](./exercises/) - Hands-on labs with starter code
- [Troubleshooting Guide](./docs/TROUBLESHOOTING.md) - Common issues and solutions
- [Model Selection Guide](./docs/MODEL-SELECTION.md) - Cost/performance optimization

### Official Documentation
- [Codex CLI Documentation](https://developers.openai.com/codex/cli/)
- [Codex App Documentation](https://developers.openai.com/codex/app/)
- [Codex MCP Documentation](https://developers.openai.com/codex/mcp/)
- [Codex GitHub Repository](https://github.com/openai/codex)
- [Agent Skills Documentation](https://developers.openai.com/codex/skills/)
- [Skills Catalog](https://github.com/openai/skills)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [agentskills.io Specification](https://agentskills.io)

## Instructor

**Kenneth Kousen**
- President, Kousen IT, Inc.
- Author & Technical Trainer
- ken.kousen@kousenit.com
- https://www.kousenit.com

## Contributing

Found an issue or want to contribute? Please:
1. Open an issue on GitHub
2. Submit a pull request
3. Share your experience

## License

This training material is licensed under the MIT License. See [LICENSE](./LICENSE) file for details.

## Acknowledgments

- OpenAI for Codex
- The open-source community for MCP tools

---

**Ready to start?** Navigate to the [exercises](./exercises/) directory and begin with Lab 1!
