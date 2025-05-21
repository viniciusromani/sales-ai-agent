import os
import hashlib
import uuid

from pathlib import Path
from qdrant_client import models
from .external.qdrant import QdrantClientSingleton, COLLECTION_NAME
from .external.openai import OpenAIClientSingleton


FILENAME = "sales_playbook"
FILE_DIR = Path(__file__).parent.parent / "data" / f"{FILENAME}.txt"
EMBEDDING_MODEL = "text-embedding-3-small"

class Seed:
    @classmethod
    async def init(cls):
        openai = OpenAIClientSingleton.get_instance()
        qdrant = QdrantClientSingleton.get_instance()

        if not await qdrant.collection_exists(COLLECTION_NAME):
            print(f"[STATUS] Collection \"{COLLECTION_NAME}\" do not exist - it will be created")
            await qdrant.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )
            
        existing_ids = set()
        try:
            scroll = await qdrant.scroll(collection_name=COLLECTION_NAME, limit=1000)
            for point in scroll[0]:
                existing_ids.add(point.id)
        except Exception:
            pass
        
        print(f"[STATUS] {len(existing_ids)} documents are already in collection")

        with open(FILE_DIR, "r", encoding="utf-8") as f:
            content = f.read().strip()

        raw_chunks = content.split("------------------------------------------------------------")
        chunks = []

        for chunk in raw_chunks:
            lines = chunk.strip().splitlines()
            topic = None
            for line in lines:
                line = line.strip()
                if not line: continue
                if line.endswith(":") and line == line.upper():
                    topic = line[:-1].lower()
                    continue
                if line.startswith("- "):
                    line = line[2:].strip()
                if topic:
                    chunks.append(f"Topic: {topic}. {line}")
        
        print(f"[STATUS] File {FILENAME}.txt read successfully - {len(chunks)} documents were found")

        chunks_to_embed = []
        for chunk in chunks:
            chunk_id = str(uuid.UUID(hashlib.md5(chunk.encode()).hexdigest()))
            
            if chunk_id in existing_ids:
                print("[SKIPPING] Document already indexed")
                continue
            
            chunks_to_embed.append({
                "chunk_id": chunk_id,
                "content": chunk
            })

        if not chunks_to_embed:
            print("[FINISH] No new documents to be inserted")
            return 
        
        print(f"[STATUS] {len(chunks_to_embed)} new documents were found to be inserted")

        embbeding_response = openai.embeddings.create(
            input=[chunk["content"] for chunk in chunks_to_embed], 
            model=EMBEDDING_MODEL
        )

        docs_to_upsert = []
        for chunk_obj, embedding_obj in zip(chunks_to_embed, embbeding_response.data):
            point = models.PointStruct(
                id=chunk_obj["chunk_id"],
                vector=embedding_obj.embedding,
                payload={"text": chunk_obj["content"], "filename": FILENAME}
            )
            docs_to_upsert.append(point)
        
        await qdrant.upsert(collection_name=COLLECTION_NAME, points=docs_to_upsert)
        print(f"[FINISH] {len(docs_to_upsert)} documents were inserted")
