import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from app.domain.message import MessageDomain
from app.domain.mappers import StacktraceMapper
from app.models.requests import ProcessMessageRequest
from app.services.message import MessageService


class TestMessageDomain:
    @pytest.mark.asyncio
    async def test_process_message_with_proper_inputs_returns(self):
        mock = SimpleNamespace(
            new_items=[
                { "type": "tool_call_item" },
                { "type": "message_output_item" }
            ],
            final_output="My final pricing is just fine"
        )

        mock_service = AsyncMock(spec=MessageService)
        mock_service.run_agent.return_value = mock

        mock_mapper = MagicMock(spec=StacktraceMapper)
        mock_mapper.map_llm_stacktrace.return_value = mock.new_items

        domain = MessageDomain(service=mock_service, mapper=mock_mapper)

        request = ProcessMessageRequest(
            conversation_history=[
                { "sender": "user", "content": "Hello!", "timestamp": "2025-01-01T00:00:00Z" },
                { "sender": "assistant", "content": "Hi! How can I help?", "timestamp": "2025-01-01T00:01:00Z" },
            ],
            current_prospect_message="What is your pricing?",
            prospect_id=None
        )

        result = await domain.process_message(request)

        expected_inputs = [
            { "role": "user", "content": "Hello!" },
            { "role": "assistant", "content": "Hi! How can I help?" },
            { "role": "user", "content": "What is your pricing?" },
        ]
        mock_service.run_agent.assert_awaited_once_with(expected_inputs)
        mock_mapper.map_llm_stacktrace.assert_called_with(mock.new_items)

        assert result["inputs"] == expected_inputs
        assert result["stacktrace"] == mock.new_items
        assert result["output"] == mock.final_output
