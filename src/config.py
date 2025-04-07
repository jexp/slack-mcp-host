from typing import Dict
import os

class Config:
    # For Cloudflare Workers, we'll use the global environment
    SLACK_API_KEY = os.environ.get("SLACK_API_KEY")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4")
    
    @staticmethod
    def get_mcp_servers() -> Dict[str, str]:
        """Get MCP server commands from environment variables"""
        mcp_servers = {}
        for key in os.environ:
            if key.startswith("SLACK_MCP_"):
                server_name = key.replace("SLACK_MCP_", "").lower()
                mcp_servers[server_name] = os.environ[key]
        return mcp_servers 