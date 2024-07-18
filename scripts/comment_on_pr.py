import os
import requests
import logging


logging.basicConfig(level=logging.INFO)


def post_comment(owner, repo, issue_number, comment_body, token):
    """
    Posts a comment to a pull request on GitHub.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {"body": comment_body}
    response = requests.post(url, json=data, headers=headers)
    return response.status_code


if __name__ == "__main__":
    github_token = os.getenv("INPUT_GH_TOKEN")
    repository = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("INPUT_PR_NUMBER")
    comment = "Thank you for your pull request! We will review it soon."

    owner, repo = repository.split("/")
    status_code = post_comment(owner, repo, pr_number, comment, github_token)

    if status_code == 201:
        logging.info("Comment posted successfully!")
    else:
        logging.info("Failed to post comment. Status code:", status_code)
