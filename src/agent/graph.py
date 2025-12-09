# src/agent/graph.py

from langgraph.graph import StateGraph, END
from src.agent.state import AgentState
from src.agent.nodes import (
  retrieve_spot_info_node,
  fetch_conditions_node,
  reason_node,
)

def create_surf_agent():
  # Initialize the graph with our state schema
  workflow = StateGraph(AgentState)
  
  # Add nodes
  workflow.add_node("retrieve", retrieve_spot_info_node)
  workflow.add_node("fetch_conditions", fetch_conditions_node)
  workflow.add_node("reason", reason_node)
  
  # Define the flow
  workflow.set_entry_point("retrieve")
  workflow.add_edge("retrieve", "fetch_conditions")
  workflow.add_edge("fetch_conditions", "reason")
  workflow.add_edge("reason", END)
  
  # Compile the graph
  return workflow.compile()

