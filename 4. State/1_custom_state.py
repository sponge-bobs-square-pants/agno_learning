from agno.agent import Agent
from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from textwrap import dedent
####################### IMPORT FOR TOOLS AND CLASSES ################################

from tools.add_product_to_cart import add_item_to_cart, show_cart, session_state
from tools.get_all_products import get_products, Product

#####################################################################################
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

sqlite_storage = SqliteStorage(table_name="agent_sessions", db_file="../tmp/state.db")
memory_db = SqliteMemoryDb(table_name="memory", db_file="../tmp/state.db")
memory = Memory(db=memory_db)
user_id = 'parthchawla65@gmail.com'
session_id = '004'

# For adding a custom state to the agent, we need to pass a dictionary to the session_state parameter of the Agent class.
# This dictionary will automatically be saved in the storage. Note the memory only stores the user data.
# Try saying the following to see the memory and session working together:
    # My name is Parth Chawla and for breakfast I drink milk.
# RESTART THE SESSION TO SEE THE MEMORY PERSIST
    # Hey
    # Do u have my favorite products available
# This will likely show you that Milk is available.

# You can ask it to add Milk to your cart and then show the cart contents.
# You can also clear your preferences by just saying it: Can you clear my preferences please and also clear my name.

# Once the dictionary is passes inside the session_state, we will need to just pass the agent: Agent instance to the tools that require it, such as add_item_to_cart and show_cart.

# After which we manipulate the state using the agent.session_state dictionary.

# In case where u dont wanna use any values from the state inside the prompt(instructions) or in description it can be available by setting the add_state_in_messages parameter to True.

# The limitation is that since it is not a defined parameter, you cannot use it as a variable to pass through some function to keep the instruction at a different place, It should be passed just like a placeholder in the instruction string, and it will be replaced automatically by the agent at runtime.


# The state will be persist in the database:
# You can check the state by running the following command:
    # sqlite3 tmp/state.db
    # SELECT * FROM agent_sessions WHERE session_id = '004';
# Here you will be able to find that on each initialization the system prompt is initialized and the total_price is set.
# The session_state dict is at the end and the state persists.

shopping_agent = Agent(
    name="Shopping Agent",
    role="Shopping agent",
    session_id=session_id,
    user_id=user_id,
    session_state = session_state,
    memory=memory,
    enable_agentic_memory=True,
    storage=sqlite_storage,
    add_history_to_messages=True,
    read_chat_history=True,
    num_history_runs=10,
    instructions=dedent("""You are a helpful assistant that always responds in a polite, upbeat and positive manner. You will show the users the products available and if the user wants he can add them to there cart. Use the show_cart tool when users want to see their cart contents. The user's total so far is {total_price}"""),
    model=OpenAIChat(
        id="gpt-4.1-mini",
        temperature=0.0,
    ),
    tools=[add_item_to_cart, get_products, show_cart],
    markdown=True,
    show_tool_calls=True,
    add_state_in_messages= True,
)

def main():
    """
    Main function to run the shopping agent in a continuous loop.
    """
    print("🛍️  Welcome to the Shopping Agent!")
    print("💬 You can ask about products, add items to cart, or view your cart.")
    print("❌ Type 'quit', 'exit', or 'bye' to end the session.\n")
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n🙏 Thank you for shopping with us! Have a great day!")
                break
            if not user_input:
                print("Please enter a message or type 'quit' to exit.")
                continue
            print("\n🤖 Shopping Agent:")
            shopping_agent.print_response(user_input)
            
        except KeyboardInterrupt:
            print("\n\n🙏 Thank you for shopping with us! Have a great day!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {str(e)}")
            print("Please try again or type 'quit' to exit.")

if __name__ == "__main__":
    main()