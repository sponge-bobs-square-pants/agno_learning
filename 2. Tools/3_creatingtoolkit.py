from agno.agent import Agent
from agno.tools import Toolkit
from agno.models.groq import Groq
from agno.utils.log import logger
import requests
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# The tool decorator cannot be used alongside the Toolkit.

class DadJokes(Toolkit):
    def __init__(self, **kwargs):
        super().__init__(
            name="DadJokes", 
            tools=[self.get_dad_joke, self.get_random_fact, self.get_inspirational_quote],
            **kwargs
        )

    def get_dad_joke(self) -> str:
        """
        Fetch a random dad joke.
        Returns:
            str: A random dad joke.
        """
        logger.info(f"Running get_dad_joke api")
        
        url = 'https://icanhazdadjoke.com'
        logger.info(f"Running get_dad_joke api")
        response = requests.get(url, headers={'Accept': 'application/json'})
        logger.debug(f"Result: {response.json()}")
        return response.json()['joke']

    def get_random_fact(self) -> str:
        """
        Fetch a random interesting fact.
        
        Returns:
            str: A random fact.
        """
        logger.info(f"Running get_random_fact api")
        
        url = 'https://uselessfacts.jsph.pl/random.json?language=en'
        response = requests.get(url)
        logger.debug(f"Result: {response.json()}")
        return response.json()['text']

    def get_inspirational_quote(self) -> str:
        """
        Fetch a random programming quote.
        
        Returns:
            str: A random programming quote.
        """
        logger.info(f"Running get_programming_quote api")
        
        url = 'https://zenquotes.io/api/random'
        response = requests.get(url, headers={'Accept': 'application/json'})
        
        quote_data = response.json()[0]
        return f'"{quote_data["q"]}" - {quote_data["a"]}'
    
agent = Agent(
    name="Random Agent",
    description="An agent that can get random things.",
    tools=[DadJokes()],
    model=Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)
# The exclude tools property excludes the tool calls mentioned and hence the agent wont have access to those tool calls
exclude_agent = Agent(
    name="Dad Joke Agent",
    description="An agent that can get dad jokes.",
    tools=[DadJokes(
                exclude_tools=["get_random_fact", "get_inspirational_quote"]
            )
        ],
    model=Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)

# The include tools property includes the tool calls mentioned and hence the agent will have access to those tool calls
include_toolkit = DadJokes(include_tools=["get_random_fact"])
include_agent = Agent(
    name="Fact Agent",
    role="An agent that can get random facts.",
    instructions="Get a random fact, if the user asks for anything else check if you have the tools to get it if not then return a message saying you don't have the tools to get it.",
    tools=[include_toolkit],
    model=Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)

# There is another property called requires_confirmation_tools which will be covered in module 5, this basically requires the user to confirm before the flow continues. Also commonly referred to as "Human in the loop" or HITL, this is used to get the user confirmation before proceeding with the tool call for important actions such as deleting data, making payments, etc.

agent.print_response("Give me a dad joke, then a random fact, and finally a inspirational quote.")
exclude_agent.print_response("Give me a random fact and an inspirational quote")
include_agent.print_response("Give me a dad joke and a inspirational quote")
