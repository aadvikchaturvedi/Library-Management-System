"""
Database initialization and setup
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "library_management")


def create_database():
    """Create the database if it doesn't exist"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' created or already exists")
        
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"Error creating database: {e}")
        return False


def create_tables():
    """Create all necessary tables"""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Create Books table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                quantity INT NOT NULL,
                issuedQuantity INT DEFAULT 0,
                address VARCHAR(255),
                status VARCHAR(50) DEFAULT 'available',
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Books table created")
        
        # Create Members table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                contactNumber VARCHAR(20),
                address VARCHAR(255),
                age INT,
                gender VARCHAR(10),
                penalty INT DEFAULT 0,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Members table created")
        
        # Create Staff table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                age INT NOT NULL,
                gender VARCHAR(10),
                role VARCHAR(100),
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Staff table created")
        
        # Create Transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT PRIMARY KEY AUTO_INCREMENT,
                bookId INT NOT NULL,
                memberId INT NOT NULL,
                issuedAt DATETIME,
                dueDate DATETIME,
                returnDate DATETIME,
                fine INT DEFAULT 0,
                createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (bookId) REFERENCES books(id),
                FOREIGN KEY (memberId) REFERENCES members(id)
            )
        """)
        print("Transactions table created")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("All tables created successfully")
        return True
    except Error as e:
        print(f"Error creating tables: {e}")
        return False


def initialize_database():
    """Initialize the database and tables"""
    print("Initializing database...")
    if create_database():
        if create_tables():
            print("Database initialization completed successfully")
            return True
    return False


if __name__ == "__main__":
    initialize_database()
