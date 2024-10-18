# app/main.py
from fastapi import FastAPI
from app.api.v1.endpoints import papers, extract

app = FastAPI()

app.include_router(papers.router, prefix="/api/v1")
app.include_router(extract.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "ZuAI Sample Paper API"}
