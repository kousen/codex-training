# Lab 2: Python Code Refactoring

## Objective
Use Codex to refactor legacy Python code into modern, maintainable, and well-tested code.

## Starting Code

The `legacy_code.py` file contains poorly written calculator and data processing code that needs significant improvement.

## Refactoring Goals

1. **Type Hints**
   - Add comprehensive type hints using Python 3.10+ syntax
   - Use typing module features (Optional, Union, List, Dict, etc.)
   - Add mypy configuration

2. **Code Structure**
   - Apply SOLID principles
   - Use design patterns where appropriate
   - Separate concerns into modules

3. **Error Handling**
   - Replace generic exceptions with specific ones
   - Add proper error messages
   - Implement logging

4. **Modern Python Features**
   - Use dataclasses or Pydantic models
   - Apply decorators for cross-cutting concerns
   - Use context managers for resource handling

5. **Testing**
   - Create pytest test suite
   - Achieve 100% code coverage
   - Add property-based tests with Hypothesis
   - Include fixtures and parameterized tests

6. **Documentation**
   - Add comprehensive docstrings (Google style)
   - Create README with usage examples
   - Generate API documentation with Sphinx

7. **Code Quality**
   - Configure and pass: black, isort, flake8, pylint
   - Add pre-commit hooks
   - Create Makefile for common tasks

## Codex Prompts Progression

### Step 1: Analyze Current Code
```bash
codex "Analyze legacy_code.py and create a refactoring plan identifying all issues and improvements needed"
```

### Step 2: Add Type Hints
```bash
codex "Add comprehensive type hints to all functions and classes using modern Python 3.10+ syntax"
```

### Step 3: Restructure with Design Patterns
```bash
codex "Refactor the calculator using the Strategy pattern and the data processor using Chain of Responsibility"
```

### Step 4: Improve Error Handling
```bash
codex "Replace all generic exceptions with custom exceptions and add proper error handling with logging"
```

### Step 5: Modernize Code
```bash
codex "Convert to use dataclasses, add decorators for validation, and implement context managers for file operations"
```

### Step 6: Create Test Suite
```bash
codex "Create comprehensive pytest test suite with fixtures, parameterized tests, and property-based tests using Hypothesis"
```

### Step 7: Add Documentation
```bash
codex "Add Google-style docstrings to all functions and classes, create usage examples"
```

### Step 8: Setup Code Quality Tools
```bash
codex "Configure black, isort, flake8, pylint, and mypy with appropriate settings. Add pre-commit hooks"
```

### Step 9: Create Build System
```bash
codex "Create a Makefile with targets for format, lint, test, coverage, and docs"
```

### Step 10: Package for Distribution
```bash
codex "Create setup.py and pyproject.toml for proper Python packaging with all dependencies"
```

## Legacy Code Issues to Fix

1. No type hints
2. Poor naming conventions
3. No error handling
4. Tightly coupled code
5. No tests
6. Magic numbers and strings
7. No documentation
8. Mixed responsibilities
9. No input validation
10. Resource leaks

## Success Criteria

- [ ] All functions have type hints
- [ ] 100% test coverage
- [ ] All linting tools pass
- [ ] Documentation generated
- [ ] Code follows PEP 8
- [ ] No code smells
- [ ] Performance improved
- [ ] Memory leaks fixed

## Advanced Challenges

1. Add async/await support
2. Implement caching with functools
3. Add CLI with Click or Typer
4. Create REST API with FastAPI
5. Add performance profiling

## Testing Your Refactored Code

```bash
# Run tests
pytest -v

# Check coverage
pytest --cov=src --cov-report=html

# Run type checking
mypy src/

# Run linting
flake8 src/
pylint src/

# Format code
black src/
isort src/

# Run all checks
make all
```

## Configuration Files to Create

### pyproject.toml
```toml
[tool.black]
line-length = 88
target-version = ['py310']

[tool.isort]
profile = "black"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### .pre-commit-config.yaml
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
```