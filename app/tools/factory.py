from typing import Dict, Type
from .custom_tool import CustomTool


class ToolFactory:
    registry: Dict[str, Type[CustomTool]] = {}

    @classmethod
    def register(cls, name: str, tool_cls: Type[CustomTool]):
        cls.registry[name] = tool_cls

    @classmethod
    def create(cls, name: str) -> CustomTool:
        tool_cls = cls.registry.get(name)
        if not tool_cls:
            raise ValueError(f"No tool registered under name '{name}'")
        return tool_cls()

def register_tool(name: str):
    def decorator(cls: Type[CustomTool]):
        ToolFactory.register(name, cls)
        return cls
    return decorator
