# Lesson-Learned Agents - Deployment Guide

**Version**: 1.0  
**Date**: 2025-07-28  
**Status**: ✅ Production Ready  

## Quick Start

All 6 lesson-learned agents are immediately ready for production use. They will auto-activate based on trigger phrases in user input.

### Trigger Phrases for Each Agent

| Agent | Trigger Phrases | Example Usage |
|-------|----------------|---------------|
| **redis-conversation-store** | "store conversation", "save to redis", "cache session" | "Store this conversation in Redis for later" |
| **lesson-complexity-analyzer** | "analyze complexity", "complexity analysis", "difficulty level" | "Analyze the complexity of this code explanation" |
| **redis-cache-manager** | "cache this", "store in redis cache", "manage cache" | "Cache this analysis result for quick access" |
| **lesson-generator** | "generate lesson", "create lesson file", "lesson from session" | "Generate a lesson from the latest Redis session" |
| **file-size-optimizer** | "optimize storage", "check file size", "storage strategy" | "Check this file size and recommend storage method" |
| **mcp-parallel-store** | "store everywhere", "parallel save", "save to multiple" | "Store this lesson in both Chroma and Qdrant" |

---

## System Requirements

### ✅ **MCP Servers (Required)**
```bash
# Verify MCP servers are available
mcp__redis__store_memory          # Redis operations
mcp__chroma__chroma_add_documents  # Chroma vector storage
mcp__qdrant__qdrant_store         # Qdrant vector storage  
mcp__manus__code_interpreter      # Python analysis
```

### ✅ **Dependencies**
- **Redis Server**: Running on localhost:6379
- **Python 3**: For lesson generation utility
- **generate_lesson.py**: Located at `/home/bryan/.claude/commands/lib/generate-lesson/`

---

## Installation Status

### ✅ **Agents Installed**
All agents are located in `/home/bryan/.claude/agents/`:
- redis-conversation-store.md
- lesson-complexity-analyzer.md  
- redis-cache-manager.md
- lesson-generator.md
- file-size-optimizer.md
- mcp-parallel-store.md

### ✅ **Auto-Discovery Active**
Agents are automatically discovered by Claude Code and will activate based on trigger phrases. No manual registration required.

---

## Usage Examples

### 📝 **Basic Lesson Creation Workflow**

```bash
# 1. Store a conversation
"Store this debugging session in Redis"

# 2. Generate a lesson
"Generate a lesson from the latest session"

# 3. Analyze complexity  
"Analyze the complexity of this generated lesson"

# 4. Optimize storage
"Check this lesson file size and recommend storage"

# 5. Store in multiple systems
"Store this lesson in both Chroma and Qdrant"
```

### 🔄 **Multi-Agent Orchestration**

Use the `/spawn` command for complex workflows:
```bash
/spawn "Create a comprehensive lesson from the current conversation, analyze its complexity, and store it in all available systems"
```

### 🎯 **Direct Agent Usage**

Reference agents directly in `/spawn`:
```bash
/spawn @.claude/agents/lesson-generator.md "Generate lesson from session 12345"
```

---

## Configuration

### 🔧 **Redis TTL Settings**

Agents use intelligent TTL management:
- **Templates**: 24 hours (86400s)
- **Analysis**: 1 hour (3600s)  
- **Generated**: 30 minutes (1800s)
- **Session**: 2 hours (7200s)
- **Project**: 7 days (604800s)

### 🗂️ **Redis Key Structure**

Agents create project-isolated keys:
```
lessons:conversation:{project}:{session_id}
lessons:analysis:{project}:{timestamp}
lessons:templates:{project}:{date}
lessons:generated:{project}:{unique_id}
lessons:cache:{project}:{cache_type}
```

### 📁 **File Storage**

Generated lessons are saved as:
```
lessons_learned_{session_id}.md
```

---

## Monitoring & Maintenance

### 📊 **Performance Monitoring**

**Expected Performance**:
- Individual agent execution: <3 seconds
- Full workflow execution: <10 seconds  
- Success rate: 100% (under normal conditions)
- Token usage: <25K tokens for complete workflow

### 🔍 **Health Checks**

Regular checks to perform:
```bash
# Check Redis connectivity
redis-cli ping

# Verify MCP servers
mcp__redis__store_memory --test
mcp__chroma__chroma_list_collections
mcp__qdrant__qdrant_list_collections

# Check utility availability
ls -la /home/bryan/.claude/commands/lib/generate-lesson/generate_lesson.py
```

### 🚨 **Troubleshooting**

Common issues and solutions:

| Issue | Solution |
|-------|----------|
| Agent not triggering | Check trigger phrase matches agent description |
| Redis connection error | Start Redis: `sudo service redis-server start` |
| MCP tool not found | Verify MCP server is running and configured |
| Lesson generation fails | Check `generate_lesson.py` permissions and Redis data |
| File size analysis error | Verify file exists and is readable |

---

## Integration Patterns

### 🔗 **With SuperClaude Framework**

Agents integrate with:
- **Command System**: Trigger via `/build`, `/analyze`, `/improve` commands
- **Persona System**: Auto-activate with appropriate personas
- **Wave Mode**: Support multi-wave orchestration for complex lessons
- **MCP Coordination**: Seamless integration with all MCP servers

### 🎨 **Custom Workflows**

Create custom workflows by combining agents:

```bash
# Educational content creation
"Store this technical explanation, analyze its complexity, generate a structured lesson, and save it everywhere"

# Session analysis
"Cache this conversation, analyze complexity, and generate insights for future reference"

# Knowledge management  
"Store this solution in Redis, generate a lesson, optimize storage, and save to knowledge base"
```

---

## Security Considerations

### 🔒 **Data Protection**
- **Project Isolation**: All Redis keys are project-scoped
- **TTL Management**: Automatic expiration prevents data accumulation
- **No Secrets**: Agents don't store or expose sensitive information
- **Proper Permissions**: File operations use appropriate access controls

### 🛡️ **Best Practices**
- Don't store sensitive data in lessons
- Review generated content before sharing
- Monitor Redis storage usage
- Use appropriate TTL settings for your use case

---

## Support & Updates

### 📞 **Getting Help**
- Check the `/home/bryan/.claude/agents/FINAL_AGENT_TESTING_REPORT.md` for detailed testing results
- Review individual agent files for specific documentation
- Use Claude Code's built-in help system

### 🔄 **Future Updates**
Agents are designed for easy maintenance:
- Update agent descriptions to modify trigger phrases
- Modify TTL settings in redis-cache-manager
- Extend functionality by adding new tools to agent frontmatter
- Create new agents following the same pattern

---

## Conclusion

✅ **The lesson-learned agent ecosystem is production-ready and immediately available for use.**

All agents have been thoroughly tested, validated, and optimized for the Claude Code SuperClaude framework. They provide a comprehensive solution for capturing, analyzing, and storing technical knowledge from conversations and debugging sessions.

**Start using immediately** - Just use the trigger phrases in normal conversation and the agents will activate automatically!

---

*Deployment guide prepared by Claude Code SuperClaude framework*  
*Last updated: 2025-07-28*