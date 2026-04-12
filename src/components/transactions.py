"""
Transactions management component
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from src.models.transaction import Transaction


def show_transactions():
    """Display transaction management interface"""
    st.markdown("# Transaction Management")
    
    tx_tab1, tx_tab2, tx_tab3 = st.tabs(
        ["Issue Book", "Return Book", "View Transactions"]
    )
    
    db = st.session_state.db
    
    # Issue Book
    with tx_tab1:
        st.subheader("Issue Book to Member")
        _issue_book(db)
    
    # Return Book
    with tx_tab2:
        st.subheader("Return Book from Member")
        _return_book(db)
    
    # View Transactions
    with tx_tab3:
        st.subheader("All Transactions")
        _view_transactions(db)


def _issue_book(db):
    """Form to issue book to member"""
    try:
        books = db.get_books()
        members = db.get_members()
        
        if books and members:
            with st.form("issue_book_form"):
                book_names = {book.id: book.name for book in books if (book.quantity - book.issuedQuantity) > 0}
                member_names = {member.id: member.name for member in members}
                
                if not book_names:
                    st.warning("No books available for issue.")
                else:
                    selected_book_id = st.selectbox(
                        "Select Book *",
                        options=list(book_names.keys()),
                        format_func=lambda x: f"{book_names[x]} (Available: {next((b.quantity - b.issuedQuantity for b in books if b.id == x), 0)})"
                    )
                    
                    selected_member_id = st.selectbox(
                        "Select Member *",
                        options=list(member_names.keys()),
                        format_func=lambda x: f"{member_names[x]} (ID: {x})"
                    )
                    
                    due_days = st.number_input("Due Days", min_value=1, max_value=60, value=14)
                    
                    if st.form_submit_button("Issue Book", use_container_width=True):
                        try:
                            transaction = Transaction(
                                bookId=selected_book_id,
                                memberId=selected_member_id,
                                issuedAt=datetime.now(),
                                dueDate=datetime.now() + timedelta(days=due_days),
                                fine=0
                            )
                            db.issue_book(transaction)
                            st.success("Book issued successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error issuing book: {str(e)}")
        else:
            st.warning("Not enough data to issue books. Please add books and members first.")
    except Exception as e:
        st.error(f"Error: {str(e)}")


def _return_book(db):
    """Form to return book from member"""
    try:
        transactions = db.get_transactions()
        # Filter for active transactions (not yet returned)
        active_transactions = [tx for tx in transactions if tx.get("returnDate") is None]
        
        if active_transactions:
            tx_descriptions = {}
            for tx in active_transactions:
                tx_descriptions[tx["id"]] = f"Book {tx['bookId']} - Member {tx['memberId']} (Due: {tx['dueDate']})"
            
            with st.form("return_book_form"):
                selected_tx_id = st.selectbox(
                    "Select Transaction *",
                    options=[tx["id"] for tx in active_transactions],
                    format_func=lambda x: tx_descriptions[x]
                )
                
                if st.form_submit_button("Return Book", use_container_width=True):
                    try:
                        db.return_book(selected_tx_id)
                        st.success("Book returned successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error returning book: {str(e)}")
        else:
            st.info("No active transactions to return.")
    except Exception as e:
        st.error(f"Error: {str(e)}")


def _view_transactions(db):
    """Display all transactions"""
    try:
        transactions = db.get_transactions()
        if transactions:
            df = pd.DataFrame(transactions)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No transactions found.")
    except Exception as e:
        st.error(f"Error loading transactions: {str(e)}")
