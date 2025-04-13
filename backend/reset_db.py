from database import engine, Base
from models import User, ClientConfig
from sqlalchemy import text

def reset_database():
    # Создаем соединение
    with engine.connect() as connection:
        # Отключаем все активные соединения с базой
        connection.execute(text("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = 'VPN_web_app'
            AND pid <> pg_backend_pid();
        """))
        connection.commit()
        
        # Удаляем базу данных
        connection.execute(text("DROP SCHEMA public CASCADE;"))
        connection.execute(text("CREATE SCHEMA public;"))
        connection.execute(text("GRANT ALL ON SCHEMA public TO postgres;"))
        connection.execute(text("GRANT ALL ON SCHEMA public TO public;"))
        connection.commit()
    
    print("База данных очищена")
    
    # Создаем таблицы заново
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы заново")

if __name__ == "__main__":
    reset_database() 