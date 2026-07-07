from sqlalchemy import Column, String, DateTime, Float, JSON, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.database.db import Base

class JobRequisition(Base):
    __tablename__ = "job_requisitions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    required_skills = Column(JSON)
    nice_to_have_skills = Column(JSON)
    required_experience_years = Column(Integer)

    location = Column(String(255))
    salary_range_min = Column(Float)
    salary_range_max = Column(Float)

    department = Column(String(255))
    status = Column(String(50), default="open")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
