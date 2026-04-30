# Inventory Module

A simple Python inventory management module used for learning Codex interaction patterns.

## Project Structure
- `inventory.py` — Core inventory functions
- `test_inventory.py` — pytest test suite (incomplete)

## Known Issues
- `remove_item` crashes on missing items
- `apply_discount` treats percentage as a decimal instead of dividing by 100
- Test coverage is incomplete

## Conventions
- Python 3.11+
- pytest for testing
- Type hints encouraged
- Google-style docstrings
