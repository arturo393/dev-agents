#!/bin/bash

# Jira Sync Script
# Loads credentials from .env and syncs with Jira using mcp-atlassian-jira

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
ENV_FILE="$PROJECT_ROOT/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env file not found at $ENV_FILE"
    echo "Please create a .env file with JIRA_URL, JIRA_USERNAME, JIRA_API_TOKEN, and JIRA_PROJECT_KEY"
    exit 1
fi

# Load environment variables
export $(grep -v '^#' "$ENV_FILE" | xargs)

# Map to mcp-atlassian-jira expected vars
export ATLASSIAN_SITE_NAME=$(echo "$JIRA_PERSONAL_URL" | sed 's|https://||' | sed 's|.atlassian.net||')
export ATLASSIAN_USER_EMAIL="$JIRA_PERSONAL_EMAIL"
export ATLASSIAN_API_TOKEN="$JIRA_PERSONAL_API_TOKEN"

if [ -z "$JIRA_PERSONAL_URL" ] || [ -z "$JIRA_PERSONAL_EMAIL" ] || [ -z "$JIRA_PERSONAL_API_TOKEN" ] || [ -z "$JIRA_ID_PROJECT" ]; then
    echo "Error: Missing required Jira credentials in .env file"
    echo "Required: JIRA_PERSONAL_URL, JIRA_PERSONAL_EMAIL, JIRA_PERSONAL_API_TOKEN, JIRA_ID_PROJECT"
    exit 1
fi

echo "Syncing with Jira project: $JIRA_ID_PROJECT"

mcp-atlassian-jira --env-file "$ENV_FILE" sync --project "$JIRA_ID_PROJECT"
