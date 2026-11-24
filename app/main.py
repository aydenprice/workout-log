import uvicorn
from fastapi import FastAPI

from app import models # (registers the Workout table)
from app.database import Base, engine
from app.routers import workouts

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workout Log API")
app.include_router(workouts.router)


@app.get("/")
def root():
    return {"message": "Workout Log API is running"}


def start():
    uvicorn.run("app.main:app", reload=True)