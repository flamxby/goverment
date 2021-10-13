from fastapi import APIRouter, Depends
from ..database import get_db
from ..schemas import ShowUser, User
from ..hashing import Hash
from .. import models
from sqlalchemy.orm import Session
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post('/', response_model=ShowUser)
def create_user(request: User, db: Session=Depends(get_db)):
    return user.create(request, db)

@router.get('/{citizen_id}', response_model=ShowUser)
def get_user(citizen_id: str, db: Session=Depends(get_db)):
    return user.get(citizen_id, db)