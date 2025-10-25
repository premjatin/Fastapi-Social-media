from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas, utils, oauth2
from app.database import get_db
router = APIRouter(tags=["Authentication"])

@router.post("/login",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(),db: Session= Depends(get_db)):
    
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail=" Invalid Credentials")
    print("Password type:", type(user_credentials.password))
    print("Password value:", repr(user_credentials.password))
    print("DB hash:", user.password)
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail=" Invalid Credentials")
    access_token=oauth2.create_access_token(data={"user_id":user.id})
    
    return {"access_token":access_token,"token_type":"bearer"}

