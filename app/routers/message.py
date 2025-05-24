from fastapi import APIRouter, Depends
from ..models.requests import ProcessMessageRequest
from ..models.entities import SalesAgentOutput
from ..domain.message import MessageDomain


router = APIRouter()

@router.post("/process_message")
async def process_message_handler(
    request: ProcessMessageRequest, 
    domain: MessageDomain = Depends(MessageDomain)
) -> SalesAgentOutput:
    result = await domain.process_message(request)
    return result
