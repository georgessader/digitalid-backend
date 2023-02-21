from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, Date, DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.database import Base

class Education(Base):
    __tablename__="educations"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(36), nullable=False)
    type = Column(Integer)
    major = Column(String(200))
    grades = Column(String(500))
    certificate = Column(String(500))
    credits_completed = Column(Integer)
    gpa = Column(Float)
    college_name = Column(String(200))
    grade_verified = Column(Boolean)
    grade_verification_status = Column(String(50))
    certificate_verified = Column(Boolean)
    certificate_verification_status = Column(String(50))
    education_verified = Column(Boolean)
    education_verification_status = Column(String(50))
