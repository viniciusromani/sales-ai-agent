import pytest
from types import SimpleNamespace
from app.domain.mappers import StacktraceMapper


llm_new_items = [
    SimpleNamespace(
        type="tool_call_item",
        agent=SimpleNamespace(name="Unit Test Agent"),
        tools=[SimpleNamespace(name="Unit Test Tool")],
        raw_item=SimpleNamespace(
            arguments='{"action":"query_knowledge_base","prospect_id":null,"query":"Available plans for our products"}',
            call_id='call_ogr5iTHUNIBNANVouRlT1j8Q',
            name='KnowledgeAugmentationTool', 
            type='function_call', 
            id='fc_683049eab2d88191b309ea334b187dac0da94f7332b71b8d', 
            status='completed'
        )
    ),
    SimpleNamespace(
        type="tool_call_output_item",
        agent=SimpleNamespace(name="Unit Test Agent"),
        tools=[SimpleNamespace(name="Unit Test Tool")],
        raw_item={
            "call_id": "call_ogr5iTHUNIBNANVouRlT1j8Q", 
            "output": '{"query": "Available plans for our products", "result": "Topic: pricing. Enterprise Plan: Custom pricing for large teams, includes dedicated account manager and SLA guarantees.\\nTopic: pricing. Early access to new features included in Enterprise Plan."}', 
            "type": "function_call_output"
        }
    ),
    SimpleNamespace(
        type="message_output_item",
        agent=SimpleNamespace(name="Unit Test Agent"),
        tools=[SimpleNamespace(name="Unit Test Tool")],
        raw_item=SimpleNamespace(
            id="msg_683049ec74948191bca216f82a39d2f60da94f7332b71b8d", 
            content=[SimpleNamespace(
                annotations=[], 
                text="Here are the available plans for our products:\n\n1. **Enterprise Plan**:\n   - Custom pricing tailored for large teams.\n   - Includes a dedicated account manager and SLA guarantees.\n   - Early access to new features is also provided.\n\nWould you like to explore how any of this plan can specifically help your company achieve its goal of doubling revenue this year?", 
                type="output_text"
            )], 
            role="assistant", 
            status="completed", 
            type="message"
        )
    )
]

class TestStacktraceMapper:
    @pytest.mark.asyncio
    async def test_maps_successfully(self):
        mapper = StacktraceMapper()
        result = mapper.map_llm_stacktrace(llm_new_items)

        assert len(result) == 3
        
        assert result[0]["type"] == "tool_call_item"
        assert result[0]["tool_name"] is not None
        assert result[0]["arguments"] is not None

        assert result[1]["type"] == "tool_call_output_item"
        assert result[1]["output"] is not None
        
        assert result[2]["type"] == "message_output_item"
        assert result[2]["output"] is not None
