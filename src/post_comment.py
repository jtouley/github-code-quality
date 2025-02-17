import os
import requests


def get_analysis_feedback():
    feedback_file = "analysis_feedback.md"
    if os.path.exists(feedback_file):
        with open(feedback_file, "r") as f:
            return f.read()
    else:
        return "No analysis feedback generated."


def post_pr_comment(comment_body):
    # Extract repository info and PR number from environment variables.
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
    # For demo purposes, here's a sample analysis feedback.
    analysis_feedback = get_analysis_feedback()
    post_pr_comment(analysis_feedback)
