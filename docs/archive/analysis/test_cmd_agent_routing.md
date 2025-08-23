# CMD Agent Select Logic - Routing Tests

## Test Cases

### Test 1: Frontend Component Creation
**Input**: "Create a responsive React dashboard component with TypeScript"
**Expected**: @build-frontend (primary) or @react-specialist (alternative)
**Domain**: frontend
**Complexity**: standard (0.5-0.7)

### Test 2: Backend API Development  
**Input**: "Build a REST API with authentication and database integration"
**Expected**: @build-backend (primary) or @full-stack-developer (alternative)
**Domain**: backend
**Complexity**: standard (0.6-0.7)

### Test 3: Security Audit
**Input**: "Comprehensive security audit of our microservices architecture"
**Expected**: @security-auditor (high confidence)
**Domain**: security  
**Complexity**: complex (0.8+)

### Test 4: Multi-Domain Task
**Input**: "Build user authentication with React frontend and Node.js backend including testing"
**Expected**: @orchestrate-agents (multi-domain coordination)
**Domains**: frontend, backend, quality
**Complexity**: complex (0.7+)

### Test 5: Simple Utility Task
**Input**: "Analyze this screenshot for UI components"
**Expected**: @analyze-screenshot
**Domain**: frontend (utility)
**Complexity**: simple (0.3)

### Test 6: Database Optimization
**Input**: "Optimize PostgreSQL queries and improve database performance"
**Expected**: @database-specialist or @postgres-pro
**Domain**: backend/data
**Complexity**: standard (0.6)

### Test 7: Documentation Task
**Input**: "Create comprehensive API documentation with examples"
**Expected**: @documentation-expert or @api-documenter
**Domain**: documentation
**Complexity**: standard (0.5)

### Test 8: Complex Orchestration
**Input**: "Migrate legacy PHP application to modern Node.js with testing and deployment"
**Expected**: @orchestrate-agents-adv (enterprise coordination)
**Domains**: backend, infrastructure, quality (4+ domains)
**Complexity**: complex (0.9+)

## Routing Decision Validation

Each test should produce:
1. **Complexity Score**: 0.0-1.0 classification
2. **Domain Detection**: List of identified domains
3. **Confidence Score**: Routing confidence (0.0-1.0)
4. **Selected Agent**: Primary routing choice
5. **Alternatives**: Backup routing options
6. **Reasoning**: Justification for selection

## Expected Performance
- **Response Time**: <100ms per routing decision
- **Accuracy**: >85% appropriate agent selection
- **Coverage**: All available agents should be routable