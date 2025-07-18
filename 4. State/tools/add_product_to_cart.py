from agno.agent import Agent
from agno.tools import tool
from typing_extensions import TypedDict
from tools.get_all_products import Product

class UserSchema(TypedDict):
    """
    Structure for a user item.
    """
    name: str
    email: str
    phone: str
    address: str
    cart: list[Product]
    total_price: float
    total_discount: float
    total_gst: float

session_state = UserSchema(
    name= "",
    email= "",
    phone= "",
    address= "",
    cart= [],
    total_price= 0.0,
    total_discount= 0.0,
    total_gst= 0.0,
)

# We have defined 2 tools here, one will add the item to the cart, for demo puposes we are not checking if the item is already in the cart and increasing the quantity, we are just adding the item to the cart. In real world application you will check for the item in the cart and increase the quantity if it is already present.

# The second tool will show the cart contents and the total price, discount and gst of the cart.

@tool( name="add_item_to_cart", show_result=True, stop_after_tool_call=False, description="Add a product to the cart", requires_confirmation=False, cache_results=False)
def add_item_to_cart(agent: Agent, item: Product) -> str:
    """
    This tool adds an item to the user's cart.
    Args:
        agent (Agent): The agent instance.
        item (Product): The product item to be added to the cart.
    Returns:
        str: A confirmation message indicating the item has been added to the cart.
    """
    try:
        agent.session_state['cart'].append(item)
        agent.session_state['total_price'] += item['price']
        agent.session_state['total_discount'] += item['discount']
        agent.session_state['total_gst'] += item['gst']
        
        print(f"Item '{item}' added to cart for user")
        return f"{item['name']} added to cart."
    except Exception as e:
        print(f"Error adding item to cart: {e}")
        return f"Error adding item to cart: {str(e)}"

@tool( name="show_cart", show_result=True, stop_after_tool_call=False, description="Display the current cart contents and totals", requires_confirmation=False, cache_results=False)
def show_cart(agent: Agent) -> str:
    """
    Display the current cart contents and totals.
    Args:
        agent (Agent): The agent instance.
    Returns:
        str: A formatted string showing cart contents and totals.
    """
    try:
        cart = agent.session_state.get('cart', [])
        if not cart:
            return "Your cart is empty."
        
        cart_summary = "🛒 **Your Cart:**\n\n"
        for item in cart:
            cart_summary += f"• {item['name']} - ₹{item['price']:.2f} (Discount: ₹{item['discount']:.2f}, GST: ₹{item['gst']:.2f})\n"
        
        cart_summary += f"\n💰 **Totals:**\n"
        cart_summary += f"• Subtotal: ₹{agent.session_state['total_price']:.2f}\n"
        cart_summary += f"• Total Discount: ₹{agent.session_state['total_discount']:.2f}\n"
        cart_summary += f"• Total GST: ₹{agent.session_state['total_gst']:.2f}\n"
        cart_summary += f"• **Final Total: ₹{agent.session_state['total_price'] - agent.session_state['total_discount'] + agent.session_state['total_gst']:.2f}**"
        
        return cart_summary
    except Exception as e:
        return f"Error displaying cart: {str(e)}"
