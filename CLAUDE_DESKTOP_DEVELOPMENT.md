# AgentGen Development Guide - Claude Desktop Reference

Comprehensive guide for agent creation, optimization, testing, and development workflows in the AgentGen system.

## 🛠️ Agent Creation Workflow

### Complete Development Process
```
Plan → Create → Optimize → Test → Deploy → Monitor
  ↓       ↓        ↓        ↓       ↓        ↓
Design  Write    <400     Valid   Install  Track
Agent   Prompt   Chars    Tools   & Test   Perf
```

## 📝 Agent Design Phase

### Step 1: Requirements Analysis
```yaml
agent_requirements:
  domain: "Specific expertise area"
  complexity_tier: "Green/Yellow/Red"
  primary_use_cases: ["case1", "case2", "case3"]
  auto_activation_triggers: ["keyword1", "keyword2"]
  required_tools: ["essential_tools_only"]
  performance_targets:
    response_time: "<500ms for Yellow, <2s for Red"
    accuracy: ">90% for domain tasks"
    token_efficiency: "<400 chars for optimal loading"
```

### Step 2: Tool Requirements Planning
```yaml
tool_selection_guide:
  core_operations:
    - "Read": File inspection, code analysis
    - "Write": New file creation (use sparingly)
    - "Edit/MultiEdit": Code modifications (primary)
    - "Grep": Pattern searching and analysis
    - "Bash": Command execution and automation
  
  specialized_operations:
    - "mcp__qdrant__qdrant_find": Enhanced agents only
    - "mcp__context7__*": Documentation lookup
    - "mcp__playwright__*": Browser automation
    - "Task": Sub-agent delegation

  tool_minimization_principle: "Grant only essential tools for security and performance"
```

### Step 3: Complexity Tier Selection
```yaml
complexity_assessment:
  Green_Tier:
    characteristics: ["Simple operations", "Single-step workflows", "Basic text processing"]
    model: "claude-3-haiku"
    token_budget: "1K-3K"
    examples: ["analyze-screenshot", "config-reader", "env-reader"]
  
  Yellow_Tier:
    characteristics: ["Standard development", "Multi-step analysis", "Code manipulation"]
    model: "claude-3-5-sonnet" 
    token_budget: "3K-15K"
    examples: ["build-frontend", "debug-issue", "test-automation"]
  
  Red_Tier:
    characteristics: ["Complex reasoning", "System architecture", "Deep analysis"]
    model: "claude-3-5-sonnet-20241022"
    token_budget: "15K+"
    examples: ["architect-specialist", "security-auditor", "performance-engineer"]
```

## ✍️ Agent Creation Templates

### Basic Agent Template (Green Complexity)
```yaml
---
name: simple-agent
description: Brief description with auto-activation keywords. Execute immediately.
tools: Read, Write, Bash
model: claude-3-haiku-20240307
---

# Simple Agent

Quick operation specialist.

## Workflow
Input → Process → Output immediately.
```

### Standard Agent Template (Yellow Complexity)
```yaml
---
name: standard-agent
description: Standard development agent for [domain]. Use proactively for [triggers].
tools: Read, Write, Edit, Grep, Bash
model: claude-3-5-sonnet-20241022
---

# Standard Development Agent

[Domain] specialist with systematic approach.

## Core Principles
1. [Primary principle]
2. [Quality standard]
3. [Performance target]

## Workflow
1. **Context Analysis** → Understand current state
2. **Planning** → Define approach and steps
3. **Implementation** → Execute with quality checks
4. **Validation** → Verify results and performance

Execute workflow immediately upon invocation.
```

### Advanced Agent Template (Red Complexity)
```yaml
---
name: advanced-specialist
description: Advanced [domain] specialist. Use proactively for complex [domain] challenges requiring deep expertise.
tools: Read, Write, Edit, MultiEdit, Grep, Bash, Task
model: claude-3-5-sonnet-20241022
---

# Advanced [Domain] Specialist

Expert-level [domain] analysis and solution development.

## Expertise Areas
- **[Area 1]**: Deep knowledge of [specific expertise]
- **[Area 2]**: Advanced [methodology/framework] application
- **[Area 3]**: [Integration/optimization] capabilities

## Core Principles
1. **[Principle 1]**: [Priority/approach]
2. **[Principle 2]**: [Quality/standard]  
3. **[Principle 3]**: [Performance/efficiency]

## Advanced Workflow
1. **Comprehensive Analysis** → Multi-dimensional problem assessment
2. **Strategic Planning** → Architecture-level solution design
3. **Systematic Implementation** → Phased execution with validation
4. **Performance Optimization** → Efficiency and quality enhancement
5. **Knowledge Integration** → Cross-domain pattern application
6. **Continuous Validation** → Quality gates and success metrics

## Quality Standards
- **[Standard 1]**: [Measurable criteria]
- **[Standard 2]**: [Performance benchmark]
- **[Standard 3]**: [Output quality requirement]

Execute advanced workflow immediately upon invocation.
```

## 🚀 Performance Optimization

### <400 Character Optimization Strategy

#### Before Optimization (Verbose)
```yaml
---
name: security-analyzer
description: This agent analyzes security vulnerabilities in code and provides comprehensive recommendations for improving security posture
tools: Read, Write, Edit, Grep, Bash, MultiEdit
---

# Security Analysis Specialist

You are a comprehensive security analysis specialist responsible for identifying vulnerabilities.

## Detailed Responsibilities
1. Analyze code for security vulnerabilities
2. Check for OWASP Top 10 issues
3. Verify input validation
4. Review authentication mechanisms
5. Assess authorization controls
6. Generate detailed security reports

Execute complete security analysis workflow.
```

#### After Optimization (<400 chars)
```yaml
---
name: security-auditor
description: Security vulnerability analysis. Use for security audits, OWASP checks.
tools: Read, Grep, Bash
---

# Security Auditor

OWASP Top 10 → auth checks → input validation → report.

Execute immediately.
```

### Optimization Techniques
```yaml
optimization_patterns:
  arrow_workflows: "Step1 → Step2 → Result"
  essential_tools: "Minimum required only"
  direct_language: "Remove explanatory text"
  action_focus: "Execute immediately"
  keyword_density: "Pack trigger words in description"
```

## 🧪 Testing & Validation

### Agent Testing Framework

#### Performance Testing
```bash
# Response time validation
test_response_time() {
    start_time=$(date +%s%N)
    @your-agent "test task"
    end_time=$(date +%s%N)
    response_time=$(((end_time - start_time) / 1000000))
    echo "Response time: ${response_time}ms"
}

# Targets:
# Green: <500ms
# Yellow: <2000ms  
# Red: <5000ms
```

#### Quality Testing
```bash
# Domain accuracy validation
test_domain_accuracy() {
    # Prepare test scenarios
    test_cases=("basic_task" "medium_complexity" "edge_case")
    
    for case in "${test_cases[@]}"; do
        result=$(echo "Test: $case" | @your-agent)
        # Validate result against expected output
        accuracy_score=$(validate_accuracy "$result" "$case")
        echo "$case: $accuracy_score% accuracy"
    done
}
```

#### Auto-Activation Testing
```bash
# Test trigger phrase recognition
test_auto_activation() {
    triggers=("analyze security" "check vulnerabilities" "audit code")
    
    for trigger in "${triggers[@]}"; do
        echo "Testing trigger: $trigger"
        # Monitor which agent activates
        result=$(echo "$trigger task" | monitor_agent_selection)
        echo "Activated: $result"
    done
}
```

### Validation Checklist
```yaml
validation_criteria:
  file_format:
    - "Valid YAML frontmatter"
    - "Required fields: name, description"
    - "Clean markdown formatting"
  
  performance:
    - "Character count <400 for optimal agents"
    - "Response time within tier limits"
    - "Tool usage minimal and appropriate"
  
  functionality:
    - "Agent activates on trigger phrases"
    - "Produces expected output format"
    - "Handles error cases gracefully"
  
  integration:
    - "Works with orchestration system"
    - "Integrates with context-manager"
    - "Compatible with existing agents"
```

## 🔧 Development Tools & Utilities

### Agent Management Interface
```bash
# Interactive agent management
/agents                           # Built-in Claude Code interface
# Features: Create, Edit, Delete, View, Tool permissions

# Direct file management
mkdir -p .claude/agents           # Create agent directory
ls -la .claude/agents/           # List current agents
```

### Development Utilities
```bash
# Agent validation script
validate_agent() {
    agent_file="$1"
    
    # Check YAML frontmatter
    if ! head -n 10 "$agent_file" | grep -q "^---$"; then
        echo "ERROR: Missing YAML frontmatter"
        return 1
    fi
    
    # Check character count
    char_count=$(wc -c < "$agent_file")
    if [ "$char_count" -gt 400 ]; then
        echo "WARNING: Agent exceeds 400 characters ($char_count)"
    fi
    
    # Check required fields
    if ! grep -q "^name:" "$agent_file"; then
        echo "ERROR: Missing required 'name' field"
        return 1
    fi
    
    echo "Agent validation passed"
}
```

### Performance Profiling
```bash
# Agent performance profiler
profile_agent() {
    agent_name="$1"
    test_task="$2"
    
    echo "Profiling $agent_name with task: $test_task"
    
    # Memory usage before
    mem_before=$(ps -o rss= -p $$)
    
    # Execute with timing
    time_output=$(time (echo "$test_task" | @$agent_name) 2>&1)
    
    # Memory usage after  
    mem_after=$(ps -o rss= -p $$)
    
    echo "Memory delta: $((mem_after - mem_before))KB"
    echo "Timing: $time_output"
}
```

## 📁 File Organization

### Project Structure Best Practices
```
your-project/
├── .claude/
│   ├── agents/                  # Project-specific agents
│   │   ├── project-specialist.md
│   │   └── custom-helper.md
│   └── settings.local.json      # Tool permissions
├── src/                         # Source code
├── tests/                       # Test files
└── docs/                        # Documentation
```

### Agent Naming Conventions
```yaml
naming_patterns:
  basic_pattern: "domain-action"
  examples:
    - "security-auditor"      # domain: security, action: audit
    - "react-optimizer"       # domain: react, action: optimize
    - "db-migrator"          # domain: database, action: migrate
  
  enhanced_pattern: "domain-specialist-enhanced"
  examples:
    - "security-auditor-enhanced"
    - "react-specialist-enhanced"
    - "performance-engineer-enhanced"
```

## 🔄 Continuous Integration

### Agent Update Workflow
```yaml
update_process:
  1_development: "Create/modify agent locally"
  2_testing: "Validate performance and functionality"  
  3_integration: "Test with existing agent ecosystem"
  4_deployment: "Install to target environments"
  5_monitoring: "Track performance and usage metrics"
```

### Version Control Best Practices
```bash
# Agent version control
git add .claude/agents/new-agent.md
git commit -m "feat: Add new-agent for [domain] operations

- Implements [functionality]
- Optimized for <400 characters
- Tested with [test scenarios]
- Performance: [metrics]"

# Tag major agent releases
git tag -a agents-v2.1 -m "Agent system update with performance improvements"
```

### Automated Testing Integration
```yaml
ci_pipeline:
  agent_validation:
    - "YAML syntax validation"
    - "Character count checks" 
    - "Required field verification"
    - "Tool permission validation"
  
  performance_testing:
    - "Response time measurement"
    - "Memory usage profiling"
    - "Auto-activation accuracy"
  
  integration_testing:
    - "Orchestration compatibility"
    - "Context-manager integration"
    - "Cross-agent communication"
```

## 🎯 Advanced Development Patterns

### Multi-Agent Coordination
```yaml
coordination_patterns:
  sequential: "Agent1 → Agent2 → Agent3 (pipeline)"
  parallel: "Agent1 + Agent2 + Agent3 (concurrent)"
  hierarchical: "Coordinator → Specialists (delegation)"
  handoff: "Agent1 → determines → Agent2 (dynamic)"
```

### Context Sharing Protocols
```json
{
  "agent_communication": {
    "sender": "agent-name",
    "receiver": "context-manager",
    "message_type": "status_update",
    "payload": {
      "task_progress": "completed_analysis",
      "findings": ["finding1", "finding2"],
      "next_recommended_agent": "specialist-name"
    }
  }
}
```

### Error Handling Patterns
```yaml
error_patterns:
  graceful_degradation: "Provide partial results when possible"
  clear_messaging: "Specific error descriptions with context"
  recovery_suggestions: "Actionable steps for user resolution"
  escalation_paths: "When to involve orchestration or other agents"
```

## 📊 Metrics & Analytics

### Performance Metrics
```yaml
key_metrics:
  response_time: "Mean, P95, P99 response times"
  accuracy: "Task completion success rate"
  efficiency: "Token usage per task"
  user_satisfaction: "Feedback scores and usage patterns"
```

### Development Analytics
```bash
# Usage analytics
analyze_agent_usage() {
    # Track most used agents
    # Identify performance bottlenecks
    # Measure user satisfaction
    # Optimize based on usage patterns
}
```

---

*Complete development guide for AgentGen Claude Desktop agent creation and optimization*