"""Tests for inventory operations, boundary cases, and reports."""

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
    inv = {"Widget": {"quantity": 10, "price": 2.50}}

    add_item(inv, "Widget", 3, 4.00)

    assert inv == {"Widget": {"quantity": 3, "price": 4.00}}


def test_remove_existing_item_preserves_other_items():
    inv = {
        "Widget": {"quantity": 10, "price": 2.50},
        "Gadget": {"quantity": 5, "price": 10.00},
    }

    remove_item(inv, "Widget")

    assert inv == {"Gadget": {"quantity": 5, "price": 10.00}}


def test_remove_missing_item_from_empty_inventory():
    inv = {}

    remove_item(inv, "Missing")

    assert inv == {}


def test_remove_missing_item_preserves_inventory():
    inv = {"Widget": {"quantity": 10, "price": 2.50}}

    remove_item(inv, "Missing")

    assert inv == {"Widget": {"quantity": 10, "price": 2.50}}


@pytest.mark.parametrize(
    ("percent", "expected_price"),
    [(0, 19.99), (50, 9.995), (100, 0.0), (12.5, 17.49125)],
)
def test_apply_discount(percent, expected_price):
    inv = {
        "Widget": {"quantity": 10, "price": 19.99},
        "Gadget": {"quantity": 5, "price": 10.00},
    }

    apply_discount(inv, "Widget", percent)

    assert inv["Widget"]["price"] == pytest.approx(expected_price)
    assert inv["Widget"]["quantity"] == 10
    assert inv["Gadget"] == {"quantity": 5, "price": 10.00}


@pytest.mark.parametrize(("amount", "expected_quantity"), [(5, 15), (0, 10)])
def test_restock_preserves_price(amount, expected_quantity):
    inv = {"Widget": {"quantity": 10, "price": 2.50}}

    restock(inv, "Widget", amount)

    assert inv == {"Widget": {"quantity": expected_quantity, "price": 2.50}}


def test_total_value():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    add_item(inv, "Gadget", 5, 10.00)
    assert get_total_value(inv) == 75.00


def test_total_value_of_empty_inventory():
    assert get_total_value({}) == 0


def test_find_low_stock():
    inv = {}
    add_item(inv, "Widget", 3, 2.50)
    add_item(inv, "Gadget", 50, 10.00)
    low = find_low_stock(inv, 5)
    assert "Widget" in low
    assert "Gadget" not in low


def test_find_low_stock_excludes_quantity_at_threshold():
    inv = {
        "Below": {"quantity": 4, "price": 1.00},
        "At": {"quantity": 5, "price": 1.00},
        "Above": {"quantity": 6, "price": 1.00},
    }

    assert find_low_stock(inv, 5) == ["Below"]


def test_find_low_stock_in_empty_inventory():
    assert find_low_stock({}, 5) == []


def test_report_contains_header():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    report = generate_report(inv)
    assert "Inventory Report" in report


def test_report_contains_sorted_items_prices_values_and_total():
    inv = {
        "Widget": {"quantity": 3, "price": 2.50},
        "Gadget": {"quantity": 2, "price": 10.00},
    }

    lines = generate_report(inv).splitlines()
    rows = [line.split() for line in lines if line.startswith(("Gadget", "Widget"))]

    assert rows == [
        ["Gadget", "2", "10.00", "20.00"],
        ["Widget", "3", "2.50", "7.50"],
    ]
    assert lines[-1].split() == ["Total", "27.50"]


def test_report_with_empty_inventory():
    lines = generate_report({}).splitlines()

    assert lines[0] == "=== Inventory Report ==="
    assert lines[1].split() == ["Item", "Qty", "Price", "Value"]
    content_rows = [line.split() for line in lines[2:] if line.strip("-")]
    assert content_rows == [["Total", "0.00"]]
