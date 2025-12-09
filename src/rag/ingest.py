# src/rag/ingest.py

# Create a function called `ingest_spots` that:
# 1. Loads spots from data/spots.json
# 2. For each spot:
#    - Generate an embedding from the "summary" field
#    - Upsert to Pinecone with:
#      - id: spot name (slugified, e.g., "naples", "rincon-indicators")
#      - vector: the embedding
#      - metadata: the full spot object (all the structured data)
# 3. Print confirmation of what was ingested
#
# You'll need:
# - Pinecone client (from pinecone import Pinecone)
# - An embedding model - use Pinecone's built-in inference API
# - Your PINECONE_API_KEY from .env

# Pinecone inference API for embeddings:
# pc = Pinecone(api_key=...)
# embedding = pc.inference.embed(
#     model="multilingual-e5-large",
#     inputs=["your text here"],
#     parameters={"input_type": "passage"}
# )

import json
from pathlib import Path
import os
from dotenv import load_dotenv
try:
    from pinecone import Pinecone
except Exception as exc:
    raise ImportError(
        "Pinecone SDK v5+ is required. Install/upgrade with: pip install 'pinecone>=5,<6'"
    ) from exc

load_dotenv()

# Get project root relative to this file (src/rag/ingest.py)
project_root = Path(__file__).parent.parent.parent
spots_path = project_root / "data" / "spots.json"


def ingest_spots():
    api_key = os.getenv("PINECONE_API_KEY")
    host = os.getenv("PINECONE_HOST")
    if not api_key:
        raise RuntimeError("PINECONE_API_KEY is not set in environment or .env")
    if not host:
        raise RuntimeError("PINECONE_HOST is not set in environment or .env")

    pc = Pinecone(api_key=api_key)
    index = pc.Index(host=host)

    with open(spots_path) as f:
        data = json.load(f)

    # print(spots)
    for spot in data["spots"]:
        print(spot["name"])
        embedding_response = pc.inference.embed(
          model="multilingual-e5-large",
          inputs=[spot["summary"]],
          parameters={"input_type": "passage"}
        )
        # Pinecone SDK returns an object with .data list of embeddings
        vector_values = (
            embedding_response.data[0].values
            if hasattr(embedding_response, "data")
            else embedding_response[0].values  # fallback for older response shapes
        )

        metadata = {
            "name": spot["name"],
            "full_data": json.dumps(spot)
        }
        spot_id = spot["name"].lower().replace(" - ", "-").replace(" ", "-")

        index.upsert(
          vectors=[
              (
                  spot_id,
                  vector_values,
                  metadata 
              )
          ]
        )
