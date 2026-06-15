from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from typing import Optional, List
from models import Category, Suplier, Product, StockMovement, MovementType

def create_category(name):
    try:
        category = Category(name=name)

def get_all_categories():

def get_category_by_id():

def update_category_name():

def delete_category():


def create_supplier(name):
    try:
        supplier = Suplier(name=name)

def get_all_suppliers

def get_supplier_by_id

def update_supplier_contacts

def deactivate_supplier

def delete_supplier


def create_product(name):
    

def get_all_products

def get_product_by_id

def get_products_by_category

def get_products_by_supplier

def update_product_prices

def update_product_min_quantity

def deactivate_product

def delete_product


def create_stock_movement

def get_all_stock_movements

def get_movements_by_product

def delete_stock_movement