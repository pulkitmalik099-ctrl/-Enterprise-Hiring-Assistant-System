from sqlalchemy import Column, String, DateTime, Float, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.database.db import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    location = Column(String(255))

    resume_text = Column(Text, nullable=False)
    resume_url = Column(String(500))

    parsed_data = Column(JSON)
    job_matches = Column(JSON)
    interview_prep = Column(JSON)
    feedback = Column(JSON)
    salary_analysis = Column(JSON)

    status = Column(String(50), default="submitted")
    quality_score = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
