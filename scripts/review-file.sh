#!/bin/bash
# Example script showing how to use arguments with Codex prompts

# Usage: ./review-file.sh <file> <focus-area>
# Example: ./review-file.sh UserService.java security

FILE=$1
FOCUS=$2

if [ -z "$FILE" ] || [ -z "$FOCUS" ]; then
    echo "Usage: $0 <file> <focus-area>"
    echo "Example: $0 UserService.java security"
    exit 1
fi

# Create temporary prompt with substituted values
cat > /tmp/review-prompt.md << EOF
Review the file ${FILE} focusing on ${FOCUS}:

## Specific checks for ${FOCUS}:
- Identify any ${FOCUS}-related issues
- Check best practices for ${FOCUS}
- Suggest improvements for ${FOCUS}

## General review:
- Check for bugs and errors
- Suggest code improvements
- Rate overall code quality (1-10)

Please provide specific line numbers and code examples for any issues found.
EOF

# Execute the review
echo "Reviewing ${FILE} with focus on ${FOCUS}..."
codex exec "$(cat /tmp/review-prompt.md)"

# Clean up
rm /tmp/review-prompt.md