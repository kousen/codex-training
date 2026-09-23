# Model Selection Guide

Choose the right model for the task, then adjust reasoning effort, verbosity,
and sandbox settings for the workflow.

---

## Quick Reference

| Model | Best For | Notes |
|-------|----------|-------|
| **GPT-6-Astra / GPT-6-Sol** | Complex coding, research, reviews, broad refactors | GPT-6 frontier models; Codex picks your account's default (check `/model`) |
| **GPT-6-Luna** | Smaller fixes, fast iteration, lighter sub-agent tasks | Lower latency and cost for scoped work |
| **GPT-5.6 (Sol / Terra / Luna) / GPT-5.5** | Everyday professional coding | Previous generations, still available |
| **Local OSS models** | Offline, privacy-sensitive, or zero-API-cost work | Use Ollama or LM Studio with realistic expectations |

---

## Recommended Defaults

### Most Students

```toml
model = "gpt-6-sol"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"
```

### API Key Authentication

The GPT-6 and GPT-5.6 families are available with API-key auth.
Run `codex debug models` to see exactly what your account can use.

```bash
codex --model gpt-6-sol
```

### Fast Scoped Work

Profiles live in per-profile files since 0.134 — `~/.codex/quick.config.toml`
with top-level keys (a `[profiles.quick]` table in `config.toml` makes the CLI
refuse to start):

```toml
# ~/.codex/quick.config.toml
model = "gpt-6-luna"
model_reasoning_effort = "low"
approval_policy = "never"
sandbox_mode = "read-only"
web_search = "disabled"
```

```bash
codex --profile quick "Explain the failing test"
```

### Hard Implementation Work

```toml
# ~/.codex/thorough.config.toml
model = "gpt-6-sol"
model_reasoning_effort = "high"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "live"
```

```bash
codex --profile thorough "Refactor the payment workflow and update tests"
```

---

## Reasoning Effort

Use `model_reasoning_effort` to tune depth without changing the model:

| Effort | Use When |
|--------|----------|
| `low` | Simple fixes, formatting, documentation |
| `medium` | Default coding, tests, moderate refactors |
| `high` | Architecture, security review, difficult debugging |
| `xhigh` | Expensive, complex work where depth matters more than latency |
| `max` | Maximum reasoning depth for the hardest problems |
| `ultra` | Maximum reasoning **plus automatic task delegation** to sub-agents |

(`minimal` still validates but no current model lists it.)

---

## Web Search Mode

| Mode | Use When |
|------|----------|
| `disabled` | Reproducible local work, exams, sensitive environments |
| `cached` | Default. Good for stable docs and general questions |
| `indexed` | Newer index-backed mode — see the config docs for how it differs from `cached` |
| `live` | Current APIs, announcements, prices, policies, or recent bugs |

For one run:

```bash
codex --search "latest Spring Boot validation documentation"
```

---

## Local Models

Local models are useful for privacy-sensitive or offline work, but they are not
drop-in replacements for frontier hosted models on large refactors or subtle
debugging.

```bash
codex --oss --local-provider ollama
```

Example profile:

```toml
# ~/.codex/local.config.toml
model_provider = "ollama"
model = "qwen2.5-coder:32b"
sandbox_mode = "workspace-write"
approval_policy = "on-request"
web_search = "disabled"
```

---

## Task Recommendations

| Task | Recommended Setup |
|------|-------------------|
| Explain code or errors | GPT-6-Luna, low/medium reasoning |
| Fix typos or small lint issues | GPT-6-Luna, read-only first if unsure |
| Add unit tests | GPT-6-Sol medium, or GPT-6-Luna for small scopes |
| Multi-file refactor | GPT-6-Sol, high reasoning |
| Security review | GPT-6-Sol, high reasoning, read-only |
| Architecture design | GPT-6-Sol, high/xhigh reasoning (ultra to delegate) |
| CI automation | GPT-6-Luna, `codex exec`, conservative permissions |
| Current library usage | GPT-6-Sol with MCP docs or live web search |

---

## Decision Flow

```text
Is it a current-docs question?
├─ Yes: use MCP docs or web_search = "live"
└─ No
   Is it small and scoped?
   ├─ Yes: gpt-6-luna
   └─ No
      Is it complex, risky, or architectural?
      ├─ Yes: gpt-6-sol, high reasoning
      └─ No: gpt-6-sol, medium reasoning
```

Pricing, rate limits, and availability change. Check the current OpenAI models
docs before teaching exact cost numbers.
