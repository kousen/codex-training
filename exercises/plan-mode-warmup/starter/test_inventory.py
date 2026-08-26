"""Comprehensive tests for the inventory module."""

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


def test_add_item_stores_quantity_and_price():
    inv = {}

    add_item(inv, "Widget", 10, 2.50)

    assert inv["Widget"] == {"quantity": 10, "price": 2.50}


def test_add_item_overwrites_existing_item():
    inv = {"Widget": {"quantity": 1, "price": 1.00}}

    add_item(inv, "Widget", 20, 3.50)

    assert inv["Widget"] == {"quantity": 20, "price": 3.50}


def test_add_item_allows_negative_quantity():
    inv = {}

    add_item(inv, "Backordered", -3, 4.00)

    assert inv["Backordered"]["quantity"] == -3


def test_remove_item_removes_existing_item():
    inv = {"Widget": {"quantity": 10, "price": 2.50}}

    remove_item(inv, "Widget")

    assert "Widget" not in inv


def test_remove_missing_item_leaves_inventory_unchanged():
    inv = {"Widget": {"quantity": 10, "price": 2.50}}

    remove_item(inv, "Missing")

    assert inv == {"Widget": {"quantity": 10, "price": 2.50}}


def test_get_total_value_sums_all_items():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    add_item(inv, "Gadget", 5, 10.00)

    assert get_total_value(inv) == pytest.approx(75.00)


def test_get_total_value_for_empty_inventory_is_zero():
    assert get_total_value({}) == 0


def test_get_total_value_includes_negative_quantities():
    inv = {
        "In stock": {"quantity": 5, "price": 10.00},
        "Backordered": {"quantity": -2, "price": 7.50},
    }

    assert get_total_value(inv) == pytest.approx(35.00)


def test_apply_discount_uses_percentage():
    inv = {"Widget": {"quantity": 10, "price": 79.99}}

    apply_discount(inv, "Widget", 12.5)

    assert inv["Widget"]["price"] == pytest.approx(69.99125)


@pytest.mark.parametrize(
    ("percent", "expected_price"),
    [(0, 100.00), (100, 0.00)],
)
def test_apply_discount_boundary_percentages(percent, expected_price):
    inv = {"Widget": {"quantity": 1, "price": 100.00}}

    apply_discount(inv, "Widget", percent)

    assert inv["Widget"]["price"] == pytest.approx(expected_price)


def test_apply_discount_for_missing_item_raises_key_error():
    with pytest.raises(KeyError):
        apply_discount({}, "Missing", 10)


def test_find_low_stock_returns_items_below_threshold():
    inv = {
        "Widget": {"quantity": 3, "price": 2.50},
        "Gadget": {"quantity": 50, "price": 10.00},
    }

    assert find_low_stock(inv, 5) == ["Widget"]


def test_find_low_stock_excludes_quantity_equal_to_threshold():
    inv = {"Widget": {"quantity": 5, "price": 2.50}}

    assert find_low_stock(inv, 5) == []


def test_find_low_stock_for_empty_inventory_is_empty():
    assert find_low_stock({}, 5) == []


def test_find_low_stock_includes_negative_quantities():
    inv = {"Backordered": {"quantity": -1, "price": 2.50}}

    assert find_low_stock(inv, 0) == ["Backordered"]


def test_restock_adds_to_existing_quantity():
    inv = {"Widget": {"quantity": 5, "price": 2.50}}

    restock(inv, "Widget", 7)

    assert inv["Widget"]["quantity"] == 12


def test_restock_with_negative_amount_reduces_quantity():
    inv = {"Widget": {"quantity": 2, "price": 2.50}}

    restock(inv, "Widget", -5)

    assert inv["Widget"]["quantity"] == -3


def test_restock_missing_item_raises_key_error():
    with pytest.raises(KeyError):
        restock({}, "Missing", 5)


def test_generate_report_contains_item_values_and_total():
    inv = {
        "Widget": {"quantity": 10, "price": 2.50},
        "Gadget": {"quantity": 5, "price": 10.00},
    }

    report = generate_report(inv)

    assert "=== Inventory Report ===" in report
    assert "Widget" in report
    assert "Gadget" in report
    assert "25.00" in report
    assert "50.00" in report
    assert "75.00" in report


def test_generate_report_sorts_items_by_name():
    inv = {
        "Widget": {"quantity": 1, "price": 1.00},
        "Gadget": {"quantity": 1, "price": 1.00},
    }

    report = generate_report(inv)

    assert report.index("Gadget") < report.index("Widget")


def test_generate_report_for_empty_inventory_has_zero_total():
    report = generate_report({})

    assert "Inventory Report" in report
    assert report.splitlines()[-1].endswith("0.00")
