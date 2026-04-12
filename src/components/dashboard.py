"""
Dashboard component
"""

import streamlit as st
import pandas as pd
from src.backend.crud import LibraryDB


def show_dashboard():
    """Display the dashboard with key metrics and recent transactions"""
    st.markdown("# Library Dashboard")
    
    try:
        db = st.session_state.db
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_books = db.total_books()
            st.metric("Total Books", total_books)
        
        with col2:
            issued_books = db.issued_books()
            st.metric("Issued Books", issued_books)
        
        with col3:
            total_members = db.total_members()
            st.metric("Total Members", total_members)
        
        with col4:
            available_books = total_books - issued_books
            st.metric("Available Books", available_books)
        
        st.markdown("---")
        
        # Recent Transactions
        st.subheader("Recent Transactions")
        transactions = db.get_transactions()
        if transactions:
            df = pd.DataFrame(transactions)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No transactions found.")
        
    except Exception as e:
        st.error(f"Error loading dashboard: {str(e)}")
