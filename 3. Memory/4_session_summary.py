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
memory_db = SqliteMemoryDb(table_name="memory", db_file="../tmp/data.db")
memory = Memory(db=memory_db)
# SESSION SUMMARY: To enable the session summary feature, we need to set enable_session_summaries to True in the Agent class.


agent = Agent(
    name="General Agent",
    role="General chat agent",
    session_id="003",
    memory=memory,
    enable_agentic_memory=True,
    storage=sqlite_storage,
    add_history_to_messages=True,
    enable_session_summaries=True,
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
user_id = 'parthchawla65@gmail.com'

# Here we dont need to pass the session_id inside the method as we have defined it in our agent itself, same goes for user_id if it is defined inside the agent we dont need to pass it in every invoke.
agent.print_response('My name is Parth Chawla. I like to code, I am currently coding ai agents using agno.', user_id=user_id, session_id='003')
agent.print_response('What are my hobbies?', user_id=user_id)
agent.print_response('My love is Masha Israfilova', user_id=user_id)
agent.print_response('List down all the question i asked so far', user_id=user_id)

# We can get the session summary using the get_session_summary method of the Memory class.
# NOTE: The session summary takes a lot of time for each reply, as session summary is updated after each response, so it is recommended to use it only when needed.

# NOTE: Session summary is generated in run time, hence it leads to slow response. It is not stored anywhere and cannot be accessed again once the agent is stopped.
session_summary = memory.get_session_summary(
        user_id=user_id,
        session_id='003'
    )
# print(session_summary)
print(f"Session summary: {session_summary.summary}\n")



