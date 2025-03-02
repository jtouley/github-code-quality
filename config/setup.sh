#!/bin/bash

echo "🚀 Setting up the Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r config/requirements.txt

echo "🛠 Installing linting tools (black, flake8, pre-commit)..."
pip install black flake8 pre-commit

echo "🔧 Installing act for local GitHub Actions testing..."
if ! command -v act &> /dev/null; then
    echo "📥 Installing act..."
    brew install act || echo "❌ Failed to install act. Install manually: https://github.com/nektos/act"
else
    echo "✅ act is already installed."
fi

# Ensure .env exists, copying from .env.example if missing
if [[ ! -f ".env" ]]; then
    echo "⚠️  .env file missing! Creating from config/.env.example..."
    if [[ -f "config/.env.example" ]]; then
        cp config/.env.example .env
        echo "✅ .env file created. Please update it with your API keys and repository info."
    else
        echo "❌ ERROR: config/.env.example not found. Cannot create .env file."
        exit 1
    fi
else
    echo "✅ .env file already exists."
fi

# Load environment variables from .env
export $(grep -v '^#' .env | xargs)

echo "🔍 Checking API credentials..."

# Validate GitHub Token
GITHUB_CHECK=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/user")

if [[ "$GITHUB_CHECK" -ne 200 ]]; then
  echo "⚠️  WARNING: GitHub Token appears to be invalid."
  echo "➡️  Reissue a new token here: https://github.com/settings/tokens"
else
  echo "✅ GitHub Token is VALID."
fi

# Validate OpenAI API Key
OPENAI_CHECK=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $OPENAI_API_KEY" "https://api.openai.com/v1/models")

if [[ "$OPENAI_CHECK" -ne 200 ]]; then
  echo "⚠️  WARNING: OpenAI API Key appears to be invalid."
  echo "➡️  Reissue a new key here: https://platform.openai.com/api-keys"
else
  echo "✅ OpenAI API Key is VALID."
fi

# Verify repository and branch existence
echo "🔍 Checking repository and branch access..."
BRANCH_CHECK=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/$REPO/branches/$GITHUB_BRANCH")

if [[ "$BRANCH_CHECK" -ne 200 ]]; then
  echo "⚠️  WARNING: Repository '$REPO' or branch '$GITHUB_BRANCH' not found!"
  echo "➡️  Check your repository settings: https://github.com/$REPO"
else
  echo "✅ Repository and branch exist."
fi

echo "🔧 Exporting PYTHONPATH to include 'src/' for pytest..."
export PYTHONPATH=$(pwd)/src
echo "PYTHONPATH set to: $PYTHONPATH"

echo "🔗 Setting up pre-commit hooks..."
pre-commit install

echo "✅ Setup complete! Here’s what to do next:"
echo "  - Run 'source venv/bin/activate' to enter the virtual environment."
echo "  - Run 'pytest tests/' to execute tests."
echo "  - Run 'black . && flake8' to lint and check formatting."
echo "  - Run 'pre-commit run --all-files' to apply pre-commit checks."
echo "  - Run 'act pull_request' to locally test GitHub Actions."

echo "🎯 You're ready to code!"