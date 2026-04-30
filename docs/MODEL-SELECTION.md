# Model Selection Guide

Choose the right model for the task, then adjust reasoning effort, verbosity,
and sandbox settings for the workflow.

---

## Quick Reference

| Model | Best For | Notes |
|-------|----------|-------|
| **GPT-5.5** | Complex coding, research, reviews, broad refactors | Start here when it appears in the Codex model picker |
| **GPT-5.4** | Everyday professional coding and hard implementation work | Use this if GPT-5.5 is not available or you authenticate with an API key |
| **GPT-5.4-mini** | Smaller fixes, fast iteration, lighter sub-agent tasks | Lower latency and cost for scoped work |
| **GPT-5.3-Codex** | Codex-tuned coding workflows and Codex Cloud compatibility | Still useful where explicitly available |
| **GPT-5.3-Codex-Spark** | Research-preview coding workflows | Availability depends on plan and surface |
| **Local OSS models** | Offline, privacy-sensitive, or zero-API-cost work | Use Ollama or LM Studio with realistic expectations |

---

## Recommended Defaults

### Most Students

```toml
model = "gpt-5.5"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
web_search = "cached"
```

If `gpt-5.5` is not available, use:

```toml
model = "gpt-5.4"
```

### API Key Authentication

GPT-5.5 availability is tied to ChatGPT authentication in Codex. If you are
using API-key auth, use GPT-5.4 unless your model picker shows otherwise.

```bash
codex --model gpt-5.4
```

### Fast Scoped Work

```toml
[profiles.quick]
model = "gpt-5.4-mini"
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
[profiles.thorough]
model = "gpt-5.5"
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
| `minimal` | Very small edits, quick explanations |
| `low` | Simple fixes, formatting, documentation |
| `medium` | Default coding, tests, moderate refactors |
| `high` | Architecture, security review, difficult debugging |
| `xhigh` | Expensive, complex work where depth matters more than latency |

---

## Web Search Mode

| Mode | Use When |
|------|----------|
| `disabled` | Reproducible local work, exams, sensitive environments |
| `cached` | Default. Good for stable docs and general questions |
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
[profiles.local]
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
| Explain code or errors | GPT-5.4-mini, low/medium reasoning |
| Fix typos or small lint issues | GPT-5.4-mini, read-only first if unsure |
| Add unit tests | GPT-5.4 or GPT-5.4-mini depending on scope |
| Multi-file refactor | GPT-5.5 or GPT-5.4, high reasoning |
| Security review | GPT-5.5 or GPT-5.4, high reasoning, read-only |
| Architecture design | GPT-5.5, high or xhigh reasoning |
| CI automation | GPT-5.4-mini or GPT-5.4, `codex exec`, conservative permissions |
| Current library usage | GPT-5.4 or GPT-5.5 with MCP docs or live web search |

---

## Decision Flow

```text
Is it a current-docs question?
├─ Yes: use MCP docs or web_search = "live"
└─ No
   Is it small and scoped?
   ├─ Yes: gpt-5.4-mini
   └─ No
      Is it complex, risky, or architectural?
      ├─ Yes: gpt-5.5, high reasoning
      └─ No: gpt-5.4, medium reasoning
```

Pricing, rate limits, and availability change. Check the current OpenAI models
docs before teaching exact cost numbers.
