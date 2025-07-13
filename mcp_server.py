from mcp.server.fastmcp import FastMCP
from typing import Dict, Any, Union
import json
import httpx
import os

mcp = FastMCP("accounts_server")

ALLOWED_ACTIONS = {
    "search", "on_search", "select", "on_select", "init", "on_init",
    "confirm", "on_confirm", "status", "on_status"
}

@mcp.tool()
async def valid_beckn_payload(payload: Dict[str, Any]) -> str:
    """Tell if the given payload is valid as per the Beckn Protocol Specification.

    Args:
        payload: The json payload to be validated
    """
    # Validate that payload has a 'context' field
    if 'context' not in payload:
        return "Invalid payload: missing 'context' field"
    
    context = payload['context']
    
    # Validate that context is a dictionary
    if not isinstance(context, dict):
        return "Invalid payload: 'context' must be a dictionary"
    
    # Validate that context has an 'action' field
    if 'action' not in context:
        return "Invalid payload: missing 'action' field in context"
    
    action = context['action']
    
    # Validate that action is not empty
    if not action:
        return "Invalid payload: 'action' field cannot be empty"
    
    # Validate that action is one of the allowed actions
    if action not in ALLOWED_ACTIONS:
        return f"Invalid payload: 'action' field must be one of {sorted(ALLOWED_ACTIONS)}"
    
    # Make POST call to Beckn OAS validator
    try:
        async with httpx.AsyncClient() as client:
            base_url = os.getenv("BECKN_VALIDATOR_URL", "http://oas-validator.becknprotocol.io/retail")
            url = f"{base_url}/{action}"
            response = await client.post(url, json=payload, timeout=30.0)
            
            if response.status_code != 200:
                return f"OAS validation failed with status {response.status_code}: {response.text}"
                
    except httpx.RequestError as e:
        return f"Failed to connect to OAS validator: {str(e)}"
    except Exception as e:
        return f"Unexpected error during OAS validation: {str(e)}"
    
    return "The provided payload is valid as per the Beckn Protocol Specification version 1.1.0."


if __name__ == "__main__":
    mcp.run(transport='stdio')