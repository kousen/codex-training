# Exercise Setup Instructions

## Overview

This directory contains hands-on exercises for learning OpenAI Codex. Each exercise is designed to teach different aspects of using Codex for real-world development tasks.

## Exercise Structure

```
exercises/
├── plan-mode-warmup/      # Lab 0: Planning, steering, and permissions (15 min)
├── java-spring-boot/      # Lab 1: REST API Development
├── python-refactoring/    # Lab 2: Code Refactoring
├── react-forms/           # Lab 3: Frontend Development
├── microservices/         # Lab 4: Distributed Systems
├── skills-creation/       # Lab 5: Custom Codex Skills
└── mcp-context7/          # Lab 6: Current docs through MCP
```

## Prerequisites

### Required Software
- Git
- Node.js 18+ and npm
- Python 3.9+
- Java 17+ and Maven
- Go 1.21+ (for microservices exercise)
- Docker and Docker Compose
- OpenAI Codex CLI installed and authenticated

### Verify Installation
```bash
# Check Codex
codex --version

# Check other tools
node --version
python --version
java --version
go version
docker --version
```

## Setup Instructions

### Lab 0: Planning and Steering Warm-Up

```bash
cd plan-mode-warmup/starter
pip install pytest  # if not already installed
```

The starter includes:
- `inventory.py` — Small Python module with two intentional bugs
- `test_inventory.py` — Partial test suite

**Your Task**: Practice planning, steering, permissions, and key slash commands while fixing bugs and adding tests.

### Lab 1: Spring Boot API

```bash
cd java-spring-boot/starter
mvn clean install
```

The starter project includes:
- Basic Spring Boot application structure
- Maven configuration with all dependencies
- Empty main class ready for implementation

**Your Task**: Use Codex to build a complete task management API.

### Lab 2: Python Refactoring

```bash
cd python-refactoring
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

The starter includes:
- `legacy_processor.py` - Poorly written code that needs refactoring
- `requirements.txt` - All necessary Python packages

**Your Task**: Use Codex to refactor the legacy code following modern Python best practices.

### Lab 3: React TypeScript Forms

```bash
cd react-forms
npm install
npm run dev
```

The starter includes:
- Vite + React + TypeScript setup
- Tailwind CSS configured
- Basic App component with placeholder
- All necessary dependencies

**Your Task**: Use Codex to build a production-ready registration form.

### Lab 4: Microservices Architecture

```bash
cd microservices

# Start infrastructure services
docker-compose up -d

# Install dependencies for each service
cd auth-service && npm install && cd ..
cd order-service && pip install -r requirements.txt && cd ..
cd notification-service && go mod download && cd ..
cd analytics-service && mvn test && cd ..
```

The starter includes:
- Docker Compose configuration for RabbitMQ, PostgreSQL, MongoDB, Redis

You'll use Codex to implement each microservice in the provided service directories (auth-service, order-service, notification-service, analytics-service).

**Your Task**: Use Codex to implement a complete microservices system.

### Lab 5: Skills Creation

```bash
cd skills-creation
```

This lab teaches you to create custom Codex skills. No starter code is needed—you'll use the built-in `$skill-creator` skill to bootstrap your own skill.

**Your Task**: Create a custom skill that generates conventional commit messages.

## Using Codex for Exercises

### Best Practices

1. **Start with AGENTS.md**: Each exercise has an AGENTS.md file that provides context to Codex
2. **Use appropriate sandbox mode**: Start with `workspace-write` and `on-request`
3. **Review generated code**: Never blindly accept AI suggestions
4. **Test frequently**: Run tests after each major change
5. **Commit often**: Use Git to track your progress
6. **Use MCP docs when APIs matter**: Ask Codex to look up current docs before using fast-moving libraries

### Example Workflow

```bash
# Navigate to exercise
cd java-spring-boot

# Start Codex
codex

# Follow the prompts in README.md
"Generate a Spring Boot REST API for task management with full CRUD operations"

# Review the generated code
# Test the implementation
./mvnw test

# Iterate and improve
"Add input validation and error handling to all endpoints"
```

## Common Commands

### Spring Boot
```bash
# Run application
mvn spring-boot:run

# Run tests
mvn test

# Build
mvn clean package
```

### Python
```bash
# Run tests
pytest

# Check coverage
pytest --cov=src --cov-report=html

# Format code
black .
isort .

# Type check
mypy .
```

### React
```bash
# Development server
npm run dev

# Run tests
npm test

# Build for production
npm run build

# Type check
npm run type-check
```

### Microservices
```bash
# Start all infrastructure
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## Troubleshooting

### Port Conflicts
If you get port already in use errors:
- Spring Boot: Change port in `application.yml`
- React: Change port in `vite.config.ts`
- Microservices: Update ports in `docker-compose.yml`

### Database Connection Issues
- Ensure Docker is running
- Check if containers are healthy: `docker ps`
- View logs: `docker-compose logs postgres`

### Package Installation Problems
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- For Python, recreate virtual environment

## Getting Help

1. Check the exercise README.md for specific instructions
2. Review the AGENTS.md file for context
3. Use Codex in Ask mode: `codex "Explain the error I'm getting"`
4. Refer to the main slides for concept explanations

## Success Tips

- Read the entire exercise README before starting
- Use Codex's session resumption if you need to take breaks
- Experiment with different prompts to get better results
- Don't hesitate to refine and iterate on generated code
- Compare your solution with others in the discussion forum
