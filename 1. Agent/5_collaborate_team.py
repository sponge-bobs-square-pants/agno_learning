# PLEASE NOTE: THIS FILE CONTAINS KNOWLEDGE WHICH WILL BE TAUGHT LATER IN THE COURSE. IT IS RECOMMENDED TO GO THROUGH THE FIRST 3 MODULES BEFORE PROCEEDING WITH THIS FILE, AS THE 2_team.py FILE IS A DEPRECATED.

# There are 3 modes inside the Team:
    # 1. Route
    # 2. Coordinate
    # 3. Collaborate
    
# The current file will explore the Collaborate mode.

from agno.team import Team
from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.arxiv import ArxivTools
import asyncio
import os
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# AGENT 1
reddit_researcher = Agent(
    name="Reddit Researcher",
    role="Research a topic on Reddit",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    add_name_to_instructions=True,
    instructions=("""
    You are a Reddit researcher.
    You will be given a topic to research on Reddit.
    You will need to find the most relevant posts on Reddit.
    """),
)

# AGENT 2
twitter_researcher = Agent(
    name="Twitter Researcher",
    model=OpenAIChat("gpt-4o"),
    role="Research trending discussions and real-time updates",
    tools=[DuckDuckGoTools()],
    add_name_to_instructions=True,
    instructions=("""
    You are a Twitter/X researcher.
    You will be given a topic to research on Twitter/X.
    You will need to find trending discussions, influential voices, and real-time updates.
    Focus on verified accounts and credible sources when possible.
    Track relevant hashtags and ongoing conversations.
    """),
)

# AGENT 3
academic_paper_researcher = Agent(
    name="Academic Paper Researcher",
    model=OpenAIChat("gpt-4o"),
    role="Research academic papers and scholarly content",
    tools=[GoogleSearchTools(), ArxivTools()],
    add_name_to_instructions=True,
    instructions=("""
    You are a academic paper researcher.
    You will be given a topic to research in academic literature.
    You will need to find relevant scholarly articles, papers, and academic discussions.
    Focus on peer-reviewed content and citations from reputable sources.
    Provide brief summaries of key findings and methodologies.
    """),
)

# AGENT 4
hackernews_researcher = Agent(
    name="HackerNews Researcher",
    model=OpenAIChat("gpt-4o"),
    role="Research a topic on HackerNews.",
    tools=[HackerNewsTools()],
    add_name_to_instructions=True,
    instructions=("""
    You are a HackerNews researcher.
    You will be given a topic to research on HackerNews.
    You will need to find the most relevant posts on HackerNews.
    """),
)

# How does the Collaborate mode work?
# In the Collaborate mode, the leader (discussion) sends a query to all team members.
# When running asynchronously this happens in parallel.
# Each team member processes the query and returns their response.
# The leader process the responses and combines them into a final response.

discussion = Team(
    name = 'Discussion Team',
    mode = 'collaborate',
    model= Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    instructions=[
        "You are a discussion master.",
        "You have to stop the discussion when you think the team has reached a consensus.",
    ],
    success_criteria="The team has reached a consensus.",
    members=[reddit_researcher, twitter_researcher, academic_paper_researcher, hackernews_researcher],
    show_tool_calls=True,
    add_datetime_to_instructions=True,
    enable_agentic_context=True,
    markdown=True,
    show_members_responses=True,
)

# For synchronous execution, you can use the following line:
# discussion.print_response("Start the discussion on the topic: 'What is the best way to learn to code?")

# for asynchronous execution, you can use the following line:
async def run_discussion():
    return discussion.print_response(
        "Start the discussion on the topic: 'What is the best way to implement RAG?'",
        stream=True,
        stream_intermediate_steps=True,
    )

if __name__ == "__main__":
    asyncio.run(run_discussion())
    
    