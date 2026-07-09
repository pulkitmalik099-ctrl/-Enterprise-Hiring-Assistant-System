from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import candidates, jobs, workflows, interviews, salaries, decisions

app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-agent AI system for enterprise recruitment",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(candidates.router)
app.include_router(jobs.router)
app.include_router(workflows.router)
app.include_router(interviews.router)
app.include_router(salaries.router)
app.include_router(decisions.router)

@app.get("/")
async def root():
    return {
        "message": "Enterprise Hiring Assistant API",
        "docs": "/api/docs",
        "version": settings.APP_VERSION,
        "available_endpoints": {
            "candidates": "/api/candidates",
            "jobs": "/api/jobs",
            "interviews": "/api/interviews",
            "salaries": "/api/salaries",
            "decisions": "/api/decisions",
            "workflows": "/api/workflows"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
