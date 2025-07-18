from datetime import datetime
import json
from agno.agent import Agent
from agno.models.groq import Groq
from agno.utils.pprint import pprint_run_response
from agno.tools.duckduckgo import DuckDuckGoTools

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

search_agent = Agent(
    name="Search Agent",
    description="An agent that can search the web using DuckDuckGo.",
    tools=[DuckDuckGoTools()],
    model=Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)

search_agent.print_response("What is the status of the Air India Airplane Crash? What caused it? What is the current situation?")