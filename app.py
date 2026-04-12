import streamlit as st
from src.backend.crud import LibraryDB
from src.components import (
    show_sidebar,
    show_dashboard,
    show_books,
    show_members,
    show_staff,
    show_transactions,
)

# Page configuration
st.set_page_config(
    page_title="Library Management System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for minimal styling
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize database connection
@st.cache_resource
def get_db():
    return LibraryDB()

# Store db in session state
if "db" not in st.session_state:
    st.session_state.db = get_db()

# =====================================================
# SIDEBAR NAVIGATION
# =====================================================
page = show_sidebar()

# =====================================================
# PAGE ROUTING
# =====================================================
if page == "Dashboard":
    show_dashboard()

elif page == "Books":
    show_books()

elif page == "Members":
    show_members()

elif page == "Staff":
    show_staff()

elif page == "Transactions":
    show_transactions()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 12px;'>Library Management System | All rights reserved.</p>",
    unsafe_allow_html=True
)
