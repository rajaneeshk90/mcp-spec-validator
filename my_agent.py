from typing import Any, Dict
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
import json
import asyncio

load_dotenv(override=True)

class BecknAgent:
    def __init__(self):
        import os
        self.params = {
            "command": "uv", 
            "args": ["run", "mcp_server.py"],
            "env": {"BECKN_VALIDATOR_URL": os.getenv("BECKN_VALIDATOR_URL", "http://oas-validator.becknprotocol.io/retail")}
        }
        self.instructions = "User are a helpful assistant who helps validate provide \
            if a provided JSON is valid as per Beckn protocol Specification. \
            Use the provided tools only to check the validity. \
            dont use any other source of truth to check validity. \
            "
        self.request = "check if the below JSON is valid as per Beckn protocol Specification. "
        self.model = "litellm/gemini/gemini-1.5-pro"
    

    async def run(self, beckn_payload: Dict[str, Any]):
        query = self.request + json.dumps(beckn_payload)
        async with MCPServerStdio(params=self.params) as mcp_server:
            agent = Agent(name="specification_expert", instructions=self.instructions, model=self.model, mcp_servers=[mcp_server])
            with trace("specification_expert"):
                result = await Runner.run(agent, query)
            return result.final_output

async def run_agent():
    beckn_agent = BecknAgent()
    beckn_payload = {
    "context": {
        "domain": "local-retail",
        "location": {
            "country": {
                "code": "IND"
            },
            "city": {
                "code": "std:080"
            }
        },
        "action": "search",
        "version": "1.1.0",
        "bap_id": "farmfresh.bap-id.com",
        "bap_uri": "https://www.55a6-124-123-32-28.ngrok-free.app",
        "transaction_id": "8100d125-76a7-4588-88be-81b97657cd09",
        "message_id": "6104c0a3-d1d1-4ded-aaa4-76e4caf727ce",
        "timestamp": "2023-11-06T09:41:09.673Z"
    },
    "message": {
        "intent": {
            "item": {
                "descriptor": {
                    "name": "Name of product/service"
                }
            },
            "fulfillment": {
                "type": "DELIVERY",
                "stops": [
                    {
                        "location": {
                            "gps": "28.4594965,77.0266383"
                        }
                    }
                ]
            }
        }
    }
}
    result = await beckn_agent.run(beckn_payload)
    print(result)

if __name__ == "__main__":
    asyncio.run(run_agent())



