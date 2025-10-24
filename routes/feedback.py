from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.logger import log_feedback

router = APIRouter()

class Feedback(BaseModel):
    question: str
    feedback: str

@router.post("/feedback")
async def receive_feedback(data: Feedback):
    try:
        log_feedback(data.question, data.feedback)
        return {"message": "Thanks for your feedback!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging feedback: {str(e)}")
