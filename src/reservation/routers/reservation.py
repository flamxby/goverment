from fastapi import APIRouter, Depends, status
from typing import List

from ..schemas import ShowReservation, Reservation, User, UnauthorizedResponse
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
    - **register_timestamp**: the datetime in ISO format
    """
    return reservation.create(request, db, current_user)

@router.get('/{reservation_id}', response_model=ShowReservation)
def get_reservation(reservation_id: int, db: Session=Depends(get_db)):
    return reservation.get(reservation_id, db)

@router.get('/{year}/{month}/{day}', response_model=List[ShowReservation])
def get_reservations_from_specific_date(year: int, month: int, day: int, db: Session=Depends(get_db)):
    return reservation.get_from_specific_date(year, month, day, db)

@router.delete('/{reservation_id}')
def delete_reservation(reservation_id: int, db: Session=Depends(get_db)):
    return reservation.delete(reservation_id, db)

@router.put('/{reservation_id}', response_model=ShowReservation)
def update_reservation(reservation_id: int, request: Reservation, db: Session=Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    return reservation.update(reservation_id, request, db, current_user)