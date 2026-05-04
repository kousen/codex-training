from inventory import remove_item, apply_discount, add_item
inv = {}
add_item(inv, 'Widget', 10, 100.0)

try:
    remove_item(inv, 'NonExistent')
    print('remove_item: FIXED')
except KeyError:
    print('remove_item: STILL BROKEN')

apply_discount(inv, 'Widget', 50)
expected = 50.0
actual = inv['Widget']['price']
print(f'apply_discount: price={actual} expected={expected} result={actual == expected}')