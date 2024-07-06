import subprocess
import json
import openai
import os
import argparse

def run_shell_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {command}\n{result.stderr}")
    return result.stdout.strip()

def get_changed_files(pr_number, repo):
    command = f"gh pr view {sanitize_input(pr_number)} --repo {sanitize_input(repo)} --json files"
    output = run_shell_command(command)
    pr_data = json.loads(output)
    return [file['path'] for file in pr_data['files']]

def get_file_diff(file_path):
    command = f"git diff HEAD~1 {sanitize_input(file_path)}"
    return run_shell_command(command)

def generate_summary(changes, max_tokens=150):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise Exception("OPENAI_API_KEY environment variable not set")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following changes:\n\n{changes}"}
        ],
        max_tokens=max_tokens
    )
    return response.choices[0].message['content'].strip()

def sanitize_input(input_str):
    return input_str.replace("'", "'\\''")

def update_pr_description(pr_number, repo, short_summary):
    sanitized_summary = sanitize_input(short_summary)
    command = f"gh pr edit {sanitize_input(pr_number)} --repo {sanitize_input(repo)} --body '{sanitized_summary}'"
    run_shell_command(command)

def post_pr_comment(pr_number, repo, long_summary):
    sanitized_summary = sanitize_input(long_summary)
    command = f"gh pr comment {sanitize_input(pr_number)} --repo {sanitize_input(repo)} --body '{sanitized_summary}'"
    run_shell_command(command)

def main(pr_number, repo):
    try:
        # Input validation for PR number and repository name
        if not pr_number.isdigit():
            raise ValueError("Invalid pull request number. It should be a numeric value.")
        if '/' not in repo or len(repo.split('/')) != 2:
            raise ValueError("Invalid repository name. It should be in the format 'owner/repo'.")

        changed_files = get_changed_files(pr_number, repo)
        all_changes = ""
        for file in changed_files:
            diff = get_file_diff(file)
            all_changes += f"Changes in {file}:\n{diff}\n\n"

        short_summary = generate_summary(all_changes, max_tokens=50)
        long_summary = generate_summary(all_changes, max_tokens=300)

        update_pr_description(pr_number, repo, short_summary)
        post_pr_comment(pr_number, repo, long_summary)

        print("Short summary appended to PR description.")
        print("Long summary posted as a comment.")
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except openai.error.OpenAIError as oae:
        print(f"OpenAI API Error: {oae}")
    except json.JSONDecodeError as jde:
        print(f"JSON Parsing Error: {jde}")
    except subprocess.CalledProcessError as cpe:
        print(f"Subprocess Error: {cpe}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize pull request changes using OpenAI's GPT model.")
    parser.add_argument("--pr-number", required=True, help="The pull request number.")
    parser.add_argument("--repo", required=True, help="The repository in the format 'owner/repo'.")
    args = parser.parse_args()

    main(args.pr_number, args.repo)
