from datetime import datetime, timedelta
from jose import JWTError, jwt
from . import schemas
from .config import settings

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        citizen_id: str = payload.get("sub")
        if citizen_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(citizen_id=citizen_id)
        return token_data
    except JWTError:
        raise credentials_exception