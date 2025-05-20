from fastapi import Depends
from typing import List

from ..models.schema import ConversationContext
from ..agent.sales import get_agent, Agent, Runner


class MessageService:
    def __init__(self, agent: Agent = Depends(get_agent)):
        self.agent = agent

    async def run_agent(self, inputs: List[ConversationContext]) -> str:
        result = await Runner.run(self.agent, inputs)
        print(result)
        return "teste"
