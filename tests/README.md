# Test Organization

Comprehensive test suite for the agentgen project, organized by test type and purpose.

## Directory Structure

```
tests/
├── unit/                        # Unit Tests
│   ├── python/
│   │   ├── agent-selection/    # CMD agent selection logic tests
│   │   └── enhanced-agents/    # Enhanced agent functionality tests
│   └── shell/
│       └── completion/          # Bash completion system tests
│
├── integration/                 # Integration Tests
│   ├── orchestration/           # Orchestration agent tests
│   ├── agents/                  # Agent builder tests
│   └── symlinks/                # Symlink system tests
│
├── debug/                       # Debug Scripts (temporary)
│   ├── completion/              # Completion debugging tools
│   └── orchestration/           # Orchestration debugging tools
│
├── fixtures/                    # Test Data & Fixtures
│   └── orchestrate-tasks/       # Test data for orchestration tests
│
├── results/                     # Test Results & Reports
│   ├── orchestration/           # Orchestration test logs
│   ├── routing/                 # Routing accuracy reports
│   └── enhanced-agents/         # Enhanced agent test reports
│
└── archived/                    # Old/Deprecated Test Versions
    └── orchestration/           # Historical orchestration tests
```

## Test Categories

### Unit Tests (`tests/unit/`)

**Python Tests (`python/`)**
- **agent-selection/**: CMD agent selection logic tests
  - `test_phase1_core.py` - Phase 1 core functionality
  - `test_phase2_integration.py` - Phase 2 intelligence layer
  - `run_tests.py` - Phase 1 test runner
  - `run_phase2_tests.py` - Phase 2 test runner
  - `routing_accuracy_test_suite.py` - Routing accuracy validation

- **enhanced-agents/**: Enhanced agent tests
  - `enhanced_agents_test_suite.py` - Comprehensive test suite
  - `enhanced_agents_specialized_tests.py` - Specialized functionality tests
  - `enhanced_agents_test_report.json` - Test results report

**Shell Tests (`shell/`)**
- **completion/**: Bash completion tests
  - `test-completion.sh` - Basic completion tests
  - `test-completion-comprehensive.sh` - Comprehensive completion tests
  - `test-completion-validation.sh` - Validation tests

### Integration Tests (`tests/integration/`)

**Orchestration Tests (`orchestration/`)**
- `test-orchestrate-tasks.sh` - Main orchestration test suite
- `test-orchestrate-tasks-working.sh` - Working test implementation

**Agent Builder Tests (`agents/`)**
- `test-agent-builder.sh` - Agent builder functionality tests

**Symlink Tests (`symlinks/`)**
- `test-symlink-agents.sh` - Symlink system integration tests

### Debug Scripts (`tests/debug/`)

Temporary debugging scripts for active development. These should be:
- Removed once issues are resolved
- Documented if they provide useful debugging patterns
- Converted to permanent tests if they validate important functionality

**Completion Debug (`completion/`)**
- `debug-completion.sh`, `debug_completion.sh` - Completion debugging

**Orchestration Debug (`orchestration/`)**
- `debug_validation_issue.sh` - Validation debugging
- `simple_debug.sh` - Simple debug script
- `test_harness_debug.sh` - Test harness debugging

### Test Fixtures (`tests/fixtures/`)

Test data and fixtures used across test suites:
- **orchestrate-tasks/**: Test data for orchestration tests

### Test Results (`tests/results/`)

All test execution results and reports:

**Orchestration Results (`orchestration/`)**
- Test execution logs with timestamps
- 12+ historical test runs preserved

**Routing Results (`routing/`)**
- `routing_accuracy_baseline.json` - Baseline accuracy metrics
- `routing_accuracy_report.md` - Detailed accuracy analysis
- `complexity_analysis.json` - Complexity tier analysis
- `migration_plan.json` - Migration planning data
- Various orchestration analysis reports

**Enhanced Agent Results (`enhanced-agents/`)**
- Currently empty - ready for future enhanced agent test results

### Archived Tests (`tests/archived/`)

Historical test versions preserved for reference:
- Old test implementations
- Deprecated test approaches
- Backup versions

**Orchestration Archive (`orchestration/`)**
- `test-orchestrate-tasks-FIXED.sh` - Fixed version
- `test-orchestrate-tasks.sh.backup` - Backup version
- Various debug/fix iterations

## Running Tests

### Python Unit Tests

**Agent Selection Tests:**
```bash
# Run from project root
cd /home/bryan/agentgen

# Phase 1 tests
python tests/unit/python/agent-selection/run_tests.py

# Phase 2 tests
python tests/unit/python/agent-selection/run_phase2_tests.py

# Routing accuracy
python tests/unit/python/agent-selection/routing_accuracy_test_suite.py
```

**Enhanced Agent Tests:**
```bash
# Run enhanced agent tests
python tests/unit/python/enhanced-agents/enhanced_agents_test_suite.py
python tests/unit/python/enhanced-agents/enhanced_agents_specialized_tests.py
```

### Shell Unit Tests

**Completion Tests:**
```bash
# From project root
./tests/unit/shell/completion/test-completion.sh
./tests/unit/shell/completion/test-completion-comprehensive.sh
./tests/unit/shell/completion/test-completion-validation.sh
```

### Integration Tests

**Orchestration Tests:**
```bash
# Main test suite
./tests/integration/orchestration/test-orchestrate-tasks.sh

# Working implementation
./tests/integration/orchestration/test-orchestrate-tasks-working.sh
```

**Agent Builder Tests:**
```bash
./tests/integration/agents/test-agent-builder.sh
```

**Symlink Tests:**
```bash
./tests/integration/symlinks/test-symlink-agents.sh
```

## Test Results

Test results are automatically saved to `tests/results/` with timestamps:
- **Orchestration logs**: `tests/results/orchestration/test-orchestrate-tasks-YYYYMMDD_HHMMSS.log`
- **Routing reports**: `tests/results/routing/*.json` and `*.md`
- **Enhanced agent reports**: `tests/results/enhanced-agents/*.json`

## Best Practices

### Writing New Tests

1. **Choose the right location:**
   - Unit tests → `tests/unit/{python|shell}/category/`
   - Integration tests → `tests/integration/category/`
   - Debug scripts → `tests/debug/category/` (temporary)

2. **Follow naming conventions:**
   - Python: `test_*.py` or `*_test.py`
   - Shell: `test-*.sh`
   - Keep names descriptive and specific

3. **Use fixtures:**
   - Add test data to `tests/fixtures/`
   - Reference with relative paths: `../../fixtures/`

4. **Save results:**
   - Output to `tests/results/category/`
   - Use timestamps for log files

### Debugging Tests

1. Use scripts in `tests/debug/` for active debugging
2. Move successful debug scripts to permanent tests or remove
3. Document useful debugging patterns in this README

### Archiving Tests

1. Old/deprecated tests go to `tests/archived/category/`
2. Include reason for archival in commit message
3. Keep for historical reference and rollback capability

## Path References

When writing tests, use these path patterns:

**From unit tests:**
```bash
FIXTURES_DIR="${SCRIPT_DIR}/../../fixtures/category"
RESULTS_DIR="${SCRIPT_DIR}/../../results/category"
```

**From integration tests:**
```bash
FIXTURES_DIR="${SCRIPT_DIR}/../../fixtures/category"
RESULTS_DIR="${SCRIPT_DIR}/../../results/category"
```

**Python imports for cmd-agent-select-logic:**
```python
# Add from tests/unit/python/agent-selection/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../cmd-agent-select-logic'))
```

## Maintenance

### Regular Cleanup

- **Weekly**: Review and remove resolved debug scripts
- **Monthly**: Archive old test versions
- **Quarterly**: Clean up old test results (keep last 3 months)

### CI/CD Integration

Tests are designed to be CI/CD friendly:
- Exit codes indicate pass/fail
- Results saved to predictable locations
- Timestamps prevent result collisions

## Contributing

When adding new tests:

1. Follow the directory structure
2. Update this README with new test descriptions
3. Include test fixtures if needed
4. Document any special setup requirements
5. Ensure tests are idempotent and can run in parallel

---

**Last Updated**: 2025-10-07
**Total Test Files**: 40+
**Test Coverage**: Unit, Integration, Debug
**Organization Status**: ✅ Complete
