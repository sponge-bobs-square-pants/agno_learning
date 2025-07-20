# PLEASE NOTE: THIS FILE CONTAINS KNOWLEDGE WHICH WILL BE TAUGHT LATER IN THE COURSE. IT IS RECOMMENDED TO GO THROUGH THE FIRST 3 MODULES BEFORE PROCEEDING WITH THIS FILE, AS THE 2_team.py FILE IS A DEPRECATED.

# There are 3 modes inside the Team:
    # 1. Route
    # 2. Coordinate
    # 3. Collaborate
    
# The current file will explore the Coordinate mode.

from agno.team import Team
from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.newspaper4k import Newspaper4kTools
import os
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# AGENT 1
searcher = Agent(
    name="Search Agent",
    role="An agent that can search the web using DuckDuckGo.",
    instructions=[
        "Given a topic, first generate a list of 3 search terms related to that topic.",
        "For each search term, search the web and analyze the results.Return the 10 most relevant URLs to the topic.",
        "You are writing for the Times of India, so the quality of the sources is important."
    ],
    tools=[DuckDuckGoTools()],
    model=Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)

# AGENT 2
writer = Agent(
    name="Writer Agent",
    role="Writes a high-quality article",
    description=(
        "You are a senior writer for the Times of India. Given a topic and a list of URLs, "
        "your goal is to write a high-quality TOI-worthy article on the topic."
    ),
    instructions=[
        "First read all urls using `read_article`."
        "Then write a high-quality TOI-worthy article on the topic."
        "The article should be well-structured, informative, engaging and catchy.",
        "Ensure the length is at least as long as a TOI cover story -- at a minimum, 15 paragraphs.",
        "Ensure you provide a nuanced and balanced opinion, quoting facts where possible.",
        "Focus on clarity, coherence, and overall quality.",
        "Never make up facts or plagiarize. Always provide proper attribution.",
        "Remember: you are writing for the Times of India, so the quality of the article is important.",
    ],
    tools=[Newspaper4kTools()],
    model=Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)


# How does the coordinate mode work?
# In the coordinate mode, the team leader (in this case, the editor) receives the query from the user.
# It analyses the query and determines how to break it down into sub-tasks.
# It then forwards the sub-tasks to the relevant team members.
# Once the team members have completed there tasks, the results are returned to the leader(editor).
# The leader then combines the results and returns a final response to the user.

editor = Team(
    name = 'Editor',
    mode = 'coordinate',
    model= Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    description="You are a senior Times of India editor. Given a topic, your goal is to write a Times of India worthy article.",
    instructions=[
        "First ask the search journalist to search for the most relevant URLs for that topic.",
        "Then ask the writer to get an engaging draft of the article.",
        "Edit, proofread, and refine the article to ensure it meets the high standards of the Times of India.",
        "The article should be extremely articulate and well written. "
        "Focus on clarity, coherence, and overall quality.",
        "Remember: you are the final gatekeeper before the article is published, so make sure the article is perfect.",
        "Once you are satisfied with the article, return it to the user.",
    ],
    members=[writer, searcher],
    add_datetime_to_instructions=True, # To add date time to the instruction so the ai is aware of the current date and time.
    add_member_tools_to_system_message=False, # This can be tried to make the agent more consistently get the transfer tool call correct
    enable_agentic_context=True, # Allow the agent to maintain a shared context and send that to members.
    share_member_interactions=True, # Share all member responses with subsequent member requests.
    show_members_responses=True,
    show_tool_calls=True,
    markdown=True,
)

editor.print_response("Write an article about the Air India Airplane Crash.")
