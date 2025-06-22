import psycopg2
from psycopg2 import Error

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                port="5432",
                database="postgres",
                user="postgres",
                password="roni7773"
            )
            print("Successfully connected to PostgreSQL")
            return self.connection
        except Error as e:
            print(f"Error connecting to PostgreSQL: {e}")
            return None
    
    def get_connection(self):
        if not self.connection or self.connection.closed:
            self.connect()
        return self.connection
    
    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")
