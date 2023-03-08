from fastapi import HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext
import random
import re
from app.database import db_session
from app.users.user_models import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def check_names(firstname, lastname):
  if len(firstname)<3 or len(lastname)<3:
    return False
  elif re.search(r"[0-9]", firstname) or re.search(r"[0-9]", lastname):
    return False
  elif re.search(r"[.,/!@#$%*_-]", firstname) or re.search(r"[.,/!@#$%*_-]", lastname):
    return False

  return True

def check_password(password):
  """Checks if a secure is good enough."""
  if len(password) < 8:
    return False
  #            capital    lower      num        symbols
  patterns = [r"[A-Z]", r"[a-z]", r"[0-9]", r"[.,/!@#$%*_-]"]
  for pattern in patterns:
    if not re.search(pattern, password):
      return False

  return True

def check_birthday(birthday):
  birthday = datetime.strptime(birthday,"%Y-%m-%d")
  if (datetime.today()-birthday).days/365 < 18:
    return False
  return True

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
  return pwd_context.hash(password)

def checkAdmin(id):
  db=next(db_session())
  try:
    admin=db.query(Users).filter(Users.id==id).first()
    if not admin:
      raise HTTPException(status_code=400, detail="User Not Found.")
    if not admin.admin:
      raise HTTPException(status_code=400, detail="Not Authorized.")
    return True
  except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)


