from fastapi import APIRouter, Query
from utils.matcher import match_response
from utils.logger import log_unanswered
from utils.langchain_agent import generate_fallback_response

router = APIRouter()

@router.get("/get")
async def get_bot_response(msg: str = Query(...)):
    response = match_response(msg)
    if response:
        return response
    log_unanswered(msg)
    return "I'm still learning and improving. Your question helps me grow smarter!"

@router.get("/llm")
async def get_llm_response(msg: str = Query(...)):
    response = match_response(msg)
    if response:
        return response
    # Fallback to LangChain
    llm_response = generate_fallback_response(msg)
    return llm_response
