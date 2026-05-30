from pydantic import BaseModel

class AudioEvent(BaseModel):
    sensor_id: int
    value: float

class AudioResponse(BaseModel):
    status: str
    processed: float
