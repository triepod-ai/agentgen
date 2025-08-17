#!/bin/bash

echo "Testing basic keyword detection..."
input="Review this code for security vulnerabilities"
input_lower=$(echo "${input}" | tr '[:upper:]' '[:lower:]')
echo "Input: $input"
echo "Lowercase: $input_lower"

security_score=0
if [[ "${input_lower}" =~ security ]]; then
    security_score=$((security_score + 1))
    echo "Found 'security'"
fi

if [[ "${input_lower}" =~ vulnerabilities ]]; then
    security_score=$((security_score + 1))
    echo "Found 'vulnerabilities'"
fi

echo "Security score: $security_score"
echo "Test completed successfully!"