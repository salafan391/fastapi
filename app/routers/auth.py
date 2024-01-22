from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database,schemas,models,utils
from sqlalchemy.orm import Session
from .oauth2 import create_access_token


router = APIRouter()

@router.post('/login',response_model=schemas.Token)
def login(user_credintials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==user_credintials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='invalid credentials')
    if not utils.verify_user(user_credintials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='invalid credentials')
    access_token = create_access_token({'user_id':user.id})
    return {'access_token':access_token,'token_type':'bearer'}



 