import argparse
import uvicorn
from dotenv import load_dotenv

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from executor import Executor

# Load environment variables
load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="Run the Purple Agent A2A server.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to bind the server")
    parser.add_argument("--port", type=int, default=9009, help="Port to bind the server")
    parser.add_argument("--card-url", type=str, help="URL to advertise in the agent card")
    args = parser.parse_args()

    # Define Purple Agent skills
    skill = AgentSkill(
        id="general-qa",
        name="General Question Answering",
        description="Answer questions on various topics including technology, science, coding, and general knowledge using the Qwen-turbo-latest language model.",
        tags=["qa", "llm", "qwen", "general-purpose", "agentx"],
        examples=[
            "What is the difference between 5G and 4G?",
            "Explain how machine learning works",
            "Write a Python function to sort a list",
            "What are the key features of the A2A protocol?"
        ]
    )

    agent_card = AgentCard(
        name="Purple Agent",
        description="Purple Agent is a baseline LLM-powered agent for the UC Berkeley AgentX Competition. It uses Alibaba's Qwen-turbo-latest model to answer questions and assist with various tasks.",
        url=args.card_url or f"http://{args.host}:{args.port}/",
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill]
    )

    request_handler = DefaultRequestHandler(
        agent_executor=Executor(),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )
    uvicorn.run(server.build(), host=args.host, port=args.port)


if __name__ == '__main__':
    main()
