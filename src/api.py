from fastapi import FastAPI, Request
from slack_app import SlackMCPHost
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
slack_host = SlackMCPHost()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/slack/events")
async def slack_events(request: Request):
    data = await request.json()
    
    # Handle Slack URL verification
    if data.get("type") == "url_verification":
        return {"challenge": data["challenge"]}

    # Handle messages
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        if event.get("type") == "message" and "bot_id" not in event:
            channel_id = event.get("channel")
            user_id = event.get("user")
            message = event.get("text")
            
            await slack_host.handle_message(channel_id, user_id, message)
    
    return {"ok": True} 