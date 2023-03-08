from fastapi import APIRouter, HTTPException, File, UploadFile,Form
from app.database import db_session
from app.users import docs_models as models
from app.users import docs_schemas as schemas
from sqlalchemy.orm import defer
from datetime import datetime
from app.users.tools import checkAdmin
import os
routes=APIRouter(
    prefix="/docs",
    tags=["Docs"]
)

@routes.post("/create")
def RequestDocument(req:schemas.requestDoc):
    db=next(db_session())
    try:
        #req.status="pending"
        req_doc=models.Requested_docs(status="pending",requested_date=datetime.now(),**req.dict(exclude_none=True))
        db.add(req_doc)
        db.commit()
        return {"detail":"Document requested"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.get("/all/{token}")
def getAllRequestedDocs(token:str):
    db=next(db_session())
    try:
        checkAdmin(token)
        docs=db.query(models.Requested_docs).order_by(models.Requested_docs.expected_date.desc()).all()
        return {"detail":docs}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.get("/{user_id}")
def getUserDocs(user_id:str):
    db=next(db_session())
    try:
        docs=db.query(models.Requested_docs).filter(models.Requested_docs.user==user_id).order_by(models.Requested_docs.expected_date.desc()).all()

        return {"detail":docs}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.patch("/{doc_id}")
def updateDoc(doc_id:int, req:schemas.updateDoc):
    db=next(db_session())
    try:
        doc=db.query(models.Requested_docs).filter(models.Requested_docs.id==doc_id)
        if not doc.first():
            raise HTTPException(status_code=400, detail="Document does not exist.")
        doc.update(values=req.dict(exclude_none=True))
        return {"detail":"Doc Updated"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.delete("/{doc_id}")
def deleteEducation(doc_id:int):
    db=next(db_session())
    try:
        doc=db.query(models.Requested_docs).filter(models.Requested_docs.id==doc_id)
        if not doc.first():
            raise HTTPException(status_code=400, detail="Document does not exist.")
        doc.delete()
        db.commit()
        return {"detail":"Document deleted"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)
