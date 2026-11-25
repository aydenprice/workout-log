from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Workout
from app.schemas import WorkoutCreate, WorkoutResponse

router = APIRouter(prefix="/workouts", tags=["workouts"])

# --- POST ---
@router.post("", response_model=WorkoutResponse, status_code=201)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db)):
    db_workout = Workout(**workout.model_dump())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


# --- GET ---
@router.get("", response_model=list[WorkoutResponse])
def read_workouts(db: Session = Depends(get_db)):
    return db.query(Workout).all()


# --- GET (By ID) ---
@router.get("/{workout_id}", response_model=WorkoutResponse)
def read_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


# --- PUT ---
@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_workout(
    workout_id: int, workout: WorkoutCreate, db: Session = Depends(get_db)
):
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    for field, value in workout.model_dump().items():
        setattr(db_workout, field, value)
    db.commit()
    db.refresh(db_workout)
    return db_workout


# --- DELETE ---
@router.delete("/{workout_id}", status_code=204)
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    db_workout = db.query(Workout).filter(Workout.id == workout_id).first()
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(db_workout)
    db.commit()