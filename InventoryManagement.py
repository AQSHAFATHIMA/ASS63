from threading import Lock

class InventoryManagement:

    LOW_STOCK = 5
    REORDER_QTY = 10

    def __init__(self):
        self.lock = Lock()

        self.warehouses = {
            "A": {},
            "B": {},
            "C": {}
        }

        self.suppliers = {}

    # Add Product
    def add_product(self, warehouse, product, quantity):

        if warehouse not in self.warehouses:
            return "Invalid warehouse"

        if not product:
            return "Invalid product"

        if quantity <= 0:
            return "Invalid quantity"

        with self.lock:
            self.warehouses[warehouse][product] = \
                self.warehouses[warehouse].get(product, 0) + quantity

        return "Product added successfully"

    # Remove Product
    def remove_product(self, warehouse, product, quantity):

        if warehouse not in self.warehouses:
            return "Invalid warehouse"

        if product not in self.warehouses[warehouse]:
            return "Invalid product"

        if quantity <= 0:
            return "Invalid quantity"

        if self.warehouses[warehouse][product] < quantity:
            return "Insufficient inventory"

        with self.lock:
            self.warehouses[warehouse][product] -= quantity

        return "Product removed successfully"

    # Transfer Stock
    def transfer_stock(self, product, quantity, source, destination):

        if source not in self.warehouses or \
           destination not in self.warehouses:
            return "Invalid warehouse"

        if source == destination:
            return "Invalid transfer"

        if product not in self.warehouses[source]:
            return "Invalid product"

        if quantity <= 0:
            return "Invalid quantity"

        if self.warehouses[source][product] < quantity:
            return "Insufficient inventory"

        with self.lock:
            self.warehouses[source][product] -= quantity

            self.warehouses[destination][product] = \
                self.warehouses[destination].get(product, 0) + quantity

        return "Stock transferred successfully"

    # Reorder
    def reorder(self, warehouse, product):

        if warehouse not in self.warehouses:
            return "Invalid warehouse"

        if product not in self.warehouses[warehouse]:
            return "Invalid product"

        if self.warehouses[warehouse][product] > self.LOW_STOCK:
            return "Reorder not required"

        with self.lock:
            self.warehouses[warehouse][product] += self.REORDER_QTY

        return "Stock reordered successfully"

    # Supplier Management
    def add_supplier(self, supplier, product):

        if not supplier or not product:
            return "Invalid supplier/product"

        self.suppliers[product] = supplier

        return "Supplier added successfully"

    def get_supplier(self, product):

        return self.suppliers.get(product, "Supplier not found")

    # Low Stock Detection
    def low_stock(self, warehouse):

        if warehouse not in self.warehouses:
            return "Invalid warehouse"

        result = []

        for product, quantity in self.warehouses[warehouse].items():

            if quantity <= self.LOW_STOCK:
                result.append(product)

        return result

    # Warehouse Selection
    def select_warehouse(self, product, quantity):

        if quantity <= 0:
            return "Invalid quantity"

        # Automatically select warehouse having
        # sufficient stock.
        for warehouse in ["A", "B", "C"]:

            stock = self.warehouses[warehouse].get(product, 0)

            if stock >= quantity:
                return warehouse

        return "No warehouse has sufficient stock"

    # Stock Availability
    def get_stock(self, warehouse, product):

        if warehouse not in self.warehouses:
            return None

        return self.warehouses[warehouse].get(product, 0)


# ---------------- MAIN PROGRAM ----------------

inventory = InventoryManagement()

print("===== INVENTORY MANAGEMENT =====")

print("\nAdding products...")

print(inventory.add_product("A", "Laptop", 10))
print(inventory.add_product("B", "Laptop", 5))
print(inventory.add_product("C", "Laptop", 8))

print(inventory.add_product("A", "Phone", 20))
print(inventory.add_product("B", "Phone", 15))
print(inventory.add_product("C", "Phone", 10))

print("\n1. Add Product")
print("2. Remove Product")
print("3. Transfer Stock")
print("4. Reorder")
print("5. Add Supplier")
print("6. Low Stock")
print("7. Select Warehouse")
print("8. Check Stock")

choice = input("\nEnter choice: ")

if choice == "1":

    w = input("Warehouse (A/B/C): ")
    p = input("Product: ")
    q = int(input("Quantity: "))

    print(inventory.add_product(w, p, q))

elif choice == "2":

    w = input("Warehouse (A/B/C): ")
    p = input("Product: ")
    q = int(input("Quantity: "))

    print(inventory.remove_product(w, p, q))

elif choice == "3":

    p = input("Product: ")
    q = int(input("Quantity: "))
    source = input("Source warehouse: ")
    destination = input("Destination warehouse: ")

    print(
        inventory.transfer_stock(
            p, q, source, destination
        )
    )

elif choice == "4":

    w = input("Warehouse (A/B/C): ")
    p = input("Product: ")

    print(inventory.reorder(w, p))

elif choice == "5":

    supplier = input("Supplier name: ")
    product = input("Product: ")

    print(
        inventory.add_supplier(
            supplier, product
        )
    )

elif choice == "6":

    w = input("Warehouse (A/B/C): ")

    print(
        "Low-stock products:",
        inventory.low_stock(w)
    )

elif choice == "7":

    product = input("Product: ")
    quantity = int(input("Required quantity: "))

    warehouse = inventory.select_warehouse(
        product, quantity
    )

    print("Automatically selected warehouse:", warehouse)

elif choice == "8":

    w = input("Warehouse (A/B/C): ")
    p = input("Product: ")

    stock = inventory.get_stock(w, p)

    if stock is None:
        print("Invalid warehouse")
    else:
        print("Available stock:", stock)

else:
    print("Invalid choice")
