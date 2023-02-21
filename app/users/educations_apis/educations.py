from fastapi import APIRouter, HTTPException
from app.database import db_session
from app.users import education_models as models
from app.users import education_schema as schemas
from sqlalchemy.orm import defer
routes=APIRouter(
    prefix="/educations",
    tags=["Educations"]
)

@routes.post("/create")
def createEducation(req:schemas.insertEducation):
    db=next(db_session())
    try:
        education=models.Education(**req.dict(exclude_none=True))
        db.add(education)
        db.commit()
        return {"detail":"education created"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.get("/all")
def getAllEducation():
    db=next(db_session())
    try:
        education=db.query(models.Education).order_by(models.Education.id.desc()).all()
        return {"detail":education}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.get("/{user_id}")
def getUserEducation(user_id:str):
    db=next(db_session())
    try:
        education=db.query(models.Education).filter(models.Education.user==user_id).order_by(models.Education.id.desc()).all()

        return {"detail":education}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.patch("/{education_id}")
def updateUserEducation(education_id:int, req:schemas.updateEducation):
    db=next(db_session())
    try:
        education=db.query(models.Education).filter(models.Education.id==education_id)
        if not education.first():
            raise HTTPException(status_code=400, detail="Education does not exist.")
        education.update(values=req.dict(exclude_none=True))
        return {"detail":"Education Updated"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.delete("/{education_id}")
def deleteEducation(education_id:int):
    db=next(db_session())
    try:
        education=db.query(models.Education).filter(models.Education.id==education_id)
        if not education.first():
            raise HTTPException(status_code=400, detail="Education does not exist.")
        education.delete()
        db.commit()
        return {"detail":"Education delete"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)
