# PLEASE NOTE: THIS FILE CONTAINS KNOWLEDGE WHICH WILL BE TAUGHT LATER IN THE COURSE. IT IS RECOMMENDED TO GO THROUGH THE FIRST 3 MODULES BEFORE PROCEEDING WITH THIS FILE, AS THE 2_team.py FILE IS A DEPRECATED.

# There are 3 modes inside the Team:
    # 1. Route
    # 2. Coordinate
    # 3. Collaborate
    
# The current file will explore the Route mode.

from agno.team import Team
from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
import os
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# AGENT 1
search_agent = Agent(
    name="Search Agent",
    role="An agent that can search the web using DuckDuckGo.",
    instructions="Always include the sources",
    tools=[DuckDuckGoTools()],
    model=Groq(
        id="qwen/qwen3-32b",
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
    model=Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)


# How does the Route mode work?
# In the route mode, the the team leader in this case the team analyses the query and determines which agent is best suited to handle the query.
# The query is then forwarded to that team member
# The response from the team member is then returned directly to the user.

team = Team(
    name = 'Agent Team',
    mode = 'route',
    model= Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    members=[search_agent, finance_agent],
    show_tool_calls=True,
    markdown=True,
    instructions=["Always include sources", "Use tables to display data", "For stock analysis always use the finance agent and for web search use the search agent"],
    show_members_responses=True,
)

team.print_response("how are the stocks prices of air india after the crash?")
# team.print_response("What is the status of the Air India Airplane Crash? What caused it? What is the current situation?")
