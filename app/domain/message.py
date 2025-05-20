from fastapi import Depends
from ..models.schema import ProcessMessageRequest
from ..services.message import MessageService


class MessageDomain:
    def __init__(self, service: MessageService = Depends(MessageService)):
        self.service = service
    
    async def process_message(
        self, 
        request: ProcessMessageRequest, 
        service: MessageService = Depends(MessageService)
    ) -> list[dict]:
        inputs = []
        if request.conversation_history:
            inputs.extend([
                {"role": message.sender, "content": message.content}
                for message in request.conversation_history
            ])
        
        inputs.append({"role": "user", "content": request.current_prospect_message})

        result = await self.service.run_agent(inputs)
        print(result)
        return inputs
