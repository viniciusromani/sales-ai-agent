import json
from typing import List, Dict
from agents import RunItem


class StacktraceMapper:
    def map_llm_stacktrace(self, items: List[RunItem]) -> List[Dict]:
        trace = []

        for item in items:
            item_trace = dict()
            item_trace["type"] = item.type

            if item_trace["type"] == "tool_call_item":
                item_trace["tool_name"] = item.raw_item.name
                item_trace["arguments"] = json.loads(item.raw_item.arguments)
            
            if item_trace["type"] == "tool_call_output_item":
                item_trace["output"] = json.loads(item.raw_item["output"])

            if item_trace["type"] == "message_output_item":
                responses = [response.text for response in item.raw_item.content]
                item_trace["output"] = " ".join(responses)

            trace.append(item_trace)
        
        return trace
