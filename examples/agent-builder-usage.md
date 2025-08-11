# Agent-Builder Usage Examples

## Basic Agent Creation

### Example 1: Create a Simple Log Analyzer
```bash
@agent-builder create a log analyzer

# Agent-builder will interview you:
# Q: What is the primary purpose?
# A: Analyze log files for errors and patterns

# Q: What domain/area?  
# A: Debugging and monitoring

# Q: What workflows will it perform?
# A: Read logs → find errors → extract patterns → generate report

# Q: What should trigger activation?
# A: "analyze logs", "check errors", "log investigation"

# Result: Creates optimized agent in .claude/agents/log-analyzer.md
```

### Example 2: Create a Database Specialist
```bash
@agent-builder create database optimization specialist

# Interview process...
# Result: Yellow-tier agent with Read, Bash, Grep tools
```

## Batch Creation

### Team Standardization
```bash
@agent-builder create batch agents for frontend team

# Agent-builder will:
# 1. Ask about team's common tasks
# 2. Generate multiple related agents
# 3. Apply consistent naming and patterns
# 4. Deploy all agents at once
```

## Agent Optimization

### Optimize Existing Agent
```bash
@agent-builder optimize existing-agent.md

# Agent-builder will:
# 1. Analyze current configuration
# 2. Apply 400-char compression
# 3. Optimize tool permissions
# 4. Validate and redeploy
```

## Template Usage

### Using Specific Templates
```bash
@agent-builder create from template green/simple-reader

# Customizes the simple-reader template for your needs
```

### Creating Custom Templates
```bash
@agent-builder create template for API testing

# Creates reusable template in templates/custom/
```

## Advanced Features

### Validation Only
```bash
@agent-builder validate my-agent.md

# Checks:
# - YAML syntax
# - Character count
# - Tool permissions
# - Activation patterns
```

### Performance Testing
```bash
@agent-builder test performance of my-agent

# Measures:
# - Initialization time
# - Token usage
# - Response latency
```

## Common Patterns

### Green Tier (Simple)
- Single tool agents
- Direct execution
- <200 characters
- Example: config-reader, log-scanner

### Yellow Tier (Standard)
- Multiple tools (3-6)
- Multi-step workflows
- <300 characters
- Example: debugger, test-runner

### Red Tier (Complex)
- Many tools (6+)
- Orchestration capabilities
- <400 characters
- Example: orchestrator, architect

## Tips for Success

1. **Keep It Focused**: Single responsibility agents perform better
2. **Use Keywords**: Include specific trigger words in descriptions
3. **Minimize Tools**: Only grant necessary tools
4. **Test Early**: Validate agents before deployment
5. **Iterate**: Use optimization feature to improve existing agents

## Troubleshooting

### Agent Not Activating
- Check description includes trigger keywords
- Add "use proactively" to description
- Verify agent file is in correct directory

### Character Limit Exceeded
- Use arrow notation (→) for workflows
- Abbreviate common terms
- Remove unnecessary words
- Use symbols from optimization patterns

### Tool Permission Issues
- Check tool names are correct
- Verify MCP tools use full format
- Ensure tools exist in environment

## Integration with Install Script

```bash
# After creating agents, install them to projects:
./install-agents /path/to/project agent-builder

# Or add to a profile for team distribution:
echo "agent-builder" >> profiles/development-team.txt
```