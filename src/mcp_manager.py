from typing import Dict, Any, List
from fastmcp import MCPClient
from config import Config

class MCPManager:
    def __init__(self):
        self.servers: Dict[str, MCPClient] = {}
        self._initialize_servers()

    def _initialize_servers(self):
        mcp_servers = Config.get_mcp_servers()
        for server_name, command in mcp_servers.items():
            self.servers[server_name] = MCPClient(command=command)

    async def get_available_tools(self) -> Dict[str, List[str]]:
        """Get all available tools from all servers"""
        tools = {}
        for server_name, client in self.servers.items():
            server_tools = await client.list_tools()
            tools[server_name] = server_tools
        return tools

    async def execute_tool(self, server_name: str, tool_name: str, parameters: Dict[str, Any]) -> str:
        """Execute a tool on specified server with given parameters"""
        if server_name not in self.servers:
            raise ValueError(f"Server {server_name} not found")
        
        client = self.servers[server_name]
        result = await client.execute_tool(tool_name, parameters)
        return result 