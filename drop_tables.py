import sys
from database import engine, Base

def main():
    print("Этот скрипт удалит ВСЕ таблицы из базы данных!")
    confirm = input("Введите 'YES' для подтверждения удаления: ")
    
    if confirm != "YES":
        print("Операция отменена.")
        return

    try:
        Base.metadata.drop_all(bind=engine)
        print("Все таблицы успешно удалены.")
    except Exception as e:
        print(f"Произошла ошибка при удалении таблиц: {e}")

if __name__ == "__main__":
    main()
