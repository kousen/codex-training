"""Simple inventory management module with a few issues to fix."""


def add_item(inventory, name, quantity, price):
    """Add an item to inventory. Overwrites if item already exists."""
    inventory[name] = {"quantity": quantity, "price": price}


def remove_item(inventory, name):
    """Remove an item from inventory."""
    inventory.pop(name, None)


def get_total_value(inventory):
    """Calculate total value of all items in inventory."""
    total = 0
    for item in inventory:
        total += inventory[item]["quantity"] * inventory[item]["price"]
    return total


def apply_discount(inventory, name, percent):
    """Apply a percentage discount to an item's price."""
    item = inventory[name]
    item["price"] = item["price"] - (item["price"] * percent / 100)


def find_low_stock(inventory, threshold):
    """Find items with quantity below threshold."""
    results = []
    for name in inventory:
        if inventory[name]["quantity"] < threshold:
            results.append(name)
    return results


def restock(inventory, name, amount):
    """Add stock to an existing item."""
    inventory[name]["quantity"] = inventory[name]["quantity"] + amount


def generate_report(inventory):
    """Generate a simple text report of inventory."""
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
