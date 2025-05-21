import os
from openai import OpenAI


EMBEDDING_MODEL = "text-embedding-3-small"

class OpenAIClientSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClientSingleton, cls).__new__(cls)
            cls._instance.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        return cls._instance

    def get_client(self) -> OpenAI:
        return self.client
    
    @classmethod
    def get_instance(cls) -> OpenAI:
        singleton = cls()
        return singleton.get_client()
