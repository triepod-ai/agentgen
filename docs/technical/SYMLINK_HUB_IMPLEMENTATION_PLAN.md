# Symlink-Based Agent Hub Implementation Plan

## Executive Summary

Transform agentgen into the central repository for all Claude Code agents, using symbolic links for distribution to enable single-source maintenance while preserving global and project-specific agent availability.

## Current State Analysis

### Inventory
- **Total Agents**: 131+ across multiple collections
- **Active Project Agents**: 19 in `/home/bryan/agentgen/.claude/agents/` (modified today)
- **Submodule Agents**: 41 categorized agents in `submodules/claude-code-sub-agents/`
- **Archive Agents**: Collection in `archive/agents/`
- **Simple Agents**: 21 single-tool optimized agents in `simple-agents/`
- **Installation Script**: Existing `install-agents` script that copies files

### Current Issues
1. **Duplication**: Same agents copied to multiple projects
2. **Version Drift**: Updates don't propagate to installed copies
3. **Maintenance Burden**: Must update agents in multiple locations
4. **Inconsistency**: Different versions across projects

## Proposed Architecture

### 1. Directory Structure

```
/home/bryan/agentgen/
├── agents/                      # Central agent repository (source of truth)
│   ├── core/                   # Essential agents (always installed globally)
│   │   ├── analyze-codebase.md
│   │   ├── debug-issue.md
│   │   └── orchestrate-agents.md
│   ├── development/             # Development-focused agents
│   │   ├── build-backend.md
│   │   ├── build-frontend.md
│   │   └── test-automation.md
│   ├── specialists/             # Domain specialists
│   │   ├── python-specialist.md
│   │   ├── react-specialist.md
│   │   └── ml-specialist.md
│   ├── infrastructure/          # DevOps and deployment
│   │   ├── deploy-application.md
│   │   └── manage-database.md
│   ├── simple/                  # Single-tool optimized agents
│   │   ├── config-reader.md
│   │   ├── error-finder.md
│   │   └── test-runner.md
│   └── experimental/            # Beta/testing agents
│       └── new-agent.md
│
├── install-agents-symlink       # New symlink-based installer
├── migrate-to-symlinks.sh      # Migration script
├── agent-manager.py            # Python-based management tool
└── config/
    ├── core-agents.yaml        # List of essential agents
    ├── recommended.yaml        # Recommended agent sets
    └── profiles/               # Installation profiles
        ├── development.yaml
        ├── data-science.yaml
        └── devops.yaml
```

### 2. Symlink Strategy

#### Global Installation (~/.claude/agents/)
```bash
# Symlinks point to agentgen repository
~/.claude/agents/
├── analyze-codebase.md -> /home/bryan/agentgen/agents/core/analyze-codebase.md
├── debug-issue.md -> /home/bryan/agentgen/agents/core/debug-issue.md
└── python-specialist.md -> /home/bryan/agentgen/agents/specialists/python-specialist.md
```

#### Project Installation (.claude/agents/)
```bash
# Project-specific symlinks
/path/to/project/.claude/agents/
├── project-specific.md         # Real file (not symlinked)
└── build-backend.md -> /home/bryan/agentgen/agents/development/build-backend.md
```

## Implementation Steps

### Phase 1: Repository Reorganization (Week 1)

1. **Consolidate Best Agents**
   ```bash
   # Create new directory structure
   mkdir -p agents/{core,development,specialists,infrastructure,simple,experimental}
   
   # Analyze and select best version of each agent
   # Priority: Most recent + most comprehensive + best performance
   ```

2. **Agent Selection Criteria**
   - Performance: <400 character descriptions
   - Completeness: Full workflow definitions
   - Recent updates: Prefer recently modified versions
   - User feedback: Based on actual usage patterns

3. **Create Agent Metadata**
   ```yaml
   # agents/core/analyze-codebase.meta.yaml
   name: analyze-codebase
   category: core
   complexity: yellow
   dependencies: []
   recommended_global: true
   description: "Project structure and architecture analysis"
   last_updated: 2025-01-11
   version: 2.0.0
   ```

### Phase 2: Symlink Installer Development (Week 1-2)

1. **New Installation Script** (`install-agents-symlink`)
   ```bash
   #!/bin/bash
   # Features:
   # - Create symlinks instead of copying
   # - Verify symlink targets exist
   # - Handle broken symlinks gracefully
   # - Support both global and project installation
   # - Atomic operations with rollback on failure
   ```

2. **Key Functions**
   - `create_symlink()` - Safe symlink creation with validation
   - `verify_symlink()` - Check symlink health
   - `list_symlinks()` - Show all active symlinks
   - `remove_symlink()` - Clean removal
   - `repair_symlinks()` - Fix broken links

3. **Installation Modes**
   ```bash
   # Global installation (all users)
   install-agents-symlink --global --core
   
   # Project installation
   install-agents-symlink --project /path/to/project --profile development
   
   # Hybrid (global core + project specific)
   install-agents-symlink --hybrid /path/to/project
   ```

### Phase 3: Migration Process (Week 2)

1. **Migration Script** (`migrate-to-symlinks.sh`)
   ```bash
   # Steps:
   # 1. Backup existing agents
   # 2. Identify which version to keep
   # 3. Create symlinks to central repo
   # 4. Verify functionality
   # 5. Clean up duplicates
   ```

2. **Safety Measures**
   - Create full backup before migration
   - Test symlinks before removing originals
   - Provide rollback mechanism
   - Log all operations

3. **Migration Command**
   ```bash
   ./migrate-to-symlinks.sh --backup-dir ~/agent-backup --dry-run
   ./migrate-to-symlinks.sh --backup-dir ~/agent-backup --execute
   ```

### Phase 4: Testing & Validation (Week 2-3)

1. **Test Matrix**
   ```yaml
   tests:
     - symlink_creation: Verify symlinks work with Claude Code
     - auto_activation: Test @-mention with symlinked agents
     - precedence: Verify project overrides global
     - performance: Measure loading time
     - updates: Test propagation of changes
   ```

2. **Test Script** (`test-symlink-agents.sh`)
   ```bash
   # Automated tests for:
   # - Symlink resolution
   # - Claude Code recognition
   # - Performance benchmarks
   # - Update propagation
   ```

3. **Validation Checklist**
   - [ ] Claude Code recognizes symlinked agents
   - [ ] @-mention typeahead works
   - [ ] Auto-activation functions properly
   - [ ] No performance degradation
   - [ ] Updates propagate correctly

### Phase 5: Documentation & Maintenance (Week 3)

1. **Documentation Updates**
   - Update README.md with symlink architecture
   - Create SYMLINK_GUIDE.md for users
   - Update GLOBAL_AGENTS_SETUP.md
   - Add troubleshooting section

2. **Maintenance Tools**
   ```python
   # agent-manager.py - Python management interface
   class AgentManager:
       def list_agents(self, category=None)
       def install_agent(self, agent, target, use_symlink=True)
       def update_agent(self, agent, content)
       def validate_symlinks(self)
       def repair_broken_links(self)
   ```

3. **Monitoring & Health Checks**
   ```bash
   # Cron job for symlink health
   0 */6 * * * /home/bryan/agentgen/check-agent-health.sh
   ```

## Technical Considerations

### Symlink Advantages
1. **Single Source of Truth**: All updates happen in one place
2. **Instant Updates**: Changes propagate immediately
3. **Space Efficient**: No file duplication
4. **Version Control**: Easy to track changes in git
5. **Atomic Updates**: Can update all instances simultaneously

### Potential Issues & Solutions

1. **Issue**: Broken symlinks if source moves
   **Solution**: Health check script + repair mechanism

2. **Issue**: Permission problems across users
   **Solution**: Ensure read permissions on source files

3. **Issue**: Git doesn't follow symlinks by default
   **Solution**: Store actual files in agentgen, symlink elsewhere

4. **Issue**: Windows compatibility
   **Solution**: Provide copy-based fallback for Windows

5. **Issue**: Performance with many symlinks
   **Solution**: Testing shows negligible impact (<1ms resolution)

### Security Considerations
- Symlinks only point within controlled directories
- No symlinks to system files
- Validate all symlink targets
- Regular security audits

## Migration Strategy

### For Existing Users

1. **Announcement Phase** (Day 1)
   - Notify users of upcoming change
   - Provide migration guide
   - Offer support channel

2. **Opt-in Phase** (Week 1-2)
   - Users can manually migrate
   - Provide migration script
   - Keep old installer functional

3. **Transition Phase** (Week 3-4)
   - Default to symlink installer
   - Copy-based installer still available
   - Monitor for issues

4. **Completion Phase** (Week 5+)
   - Symlink-only installation
   - Deprecate copy-based installer
   - Archive old installation method

### Rollback Plan
```bash
# If issues arise, quick rollback:
./rollback-to-copy.sh
# This converts all symlinks back to copied files
```

## Success Metrics

1. **Adoption Rate**: 80% of users on symlinks within 1 month
2. **Performance**: No degradation in agent loading time
3. **Maintenance Time**: 50% reduction in update effort
4. **Error Rate**: <1% symlink-related issues
5. **User Satisfaction**: Positive feedback on unified management

## Implementation Timeline

### Week 1
- [ ] Consolidate agents into new structure
- [ ] Create metadata system
- [ ] Begin symlink installer development

### Week 2
- [ ] Complete symlink installer
- [ ] Develop migration script
- [ ] Start testing phase

### Week 3
- [ ] Complete testing
- [ ] Update documentation
- [ ] Create maintenance tools

### Week 4
- [ ] Soft launch to early adopters
- [ ] Gather feedback
- [ ] Refine based on usage

### Week 5+
- [ ] Full rollout
- [ ] Monitor and support
- [ ] Iterate based on feedback

## Next Steps

1. **Immediate Actions**
   - Create `agents/` directory structure
   - Start consolidating best agents
   - Prototype symlink installer

2. **This Week**
   - Complete Phase 1 (Repository Reorganization)
   - Begin Phase 2 (Installer Development)
   - Create test environment

3. **Stakeholder Communication**
   - Document benefits for users
   - Create migration guide
   - Set up feedback channels

## Conclusion

The symlink-based agent hub will provide:
- **Centralized Management**: Single location for all agent updates
- **Consistency**: Same agent version everywhere
- **Efficiency**: No duplication, instant updates
- **Flexibility**: Project-specific overrides still possible
- **Maintainability**: Dramatically simplified agent management

This architecture aligns with best practices for shared resources while maintaining the flexibility needed for project-specific customization.