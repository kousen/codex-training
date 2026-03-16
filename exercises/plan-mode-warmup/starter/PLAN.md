# Reliability Hardening for `inventory.py`

## Summary
Strengthen the module without redesigning its API. Keep the current function names and dict-based usage, but make behavior explicit, validated, and fully covered by tests so callers get predictable outcomes instead of silent bad state.

## Key Changes
- Keep the current public functions and in-place mutation model; do not introduce a new object model.
- Add type hints for the inventory structure and item payloads so the contract is visible in code.
- Standardize input validation:
  - `add_item`: reject empty names, negative quantities, and negative prices.
  - `remove_item`: raise a clear `KeyError` with item name if the item does not exist.
  - `apply_discount`: raise on missing items and reject discounts outside `0..100`.
  - `restock`: raise on missing items and reject non-positive restock amounts.
  - `find_low_stock`: reject negative thresholds.
- Normalize error style so invalid caller input uses `ValueError` and missing inventory entries use `KeyError`.
- Improve docstrings to describe arguments, mutation behavior, and raised exceptions in Google style.
- Keep `generate_report` output format stable unless validation failures prevent invalid data from existing.

## Test Plan
- Add happy-path tests for `remove_item`, `restock`, and `apply_discount`.
- Add failure-path tests for all validation rules:
  - missing item removal, discount, and restock
  - negative quantity, negative price, invalid threshold
  - discount below `0` or above `100`
  - zero or negative restock amount
  - empty item names
- Add report-focused tests that verify sorted item order and total calculation formatting.
- Keep the suite at the unit-test level with `pytest`; no integration or I/O work is needed.

## Public API / Interface Impact
- Function names and parameter lists remain unchanged.
- Behavioral contract becomes stricter:
  - missing items no longer behave leniently
  - invalid numeric inputs are rejected instead of being allowed into state
- Internal typing additions are non-breaking and only improve readability/tooling.

## Assumptions
- Backward compatibility means preserving the existing dict-based API, not preserving lenient edge-case behavior.
- Raising exceptions for bad inputs is preferred over silent no-ops because the project priority is reliability.
- No persistence, CLI, or packaging work is needed for this improvement pass.
