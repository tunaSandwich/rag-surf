# src/rag/retrieve.py

# Create a function called `retrieve_spot_info` that:
# 1. Takes a query string (e.g., "Should I surf Naples?")
# 2. Embeds the query using Pinecone's inference API
#    - Use input_type: "query" (not "passage" — remember the asymmetry)
# 3. Searches the index for the top matching vectors
# 4. Returns the full_data (parsed from JSON) for each match
#
# Function signature:
# def retrieve_spot_info(query: str, top_k: int = 2) -> list[dict]:

# Return format:
# [
#   {"name": "Naples", "ideal_tide": "low_to_mid", ...},
#   {"name": "Rincon - The Cove", ...}
# ]

import os
from dotenv import load_dotenv
import json

try:
    from pinecone import Pinecone
except Exception as exc:
    raise ImportError(
        "Pinecone SDK v5+ is required. Install/upgrade with: pip install 'pinecone>=5,<6'"
    ) from exc

load_dotenv()

def retrieve_spot_info(query: str, top_k: int = 2) -> list[dict]:
  api_key = os.getenv("PINECONE_API_KEY")
  host = os.getenv("PINECONE_HOST")
  if not api_key:
    raise RuntimeError("PINECONE_API_KEY is not set in environment or .env")
  if not host:
    raise RuntimeError("PINECONE_HOST is not set in environment or .env")

  pc = Pinecone(api_key=api_key)
  index = pc.Index(host=host)

  embedding_response = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[query],
    parameters={"input_type": "query"}
  )
  vector_values = (
    embedding_response.data[0].values
    if hasattr(embedding_response, "data")
    else embedding_response[0].values  # fallback for older response shapes
  )
  #  Returns the full_data (parsed from JSON) for each match
  results = index.query(vector=vector_values, top_k=top_k, include_metadata=True)

  # results.matches is the list of matches
  spots = []
  for match in results.matches:
      print(f"Match: {match.metadata['name']} (score: {match.score})")
      spots.append(json.loads(match.metadata["full_data"]))
    
  return spots
