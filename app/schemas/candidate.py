from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    location: Optional[str] = None
    resume_text: str


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    parsed_data: Optional[Dict[str, Any]] = None
    job_matches: Optional[Dict[str, Any]] = None
    interview_prep: Optional[Dict[str, Any]] = None
    feedback: Optional[Dict[str, Any]] = None
    salary_analysis: Optional[Dict[str, Any]] = None


class CandidateResponse(CandidateBase):
    id: UUID
    resume_url: Optional[str]
    parsed_data: Optional[Dict[str, Any]]
    job_matches: Optional[Dict[str, Any]]
    interview_prep: Optional[Dict[str, Any]]
    feedback: Optional[Dict[str, Any]]
    salary_analysis: Optional[Dict[str, Any]]
    status: str
    quality_score: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
