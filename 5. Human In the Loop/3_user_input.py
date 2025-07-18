from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.tools import tool
from typing import Literal, List
from datetime import datetime
from agno.tools.function import UserInputField
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

# When more information is required from the user and not just a simple confirmation, we can do so by using the `requires_user_input` parameter in the tool decorator.

# This will trigger for asking for input fields defined in the `user_input_fields` parameter of the tool decorator.

# Here we set the tool along with the decorator and set the requires_confirmation to True
# This means the ai will ask the user for confirmation before calling the tool

# The fields which needs to be filled by the user are defined in the user_input_fields parameter
# If you leave the user_input_fields parameter empty, all the fields will be needed to be filled by the user

@tool( name="draft_email", show_result=True, stop_after_tool_call=True, description="Draft email for the user", requires_user_input=True, user_input_fields=['to', 'tone'])
def draft_email(to: str, subject: str, body: str, tone: Literal['casual', 'formal']) -> str:
    """
        Draft an email for the user
        Args:
            to (str): The recipient of the email.
            subject (str): The subject of the email.
            body (str): The body of the email.
            tone (Literal['casual', 'formal']): The tone of the email.
        Returns:
            str: The drafted email.
    """
    print(f"Tool called")
    now = datetime.now()
    hour = now.hour
    if 5 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    if tone == 'formal':
        greeting_line = f"{greeting}, {to}"
    else:
        greeting_line = f"Hey {to}, {greeting.lower()}!"

    email = f"""
        {greeting_line}

        Subject: {subject}

        {body}

        Best regards,\nYour HITL Assistant
    """
    return email.strip()

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
    instructions="You are a helpful assistant that always responds in a polite, upbeat and positive manner. Help the user draft emails, based upon the user's input. You will ask the user for the subject and what the email is about so that you can draft an email for them. Once you have the subject and the body of the email call the draft_email tool to draft the email.",
    model=OpenAIChat(
        id="gpt-4.1-mini",
        temperature=0.0,
    ),
    tools=[draft_email],
    markdown=True,
    show_tool_calls=True,
)


while True:
    user_message = input("You: ")
    if user_message.lower() in ["exit", "quit"]:
        print("Exiting chat.")
        break

    response = agent.run(user_message)
    # We check if the agent is paused, if it is that means its waiting for some type of confirmation or user input
    
    if agent.is_paused:
        # We check if any of the tools are waiting for the user input
        for tool in agent.run_response.tools_requiring_user_input:
            # If they do, we add the dict to inbuilt UserInputField imported frm agno and itterate over the it and ask for each field
            input_schema: List[UserInputField] = tool.user_input_schema 
            for field in input_schema:
                if field.value is None:
                    user_input = input(f"Please provide {field.name} ({field.field_type.__name__}): ")
                    field.value = user_input
                else:
                    print(f"Value provided by the agent: {field.value}")
        # Once done the normal flow resumes and the tool is executed
        response = agent.continue_run()
        print('HITL: ', response.content if hasattr(response, 'content') else response)
    else:
        print('HITL: ', response.content if hasattr(response, 'content') else response)

