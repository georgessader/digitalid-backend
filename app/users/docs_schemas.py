from typing import Optional
from enum import Enum
from datetime import date
from pydantic import BaseModel
from fastapi import Query

class requestDoc(BaseModel):
    user : str=Query(..., max_length=36)
    expected_date : date=Query(...)
    document_type : int=Query(...)
    comment : Optional[str]

class updateDoc(BaseModel):
    expected_date : Optional[date]
    document_type : Optional[int]
    comment : Optional[str]