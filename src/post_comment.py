import os
import requests
from src.analyzer import analyze_repo
from src.config_loader import load_config
from src.utils import log


class FeedbackFormatter:
    """Formats analysis feedback according to configuration."""

    def __init__(self):
        self.config = load_config()
        self.format_config = self.config.get("feedback_format", {})

    def format_file_feedback(self, file, result):
        """Formats feedback for a single file according to the template."""
        template = self.format_config.get("message_template", "")

        return template.format(
            file=file,
            dry_score=result.get("dry_score", "N/A"),
            dry_analysis=result.get("full_analysis", "No analysis available."),
            solid_score=result.get("solid_score", "N/A"),
            solid_analysis=result.get("full_analysis", "No analysis available."),
        )

    def format_all_feedback(self, results):
        """Formats feedback for all analyzed files."""
        if not results:
            return "No analysis feedback generated."

        feedback = ""
        for file, result in results.items():
            feedback += self.format_file_feedback(file, result)

        return feedback


class FeedbackProvider:
    """Provides analysis feedback from various sources."""

    def __init__(self):
        self.formatter = FeedbackFormatter()

    def get_from_analysis(self):
        """Gets feedback by running a fresh analysis."""
        try:
            results = analyze_repo()
            if results:
                return self.formatter.format_all_feedback(results)
        except Exception as e:
            log(f"Error fetching fresh analysis: {e}")
            return None

    def get_from_file(self, filename="analysis_feedback.md"):
        """Gets feedback from a cached file."""
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    return f.read()
            except Exception as e:
                log(f"Error reading feedback file: {e}")

        return None

    def get_feedback(self):
        """Gets feedback, prioritizing fresh analysis but falling back to cached file."""
        # Try to get fresh analysis first
        feedback = self.get_from_analysis()

        # If that fails, try to get from file
        if not feedback:
            feedback = self.get_from_file()

        # If both fail, return a default message
        if not feedback:
            feedback = "No analysis feedback generated."

        return feedback


class GitHubPRCommenter:
    """Handles posting comments to GitHub PRs."""

    def __init__(self):
        self.repo = os.getenv("GITHUB_REPOSITORY")
        self.pr_number = self._extract_pr_number()
        self.token = os.getenv("GITHUB_TOKEN")

    def _extract_pr_number(self):
        """Extracts PR number from GitHub environment variables."""
        ref = os.getenv("GITHUB_REF", "")
        if not ref or "pull" not in ref:
            return None

        try:
            return ref.split("/")[2]
        except (IndexError, TypeError):
            log(f"Could not extract PR number from reference: {ref}")
            return None

    def _validate(self):
        """Validates that all required information is available."""
        if not self.pr_number:
            log("No PR number found. Is this running in a pull request context?")
            return False

        if not self.token:
            log("GITHUB_TOKEN is not set in the environment.")
            return False

        if not self.repo:
            log("GITHUB_REPOSITORY is not set in the environment.")
            return False

        return True

    def post_comment(self, comment_body):
        """Posts a comment to a GitHub Pull Request."""
        if not self._validate():
            return False

        url = (
            f"https://api.github.com/repos/{self.repo}/issues/{self.pr_number}/comments"
        )
        headers = {
            "Authorization": f"token {self.token}",
            "Content-Type": "application/json",
        }
        payload = {"body": comment_body}

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                log("Successfully posted PR comment.")
                return True
            else:
                log(f"Failed to post comment: {response.status_code} {response.json()}")
                return False
        except Exception as e:
            log(f"Error posting PR comment: {e}")
            return False


def post_pr_comment(comment_body=None):
    """Main function to post analysis feedback as a PR comment."""
    # If no comment body is provided, get it from the feedback provider
    if comment_body is None:
        provider = FeedbackProvider()
        comment_body = provider.get_feedback()

    # Post the comment to the PR
    commenter = GitHubPRCommenter()
    return commenter.post_comment(comment_body)


def get_analysis_feedback():
    """Entry point to get analysis feedback."""
    provider = FeedbackProvider()
    return provider.get_feedback()


if __name__ == "__main__":
    # Fetch analysis feedback dynamically and post it to the PR
    feedback = get_analysis_feedback()
    post_pr_comment(feedback)
