from fastapi import FastAPI
from . import models
from .database import engine
from .routers import reservation, user, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(reservation.router)
app.include_router(user.router)
app.include_router(authentication.router)