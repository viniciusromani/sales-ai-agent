import pytest
from types import SimpleNamespace

from app.tools.custom_tool import CustomTool, RunContextWrapper, Any, Dict, BaseModel
from app.tools.factory import ToolFactory, register_tool


class TestToolFactory:
    @pytest.mark.asyncio
    async def test_register(self):
        class Args(BaseModel):
            args1: str

        class UnitTestTool(CustomTool[Args]):
            def __init__(self):
                super().__init__(Args)

            def get_description(self) -> str:
                return "Unit test tool"
            
            async def run_function(self, ctx: RunContextWrapper[Any], args: str) -> Dict[str, Any]:
                return { "tool": "unit test" }
        
        ToolFactory.register("unittest", UnitTestTool)
        instance = ToolFactory.create("unittest")

        assert isinstance(instance, UnitTestTool)
        assert await instance.run_function(None, "") == { "tool": "unit test" }

    @pytest.mark.asyncio
    async def test_register_with_decorator(self):
        class Args(BaseModel):
            args1: str

        @register_tool("unittest")
        class UnitTestTool(CustomTool[Args]):
            def __init__(self):
                super().__init__(Args)

            def get_description(self) -> str:
                return "Unit test tool"
            
            async def run_function(self, ctx: RunContextWrapper[Any], args: str) -> Dict[str, Any]:
                return { "tool": "unit test" }
        
        instance = ToolFactory.create("unittest")

        assert isinstance(instance, UnitTestTool)
        assert await instance.run_function(None, "") == { "tool": "unit test" }

    def test_tool_not_registered_raises(self):
        with pytest.raises(ValueError) as exc_info:
            ToolFactory.create("nonexistent")

        assert "No tool registered under name 'nonexistent'" in str(exc_info.value)
