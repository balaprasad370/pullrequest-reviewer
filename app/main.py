from fastapi import FastAPI
from app.api.endpoints import router

app = FastAPI(title="Code Review Agent")
app.include_router(router)