---
name: Jira Sync
description: Syncs with Jira using mcp-atlassian-jira command and .env file for credentials.
---

# Jira Sync Skill

This skill syncs project tasks and issues with Jira using the `mcp-atlassian-jira` CLI tool with credentials loaded from `.env` file.

## Prerequisites

- `mcp-atlassian-jira` command installed and available in PATH
- `.env` file with Jira credentials in the project root

## Environment Variables

The project `.env` file should contain:

```env
JIRA_PERSONAL_URL=https://safetymind-team-ogsoj2pu.atlassian.net
JIRA_PERSONAL_EMAIL=your-email@domain.com
JIRA_PERSONAL_API_TOKEN=your-api-token
JIRA_ID_PROJECT=YOUR_PROJECT
```

## Usage

### Sync Issues from Jira

```bash
mcp-atlassian-jira --env-file .env sync --project $JIRA_PROJECT_KEY
```

### List Jira Issues

```bash
mcp-atlassian-jira --env-file .env list --project $JIRA_PROJECT_KEY --status "In Progress"
```

### Create Jira Issue

```bash
mcp-atlassian-jira --env-file .env create \
  --project $JIRA_PROJECT_KEY \
  --type Task \
  --title "Issue title" \
  --description "Issue description"
```

### Update Jira Issue

```bash
mcp-atlassian-jira --env-file .env update \
  --issue PROJECT-123 \
  --status "Done" \
  --comment "Completed via sync"
```

## Integration with Agents

To use this skill within an agent, source the credentials and execute:

```bash
source .env && mcp-atlassian-jira sync --project $JIRA_PROJECT_KEY
```
