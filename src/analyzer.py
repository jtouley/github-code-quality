import os
import json
import re
from dotenv import load_dotenv
from src.github_client import GitHubClient
from src.ai_client import AIClient
from src.config_loader import load_config
from src.utils import log

load_dotenv()  # Loads environment variables from .env if available


class AnalysisResultHandler:
    """Handles analysis results processing and storage."""

    def __init__(self, output_file="analysis_feedback.md"):
        self.output_file = output_file
        self.config = load_config()

    def extract_scores(self, response_text):
        """Extracts DRY and SOLID scores (1-10) from OpenAI's response."""
        dry_match = re.search(
            r"### DRY Analysis\n\*\*Score:\s*(\d+)/10\*\*", response_text
        )
        solid_match = re.search(
            r"### SOLID Analysis\n\*\*Score:\s*(\d+)/10\*\*", response_text
        )

        dry_score = int(dry_match.group(1)) if dry_match else None
        solid_score = int(solid_match.group(1)) if solid_match else None

        return dry_score, solid_score

    def format_result(self, path, analysis):
        """Creates a formatted result object from the analysis text."""
        dry_score, solid_score = self.extract_scores(analysis)

        return {
            "dry_score": dry_score if dry_score is not None else "N/A",
            "solid_score": solid_score if solid_score is not None else "N/A",
            "full_analysis": analysis,
        }

    def save_results(self, results):
        """Saves analysis results to the output file."""
        with open(self.output_file, "w") as f:
            for file, feedback in results.items():
                f.write(f"## Analysis for {file}\n")
                f.write(json.dumps(feedback, indent=2) + "\n\n")

        log(f"Analysis results saved to {self.output_file}")
        return results


class CodeAnalyzer:
    """Handles code analysis operations."""

    def __init__(self):
        self.env_vars = self._validate_environment()
        if not self.env_vars:
            return

        self.github_client = GitHubClient(self.env_vars["repo"])
        self.ai_client = AIClient()
        self.result_handler = AnalysisResultHandler()

    def _validate_environment(self):
        """Validates required environment variables."""
        if os.getenv("ENABLE_ANALYSIS", "true").lower() != "true":
            log("Code analysis is disabled. Exiting.")
            return None

        repo_name = os.getenv("REPO")
        if not repo_name:
            log("REPO environment variable is not set.")
            return None

        return {"repo": repo_name}

    def prepare_code_for_analysis(self, code):
        """Prepares code for analysis by wrapping it in markdown code blocks."""
        return f"```\n{code}\n```"

    def analyze_file(self, path, code):
        """Analyzes a single file and returns the formatted results."""
        prompt_code = self.prepare_code_for_analysis(code)
        analysis = self.ai_client.analyze_code(prompt_code)
        return self.result_handler.format_result(path, analysis)

    def analyze_repo(self):
        """Main method to analyze the entire repository."""
        if not self.env_vars:
            return {}

        files = self.github_client.get_files()
        results = {}

        for path, code in files:
            results[path] = self.analyze_file(path, code)

        # Save results and also return them for programmatic use
        return self.result_handler.save_results(results)


def analyze_repo():
    """Entry point function that returns analysis results."""
    analyzer = CodeAnalyzer()
    return analyzer.analyze_repo()


if __name__ == "__main__":
    analyze_repo()
