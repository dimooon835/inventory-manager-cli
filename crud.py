from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models


def create_category(db: Session, name: str):
    try:
        category = models.Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Ошибка: Категория с таким именем уже существует или данные некорректны.")

def create_supplier(db: Session, name: str, phone: str = None, email: str = None):
    try:
        supplier = models.Supplier(name=name, phone=phone, email=email)
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier
    except IntegrityError:
        db.rollback()
        raise ValueError("Ошибка: Поставщик с таким именем или email уже существует.")

def create_product(db: Session, name: str, sku: str, category_id: int, supplier_id: int = None, 
                   purchase_price: float = 0.0, selling_price: float = 0.0, min_quantity: int = 0):
    try:
        product = models.Product(
            name=name, sku=sku, category_id=category_id, supplier_id=supplier_id,
            purchase_price=purchase_price, selling_price=selling_price, min_quantity=min_quantity
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    except IntegrityError:
        db.rollback()
        raise ValueError("Ошибка: Не удалось создать товар. Проверьте уникальность SKU, корректность ID связей и неотрицательность цен.")

def create_movement(db: Session, product_id: int, movement_type: str, quantity: int, comment: str = None):
    try:
        movement = models.StockMovement(product_id=product_id, movement_type=movement_type, quantity=quantity, comment=comment)
        db.add(movement)
        db.commit()
        db.refresh(movement)
        return movement
    except IntegrityError:
        db.rollback()
        raise ValueError("Ошибка: Не удалось зафиксировать операцию. Количество должно быть > 0, тип: IN, OUT или ADJUST.")


def get_categories(db: Session):
    return db.query(models.Category).all()

def get_suppliers(db: Session):
    return db.query(models.Supplier).all()

def get_products(db: Session):
    return db.query(models.Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def update_product_prices(db: Session, product_id: int, purchase: float = None, selling: float = None):
    product = get_product_by_id(db, product_id)
    if not product:
        return None
    try:
        if purchase is not None: product.purchase_price = purchase
        if selling is not None: product.selling_price = selling
        db.commit()
        return product
    except IntegrityError:
        db.rollback()
        raise ValueError("Ошибка: Цены не могут быть отрицательными.")

def deactivate_supplier(db: Session, supplier_id: int):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if supplier:
        supplier.is_active = False
        db.commit()
    return supplier

def deactivate_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if product:
        product.is_active = False
        db.commit()
    return product


def delete_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category:
        if db.query(models.Product).filter(models.Product.category_id == category_id).count() > 0:
            raise ValueError("Нельзя удалить категорию, если в ней есть товары.")
        db.delete(category)
        db.commit()
        return True
    return False

def delete_supplier(db: Session, supplier_id: int):
    supplier = db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()
    if supplier:
        if db.query(models.Product).filter(models.Product.supplier_id == supplier_id).count() > 0:
            raise ValueError("Нельзя удалить поставщика, если к нему привязаны товары.")
        db.delete(supplier)
        db.commit()
        return True
    return False

def delete_product(db: Session, product_id: int):
    product = get_product_by_id(db, product_id)
    if product:
        if db.query(models.StockMovement).filter(models.StockMovement.product_id == product_id).count() > 0:
            raise ValueError("Нельзя удалить товар, потому что по нему уже есть складские операции.")
        db.delete(product)
        db.commit()
        return True
    return False