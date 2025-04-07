# Slack MCP Host

A Slack bot that integrates MCP (Machine Control Protocol) servers with Slack, providing LLM-powered interactions in dedicated channels. The bot can execute tools from configured MCP servers and present results in a user-friendly format.

## Features

- 🤖 LLM-powered conversations in Slack
- 🔧 Integration with multiple MCP servers
- 📝 Markdown rendering support
- 🔍 Collapsible tool execution results
- 💾 Conversation history maintenance
- 🔐 Secure configuration management

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) for dependency management
- A Slack workspace with admin access
- OpenAI API access
- One or more MCP servers

## Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/slack-mcp-host.git
cd slack-mcp-host
```

2. **Create and activate virtual environment**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
uv sync
```

4. **Configure environment**
```bash
cp .env.example .env
```
Edit `.env` with your credentials:
```bash
SLACK_API_KEY=xoxb-your-slack-bot-token
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4

# MCP Servers
SLACK_MCP_NEO4J_MOVIES=uvx mcp-neo4j-cypher --url neo4j+s://demo.neo4jlabs.com --username movies --password movies
SLACK_MCP_TIME=uvx mcp-server-time
```

5. **Create Slack App**
- Go to [api.slack.com/apps](https://api.slack.com/apps)
- Click "Create New App" → "From an app manifest"
- Select your workspace
- Copy and paste the contents of `manifest.yml`
- Create the app and install it to your workspace

## Deployment

### Cloudflare Workers

1. **Install Wrangler**
```bash
npm install -g wrangler
```

2. **Login to Cloudflare**
```bash
wrangler login
```

3. **Set secrets**
```bash
wrangler secret put SLACK_API_KEY
wrangler secret put OPENAI_API_KEY
```

4. **Deploy**
```bash
wrangler deploy
```

5. **Update Slack App configuration**
- Go to your Slack App settings
- Update the Event Subscription URL to your Cloudflare Workers URL:
  `https://slack-mcp-host.<your-worker-subdomain>.workers.dev/slack/events`

## Usage Example

Here's an example interaction flow:

1. **User starts conversation**
```
User: Can you help me find movies directed by Christopher Nolan?
```

2. **Bot responds with tool execution**
```
Bot: I'll help you find movies directed by Christopher Nolan using the Neo4j Movies database.

<details><summary>Tool Results</summary>
Tool neo4j_movies result:
- Inception (2010)
- The Dark Knight (2008)
- Interstellar (2014)
- Memento (2000)
- The Prestige (2006)
</details>

Would you like to know more details about any of these movies?
```

3. **User follows up**
```
User: Tell me more about Inception
```

4. **Bot executes another query**
```
Bot: I'll get the details about Inception for you.

<details><summary>Tool Results</summary>
Tool neo4j_movies result:
Title: Inception (2010)
Director: Christopher Nolan
Cast: Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page
Plot: A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.
</details>

The movie received critical acclaim for its innovative storytelling and visual effects. Would you like to know about any other movies or specific aspects of Inception?
```

## Development

To run locally for development:

```bash
uvicorn src.api:app --reload --port 8000
```

Use [ngrok](https://ngrok.com/) or similar to expose your local server:
```bash
ngrok http 8000
```

Update your Slack App's Event Subscription URL with the ngrok URL.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
