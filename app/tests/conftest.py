import pytest
from dotenv import load_dotenv
from unittest.mock import AsyncMock, MagicMock, patch


load_dotenv()

@pytest.fixture
def mock_qdrant():
    with patch("app.external.qdrant.QdrantClientSingleton.get_instance") as mock:
        async_mock = AsyncMock()
        mock.return_value = async_mock
        yield mock

@pytest.fixture
def mock_openai():
    with patch("app.external.qdrant.OpenAIClientSingleton.get_instance") as mock:
        magic_mock = MagicMock()
        mock.return_value = magic_mock
        yield mock
