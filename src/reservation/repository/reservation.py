from sqlalchemy.orm import Session
from .. import models, schemas
from datetime import datetime
from fastapi import status, HTTPException




def get_all(db: Session):
    reservations = db.query(models.Reservation).all()
    return reservations

def create(request: schemas.Reservation, db: Session, current_user: schemas.User):
    request_body = {
        "register_timestamp": request.register_timestamp,
        "user_id": current_user.user_id
    }
    new_reservation = models.Reservation(**request_body)
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

def get(reservation_id: int, db: Session):
    reservation = db.query(models.Reservation).filter(models.Reservation.reservation_id == reservation_id)
    if not reservation.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reservation with this id")
    else:
        return reservation

def delete(reservation_id: int, db: Session):
    reservation = db.query(models.Reservation).filter(models.Reservation.reservation_id == reservation_id)
    if not reservation.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reservation with this id")
    reservation.delete()
    db.commit()
    return "Delete Successfully"

def get_from_specific_date(selected_year: int, selected_month: int, selected_day: int, db: Session):
    min_datetime = datetime(selected_year, selected_month, selected_day, 0, 0)
    max_datetime = datetime(selected_year, selected_month, selected_day, 23, 59, 59, 999999)
    reservation = db.query(models.Reservation).filter(models.Reservation.register_timestamp.between(min_datetime, max_datetime)).all()
    return reservation

def update(reservation_id: int, request: schemas.Reservation, db: Session, current_user: schemas.User):
    reservation = db.query(models.Reservation).filter(models.Reservation.reservation_id == reservation_id)
    if not reservation.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reservation with this id")
    request_body = {
        "register_timestamp": request.register_timestamp,
        "user_id": current_user.user_id
    }
    reservation.update(request_body)
    db.commit()
    return "Updated"