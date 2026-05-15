from langchain.tools import tool


@tool
def check_order_status(order_id: str) -> str:
    return f"Order {order_id} is shipped and will arrive soon."


@tool
def get_product_details(product_name: str) -> str:
    return f"{product_name} is a high-quality product with warranty."