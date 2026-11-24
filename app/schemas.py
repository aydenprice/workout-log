import datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkoutBase(BaseModel):
    exercise: str = Field(min_length=1)
    sets: int = Field(ge=1)
    reps: int = Field(ge=1)
    weight: float = Field(ge=0)
    date: datetime.date


class WorkoutCreate(WorkoutBase):
    pass


class WorkoutResponse(WorkoutBase):
    id: int

    model_config = ConfigDict(from_attributes=True)