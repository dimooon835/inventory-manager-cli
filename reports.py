from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Product, Category, Supplier, StockMovement, MovementType
import models

def calculate_stock(db: Session, product_id: int) -> int:
    movements = db.query(models.StockMovement).filter(models.StockMovement.product_id == product_id).all()
    stock = 0
    for m in movements:
        if m.movement_type in ('IN', 'ADJUST'):
            stock += m.quantity
        elif m.movement_type == 'OUT':
            stock -= m.quantity
    return stock

def get_products_with_details(db: Session):
    return db.query(
        models.Product, models.Category.name, models.Supplier.name
    ).join(models.Category, models.Product.category_id == models.Category.id)\
     .outerjoin(models.Supplier, models.Product.supplier_id == models.Supplier.id).all()

def get_operation_history(db: Session, product_id: int = None):
    query = db.query(models.StockMovement, models.Product).join(models.Product)
    if product_id:
        query = query.filter(models.StockMovement.product_id == product_id)
    return query.order_by(models.StockMovement.created_at.desc()).all()

def get_products_by_category(db: Session, cat_id: int):
    return db.query(models.Product).filter(models.Product.category_id == cat_id).all()

def get_products_by_supplier(db: Session, sup_id: int):
    return db.query(models.Product).filter(models.Product.supplier_id == sup_id).all()



def count_products_per_category(db: Session):
    return db.query(models.Category.name, func.count(models.Product.id))\
        .join(models.Product).group_by(models.Category.name).all()

def count_products_per_supplier(db: Session):
    return db.query(models.Supplier.name, func.count(models.Product.id))\
        .join(models.Product).group_by(models.Supplier.name).all()

def get_all_current_stocks(db: Session):
    products = db.query(models.Product).all()
    return {p.name: calculate_stock(db, p.id) for p in products}

def get_low_stock_products(db: Session):
    products = db.query(models.Product).all()
    low_stock = []
    for p in products:
        current = calculate_stock(db, p.id)
        if current <= p.min_quantity:
            low_stock.append((p.name, current, p.min_quantity))
    return low_stock

def calculate_warehouse_value(db: Session):
    products = db.query(models.Product).all()
    total_purchase_val = 0.0
    total_selling_val = 0.0
    total_profit_val = 0.0

    for p in products:
        stock = calculate_stock(db, p.id)
        total_purchase_val += stock * p.purchase_price
        total_selling_val += stock * p.selling_price
        total_profit_val += stock * (p.selling_price - p.purchase_price)

    return total_purchase_val, total_selling_val, total_profit_val


