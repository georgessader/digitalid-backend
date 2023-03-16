from typing import Optional
from enum import Enum
from datetime import date
from pydantic import BaseModel
from fastapi import Query

class insertHealth(BaseModel):
    user : str=Query(..., max_length=36)
    chronic_disease : str=Query(...)
    allergy : str=Query(...)
    nssf_number : str=Query(...)

class updateHealth(BaseModel):
    chronic_disease : Optional[str]
    allergy : Optional[str]
    nssf_number : Optional[str]

class verifyHealth(BaseModel):
    health_id : int = Query(...)
    health_report_verified : Optional[bool]
    vaccination_verified : Optional[bool]
    insurance_verified : Optional[bool]