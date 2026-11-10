from database import Base
from zoneinfo import ZoneInfo
from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from pydantic import BaseModel, Field

def get_current_time():
    return datetime.now(ZoneInfo("America/Sao_Paulo"))

def format_recorded_at(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")

class Readings(Base):
    __tablename__ = 'readings'

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    luminosity = Column(Integer, nullable=False)
    air_quality = Column(Float, nullable=False)
    rainfall = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True), default=get_current_time)

class ReadingsRequest(BaseModel):
    temperature: float = Field(description="Temperatura do ambiente em °C")
    humidity: float = Field(description="Umidade relativa do ar em %")
    pressure: float = Field(description="Pressão atmosférica em hPa")
    luminosity: int = Field(description="Valor de luminosidade captado pelo LDR")
    air_quality: float = Field(description="Valor medido pelo sensor MQ-135")
    rainfall: float = Field(description="Valor de chuva medido pelo pluviômetro")

    model_config = {
    "json_schema_extra": {
        "example": {
            "temperature": 25.5,
            "humidity": 65.0,
            "pressure": 1013.25,
            "luminosity": 750,
            "air_quality": 120.0,
            "rainfall": 0.0
        }
    }
}