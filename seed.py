import sys
from database import get_db, engine, Base
from models import Category, Supplier, Product, StockMovement, MovementType
# from crud import create_category, create_supplier, create_product, create_stock_movement

def seed_data(db):
    categories = {}
    for name in ["Electronics", "Furniture", "Office Supplies", "Tools"]:
        existing = db.query(Category).filter(Category.name == name).first()
        if existing:
            categories[name] = existing
        else:
            categories = Category(name=name)
            db.add(categories)
            db.flush()
            categories[name] = categories
            print(f"Категория создана")

    suppliers = {}
    supplier_list = [
        {"name": "TechTrade", "phone": "+123456789", "email": "info@techtrade.com"},
        {"name": "OfficeMarket", "phone": "+987654321", "email": "sales@officemarket.com"},
        {"name": "WoodFactory", "phone": "+555123456", "email": None},
        {"name": "GlobalTools", "phone": "+555987654", "email": "contact@globaltools.org"}
    ]

    for s in supplier_list:
        existing = db.query(Supplier).filter(Supplier.name == s["name"]).first()
        if existing:
            categories[s["name"]] = existing
        else:
            suppliers = Supplier(name=s["name"], phone=s["phone"], email=s["email"])
            db.add(suppliers)
            db.flush()
            suppliers[s["name"]] = suppliers
            print(f"Поставщик создан")

    if db.query(Product).count() == 0:
        products_data = [
            {"name": "Laptop Lenovo ThinkPad", "sku": "SKU-001", "cat": "Electronics", "sup": "TechTrade", "pp": 70000, "sp": 95000, "min": 5},
            {"name": "Wireless Mouse", "sku": "SKU-002", "cat": "Electronics", "sup": "TechTrade", "pp": 1500, "sp": 2500, "min": 20},
            {"name": "Office Chair", "sku": "SKU-003", "cat": "Furniture", "sup": "WoodFactory", "pp": 8000, "sp": 12000, "min": 3},
            {"name": "A4 Paper Pack", "sku": "SKU-004", "cat": "Office Supplies", "sup": "OfficeMarket", "pp": 300, "sp": 450, "min": 10},
            {"name": "Screwdriver Set", "sku": "SKU-005", "cat": "Tools", "sup": "GlobalTools", "pp": 1200, "sp": 1800, "min": 5},
            {"name": "Monitor 27 inch", "sku": "SKU-006", "cat": "Electronics", "sup": "TechTrade", "pp": 25000, "sp": 35000, "min": 2},
        ]

        for p in products_data:
            products = Product(
                name=p["name"],
                sku=p["sku"],
                category_id=categories[p["cat"]].id,
                supplier_id=suppliers[p["sup"]].id,
                purchase_price=p["pp"],
                selling_price=p["sp"],
                min_quantity=p["min"]
            )
            db.add(products)

        db.flush()
        print(f"Товары созданы")

    if db.query(StockMovement).count() == 0:
        first_product = db.query(Product).first()

        # movements_data = [
        #     {"sku": "SKU-001", "type": "IN", "qty": 10, "comment": "Поставка ноутбуков"},
        #     {"sku": "SKU-002", "type": "IN", "qty": 30, "comment": "Поставка мышек"},
        #     {"sku": "SKU-003", "type": "IN", "qty": 15, "comment": "Поставка кресел"},
        #     {"sku": "SKU-004", "type": "IN", "qty": 200, "comment": "Поставка бумаги А4"},
        #     {"sku": "SKU-005", "type": "IN", "qty": 25, "comment": "Поставка набора инструментов"},
        #     {"sku": "SKU-001", "type": "OUT", "qty": 2, "comment": "Списание ноутбуков"},
        #     {"sku": "SKU-002", "type": "OUT", "qty": 5, "comment": "Списание мышек"},
        #     {"sku": "SKU-004", "type": "OUT", "qty": 80, "comment": "Списание бумаги А4"},
        #     {"sku": "SKU-003", "type": "ADJUST", "qty": 1, "comment": "Корректировка кресел"},
        # ]

        if first_product:
            move_in = StockMovement(
                product_id=first_product.id,
                movement_type=MovementType.IN,
                quantity=50,
                comment="Начальное заполнение склада"
            )

            db.add(move_in)

            move_out = StockMovement(
                product_id=first_product.id,
                movement_type=MovementType.OUT,
                quantity=5,
                comment="Первая продажа"
            )

            db.add(move_out)
            print("Созданы начальные складские операции")
        else:
            print("Нет товаров для создания операций")

    db.commit()
    print("Seed завершён")

if __name__ == "__main__":
    try:
        with get_db() as db:
            seed_data(db)
    except Exception as e:
        print(f"Критическая ошибка")
        sys.exit(1)