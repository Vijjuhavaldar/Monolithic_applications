
from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data: dict):
        # Use a dictionary unpacking for more efficient object creation
        return Product(**data)


def list_products() -> list[Product]:
    # Optimize data fetching by batching and processing directly in the list comprehension
    products_data = dao.list_products()
    return [Product.load(product) for product in products_data]


def get_product(product_id: int) -> Product:
    # Fetch and validate product in one step
    if not (product_data := dao.get_product(product_id)):
        raise ValueError(f"Product with ID {product_id} not found.")
    return Product.load(product_data)


def add_product(product: dict):
    # Inline validation to ensure required keys exist in the product data
    required_keys = {'id', 'name', 'description', 'cost', 'qty'}
    if missing_keys := required_keys - product.keys():
        raise ValueError(f"Missing required keys: {missing_keys}")
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    # Validate input and ensure product exists before updating quantity
    if qty < 0:
        raise ValueError("Quantity cannot be negative")
    if not dao.get_product(product_id):
        raise ValueError(f"Product with ID {product_id} not found.")
    dao.update_qty(product_id, qty)
