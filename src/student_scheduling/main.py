"""Main module for the StudentScheduling FastAPI application."""

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
