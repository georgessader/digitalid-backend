from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, Date, DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.database import Base

class Health(Base):
    __tablename__="health"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(36), nullable=False)
    health_report = Column(String(500))
    chronic_disease = Column(String(300))
    allergy = Column(String(300))
    vaccination_report = Column(String(500))
    nssf_number = Column(String(200))
    insurance_doc = Column(String(500))
    insurance_expiry_date = Column(Date)
    health_report_verified = Column(Boolean)
    health_report_verification_status = Column(String(50))
    vaccination_verified = Column(Boolean)
    vaccination_verification_status = Column(String(50))
    insurance_verified = Column(Boolean)
    insurance_verification_status = Column(String(50))
    health_verification = Column(Boolean)
    health_verification_status = Column(String(50))