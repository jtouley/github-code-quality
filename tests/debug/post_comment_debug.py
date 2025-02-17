import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def post_pr_comment(comment_body):
    repo = os.getenv("REPO")  # Use REPO from .env
    pr_number = "2"  # Hardcoded PR number for testing

    if not pr_number:
        print("PR number is missing.")
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
        print("✅ Successfully posted PR comment.")
    else:
        print(f"❌ Failed to post comment: {response.status_code}")
        print("Response:", response.json())


if __name__ == "__main__":
    # Test comment for debugging
    test_comment = "🚀 This is a test comment posted via script for debugging purposes."
    post_pr_comment(test_comment)
