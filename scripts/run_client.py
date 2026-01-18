"""Simple client to test the Purple Agent."""

import asyncio
import httpx
from a2a.client import A2ACardResolver, ClientConfig, ClientFactory
from a2a.types import Message, Part, Role, TextPart
from uuid import uuid4


def create_message(text: str) -> Message:
    """Create a simple text message."""
    return Message(
        kind="message",
        role=Role.user,
        parts=[Part(TextPart(kind="text", text=text))],
        message_id=uuid4().hex,
        context_id=None,
    )


async def test_agent(agent_url: str = "http://localhost:9009"):
    """Send a test message to the agent and print the response."""
    print(f"🔗 Connecting to Purple Agent at {agent_url}...")
    
    async with httpx.AsyncClient(timeout=60) as httpx_client:
        # Get agent card
        resolver = A2ACardResolver(httpx_client=httpx_client, base_url=agent_url)
        agent_card = await resolver.get_agent_card()
        print(f"✅ Connected to: {agent_card.name}")
        print(f"📝 Description: {agent_card.description}")
        print(f"🎯 Skills: {[s.name for s in agent_card.skills]}")
        print("-" * 50)
        
        # Create client
        config = ClientConfig(httpx_client=httpx_client, streaming=False)
        factory = ClientFactory(config)
        client = factory.create(agent_card)
        
        # Test questions
        test_questions = [
            "Hello! Can you introduce yourself?",
            "What is the A2A protocol?",
            "Write a simple Python hello world function.",
        ]
        
        for question in test_questions:
            print(f"\n💬 User: {question}")
            message = create_message(question)
            
            response_text = ""
            async for event in client.send_message(message):
                match event:
                    case Message() as msg:
                        for part in msg.parts:
                            if hasattr(part.root, 'text'):
                                response_text += part.root.text
                    case (task, update):
                        if task.artifacts:
                            for artifact in task.artifacts:
                                for part in artifact.parts:
                                    if hasattr(part.root, 'text'):
                                        response_text += part.root.text
            
            print(f"🤖 Agent: {response_text[:500]}{'...' if len(response_text) > 500 else ''}")
            print("-" * 50)


if __name__ == "__main__":
    asyncio.run(test_agent())
