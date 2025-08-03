# Autonomous Code Review Agent

## Features
- Analyze GitHub PRs using AI (style, bugs, performance, best practices)
- Async task handling using Celery + Redis
- API: /analyze-pr, /status/{task_id}, /results/{task_id}
- Dockerized setup



## Setup

1. Clone the repository:

```bash
git clone https://github.com/balaprasad370/pullrequest-reviewer
cd pullrequest-reviewer
```

and then  

```bash
docker-compose up --build
```

## Example Request
```bash
curl -X POST http://localhost:8000/analyze-pr -H "Content-Type: application/json" -d '{"repo_url":"https://github.com/user/repo","pr_number":1}'
```