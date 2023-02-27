from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, Date, DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.database import Base

class Dates():
  requested_date = Column(DateTime, server_default=func.now(), nullable=False)

class Requested_docs(Base):
  __tablename__="requested_docs"

  id = Column(Integer, primary_key=True, index=True)
  user = Column(String(36), nullable=False)
  requested_date = Column(Date)
  expected_date = Column(Date)
  document_type = Column(Integer)
  comment = Column(String(500))
  status = Column(String(50))
