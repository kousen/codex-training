"""Tests for inventory module behavior and validation."""
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
    assert inv["Widget"]["price"] == 2.50


def test_add_item_overwrites_existing_item():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    add_item(inv, "Widget", 5, 3.00)
    assert inv["Widget"] == {"quantity": 5, "price": 3.00}


def test_add_item_rejects_empty_name():
    inv = {}
    with pytest.raises(ValueError, match="must not be empty"):
        add_item(inv, "   ", 10, 2.50)


def test_add_item_rejects_negative_quantity():
    inv = {}
    with pytest.raises(ValueError, match="non-negative"):
        add_item(inv, "Widget", -1, 2.50)


def test_add_item_rejects_negative_price():
    inv = {}
    with pytest.raises(ValueError, match="non-negative"):
        add_item(inv, "Widget", 1, -0.01)


def test_total_value():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    add_item(inv, "Gadget", 5, 10.00)
    assert get_total_value(inv) == 75.00


def test_total_value_empty_inventory_is_zero():
    assert get_total_value({}) == 0.0


def test_find_low_stock():
    inv = {}
    add_item(inv, "Widget", 3, 2.50)
    add_item(inv, "Gadget", 50, 10.00)
    low = find_low_stock(inv, 5)
    assert "Widget" in low
    assert "Gadget" not in low


def test_find_low_stock_empty_inventory_returns_empty_list():
    assert find_low_stock({}, 5) == []


def test_find_low_stock_rejects_negative_threshold():
    with pytest.raises(ValueError, match="non-negative"):
        find_low_stock({}, -1)


def test_report_contains_header():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    report = generate_report(inv)
    assert "Inventory Report" in report


def test_report_empty_inventory_shows_zero_total():
    report = generate_report({})
    assert report.splitlines()[-1].startswith("Total")
    assert report.splitlines()[-1].endswith("0.00")


def test_report_sorts_items_and_includes_total():
    inv = {}
    add_item(inv, "Widget", 2, 5.00)
    add_item(inv, "Adapter", 1, 10.00)
    report = generate_report(inv)
    assert report.index("Adapter") < report.index("Widget")
    assert report.splitlines()[-1].startswith("Total")
    assert report.splitlines()[-1].endswith("20.00")


def test_remove_item_deletes_existing_item():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    remove_item(inv, "Widget")
    assert "Widget" not in inv


def test_remove_item_missing_key_raises_clear_error():
    inv = {}
    with pytest.raises(KeyError, match="Item not found: Missing"):
        remove_item(inv, "Missing")


def test_remove_item_rejects_empty_name():
    with pytest.raises(ValueError, match="must not be empty"):
        remove_item({}, "   ")


def test_apply_discount_uses_percentage_value():
    inv = {}
    add_item(inv, "Widget", 10, 100.00)
    apply_discount(inv, "Widget", 20)
    assert inv["Widget"]["price"] == 80.00


@pytest.mark.parametrize(
    ("percent", "expected_price"),
    [(0, 100.00), (100, 0.00)],
)
def test_apply_discount_accepts_boundary_percentages(percent, expected_price):
    inv = {}
    add_item(inv, "Widget", 10, 100.00)
    apply_discount(inv, "Widget", percent)
    assert inv["Widget"]["price"] == expected_price


def test_apply_discount_missing_item_raises():
    with pytest.raises(KeyError, match="Item not found: Missing"):
        apply_discount({}, "Missing", 20)


def test_apply_discount_rejects_empty_name():
    inv = {}
    add_item(inv, "Widget", 10, 100.00)
    with pytest.raises(ValueError, match="must not be empty"):
        apply_discount(inv, "   ", 20)


@pytest.mark.parametrize("percent", [-1, 101])
def test_apply_discount_rejects_out_of_range_percent(percent):
    inv = {}
    add_item(inv, "Widget", 10, 100.00)
    with pytest.raises(ValueError, match="between 0 and 100"):
        apply_discount(inv, "Widget", percent)


def test_restock_increases_quantity():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    restock(inv, "Widget", 5)
    assert inv["Widget"]["quantity"] == 15
    assert inv["Widget"]["price"] == 2.50


def test_restock_missing_item_raises():
    with pytest.raises(KeyError, match="Item not found: Missing"):
        restock({}, "Missing", 3)


def test_restock_rejects_empty_name():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    with pytest.raises(ValueError, match="must not be empty"):
        restock(inv, "   ", 3)


@pytest.mark.parametrize("amount", [0, -1])
def test_restock_rejects_non_positive_amount(amount):
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    with pytest.raises(ValueError, match="greater than zero"):
        restock(inv, "Widget", amount)
