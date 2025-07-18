from datetime import datetime
import json
from agno.agent import Agent
from agno.models.groq import Groq
from agno.utils.pprint import pprint_run_response
from agno.tools.duckduckgo import DuckDuckGoTools
import requests
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

def get_dad_jokes():
    """
    Fetch a random dad joke from the icanhazdadjoke API.

    Returns:
        str: random dad joke from the API.
    """
    
    url = 'https://icanhazdadjoke.com'
    response = requests.get(url, headers={'Accept': 'application/json'})
    # print(response.json())
    return response.json()['joke']

search_agent = Agent(
    name="Search Agent",
    description="An agent that can search the web using DuckDuckGo.",
    tools=[DuckDuckGoTools(), get_dad_jokes],
    model=Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)

search_agent.print_response("Can you tell me a dad joke?")