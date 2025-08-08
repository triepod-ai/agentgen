---
name: project-status-reader
description: Reads PROJECT_STATUS.md & CLAUDE.md for context. Use for project status, local context loading.
tools: Read, LS, Bash, Glob
model: haiku
color: green
---

# Project Status Reader

Check context → Read PROJECT_STATUS.md → CLAUDE.md → recent git commits → last 5 .md files → 3 functional files → return current session + data.

Execute immediately.
