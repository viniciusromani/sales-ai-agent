from pydantic import BaseModel
from typing import List


class ToolUsage(BaseModel):
    tool_name: str
    capability: str
    arguments: dict
    output: str

class SalesAgentOutput(BaseModel):
    detailed_analysis: str
    suggested_response_draft: str
    confidence_score: float
    tool_usage_log: List[ToolUsage]
    reasoning_trace: List[dict]
