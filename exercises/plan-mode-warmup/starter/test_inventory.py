"""Basic tests for inventory module — some are missing, some will fail."""
from inventory import (
    add_item,
    apply_discount,
    find_low_stock,
    generate_report,
    get_total_value,
    remove_item,
    restock,
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


def test_remove_missing_item_does_not_crash():
    inv = {}
    remove_item(inv, "Missing")
    assert inv == {}


def test_apply_discount_uses_percentage():
    inv = {}
    add_item(inv, "Widget", 10, 20.00)
    apply_discount(inv, "Widget", 25)
    assert inv["Widget"]["price"] == 15.00


def test_find_low_stock():
    inv = {}
    add_item(inv, "Widget", 3, 2.50)
    add_item(inv, "Gadget", 50, 10.00)
    low = find_low_stock(inv, 5)
    assert "Widget" in low
    assert "Gadget" not in low


def test_restock_adds_to_existing_quantity():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    restock(inv, "Widget", 5)
    assert inv["Widget"]["quantity"] == 15


def test_report_contains_header():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    report = generate_report(inv)
    assert "Inventory Report" in report


def test_report_handles_empty_inventory():
    report = generate_report({})
    assert "Inventory Report" in report
    assert "Total" in report
    assert "0.00" in report
