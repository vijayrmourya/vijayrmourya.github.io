#!/usr/bin/env bash
# Generic commit and push helper for GitHub Actions
# Expects these environment variables (workflow should set them):
# FILES - space-separated list of files to `git add`
# COMMIT_MSG_TEMPLATE - commit message, may contain {COUNT} placeholder
# COUNT_CMD - optional shell command to compute count (stdout used)

set -euo pipefail

: "${FILES:?FILES must be set (space-separated)}"
COMMIT_MSG_TEMPLATE="${COMMIT_MSG_TEMPLATE:-chore: update files [skip ci]}"
COUNT_CMD="${COUNT_CMD:-}"

# Configure git
git config --local user.name "github-actions[bot]"
git config --local user.email "github-actions[bot]@users.noreply.github.com"

# Get current branch
BRANCH=${GITHUB_REF#refs/heads/}

# Add files
# shellcheck disable=SC2086
git add ${FILES}

# Check if there are changes
if git diff --staged --quiet; then
  echo "No changes to commit"
  exit 0
fi

# Compute count if needed
COUNT=""
if [ -n "${COUNT_CMD}" ]; then
  COUNT=$(eval "${COUNT_CMD}" 2>/dev/null || echo "0")
fi

# Replace {COUNT} in message
COMMIT_MSG=${COMMIT_MSG_TEMPLATE//"{COUNT}"/$COUNT}
COMMIT_MSG=${COMMIT_MSG//\{COUNT\}/$COUNT}

# Commit
git commit -m "$COMMIT_MSG"

# Rebase rather than creating a merge commit. If another update touched the same
# generated file, fail safely and leave the branch unchanged for review.
git pull --rebase origin "$BRANCH"
git push origin "$BRANCH"

echo "Changes pushed"

