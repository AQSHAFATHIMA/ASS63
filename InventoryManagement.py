from threading import Lock


class InventoryManagement:

    LOW_STOCK = 5
    REORDER_QUANTITY = 10

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

        return "Product added"

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

        return "Product removed"

    # Transfer Stock
    def transfer_stock(
            self, product, quantity,
            source, destination):

        if source not in self.warehouses:
            return "Invalid warehouse"

        if destination not in self.warehouses:
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

        return "Stock transferred"

    # Reorder
    def reorder(self, warehouse, product):

        if warehouse not in self.warehouses:
            return "Invalid warehouse"

        if product not in self.warehouses[warehouse]:
            return "Invalid product"

        if self.warehouses[warehouse][product] > self.LOW_STOCK:
            return "Reorder not required"

        self.warehouses[warehouse][product] += \
            self.REORDER_QUANTITY

        return "Reorder successful"

    # Supplier Management
    def add_supplier(self, supplier, product):

        if not supplier or not product:
            return "Invalid supplier/product"

        self.suppliers[product] = supplier

        return "Supplier added"

    def get_supplier(self, product):

        return self.suppliers.get(
            product, "Supplier not found"
        )

    # Low-stock Detection
    def low_stock(self, warehouse):

        if warehouse not in self.warehouses:
            return "Invalid warehouse"

        result = []

        for product, quantity in \
                self.warehouses[warehouse].items():

            if quantity <= self.LOW_STOCK:
                result.append(product)

        return result

    # Automatic Warehouse Selection
    def select_warehouse(self, product, quantity):

        if quantity <= 0:
            return "Invalid quantity"

        for warehouse in ["A", "B", "C"]:

            stock = self.warehouses[
                warehouse
            ].get(product, 0)

            if stock >= quantity:
                return warehouse

        return "No warehouse available"

    # Stock Availability
    def get_stock(self, warehouse, product):

        if warehouse not in self.warehouses:
            return None

        return self.warehouses[
            warehouse
        ].get(product, 0)
