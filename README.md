# GitHub Code Quality Analyzer

## Overview

This project analyzes a GitHub repository’s Python code for adherence to DRY (Don’t Repeat Yourself) and SOLID principles using OpenAI’s API. It’s built as a reusable GitHub Action, making it easy to integrate into any repository.

### 🔥 Features:
- Automated DRY & SOLID Analysis – Evaluates redundancy and software design principles.
- Configurable Weights & Severity Thresholds – Tailor the analysis to your team’s needs.
- PR Integration – Posts analysis results directly in pull requests.
- Flexible Prompt Customization – Controls for depth, language specificity, and verbosity.

## 📌 Setup & Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/github-code-quality.git
cd github-code-quality
```

### 2️⃣ Run the Setup Script
```sh
bash config/setup.sh
```
Alternatively, install dependencies manually:
```sh
python -m venv venv
source venv/bin/activate
pip install -r config/requirements.txt
```

### 3️⃣ Configure Environment Variables
Copy .env.example to .env and update with your API keys and repository info.
```sh
cp config/.env.example .env
```

## ⚙️ Configuration (config.yaml)

Customize the analysis behavior by modifying config/config.yaml.

### 1️⃣ DRY Analysis Configuration
```yaml
analysis:
  dry:
    enabled: true
    weight: 0.6  # Weight of DRY analysis in final scoring
    focus_areas:
      logic_reuse: 0.4  # Encourages function reuse
      data_centralization: 0.3  # Promotes shared data structures
      abstraction_level: 0.3  # Encourages modular design
    severity_threshold: 0.7  # Warning threshold
```

### 2️⃣ SOLID Principles Configuration
```yaml
  solid:
    enabled: true
    weight: 0.4
    principles:
      srp:  # Single Responsibility Principle
        enabled: true
        weight: 0.3
      ocp:  # Open/Closed Principle
        enabled: true
        weight: 0.2
      dip:  # Dependency Inversion Principle
        enabled: true
        weight: 0.5
    severity_threshold: 0.6
```
### 3️⃣ PR Feedback Format
```yaml
feedback_format:
  include_dry_score: true
  include_solid_score: true
  message_template: |
    ## Analysis for {file}

    ### DRY Analysis
    **Score:** {dry_score}/10
    {dry_analysis}

    ### SOLID Principles Analysis
    **Score:** {solid_score}/10
    {solid_analysis}
```
## 🏃 Running the Analysis Locally
To test before pushing changes:
```sh
python src/analyzer.py
```
For debugging PR comments:
```sh
python src/post_comment.py
```

## Sample Output:
```json
 "src/analyzer.py": {
|     "dry_score": 7,
|     "solid_score": 5,
|     "full_analysis": "### DRY Analysis\n**Score: 7/10**  \n**Summary:** The code adheres reasonably well to the DRY (Don't Repeat Yourself) principle, but there are some areas for improvement. The `extract_scores` function is a good example of reusing logic to avoid repetition when extracting scores from the AI's response. However, the code could benefit from further abstraction in areas where similar patterns are observed. For instance, the logic for handling the absence of the `REPO` environment variable and the `ENABLE_ANALYSIS` flag could be encapsulated in a separate function to avoid redundancy and improve readability. Additionally, the way results are written to the file could be refactored into a dedicated function to streamline the code and reduce repetition. Overall, while the code avoids significant redundancy, there are opportunities for better reuse and encapsulation.\n\n### SOLID Analysis\n**Score: 5/10**  \n**Summary:** The code demonstrates partial adherence to the SOLID principles, particularly in terms of the Single Responsibility Principle (SRP) and the Open/Closed Principle (OCP). The `analyze_repo` function has multiple responsibilities: it checks environment variables, initializes clients, processes files, and writes results to a file. This violates the SRP, as it would be better to separate these concerns into distinct functions or classes. The code does not exhibit clear adherence to the OCP, as any changes to the analysis process would require modifications to the `analyze_repo` function itself. The Dependency Inversion Principle (DIP) is somewhat respected through the use of environment variables for configuration, but the tight coupling between the `analyze_repo` function and the specific clients (e.g., `GitHubClient` and `AIClient`) could be improved by using interfaces or abstract classes. Overall, the code could benefit from a more modular design that adheres more closely to SOLID principles."
 ```

## 🛠️ Local Testing with act

This repository supports local testing of the GitHub Action using [act](https://github.com/nektos/act) by [nektos](https://github.com/nektos).

### Test the Action Locally

Run the following command to simulate a pull request event:

```sh
act pull_request --container-architecture linux/amd64 --secret-file .env
```
Drop the `--container-architecture linux/amd64` if you're using a mac with Intel processors or any other Windows/Linux based machines.

This command uses the variables defined in your .env file to mimic the GitHub environment.

## GitHub Action Integration

The included GitHub Action (in .github/workflows/code_quality.yml) runs on pull requests against main or development. To use this action in another repository:
- Reference this repository as an action or copy the workflow file.
- Ensure that the target repository has the necessary secrets (GITHUB_TOKEN and OPENAI_API_KEY).

## ✅ Code Quality Checks
- Linting: Run black . and flake8 to check code formatting and style.
```sh
pre-commit run --all-files
```
- Pre-commit Hooks:
Install pre-commit hooks:
```sh
pip install pre-commit
pre-commit install
```

- Run Tests using pytest:
```sh
pytest tests/
```

## Future Enhancements
- Improve prompt engineering for better DRY/SOLID scoring.
- Add error handling and logging enhancements.
- Extend analysis to multiple programming languages.
- Integrate a Streamlit dashboard for visualization.

## 🔹 What’s New?

- 1️⃣ Configurable Analysis Weights & Focus Areas
- 2️⃣ Modular Setup via setup.sh
- 3️⃣ Local Testing with act for PR Simulations
- 4️⃣ More Robust GitHub Action Integration

This README ensures that teams can easily configure, test locally, and scale the analysis. 🚀 Let me know if you need refinements!

### Happy coding, and let’s keep our code DRY and SOLID!