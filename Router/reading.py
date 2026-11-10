from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from model import Readings, ReadingsRequest, format_recorded_at


router = APIRouter(
    prefix="/readings",
    tags=['Readings']
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_reading(new_reading: ReadingsRequest, db: db_dependency):
    reading_model = Readings(
        temperature=new_reading.temperature,
        humidity=new_reading.humidity,
        pressure=new_reading.pressure,
        luminosity=new_reading.luminosity,
        air_quality=new_reading.air_quality,
        rainfall=new_reading.rainfall
    )

    db.add(reading_model)
    db.commit()
    db.refresh(reading_model)


# Função para pegar historico de readings para se precisar fazer levantamento diario(ou qualquer tempo) para o dashboard
# @router.get("/history", status_code=status.HTTP_200_OK)
# async def get_readings_history(db: db_dependency):
#     return db.query(Readings).all()

@router.get("/latest", status_code=status.HTTP_200_OK)
async def get_latest_reading(db: db_dependency):
    reading = db.query(Readings).order_by(Readings.recorded_at.desc()).first()

    if reading is None:
        return None

    return {
        "id": reading.id,
        "temperature": reading.temperature,
        "humidity": reading.humidity,
        "pressure": reading.pressure,
        "luminosity": reading.luminosity,
        "air_quality": reading.air_quality,
        "rainfall": reading.rainfall,
        "recorded_at": format_recorded_at(reading.recorded_at)
    }
