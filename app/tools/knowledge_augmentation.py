import json

from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel
from agents import RunContextWrapper, FunctionTool

from .factory import register_tool
from .custom_tool import CustomTool
from ..external.qdrant import QdrantClientSingleton, COLLECTION_NAME, LIMIT
from ..external.openai import OpenAIClientSingleton, EMBEDDING_MODEL
from .. import PROJECT_ROOT


class Args(BaseModel):
    action: Literal["fetch_prospect_details", "query_knowledge_base"]
    prospect_id: Optional[str] = None
    query: Optional[str] = None

@register_tool("KnowledgeAugmentationTool")
class KnowledgeAugmentationTool(CustomTool[Args]):
    def __init__(self):
        super().__init__(Args)
        self.qdrant = QdrantClientSingleton.get_instance()
        self.openai = OpenAIClientSingleton.get_instance()

    def fetch_prospect_details(self, prospect_id: str) -> Dict[str, Any]:
        with open(str(PROJECT_ROOT) + "/data/crm.json") as crm_file:
            MOCK_CRM = json.load(crm_file)
            return MOCK_CRM.get(prospect_id, {"error": "Prospect not found"})

    async def query_knowledge_base(self, query: str) -> Dict[str, Any]:
        embedded_query = self.openai.embeddings.create(
            input=query,
            model=EMBEDDING_MODEL
        ).data[0].embedding

        results = await self.qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=embedded_query,
            limit=LIMIT
        )

        result = None
        if results.points:
            result = results.points[0].payload["text"]

        return {
            "query": query,
            "result": result
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
            return await self.query_knowledge_base(parsed.query)
        
        raise ValueError(f"Unsupported action: {parsed.action}")
