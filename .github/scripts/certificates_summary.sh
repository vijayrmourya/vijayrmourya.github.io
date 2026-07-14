#!/usr/bin/env bash
# Safely write a certificates summary to $GITHUB_STEP_SUMMARY
# Usage: certificates_summary.sh PATH_TO_CERT_JSON

set -euo pipefail

CERT_FILE="${1:-assets/certificates.json}"
STEP_SUMMARY="${GITHUB_STEP_SUMMARY:-}"

# Compute count safely
if [ -f "$CERT_FILE" ]; then
  COUNT=$(grep -c '"title":' "$CERT_FILE" 2>/dev/null || echo "0")
else
  COUNT=0
fi

# If GITHUB_STEP_SUMMARY is set, append there; otherwise print to stdout
SUMMARY_CONTENT="### 📜 Certificate Generation Summary

- **Total Certificates**: $COUNT
- **Generated**: $(date -u +'%Y-%m-%d %H:%M:%S UTC')
- **Status**: ✅ Complete
"

if [ -n "$STEP_SUMMARY" ]; then
  echo "$SUMMARY_CONTENT" >> "$STEP_SUMMARY"
else
  echo "$SUMMARY_CONTENT"
fi

