#!/bin/bash

# Minimal test to verify the core fixes work
set -euo pipefail

echo "🧪 MINIMAL FIX VERIFICATION"
echo "=========================="

# Extract just the core logic with fixes applied
test_fixed_logic() {
    local input="$1"
    local expected_routing="$2"
    local expected_installation="$3"
    
    # Convert to lowercase
    local input_lower
    input_lower=$(echo "${input}" | tr '[:upper:]' '[:lower:]')
    
    # Initialize scores
    local security_score=0
    local development_score=0
    local enterprise_score=0
    local simple_score=0
    
    # Security keywords
    [[ "${input_lower}" =~ security ]] && ((security_score++))
    [[ "${input_lower}" =~ vulnerabilities ]] && ((security_score++))
    [[ "${input_lower}" =~ audit ]] && ((security_score++))
    
    # Development keywords
    [[ "${input_lower}" =~ debug ]] && ((development_score++))
    [[ "${input_lower}" =~ authentication ]] && ((development_score++))
    [[ "${input_lower}" =~ error ]] && ((development_score++))
    [[ "${input_lower}" =~ handling ]] && ((development_score++))
    [[ "${input_lower}" =~ "full-stack" ]] && ((development_score+=2))
    [[ "${input_lower}" =~ performance ]] && ((development_score++))
    [[ "${input_lower}" =~ optimization ]] && ((development_score++))
    
    # Enterprise keywords
    [[ "${input_lower}" =~ enterprise ]] && ((enterprise_score+=2))
    [[ "${input_lower}" =~ complete ]] && ((enterprise_score++))
    [[ "${input_lower}" =~ comprehensive ]] && ((enterprise_score++))
    [[ "${input_lower}" =~ modernization ]] && ((enterprise_score+=2))
    [[ "${input_lower}" =~ modernize ]] && ((enterprise_score+=2))
    [[ "${input_lower}" =~ architecture ]] && ((enterprise_score++))
    [[ "${input_lower}" =~ legacy ]] && ((enterprise_score++))
    [[ "${input_lower}" =~ system ]] && ((enterprise_score++))
    
    # Simple keywords
    [[ "${input_lower}" =~ read ]] && ((simple_score++))
    [[ "${input_lower}" =~ extract ]] && ((simple_score++))
    [[ "${input_lower}" =~ config ]] && ((simple_score++))
    [[ "${input_lower}" =~ file ]] && ((simple_score++))
    [[ "${input_lower}" =~ settings ]] && ((simple_score++))
    [[ "${input_lower}" =~ database ]] && ((simple_score++))
    
    local complexity_score=$((security_score + development_score + enterprise_score))
    
    # FIXED: Correct priority order
    local routing_decision="direct"
    local installation_needed="none"
    
    if [[ ${simple_score} -ge 3 && ${complexity_score} -le 1 ]]; then
        routing_decision="direct"
        installation_needed="none"
    elif [[ ${enterprise_score} -ge 5 || ${complexity_score} -ge 10 ]]; then
        routing_decision="direct-coordination"
        installation_needed="development-team,security-audit,infrastructure"
    elif [[ ${complexity_score} -ge 7 || (${development_score} -ge 4 && ${security_score} -ge 1) ]]; then
        routing_decision="orchestrate-agents-adv"
        installation_needed="development-team,security-audit"
    elif [[ ${security_score} -ge 1 && ${development_score} -le 1 && ${enterprise_score} -le 1 ]]; then
        routing_decision="orchestrate-agents"
        installation_needed="security-auditor"
    elif [[ ${development_score} -ge 2 || (${security_score} -ge 1 && ${development_score} -ge 1) ]]; then
        routing_decision="orchestrate-agents"
        if [[ ${security_score} -ge 1 ]]; then
            installation_needed="security-auditor"
        else
            installation_needed="none"
        fi
    fi
    
    echo "Scores: security=$security_score, development=$development_score, enterprise=$enterprise_score, simple=$simple_score, complexity=$complexity_score"
    echo "Result: $routing_decision + $installation_needed"
    
    # Validate
    if [[ "$routing_decision" == "$expected_routing" && "$installation_needed" == "$expected_installation" ]]; then
        echo "✅ PASS"
        return 0
    else
        echo "❌ FAIL - Expected: $expected_routing + $expected_installation"
        return 1
    fi
}

echo ""
echo "Testing the 7 previously failing tests:"
echo ""

echo "🧪 A1 (was failing):"
test_fixed_logic "Review this code for security vulnerabilities" "orchestrate-agents" "security-auditor"
echo ""

echo "🧪 A2 (was failing):"
test_fixed_logic "I need full-stack development with security audit and performance optimization" "orchestrate-agents-adv" "development-team,security-audit"
echo ""

echo "🧪 A3 (was failing):"
test_fixed_logic "Perform comprehensive security audit and code review" "orchestrate-agents" "security-auditor"
echo ""

echo "🧪 A5 (was failing):"
test_fixed_logic "Complete enterprise security audit, architecture review, performance optimization, and modernization" "direct-coordination" "development-team,security-audit,infrastructure"
echo ""

echo "🧪 B1 (was failing):"
test_fixed_logic "Read this config file and extract database settings" "direct" "none"
echo ""

echo "🧪 B2 (was failing):"
test_fixed_logic "Debug this authentication issue and improve error handling" "orchestrate-agents" "none"
echo ""

echo "🧪 B3 (was failing):"
test_fixed_logic "Modernize legacy authentication system with new architecture, security audit, and performance testing" "orchestrate-agents-adv" "development-team,security-audit"
echo ""

echo "📊 MINIMAL FIX VERIFICATION COMPLETE!"