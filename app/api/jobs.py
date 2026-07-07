from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from app.schemas.job import JobRequisitionCreate, JobRequisitionUpdate, JobRequisitionResponse
from app.models.job import JobRequisition
from app.models.candidate import Candidate
from app.database.db import get_db
from app.agents.orchestrator import OrchestratorAgent

router = APIRouter(prefix="/api/jobs", tags=["jobs"])
orchestrator = OrchestratorAgent()


@router.post("/", response_model=JobRequisitionResponse)
async def create_job(
    job_create: JobRequisitionCreate,
    db: Session = Depends(get_db)
):
    """Create a new job requisition."""
    try:
        db_job = JobRequisition(**job_create.dict())
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{job_id}", response_model=JobRequisitionResponse)
async def get_job(
    job_id: str,
    db: Session = Depends(get_db)
):
    """Get job requisition details."""
    job = db.query(JobRequisition).filter(JobRequisition.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobRequisitionResponse)
async def update_job(
    job_id: str,
    job_update: JobRequisitionUpdate,
    db: Session = Depends(get_db)
):
    """Update a job requisition."""
    job = db.query(JobRequisition).filter(JobRequisition.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    update_data = job_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)
    return job


@router.get("/", response_model=List[JobRequisitionResponse])
async def list_jobs(
    status: str = "open",
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all job requisitions."""
    query = db.query(JobRequisition)
    if status:
        query = query.filter(JobRequisition.status == status)
    return query.offset(skip).limit(limit).all()


@router.delete("/{job_id}")
async def delete_job(
    job_id: str,
    db: Session = Depends(get_db)
):
    """Delete a job requisition."""
    job = db.query(JobRequisition).filter(JobRequisition.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(job)
    db.commit()
    return {"message": "Job deleted"}


@router.post("/{job_id}/match-candidates", response_model=dict)
async def match_candidates_to_job(
    job_id: str,
    candidate_ids: List[str],
    db: Session = Depends(get_db)
):
    """Match candidates to a specific job."""
    job = db.query(JobRequisition).filter(JobRequisition.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    candidates = db.query(Candidate).filter(Candidate.id.in_(candidate_ids)).all()
    if not candidates:
        raise HTTPException(status_code=404, detail="No candidates found")

    job_data = {
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

    results = []
    for candidate in candidates:
        candidate_data = candidate.parsed_data or {
            "name": candidate.name,
            "email": candidate.email,
            "skills": []
        }

        match_result = await orchestrator.job_matcher.execute(
            candidate_data=candidate_data,
            available_jobs=[job_data]
        )

        if match_result.success and match_result.data.get("matches"):
            results.append({
                "candidate_id": str(candidate.id),
                "candidate_name": candidate.name,
                "match_data": match_result.data["matches"][0]
            })

    return {
        "job_id": job_id,
        "job_title": job.title,
        "total_matches": len(results),
        "matches": results
    }
