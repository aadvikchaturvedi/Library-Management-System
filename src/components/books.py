"""
Books management component
"""

import streamlit as st
import pandas as pd
from src.models.book import Book


def show_books():
    """Display book management interface"""
    st.markdown("# Book Management")
    
    book_tab1, book_tab2, book_tab3, book_tab4 = st.tabs(
        ["View Books", "Add Book", "Search", "Update"]
    )
    
    db = st.session_state.db
    
    # View Books
    with book_tab1:
        st.subheader("All Books")
        _view_books(db)
    
    # Add Book
    with book_tab2:
        st.subheader("Add New Book")
        _add_book(db)
    
    # Search Books
    with book_tab3:
        st.subheader("Search Books")
        _search_books(db)
    
    # Update Book
    with book_tab4:
        st.subheader("Update Book")
        _update_book(db)


def _view_books(db):
    """Display all books"""
    try:
        books = db.get_books()
        if books:
            books_data = []
            for book in books:
                books_data.append({
                    "ID": book.id,
                    "Name": book.name,
                    "Quantity": book.quantity,
                    "Issued": book.issuedQuantity,
                    "Available": book.quantity - book.issuedQuantity,
                    "Status": book.status,
                    "Address": book.address
                })
            df = pd.DataFrame(books_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No books found in the library.")
    except Exception as e:
        st.error(f"Error loading books: {str(e)}")


def _add_book(db):
    """Form to add new book"""
    with st.form("add_book_form"):
        name = st.text_input("Book Name *", max_chars=100)
        quantity = st.number_input("Quantity *", min_value=1, value=1)
        address = st.text_input("Address/Location", max_chars=100)
        status = st.selectbox("Status", ["available", "unavailable"])
        
        if st.form_submit_button("Add Book", use_container_width=True):
            if name:
                try:
                    new_book = Book(
                        name=name,
                        quantity=int(quantity),
                        issuedQuantity=0,
                        address=address,
                        status=status
                    )
                    db.add_book(new_book)
                    st.success("Book added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding book: {str(e)}")
            else:
                st.warning("Please fill in all required fields (*)")


def _search_books(db):
    """Search books by keyword"""
    search_keyword = st.text_input("Enter book name to search:")
    if search_keyword:
        try:
            results = db.search_book(search_keyword)
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No books found matching your search.")
        except Exception as e:
            st.error(f"Error searching books: {str(e)}")


def _update_book(db):
    """Update existing book"""
    try:
        books = db.get_books()
        if books:
            book_names = {book.id: book.name for book in books}
            selected_book_id = st.selectbox(
                "Select Book to Update",
                options=list(book_names.keys()),
                format_func=lambda x: f"{book_names[x]} (ID: {x})"
            )
            
            selected_book = next((b for b in books if b.id == selected_book_id), None)
            
            with st.form("update_book_form"):
                name = st.text_input("Book Name", value=selected_book.name)  # type: ignore
                quantity = st.number_input("Quantity", value=selected_book.quantity, min_value=0)  # type: ignore
                address = st.text_input("Address", value=selected_book.address)  # type: ignore
                status = st.selectbox("Status", ["available", "unavailable"],   # type: ignore
                                    index=0 if selected_book.status == "available" else 1)  # type: ignore
                
                if st.form_submit_button("Update Book", use_container_width=True):
                    try:
                        updated_book = Book(
                            id=selected_book.id,  # type: ignore
                            name=name or "",  # type: ignore
                            quantity=int(quantity),  # type: ignore
                            issuedQuantity=selected_book.issuedQuantity,  # type: ignore
                            address=address or "",  # type: ignore
                            status=status  # type: ignore
                        )
                        db.update_book(selected_book_id, updated_book)
                        st.success("Book updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating book: {str(e)}")
        else:
            st.info("No books available to update.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
