from typing import Dict, Type
from agents import Agent, Runner, trace


class AgentFactory:
    registry: Dict[str, Type[Agent]] = {}

    @classmethod
    def register(cls, name: str, tool_cls: Type[Agent]):
        cls.registry[name] = tool_cls

    @classmethod
    def create(cls, name: str) -> Agent:
        tool_cls = cls.registry.get(name)
        if not tool_cls:
            raise ValueError(f"No agent registered under name '{name}'")
        return tool_cls()

def register_agent(name: str):
    def decorator(cls: Type[Agent]):
        AgentFactory.register(name, cls)
        return cls
    return decorator
