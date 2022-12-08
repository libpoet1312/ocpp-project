from pydantic import BaseModel


class ChargingPointBase(BaseModel):
    id: int


class ChargingPoint(ChargingPointBase):
    class Config:
        orm_mode = True
