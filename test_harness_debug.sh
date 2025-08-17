#!/bin/bash

# Exact replication of test harness to debug the validation issue
set -euo pipefail

echo "🔧 Test Harness Debug - Exact Replication"
echo "========================================="

# Logging functions (simplified)
log() {
    echo "[DEBUG] $*"
}

# EXACT copy of simulate_orchestrate_tasks_request() from current test script
simulate_orchestrate_tasks_request() {
    local input="$1"
    local expected_routing="$2"
    local expected_installation="$3"
    
    log "Simulating request: ${input}"
    log "Expected routing: ${expected_routing}"
    log "Expected installation: ${expected_installation}"
    
    # Convert input to lowercase for case-insensitive matching
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
    
    # Log scoring for debugging
    log "Keyword scores: security=${security_score}, development=${development_score}, enterprise=${enterprise_score}, simple=${simple_score}, total=${complexity_score}"
    log "Decision: agents=${agents_needed}, installation=${installation_needed}, routing=${routing_decision}"
    
    # Validate against expected results
    local validation_success=true
    
    if [[ "${routing_decision}" != "${expected_routing}" ]]; then
        log "MISMATCH: Expected routing '${expected_routing}', got '${routing_decision}'"
        validation_success=false
    fi
    
    if [[ "${installation_needed}" != "${expected_installation}" ]]; then
        log "MISMATCH: Expected installation '${expected_installation}', got '${installation_needed}'"
        validation_success=false
    fi
    
    echo "${validation_success}"
}

# Test the exact cases that are failing
echo "🧪 Testing A1 with exact harness replication:"
result_a1=$(simulate_orchestrate_tasks_request "Review this code for security vulnerabilities" "orchestrate-agents" "security-auditor")
echo "Result captured: '$result_a1'"
echo "Test would $([ "$result_a1" = "true" ] && echo "PASS" || echo "FAIL")"
echo ""

echo "🧪 Testing A2 with exact harness replication:"
result_a2=$(simulate_orchestrate_tasks_request "I need full-stack development with security audit and performance optimization" "orchestrate-agents-adv" "development-team,security-audit")
echo "Result captured: '$result_a2'"
echo "Test would $([ "$result_a2" = "true" ] && echo "PASS" || echo "FAIL")"
echo ""

echo "🧪 Testing A3 with exact harness replication:"
result_a3=$(simulate_orchestrate_tasks_request "Perform comprehensive security audit and code review" "orchestrate-agents" "security-auditor")
echo "Result captured: '$result_a3'"
echo "Test would $([ "$result_a3" = "true" ] && echo "PASS" || echo "FAIL")"
echo ""

echo "🧪 Testing B1 with exact harness replication:"
result_b1=$(simulate_orchestrate_tasks_request "Read this config file and extract database settings" "direct" "none")
echo "Result captured: '$result_b1'"
echo "Test would $([ "$result_b1" = "true" ] && echo "PASS" || echo "FAIL")"
echo ""

echo "🧪 Testing B2 with exact harness replication:"
result_b2=$(simulate_orchestrate_tasks_request "Debug this authentication issue and improve error handling" "orchestrate-agents" "none")
echo "Result captured: '$result_b2'"
echo "Test would $([ "$result_b2" = "true" ] && echo "PASS" || echo "FAIL")"
echo ""

echo "📊 SUMMARY:"
echo "A1: $result_a1 ($([ "$result_a1" = "true" ] && echo "should PASS" || echo "should FAIL"))"
echo "A2: $result_a2 ($([ "$result_a2" = "true" ] && echo "should PASS" || echo "should FAIL"))"
echo "A3: $result_a3 ($([ "$result_a3" = "true" ] && echo "should PASS" || echo "should FAIL"))"
echo "B1: $result_b1 ($([ "$result_b1" = "true" ] && echo "should PASS" || echo "should FAIL"))"
echo "B2: $result_b2 ($([ "$result_b2" = "true" ] && echo "should PASS" || echo "should FAIL"))"

# Now test if string comparisons work properly
echo ""
echo "🔍 Testing string comparison edge cases:"
test_str1="true"
test_str2="true"
if [[ "$test_str1" == "$test_str2" ]]; then
    echo "✅ Basic string comparison works"
else
    echo "❌ Basic string comparison broken"
fi

# Test with captured result
echo "Testing with actual result:"
if [[ "$result_a1" == "true" ]]; then
    echo "✅ A1 comparison works correctly"
else
    echo "❌ A1 comparison fails: '$result_a1' != 'true'"
    echo "Length of result_a1: ${#result_a1}"
    echo "Hex dump: $(echo -n "$result_a1" | xxd)"
fi