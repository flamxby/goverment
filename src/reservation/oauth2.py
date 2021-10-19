from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from . import token, database, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user(citizen_id: str, db: Session):
    return db.query(models.User).filter(models.User.citizen_id == citizen_id).first()

def get_current_user(data: str=Depends(oauth2_scheme), db: Session=Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = token.verify_token(data, credentials_exception)
    user = get_user(token_data.citizen_id, db)
    if user is None:
        raise credentials_exception
    return user
