from fastapi import Depends
from typing import List

from ..models.entities import ConversationContext
from ..agents.factory import Agent, Runner, AgentFactory, trace


class MessageService:
    def __init__(self, agent: Agent = Depends(AgentFactory.create("SalesAgent").get_agent)):
        self.agent = agent

    async def run_agent(self, inputs: List[ConversationContext]) -> str:
        with trace("Vinicius Romani - Sales AI Agent - Technical Challenge"):
            result = await Runner.run(self.agent, inputs)
            return result
