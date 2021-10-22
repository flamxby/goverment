from fastapi import APIRouter, Depends, status
from typing import List

from ..schemas import ShowReservation, Reservation, User, UnauthorizedResponse, NotFoundResponse
from ..database import get_db
from .. import oauth2
from sqlalchemy.orm import Session
from ..repository import reservation

router = APIRouter(
    prefix='/reservation',
    tags=['Reservations']
)

@router.get('/', response_model=List[ShowReservation])
def get_all_reservation(db: Session=Depends(get_db)):
    """
    Get all the reservations that is created
    """
    return reservation.get_all(db)

@router.post('/', 
    response_model=ShowReservation, 
    status_code=status.HTTP_201_CREATED, 
    summary="Create a Reservation", 
    responses={status.HTTP_201_CREATED: {"model": ShowReservation, "description": "Create Successful"},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedResponse, "description": "Send a request but not authenticated"}
    })
def create_reservation(request: Reservation, db: Session=Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    """
    Create a reservation with this information (need to authorize):
    ### Request Body:
    - **register_timestamp**: the datetime as an ISO format e.g., "2021-10-22T14:52:14.933Z"
    """
    return reservation.create(request, db, current_user)

@router.get('/{reservation_id}', 
    response_model=ShowReservation,
    responses={status.HTTP_404_NOT_FOUND: {"model": NotFoundResponse, "description": "Send a request but no object was found"}
    })
def get_reservation(reservation_id: int, db: Session=Depends(get_db)):
    """
    Get the specific reservation's detail from reservation's id:
    ### Parameters:
    - **reservation_id**: the id of the specific reservation as an integer e.g., 1
    """
    return reservation.get(reservation_id, db)

@router.get('/{year}/{month}/{day}', response_model=List[ShowReservation],)
def get_reservations_from_specific_date(year: int, month: int, day: int, db: Session=Depends(get_db)):
    """
    Get the specific reservation's detail from the specific year, month, and day:
    ### Parameters:
    - **year**: the year of the specific reservation as an integer e.g., 2020
    - **month**: the month of the specific reservation as an integer e.g., 10
    - **day**: the day of the specific reservation as an integer e.g., 21
    """
    return reservation.get_from_specific_date(year, month, day, db)

@router.delete('/{reservation_id}',
    responses={ status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedResponse, "description": "Send a request but not authenticated"},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundResponse, "description": "Send a request but no object was found"}
    })
def delete_reservation(reservation_id: int, db: Session=Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    """
    Delete the specific reservation from reservation's id:
    ### Parameters:
    - **reservation_id**: the id of the specific reservation as an integer e.g., 1
    """
    return reservation.delete(reservation_id, db)

@router.put('/{reservation_id}', response_model=ShowReservation,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedResponse, "description": "Send a request but not authenticated"},
        status.HTTP_404_NOT_FOUND: {"model": NotFoundResponse, "description": "Send a request but no object was found"}
    })
def update_reservation(reservation_id: int, request: Reservation, db: Session=Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    """
    Update the specific reservation from reservation's id with this information (need to authorize):
    ### Parameters:
    - **reservation_id**: the id of the specific reservation as an integer e.g., 1
    ### Request Body:
    - **register_timestamp**: the datetime as an ISO format e.g., "2021-10-22T14:52:14.933Z"
    """
    return reservation.update(reservation_id, request, db, current_user)