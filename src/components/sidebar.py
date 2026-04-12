"""
Sidebar component for navigation
"""

import streamlit as st


def show_sidebar():
    """Display the sidebar with navigation options"""
    st.sidebar.markdown("# Navigation")
    page = st.sidebar.radio(
        "Select a section:",
        ["Dashboard", "Books", "Members", "Staff", "Transactions"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "**Library Management System**\n\n"
        "A comprehensive system to manage books, members, staff, and transactions."
    )
    
    return page
