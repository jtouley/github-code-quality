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

Sample Output:
```md
 "src/analyzer.py": "### DRY (Don't Repeat Yourself) Analysis\n\n**Score: 6/10**\n\n**Summary:**\nThe code adheres to the DRY principle to some extent, but there are areas where repetition could be reduced. For instance, the error handling for the environment variable REPO could be encapsulated into a separate function to avoid redundancy if similar checks are needed elsewhere in the code. Additionally, the process of initializing clients could be abstracted into a function to promote reuse and clarity. However, the code does not contain significant duplication, which is why it scores moderately well.\n\n### SOLID Principles Analysis\n\n**Score: 5/10**\n\n**Summary:**\nThe code exhibits some adherence to the SOLID principles but lacks in certain areas. \n\n- **Single Responsibility Principle (SRP):** The analyze_repo function does multiple things: it checks environment variables, initializes clients, and processes files. This could be broken down into smaller, more focused functions.\n  \n- **Open/Closed Principle (OCP):** The function is not easily extendable without modifying the existing code, as adding new types of analysis or output formats would require changes to the analyze_repo function itself.\n  \n- **Liskov Substitution Principle (LSP):** This principle is not directly applicable here as there are no class hierarchies involved.\n  \n- **Interface Segregation Principle (ISP):** The code does not define interfaces, so this principle isn't relevant in its current form.\n  \n- **Dependency Inversion Principle (DIP):** The function directly instantiates GitHubClient and AIClient, which can make testing and substituting these dependencies more difficult. Using dependency injection could improve this aspect.\n\nOverall, while the code is functional, it could benefit from a more modular design that adheres more closely to SOLID principles."
 ```

## GitHub Action Integration

The included GitHub Action (in .github/workflows/code_quality.yml) runs on pull requests against main or development. To use this action in another repository:
- Reference this repository as an action or copy the workflow file.
- Ensure that the target repository has the necessary secrets (GITHUB_TOKEN and OPENAI_API_KEY).

## Code Quality
- Linting: Run black . and flake8 to check code formatting and style.
- TODOs: See inline comments for areas marked for future improvements.

## Future Enhancements
- Improve prompt engineering for better DRY/SOLID scoring.
- Add error handling and logging enhancements.
- Extend analysis to multiple programming languages.
- Integrate a Streamlit dashboard for visualization.
