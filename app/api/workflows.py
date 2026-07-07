from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.agents.orchestrator import OrchestratorAgent
from app.models.candidate import Candidate
from app.models.job import JobRequisition

router = APIRouter(prefix="/api/workflows", tags=["workflows"])
orchestrator = OrchestratorAgent()


class ResumeAnalysisRequest(BaseModel):
    resume_text: str
    candidate_email: str
    available_jobs: Optional[List[Dict[str, Any]]] = None
    interview_type: str = "technical"


class InterviewFeedbackRequest(BaseModel):
    candidate_data: Dict[str, Any]
    interview_performance: Dict[str, Any]
    job_data: Dict[str, Any]
    offer_salary: Optional[float] = None


class FullPipelineRequest(BaseModel):
    resume_text: str
    candidate_email: str
    available_job_ids: Optional[List[str]] = None
    interview_type: str = "technical"


@router.post("/analyze-resume", response_model=dict)
async def analyze_resume(
    request: ResumeAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Analyze resume and optionally match to jobs."""
    try:
        resume_analysis = await orchestrator.resume_analyzer.execute(
            resume_text=request.resume_text,
            candidate_email=request.candidate_email
        )

        if not resume_analysis.success:
            raise HTTPException(status_code=400, detail=resume_analysis.error)

        result = {
            "candidate_email": request.candidate_email,
            "resume_analysis": resume_analysis.dict()
        }

        if request.available_jobs:
            match_result = await orchestrator.job_matcher.execute(
                candidate_data=resume_analysis.data,
                available_jobs=request.available_jobs
            )
            result["job_matches"] = match_result.dict()

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/interview-feedback", response_model=dict)
async def generate_interview_feedback(
    request: InterviewFeedbackRequest,
    db: Session = Depends(get_db)
):
    """Generate feedback and salary analysis after interview."""
    try:
        result = await orchestrator.execute_interview_feedback_pipeline(
            candidate_data=request.candidate_data,
            interview_performance=request.interview_performance,
            job_data=request.job_data
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/full-pipeline", response_model=dict)
async def execute_full_pipeline(
    request: FullPipelineRequest,
    db: Session = Depends(get_db)
):
    """Execute complete hiring pipeline for a candidate."""
    try:
        available_jobs = []

        if request.available_job_ids:
            jobs = db.query(JobRequisition).filter(
                JobRequisition.id.in_(request.available_job_ids)
            ).all()
            available_jobs = [
                {
                    "id": str(job.id),
                    "title": job.title,
                    "description": job.description,
                    "required_skills": job.required_skills or [],
                    "nice_to_have_skills": job.nice_to_have_skills or [],
                    "salary_range_min": job.salary_range_min,
                    "salary_range_max": job.salary_range_max,
                    "department": job.department,
                    "location": job.location
                }
                for job in jobs
            ]
        else:
            jobs = db.query(JobRequisition).filter(
                JobRequisition.status == "open"
            ).limit(10).all()
            available_jobs = [
                {
                    "id": str(job.id),
                    "title": job.title,
                    "description": job.description,
                    "required_skills": job.required_skills or [],
                    "nice_to_have_skills": job.nice_to_have_skills or [],
                    "salary_range_min": job.salary_range_min,
                    "salary_range_max": job.salary_range_max,
                    "department": job.department,
                    "location": job.location
                }
                for job in jobs
            ]

        if not available_jobs:
            raise HTTPException(status_code=400, detail="No job positions available")

        result = await orchestrator.execute_full_pipeline(
            resume_text=request.resume_text,
            candidate_email=request.candidate_email,
            available_jobs=available_jobs,
            interview_type=request.interview_type
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/agent/{agent_name}", response_model=dict)
async def execute_agent(
    agent_name: str,
    params: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Execute a specific agent with custom parameters."""
    try:
        result = await orchestrator.execute_specific_agent(
            agent_name=agent_name,
            **params
        )

        if not result.success:
            raise HTTPException(status_code=400, detail=result.error)

        return result.dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
