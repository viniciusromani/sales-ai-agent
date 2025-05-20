from datetime import datetime
from pydantic import BaseModel
from typing import List, Literal, Optional


class Message(BaseModel):
    sender: Literal["user", "assistant"]
    content: str
    timestamp: datetime

class ProcessMessageRequest(BaseModel):
    conversation_history: List[Message]
    current_prospect_message: str
    prospect_id: Optional[str] = None

class ConversationContext(BaseModel):
    role: Literal["user", "assistant"]
    content: str
