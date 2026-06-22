from database import engine, Base

Base.metadata.drop_all(bind=engine)
print("Таблицы удалены")