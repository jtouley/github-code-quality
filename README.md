# GitHub Code Quality Analyzer

## Overview
This project analyzes a GitHub repository's Python code for adherence to DRY and SOLID principles using OpenAI's API. It’s built as a reusable GitHub Action so you can easily integrate it into any repo.

## Setup

### 1. Clone the Repository
```sh
git clone https://github.com/yourusername/github-code-quality.git
cd github-code-quality
```

### 2. Set Up the Virtual Environment
```sh
bash setup.sh
source venv/bin/activate
```

### 3. Configure Environment Variables
Copy .env.example to .env and update with your API keys and repository info.
```sh
cp .env.example .env
```

### 4. Run Locally
```sh
python src/analyzer.py
```

### 5. Run Tests
```sh
pytest tests/
```

## GitHub Action Integration

The included GitHub Action (in .github/workflows/code_quality.yml) runs on pull requests against main or development. To use this action in another repository:
	•	Reference this repository as an action or copy the workflow file.
	•	Ensure that the target repository has the necessary secrets (GITHUB_TOKEN and OPENAI_API_KEY).

## Code Quality
	•	Linting: Run black . and flake8 to check code formatting and style.
	•	TODOs: See inline comments for areas marked for future improvements.

## Future Enhancements
	•	Improve prompt engineering for better DRY/SOLID scoring.
	•	Add error handling and logging enhancements.
	•	Extend analysis to multiple programming languages.
	•	Integrate a Streamlit dashboard for visualization.
