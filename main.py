from fastapi import FastAPI
from database import Base, engine
from model import Readings
from Router import reading

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(reading.router)