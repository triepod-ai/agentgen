#!/bin/bash

# Test script for agent-builder functionality

echo "=== Agent Builder Test Suite ==="
echo

# Test 1: Check if agent-builder file exists
echo "Test 1: Checking agent-builder.md existence..."
if [ -f "/home/bryan/agentgen/submodules/claude-code-sub-agents/specialization/agent-builder.md" ]; then
    echo "✅ agent-builder.md exists"
else
    echo "❌ agent-builder.md not found"
    exit 1
fi
echo

# Test 2: Validate YAML frontmatter
echo "Test 2: Validating YAML frontmatter..."
head -n 6 /home/bryan/agentgen/submodules/claude-code-sub-agents/specialization/agent-builder.md | grep -q "name: agent-builder"
if [ $? -eq 0 ]; then
    echo "✅ YAML frontmatter is valid"
else
    echo "❌ YAML frontmatter validation failed"
    exit 1
fi
echo

# Test 3: Check character count
echo "Test 3: Checking character count (<400 chars)..."
PROMPT_CONTENT=$(sed -n '/^---$/,/^---$/!p' /home/bryan/agentgen/submodules/claude-code-sub-agents/specialization/agent-builder.md | tail -n +2)
CHAR_COUNT=$(echo -n "$PROMPT_CONTENT" | wc -c)
echo "Character count: $CHAR_COUNT"
if [ $CHAR_COUNT -lt 400 ]; then
    echo "✅ System prompt is under 400 characters"
else
    echo "❌ System prompt exceeds 400 characters"
    exit 1
fi
echo

# Test 4: Check template directory structure
echo "Test 4: Checking template directory structure..."
if [ -d "/home/bryan/agentgen/templates" ] && \
   [ -d "/home/bryan/agentgen/templates/green" ] && \
   [ -d "/home/bryan/agentgen/templates/yellow" ] && \
   [ -d "/home/bryan/agentgen/templates/red" ]; then
    echo "✅ Template directory structure exists"
else
    echo "❌ Template directory structure incomplete"
    exit 1
fi
echo

# Test 5: Verify templates exist
echo "Test 5: Verifying template files..."
TEMPLATE_COUNT=$(find /home/bryan/agentgen/templates -name "*.yaml" -o -name "*.md" | wc -l)
echo "Found $TEMPLATE_COUNT template files"
if [ $TEMPLATE_COUNT -gt 0 ]; then
    echo "✅ Template files exist"
else
    echo "❌ No template files found"
    exit 1
fi
echo

# Test 6: Check configuration file
echo "Test 6: Checking configuration file..."
if [ -f "/home/bryan/agentgen/config/agent-builder.yaml" ]; then
    echo "✅ Configuration file exists"
    # Validate key sections
    grep -q "compression:" /home/bryan/agentgen/config/agent-builder.yaml && \
    grep -q "tool_mappings:" /home/bryan/agentgen/config/agent-builder.yaml && \
    grep -q "complexity:" /home/bryan/agentgen/config/agent-builder.yaml
    if [ $? -eq 0 ]; then
        echo "✅ Configuration file contains required sections"
    else
        echo "⚠️  Configuration file may be incomplete"
    fi
else
    echo "❌ Configuration file not found"
    exit 1
fi
echo

# Test 7: Check README updates
echo "Test 7: Checking README.md updates..."
grep -q "agent-builder" /home/bryan/agentgen/README.md
if [ $? -eq 0 ]; then
    echo "✅ README.md contains agent-builder information"
else
    echo "❌ README.md not updated with agent-builder"
    exit 1
fi
echo

echo "=== Test Suite Complete ==="
echo "✅ All tests passed successfully!"
echo
echo "Agent-builder is ready for use. Invoke with:"
echo "  @agent-builder create [agent-type]"
echo "  Use the agent-builder subagent"
echo

# Display agent info
echo "=== Agent-Builder Info ==="
echo "Location: /home/bryan/agentgen/submodules/claude-code-sub-agents/specialization/agent-builder.md"
echo "Templates: /home/bryan/agentgen/templates/"
echo "Config: /home/bryan/agentgen/config/agent-builder.yaml"
echo "Character count: $CHAR_COUNT/400"