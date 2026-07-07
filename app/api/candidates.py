from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateResponse
from app.models.candidate import Candidate
from app.database.db import get_db
from app.agents.orchestrator import OrchestratorAgent

router = APIRouter(prefix="/api/candidates", tags=["candidates"])
orchestrator = OrchestratorAgent()


@router.post("/upload", response_model=dict)
async def upload_candidate(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and analyze a candidate resume."""
    try:
        content = await file.read()
        resume_text = content.decode('utf-8')

        candidate_data = CandidateCreate(
            name="Uploaded Candidate",
            email=file.filename or "candidate@example.com",
            resume_text=resume_text
        )

        db_candidate = Candidate(**candidate_data.dict())
        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)

        result = await orchestrator.resume_analyzer.execute(
            resume_text=resume_text,
            candidate_email=db_candidate.email
        )

        if result.success:
            db_candidate.parsed_data = result.data
            db.commit()

        return {
            "candidate_id": str(db_candidate.id),
            "analysis": result.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/analyze", response_model=dict)
async def analyze_candidate(
    candidate_create: CandidateCreate,
    db: Session = Depends(get_db)
):
    """Analyze a candidate's resume."""
    try:
        db_candidate = Candidate(**candidate_create.dict())
        db.add(db_candidate)
        db.commit()
        db.refresh(db_candidate)

        result = await orchestrator.resume_analyzer.execute(
            resume_text=candidate_create.resume_text,
            candidate_email=candidate_create.email
        )

        if result.success:
            db_candidate.parsed_data = result.data
            db.commit()

        return {
            "candidate_id": str(db_candidate.id),
            "analysis": result.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: str,
    db: Session = Depends(get_db)
):
    """Get candidate details."""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: str,
    candidate_update: CandidateUpdate,
    db: Session = Depends(get_db)
):
    """Update candidate information."""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    update_data = candidate_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(candidate, field, value)

    db.commit()
    db.refresh(candidate)
    return candidate


@router.get("/", response_model=List[CandidateResponse])
async def list_candidates(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """List all candidates."""
    return db.query(Candidate).offset(skip).limit(limit).all()


@router.delete("/{candidate_id}")
async def delete_candidate(
    candidate_id: str,
    db: Session = Depends(get_db)
):
    """Delete a candidate."""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    db.delete(candidate)
    db.commit()
    return {"message": "Candidate deleted"}
