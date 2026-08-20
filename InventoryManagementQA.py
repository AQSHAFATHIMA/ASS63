from InventoryManagement import InventoryManagement
from threading import Thread


def test_stock_availability():

    inv = InventoryManagement()

    inv.add_product("A", "Laptop", 10)

    assert inv.get_stock("A", "Laptop") == 10

    print("Stock availability: PASS")


def test_insufficient_inventory():

    inv = InventoryManagement()

    inv.add_product("A", "Laptop", 5)

    result = inv.remove_product(
        "A", "Laptop", 10
    )

    assert result == "Insufficient inventory"

    print("Insufficient inventory: PASS")


def test_warehouse_transfer():

    inv = InventoryManagement()

    inv.add_product("A", "Laptop", 10)

    result = inv.transfer_stock(
        "Laptop", 4, "A", "B"
    )

    assert result == \
        "Stock transferred successfully"

    assert inv.get_stock("A", "Laptop") == 6

    assert inv.get_stock("B", "Laptop") == 4

    print("Warehouse transfer: PASS")


def order(inv):

    inv.remove_product(
        "A", "Laptop", 1
    )


def test_concurrent_orders():

    inv = InventoryManagement()

    inv.add_product("A", "Laptop", 10)

    threads = []

    for i in range(5):

        t = Thread(
            target=order,
            args=(inv,)
        )

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert inv.get_stock("A", "Laptop") == 5

    print("Concurrent orders: PASS")


def test_reorder_threshold():

    inv = InventoryManagement()

    inv.add_product("A", "Laptop", 5)

    result = inv.reorder(
        "A", "Laptop"
    )

    assert result == \
        "Stock reordered successfully"

    assert inv.get_stock("A", "Laptop") == 15

    print("Reorder threshold: PASS")


def test_invalid_product():

    inv = InventoryManagement()

    result = inv.remove_product(
        "A", "Mobile", 2
    )

    assert result == "Invalid product"

    print("Invalid product: PASS")


def test_negative_inventory():

    inv = InventoryManagement()

    inv.add_product("A", "Laptop", 5)

    result = inv.remove_product(
        "A", "Laptop", 10
    )

    assert result == "Insufficient inventory"

    assert inv.get_stock("A", "Laptop") >= 0

    print("Negative inventory prevention: PASS")


def test_multiple_warehouses():

    inv = InventoryManagement()

    inv.add_product("A", "Laptop", 5)
    inv.add_product("B", "Laptop", 10)
    inv.add_product("C", "Laptop", 20)

    assert len(inv.warehouses) == 3

    assert "A" in inv.warehouses
    assert "B" in inv.warehouses
    assert "C" in inv.warehouses

    print("Multiple warehouses: PASS")


def test_low_stock():

    inv = InventoryManagement()

    inv.add_product("A", "Laptop", 3)

    result = inv.low_stock("A")

    assert "Laptop" in result

    print("Low-stock detection: PASS")


def test_supplier_management():

    inv = InventoryManagement()

    result = inv.add_supplier(
        "ABC Suppliers",
        "Laptop"
    )

    assert result == \
        "Supplier added successfully"

    assert inv.get_supplier("Laptop") == \
        "ABC Suppliers"

    print("Supplier management: PASS")


def test_automatic_warehouse_selection():

    inv = InventoryManagement()

    inv.add_product("A", "Laptop", 2)
    inv.add_product("B", "Laptop", 10)
    inv.add_product("C", "Laptop", 20)

    warehouse = inv.select_warehouse(
        "Laptop", 8
    )

    assert warehouse == "B"

    print("Automatic warehouse selection: PASS")


# ---------------- RUN ALL TESTS ----------------

print("===== INVENTORY QA TESTING =====")

test_stock_availability()
test_insufficient_inventory()
test_warehouse_transfer()
test_concurrent_orders()
test_reorder_threshold()
test_invalid_product()
test_negative_inventory()
test_multiple_warehouses()

# Additional development requirements
test_low_stock()
test_supplier_management()
test_automatic_warehouse_selection()

print("\nALL INVENTORY TESTS PASSED")
