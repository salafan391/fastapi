from datetime import datetime,timedelta
from jose import JWTError,jwt
from .. import schemas
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from .. import config


oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY=config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=config.settings.access_token_expire_minutes


def create_access_token(data:dict):
    to_encode=data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        id:str=payload.get('user_id')
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(token_id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail={'message':'not validate credentials'},
                                          headers={'WWW-Authenticate':'Bearer'})
    return verify_access_token(token,credentials_exception)





