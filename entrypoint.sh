#!/bin/bash
set -e

# Export GitHub Actions inputs as environment variables expected by your code
export OPENAI_API_KEY=$INPUT_OPENAI_API_KEY
export REPO=$INPUT_REPO
export GITHUB_TOKEN=$INPUT_GITHUB_TOKEN
export ENABLE_ANALYSIS=true

# Run the analyzer
python src/analyzer.py