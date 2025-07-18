from datetime import datetime
import json
from agno.agent import Agent
from agno.models.groq import Groq
from agno.utils.pprint import pprint_run_response
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools import tool
import requests
import os
from dotenv import load_dotenv
from typing import Any, Callable, Dict
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class CustomTool:
    """
    A custom tool that can be used by the agent.
    This tool fetches a random dad joke from the icanhazdadjoke API.
    """
    def logger(function_name: str, function_call: Callable, arguments: Dict[str, Any]):
        """
        Logs the function call and its arguments.
        
        Args:
            function_name (str): The name of the function being called.
            function_call (Callable): The function being called.
            arguments (Dict[str, Any]): The arguments passed to the function.
        """
        result = function_call(**arguments)
        print(f"Function call completed with result: {result}")
        return result
        
    # THE TOOL DECORATOR CAN TAKE THESE PROPERTIES, BELOW IS THE LIST AND THE EXPLANATION:
    
    # 1. NameL The name of the tool, which will be used to call it.
    
    # 2. Show_result: Whether to show the result of the tool call in the response, sometimes the tool might need to be called but the response does not need to appear the result.
    
    # 3. Stop_after_tool_call: Whether to stop the agent after the tool call or not, if set to True, the agent will stop after the tool call has been made and return the exact result of the tool call, if False, another AI call will be made to process the result of the tool call and AI will format the result.
    
    # 4. Description: A description of the tool.
    
    # 5. Tool_hooks: A list of hooks that will be called during the tool call.
    # You can have more properties here to define when the hooks are supposed to be called:
        # a. pre_hook: Hooks to run before the tool has been called. Generally can be used to change the data using logic
        # b. post_hook: Hooks to run after the tool has been called. Generally can be used to alter the response using logic
        
    # 6. Requires_confirmation: Whether the tool requires confirmation before being called or not.
    
    # 7. Cache_results: Whether to cache the results of the tool call or not, if set to True, the results will be cached and returned from the cache if the same tool is called again with the same arguments. Useful for situations where the results are deterministic, for example, list of departments in a hospital which will always be the same and not change, during that time we can cache the results and return them from the cache instead of calling the tool again saving time and resources.
    
    # 8. Cache_dir: The directory where the cache will be stored, if not provided, the cache will be stored in the default cache directory.
    
    # 9. Cache_ttl: The time to live for the cache, after which the cache will be invalidated and the tool will be called again, if not provided, the cache will never expire.
    
    # THERE CAN BE MORE PARAMETERS SUCH AS: requires_user_input, user_input_fields, external_execution
    # Exact list and explanation can be found at https://docs.agno.com/tools/tool-decorator
    @tool( name="get_data_joke", show_result=True, stop_after_tool_call=True, description="Fetch a random dad joke from the icanhazdadjoke API.", tool_hooks=[logger], requires_confirmation=False, cache_results=True, cache_dir='/Users/parth/Desktop/personal/agno/cache', cache_ttl=3600)
    
    def get_dad_joke() -> str:
        """
        Fetch a random dad joke.
        
        Returns:
            str: A random dad joke.
        """
        url = 'https://icanhazdadjoke.com'
        response = requests.get(url, headers={'Accept': 'application/json'})
        print(response.json())
        return response.json()['joke']

search_agent = Agent(
    name="Search Agent",
    description="An agent that can search the web using DuckDuckGo.",
    tools=[DuckDuckGoTools(), CustomTool.get_dad_joke],
    model=Groq(
        id="qwen/qwen3-32b",
        temperature=0.0,
    ),
    markdown=True,
    show_tool_calls=True,
)

search_agent.print_response("Can you tell me a dad joke?")