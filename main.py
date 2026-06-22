import sys
from database import SessionLocal
import crud
import reports

def main_menu():
    db = SessionLocal()
    while True:
        print("\n=== Inventory Manager CLI ===")
        print("1. Создать категорию          11. Добавить поступление товара")
        print("2. Показать все категории     12. Добавить списание товара")
        print("3. Создать поставщика         13. Добавить корректировку остатка")
        print("4. Показать всех поставщиков  14. Показать историю операций")
        print("5. Деактивировать поставщика  15. Показать операции по товару")
        print("6. Создать товар              16. Показать текущие остатки")
        print("7. Показать все товары        17. Показать товары, которые заканчиваются")
        print("8. Показать товар по id       18. Показать общую стоимость склада")
        print("9. Обновить цену товара       19. Показать товары по категориям")
        print("10. Деактивировать товар      20. Показать товары по поставщикам")
        print("0. Выход")
        
        choice = input("\nВыберите пункт меню: ").strip()

        try:
            if choice == "1":
                name = input("Название категории: ")
                crud.create_category(db, name)
                print("Категория добавлена.")
            elif choice == "2":
                for c in crud.get_categories(db):
                    print(f"[{c.id}] {c.name}")
            elif choice == "3":
                name = input("Имя поставщика: ")
                phone = input("Телефон: ") or None
                email = input("Email: ") or None
                crud.create_supplier(db, name, phone, email)
                print("Поставщик добавлен.")
            elif choice == "4":
                for s in crud.get_suppliers(db):
                    print(f"[{s.id}] {s.name} | Активен: {s.is_active}")
            elif choice == "5":
                sid = int(input("ID поставщика для деактивации: "))
                crud.deactivate_supplier(db, sid)
                print("Статус изменен.")
            elif choice == "6":
                name = input("Название товара: ")
                sku = input("SKU: ")
                cid = int(input("ID категории: "))
                sid = input("ID поставщика (Enter если нет): ")
                sid = int(sid) if sid else None
                p_price = float(input("Закупочная цена: ") or 0)
                s_price = float(input("Продажная цена: ") or 0)
                min_q = int(input("Минимальный остаток: ") or 0)
                crud.create_product(db, name, sku, cid, sid, p_price, s_price, min_q)
                print("Товар добавлен.")
            elif choice == "7":
                for p, c_name, s_name in reports.get_products_with_details(db):
                    print(f"ID: {p.id} | {p.name} | SKU: {p.sku} | Кат: {c_name} | Пост: {s_name or 'Нет'} | Цена: {p.selling_price}")
            elif choice == "8":
                pid = int(input("ID товара: "))
                p = crud.get_product_by_id(db, pid)
                if p: print(f"{p.name} (SKU: {p.sku}) - Продажа: {p.selling_price}")
                else: print("Товар не найден.")
            elif choice == "9":
                pid = int(input("ID товара: "))
                p_price = float(input("Новая закуп. цена (Enter чтобы пропустить): ") or -1)
                s_price = float(input("Новая прод. цена (Enter чтобы пропустить): ") or -1)
                crud.update_product_prices(db, pid, 
                                           p_price if p_price >= 0 else None, 
                                           s_price if s_price >= 0 else None)
                print("Цены обновлены.")
            elif choice == "10":
                pid = int(input("ID товара для деактивации: "))
                crud.deactivate_product(db, pid)
                print("Товар деактивирован.")
            elif choice == "11":
                pid = int(input("ID товара: "))
                qty = int(input("Количество: "))
                comm = input("Комментарий: ")
                crud.create_movement(db, pid, "IN", qty, comm)
                print("Поступление оформлено.")
            elif choice == "12":
                pid = int(input("ID товара: "))
                qty = int(input("Количество: "))
                comm = input("Комментарий: ")
                crud.create_movement(db, pid, "OUT", qty, comm)
                print("Списание оформлено.")
            elif choice == "13":
                pid = int(input("ID товара: "))
                qty = int(input("Количество: "))
                comm = input("Комментарий: ")
                crud.create_movement(db, pid, "ADJUST", qty, comm)
                print("Корректировка оформлена.")
            elif choice == "14":
                for m, p in reports.get_operation_history(db):
                    print(f"{m.created_at} | {p.name} | {m.movement_type} | Кол-во: {m.quantity} | {m.comment or ''}")
            elif choice == "15":
                pid = int(input("ID товара: "))
                for m, p in reports.get_operation_history(db, pid):
                    print(f"{m.created_at} | {m.movement_type} | {m.quantity} | {m.comment or ''}")
            elif choice == "16":
                for name, stock in reports.get_all_current_stocks(db).items():
                    print(f"{name}: {stock}")
            elif choice == "17":
                for name, cur, min_q in reports.get_low_stock_products(db):
                    print(f"{name} (Остаток: {cur} / Мин: {min_q})")
            elif choice == "18":
                p_val, s_val, profit = reports.calculate_warehouse_value(db)
                print(f"Общая закупочная стоимость: {p_val}")
                print(f"Потенциальная выручка: {s_val}")
                print(f"Потенциальная прибыль: {profit}")
            elif choice == "19":
                cid = int(input("ID категории: "))
                for p in reports.get_products_by_category(db, cid):
                    print(f"{p.name} (SKU: {p.sku})")
            elif choice == "20":
                sid = int(input("ID поставщика: "))
                for p in reports.get_products_by_supplier(db, sid):
                    print(f"{p.name} (SKU: {p.sku})")
            elif choice == "0":
                print("Выход из программы.")
                break
            else:
                print("Некорректный выбор.")
        except Exception as e:
            print(f"\n[Ошибка] {e}")

    db.close()

if __name__ == "__main__":
    main_menu()
