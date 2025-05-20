import pytest
from app.services.message import MessageService
from app.agent.sales import Agent
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_run_agent_calls_runner_and_returns_result():
    agent = Agent(name="Test Agent", instructions="...", model="gpt-4o-mini")
    service = MessageService(agent=agent)

    inputs = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"},
        {"role": "user", "content": "What's your price?"}
    ]

    with patch("app.services.message.Runner.run", new_callable=AsyncMock) as mock_runner:
        mock_runner.return_value = "teste"

        result = await service.run_agent(inputs)

        mock_runner.assert_awaited_once_with(agent, inputs)
        assert result == "teste"
