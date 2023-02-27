from typing import Optional
from enum import Enum
from datetime import date
from pydantic import BaseModel
from fastapi import Query

class insertCareer(BaseModel):
    user : str=Query(..., max_length=36)
    portfolio_url : str=Query(...)
    linkedin_url : str=Query(...)
    years_experience : int=Query(...)
    job_title : str=Query(...)
    company_name : str=Query(...)

class updateCareer(BaseModel):
    portfolio_url : Optional[str]
    linkedin_url : Optional[str]
    years_experience : Optional[int]
    job_title : Optional[str]
    company_name : Optional[str]

class verifyCareer(BaseModel):
    cv_verified : Optional[bool]
    cover_letter_verified : Optional[bool]