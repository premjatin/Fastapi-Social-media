from app import utils
from app import models,schemas
from app.database import get_db
from fastapi import status , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router= APIRouter(prefix="/users",tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # 1. Hash the plain-text password from the incoming request
    hashed_password = utils.hash(user.password)
    
    # 2. Create a new SQLAlchemy User model instance.
    #    Do NOT modify the 'user' Pydantic model.
    #    Instead, explicitly set the email from the Pydantic model
    #    and the password to your new hashed_password.
    new_user = models.User(email=user.email, password=hashed_password)
    
    # 3. Add to the database as before
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db: Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user