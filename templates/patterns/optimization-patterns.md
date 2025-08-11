# Agent Optimization Patterns

## Compression Techniques

### Arrow Notation
Replace verbose workflow descriptions with arrows:
- ❌ "First read the file, then analyze it, finally return results"
- ✅ "Read → analyze → return"

### Symbol Shortcuts
- & = and
- | = or
- → = then/leads to
- ⇒ = transforms to
- ∴ = therefore
- ∵ = because

### Essential Words Only
- ❌ "The agent should process and validate the input data"
- ✅ "Process & validate input"

### Action-First Language
- ❌ "This agent is responsible for debugging"
- ✅ "Debug errors"

### Tool Minimization
Only include tools actually needed:
- Read-only agents: Read
- Generation agents: Write
- Analysis agents: Read, Grep, Glob
- Full development: Read, Write, Edit, Bash

### Trigger Keywords
Include specific activation words:
- "Use for [specific triggers]"
- "Auto-activates on [keywords]"
- "Use proactively for [scenarios]"

## Character Count Guidelines

### Under 200 chars (Ultra-Simple)
```
Read {{target}} → {{action}} → return.
Execute immediately.
```

### Under 300 chars (Simple with Context)
```
**Role**: {{role}}
{{step1}} → {{step2}} → {{step3}}
Execute workflow immediately.
```

### Under 400 chars (Standard)
```
**Role**: {{role}}
## Workflow
1. {{step1}}
2. {{step2}}
3. {{step3}}
Execute immediately.
```