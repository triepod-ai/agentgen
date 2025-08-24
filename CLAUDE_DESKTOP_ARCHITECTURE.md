# AgentGen System Architecture - Claude Desktop Reference

Detailed system architecture, agent categories, and complexity tiers for the AgentGen platform.

## 🏗️ Complete Directory Structure

```
/home/bryan/agentgen/
├── agents/                          # Central agent hub (36+ agents)
│   ├── core/                       # Essential agents (8)
│   │   ├── analyze-codebase.md     # Project analysis
│   │   ├── build-frontend.md       # UI development
│   │   ├── build-backend.md        # API development
│   │   ├── debug-issue.md          # Error resolution
│   │   ├── review-code.md          # Quality assurance
│   │   ├── test-automation.md      # Testing workflows
│   │   ├── deploy-application.md   # Deployment
│   │   └── generate-documentation.md
│   ├── development/                # Development specialists (7)
│   │   ├── frontend-developer.md   # UI/UX specialist
│   │   ├── full-stack-developer.md # Complete development
│   │   ├── nextjs-pro.md          # Next.js expert
│   │   ├── react-pro.md           # React specialist
│   │   ├── ui-designer.md         # Interface design
│   │   ├── ux-designer.md         # User experience
│   │   └── build-runner.md        # Build automation
│   ├── specialists/                # Domain experts (7)
│   │   ├── architect-specialist.md # System architecture
│   │   ├── database-specialist.md  # Database optimization
│   │   ├── ml-specialist.md       # Machine learning
│   │   ├── performance-engineer.md # Performance optimization
│   │   ├── python-specialist.md   # Python expertise
│   │   ├── react-specialist.md    # Advanced React patterns
│   │   └── security-auditor.md    # Security analysis
│   ├── infrastructure/             # DevOps & infrastructure (5)
│   │   ├── cloud-architect-specialist.md
│   │   ├── deployment-engineer.md  # CI/CD pipelines
│   │   ├── data-engineer.md       # Data infrastructure
│   │   ├── manage-database.md     # Database operations
│   │   └── configure-environment.md
│   ├── quality-testing/            # QA & testing (4)
│   │   ├── code-reviewer.md       # Code quality
│   │   ├── debugger.md           # Issue investigation
│   │   ├── qa-expert.md          # Quality assurance
│   │   └── test-automator.md     # Automated testing
│   ├── content-communication/      # Content creation (4)
│   │   ├── api-documenter.md      # API documentation
│   │   ├── documentation-expert.md # Technical writing
│   │   ├── product-manager.md     # Product strategy
│   │   └── create-lesson.md       # Educational content
│   ├── data-ai/                   # Data & ML specialists (4)
│   │   ├── analyze-performance.md  # Performance analysis
│   │   ├── extract-insights.md    # Data insights
│   │   ├── process-data.md        # Data processing
│   │   └── train-model.md         # Model training
│   ├── tools-utilities/           # Utility agents (5)
│   │   ├── analyze-screenshot.md   # Image analysis
│   │   ├── config-reader.md       # Configuration reading
│   │   ├── env-reader.md          # Environment inspection
│   │   ├── log-reader.md          # Log analysis
│   │   └── readme-reader.md       # Documentation reading
│   └── simple/                    # Basic task agents (varies)
├── profiles/                      # Strategic team profiles
│   ├── enterprise-leadership.txt  # 9 strategic decision-makers
│   ├── modern-web-stack.txt      # 12 TypeScript/React specialists
│   ├── startup-mvp.txt           # 11 lean rapid development
│   ├── core.txt                  # 16 essential agents
│   └── development-team.txt      # 32 complete coverage
├── enhanced/                     # ML-enhanced agents
│   ├── security-auditor-enhanced.md
│   ├── react-specialist-enhanced.md
│   ├── performance-engineer-enhanced.md
│   └── architect-specialist-enhanced.md
├── install-agents*               # Primary installer script
├── install-agents-symlink*       # Legacy symlink installer
├── migrate-to-symlinks.sh*       # Migration utility
└── docs/                         # Comprehensive documentation
    ├── technical/                # Technical specifications
    ├── advanced/                 # Advanced features
    ├── getting-started/          # User guides
    └── reference/                # Reference materials
```

## 🎯 Agent Categories & Complexity Tiers

### Complexity-Based Model Selection

| Tier | Model | Token Budget | Response Time | Use Cases |
|------|-------|--------------|---------------|-----------|
| **Green** | claude-3-haiku | 1K-3K | <500ms | Simple operations, quick tasks |
| **Yellow** | claude-3-5-sonnet | 3K-15K | 500ms-2s | Standard development, moderate complexity |
| **Red** | claude-3-5-sonnet-20241022 | 15K+ | 2s+ | Complex reasoning, architecture, security |

### Agent Categories Detail

#### Core Development (8 agents) - Yellow/Red Complexity
- **analyze-codebase**: Project structure analysis, architectural review (Red)
- **analyze-performance**: System optimization, bottleneck identification (Red)  
- **build-frontend**: UI components, React/Vue development (Yellow)
- **build-backend**: APIs, services, database integration (Yellow)
- **debug-issue**: Error investigation, root cause analysis (Yellow)
- **test-automation**: Unit tests, integration tests, coverage (Yellow)
- **review-code**: Quality assessment, security review (Yellow)
- **generate-documentation**: API docs, README files, guides (Yellow)

#### Development Specialists (7 agents) - Yellow Complexity
- **frontend-developer**: UI/UX specialist with accessibility focus
- **full-stack-developer**: End-to-end application development
- **nextjs-pro**: Next.js expert with SSR/SSG optimization
- **react-pro**: Modern React with hooks and performance
- **ui-designer**: Visual design and component systems
- **ux-designer**: User experience and interaction design
- **build-runner**: Build automation and CI/CD integration

#### Specialist Agents (7 agents) - Red Complexity
- **architect-specialist**: System design, microservices, scalability
- **database-specialist**: Complex queries, optimization, sharding
- **ml-specialist**: Machine learning, model architecture
- **performance-engineer**: System optimization, monitoring
- **python-specialist**: Advanced Python patterns, async/await
- **react-specialist**: Advanced React patterns, performance
- **security-auditor**: Vulnerability assessment, compliance

#### Infrastructure & DevOps (5 agents) - Yellow/Red Complexity
- **cloud-architect-specialist**: AWS/Azure/GCP infrastructure (Red)
- **deployment-engineer**: CI/CD pipelines, orchestration (Yellow)
- **data-engineer**: Data pipelines, ETL/ELT systems (Yellow)
- **manage-database**: Database operations and maintenance (Yellow)
- **configure-environment**: Environment setup and management (Yellow)

#### Quality & Testing (4 agents) - Yellow Complexity
- **code-reviewer**: Code quality analysis and recommendations
- **debugger**: Systematic debugging and issue resolution
- **qa-expert**: Quality assurance processes and testing strategy
- **test-automator**: Automated testing framework design

#### Content & Communication (4 agents) - Yellow Complexity
- **api-documenter**: OpenAPI specs, SDK documentation
- **documentation-expert**: Technical writing and guides
- **product-manager**: Product strategy and requirements
- **create-lesson**: Educational content and tutorials

#### Data & AI (4 agents) - Yellow/Red Complexity
- **analyze-performance**: Performance metrics and optimization (Red)
- **extract-insights**: Data analysis and pattern recognition (Yellow)
- **process-data**: ETL pipelines and data transformation (Yellow)
- **train-model**: ML model training and optimization (Red)

#### Tools & Utilities (5 agents) - Green/Yellow Complexity
- **analyze-screenshot**: Image analysis and data extraction (Green)
- **config-reader**: Configuration file inspection (Green)
- **env-reader**: Environment variable analysis (Green)
- **log-reader**: Log file analysis and error detection (Yellow)
- **readme-reader**: Documentation parsing and understanding (Green)

## 🔄 Agent Storage & Precedence System

### Storage Hierarchy
```bash
# Priority order (highest to lowest)
1. PROJECT_AGENTS="{project}/.claude/agents/"     # Project-specific overrides
2. USER_AGENTS="~/.claude/agents/"               # User-wide availability
3. AGENT_HUB="/home/bryan/agentgen/agents/"      # Central reference
```

### Precedence Rules
- **Project agents** override all others (isolated to specific project)
- **Global agents** available across all projects (user-wide)
- **Hub agents** serve as templates and reference (read-only)
- **Name conflicts** resolved by precedence order
- **Symlink mode** provides live updates from hub to installations

### Agent File Format
```yaml
---
name: agent-name                    # Unique identifier (required)
description: When and how to use    # Auto-activation trigger (required)
tools: Read, Write, Edit           # Tool permissions (optional - inherits all if omitted)
model: claude-3-5-sonnet-20241022  # Complexity tier override (optional)
color: blue                        # UI theming (optional)
---

# Agent System Prompt

Detailed instructions defining:
- Agent's role and expertise
- Workflow and methodology  
- Output format and standards
- Quality criteria and constraints

## Workflow
1. Step → Step → Result
2. Execute immediately upon invocation
```

## 🌐 Context-Manager Integration

### Knowledge Graph System
- **Location**: `/sub-agents/context/context-manager.json`
- **Updates**: Real-time project structure mapping
- **Integration**: Automatic with all orchestration agents
- **Benefits**: Eliminates redundant context questions

### Communication Protocol
```json
{
  "requesting_agent": "agent-name",
  "request_type": "get_task_briefing",
  "timestamp": "2025-08-14T12:08:08Z",
  "payload": {
    "query": "Project understanding request",
    "context": "Current operation context"
  }
}
```

## 🚀 Orchestration Architecture

### 4-Tier Orchestration System
1. **@orchestrate-tasks** (Primary) - Intelligent routing with context integration
2. **@orchestrate-agents** (Standard) - 1-3 agent coordination  
3. **@orchestrate-agents-adv** (Enterprise) - 4+ agent complex operations
4. **Direct Coordination** - Specialist-to-specialist communication

### Performance Characteristics
- **Routing Decision**: <100ms for complexity assessment
- **Context Query**: <500ms for project understanding
- **Agent Loading**: <400ms for optimized agents
- **Cross-Agent Communication**: <200ms via JSON protocol
- **Total Orchestration**: <2s for complex multi-agent workflows

## 🔧 Installation Modes

### Symlink Mode (Recommended)
- **Benefits**: Live updates, no duplication, single source of truth
- **Storage**: Symbolic links to central hub
- **Updates**: Instant propagation of agent improvements
- **Management**: Health checks and repair commands
- **Usage**: `./install-agents --symlink --profile [profile] [target]`

### Copy Mode (Traditional)
- **Benefits**: Isolated installations, offline capability
- **Storage**: Independent file copies
- **Updates**: Manual via reinstallation
- **Management**: Version tracking per installation
- **Usage**: `./install-agents --copy --profile [profile] [target]`

### Migration Support
```bash
# Convert existing copy-based installations to symlinks
./migrate-to-symlinks.sh /path/to/target

# Health monitoring for symlink integrity
./install-agents --symlink --health
./install-agents --symlink --repair
```

## 📊 Performance Optimization

### Agent Loading Performance
- **Target**: <400ms initialization time
- **Character Limit**: <400 characters for optimal loading
- **Tool Minimization**: Grant only required tools
- **Prompt Optimization**: Clear, concise system instructions
- **Caching**: Session-level agent reuse

### System Resource Management
- **Token Budget**: Complexity-appropriate model selection
- **Parallel Operations**: Concurrent agent coordination
- **Context Sharing**: Efficient information passing
- **Memory Management**: Intelligent context window usage
- **Response Time**: <2s for complex multi-agent workflows

---

*Complete system architecture reference for AgentGen Claude Desktop integration*