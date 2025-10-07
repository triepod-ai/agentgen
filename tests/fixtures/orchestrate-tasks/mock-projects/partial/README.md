# Partial Test Project

This is a mock project with some agents installed, used for testing partial agent availability scenarios.

## Project Structure
- `.claude/agents/` directory exists
- Has basic development agents: `code-reviewer`, `debugger`
- Missing specialized agents for security, performance, etc.

## Expected Test Scenarios
- Additional agent installation
- Capability gap detection
- Incremental profile installation
- Mixed existing/new agent coordination

## Typical Test Cases
- A3: Partial agent availability
- B2: Standard development routing
- C4: Partial installation success
- D4: Cross-orchestrator handoff

## Available Agents
- code-reviewer: Quality assurance and code review
- debugger: Root cause analysis and troubleshooting

## Missing Capabilities
- Security auditing
- Performance optimization  
- Frontend/UI development
- Documentation generation
- Infrastructure/deployment