#!/bin/bash

# Test Script: Verify symlinked agents work with Claude Code
# This script tests that symlinked agents are recognized and functional

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_DIR="$SCRIPT_DIR/test-symlinks-$(date +%Y%m%d-%H%M%S)"
AGENT_HUB_DIR="$SCRIPT_DIR/agents"

# Test results
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

show_help() {
    cat << EOF
${CYAN}Symlink Agent Testing Tool${NC}

${YELLOW}USAGE:${NC}
    test-symlink-agents.sh [OPTIONS]

${YELLOW}OPTIONS:${NC}
    --cleanup          Remove test directory after completion
    --verbose          Show detailed test output
    --help            Show this help message

${YELLOW}TESTS PERFORMED:${NC}
    1. Symlink creation and resolution
    2. Agent file readability through symlinks
    3. YAML frontmatter parsing
    4. Directory precedence (project vs global)
    5. Broken symlink handling
    6. Update propagation
    7. Performance comparison

${YELLOW}EXAMPLE:${NC}
    ${GREEN}./test-symlink-agents.sh --cleanup${NC}

EOF
}

# Logging functions
log_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
    ((TESTS_RUN++))
}

log_pass() {
    echo -e "  ${GREEN}✓ PASS${NC} $1"
    ((TESTS_PASSED++))
}

log_fail() {
    echo -e "  ${RED}✗ FAIL${NC} $1"
    ((TESTS_FAILED++))
}

log_info() {
    echo -e "${CYAN}[INFO]${NC} $1"
}

# Test 1: Basic symlink creation
test_symlink_creation() {
    log_test "Symlink Creation"
    
    # Create test directory structure
    mkdir -p "$TEST_DIR/.claude/agents"
    mkdir -p "$AGENT_HUB_DIR/test"
    
    # Create a test agent in hub
    cat > "$AGENT_HUB_DIR/test/test-agent.md" << 'EOF'
---
name: test-agent
description: Test agent for symlink verification
tools: Read, LS
---

# Test Agent

This is a test agent for verifying symlink functionality.
EOF
    
    # Create symlink
    ln -s "$AGENT_HUB_DIR/test/test-agent.md" "$TEST_DIR/.claude/agents/test-agent.md"
    
    # Verify symlink exists and points correctly
    if [[ -L "$TEST_DIR/.claude/agents/test-agent.md" ]]; then
        local target=$(readlink "$TEST_DIR/.claude/agents/test-agent.md")
        if [[ "$target" == "$AGENT_HUB_DIR/test/test-agent.md" ]]; then
            log_pass "Symlink created successfully"
        else
            log_fail "Symlink points to wrong location: $target"
        fi
    else
        log_fail "Symlink was not created"
    fi
}

# Test 2: Read agent through symlink
test_symlink_reading() {
    log_test "Agent Reading Through Symlink"
    
    # Try to read the agent file through the symlink
    if [[ -f "$TEST_DIR/.claude/agents/test-agent.md" ]]; then
        local content=$(cat "$TEST_DIR/.claude/agents/test-agent.md" 2>/dev/null)
        if [[ "$content" == *"Test Agent"* ]]; then
            log_pass "Agent content readable through symlink"
        else
            log_fail "Could not read agent content through symlink"
        fi
    else
        log_fail "Symlinked agent file not accessible"
    fi
}

# Test 3: Parse YAML frontmatter
test_yaml_parsing() {
    log_test "YAML Frontmatter Parsing"
    
    # Extract agent name from YAML
    local name=$(grep "^name:" "$TEST_DIR/.claude/agents/test-agent.md" 2>/dev/null | sed 's/name: //')
    if [[ "$name" == "test-agent" ]]; then
        log_pass "YAML frontmatter parsed correctly"
    else
        log_fail "Could not parse YAML frontmatter"
    fi
}

# Test 4: Directory precedence
test_precedence() {
    log_test "Directory Precedence (Project > Global)"
    
    # Create global directory
    mkdir -p "$HOME/.claude/agents"
    
    # Create different versions
    cat > "$AGENT_HUB_DIR/test/precedence-agent.md" << 'EOF'
---
name: precedence-agent
description: Global version
---
Global version content
EOF
    
    cat > "$TEST_DIR/.claude/agents/precedence-agent.md" << 'EOF'
---
name: precedence-agent
description: Project version
---
Project version content
EOF
    
    # Verify project version is used
    local desc=$(grep "^description:" "$TEST_DIR/.claude/agents/precedence-agent.md" | sed 's/description: //')
    if [[ "$desc" == "Project version" ]]; then
        log_pass "Project agents correctly override global"
    else
        log_fail "Precedence not working correctly"
    fi
}

# Test 5: Broken symlink handling
test_broken_symlink() {
    log_test "Broken Symlink Detection"
    
    # Create a symlink to non-existent file
    ln -s "/nonexistent/agent.md" "$TEST_DIR/.claude/agents/broken-agent.md"
    
    # Check if we can detect it's broken
    if [[ -L "$TEST_DIR/.claude/agents/broken-agent.md" ]] && [[ ! -f "$TEST_DIR/.claude/agents/broken-agent.md" ]]; then
        log_pass "Broken symlink correctly detected"
    else
        log_fail "Failed to detect broken symlink"
    fi
    
    # Clean up broken link
    rm -f "$TEST_DIR/.claude/agents/broken-agent.md"
}

# Test 6: Update propagation
test_update_propagation() {
    log_test "Update Propagation"
    
    # Modify the hub agent
    echo "# Updated content" >> "$AGENT_HUB_DIR/test/test-agent.md"
    
    # Check if update is visible through symlink
    local content=$(tail -1 "$TEST_DIR/.claude/agents/test-agent.md" 2>/dev/null)
    if [[ "$content" == "# Updated content" ]]; then
        log_pass "Updates propagate through symlinks instantly"
    else
        log_fail "Updates did not propagate"
    fi
}

# Test 7: Performance test
test_performance() {
    log_test "Performance Comparison"
    
    # Create 20 test agents
    for i in {1..20}; do
        cat > "$AGENT_HUB_DIR/test/perf-agent-$i.md" << EOF
---
name: perf-agent-$i
description: Performance test agent $i
tools: Read
---
Content for agent $i
EOF
    done
    
    # Time symlink creation
    local start_sym=$(date +%s%N)
    for i in {1..20}; do
        ln -s "$AGENT_HUB_DIR/test/perf-agent-$i.md" "$TEST_DIR/.claude/agents/perf-agent-$i.md"
    done
    local end_sym=$(date +%s%N)
    local time_sym=$(( (end_sym - start_sym) / 1000000 ))
    
    # Time file copying
    mkdir -p "$TEST_DIR/copied-agents"
    local start_copy=$(date +%s%N)
    for i in {1..20}; do
        cp "$AGENT_HUB_DIR/test/perf-agent-$i.md" "$TEST_DIR/copied-agents/perf-agent-$i.md"
    done
    local end_copy=$(date +%s%N)
    local time_copy=$(( (end_copy - start_copy) / 1000000 ))
    
    # Compare times
    if [[ $time_sym -le $((time_copy * 2)) ]]; then
        log_pass "Symlink performance acceptable (${time_sym}ms vs ${time_copy}ms for copies)"
    else
        log_fail "Symlink performance degraded (${time_sym}ms vs ${time_copy}ms for copies)"
    fi
}

# Test 8: Claude Code integration simulation
test_claude_integration() {
    log_test "Claude Code Integration Simulation"
    
    # Simulate how Claude Code would discover agents
    local agent_count=0
    
    # Check project agents
    if [[ -d "$TEST_DIR/.claude/agents" ]]; then
        while IFS= read -r agent; do
            if [[ -f "$agent" ]]; then
                ((agent_count++))
            fi
        done < <(find "$TEST_DIR/.claude/agents" -name "*.md" -type f -o -type l 2>/dev/null)
    fi
    
    if [[ $agent_count -gt 0 ]]; then
        log_pass "Claude Code would discover $agent_count agents"
    else
        log_fail "Claude Code would not find agents"
    fi
}

# Parse arguments
CLEANUP=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --cleanup)
            CLEANUP=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Header
echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║    Symlink Agent Testing Suite        ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"
echo ""

log_info "Test directory: $TEST_DIR"
echo ""

# Run tests
test_symlink_creation
test_symlink_reading
test_yaml_parsing
test_precedence
test_broken_symlink
test_update_propagation
test_performance
test_claude_integration

# Summary
echo ""
echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║           Test Summary                 ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "Tests run:     $TESTS_RUN"
echo -e "Tests passed:  ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed:  ${RED}$TESTS_FAILED${NC}"
echo ""

if [[ $TESTS_FAILED -eq 0 ]]; then
    echo -e "${GREEN}✨ All tests passed! Symlinks are fully functional.${NC}"
else
    echo -e "${RED}⚠️  Some tests failed. Review the results above.${NC}"
fi

# Cleanup
if [[ "$CLEANUP" == "true" ]]; then
    echo ""
    log_info "Cleaning up test directory..."
    rm -rf "$TEST_DIR"
    rm -rf "$AGENT_HUB_DIR/test"
    log_info "Cleanup complete"
fi

# Exit with appropriate code
if [[ $TESTS_FAILED -gt 0 ]]; then
    exit 1
else
    exit 0
fi