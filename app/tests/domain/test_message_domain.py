import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from app.domain.message import MessageDomain
from app.models.requests import ProcessMessageRequest
from app.services.message import MessageService


class TestMessageDomain:
    @pytest.mark.asyncio
    async def test_process_message_with_proper_inputs_returns(self):
        mock = SimpleNamespace(
            final_output={
                "detailed_analysis": "The user is asking about pricing",
                "suggested_response_draft": "Our pricing takes in account lead score",
                "confidence_score": 0.56,
                "tool_usage_log": [
                    {
                        "tool_name": "Unit test tool",
                        "capability": "capability",
                        "arguments": "{\"action\": \"fetch_prospect_details\", \"prospect_id\": \"1813ea21-5e93-4a19-ac0e-952535ededde\", \"query\": null, \"topic\": null}",
                        "output": "{\"name\": \"Acme Corp\", \"lead_score\": 87, \"company_size\": \"200-500\", \"technologies\": [\"AWS\", \"Grafana\"], \"past_interactions\": [\"Asked about pricing\", \"Mentioned a competitor\"]}"
                    }
                ],
                "reasoning_trace": [
                    {
                        "type": "tool_call_item",
                        "tool_name": "Unit test tool",
                        "arguments": { }
                    },
                    {
                        "type": "tool_call_output_item",
                        "output": { }
                    },
                    {
                        "type": "message_output_item",
                        "output": "Here are the available plans for our product:\n\n1. **Free 14-Day Trial:** Available for all plans.\n   \n2. **Basic Plan:** $29/user/month\n   - Includes access to core CRM features and email integration.\n\n3. **Pro Plan:** $59/user/month\n   - Adds advanced analytics, AI-powered lead scoring, and priority support.\n\n4. **Enterprise Plan:** Custom pricing\n   - Tailored for large teams, includes dedicated account manager and SLA guarantees. \n\nWould you like some help in selecting the plan that best fits your goal of doubling your revenue this year?"
                    }
                ]
            }
        )

        mock_service = AsyncMock(spec=MessageService)
        mock_service.run_agent.return_value = mock

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

        print(result)

        assert result["detailed_analysis"] is not None
        assert result["suggested_response_draft"] is not None
        assert result["confidence_score"] >= 0 and result["confidence_score"] <= 1
        assert len(result["tool_usage_log"]) == 1
        assert len(result["reasoning_trace"]) == 3
