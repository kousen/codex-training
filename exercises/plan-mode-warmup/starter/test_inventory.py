"""Inventory behavior, including currently permitted negative values."""
from copy import deepcopy

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


@pytest.mark.parametrize("quantity", [10, 0, -3])
def test_add_item(quantity):
    inv = {}
    add_item(inv, "Widget", quantity, 2.50)
    assert inv == {"Widget": {"quantity": quantity, "price": 2.50}}


def test_add_item_overwrites_existing_item_and_preserves_others():
    inv = {
        "Widget": {"quantity": 10, "price": 2.50},
        "Gadget": {"quantity": 5, "price": 10.00},
    }
    add_item(inv, "Widget", 2, 3.75)
    assert inv == {
        "Widget": {"quantity": 2, "price": 3.75},
        "Gadget": {"quantity": 5, "price": 10.00},
    }


def test_total_value():
    inv = {}
    add_item(inv, "Widget", 10, 2.50)
    add_item(inv, "Gadget", 5, 10.00)
    assert get_total_value(inv) == 75.00


def test_total_value_empty_inventory():
    assert get_total_value({}) == 0


@pytest.mark.parametrize(
    "quantity, price, expected", [(0, 2.50, 0), (-3, 2.50, -7.50), (3, 0, 0), (3, 0.10, 0.30)]
)
def test_total_value_edge_cases(quantity, price, expected):
    inv = {"Widget": {"quantity": quantity, "price": price}}
    assert get_total_value(inv) == pytest.approx(expected)


def test_remove_existing_item():
    inv = {"Widget": {"quantity": 10, "price": 2.50}}
    remove_item(inv, "Widget")
    assert inv == {}


def test_remove_item_preserves_other_items():
    inv = {
        "Widget": {"quantity": 10, "price": 2.50},
        "Gadget": {"quantity": 5, "price": 10.00},
    }
    remove_item(inv, "Widget")
    assert inv == {"Gadget": {"quantity": 5, "price": 10.00}}


def test_remove_missing_item():
    inv = {"Widget": {"quantity": 10, "price": 2.50}}
    remove_item(inv, "Missing")
    assert inv == {"Widget": {"quantity": 10, "price": 2.50}}


def test_remove_item_from_empty_inventory():
    inv = {}
    remove_item(inv, "Missing")
    assert inv == {}


@pytest.mark.parametrize(
    "percent, expected_price", [(0, 2.50), (20, 2.00), (12.5, 2.1875), (100, 0.00)]
)
def test_apply_discount(percent, expected_price):
    inv = {
        "Widget": {"quantity": 10, "price": 2.50},
        "Gadget": {"quantity": 5, "price": 10.00},
    }
    apply_discount(inv, "Widget", percent)
    assert inv["Widget"]["price"] == pytest.approx(expected_price)
    assert inv["Widget"]["quantity"] == 10
    assert inv["Gadget"] == {"quantity": 5, "price": 10.00}


def test_apply_discount_to_zero_price():
    inv = {"Widget": {"quantity": 10, "price": 0.00}}
    apply_discount(inv, "Widget", 20)
    assert inv == {"Widget": {"quantity": 10, "price": 0.00}}


def test_repeated_discounts_use_current_price():
    inv = {"Widget": {"quantity": 10, "price": 100.00}}
    apply_discount(inv, "Widget", 20)
    apply_discount(inv, "Widget", 20)
    assert inv["Widget"]["price"] == pytest.approx(64.00)


@pytest.mark.parametrize("populated", [False, True])
def test_apply_discount_missing_item_raises_without_mutation(populated):
    inv = {"Widget": {"quantity": 10, "price": 2.50}} if populated else {}
    original = deepcopy(inv)
    with pytest.raises(KeyError, match="Missing"):
        apply_discount(inv, "Missing", 20)
    assert inv == original


def test_find_low_stock():
    inv = {
        "Negative": {"quantity": -2, "price": 1.00},
        "Zero": {"quantity": 0, "price": 1.00},
        "Below": {"quantity": 3, "price": 1.00},
        "At threshold": {"quantity": 5, "price": 1.00},
        "Above": {"quantity": 50, "price": 1.00},
    }
    assert set(find_low_stock(inv, 5)) == {"Negative", "Zero", "Below"}


@pytest.mark.parametrize("threshold", [-1, 0, 5])
def test_find_low_stock_empty_inventory(threshold):
    assert find_low_stock({}, threshold) == []


@pytest.mark.parametrize("threshold, expected", [(-2, []), (0, ["Widget"]), (1, ["Widget"])])
def test_find_low_stock_negative_quantity_and_threshold(threshold, expected):
    inv = {"Widget": {"quantity": -2, "price": 2.50}}
    assert find_low_stock(inv, threshold) == expected


@pytest.mark.parametrize(
    "quantity, amount, expected", [(10, 5, 15), (10, 0, 10), (10, -3, 7), (10, -15, -5), (-3, 5, 2)]
)
def test_restock(quantity, amount, expected):
    inv = {
        "Widget": {"quantity": quantity, "price": 2.50},
        "Gadget": {"quantity": 5, "price": 10.00},
    }
    restock(inv, "Widget", amount)
    assert inv == {
        "Widget": {"quantity": expected, "price": 2.50},
        "Gadget": {"quantity": 5, "price": 10.00},
    }


@pytest.mark.parametrize("populated", [False, True])
def test_restock_missing_item_raises_without_mutation(populated):
    inv = {"Widget": {"quantity": 10, "price": 2.50}} if populated else {}
    original = deepcopy(inv)
    with pytest.raises(KeyError, match="Missing"):
        restock(inv, "Missing", 5)
    assert inv == original


def test_report_contains_sorted_items_formatted_values_and_total():
    inv = {
        "Widget": {"quantity": 3, "price": 2.50},
        "Gadget": {"quantity": 2, "price": 1.234},
    }
    lines = generate_report(inv).splitlines()
    assert lines[0] == "=== Inventory Report ==="
    assert lines[1].split() == ["Item", "Qty", "Price", "Value"]
    assert lines[2] == lines[-2] == "-" * 45
    assert [line.split() for line in lines[3:-2]] == [
        ["Gadget", "2", "1.23", "2.47"],
        ["Widget", "3", "2.50", "7.50"],
    ]
    assert lines[-1].split() == ["Total", "9.97"]


def test_report_empty_inventory():
    lines = generate_report({}).splitlines()
    assert len(lines) == 5
    assert lines[0] == "=== Inventory Report ==="
    assert lines[1].split() == ["Item", "Qty", "Price", "Value"]
    assert lines[2] == lines[3] == "-" * 45
    assert lines[-1].split() == ["Total", "0.00"]


@pytest.mark.parametrize("quantity, value", [(0, "0.00"), (-3, "-7.50")])
def test_report_zero_and_negative_quantities(quantity, value):
    inv = {"Widget": {"quantity": quantity, "price": 2.50}}
    lines = generate_report(inv).splitlines()
    assert lines[3].split() == ["Widget", str(quantity), "2.50", value]
    assert lines[-1].split() == ["Total", value]


def test_queries_do_not_mutate_inventory():
    inv = {
        "Widget": {"quantity": 3, "price": 2.50},
        "Gadget": {"quantity": 5, "price": 10.00},
    }
    original = deepcopy(inv)
    get_total_value(inv)
    find_low_stock(inv, 5)
    generate_report(inv)
    assert inv == original
