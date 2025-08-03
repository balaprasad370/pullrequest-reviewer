from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from app.core.config import redis_client, celery_app
from app.tasks.analyze_pr import analyze_pr_task
from app.api.schemas import AnalyzePRRequest
import json



router = APIRouter()

@router.post("/analyze-pr")
def analyze_pr(request: AnalyzePRRequest):
    task = analyze_pr_task.delay(request.dict())
    return {"task_id": task.id}

@router.get("/status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "status": result.status}

@router.get("/results/{task_id}")
def get_results(task_id: str):
    result = redis_client.get(task_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Results not ready")
    return json.loads(result)