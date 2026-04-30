# Lab 6: MCP Servers with Context7

## Objective

Configure an MCP (Model Context Protocol) server in Codex and use it to pull
current library documentation into your prompts.

**Time:** 15-20 minutes

## Background: What Is MCP?

MCP is a protocol that lets Codex connect to external tools, data sources, and
documentation servers. Instead of relying only on model knowledge, Codex can
call MCP tools during a conversation.

Context7 is a documentation MCP server. It commonly exposes tools like:

| Tool | Purpose |
|------|---------|
| `resolve-library-id` | Converts a library name, such as `react-hook-form`, to a Context7 library ID |
| `query-docs` | Fetches current documentation and code examples for that library |

## Prerequisites

- Codex CLI installed and authenticated
- Node.js 18+ with `npx` available
- Internet access

Most Context7 setups work without an API key. If your Context7 account or
environment requires authentication, follow the Context7 dashboard instructions
and put secrets in environment variables, not directly in `config.toml`.

## Step 1: Add Context7 to Codex

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
```

Verify the server is configured:

```bash
codex mcp list
```

Restart Codex after adding the server, then inspect the live session:

```text
/mcp
```

## What Just Happened?

The CLI added a block like this to `~/.codex/config.toml`:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

When Codex starts, it launches the server as a subprocess, discovers the tools,
and can call those tools when your prompt asks for current docs.

## Step 2: Test a Documentation Query

Start Codex and ask:

```text
Use context7 to look up the current react-hook-form docs. What does
useForm return, and which return values matter for validation errors?
```

Observe:

- Codex resolves the library name
- Codex queries documentation before answering
- The answer should be grounded in current API details

## Step 3: Apply It to Lab 3

```bash
cd exercises/react-forms/starter
codex
```

Prompt:

```text
Use context7 to look up the current Zod and React Hook Form docs, then
create a registration form schema with email, password, confirmPassword,
username, and terms validation. Use the current APIs.
```

Then ask Codex to verify the implementation:

```text
Run the relevant tests and type checks. If there is a UI, tell me how to
inspect it in the browser before accepting the diff.
```

## Step 4: Try Other Libraries

```text
Use context7 to look up the current Spring Boot @RestController docs and
summarize the recommended exception-handling approach.
```

```text
Use context7 to find the current pytest fixtures documentation and show
how to use tmp_path in a test.
```

## Configuration Options

### User-Level Config

`codex mcp add` writes user-level MCP config by default:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
startup_timeout_sec = 20
tool_timeout_sec = 60
```

### Project-Level Config

For a project-specific MCP server, create `.codex/config.toml` in a trusted
project:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
startup_timeout_sec = 20
tool_timeout_sec = 60
```

Project-level config is useful when a server exposes data specific to one
codebase, such as a local database schema or internal docs.

### Remote HTTP Servers

Some MCP servers use HTTP instead of a local process:

```toml
[mcp_servers.context7_remote]
url = "https://mcp.context7.com/mcp"
startup_timeout_sec = 20
tool_timeout_sec = 60
```

If a bearer token is required:

```toml
[mcp_servers.example_remote]
url = "https://example.com/mcp"
bearer_token_env_var = "EXAMPLE_MCP_TOKEN"
```

OAuth-capable MCP servers can be authenticated with:

```bash
codex mcp login server-name
```

## Optional: Add OpenAI Docs MCP

```bash
codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp
```

Use it when working with Codex, the OpenAI API, ChatGPT Apps SDK, or other
OpenAI developer products.

## Success Criteria

- [ ] `context7` appears in `codex mcp list`
- [ ] `/mcp` shows the server in an interactive session
- [ ] Codex can resolve a library name to a Context7 ID
- [ ] Codex can fetch documentation before generating code
- [ ] You used current docs in at least one exercise prompt

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server fails to start | Check that `npx` is on your `PATH` and Node.js 18+ is installed |
| Tools do not appear | Restart Codex after adding the server |
| Tool call times out | Check network access and increase `tool_timeout_sec` |
| Auth fails | Use environment variables or `codex mcp login` for supported servers |

## Advanced Challenges

1. Add a second MCP server, such as GitHub or PostgreSQL.
2. Add a project-scoped MCP config for one exercise.
3. Add an `AGENTS.md` note telling Codex when to use current docs before coding.
