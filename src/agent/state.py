# src/graph.py

from typing import TypedDict

class AgentState(TypedDict):
    query: str                   # User's question
    spot_name: str               # Extracted spot name (Naples, Rincon, etc.)
    spot_info: dict | None       # Retrieved from Pinecone
    buoy_data: dict | None       # From buoy tool
    tide_data: dict | None       # From tide tool
    response: str | None         # Final recommendation
