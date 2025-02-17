import os
import requests


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
    analysis_feedback = (
        "## Code Quality Analysis Summary\n\n"
        "- **DRY:** 7/10 – Some repetition in error handling could be refactored into a common utility.\n"
        "- **SOLID:** 6/10 – The code works but could use improved modularity and dependency injection.\n\n"
        "This analysis serves as a real-world example for our team to discuss and improve our ETL/ELT pipeline design.\n"
        "Let's iterate further and aim for more maintainable, scalable code!"
    )
    post_pr_comment(analysis_feedback)
