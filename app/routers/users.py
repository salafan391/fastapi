from fastapi import Response,status,HTTPException,Depends,APIRouter
from .. schemas import *
from .. import models
from sqlalchemy.orm import Session
from .. database import get_db
from .. import utils
from typing import List


router = APIRouter(prefix='/users',
                   tags=['users'])


@router.post('/create_user',status_code=status.HTTP_201_CREATED,response_model=UserResponse)
def post(user:CreateUser,db:Session=Depends(get_db)):
    print(type(user.password))
    hashed_password = utils.hashing(user.password)
    print(type(hashed_password))
    user.password = hashed_password
    print(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@router.get('/',response_model=List[UserResponse])
def get_users(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/{item_id}',response_model=UserResponse)
def get_user(item_id,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==item_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"404 not found")
    return user


@router.put('/{item_id}',status_code=status.HTTP_202_ACCEPTED)
def update_user(item_id:str,user:CreateUser,db:Session=Depends(get_db)):
    hash_password = hash(user.password)
    user.password = hash_password
    update_user = db.query(models.User).filter(models.User.id==item_id)
    if update_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    update_user.update(user.model_dump(),synchronize_session=False)
    db.commit()
    return update_user.first()