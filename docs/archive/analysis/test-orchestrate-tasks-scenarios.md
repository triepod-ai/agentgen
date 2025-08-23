# @orchestrate-tasks Agent Test Scenarios

Comprehensive test scenarios for the @orchestrate-tasks agent focusing on agent installation, escalation logic, and error recovery.

## Overview

This test suite validates the core capabilities of @orchestrate-tasks:
- **Agent installation triggers and handling**
- **Proper escalation to @orchestrate-agents and @orchestrate-agents-adv**
- **Error recovery and fallback strategies**
- **Complex multi-agent coordination patterns**
- **Integration with @install-agents-manager and context-manager**

## Test Categories

### A. Agent Installation Tests

#### A1. Single Missing Agent Detection
**Setup**: Project with no agents installed
**Input**: "Review this code for security vulnerabilities"
**Expected**: 
- Detect missing `security-auditor` agent
- Delegate to @install-agents-manager: `cd /home/bryan/agentgen && ./install-agents security-auditor`
- Route to @orchestrate-agents with confirmed agent availability
**Validation**: Check agent installation command, verify routing decision

#### A2. Multiple Agents Requiring Profile
**Setup**: Project with no agents installed
**Input**: "I need full-stack development with security audit and performance optimization"
**Expected**:
- Detect need for multiple agent categories
- Recommend profile installation: `development-team` + `security-audit` profiles
- Route to @orchestrate-agents-adv for complex coordination
**Validation**: Verify profile selection logic, complex routing

#### A3. Partial Agent Availability
**Setup**: Project with `code-reviewer` but missing `security-auditor`
**Input**: "Perform comprehensive security audit and code review"
**Expected**:
- Detect partial capability (code-reviewer exists, security-auditor missing)
- Install only missing agent: `security-auditor`
- Route to @orchestrate-agents for simple coordination
**Validation**: Efficient installation strategy, appropriate routing

#### A4. Global vs Project Installation Decision
**Setup**: User requests development workflow setup
**Input**: "Set up comprehensive development environment for my team"
**Expected**:
- Analyze scope (team vs individual)
- Recommend profile installation with scope flag
- Install command: `./install-agents --profile development-team` (project scope)
**Validation**: Correct scope determination, appropriate installation strategy

#### A5. Complex Enterprise Workflow
**Setup**: Large project requiring comprehensive coverage
**Input**: "Complete enterprise security audit, architecture review, performance optimization, and modernization"
**Expected**:
- Detect enterprise-scale requirements (8+ agents across domains)
- Install multiple coordinated profiles
- Route to @orchestrate-agents-adv or direct coordination
**Validation**: Enterprise detection logic, multi-profile strategy

### B. Escalation Logic Tests

#### B1. Simple Task - No Escalation
**Setup**: Project with required agents available
**Input**: "Read this config file and extract database settings"
**Expected**:
- Analyze as Green complexity task
- Route directly to single agent: `@config-reader`
- No escalation to other orchestrators
**Validation**: Complexity assessment accuracy, direct routing

#### B2. Standard Development - Route to orchestrate-agents
**Setup**: Project with development agents available
**Input**: "Debug this authentication issue and improve error handling"
**Expected**:
- Analyze as Yellow complexity (2-3 agents)
- Route to @orchestrate-agents: `@debugger` + `@code-reviewer`
- Provide specific coordination instructions
**Validation**: Yellow complexity detection, appropriate orchestrator selection

#### B3. Complex Multi-Domain - Route to orchestrate-agents-adv
**Setup**: Project with comprehensive agent coverage
**Input**: "Modernize legacy authentication system with new architecture, security audit, and performance testing"
**Expected**:
- Analyze as Red complexity (4+ agents, multi-domain)
- Route to @orchestrate-agents-adv
- Provide enterprise coordination pattern
**Validation**: Red complexity detection, advanced orchestrator routing

#### B4. Ambiguous Complexity Assessment
**Setup**: Project with mixed requirements
**Input**: "Fix this bug and maybe improve the code a bit"
**Expected**:
- Conservative assessment (prefer simpler routing)
- Route to @orchestrate-agents initially
- Provide escalation option if complexity increases
**Validation**: Conservative bias in complexity assessment

#### B5. Boundary Conditions - 3 vs 4 Agents
**Setup**: Test complexity threshold boundaries
**Input**: "Code review, security check, performance test, and documentation update"
**Expected**:
- Exactly 4 agents required
- Route to @orchestrate-agents-adv (Red complexity threshold)
- Enterprise coordination pattern
**Validation**: Precise threshold detection, correct routing

### C. Error Recovery Tests

#### C1. Agent Installation Failure - Permission Denied
**Setup**: Simulate permission failure during installation
**Input**: "Need security audit capabilities"
**Mock Error**: Permission denied when accessing /home/bryan/agentgen
**Expected**:
- Catch installation failure
- Provide alternative installation methods
- Fallback to available agents with reduced capability
**Validation**: Error detection, graceful degradation

#### C2. Profile Installation Timeout
**Setup**: Simulate timeout during profile installation
**Input**: "Set up complete development team"
**Mock Error**: Installation command times out
**Expected**:
- Detect timeout condition
- Fall back to individual agent installation
- Provide manual installation guidance
**Validation**: Timeout handling, fallback strategy

#### C3. Orchestrator Unavailability
**Setup**: Mock @orchestrate-agents-adv unavailable
**Input**: Complex enterprise request requiring advanced orchestration
**Expected**:
- Detect orchestrator unavailability
- Fall back to direct multi-agent coordination
- Create TodoWrite task lists for manual coordination
**Validation**: Fallback mechanism, alternative coordination

#### C4. Partial Installation Success
**Setup**: Some agents install successfully, others fail
**Input**: "Need frontend development with security focus"
**Mock**: Frontend agents install, security agents fail
**Expected**:
- Report partial success
- Provide options: retry failed installs or proceed with available agents
- Graceful degradation with reduced capabilities
**Validation**: Partial success handling, user options

#### C5. Context-Manager Communication Failure
**Setup**: Mock context-manager unavailable
**Input**: Any task requiring project context
**Expected**:
- Detect context-manager unavailability
- Proceed with basic agent availability scan
- Provide degraded service with warning
**Validation**: Context failure handling, service degradation

### D. Integration Tests

#### D1. Context-Manager Integration Success
**Setup**: Fully operational context-manager
**Input**: "Analyze current project structure and improve architecture"
**Expected**:
- Query context-manager for project state
- Receive comprehensive project understanding
- Use context for informed agent selection and routing
**Validation**: Context query format, context integration

#### D2. Install-Agents-Manager Delegation
**Setup**: Missing agents requiring installation
**Input**: "Set up comprehensive testing infrastructure"
**Expected**:
- Delegate to @install-agents-manager
- Monitor installation progress
- Verify successful installation before proceeding
**Validation**: Delegation protocol, progress monitoring

#### D3. TodoWrite Task List Creation
**Setup**: Complex multi-phase workflow
**Input**: "Implement complete authentication system with testing and documentation"
**Expected**:
- Create comprehensive TodoWrite task list
- Break down workflow into phases
- Track progress across multiple agents
**Validation**: Task breakdown quality, progress tracking

#### D4. Cross-Orchestrator Handoff
**Setup**: Task starts simple but becomes complex
**Input**: "Fix this small bug" → discovered to be architectural issue
**Expected**:
- Initially route to @orchestrate-agents
- Detect increased complexity during execution
- Escalate to @orchestrate-agents-adv mid-workflow
**Validation**: Dynamic escalation, handoff protocol

#### D5. Multi-Phase Workflow Coordination
**Setup**: Enterprise-scale project
**Input**: "Complete legacy system modernization"
**Expected**:
- Create multi-phase coordination plan
- Phase 1: Analysis agents
- Phase 2: Implementation agents  
- Phase 3: Validation agents
**Validation**: Phase organization, agent coordination

### E. Performance & Edge Cases

#### E1. Large-Scale Agent Requirements
**Setup**: Enterprise project requiring 20+ agents
**Input**: "Complete enterprise transformation: architecture, security, performance, frontend, backend, AI/ML, data, testing, documentation, deployment"
**Expected**:
- Efficiently handle large agent requirements
- Group into logical profiles and categories
- Optimize installation strategy
**Validation**: Performance with large requirements, optimization

#### E2. Rapid Context Switching
**Setup**: Multiple requests in quick succession
**Input**: Sequence of different task types requiring different agents
**Expected**:
- Handle context switching efficiently
- Avoid redundant agent installations
- Maintain context across rapid requests
**Validation**: Context switching performance, efficiency

#### E3. Concurrent Task Handling
**Setup**: Multiple simultaneous requests
**Input**: Two complex tasks requiring different agent sets
**Expected**:
- Handle concurrent requests appropriately
- Avoid installation conflicts
- Coordinate resource usage
**Validation**: Concurrency handling, resource management

#### E4. Resource Constraint Scenarios
**Setup**: Limited disk space or memory
**Input**: Request requiring large profile installation
**Mock**: Disk space warning during installation
**Expected**:
- Detect resource constraints
- Suggest minimal installation strategies
- Prioritize essential agents
**Validation**: Resource awareness, optimization

#### E5. Malformed or Ambiguous Requests
**Setup**: Various edge case inputs
**Input Examples**:
- Empty request: ""
- Contradictory: "Simple quick task but make it enterprise-scale"
- Vague: "Make things better"
**Expected**:
- Handle gracefully with clarification requests
- Provide helpful suggestions
- Avoid unnecessary agent installations
**Validation**: Edge case handling, user guidance

## Test Data Requirements

### Mock Agent Configurations
- Available agents list
- Installation success/failure responses
- Agent capability matrices
- Profile definitions

### Sample Project Structures
- Empty project (no agents)
- Partial project (some agents)
- Full project (complete agent coverage)
- Legacy project (outdated agents)

### Mock Context-Manager Responses
- Project state information
- Agent activity logs
- Workflow patterns

## Validation Criteria

### Installation Logic
- ✅ Correct agent/profile selection
- ✅ Appropriate installation scope (project/global)
- ✅ Efficient installation strategy
- ✅ Proper error handling

### Escalation Logic
- ✅ Accurate complexity assessment
- ✅ Correct orchestrator selection
- ✅ Appropriate routing parameters
- ✅ Boundary condition handling

### Error Recovery
- ✅ Graceful failure handling
- ✅ Appropriate fallback strategies
- ✅ Clear error communication
- ✅ Recovery option provision

### Integration Quality
- ✅ Smooth component integration
- ✅ Proper delegation protocols
- ✅ Effective progress monitoring
- ✅ Context preservation

### Performance
- ✅ Efficient resource usage
- ✅ Fast response times
- ✅ Scalable handling of complex requests
- ✅ Minimal redundant operations

## Test Execution Framework

Each test includes:
1. **Setup**: Initial conditions and prerequisites
2. **Input**: Specific request or trigger  
3. **Mock Responses**: Simulated component responses
4. **Expected Output**: Detailed expected behavior
5. **Validation**: Automated checks and assertions
6. **Teardown**: Cleanup and reset actions

## Success Metrics

- **Coverage**: All major code paths tested
- **Accuracy**: Correct behavior in all scenarios
- **Robustness**: Graceful handling of all edge cases
- **Performance**: Acceptable response times and resource usage
- **Usability**: Clear, helpful output in all conditions