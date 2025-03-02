import os
from src.analyzer import analyze_repo
from src.config_loader import load_config
import requests


def get_analysis_feedback():
    """Fetches analysis feedback, prioritizing fresh results but falling back to a cached file."""
    config = load_config()
    format_config = config.get("feedback_format", {})

    try:
        analysis_results = analyze_repo()
        if analysis_results:
            feedback = ""
            for file, result in analysis_results.items():
                feedback += format_config.get("message_template", "").format(
                    file=file,
                    dry_score=result.get("dry_score", "N/A"),
                    dry_analysis=result.get("full_analysis", "No analysis available."),
                    solid_score=result.get("solid_score", "N/A"),
                    solid_analysis=result.get(
                        "full_analysis", "No analysis available."
                    ),
                )
            return feedback
    except Exception as e:
        print(f"Error fetching fresh analysis, falling back to cached file: {e}")

    # Fall back to file-based approach if necessary
    feedback_file = "analysis_feedback.md"
    if os.path.exists(feedback_file):
        with open(feedback_file, "r") as f:
            return f.read()

    return "No analysis feedback generated."


def post_pr_comment(comment_body):
    """Posts a comment to a GitHub Pull Request containing the analysis feedback."""
    repo = os.getenv("GITHUB_REPOSITORY")  # e.g., "myorg/myrepo"
    ref = os.getenv("GITHUB_REF", "")  # e.g., "refs/pull/123/merge"
    pr_number = ref.split("/")[2] if "pull" in ref else None

    if not pr_number:
        print("No PR number found. Is this running in a pull request context?")
        return

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN is not set in the environment.")

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
    }
    payload = {"body": comment_body}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Successfully posted PR comment.")
    else:
        print("Failed to post comment:", response.json())


if __name__ == "__main__":
    # Fetch analysis feedback dynamically and post it to the PR
    analysis_feedback = get_analysis_feedback()
    post_pr_comment(analysis_feedback)
