from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from rich.pretty import pprint
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

sqlite_storage = SqliteStorage(table_name="agent_sessions", db_file="../tmp/data.db")

# WE CAN STORE THE USER'S DATA IN MEMORY AUTOMATICALLY AND WILL PERSISTS ACROSS ALL THE CHAT BASED ON THE USER ID

# CREATING MEMORY DB
memory_db = SqliteMemoryDb(table_name="memory", db_file="../tmp/data.db")

agent = Agent(
    name="General Agent",
    role="General chat agent",
    session_id="003",
    memory=Memory(db=memory_db),
    # We need to enable the agentic memory by setting enable_agentic_memory to True
    enable_agentic_memory=True,
    storage=sqlite_storage,
    add_history_to_messages=True,
    read_chat_history=True,
    num_history_runs=10,
    instructions="You are a helpful assistant that always responds in a polite, upbeat and positive manner.",
    model=Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)

# This is the id for the user, based upon this id the data of the user will be saved inside the sql database in the memory table.
# You can check what data is saved using the following command:
    # sqlite3 tmp/data.db
    # SELECT * FROM memory WHERE user_id = 'parthchawla65@gmail.com';
user_id = 'parthchawla65@gmail.com'
# agent.print_response('My name is Parth Chawla. I like to code, I am currently coding ai agents using agno.', user_id=user_id)
agent.print_response('What are my hobbies?', user_id=user_id)
agent.print_response('List down all the question i asked so far', user_id=user_id)
