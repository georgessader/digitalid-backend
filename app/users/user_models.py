from sqlalchemy import Boolean, Column, ForeignKey, Integer, Float, String, Date, DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.database import Base

class Dates():
  date_created = Column(DateTime, server_default=func.now(), nullable=False)
  date_modified = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

class Users(Base):
  __tablename__ = "users"

  id = Column(String(36), primary_key=True, index=True, default=uuid4)
  first_name = Column(String(100),nullable=False)
  middle_name = Column(String(100),nullable=False)
  last_name = Column(String(100),nullable=False)
  email = Column(String(200), unique=True, nullable=False)
  phone_number = Column(String(100), unique=True, nullable=False)
  date_of_birth = Column(Date, nullable=False)
  place_of_birth = Column(String(300), nullable=False)
  country = Column(String(300), nullable=False)
  city = Column(String(300), nullable=False)
  postal_code = Column(String(50), nullable=False)
  district = Column(String(300), nullable=False)
  id_image = Column(String(500))
  id_number = Column(String(150))
  selfie = Column(String(500))
  id_image_verified = Column(Boolean)
  id_image_verification_status = Column(String(50))
  selfie_verified = Column(Boolean)
  selfie_verification_status = Column(String(50))
  user_verified = Column(Boolean)
  user_verification_status = Column(String(50))
  password = Column(String(300), nullable=False)
  admin = Column(Boolean, default=False)
  logged_in = Column(Boolean, default=False)