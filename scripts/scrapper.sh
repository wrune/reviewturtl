#!/bin/bash

# Script to fetch PR diffs and comments using GitHub CLI

# GitHub repository and PR number
REPO="quickwit-inc/quickwit"
PR_NUMBER=5208
OUTPUT_BASE_DIR="data"  # Base output directory
OUTPUT_DIR="$OUTPUT_BASE_DIR/${REPO//\//_}/pr_$PR_NUMBER"  # Output directory with REPO and PR number

# Check if jq is installed
if ! command -v jq &> /dev/null
then
    echo "jq could not be found. Please install jq to proceed."
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Fetch PR diff
echo "Fetching PR diff..."
gh pr diff $PR_NUMBER --repo $REPO > $OUTPUT_DIR/pr_diff.diff

if [ $? -ne 0 ]; then
    echo "Failed to fetch PR diff."
    exit 1
fi

# Fetch PR comments
echo "Fetching PR comments..."
gh pr view $PR_NUMBER --repo $REPO --json comments | jq '.comments' > $OUTPUT_DIR/pr_comments.json

if [ $? -ne 0 ]; then
    echo "Failed to fetch PR comments."
    exit 1
fi

echo "PR diff and comments have been fetched and saved to $OUTPUT_DIR/pr_diff.diff and $OUTPUT_DIR/pr_comments.json respectively."
