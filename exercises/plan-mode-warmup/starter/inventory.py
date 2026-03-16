"""Simple inventory management helpers with explicit validation."""

from typing import TypedDict


class InventoryItem(TypedDict):
    """Stored inventory item state."""

    quantity: int
    price: float


Inventory = dict[str, InventoryItem]


def _validate_name(name: str) -> None:
    """Validate an inventory item name."""
    if not name.strip():
        raise ValueError("Item name must not be empty.")


def _require_existing_item(inventory: Inventory, name: str) -> InventoryItem:
    """Return an existing item or raise a clear error."""
    _validate_name(name)
    if name not in inventory:
        raise KeyError(f"Item not found: {name}")
    return inventory[name]


def add_item(inventory: Inventory, name: str, quantity: int, price: float) -> None:
    """Add an item to inventory.

    Args:
        inventory: Inventory mapping mutated in place.
        name: Item name. Must not be empty.
        quantity: Item quantity. Must be non-negative.
        price: Item price. Must be non-negative.

    Raises:
        ValueError: If the name is empty or quantity/price is negative.
    """
    _validate_name(name)
    if quantity < 0:
        raise ValueError("Quantity must be non-negative.")
    if price < 0:
        raise ValueError("Price must be non-negative.")
    inventory[name] = {"quantity": quantity, "price": price}


def remove_item(inventory: Inventory, name: str) -> None:
    """Remove an item from inventory.

    Args:
        inventory: Inventory mapping mutated in place.
        name: Item name to remove.

    Raises:
        KeyError: If the item does not exist.
        ValueError: If the name is empty.
    """
    _require_existing_item(inventory, name)
    del inventory[name]


def get_total_value(inventory: Inventory) -> float:
    """Calculate total value of all items in inventory.

    Args:
        inventory: Inventory mapping to summarize.

    Returns:
        The sum of quantity multiplied by price for each item.
    """
    total = 0.0
    for item in inventory.values():
        total += item["quantity"] * item["price"]
    return total


def apply_discount(inventory: Inventory, name: str, percent: float) -> None:
    """Apply a percentage discount to an item's price.

    Args:
        inventory: Inventory mapping mutated in place.
        name: Item name receiving the discount.
        percent: Discount percentage between 0 and 100 inclusive.

    Raises:
        KeyError: If the item does not exist.
        ValueError: If the name is empty or discount percent is invalid.
    """
    if percent < 0 or percent > 100:
        raise ValueError("Discount percent must be between 0 and 100.")
    item = _require_existing_item(inventory, name)
    item["price"] = item["price"] - (item["price"] * (percent / 100))


def find_low_stock(inventory: Inventory, threshold: int) -> list[str]:
    """Find items with quantity below a threshold.

    Args:
        inventory: Inventory mapping to inspect.
        threshold: Quantity threshold. Must be non-negative.

    Returns:
        A list of item names with quantity lower than the threshold.

    Raises:
        ValueError: If the threshold is negative.
    """
    if threshold < 0:
        raise ValueError("Threshold must be non-negative.")
    results = []
    for name, item in inventory.items():
        if item["quantity"] < threshold:
            results.append(name)
    return results


def restock(inventory: Inventory, name: str, amount: int) -> None:
    """Add stock to an existing item.

    Args:
        inventory: Inventory mapping mutated in place.
        name: Item name to update.
        amount: Quantity to add. Must be greater than zero.

    Raises:
        KeyError: If the item does not exist.
        ValueError: If the name is empty or amount is not positive.
    """
    if amount <= 0:
        raise ValueError("Restock amount must be greater than zero.")
    item = _require_existing_item(inventory, name)
    item["quantity"] = item["quantity"] + amount


def generate_report(inventory: Inventory) -> str:
    """Generate a fixed-width text report of inventory contents.

    Args:
        inventory: Inventory mapping to render.

    Returns:
        A multi-line string with:
        - a title line, ``=== Inventory Report ===``
        - a column header line for item name, quantity, price, and value
        - a separator line
        - one fixed-width row per item, sorted alphabetically by item name
        - a closing separator and a final total line

        Prices and per-item values are formatted with two decimal places.
    """
    lines = []
    lines.append("=== Inventory Report ===")
    lines.append(f"{'Item':<20} {'Qty':>5} {'Price':>8} {'Value':>10}")
    lines.append("-" * 45)
    for name in sorted(inventory.keys()):
        item = inventory[name]
        value = item["quantity"] * item["price"]
        lines.append(f"{name:<20} {item['quantity']:>5} {item['price']:>8.2f} {value:>10.2f}")
    lines.append("-" * 45)
    lines.append(f"{'Total':<20} {'':>5} {'':>8} {get_total_value(inventory):>10.2f}")
    return "\n".join(lines)
