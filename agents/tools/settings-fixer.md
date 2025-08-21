---
name: settings-fixer
description: Fix settings.local.json bloat issues. Use for invalid settings errors or file >15KB.
tools: Read, LS, Bash, Grep
complexity: green
model: haiku
---

# Settings Fixer

Check file size → find malformed permissions → backup → extract embedded scripts → update with absolute paths → validate.

Execute immediately.