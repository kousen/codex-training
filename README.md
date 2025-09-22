# OpenAI Codex CLI Training

A comprehensive training course for mastering OpenAI Codex CLI - the lightweight terminal-based AI coding agent.

## Course Overview

This 5-hour hands-on workshop covers everything from basic installation to advanced multi-model configurations, custom MCP servers, and enterprise deployment patterns.

### What You'll Learn

- 🚀 **Installation & Setup**: Multiple authentication methods, configuration strategies
- 🛡️ **Safety & Security**: Sandbox modes, approval policies, secure configurations
- 🎯 **Core Features**: Project memory (AGENTS.md), custom prompts, profiles
- 🔧 **Advanced Capabilities**: MCP integration, multi-model support, CI/CD workflows
- 💻 **Practical Skills**: Real-world exercises in Java, Python, and TypeScript

## Prerequisites

- Command-line experience
- Basic programming knowledge in at least one language
- Git familiarity
- Docker (for advanced exercises)

## Repository Structure

```
codex-training/
├── slides.md                     # Slidev presentation
├── exercises/                    # Hands-on labs
│   ├── java-spring-boot/        # Spring Boot REST API
│   ├── python-refactoring/      # Legacy code refactoring
│   ├── react-forms/             # React TypeScript forms
│   └── microservices/           # Multi-language microservices
├── config-examples/              # Sample configurations
│   ├── basic-config.toml        # Minimal setup
│   ├── advanced-config.toml     # Full features
│   └── mcp-servers.toml         # MCP configurations
└── scripts/                      # Utility scripts
    ├── setup.sh                  # Environment setup
    └── verify-install.sh         # Installation check
```

## Quick Start

### 1. Install Codex

```bash
# Via npm (recommended)
npm install -g @openai/codex

# Via Homebrew
brew install codex

# Verify installation
codex --version
```

### 2. Authenticate

```bash
# ChatGPT account (recommended)
codex login

# Or use API key
export OPENAI_API_KEY="your-key"
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

## Key Codex Features Covered

### Core Features
- ✅ Terminal UI navigation
- ✅ Sandbox modes and approval policies
- ✅ Project memory with AGENTS.md
- ✅ Custom prompts and profiles
- ✅ Session management and resumption

### Advanced Features
- ✅ Model Context Protocol (MCP)
- ✅ Multi-model provider support (OpenAI, Anthropic, Ollama)
- ✅ Running as MCP server
- ✅ CI/CD integration
- ✅ Headless execution

### Configuration
- ✅ TOML configuration files
- ✅ Environment variables
- ✅ Shell environment policies
- ✅ Notification systems
- ✅ Logging and debugging

## Tips for Success

1. **Start with Read-Only Mode**: Get comfortable before making changes
2. **Use AGENTS.md**: Provide context for better results
3. **Create Profiles**: Separate development/production configurations
4. **Review Generated Code**: Never blindly accept AI suggestions
5. **Leverage MCP**: Extend capabilities with external tools
6. **Test Thoroughly**: Always verify generated code works correctly

## Useful Commands Reference

```bash
# Basic usage
codex                          # Interactive mode
codex -n "prompt"             # Non-interactive
codex --resume                # Resume last session
codex --search "text"         # Search codebase

# Configuration
codex --profile dev           # Use specific profile
codex --sandbox-mode auto     # Set sandbox mode
codex --approval-policy never # Set approval policy

# Advanced
codex serve                   # Run as MCP server
codex doctor                  # Diagnose issues
codex login --headless        # Headless authentication
codex --list-sessions         # Show all sessions
```

## Resources

- [Official Codex Documentation](https://github.com/openai/codex/docs)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Course Slides](./slides.md)
- [Exercise Solutions](./exercises/)

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

- OpenAI for Codex CLI
- Anthropic for inspiration from Claude Code
- The open-source community for MCP tools

---

**Ready to start?** Navigate to the [exercises](./exercises/) directory and begin with Lab 1!