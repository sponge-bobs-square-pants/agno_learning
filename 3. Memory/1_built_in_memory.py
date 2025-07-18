from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from rich.pretty import pprint
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# To make the model remember the conversation history we have 3 parameters which we can configure:

    # 1. add_history_to_messages: Whether to add the conversation history to the messages or not, if set to True, the conversation history will be added to the messages and the model will be able to remember the conversation history.
    
    # 2. num_history_runs: The numbers of previous runs to automatically be append to each message that is sent to the agent.
    
    # 3. read_chat_history: When set to True it gives the agent access to get_chat_history() which allows the agent to read any chat message in the entire chat history

# the qwen model shows a <think> tag, please note that it is the model's issue for presenting that, the openai models do not have that issue.
general_agent = Agent(
    name="General Agent",
    role="General chat agent",
    add_history_to_messages=True,
    read_chat_history=True,
    num_history_runs=3,
    instructions="You are a helpful assistant that always responds in a polite, upbeat and positive manner.",
    model=Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)

general_agent.print_response("Share a 2 sentence horror story")
pprint([m.model_dump(include={"role", "content"}) for m in general_agent.get_messages_for_session()])
general_agent.print_response("What was my first message?")
pprint([m.model_dump(include={"role", "content"}) for m in general_agent.get_messages_for_session()])