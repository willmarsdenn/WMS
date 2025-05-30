# WMS - Warehouse Management System 

## Requirements

- PyTest (For Testing)

## Features

- Inventory management with low stock product searching
- Supplier management
- Order Processing (Purchases and Sales)
- Financial Reporting
- Command Line Interface

## Usage

```bash
# Run tests
pytest

# Run WMS
python main.py
```

## Commands

```
# Add product to inventory
add_product 1201 "Floor Lamp" "A description of the floor lamp" 100 5 10

# Add a supplier
add_supplier 12 "Floor Lamps Inc" sales@floorlamps.com 0478378323

# Create and process orders
create_purchase_order 9214 12
add_order_item 1201 5
process_order

# View financial reports and statements
financial_report
low_stock_report
```

