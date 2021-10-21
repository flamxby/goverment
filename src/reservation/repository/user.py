from .. import schemas, models
from ..hashing import Hash
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def create(request: schemas.User, db: Session):
    request_body = {
        "name": request.name,
        "surname": request.surname,
        "citizen_id": request.citizen_id,
        "birth_date": request.birth_date,
        "occupation": request.occupation,
        "address": request.address,
        "password": Hash.bcrypt(request.password)
    }
    new_user = models.User(**request_body)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get(citizen_id, db: Session):
    user = db.query(models.User).filter(models.User.citizen_id == citizen_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user with this id")
    return user