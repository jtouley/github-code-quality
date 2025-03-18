#!/bin/bash
set -e

# Debug - print all environment variables
echo "Debugging environment variables:"
env | sort

# Export GitHub Actions inputs as environment variables expected by your code
# GitHub Actions converts input names to uppercase and prepends INPUT_
if [ -n "$INPUT_GITHUB_TOKEN" ]; then
  export GITHUB_TOKEN=$INPUT_GITHUB_TOKEN
  echo "GITHUB_TOKEN set from INPUT_GITHUB_TOKEN"
else
  echo "ERROR: INPUT_GITHUB_TOKEN is not set"
fi

if [ -n "$INPUT_OPENAI_API_KEY" ]; then
  export OPENAI_API_KEY=$INPUT_OPENAI_API_KEY
  echo "OPENAI_API_KEY set from INPUT_OPENAI_API_KEY"
else
  echo "ERROR: INPUT_OPENAI_API_KEY is not set"
fi

if [ -n "$INPUT_REPO" ]; then
  export REPO=$INPUT_REPO
  echo "REPO set to: $REPO"
else
  echo "ERROR: INPUT_REPO is not set"
fi

export ENABLE_ANALYSIS=true

# Print working directory for debugging
echo "Current working directory: $(pwd)"
ls -la

# Run the analyzer
echo "Running: python /app/src/analyzer.py"
python /app/src/analyzer.py