# Codex Troubleshooting Guide

Quick solutions to common issues you may encounter during the training.

## Step zero: `codex doctor`

Before the manual recipes below, run the built-in diagnostic:

```bash
codex doctor            # install, config, auth, network, runtime health
codex doctor --all      # everything, including slower checks
codex doctor --json     # redacted machine-readable report (for bug reports)
```

It also surfaces startup warnings for skills, hooks, plugins, MCP, and
deprecated config — which covers most of this guide's sections in one shot.

---

## Installation Issues

### "codex: command not found"

**Cause:** Codex not in PATH or not installed correctly.

```bash
# Check if installed
which codex

# Reinstall via Homebrew (macOS/Linux)
brew reinstall --cask codex

# Or via npm
npm uninstall -g @openai/codex
npm install -g @openai/codex

# Verify installation
codex --version
```

### "Error: EACCES permission denied"

**Cause:** npm global directory permission issues.

```bash
# Fix npm permissions (recommended)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Reinstall
npm install -g @openai/codex
```

---

## Authentication Issues

### "Authentication failed" or "Invalid API key"

```bash
# Re-authenticate with ChatGPT account
codex login

# Or store an API key with Codex
printenv OPENAI_API_KEY | codex login --with-api-key
```

### "Rate limit exceeded"

**Cause:** Too many requests in a short period.

```bash
# Wait 60 seconds and retry
# Or switch to a faster model
codex --model gpt-5.4-mini

# Check your rate limits
cat ~/.codex/config.toml | grep rate
```

### Login hangs in headless environment

```bash
# Use device-auth flow for SSH/remote environments
codex login --device-auth

# Follow the URL and enter the code manually
```

---

## Sandbox Issues

### "Operation not permitted" in sandbox mode

**Cause:** Sandbox is blocking the operation.

```bash
# Check current sandbox mode
grep sandbox_mode ~/.codex/config.toml

# Restart with a more permissive sandbox if needed
codex --sandbox danger-full-access
```

### "Cannot write to file outside workspace"

**Cause:** `workspace-write` sandbox restricts writes to current directory.

```bash
# Option 1: Navigate to the target directory first
cd /path/to/project
codex

# Option 2: Use danger-full-access mode
codex --sandbox danger-full-access
```

---

## MCP (Model Context Protocol) Issues

### "MCP server failed to start"

```bash
# Test the MCP server directly
npx @modelcontextprotocol/server-github --help

# Check environment variables
echo $GITHUB_TOKEN

# Verify config syntax
cat ~/.codex/config.toml | grep -A5 mcp_servers
```

### "MCP server timeout"

**Cause:** Server taking too long to initialize.

```toml
# Add timeout configuration in config.toml
[mcp_servers.github]
command = "npx"
args = ["@modelcontextprotocol/server-github"]
startup_timeout_sec = 30  # Increase timeout
```

### "Tool not found" from MCP server

```bash
# List available tools from the server
codex "List all available MCP tools"

# Check server is loaded
codex "What MCP servers are connected?"
```

---

## Session Issues

### "Session context too long"

**Cause:** Conversation exceeded context window.

```bash
# Start a fresh session
codex

# Or resume an existing session
codex resume
```

### "Cannot resume session"

```bash
# List available sessions
codex resume

# If corrupted, move session data aside
mv ~/.codex/sessions ~/.codex/sessions.backup

# Start fresh
codex
```

---

## Model Issues

### "Model not available"

```bash
# Launch with a specific known-good model
codex --model gpt-5.6-sol

# See exactly which models your account can use
codex debug models

# In the TUI, use /model to inspect or switch models interactively
```

### "Unexpected model behavior"

```bash
# Check current model
grep model ~/.codex/config.toml

# Try with explicit model
codex --model gpt-5.6-sol

# Use a profile with known-good settings
# (profiles are per-file since 0.134: ~/.codex/<name>.config.toml)
codex --profile thorough
```

---

## Performance Issues

### Codex is slow

1. **Check network connection**
   ```bash
   ping api.openai.com
   ```

2. **Try a faster model**
   ```bash
   codex --model gpt-5.4-mini
   ```

3. **Reduce context size**
   ```toml
   # In config.toml
   project_doc_max_bytes = 16384  # Smaller AGENTS.md limit
   ```

4. **Check for MCP server issues**
   ```bash
   # Temporarily disable MCP
   mv ~/.codex/config.toml ~/.codex/config.toml.bak
   codex  # Test without MCP
   ```

### High token usage

```bash
# Use mini model for simple tasks
codex --model gpt-5.4-mini

# Be specific in prompts (shorter responses)
codex "Fix the bug on line 42"  # vs "Review the whole file"
```

---

## Exercise-Specific Issues

### Spring Boot won't start

```bash
# Check Java version (need 17+)
java -version

# Clean and rebuild
./mvnw clean install -DskipTests

# Check for port conflicts
lsof -i :8080
```

### Python dependencies fail

```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Docker containers won't start

```bash
# Check Docker is running
docker ps

# Reset containers
docker-compose down -v
docker-compose up -d

# Check logs
docker-compose logs rabbitmq
```

### React tests fail

```bash
# Clear node_modules
rm -rf node_modules package-lock.json
npm install

# Run tests with verbose output
npm test -- --verbose
```

---

## Getting Help

### Collect diagnostic information

```bash
# Codex version
codex --version

# Configuration
cat ~/.codex/config.toml

# Recent logs (if logging enabled)
tail -100 ~/.codex/log/codex-tui.log
```

### Reset to defaults

```bash
# Backup current config
mv ~/.codex ~/.codex.backup

# Codex will create fresh defaults
codex
```

### Report issues

1. Check [GitHub Issues](https://github.com/openai/codex/issues)
2. Include: version, OS, config (redact API keys), error message
3. Provide minimal reproduction steps

---

## Quick Reference

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| "command not found" | Not installed | `brew install --cask codex` |
| "Authentication failed" | Bad credentials | `mv ~/.codex/auth ~/.codex/auth.backup && codex login` |
| "Operation not permitted" | Sandbox restriction | Inspect permissions, or relaunch with `--sandbox danger-full-access` |
| "MCP server failed" | Missing env var | Check `$GITHUB_TOKEN` etc. |
| "Rate limit exceeded" | Too many requests | Wait 60s or use smaller model |
| Slow responses | Large context | Reduce `project_doc_max_bytes` |
| Session corrupted | Cache issue | `mv ~/.codex/sessions ~/.codex/sessions.backup` |
