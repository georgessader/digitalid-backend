from fastapi import APIRouter, HTTPException
from app.database import db_session
from app.users import health_models as models
from app.users import health_schemas as schemas
from sqlalchemy.orm import defer

routes=APIRouter(
    prefix="/health",
    tags=["Health"]
)

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
