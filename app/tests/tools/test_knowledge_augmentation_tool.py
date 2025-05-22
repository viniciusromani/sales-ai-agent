import pytest
import json

from types import SimpleNamespace
from unittest.mock import patch, mock_open
from app.tools.knowledge_augmentation import KnowledgeAugmentationTool, Args


prospect_details = {
    "acb914e1-8eae-44e1-ae3c-74a048c71609": {
        "name": "Acme Corp",
        "lead_score": 87,
        "company_size": "200-500",
        "technologies": ["AWS", "Grafana"],
        "past_interactions": ["Asked about pricing", "Mentioned a competitor"]
    }
}

class TestKnowledgeAugmentationTool:
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(prospect_details))
    def test_fetch_prospect_details_found(self, mock_qdrant, mock_openai):
        tool = KnowledgeAugmentationTool()
        details = tool.fetch_prospect_details("acb914e1-8eae-44e1-ae3c-74a048c71609")
        assert details == prospect_details["acb914e1-8eae-44e1-ae3c-74a048c71609"]

    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps(prospect_details))
    def test_fetch_prospect_details_not_found(self, mock_qdrant, mock_openai):
        tool = KnowledgeAugmentationTool()
        details = tool.fetch_prospect_details("ed2905f2-1702-4c65-a181-05bad2c8705e")
        assert details == { "error": "Prospect not found" }

    @pytest.mark.asyncio
    async def test_query_knowledge_base_returns_results(self, mock_qdrant, mock_openai):
        mock_result = SimpleNamespace(
            points=[
                SimpleNamespace(payload={ "text": "Our flagship product is an incredible CRM" })
            ]
        )
        mock_openai.embeddings.create.return_value = [0.1, 0.2, 0.3]
        mock_qdrant.return_value.query_points.return_value = mock_result
        
        tool = KnowledgeAugmentationTool()

        knowledge = await tool.query_knowledge_base("What is our company flagship product?")
        assert knowledge["query"] == "What is our company flagship product?"
        assert knowledge["result"] == "Our flagship product is an incredible CRM"
    
    @pytest.mark.asyncio
    async def test_query_knowledge_base_no_results(self, mock_qdrant, mock_openai):
        mock_result = SimpleNamespace(
            points=[]
        )
        mock_openai.embeddings.create.return_value = [0.1, 0.2, 0.3]
        mock_qdrant.return_value.query_points.return_value = mock_result
        
        tool = KnowledgeAugmentationTool()

        knowledge = await tool.query_knowledge_base("What is our company flagship product?")
        assert knowledge["query"] == "What is our company flagship product?"
        assert knowledge["result"] == None
