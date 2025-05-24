import os
from pathlib import Path
from agents import Agent
from .. import PROJECT_ROOT, logger, raise_exception

from .factory import register_agent
from ..tools.factory import ToolFactory


@register_agent("SalesAgent")
class SalesAgent():
    def get_name(self) -> str:
        return "Sales Agent"
    
    def get_instructions(self) -> str:
        filename = "instructions.md"
        file_path = Path(PROJECT_ROOT / "app" / "agents" / filename)
        instructions = ""

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                instructions = file.read()
                
        except FileNotFoundError:
            logger.error(f"instructions.md file not found at location {str(file_path)}")
            raise_exception(500, f"instructions.md file not found at location {str(file_path)}")
        except Exception as e:
            logger.error(f"Could not load instructions.md file {e}")
            raise_exception(500, f"Could not load instructions.md file {e}")

        if not instructions:
            logger.error("instructions.md was loaded but it has no content")
            raise_exception(500, "instructions.md can not be empty")

        return instructions

    def get_agent(self) -> Agent:
        return Agent(
            name=self.get_name(),
            instructions=self.get_instructions(),
            model="gpt-4o-mini",
            tools=[ToolFactory.create("KnowledgeAugmentationTool").get_tool()]
        )
