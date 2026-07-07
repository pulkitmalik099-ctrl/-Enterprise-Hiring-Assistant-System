from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class JobRequisitionBase(BaseModel):
    title: str
    description: str
    required_skills: Optional[List[str]] = None
    nice_to_have_skills: Optional[List[str]] = None
    required_experience_years: Optional[int] = None
    location: Optional[str] = None
    salary_range_min: Optional[float] = None
    salary_range_max: Optional[float] = None
    department: Optional[str] = None


class JobRequisitionCreate(JobRequisitionBase):
    pass


class JobRequisitionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    nice_to_have_skills: Optional[List[str]] = None
    required_experience_years: Optional[int] = None
    location: Optional[str] = None
    salary_range_min: Optional[float] = None
    salary_range_max: Optional[float] = None
    department: Optional[str] = None
    status: Optional[str] = None


class JobRequisitionResponse(JobRequisitionBase):
    id: UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
