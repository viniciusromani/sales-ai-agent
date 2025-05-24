import json

from pathlib import Path
from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel
from agents import RunContextWrapper

from .factory import register_tool
from .custom_tool import CustomTool
from ..external.qdrant import QdrantClientSingleton, COLLECTION_NAME, LIMIT
from ..external.openai import OpenAIClientSingleton, EMBEDDING_MODEL
from .. import PROJECT_ROOT, logger, raise_exception


class Args(BaseModel):
    action: Literal["fetch_prospect_details", "query_knowledge_base"]
    prospect_id: Optional[str] = None
    query: Optional[str] = None
    topic: Optional[str] = None

@register_tool("KnowledgeAugmentationTool")
class KnowledgeAugmentationTool(CustomTool[Args]):
    def __init__(self):
        super().__init__(Args)
        self.qdrant = QdrantClientSingleton.get_instance()
        self.openai = OpenAIClientSingleton.get_instance()

    def fetch_prospect_details(self, prospect_id: str) -> str:
        filename = "instructions.md"
        file_path = Path(PROJECT_ROOT / "data" / filename)
        MOCK_CRM = {}

        try:
            with open(Path(PROJECT_ROOT / "data" / "crm.json")) as crm_file:
                MOCK_CRM = json.load(crm_file)
                
        except FileNotFoundError:
            logger.error(f"crm.json file not found at location {str(file_path)}")
            raise_exception(500, f"crm.json file not found at location {str(file_path)}")
        except Exception as e:
            logger.error(f"Could not load crm.json file {e}")
            raise_exception(500, f"Could not load crm.json file {e}")

        result = MOCK_CRM.get(prospect_id, {"error": "Prospect not found"})
        return json.dumps(result)

    async def query_knowledge_base(self, query: str, topic: Optional[str]) -> str:
        try:
            embedded_query = self.openai.embeddings.create(
                input=query,
                model=EMBEDDING_MODEL
            ).data[0].embedding
        except Exception as e:
            logger.error(f"Could not vector user input in openai API {e}")
            raise_exception(500, f"Could not vector user input in openai API {e}")
        
        try:
            results = await self.qdrant.query_points(
                collection_name=COLLECTION_NAME,
                query=embedded_query,
                limit=LIMIT
            )
        except Exception as e:
            logger.error(f"Could not perform vector similarity search on qdrant {e}")
            raise_exception(500, f"Could not perform vector similarity search on qdrant {e}")

        result = None
        if results.points:
            texts = [point.payload["text"] for point in results.points]
            result = "\n".join(texts)
        
        return json.dumps({
            "query": query,
            "result": result
        })
    
    def get_description(self) -> str:
        return """
            # Description

            This tool helps augment the assistant's knowledge by accessing relevant sales data and documentation.

            # Capabilities

            1. Fetch CRM details using `fetch_prospect_details(prospect_id: str)`.
                * Retrieves structured information about a sales prospect.
                * Fields include: `lead_score`, `company_size`, `technologies`, and `past_interactions`.
                * Requires: `prospect_id` (str)

            2. Search the sales knowledge base using `query_knowledge_base(query: str, filters: Optional[dict])`.
                * Performs a semantic search over internal documents that always splitted in topics such as:
                    - Product Documentation
                    - Pricing
                    - Competitor Comparison
                    - Sales Playbook Snippets
                * Returns relevant snippets.
                * Requires: `query` (str)
                * Optional: `topic` (str)
            
            # Instructions

            * Use this tool to supplement your answers with real data rather than guessing. 
            * Do not use a capability if it is not needed.
            * You are not required to use both capabilities every time you use this tool.
        """
    
    async def run_function(self, ctx: RunContextWrapper[Any], args: str) -> Dict[str, Any]:
        parsed = self.args_model.model_validate_json(args)
        
        if parsed.action == "fetch_prospect_details":
            return self.fetch_prospect_details(parsed.prospect_id)
        if parsed.action == "query_knowledge_base":
            return await self.query_knowledge_base(parsed.query, parsed.topic)
        
        raise ValueError(f"Unsupported action: {parsed.action}")
