# 🧠 Autonomous Code Review Agent

An AI-powered system that automatically reviews GitHub pull requests for **style**, **bugs**, **performance issues**, and **best practices**.

---

## ✨ Features

- Analyze public GitHub PRs using OpenAI
- Detect style violations, bugs, and code smells
- Asynchronous task handling via Celery + Redis
- RESTful API built with FastAPI
- Dockerized for easy setup and deployment

---

## ⚙️ Tech Stack

- **FastAPI** – API server  
- **Celery** – Asynchronous task queue  
- **Redis** – Message broker for Celery  
- **Docker** – Containerization  
- **OpenAI API** – AI-based code review  
- **GitHub API** – Fetch PR diff for analysis  

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/balaprasad370/pullrequest-reviewer
cd pullrequest-reviewer
```

---

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your own credentials:

```env
REDIS_URL=redis://localhost:6379/0
GITHUB_TOKEN=your_github_token_here
OPENAI_TOKEN=your_openai_token
```

> 🔑 `GITHUB_TOKEN`: A GitHub personal access token (for accessing PRs)  
> 🤖 `OPENAI_TOKEN`: Your OpenAI API key  
> 🛠️ `REDIS_URL`: Local Redis URL used by Celery (default is fine for local Docker setup)

---

### 3. Build and Run Locally

Start the system with:

```bash
docker-compose up --build
```

This runs:
- `FastAPI` server at [http://localhost:8000](http://localhost:8000)
- `Celery` worker in a background container
- `Redis` broker service

---

## 📬 API Endpoints

### 🔹 `POST /analyze-pr`

Submits a GitHub pull request for AI-based code review.

#### Example:
```bash
curl -X POST http://localhost:8000/analyze-pr   -H "Content-Type: application/json"   -d '{"repo_url":"https://github.com/user/repo","pr_number":1}'
```

---

### 🔹 `POST /status/{task_id}`

Checks the status of a background task.

#### Example:
```bash
curl -X POST http://localhost:8000/status/abc123
```

---

### 🔹 `GET /results/{task_id}`

Fetches the results of a completed analysis.

#### Example:
```bash
curl http://localhost:8000/results/abc123
```

---

## 🧪 Example `.env` File

```env
REDIS_URL=redis://localhost:6379/0
GITHUB_TOKEN=your_github_token_here
OPENAI_TOKEN=your_openai_token
```

---

## 🛠 Notes

- Only public GitHub repositories are supported
- OpenAI API usage may incur costs — monitor your API usage
- All tasks are processed asynchronously using Celery workers
- The backend is fully containerized for easy local or cloud deployment

---
