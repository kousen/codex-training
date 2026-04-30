# Lab 0: Planning, Steering, and Permissions Warm-Up

## Objective

Get comfortable with the Codex interaction loop before the larger coding labs.
You will ask Codex to plan before editing, steer an in-flight task, inspect
permissions, and verify the resulting code.

**Time:** 15-20 minutes

## Setup

```bash
cd exercises/plan-mode-warmup/starter
```

Verify Python and pytest are available:

```bash
python --version   # 3.9+
pip install pytest # if not already installed
```

## Part 1: Ask for a Plan

Start Codex:

```bash
codex
```

Paste this prompt:

```text
Fix the bugs in inventory.py. Make a brief plan first, then wait for
my approval before editing. The remove_item function crashes when the
item doesn't exist, and apply_discount treats the percent parameter
incorrectly.
```

Before approving the plan, check:

- Does it address both bugs?
- Does it mention the right files?
- Does it include verification?
- Is the scope small enough for this lab?

Approve the plan, or reply with a correction before Codex edits.

## Part 2: Verify the Fix

Run this quick smoke test:

```bash
python -c "
from inventory import remove_item, apply_discount, add_item
inv = {}
add_item(inv, 'Widget', 10, 100.0)

try:
    remove_item(inv, 'NonExistent')
    print('remove_item: FIXED')
except KeyError:
    print('remove_item: STILL BROKEN')

apply_discount(inv, 'Widget', 50)
expected = 50.0
actual = inv['Widget']['price']
print(f'apply_discount: price={actual} expected={expected} result={actual == expected}')
"
```

## Part 3: Steer a Running Task

Ask Codex for a larger follow-up:

```text
Add comprehensive tests to test_inventory.py. Cover all functions
including remove_item, apply_discount, and restock. Include edge
cases like empty inventory and negative quantities.
```

While Codex is working, send a follow-up:

```text
Also add a test for generate_report with an empty inventory.
```

Observe how Codex incorporates the new guidance into the current task or the
next step in the conversation.

Run the tests:

```bash
pytest -v
```

If any test fails, ask Codex to diagnose and fix the failure.

## Part 4: Inspect the Session

Try these slash commands inside Codex:

| Command | Use |
|---------|-----|
| `/status` | Inspect model, session, and usage details |
| `/permissions` | View or adjust sandbox and approval settings |
| `/diff` | Review pending file changes |
| `/model` | Inspect or switch the active model |
| `/fast` | Toggle faster output when available |
| `/review` | Ask Codex to review the diff before you accept it |
| `/mcp` | Inspect configured MCP servers |
| `/skills` | Inspect available skills |
| `/help` | See the commands available in your installed version |

The exact command list can vary by Codex surface and installation. Use `/help`
as the source of truth in the live session.

## Part 5: Permissions Practice

Run `/permissions` and check the current sandbox and approval policy.

Recommended training setup:

```text
sandbox: workspace-write
approval: on-request
```

For review-only work, switch to read-only:

```bash
codex --sandbox read-only
```

For unattended automation, prefer a narrow task with conservative permissions:

```bash
codex exec "Review the uncommitted diff for bugs; do not edit files" \
  --sandbox read-only \
  --ask-for-approval never
```

## Success Criteria

- [ ] You asked Codex to propose a plan before editing
- [ ] You approved or corrected the plan
- [ ] You steered a running task with a follow-up message
- [ ] You inspected permissions and reviewed the diff
- [ ] `pytest -v` passes
- [ ] Both bugs in `inventory.py` are fixed

## Key Takeaways

1. Ask for a plan when scope, risk, or file ownership matters.
2. Use `/diff` and `/review` before accepting changes.
3. Keep sandbox and approval settings aligned with the task.
4. Verify with tests before moving on to the next lab.
