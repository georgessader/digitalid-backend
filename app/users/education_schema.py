from typing import Optional
from enum import Enum
from datetime import date
from pydantic import BaseModel
from fastapi import Query

class insertEducation(BaseModel):
    user : str=Query(..., max_length=36)
    type : int=Query(...)
    major : str=Query(...)
    credits_completed : Optional[int]
    gpa: Optional[float]
    college_name : str=Query(...)

class updateEducation(BaseModel):
    type : Optional[int]
    major : Optional[str]
    credits_completed : Optional[int]
    gpa: Optional[float]
    college_name : Optional[str]

class verifyEducation(BaseModel):
    education_id : int=Query(...)
    grade_verified : Optional[bool]
    certificate_verified : Optional[bool]

    