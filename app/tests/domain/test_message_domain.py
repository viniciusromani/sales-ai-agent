import pytest
from app.domain.message import MessageDomain
from app.models.requests import ProcessMessageRequest
from app.services.message import MessageService
from unittest.mock import AsyncMock


class TestMessageDomain:
    @pytest.mark.asyncio
    async def test_process_message_with_proper_inputs_returns(self):
        mock_service = AsyncMock(spec=MessageService)
        mock_service.run_agent.return_value = { "reply": "Here's our pricing..." }
        domain = MessageDomain(service=mock_service)

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
        assert result == expected_inputs
