from fastapi import APIRouter, Depends
from typing import List
from ..schemas import ShowReservation, Reservation, User
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

@router.post('/', response_model=ShowReservation)
def create_reservation(request: Reservation, db: Session=Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    return reservation.create(request, db, current_user)

@router.get('/{reservation_id}', response_model=ShowReservation)
def get_reservation(reservation_id: int, db: Session=Depends(get_db)):
    return reservation.get(reservation_id, db)

@router.get('/{year}/{month}/{day}', response_model=List[ShowReservation])
def get_reservations_from_specific_date(year: int, month: int, day: int, db: Session=Depends(get_db)):
    return reservation.get_from_specific_date(year, month, day, db)