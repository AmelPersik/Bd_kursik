import psycopg2
from psycopg2.extras import DictCursor
from config import DB_CONFIG


class Database:
    def __init__(self):
        """Инициализация подключения к базе данных."""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor(cursor_factory=DictCursor)
            print("Подключение к базе данных выполнено успешно.")
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def fetch_all(self, query, params=None):
        """Выполнить SELECT-запрос и вернуть все результаты."""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return []

    def execute(self, query, params=None):
        """Выполнить запрос INSERT/UPDATE/DELETE."""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            self.conn.rollback()

    def close(self):
        """Закрыть соединение с базой данных."""
        self.cursor.close()
        self.conn.close()
        print("Соединение с базой данных закрыто.")