# Purple Agent - UC Berkeley AgentX Competition

A baseline LLM-powered agent for the UC Berkeley AgentX Competition using Alibaba's Qwen-turbo-latest model and the A2A (Agent-to-Agent) protocol.

## Features

- 🤖 **Qwen-turbo-latest Integration**: Powered by Alibaba's latest Qwen language model via DashScope API
- 🔗 **A2A Protocol Compliant**: Built on the Agent-to-Agent protocol for seamless agent communication
- 💬 **General Q&A**: Answers questions on various topics including technology, coding, and general knowledge
- 🚀 **Easy Deployment**: Docker-ready with simple local development setup

## Project Structure

```
src/
├─ server.py      # Server setup and agent card configuration
├─ executor.py    # A2A request handling
├─ agent.py       # Qwen LLM agent implementation
└─ messenger.py   # A2A messaging utilities
tests/
└─ test_agent.py  # Agent tests
.env.example      # Environment variables template
Dockerfile        # Docker configuration
pyproject.toml    # Python dependencies
```

## Quick Start

### 1. Set up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your DashScope API key
# Get your key from: https://dashscope.console.aliyun.com/
```

### 2. Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### 3. Run the Agent Server

```bash
# Using uv
uv run src/server.py

# Or directly with Python
python src/server.py
```

The agent will be available at `http://localhost:9009`

## Running with Docker

```bash
# Build the image
docker build -t purple-agent .

# Run the container (pass your API key)
docker run -p 9009:9009 -e DASHSCOPE_API_KEY=your_key_here purple-agent
```

## Testing

```bash
# Install test dependencies
uv sync --extra test

# Start your agent first, then run tests
uv run pytest --agent-url http://localhost:9009
```

## API Usage

Once running, you can interact with the agent via the A2A protocol:

- **Agent Card**: `GET http://localhost:9009/.well-known/agent-card.json`
- **Send Message**: `POST http://localhost:9009/` with A2A message format

## Configuration

| Environment Variable | Description | Required |
|---------------------|-------------|----------|
| `DASHSCOPE_API_KEY` | Your DashScope API key for Qwen models | Yes |

## About AgentX Competition

This agent is built for the [UC Berkeley AgentX Competition](https://rdi.berkeley.edu/agentx), which focuses on advancing LLM Agents technology. The competition includes both Entrepreneurship and Research tracks.

## License

MIT License
