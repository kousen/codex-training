"""Basic tests for inventory module — some are missing, some will fail."""
import pytest

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


def test_total_value_empty_inventory():
    assert get_total_value({}) == 0


def test_remove_existing_item():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    remove_item(inv, "Widget")
    assert "Widget" not in inv


def test_remove_missing_item_does_not_crash():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    remove_item(inv, "Gadget")
    assert inv == {"Widget": {"quantity": 10, "price": 2.50}}


def test_apply_discount_uses_percent():
    inv = {}
    add_item(inv, "Widget", 10, 100.00)
    apply_discount(inv, "Widget", 20)
    assert inv["Widget"]["price"] == 80.00


def test_apply_discount_missing_item_raises_key_error():
    with pytest.raises(KeyError):
        apply_discount({}, "Widget", 20)


def test_find_low_stock():
    inv = {}
    add_item(inv, "Widget", 3, 2.50)
    add_item(inv, "Gadget", 50, 10.00)
    low = find_low_stock(inv, 5)
    assert "Widget" in low
    assert "Gadget" not in low


def test_find_low_stock_excludes_items_equal_to_threshold():
    inv = {}
    add_item(inv, "Widget", 5, 2.50)
    assert find_low_stock(inv, 5) == []


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


def test_report_with_empty_inventory():
    report = generate_report({})

    assert "Inventory Report" in report
    assert "Item" in report
    assert "Total" in report
    assert "0.00" in report


def test_report_contains_sorted_items_and_total():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    add_item(inv, "Gadget", 5, 10.00)

    report = generate_report(inv)

    assert report.index("Gadget") < report.index("Widget")
    assert "Total" in report
    assert "75.00" in report
