# GitHub Actions Workflows

Example workflows demonstrating Codex in CI/CD pipelines.

## Available Workflows

### `codex-review.yml`

Automated code review on pull requests using Codex.

**Features:**
- Triggers on PR open/update
- Reviews only changed code files
- Posts review as PR comment
- Uses cost-effective mini model

**Setup:**

1. Add your OpenAI API key as a repository secret:
   - Go to Settings → Secrets → Actions
   - Add `OPENAI_API_KEY`

2. Enable workflow:
   - Copy `.github/workflows/codex-review.yml` to your repo
   - Adjust file patterns as needed

**Customization:**

```yaml
# Change which files trigger review
paths:
  - '**.java'
  - '**.py'
  # Add your extensions

# Use different model
--model gpt-5.4        # More thorough
--model gpt-5.4-mini   # Faster, cheaper
```

## Security Notes

- Never commit API keys to the repository
- Use GitHub Secrets for all credentials
- Prefer `--sandbox read-only --ask-for-approval never` for review-only CI tasks
- Review generated comments before merging
