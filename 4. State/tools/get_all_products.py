from agno.agent import Agent
from agno.tools import tool
from typing_extensions import TypedDict

class Product(TypedDict):
    """
    Structure for a product item.
    """
    name: str
    id: str
    price: float
    discount: float
    gst: float

# For the demo purposes we have not set the quantity of the available products, hence we are just fetching the products and caching them. In real world applications, you would have to fetch the products from a database each time and update the quantity of the products in the database.

@tool( name="get_products", show_result=True, stop_after_tool_call=False, description="Get list of available products from the inventory", requires_confirmation=False, cache_results=True, cache_dir='/Users/parth/Desktop/personal/agno/cache', cache_ttl=3600)
def get_products() -> list[Product]:
    """
    Fetch a list of available products.
    
    Returns:
        list[Product]: A list of product items.
    """
    # Simulating a product inventory
    products = [
        Product(name="Milk", id="prod001", price=160.0, discount=20.0, gst=26.0),
        Product(name="Cheese", id="prod002", price=280.0, discount=10.0, gst=25.0),
        Product(name="Eggs", id="prod003", price=140.0, discount=0.0, gst=20.0),
    ]
    return products