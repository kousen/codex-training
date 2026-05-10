"""Basic tests for inventory module — some are missing, some will fail."""
from inventory import (
    add_item,
    apply_discount,
    find_low_stock,
    generate_report,
    get_total_value,
    remove_item,
)


def test_add_item():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    assert "Widget" in inv
    assert inv["Widget"]["quantity"] == 10


def test_total_value():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    add_item(inv, "Gadget", 5, 10.00)
    assert get_total_value(inv) == 75.00


def test_remove_existing_item():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    remove_item(inv, "Widget")
    assert "Widget" not in inv


def test_remove_missing_item_does_not_raise():
    inv = {}
    remove_item(inv, "Missing")
    assert inv == {}


def test_apply_discount_uses_whole_percent():
    inv = {}
    add_item(inv, "Widget", 10, 100.00)
    apply_discount(inv, "Widget", 20)
    assert inv["Widget"]["price"] == 80.00


def test_find_low_stock():
    inv = {}
    add_item(inv, "Widget", 3, 2.50)
    add_item(inv, "Gadget", 50, 10.00)
    low = find_low_stock(inv, 5)
    assert "Widget" in low
    assert "Gadget" not in low


def test_report_contains_header():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    report = generate_report(inv)
    assert "Inventory Report" in report


def test_generate_report_with_empty_inventory():
    inv = {}
    report = generate_report(inv)
    assert report == "\n".join([
        "=== Inventory Report ===",
        f"{'Item':<20} {'Qty':>5} {'Price':>8} {'Value':>10}",
        "-" * 45,
        "-" * 45,
        f"{'Total':<20} {'':>5} {'':>8} {0:>10.2f}",
    ])
