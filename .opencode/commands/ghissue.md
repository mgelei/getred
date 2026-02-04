---
description: Fetch a GitHub issue and generate detailed implementation plan
agent: plan
---

Issue details JSON:
!`gh issue view $1 --json title,body,url,labels,milestone,assignees,state,createdAt,updatedAt,comments`

Parse this JSON and create a detailed implementation plan for the GitHub issue.

Follow AGENTS.md guidelines strictly: Python 3.12+, PEP8, snake_case, minimal deps, pytest, conventional commits.

**Plan Structure:**
- Use the explore agent to analyze codebase relevance.
- Use todowrite for implementation steps: research, design, code changes, tests, lint/typecheck.
- Verify with pytest; suggest PR with version bump if needed.
- Prioritize deterministic tests, no live API calls..
