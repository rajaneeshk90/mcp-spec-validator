Test the server manually

`echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}' | python mcp_server.py`

Your server is running. Now let me test if it responds to MCP protocol messages:

`echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}' | python mcp_server.py`

response

`{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","capabilities":{"experimental":{},"prompts":
{"listChanged":false},"resources":{"subscribe":false,"listChanged":false},"tools":{"listChanged":false}},"ser
verInfo":{"name":"accounts_server","version":"1.9.4"}}}`

let me test if it lists the tools:

`
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}' | python mcp_server.py
`

`
(echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}'; echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}') | python mcp_server.py
`

result

`

`