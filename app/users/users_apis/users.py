from fastapi import APIRouter, HTTPException, Form, UploadFile, File
import os
from app.database import db_session
from app.users import user_models
from app.users import user_schema
from sqlalchemy.orm import defer
from app.users.tools import (hash_password, check_birthday,check_names,check_password,verify_password, checkAdmin)
routes=APIRouter(
    prefix="/users",
    tags=["Users"]
)


@routes.post("/file/upload")
async def uploadDocument(
    user: str=Form(...),
    document_type: int=Form(...),
    file: UploadFile = File(...)
):
    db=next(db_session())
    try:
        file_location = os.path.join(f"../digitalid/public/uploads/user/{user}", file.filename)
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as file_object:
            file_object.write(file.file.read())
        if document_type==1:
            data={
                "id_image":file_location,
                "id_image_verified":False,
                "id_image_verification_status":"pending",
                "user_verified":False,
                "user_verification_status":"pending"
            }
        elif document_type==2:
            data={
                "selfie":file_location,
                "selfie_verified":False,
                "selfie_verification_status":"pending",
                "user_verified":False,
                "user_verification_status":"pending"
            }
        else:
            raise HTTPException(status_code=400, detail="Type does not exist.")
        doc=db.query(user_models.Users).filter(user_models.Users.id==user).update(values=data)
        #db.add(doc)
        db.commit()
        return {"info": "File uploaded successfully"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)


@routes.post("/register")
def createUser( req:user_schema.insertUser):
    db= next(db_session())
    try:
        if not check_names(req.first_name, req.last_name):
            raise HTTPException(status_code=400, detail="Firstname/Lastname not valid.")
        if not check_password(req.password):
            raise HTTPException(status_code=400, detail="Password is not secure.")
        if not check_birthday(str(req.date_of_birth)):
            raise HTTPException(status_code=400, detail="User should be at least 18 years old.")
        user=db.query(user_models.Users).filter(user_models.Users.email==req.email).first()
        if user:
            raise HTTPException(status_code=400, detail="User already exist.")
        req.first_name= req.first_name.capitalize()
        req.last_name=req.last_name.capitalize()
        req.middle_name=req.middle_name.capitalize()
        if req.password!=req.confirm_password:
            raise HTTPException(status_code=400, detail="Password doesn't matches.")
        req.password=hash_password(req.password)
        req=req.dict(exclude_none=True)
        del req["confirm_password"]
        user=user_models.Users(**req)
        db.add(user)
        db.commit()
        return {"detail":"user created"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.post("/login")
def userLogin(req:user_schema.UserLogin):
    """
    Endpoint for user to login
    """
    db=next(db_session())
    try:
        user=db.query(user_models.Users).filter(user_models.Users.email==req.email).first()
        if not user:
            raise HTTPException(status_code=400, detail="User Not Found.")
        if not verify_password(req.password,user.password):
            raise HTTPException(status_code=400, detail="Wrong password.")
        user=user.__dict__
        del user["password"]
        db.query(user_models.Users).filter(user_models.Users.email==req.email).update(values={"logged_in":True})
        db.commit()
        return user
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.post("/logout/{user_id}")
def userlogout(user_id:str):
    """
    Endpoint to logout
    """
    db=next(db_session())
    try:
        user=db.query(user_models.Users).filter(user_models.Users.id==user_id)
        if not user.first():
            raise HTTPException(status_code=400, detail="User Not Found.")
        user.update(values={"logged_in":False})
        db.commit()
        return {"detail":"logged_out"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.patch("/password")
def resetUserPassword(req:user_schema.ResetPassword):
    """
    Endpoint to reset user password.
    """
    db=next(db_session())
    try:
        user=db.query(user_models.Users).filter(user_models.Users.email==req.email, user_models.Users.id_number==req.id_number, user_models.Users.phone_number==req.phone_number)
        if not user.first():
            raise HTTPException(status_code=400, detail="User Not Found.")
        req.password=hash_password(req.password)
        user.update(values={"password":req.password})
        db.commit()
        return {"detail":"Password changed"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.get("/details/{user_id}")
def getUserDetail(user_id:str):
    """
    Endpoint to get user details
    """
    db=next(db_session())
    try:
        user=db.query(user_models.Users).filter(user_models.Users.id==user_id).options(defer("password")).first()
        if not user:
            raise HTTPException(status_code=400, detail="User Not Found.")
        return user
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.get("/all/{token}")
def getAllUsers(token:str):
    """
    Endpoint to get all users detail
    """
    db=next(db_session())
    try:
        checkAdmin(token)
        user=db.query(user_models.Users).options(defer("password")).all()
        
        return user
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)


@routes.post("/admin/assign/{user_id}/{token}")
def asssignAdmin(user_id:str, token:str):
    """
    Endpoint to assign an admin
    """
    db=next(db_session())
    try:
        checkAdmin(token)
        user=db.query(user_models.Users).filter(user_models.Users.id==user_id)
        if not user.first():
            raise HTTPException(status_code=400, detail="User Not Found.")
        user.update(values={"admin":True})
        db.commit()
        return {"detail":"assigned as admin"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.post("/admin/remove/{user_id}/{token}")
def removeAdmin(user_id:str, token:str):
    """
    Endpoint to remove an admin
    """
    db=next(db_session())
    try:
        checkAdmin(token)
        user=db.query(user_models.Users).filter(user_models.Users.id==user_id)
        if not user.first():
            raise HTTPException(status_code=400, detail="User Not Found.")
        user.update(values={"admin":False})
        db.commit()
        return {"detail":"removed as admin"}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)

@routes.patch("/verify/{user_id}/{token}")
def verifyUser(user_id:str,token:str,req:user_schema.verifyUser):
    db=next(db_session())
    try:
        checkAdmin(token)
        user=db.query(user_models.Users).filter(user_models.Users.id==user_id)
        if not user.first():
            raise HTTPException(status_code=400, detail="User does not exist.")
        id_status=""
        selfie_status=""
        if req.selfie_verified:
            selfie_status="verified"
        elif req.selfie_verified==False:
            selfie_status="rejected"
        if req.id_image_verified:
            id_status="verified"
        elif req.id_image_verified==False:
            id_status="rejected"
        data={
            **req.dict(exclude_none=True),
            "id_image_verification_status":id_status if id_status!="" else user.first().id_image_verification_status,
            "selfie_verification_status":selfie_status if selfie_status!="" else user.first().selfie_verification_status
        }
        user.update(values=data)
        db.commit()
        check_user=db.query(user_models.Users).filter(user_models.Users.id==user_id)
        if check_user.first().id_image_verified and check_user.first().selfie_verified:
            data={
                "user_verified":True,
                "user_verification_status":"verified"
            }
            check_user.update(values=data)
            db.commit()
        else:
            data={
                "user_verified":False,
                "user_verification_status":"rejected"
            }
            check_user.update(values=data)
            db.commit()
        return {"detail":"Verification updated."}
    except HTTPException as http_error:
        raise HTTPException(status_code=http_error.status_code, detail=http_error.detail)
