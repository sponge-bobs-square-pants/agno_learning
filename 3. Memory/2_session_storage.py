from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.storage.mongodb import MongoDbStorage
from agno.storage.postgres import PostgresStorage
from rich.pretty import pprint
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
POSTGRES_URI = os.getenv("POSTGRES_URI")
MONGO_URI = os.getenv("MONGODB_URL")

# SESSION STORAGE:
    # The built in memory works great, but it wont be able to remember the conversation once the agent is stopped.
    # For remembering chat history across reboots and persisting it we use session storage.
    # storage: You can pass your preferred storage in the parameter and boot sessions across reboots.

# INTEGRATION WITH SQLITE STORAGE:
sqlite_storage = SqliteStorage(table_name="agent_sessions", db_file="../tmp/data.db")

# INTEGRATION WITH MONGODB STORAGE:
mongodb_storage = MongoDbStorage(collection_name='agent_sessions', db_url=MONGO_URI, db_name='agno')

# POSTGRESQL STORAGE:
postgres_storage = PostgresStorage(table_name="agent_sessions", db_url=POSTGRES_URI, auto_upgrade_schema=True)

agent = Agent(
    name="General Agent",
    role="General chat agent",
    session_id="003",
    storage=sqlite_storage,
    add_history_to_messages=True,
    read_chat_history=True,
    num_history_runs=3,
    instructions="You are a helpful assistant that always responds in a polite, upbeat and positive manner.",
    model=OpenAIChat(
        id="gpt-4.1-mini",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)
    
agent.print_response("can you list down all my questions before this")
agent.print_response("What is the capital of France?")
# agent.print_response("can you list down all my questions before this")
