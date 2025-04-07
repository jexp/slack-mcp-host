from typing import List, Dict, Any
import openai
from config import Config

class LLMManager:
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=Config.OPENAI_API_KEY,
            base_url=Config.OPENAI_BASE_URL
        )
        self.model = Config.OPENAI_MODEL

    async def process_message(self, 
                            message: str, 
                            conversation_history: List[Dict[str, str]], 
                            available_tools: Dict[str, List[str]]) -> Dict[str, Any]:
        """Process a message and return response with potential tool calls"""
        
        # Format tools for the LLM
        tools_description = self._format_tools_description(available_tools)
        
        messages = [
            {"role": "system", "content": f"""You are an AI assistant with access to the following tools:
{tools_description}

When you need to use a tool, respond with a JSON structure containing:
- "response": Your markdown-formatted response to the user
- "tool_calls": List of tool calls, each containing "server", "tool", and "parameters"

Keep conversation history in mind when responding."""},
        ]
        
        # Add conversation history
        messages.extend([{"role": "user" if msg["role"] == "user" else "assistant", 
                         "content": msg["content"]} for msg in conversation_history])
        
        # Add current message
        messages.append({"role": "user", "content": message})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"}
        )

        return response.choices[0].message.content

    def _format_tools_description(self, tools: Dict[str, List[str]]) -> str:
        description = []
        for server, server_tools in tools.items():
            description.append(f"\nServer: {server}")
            for tool in server_tools:
                description.append(f"- {tool}")
        return "\n".join(description) 