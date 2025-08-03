import requests
from app.core.config import redis_client
import json
import os
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_github_pr_files(repo_url, pr_number, token, task_id):
    taskDetails = json.loads(redis_client.get(task_id))
    taskDetails["status"] = "processing"
    redis_client.set(task_id, json.dumps(taskDetails))
    if(token is None):
        token = GITHUB_TOKEN
    owner_repo = repo_url.split("github.com/")[-1]
    api_url = f"https://api.github.com/repos/{owner_repo}/pulls/{pr_number}/files"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(api_url, headers=headers)
    response.raise_for_status()

    files = response.json()
    return [
        {
            "filename": f["filename"],
            "patch": f.get("patch", "")  # The code diff
        } for f in files
    ]
