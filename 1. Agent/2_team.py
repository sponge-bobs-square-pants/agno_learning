# THIS HAS BEEN DEPRECATED

from datetime import datetime
import json
from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.utils.pprint import pprint_run_response
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# define the agents
# Here we will see how we can use OpenAI instead of Groq for the agents.
# For each agent, we can define the Model which will be used for the agent's responses.

# AGENT 1
search_agent = Agent(
    name="Search Agent",
    role="An agent that can search the web using DuckDuckGo.",
    instructions="Always include the sources",
    tools=[DuckDuckGoTools()],
    model=OpenAIChat(
        id="gpt-4.1-mini",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)

# AGENT 2
finance_agent = Agent(
    name="Finance Agent",
    role="An agent that can fetch stock data using YFinance.",
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True,stock_fundamentals=True,company_info=True)],
    instructions="Use tables to display data",
    model=OpenAIChat(
        id="gpt-4.1-mini",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)

# MAKE A TEAM
agent_team = Agent(
    team=[search_agent, finance_agent],
    name="Agent Team",
    model=OpenAIChat(
        id="gpt-4.1-mini",
        temperature=0.0,
    ),
    instructions=["Always include sources", "Use tables to display data", "For stock analysis always use the finance agent and for web search use the search agent"],
    show_tool_calls=True,
    markdown=True,
)

agent_team.print_response("can you analyse the apple, google and microsoft stocks and tell me which one is the best to invest?")