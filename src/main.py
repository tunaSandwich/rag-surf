# src/main.py
from src.agent.graph import create_surf_agent

def main():
    agent = create_surf_agent()
    
    # Run the agent
    result = agent.invoke({
        "query": "Is it good at the cove?",
        "spot_name": "",
        "spot_info": None,
        "buoy_data": None,
        "tide_data": None,
        "response": None
    })
    
    print(result["response"])

if __name__ == "__main__":
    main()
