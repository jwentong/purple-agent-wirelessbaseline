import os
from openai import OpenAI
from dotenv import load_dotenv

from a2a.server.tasks import TaskUpdater
from a2a.types import Message, TaskState, Part, TextPart
from a2a.utils import get_message_text, new_agent_text_message

from messenger import Messenger

# Load environment variables
load_dotenv()


class Agent:
    """Purple Agent - A baseline LLM agent using Qwen-turbo-latest for UC Berkeley AgentX Competition."""
    
    def __init__(self):
        self.messenger = Messenger()
        # Initialize Qwen client via DashScope API (OpenAI compatible)
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )
        self.model = "qwen-turbo-latest"
        self.system_prompt = """You are Purple Agent, an intelligent AI assistant participating in the UC Berkeley AgentX Competition. 

Your capabilities include:
- Answering questions accurately and comprehensively
- Providing helpful explanations and analysis
- Assisting with various tasks including coding, writing, and problem-solving

Please provide clear, well-structured responses. If you're unsure about something, acknowledge the uncertainty rather than making up information."""

    async def run(self, message: Message, updater: TaskUpdater) -> None:
        """Process incoming message and generate response using Qwen LLM.

        Args:
            message: The incoming message
            updater: Report progress (update_status) and results (add_artifact)
        """
        input_text = get_message_text(message)

        # Update status to show we're processing
        await updater.update_status(
            TaskState.working, new_agent_text_message("🤔 Thinking...")
        )

        try:
            # Call Qwen-turbo-latest model
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": input_text}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            
            # Extract the response text
            response_text = response.choices[0].message.content
            
            # Add the response as an artifact
            await updater.add_artifact(
                parts=[Part(root=TextPart(text=response_text))],
                name="Response",
            )
            
        except Exception as e:
            error_message = f"Error calling Qwen API: {str(e)}"
            await updater.add_artifact(
                parts=[Part(root=TextPart(text=error_message))],
                name="Error",
            )
