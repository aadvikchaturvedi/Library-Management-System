import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import List

from src.models.book import Book
from src.models.member import Member
from src.models.staff import Staff
from src.models.transaction import Transaction


class LibraryDB:
    def __init__(self):
        self.conn = None
        self.cursor = None
        try:
            self.conn = mysql.connector.connect(
                host=os.getenv("DB_HOST") or "localhost",
                user=os.getenv("DB_USER") or "root",
                password=os.getenv("DB_PASSWORD") or "",
                database=os.getenv("DB_NAME") or "library_management"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            print("Database Connected Successfully")

        except Error as e:
            print("Database Connection Error:", e)
            self.cursor = None
            self.conn = None

    # =====================================================
    # BOOK CRUD
    # =====================================================

    def add_book(self, book: Book):
        sql = """
        INSERT INTO books(name, quantity, issuedQuantity, address, status)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (
            book.name,
            book.quantity,
            book.issuedQuantity,
            book.address,
            book.status
        ))
        self.conn.commit()

    def get_books(self) -> List[Book]:
        if not self.cursor:
            return []
        try:
            self.cursor.execute("SELECT * FROM books")
            rows = self.cursor.fetchall()

            return [
                Book(
                    id=int(row["id"]) if row["id"] else None,  # type: ignore
                    name=str(row["name"]) if row["name"] else "",  # type: ignore
                    quantity=int(row["quantity"]) if row["quantity"] else 0,  # type: ignore
                    issuedQuantity=int(row["issuedQuantity"]) if row["issuedQuantity"] else 0,  # type: ignore
                    address=str(row["address"]) if row["address"] else "",  # type: ignore
                    status=str(row["status"]) if row["status"] else ""  # type: ignore
                )
                for row in rows
            ]
        except Exception:
            return []

    def search_book(self, keyword: str):
        if not self.cursor:
            return []
        try:
            sql = "SELECT * FROM books WHERE name LIKE %s"
            self.cursor.execute(sql, ('%' + keyword + '%',))
            return self.cursor.fetchall()
        except Exception:
            return []

    def update_book(self, book_id: int, book: Book):
        sql = """
        UPDATE books
        SET name=%s,
            quantity=%s,
            issuedQuantity=%s,
            address=%s,
            status=%s
        WHERE id=%s
        """
        self.cursor.execute(sql, (
            book.name,
            book.quantity,
            book.issuedQuantity,
            book.address,
            book.status,
            book_id
        ))
        self.conn.commit()

    def delete_book(self, book_id: int):
        self.cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
        self.conn.commit()

    # =====================================================
    # MEMBER CRUD
    # =====================================================

    def add_member(self, member: Member):
        sql = """
        INSERT INTO members(name, contactNumber, address, age, gender, penalty)
        VALUES(%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (
            member.name,
            member.contactNumber,
            member.address,
            member.age,
            member.gender,
            member.penalty
        ))
        self.conn.commit()

    def get_members(self) -> List[Member]:
        if not self.cursor:
            return []
        try:
            self.cursor.execute("SELECT * FROM members")
            rows = self.cursor.fetchall()

            return [
                Member(
                    id=int(row["id"]) if row["id"] else None,  # type: ignore
                    name=str(row["name"]) if row["name"] else "",  # type: ignore
                    contactNumber=str(row["contactNumber"]) if row["contactNumber"] else "",  # type: ignore
                    address=str(row["address"]) if row["address"] else "",  # type: ignore
                    age=int(row["age"]) if row["age"] else 0,  # type: ignore
                    gender=str(row["gender"]) if row["gender"] else "",  # type: ignore
                    penalty=int(row["penalty"]) if row["penalty"] else 0  # type: ignore
                )
                for row in rows
            ]
        except Exception:
            return []

    def update_member(self, member_id: int, member: Member):
        sql = """
        UPDATE members
        SET name=%s,
            contactNumber=%s,
            address=%s,
            age=%s,
            gender=%s,
            penalty=%s
        WHERE id=%s
        """
        self.cursor.execute(sql, (
            member.name,
            member.contactNumber,
            member.address,
            member.age,
            member.gender,
            member.penalty,
            member_id
        ))
        self.conn.commit()

    def delete_member(self, member_id: int):
        self.cursor.execute("DELETE FROM members WHERE id=%s", (member_id,))
        self.conn.commit()

    # =====================================================
    # STAFF CRUD
    # =====================================================

    def add_staff(self, staff: Staff):
        sql = """
        INSERT INTO staff(name, age, gender, role)
        VALUES(%s, %s, %s, %s)
        """
        self.cursor.execute(sql, (
            staff.name,
            staff.age,
            staff.gender,
            staff.role
        ))
        self.conn.commit()

    def get_staff(self) -> List[Staff]:
        if not self.cursor:
            return []
        try:
            self.cursor.execute("SELECT * FROM staff")
            rows = self.cursor.fetchall()

            return [
                Staff(
                    id=int(row["id"]) if row["id"] else None,  # type: ignore
                    name=str(row["name"]) if row["name"] else "",  # type: ignore
                    age=int(row["age"]) if row["age"] else 0,  # type: ignore
                    gender=str(row["gender"]) if row["gender"] else "",  # type: ignore
                    role=str(row["role"]) if row["role"] else ""  # type: ignore
                )
                for row in rows
            ]
        except Exception:
            return []

    def update_staff(self, staff_id: int, staff: Staff):
        sql = """
        UPDATE staff
        SET name=%s,
            age=%s,
            gender=%s,
            role=%s
        WHERE id=%s
        """
        self.cursor.execute(sql, (
            staff.name,
            staff.age,
            staff.gender,
            staff.role,
            staff_id
        ))
        self.conn.commit()

    def delete_staff(self, staff_id: int):
        self.cursor.execute("DELETE FROM staff WHERE id=%s", (staff_id,))
        self.conn.commit()

    # =====================================================
    # TRANSACTIONS
    # =====================================================

    def issue_book(self, transaction: Transaction):
        self.cursor.execute(
            "SELECT quantity FROM books WHERE id=%s",
            (transaction.bookId,)
        )
        book = self.cursor.fetchone()

        if not book:
            raise ValueError("Book not found")

        if int(book["quantity"]) <= 0:  # type: ignore
            raise ValueError("Book not available")

        sql = """
        INSERT INTO transactions(bookId, memberId, issuedAt, dueDate, fine)
        VALUES(%s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (
            transaction.bookId,
            transaction.memberId,
            transaction.issuedAt,
            transaction.dueDate,
            transaction.fine
        ))

        self.cursor.execute("""
            UPDATE books
            SET quantity = quantity - 1,
                issuedQuantity = issuedQuantity + 1
            WHERE id=%s
        """, (transaction.bookId,))

        self.conn.commit()

    def return_book(self, transaction_id: int):
        self.cursor.execute("""
            SELECT id, bookId, memberId, dueDate, returnDate
            FROM transactions
            WHERE id=%s
        """, (transaction_id,))

        tx = self.cursor.fetchone()

        if not tx:
            raise ValueError("Transaction not found")

        if tx["returnDate"] is not None:  # type: ignore
            raise ValueError("Book already returned")

        today = datetime.now()
        fine = 0

        due_date = tx["dueDate"]  # type: ignore
        if today > due_date:  # type: ignore
            days_late = (today - due_date).days  # type: ignore
            fine = days_late * 5

        self.cursor.execute("""
            UPDATE transactions
            SET returnDate=%s,
                fine=%s
            WHERE id=%s
        """, (today, fine, transaction_id))

        self.cursor.execute("""
            UPDATE books
            SET quantity = quantity + 1,
                issuedQuantity = issuedQuantity - 1
            WHERE id=%s
        """, (int(tx["bookId"]),))  # type: ignore

        if fine > 0:
            self.cursor.execute("""
                UPDATE members
                SET penalty = penalty + %s
                WHERE id=%s
            """, (fine, int(tx["memberId"])))  # type: ignore

        self.conn.commit()
        print(f"Book Returned. Fine = {fine}")

    def get_transactions(self):
        if not self.cursor:
            return []
        try:
            self.cursor.execute("SELECT * FROM transactions")
            return self.cursor.fetchall()
        except Exception:
            return []

    # =====================================================
    # DASHBOARD
    # =====================================================

    def total_books(self):
        if not self.cursor:
            return 0
        try:
            self.cursor.execute(
                "SELECT COALESCE(SUM(quantity + issuedQuantity), 0) AS total FROM books"
            )
            result = self.cursor.fetchone()
            return int(result["total"]) if result else 0  # type: ignore
        except Exception:
            return 0

    def issued_books(self):
        if not self.cursor:
            return 0
        try:
            self.cursor.execute(
                "SELECT COALESCE(SUM(issuedQuantity), 0) AS total FROM books"
            )
            result = self.cursor.fetchone()
            return int(result["total"]) if result else 0  # type: ignore
        except Exception:
            return 0

    def total_members(self):
        if not self.cursor:
            return 0
        try:
            self.cursor.execute(
                "SELECT COUNT(*) AS total FROM members"
            )
            result = self.cursor.fetchone()
            return int(result["total"]) if result else 0  # type: ignore
        except Exception:
            return 0

    # =====================================================
    # CLOSE CONNECTION
    # =====================================================

    def close(self):
        self.cursor.close()
        self.conn.close()
        print("Database Connection Closed")