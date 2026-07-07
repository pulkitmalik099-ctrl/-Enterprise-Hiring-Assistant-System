import pytest
from sqlalchemy.orm import Session
from app.models.candidate import Candidate
from app.models.job import JobRequisition
from app.database.db import SessionLocal


def test_candidate_model_creation():
    db = SessionLocal()
    try:
        candidate = Candidate(
            name="John Doe",
            email="john@example.com",
            phone="123-456-7890",
            location="New York",
            resume_text="Sample resume text",
            status="submitted"
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        assert candidate.id is not None
        assert candidate.name == "John Doe"
        assert candidate.email == "john@example.com"
        assert candidate.status == "submitted"
    finally:
        db.close()


def test_job_requisition_model_creation():
    db = SessionLocal()
    try:
        job = JobRequisition(
            title="Senior Software Engineer",
            description="Looking for experienced engineer",
            required_skills=["Python", "FastAPI", "PostgreSQL"],
            location="San Francisco",
            salary_range_min=150000,
            salary_range_max=200000,
            department="Engineering",
            status="open"
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        assert job.id is not None
        assert job.title == "Senior Software Engineer"
        assert job.salary_range_min == 150000
        assert job.status == "open"
    finally:
        db.close()
