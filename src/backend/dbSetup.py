import mysql.connector
from mysql.connector import Error
import os

class DBConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None
    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=os.getenv('MYSQL_PASSWORD'),
                database="library_db"
            )

            if self.conn.is_connected():
                self.cursor = self.conn.cursor(dictionary=True)
                print("Connected to MySQL Database")

        except Error as e:
            print("Error while connecting:", e)

    def close(self):
        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()
            print("Connection Closed")