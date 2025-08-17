#!/bin/bash

# Debug script to isolate the validation function issue
# The logic is working correctly but tests are failing - let's find out why

set -euo pipefail

echo "🔍 Debugging Validation Function Issue"
echo "======================================"

# Test the validation function in isolation
debug_validation_function() {
    local input="$1"
    local expected_routing="$2" 
    local expected_installation="$3"
    
    echo "Input: $input"
    echo "Expected routing: $expected_routing"
    echo "Expected installation: $expected_installation"
    echo ""
    
    # Copy the exact logic from simulate_orchestrate_tasks_request()
    local input_lower
    input_lower=$(echo "${input}" | tr '[:upper:]' '[:lower:]')
    
    # Initialize scoring variables
    local security_score=0
    local development_score=0
    local enterprise_score=0
    local simple_score=0
    local complexity_score=0
    
    # Security keywords scoring
    [[ "${input_lower}" =~ security ]] && ((security_score++))
    [[ "${input_lower}" =~ vulnerabilities ]] && ((security_score++))
    [[ "${input_lower}" =~ vulnerability ]] && ((security_score++))
    [[ "${input_lower}" =~ audit ]] && ((security_score++))
    [[ "${input_lower}" =~ secure ]] && ((security_score++))
    
    # Development keywords scoring
    [[ "${input_lower}" =~ debug ]] && ((development_score++))
    [[ "${input_lower}" =~ fix ]] && ((development_score++))
    [[ "${input_lower}" =~ improve ]] && ((development_score++))
    [[ "${input_lower}" =~ develop ]] && ((development_score++))
    [[ "${input_lower}" =~ build ]] && ((development_score++))
    [[ "${input_lower}" =~ authentication ]] && ((development_score++))
    [[ "${input_lower}" =~ error ]] && ((development_score++))
    [[ "${input_lower}" =~ handling ]] && ((development_score++))
    [[ "${input_lower}" =~ "code review" ]] && ((development_score++))
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
    
    # Calculate total complexity score
    complexity_score=$((security_score + development_score + enterprise_score))
    
    # Determine agent needs and installation requirements
    local agents_needed=1
    local installation_needed="none"
    local routing_decision="direct"
    
    # Routing logic based on keyword analysis
    if [[ ${simple_score} -ge 3 && ${complexity_score} -le 1 ]]; then
        # Simple tasks: Read config files, extract data, etc.
        agents_needed=1
        installation_needed="none"
        routing_decision="direct"
        
    elif [[ ${security_score} -ge 1 && ${development_score} -le 1 && ${enterprise_score} -le 1 ]]; then
        # Security-focused tasks: Single security agent needed
        agents_needed=1
        installation_needed="security-auditor"
        routing_decision="orchestrate-agents"
        
    elif [[ ${development_score} -ge 2 || (${security_score} -ge 1 && ${development_score} -ge 1) ]]; then
        # Standard development tasks: 2-3 agents
        agents_needed=2
        if [[ ${security_score} -ge 1 ]]; then
            installation_needed="security-auditor"
        else
            installation_needed="none"
        fi
        routing_decision="orchestrate-agents"
        
    elif [[ ${enterprise_score} -ge 5 || ${complexity_score} -ge 10 ]]; then
        # Enterprise-scale tasks: 8+ agents
        agents_needed=8
        installation_needed="development-team,security-audit,infrastructure"
        routing_decision="direct-coordination"
        
    elif [[ ${complexity_score} -ge 7 || (${development_score} -ge 4 && ${security_score} -ge 1) ]]; then
        # Complex multi-domain tasks: 4+ agents
        agents_needed=5
        installation_needed="development-team,security-audit"
        routing_decision="orchestrate-agents-adv"
        
    else
        # Default case: simple direct routing
        agents_needed=1
        installation_needed="none"
        routing_decision="direct"
    fi
    
    echo "Scores: security=${security_score}, development=${development_score}, enterprise=${enterprise_score}, simple=${simple_score}, total=${complexity_score}"
    echo "ACTUAL routing: '${routing_decision}'"
    echo "ACTUAL installation: '${installation_needed}'"
    echo ""
    
    # Now test the validation EXACTLY as it appears in the test script
    echo "=== VALIDATION TESTING ==="
    
    local validation_success=true
    
    if [[ "${routing_decision}" != "${expected_routing}" ]]; then
        echo "❌ ROUTING MISMATCH: Expected '${expected_routing}', got '${routing_decision}'"
        validation_success=false
    else
        echo "✅ ROUTING MATCH: '${routing_decision}'"
    fi
    
    if [[ "${installation_needed}" != "${expected_installation}" ]]; then
        echo "❌ INSTALLATION MISMATCH: Expected '${expected_installation}', got '${installation_needed}'"
        validation_success=false
    else
        echo "✅ INSTALLATION MATCH: '${installation_needed}'"
    fi
    
    echo "Final validation result: ${validation_success}"
    echo "----------------------------------------"
    echo ""
    
    # Return the validation result like the original function
    echo "${validation_success}"
}

# Test the problematic cases
echo "🧪 Testing A1 (should be correct but is failing):"
result_a1=$(debug_validation_function "Review this code for security vulnerabilities" "orchestrate-agents" "security-auditor")
echo "A1 Result: $result_a1"
echo ""

echo "🧪 Testing A3 (should be correct but is failing):"
result_a3=$(debug_validation_function "Perform comprehensive security audit and code review" "orchestrate-agents" "security-auditor") 
echo "A3 Result: $result_a3"
echo ""

echo "🧪 Testing B1 (should be correct but is failing):"
result_b1=$(debug_validation_function "Read this config file and extract database settings" "direct" "none")
echo "B1 Result: $result_b1"
echo ""

echo "🧪 Testing B2 (should be correct but is failing):"
result_b2=$(debug_validation_function "Debug this authentication issue and improve error handling" "orchestrate-agents" "none")
echo "B2 Result: $result_b2"
echo ""

echo "🧪 Testing working case A4 (comparison):"
# This test passes, let's see if validation works for it too (though it doesn't use this function)
echo "A4 doesn't use the validation function, so let's test a different working one..."

echo "🧪 Testing A2 (appears correct in logs but failing):"
result_a2=$(debug_validation_function "I need full-stack development with security audit and performance optimization" "orchestrate-agents-adv" "development-team,security-audit")
echo "A2 Result: $result_a2"
echo ""

echo "📊 SUMMARY OF DEBUG RESULTS:"
echo "A1: $result_a1 (should be true)"
echo "A2: $result_a2 (should be true)" 
echo "A3: $result_a3 (should be true)"
echo "B1: $result_b1 (should be true)"
echo "B2: $result_b2 (should be true)"

if [[ "$result_a1" == "true" && "$result_a2" == "true" && "$result_a3" == "true" && "$result_b1" == "true" && "$result_b2" == "true" ]]; then
    echo ""
    echo "🎯 CONCLUSION: The validation logic works perfectly in isolation!"
    echo "   This confirms the bug is in the test harness, not the logic."
    echo "   The issue is likely in how the test script calls or processes"
    echo "   the simulate_orchestrate_tasks_request() function."
else
    echo ""
    echo "🤔 Some validation still failing - need to investigate further"
fi