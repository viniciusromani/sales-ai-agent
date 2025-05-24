import os
from qdrant_client import AsyncQdrantClient, models
from .openai import OpenAIClientSingleton


COLLECTION_NAME = "documents" 
LIMIT = 5

class QdrantClientSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QdrantClientSingleton, cls).__new__(cls)
            cls._instance.client = AsyncQdrantClient(host=os.getenv("QDRANT_HOST"), port=6333)
        return cls._instance

    def get_client(self) -> AsyncQdrantClient:
        return self.client
    
    @classmethod
    def get_instance(cls) -> AsyncQdrantClient:
        singleton = cls()
        return singleton.get_client()
