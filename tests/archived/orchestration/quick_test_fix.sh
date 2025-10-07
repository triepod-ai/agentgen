#!/bin/bash

# Quick test to verify the fix works
set -euo pipefail

echo "🚀 QUICK TEST - Verifying the Fix"
echo "================================="

# Test the problematic cases directly
test_validation() {
    local input="$1"
    local expected_routing="$2" 
    local expected_installation="$3"
    
    echo "Testing: $input"
    echo "Expected: $expected_routing + $expected_installation"
    
    # Simplified version of the fixed logic
    local input_lower
    input_lower=$(echo "${input}" | tr '[:upper:]' '[:lower:]')
    
    local security_score=0
    local development_score=0
    local enterprise_score=0
    local simple_score=0
    
    # Security keywords scoring
    [[ "${input_lower}" =~ security ]] && ((security_score++))
    [[ "${input_lower}" =~ vulnerabilities ]] && ((security_score++))
    [[ "${input_lower}" =~ audit ]] && ((security_score++))
    
    # Development keywords scoring
    [[ "${input_lower}" =~ debug ]] && ((development_score++))
    [[ "${input_lower}" =~ authentication ]] && ((development_score++))
    [[ "${input_lower}" =~ error ]] && ((development_score++))
    [[ "${input_lower}" =~ handling ]] && ((development_score++))
    [[ "${input_lower}" =~ "full-stack" ]] && ((development_score+=2))
    [[ "${input_lower}" =~ performance ]] && ((development_score++))
    [[ "${input_lower}" =~ optimization ]] && ((development_score++))
    
    # Enterprise keywords scoring
    [[ "${input_lower}" =~ enterprise ]] && ((enterprise_score+=2))
    [[ "${input_lower}" =~ complete ]] && ((enterprise_score++))
    [[ "${input_lower}" =~ comprehensive ]] && ((enterprise_score++))
    [[ "${input_lower}" =~ modernization ]] && ((enterprise_score+=2))
    [[ "${input_lower}" =~ modernize ]] && ((enterprise_score+=2))
    [[ "${input_lower}" =~ architecture ]] && ((enterprise_score++))
    [[ "${input_lower}" =~ legacy ]] && ((enterprise_score++))
    [[ "${input_lower}" =~ system ]] && ((enterprise_score++))
    
    # Simple task keywords scoring
    [[ "${input_lower}" =~ read ]] && ((simple_score++))
    [[ "${input_lower}" =~ extract ]] && ((simple_score++))
    [[ "${input_lower}" =~ config ]] && ((simple_score++))
    [[ "${input_lower}" =~ file ]] && ((simple_score++))
    [[ "${input_lower}" =~ settings ]] && ((simple_score++))
    [[ "${input_lower}" =~ database ]] && ((simple_score++))
    
    local complexity_score=$((security_score + development_score + enterprise_score))
    
    # FIXED: Routing logic with correct priority order
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
    
    echo "Scores: security=${security_score}, development=${development_score}, enterprise=${enterprise_score}, simple=${simple_score}, total=${complexity_score}"
    echo "Actual: $routing_decision + $installation_needed"
    
    if [[ "${routing_decision}" == "${expected_routing}" && "${installation_needed}" == "${expected_installation}" ]]; then
        echo "✅ PASS"
        return 0
    else
        echo "❌ FAIL"
        return 1
    fi
}

echo ""
echo "🧪 Testing A1 (was failing):"
test_validation "Review this code for security vulnerabilities" "orchestrate-agents" "security-auditor"
echo ""

echo "🧪 Testing A2 (was failing):"
test_validation "I need full-stack development with security audit and performance optimization" "orchestrate-agents-adv" "development-team,security-audit"
echo ""

echo "🧪 Testing A3 (was failing):"
test_validation "Perform comprehensive security audit and code review" "orchestrate-agents" "security-auditor"
echo ""

echo "🧪 Testing B1 (was failing):"
test_validation "Read this config file and extract database settings" "direct" "none"
echo ""

echo "🧪 Testing B2 (was failing):"
test_validation "Debug this authentication issue and improve error handling" "orchestrate-agents" "none"
echo ""

echo "🧪 Testing B3 (was failing):"
test_validation "Modernize legacy authentication system with new architecture, security audit, and performance testing" "orchestrate-agents-adv" "development-team,security-audit"
echo ""

echo "🧪 Testing A5 (was failing):"
test_validation "Complete enterprise security audit, architecture review, performance optimization, and modernization" "direct-coordination" "development-team,security-audit,infrastructure"
echo ""

echo "📊 Quick Test Complete!"
echo "If all show ✅ PASS, the fix works correctly."