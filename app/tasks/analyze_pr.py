from app.core.config import redis_client, celery_app
from app.core.github_utils import fetch_github_pr_files
from app.ai.agent import run_ai_agent
import json

@celery_app.task(bind=True)
def analyze_pr_task(self, data):
    taskDetails = {
        "task_id": self.request.id,
        "status": "Not Valid Request",
        "results": {}
    }
    try:
        # Validate required fields
        if not all(key in data for key in ["repo_url", "pr_number"]):
            raise ValueError("Missing required fields: repo_url and pr_number")
            
        repo_url = data["repo_url"]
        pr_number = data["pr_number"] 
        token = data.get("github_token")
        taskDetails.update({
            "status": "processing"
        })

        
        redis_client.set(self.request.id, json.dumps(taskDetails))
        files = fetch_github_pr_files(repo_url, pr_number, token, self.request.id)
        report = run_ai_agent(files)
        
        taskDetails.update({
            "results": report,
            "status": "completed"
        })
        
        redis_client.set(self.request.id, json.dumps(taskDetails))
        return taskDetails
        
    except Exception as e:
        taskDetails.update({
            "status": "failed",
            "error": str(e)
        })
        redis_client.set(self.request.id, json.dumps(taskDetails))
        raise