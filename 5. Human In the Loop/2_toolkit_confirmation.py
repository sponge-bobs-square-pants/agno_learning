from agno.agent import Agent
from agno.tools import Toolkit
from agno.models.openai import OpenAIChat
from agno.utils.log import logger
import requests
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

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
    
    
# For the toolkit, we just define the requires_confirmation_tools list which contains the tools that require confirmation before execution.
# This will be used in the agent to pause and ask for confirmation before executing the tool.
# The other tools will run without confirmation.

agent = Agent(
    name="Random Agent",
    description="An agent that can get random things.",
    tools=[DadJokes(requires_confirmation_tools=['get_dad_joke'])],
    model=OpenAIChat(
        id="gpt-4.1-mini",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)

while True:
    user_message = input("You: ")
    if user_message.lower() in ["exit", "quit"]:
        print("Exiting chat.")
        break

    response = agent.run(user_message)
    if agent.is_paused:
        for tool in agent.run_response.tools_requiring_confirmation:
            user_confirmation = input("Do you want to proceed with the tool call? (yes/no): ")
            while user_confirmation.lower() not in ['yes', 'no']:
                user_confirmation = input("Do you want to proceed with the tool call? (yes/no): ")
            tool.confirmed = user_confirmation.lower() == 'yes'
            
        if user_confirmation.lower() == 'yes':
            response = agent.continue_run()
            print('HITL: ',response.content if hasattr(response, 'content') else response)
        else:
            followup = agent.run("Tool call was cancelled. Let's continue our conversation.")
            print('HITL: ', followup.content if hasattr(followup, 'content') else followup)
    else:
        print('HITL: ', response.content if hasattr(response, 'content') else response)

