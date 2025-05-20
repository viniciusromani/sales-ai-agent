from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel
from agents import RunContextWrapper, FunctionTool
from .factory import register_tool
from .custom_tool import CustomTool


class Args(BaseModel):
    action: Literal["fetch_prospect_details", "query_knowledge_base"]
    prospect_id: Optional[str] = None
    query: Optional[str] = None

@register_tool("KnowledgeAugmentationTool")
class KnowledgeAugmentationTool(CustomTool[Args]):
    def __init__(self):
        super().__init__(Args)

    def fetch_prospect_details(self, prospect_id: str) -> Dict[str, Any]:
        MOCK_CRM_DATA = {
            "123": {
                "name": "Acme Corp",
                "lead_score": 87,
                "company_size": "2t01-500",
                "technologies": ["AWS", "Snowflake"],
                "past_interactions": ["Asked about pricing", "Mentioned a competitor"],
            }
        }
        return MOCK_CRM_DATA.get(prospect_id, {"error": "Prospect not found"})

    def query_knowledge_base(self, query: str) -> Dict[str, Any]:
        return {
            "query": query,
            "results": [
                {"document": "Sales Playbook", "snippet": "Handle pricing objections by..."},
                {"document": "Product Overview", "snippet": "Our product supports SSO and..."},
            ]
        }
    
    def get_description(self) -> str:
        return """
            This tool helps augment the assistant's knowledge by accessing relevant sales data and documentation.

            It supports two key capabilities:

            1. **CRM Data Retrieval** (`action="fetch_prospect_details"`):
            - Retrieves structured information about a sales prospect.
            - Fields include: `lead_score`, `company_size`, `technologies`, and `past_interactions`.
            - Requires: `prospect_id` (str)

            2. **Knowledge Base Search** (`action="query_knowledge_base"`):
            - Performs a semantic search over internal documents such as:
                - Sales playbooks
                - Product documentation
                - Competitive analysis
            - Returns relevant snippets.
            - Requires: `query` (str)

            Use this tool to supplement your answers with real data rather than guessing. If you need to reference product capabilities, handle objections, or understand a lead’s context, call this tool.
        """
    
    async def run_function(self, ctx: RunContextWrapper[Any], args: str) -> Dict[str, Any]:
        parsed = self.args_model.model_validate_json(args)
        
        if parsed.action == "fetch_prospect_details":
            return self.fetch_prospect_details(parsed.prospect_id)
        if parsed.action == "query_knowledge_base":
            return self.query_knowledge_base(parsed.query)
        
        raise ValueError(f"Unsupported action: {parsed.action}")
