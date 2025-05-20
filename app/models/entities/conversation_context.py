from pydantic import BaseModel
from typing import Literal


class ConversationContext(BaseModel):
    role: Literal["user", "assistant"]
    content: str
