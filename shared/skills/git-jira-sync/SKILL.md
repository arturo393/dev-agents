---
name: git-jira-sync
description: "Use when the user asks to create commits, push changes, and synchronize Jira status/comments/worklogs with repository progress across this workspace. Triggers: commit, push, sync jira, worklog, update jira, installer, ID-*."
---

# Git Jira Sync

## Purpose

Provide a standard Copilot workflow for:

1. Reviewing repository status and recent changes.
2. Creating non-interactive commits.
3. Pushing branch updates.
4. Synchronizing Jira issue progress (status, comment, worklog).
5. Recording a trace entry in the sync registry.

## Scope

Workspace scope: all repositories under the current workspace root
Primary area example: products/drs/sw-drsmonitoring/master-installer-v2
Primary issue example: ID-1373

## Required Inputs

1. Jira issue key, for example ID-1373.
2. Target repository path.
3. Commit message (if commit is requested).
4. Optional worklog duration, for example 30m or 1h 15m.
5. Optional Jira comment text.

## Workflow

1. Collect context.
- Run git status and short git log in the requested repo.
- Confirm changed files and branch.
- If workspace has unrelated dirty files, do not revert them.

2. Commit and push.
- Stage only intended files when possible.
- Use non-interactive git commands only.
- Commit with a clear action-oriented message.
- Push to current branch when user requests upload.

3. Read Jira current state.
- Retrieve issue summary, status, parent, updated timestamp, and time tracking.
- Keep a before snapshot in the response.

4. Sync Jira updates.
- Add concise technical comment reflecting what changed in repo.
- Add worklog only for real work completed.
- Transition status only if evidence supports it.

5. Update sync registry.
- Append one line in <repo>/reports/jira_sync_registry.md with:
  - timestamp
  - issue key
  - jira status
  - jira updated
  - jira timespent
  - git branch
  - git head
  - git dirty summary

6. Return a final sync summary.
- What was committed and pushed.
- What was updated in Jira.
- Any blockers or manual steps still needed.

## Safety Rules

1. Never use destructive git commands unless explicitly requested.
2. Never amend commits unless explicitly requested.
3. Never log secrets, tokens, or credentials in comments or registry.
4. Do not fabricate worklogs.
5. Keep Jira comments concise and evidence-based.

## Output Template

Use this structure in final response:

1. Git: branch, commit(s), push result.
2. Jira: status before and after, comment/worklog actions.
3. Registry: file updated and latest row summary.
4. Pending: next action if anything remains.
