from fastapi import APIRouter, Depends, status
from ..database import get_db
from ..schemas import ShowUser, User, NotFoundResponse
from ..hashing import Hash
from .. import models
from sqlalchemy.orm import Session
from ..repository import user

router = APIRouter(
    prefix="/user",
    tags=['Users']
)

@router.post('/', response_model=ShowUser, status_code=status.HTTP_201_CREATED, responses={status.HTTP_201_CREATED: {"model": ShowUser, "description": "Create Successful"}})
def create_user(request: User, db: Session=Depends(get_db)):
    """
    Create a user with these information:
    ### Request Body:
    - **name**: the name of the user
    - **surname**: the surname of the user
    - **citizen_id**: the citizen id of the user
    - **birth_date**: the birthdate of the user
    - **occupation**: the occupation of the user
    - **address**: the address of the user
    - **password**: the password of the user
    """
    return user.create(request, db)

@router.get('/{citizen_id}', response_model=ShowUser, responses={status.HTTP_404_NOT_FOUND: {"model": NotFoundResponse, "description": "Send a request but no object was found"}})
def get_user(citizen_id: str, db: Session=Depends(get_db)):
    """
    Get the specific user's detail from the citizen id:
    ### Parameters:
    - **citizen_id**: the citizen id of the specific user
    """
    return user.get(citizen_id, db)