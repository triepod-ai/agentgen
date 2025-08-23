# Knowledge-Enhanced Agent Templates

Templates for creating specialized agents with pre-loaded domain expertise and intelligent knowledge retrieval capabilities.

## 📚 Template Overview

### Red Tier - Expert Specialist (`red-tier-specialist.md`)
**Purpose**: Comprehensive domain experts with extensive knowledge bases
**Performance**: <400 chars optimized for complex reasoning
**Knowledge Access**: 4-tier access pattern (embedded → fast → comprehensive → deep)
**Use Cases**: Complex problem-solving, architectural decisions, expert consultation

**Features**:
- Extensive embedded knowledge for instant responses
- Multi-collection Qdrant integration for deep analysis  
- Cross-domain knowledge synthesis capabilities
- Advanced workflow engine with quality gates
- Comprehensive error handling and fallbacks

### Yellow Tier - Focused Helper (`yellow-tier-helper.md`)  
**Purpose**: Targeted specialists for specific development tasks
**Performance**: Balanced performance and knowledge depth
**Knowledge Access**: 3-tier access (embedded → detailed → framework docs)
**Use Cases**: Development tasks, implementation guidance, best practice application

**Features**:
- Core domain patterns embedded for quick access
- Targeted Qdrant collection for detailed guidance
- Context7 integration for framework documentation
- Streamlined workflow optimized for development tasks

### Green Tier - Essential Assistant (`green-tier-assistant.md`)
**Purpose**: Lightweight assistants for common tasks
**Performance**: <400 chars, optimized for speed
**Knowledge Access**: 2-tier access (embedded → queryable details)
**Use Cases**: Quick help, basic questions, simple implementations

**Features**:
- Essential knowledge embedded for immediate responses
- Single collection access for detailed information
- Minimal tool footprint for fast execution
- Focused on most common use cases

## 🛠️ Template Customization Guide

### Required Replacements
Replace all `{placeholder}` values with domain-specific information:

#### Core Configuration
- `{domain}`: Technology domain (react, security, devops)
- `{Domain}`: Capitalized domain name for titles
- `{source_count}`: Number of authoritative sources
- `{key_sources}`: List of primary knowledge sources
- `{knowledge_points}`: Total knowledge points in collections

#### Knowledge Collections
- `{primary_collection}`: Main Qdrant collection name
- `{secondary_collection}`: Additional collection (Red tier only)
- `{cross_reference_collection}`: Cross-domain collection (Red tier only)
- `{essential_collection}`: Core collection (Green tier)

#### Capabilities & Use Cases
- `{primary_use_cases}`: Main scenarios where agent excels
- `{secondary_use_cases}`: Additional capabilities
- `{common_tasks}`: Typical tasks the agent handles
- `{coverage_areas}`: Knowledge domain coverage areas

#### Knowledge Areas & Patterns
- `{Primary_Knowledge_Area}`: Main expertise area
- `{Pattern_1}`, `{Pattern_2}`: Specific patterns with descriptions
- `{Key_Concept_1}`: Important concepts to embed
- `{query_example_1}`: Example queries for knowledge retrieval

#### Quality Metrics
- `{credibility_score}`: Source authority score (0-100)
- `{accuracy_percentage}`: Knowledge accuracy percentage
- `{coverage_percentage}`: Domain coverage percentage
- `{freshness_status}`: Knowledge currency status

### Customization Examples

#### React Testing Specialist (Red Tier)
```yaml
domain: react-testing
Domain: React Testing
source_count: 50
key_sources: Jest docs, Testing Library guides, React docs
knowledge_points: 1200
primary_collection: react_testing_strategies_comprehensive
secondary_collection: react_component_patterns_core  
cross_reference_collection: frontend_testing_integration
```

#### API Security Helper (Yellow Tier)
```yaml
domain: api-security
Domain: API Security
source_count: 25
key_sources: OWASP API Security Top 10, security frameworks
knowledge_points: 800
primary_collection: api_security_patterns_core
```

#### Docker Assistant (Green Tier)
```yaml
domain: docker
Domain: Docker
key_sources: Docker official documentation
essential_collection: container_patterns_essential
```

## 🚀 Agent Creation Process

### Step 1: Choose Template Tier
Select template based on complexity and knowledge requirements:
- **Green**: Simple, frequently used tasks
- **Yellow**: Moderate complexity, specialized tasks  
- **Red**: Complex reasoning, expert-level guidance

### Step 2: Knowledge Preparation
Ensure required Qdrant collections exist:
```bash
# Check available collections
@knowledge-curator "analyze available {domain} knowledge"

# Create knowledge base if needed
@knowledge-curator "build comprehensive {domain} knowledge base"
```

### Step 3: Template Customization
1. Copy appropriate template file
2. Replace all `{placeholder}` values
3. Customize knowledge areas and patterns
4. Adjust tools list for domain needs

### Step 4: Knowledge Integration Testing
```bash
# Test knowledge connectivity
@specialist-agent-builder "validate {domain} agent knowledge integration"

# Performance validation
@specialist-agent-builder "benchmark {domain} agent response times"
```

### Step 5: Deployment
```bash
# Deploy to project
./install-agents --symlink --custom /path/to/custom-agent.md

# Deploy globally
cp custom-agent.md ~/.claude/agents/
```

## 📊 Performance Guidelines

### Response Time Targets
| Tier | Embedded Knowledge | Single Collection | Multi-Collection |
|------|-------------------|-------------------|------------------|
| Green | <10ms | <500ms | N/A |
| Yellow | <10ms | <500ms | <2s |
| Red | <10ms | <500ms | <15s |

### Knowledge Integration Best Practices
1. **Embedded Knowledge**: Core patterns that are accessed frequently
2. **Single Collection Queries**: Specific implementation details
3. **Multi-Collection Synthesis**: Complex cross-domain analysis
4. **Fallback Strategies**: Graceful degradation when knowledge unavailable

### Optimization Tips
- Keep embedded knowledge under 200 tokens for fast loading
- Use specific query patterns to improve Qdrant retrieval accuracy
- Cache frequently accessed knowledge for better performance
- Monitor knowledge usage to optimize collection organization

## 🔍 Troubleshooting

### Common Issues

#### Knowledge Collection Not Found
```bash
# Check collection availability
@knowledge-curator "list available {domain} collections"

# Create missing collection
@knowledge-curator "create {domain} knowledge collection"
```

#### Slow Knowledge Retrieval
- Optimize query specificity
- Consider moving frequently accessed knowledge to embedded section
- Check Qdrant collection size and consider splitting large collections

#### Inconsistent Knowledge Quality
- Review source credibility scores
- Update knowledge with more authoritative sources
- Implement knowledge validation workflows

### Performance Monitoring
Track agent performance metrics:
- Knowledge retrieval response times
- Query success rates
- User satisfaction with knowledge quality
- Collection usage patterns

## 📈 Future Enhancements

### Planned Features
- **Dynamic Knowledge Loading**: Load knowledge based on conversation context
- **Knowledge Quality Scoring**: Automated assessment of knowledge accuracy
- **Cross-Agent Knowledge Sharing**: Share knowledge insights between agents
- **Personalized Knowledge**: Adapt knowledge presentation based on user expertise

### Integration Roadmap
- **Context-Manager Integration**: Enhanced project-aware knowledge access
- **Real-time Knowledge Updates**: Continuous knowledge base refreshing
- **Expert Validation Workflows**: Human expert review integration
- **Knowledge Analytics**: Advanced usage analytics and optimization

---

**Status**: Templates Ready for Production Use ✅
**Next Steps**: Create first knowledge-enhanced specialist agents
**Support**: Use @specialist-agent-builder for automated agent creation