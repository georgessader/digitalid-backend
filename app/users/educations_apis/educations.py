from fastapi import APIRouter, HTTPException, File, UploadFile,Form
from app.database import db_session
from app.users import education_models as models
from app.users import education_schema as schemas
from sqlalchemy.orm import defer
import os
routes=APIRouter(
    prefix="/educations",
    tags=["Educations"]
)


@routes.post("/file/upload")
async def uploadDocument(
    user: str=Form(...),
    education_id:int=Form(...),
    document_type: int=Form(...),
    file: UploadFile = File(...)
):
    db=next(db_session())
    try:
        file_location = os.path.join(f"uploads/education/{user}", file.filename)
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as file_object:
            file_object.write(file.file.read())
        if document_type==1:
            data={
                "grades":file_location,
                "grade_verified":False,
                "grade_verification_status":"pending",
                "education_verified":False,
                "education_verification_status":"pending"
            }
        elif document_type==2:
            data={
                "certificate":file_location,
                "certificate_verified":False,
                "certificate_verification_status":"pending",
                "education_verified":False,
                "education_verification_status":"pending"
            }
        else:
            raise HTTPException(status_code=400, detail="Type does not exist.")
        doc=db.query(models.Education).filter(models.Education.id==education_id).update(values=data)
        #db.add(doc)
        db.commit()
        return {"info": "File uploaded successfully"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)


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

@routes.patch("/verify/{user_id}")
def verifyEducation(user_id:str,req:schemas.verifyEducation):
    db=next(db_session())
    try:
        education=db.query(models.Education).filter(models.Education.user==user_id)
        if not education.first():
            raise HTTPException(status_code=400, detail="Education does not exist.")
        grade_status=""
        certificate_status=""
        if req.grade_verified:
            grade_status="verified"
        elif req.grade_verified==False:
            grade_status="rejected"
        if req.certificate_verified:
            certificate_status="verified"
        elif req.certificate_verified==False:
            certificate_status="rejected"
        data={
            **req.dict(exclude_none=True),
            "grade_verification_status":grade_status if grade_status!="" else education.first().grade_verification_status,
            "certificate_verification_status":certificate_status if certificate_status!="" else education.first().certificate_verification_status
        }
        education.update(values=data)
        db.commit()
        check_verification=db.query(models.Education).filter(models.Education.user==user_id)
        if check_verification.first().grade_verified and check_verification.first().certificate_verified:
            data={
                "education_verified":True,
                "education_verification_status":"verified"
            }
            check_verification.update(values=data)
            db.commit()
        else:
            data={
                "education_verified":False,
                "education_verification_status":"Rejected"
            }
            check_verification.update(values=data)
            db.commit()
        return {"detail":"Verification updated."}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

