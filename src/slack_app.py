from typing import Dict, List
import asyncio
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import Config
from llm_manager import LLMManager
from mcp_manager import MCPManager

class SlackMCPHost:
    def __init__(self):
        self.client = WebClient(token=Config.SLACK_API_KEY)
        self.llm_manager = LLMManager()
        self.mcp_manager = MCPManager()
        self.conversation_history: Dict[str, List[Dict[str, str]]] = {}

    async def handle_message(self, channel_id: str, user_id: str, message: str):
        """Handle incoming message from Slack"""
        # Initialize conversation history for new channels
        if channel_id not in self.conversation_history:
            self.conversation_history[channel_id] = []

        # Add user message to history
        self.conversation_history[channel_id].append({
            "role": "user",
            "content": message
        })

        try:
            # Get available tools
            available_tools = await self.mcp_manager.get_available_tools()

            # Process message with LLM
            llm_response = await self.llm_manager.process_message(
                message,
                self.conversation_history[channel_id],
                available_tools
            )

            # Execute any tool calls
            if "tool_calls" in llm_response:
                tool_results = []
                for tool_call in llm_response["tool_calls"]:
                    result = await self.mcp_manager.execute_tool(
                        tool_call["server"],
                        tool_call["tool"],
                        tool_call["parameters"]
                    )
                    tool_results.append(f"Tool {tool_call['tool']} result: {result}")

                # Add tool results as collapsible section
                tool_results_text = "\n".join(tool_results)
                response_text = (f"{llm_response['response']}\n\n"
                               f"<details><summary>Tool Results</summary>\n\n{tool_results_text}\n</details>")
            else:
                response_text = llm_response["response"]

            # Send response to Slack
            self.client.chat_postMessage(
                channel=channel_id,
                text=response_text,
                mrkdwn=True
            )

            # Add assistant response to history
            self.conversation_history[channel_id].append({
                "role": "assistant",
                "content": response_text
            })

        except SlackApiError as e:
            print(f"Error sending message: {e.response['error']}")
        except Exception as e:
            print(f"Error processing message: {e}") 