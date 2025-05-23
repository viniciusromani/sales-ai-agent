import json

from fastapi import Depends
from agents import RunItem

from .mappers import StacktraceMapper
from ..models.requests import ProcessMessageRequest
from ..services.message import MessageService


class MessageDomain:
    def __init__(
        self, 
        service: MessageService = Depends(MessageService),
        mapper: StacktraceMapper = Depends(StacktraceMapper)
    ):
        self.service = service
        self.mapper = mapper
    
    async def process_message(self, request: ProcessMessageRequest) -> list[dict]:
        inputs = []
        if request.conversation_history:
            inputs.extend([
                {"role": message.sender, "content": message.content}
                for message in request.conversation_history
            ])

        user_message = request.current_prospect_message
        if request.prospect_id:
            user_message += "\n\nProspect ID: " + request.prospect_id

        inputs.append({"role": "user", "content": user_message})

        result = await self.service.run_agent(inputs)
        stacktrace = self.mapper.map_llm_stacktrace(result.new_items)

        return { 
            "inputs": inputs, 
            "stacktrace": stacktrace, 
            "output": result.final_output
        }
