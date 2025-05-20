from abc import ABC, abstractmethod
from typing import Any, Dict, Type, Generic, TypeVar
from pydantic import BaseModel
from agents import FunctionTool, RunContextWrapper


T = TypeVar("T", bound=BaseModel)

class CustomTool(ABC, Generic[T]):
    def __init__(self, args_model: Type[T]):
        self.args_model = args_model

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    async def run_function(self, ctx: RunContextWrapper[Any], args: str) -> Dict[str, Any]:
        pass

    def get_name(self) -> str:
        return self.__class__.__name__

    def get_tool(self) -> FunctionTool:
        return FunctionTool(
            name=self.get_name(),
            description=self.get_description(),
            params_json_schema={
                **self.args_model.model_json_schema(),
                "required": list(self.args_model.model_fields.keys()),
                "additionalProperties": False
            },
            on_invoke_tool=self.run_function,
        )
