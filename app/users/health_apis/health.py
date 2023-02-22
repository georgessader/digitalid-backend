from fastapi import APIRouter, HTTPException, File, UploadFile,Form
import os
from app.database import db_session
from app.users import health_models as models
from app.users import health_schemas as schemas
from sqlalchemy.orm import defer

routes=APIRouter(
    prefix="/health",
    tags=["Health"]
)

@routes.post("/file/upload")
async def uploadDocument(
    user: str=Form(...),
    health_id:int=Form(...),
    document_type: int=Form(...),
    expiry_date: str=Form(None),
    file: UploadFile = File(...)
):
    db=next(db_session())
    try:
        file_location = os.path.join(f"uploads/health/{user}", file.filename)
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as file_object:
            file_object.write(file.file.read())
        if document_type==1:
            data={"health_report":file_location}
        elif document_type==2:
            data={"vaccination_report":file_location}
        elif document_type==3:
            if not expiry_date:
                raise HTTPException(status_code=400, detail="Expiry Date is required.")
            data={"insurance_doc":file_location,"insurance_expiry_date":expiry_date}
        else:
            raise HTTPException(status_code=400, detail="Type does not exist.")
        doc=db.query(models.Health).filter(models.Health.id==health_id).update(values=data)
        #db.add(doc)
        db.commit()
        return {"info": "File uploaded successfully"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)


@routes.post("/create")
def createHealth(req:schemas.insertHealth):
    db=next(db_session())
    try:
        health=models.Health(**req.dict(exclude_none=True))
        db.add(health)
        db.commit()
        return {"detail":"health created"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.get("/all")
def getAllHealth():
    db=next(db_session())
    try:
        health=db.query(models.Health).order_by(models.Health.id.desc()).all()
        return {"detail":health}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.get("/{user_id}")
def getUserHealth(user_id:str):
    db=next(db_session())
    try:
        health=db.query(models.Health).filter(models.Health.user==user_id).order_by(models.Health.id.desc()).all()

        return {"detail":health}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.patch("/{health_id}")
def updateUserHealth(health_id:int, req:schemas.updateHealth):
    db=next(db_session())
    try:
        health=db.query(models.Health).filter(models.Health.id==health_id)
        if not health.first():
            raise HTTPException(status_code=400, detail="Health does not exist.")
        health.update(values=req.dict(exclude_none=True))
        return {"detail":"Health Updated"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.delete("/{health_id}")
def deleteEducation(health_id:int):
    db=next(db_session())
    try:
        health=db.query(models.Health).filter(models.Health.id==health_id)
        if not health.first():
            raise HTTPException(status_code=400, detail="Health does not exist.")
        health.delete()
        db.commit()
        return {"detail":"Health delete"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)
