from typing import Optional
from enum import Enum
from datetime import date
from pydantic import BaseModel
from fastapi import Query

class insertUser(BaseModel):
    first_name: str=Query(None, max_length=75)
    middle_name: str=Query(None, max_length=75)
    last_name: str=Query(None, max_length=75)
    email: str=Query(... , min_length=1,max_length=199, regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    phone_number: str=Query(
        None, min_length=1, max_length=20,
        regex="^\+?\d{8,20}$"
    )
    date_of_birth: date=Query(...)
    place_of_birth: str=Query(...)
    country: str=Query(...)
    city:  str=Query(...)
    postal_code: str=Query(...)
    district: str=Query(...)
    id_number: str=Query(...)
    password: str=Query(..., min_length=1, max_length=128)
    confirm_password: str=Query(..., min_length=1, max_length=128)

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str=Query(... , min_length=1,max_length=199, regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    password: str=Query(..., min_length=1, max_length=128)

    class Config:
        orm_mode = True

class ResetPassword(BaseModel):
    email: str=Query(... , min_length=1,max_length=199, regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    phone_number: str=Query(
        None, min_length=1, max_length=20,
        regex="^\+?\d{8,20}$"
    )
    id_number: str=Query(...)
    password: str=Query(..., min_length=1, max_length=128)