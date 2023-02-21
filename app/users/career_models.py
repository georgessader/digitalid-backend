from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, Date, DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.database import Base

class Career(Base):
    __tablename__="career"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(36), nullable=False)
    cv = Column(String(500))
    cover_letter = Column(String(500))
    portfolio_url = Column(String(500))
    linkedin_url = Column(String(500))
    years_experience = Column(Integer)
    job_title = Column(String(200))
    company_name = Column(String(200))
    cv_verified = Column(Boolean)
    cv_verification_status = Column(String(50))
    cover_letter_verified = Column(Boolean)
    cover_letter_verification_status = Column(String(50))
    career_verified = Column(Boolean)
    career_verification_status = Column(String(50))
