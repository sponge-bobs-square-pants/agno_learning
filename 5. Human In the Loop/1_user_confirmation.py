from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
import requests
from agno.tools import tool
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

sqlite_storage = SqliteStorage(table_name="agent_sessions", db_file="../tmp/data.db")
memory_db = SqliteMemoryDb(table_name="memory", db_file="../tmp/data.db")
memory = Memory(db=memory_db)
user_id = 'parthchawla65@gmail.com'
session_id = "003"


# Here we set the tool along with the decorator and set the requires_confirmation to True
# This means the ai will ask the user for confirmation before calling the tool

@tool( name="get_data_joke", show_result=True, stop_after_tool_call=True, description="Fetch a random dad joke from the icanhazdadjoke API.", requires_confirmation=True)
def get_dad_joke() -> str:
    """
        Fetch a random dad joke.
        
        Returns:
            str: A random dad joke.
    """
    url = 'https://icanhazdadjoke.com'
    response = requests.get(url, headers={'Accept': 'application/json'})
    return response.json()['joke']



agent = Agent(
    name="General Agent",
    role="General chat agent",
    session_id=session_id,
    memory=memory,
    enable_agentic_memory=True,
    storage=sqlite_storage,
    add_history_to_messages=True,
    read_chat_history=True,
    num_history_runs=10,
    instructions="You are a helpful assistant that always responds in a polite, upbeat and positive manner.",
    model=OpenAIChat(
        id="gpt-4.1-mini",
        temperature=0.0,
    ),
    tools=[get_dad_joke],
    markdown=True,
    show_tool_calls=True,
)

while True:
    user_message = input("You: ")
    if user_message.lower() in ["exit", "quit"]:
        print("Exiting chat.")
        break

    response = agent.run(user_message)

    # We check if the agent is paused, if it is that means its waiting for some type of confirmation
    
    if agent.is_paused:
        print("Agent is paused, waiting for user confirmation...")
        # We check if any of the tools are waiting for the confirmation
        for tool in agent.run_response.tools_requiring_confirmation:
            print(f"Tool '{tool.tool_name}' requires confirmation before execution.")
            # If they do, we ask for that inside the while loop until we get it
            user_confirmation = input("Do you want to proceed with the tool call? (yes/no): ")
            while user_confirmation.lower() not in ['yes', 'no']:
                print("Invalid input. Please enter 'yes' or 'no'.")
                user_confirmation = input("Do you want to proceed with the tool call? (yes/no): ")
            tool.confirmed = user_confirmation.lower() == 'yes'
        # If we get the confirmation we resume the flow with the tool execution
        # If we get a rejection for the tool call, we continue with the normal flow.
        
        if user_confirmation.lower() == 'yes':
            response = agent.continue_run()
            print('HITL: ',response.content if hasattr(response, 'content') else response)
        else:
            print("Tool call cancelled by user.")
            # Resume normal chat by prompting the agent for a follow-up
            followup = agent.run("Tool call was cancelled. Let's continue our conversation.")
            print('HITL: ', followup.content if hasattr(followup, 'content') else followup)
    else:
        print('HITL: ', response.content if hasattr(response, 'content') else response)

