from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
from ..hashing import Hash


router = APIRouter(
    tags=['Authentication']
)

@router.post('/login', responses={status.HTTP_404_NOT_FOUND: {"model": schemas.NotFoundResponse, "description": "Send a request but no object was found"}})
def login(request: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    """
    Authenticate the user using this information:
    ### Request Body:
    - **username**: the citizen id of the user (13 digits) as a string e.g., "1134506547512"
    - **password**: the password of the user as a string e.g., "Verystrongpassword"
    """
    user = db.query(models.User).filter(models.User.citizen_id == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot found {request.citizen_id} citizen id")
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    # generate a jwt token
    access_token = token.create_access_token(data={"sub": user.citizen_id})
    return {"access_token": access_token, "token_type": "bearer"}