from fastapi import APIRouter, HTTPException, File, UploadFile, Form
import os
from app.database import db_session
from app.users import career_models as models
from app.users import careers_schemas as schemas
from sqlalchemy.orm import defer

routes=APIRouter(
    prefix="/career",
    tags=["Career"]
)

@routes.post("/file/upload")
async def uploadDocument(
    user: str=Form(...),
    career_id:int=Form(...),
    document_type: int=Form(...),
    file: UploadFile = File(...)
):
    db=next(db_session())
    try:
        file_location = os.path.join(f"uploads/career/{user}", file.filename)
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as file_object:
            file_object.write(file.file.read())
        if document_type==1:
            data={"cv":file_location}
        elif document_type==2:
            data={"cover_letter":file_location}
        else:
            raise HTTPException(status_code=400, detail="Type does not exist.")
        doc=db.query(models.Career).filter(models.Career.id==career_id).update(values=data)
        #db.add(doc)
        db.commit()
        return {"info": "File uploaded successfully"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)


@routes.post("/create")
def createCareer(req:schemas.insertCareer):
    db=next(db_session())
    try:
        career=models.Career(**req.dict(exclude_none=True))
        db.add(career)
        db.commit()
        return {"detail":"career created"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.get("/all")
def getAllCareers():
    db=next(db_session())
    try:
        career=db.query(models.Career).order_by(models.Career.id.desc()).all()
        return {"detail":career}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.get("/{user_id}")
def getUserCareer(user_id:str):
    db=next(db_session())
    try:
        career=db.query(models.Career).filter(models.Career.user==user_id).order_by(models.Career.id.desc()).all()

        return {"detail":career}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.patch("/{career_id}")
def updateUserCareer(career_id:int, req:schemas.updateCareer):
    db=next(db_session())
    try:
        career=db.query(models.Career).filter(models.Career.id==career_id)
        if not career.first():
            raise HTTPException(status_code=400, detail="Career does not exist.")
        career.update(values=req.dict(exclude_none=True))
        return {"detail":"Career Updated"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.delete("/{career_id}")
def deleteCareer(career_id:int):
    db=next(db_session())
    try:
        career=db.query(models.Career).filter(models.Career.id==career_id)
        if not career.first():
            raise HTTPException(status_code=400, detail="Career does not exist.")
        career.delete()
        db.commit()
        return {"detail":"Career delete"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)
