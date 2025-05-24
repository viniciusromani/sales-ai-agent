import pytest
import json

from unittest.mock import patch, mock_open
from app.agents.sales import SalesAgent


mock_md = """
# Unit Test

Mocking md file
"""

class TestSalesAgent:
    @patch("builtins.open", new_callable=mock_open, read_data=mock_md)
    def test_get_instructions_returns(self, mock_file):
        agent = SalesAgent()
        result = agent.get_instructions()
        assert result == mock_md

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_get_instructions_file_not_found(self, mock_file):
        agent = SalesAgent()
        
        with pytest.raises(Exception) as exc_info:
            agent.get_instructions()
        
        assert exc_info.value.status_code == 500
        assert "instructions.md file not found at location" in str(exc_info.value)
    
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_get_instructions_empty_file(self, mock_file):
        agent = SalesAgent()

        with pytest.raises(Exception) as exc_info:
            agent.get_instructions()
        
        assert exc_info.value.status_code == 500
        assert "instructions.md can not be empty" in str(exc_info.value)

    @patch("builtins.open", side_effect=RuntimeError("Unexpected error"))
    def test_get_instructions_generic_exception(self, mock_file):
        agent = SalesAgent()

        with pytest.raises(Exception) as exc_info:
            agent.get_instructions()
        
        assert exc_info.value.status_code == 500
        assert "Could not load instructions.md file" in str(exc_info.value)
