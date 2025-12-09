# src/agent/nodes.py

import os
from src.rag.retrieve import retrieve_spot_info
from src.tools.buoy import fetch_buoy_data
from src.tools.tides import fetch_tide_data
from src.agent.state import AgentState
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def retrieve_spot_info_node(state: AgentState):
  spot_info = retrieve_spot_info(state["query"])

  return {"spot_info": spot_info[0], "spot_name": spot_info[0]["name"]}

def fetch_conditions_node(state: AgentState):
  buoy_data = fetch_buoy_data()
  tide_data = fetch_tide_data()

  return {"buoy_data": buoy_data, "tide_data": tide_data}

def reason_node(state: AgentState):
  spot_info = state["spot_info"]
  buoy_data = state["buoy_data"]
  tide_data = state["tide_data"]

  # Calls an LLM to generate a recommendation
  llm = ChatAnthropic(model="claude-sonnet-4-20250514", api_key=os.getenv("ANTHROPIC_API_KEY"))
  prompt = ChatPromptTemplate.from_template(
  """
    ROLE
    You are an experienced surf forecaster who helps surfers decide whether to paddle out and what equipment to bring. You analyze conditions pragmatically, prioritizing fun factor over perfection.

    CONTEXT
    Spot: {spot_info}
    Buoy Data: {buoy_data}
    Tide Data: {tide_data}

    TASK
    Analyze the current conditions and provide a surf recommendation.

    ANALYSIS FRAMEWORK
    Consider these factors in order of importance:
    1. **Swell**: Is the swell direction favorable for this spot? Is the period long enough to produce quality waves? Is the size appropriate?
    3. **Tide**: Is the current or upcoming tide optimal for this spot?
    4. **Overall vibe**: Would an experienced local paddle out right now?

    OUTPUT FORMAT
    **Verdict**: [🟢 GO / 🟡 MAYBE / 🔴 SKIP] - One sentence summary

    **Conditions breakdown**:
    - Swell: [brief assessment] 
    - Tide: [brief assessment]

    **Board recommendation**: [shortboard / midlength / longboard / foil] - Why this board fits these conditions

    **Best window**: [If applicable, when conditions will peak today]
    """
  )

  chain = prompt | llm | StrOutputParser()
  response = chain.invoke({"spot_info": spot_info, "buoy_data": buoy_data, "tide_data": tide_data})

  return {"response": response}
