#!/bin/bash

# Ultra-simple debug to find the hanging issue
set -euo pipefail

echo "Testing basic regex operations..."

input="Review this code for security vulnerabilities"
input_lower=$(echo "${input}" | tr '[:upper:]' '[:lower:]')

echo "Input: $input"
echo "Lowercase: $input_lower"

security_score=0

echo "Testing security keyword..."
if [[ "${input_lower}" =~ security ]]; then
    echo "Found 'security'"
    ((security_score++))
else
    echo "Did not find 'security'"
fi

echo "Security score: $security_score"

echo "Testing vulnerabilities keyword..."
if [[ "${input_lower}" =~ vulnerabilities ]]; then
    echo "Found 'vulnerabilities'"
    ((security_score++))
else
    echo "Did not find 'vulnerabilities'"
fi

echo "Final security score: $security_score"
echo "Test completed successfully!"