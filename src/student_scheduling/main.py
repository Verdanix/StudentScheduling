"""Main module for the StudentScheduling FastAPI application."""

import uvicorn
from fastapi import FastAPI

TITLE = "StudentScheduling"
DESCRIPTION = (
    "Customizable shift scheduling for student-run stores built for my highschool."
)
app = FastAPI(title=TITLE, description=DESCRIPTION)


@app.get("/")
def index() -> dict:
    """
    Root endpoint that returns the main page.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the Student Scheduling API"}


def start():
    """
    Start the FastAPI application using Uvicorn.
    """
    uvicorn.run(
        "src.student_scheduling.main:app", host="0.0.0.0", port=8000, reload=True
    )
