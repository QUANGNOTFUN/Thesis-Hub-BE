from fastapi import APIRouter, Depends
from typing import Any

from app.shared.database import get_db

router = APIRouter()


@router.get("/", response_model=dict)
def read_example(db=Depends(get_db)) -> Any:
    """
    Example endpoint for the feature. Replace with actual handlers.
    """
    # ...use db session, call service/crud functions...
    return {"message": "example feature is healthy"}

