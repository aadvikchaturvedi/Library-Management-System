"""
Staff management component
"""

import streamlit as st
import pandas as pd
from src.models.staff import Staff


def show_staff():
    """Display staff management interface"""
    st.markdown("# Staff Management")
    
    staff_tab1, staff_tab2, staff_tab3 = st.tabs(
        ["View Staff", "Add Staff", "Update"]
    )
    
    db = st.session_state.db
    
    # View Staff
    with staff_tab1:
        st.subheader("All Staff Members")
        _view_staff(db)
    
    # Add Staff
    with staff_tab2:
        st.subheader("Add New Staff Member")
        _add_staff(db)
    
    # Update Staff
    with staff_tab3:
        st.subheader("Update Staff Member")
        _update_staff(db)


def _view_staff(db):
    """Display all staff members"""
    try:
        staff_members = db.get_staff()
        if staff_members:
            staff_data = []
            for staff in staff_members:
                staff_data.append({
                    "ID": staff.id,
                    "Name": staff.name,
                    "Age": staff.age,
                    "Gender": staff.gender,
                    "Role": staff.role
                })
            df = pd.DataFrame(staff_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No staff members found.")
    except Exception as e:
        st.error(f"Error loading staff: {str(e)}")


def _add_staff(db):
    """Form to add new staff member"""
    with st.form("add_staff_form"):
        name = st.text_input("Staff Name *", max_chars=100)
        age = st.number_input("Age *", min_value=18, max_value=100, value=28)
        gender = st.selectbox("Gender", ["M", "F", "Other"])
        role = st.text_input("Role/Position *", max_chars=50)
        
        if st.form_submit_button("Add Staff", use_container_width=True):
            if name and role:
                try:
                    new_staff = Staff(
                        name=name,
                        age=int(age),
                        gender=gender,
                        role=role
                    )
                    db.add_staff(new_staff)
                    st.success("Staff member added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding staff: {str(e)}")
            else:
                st.warning("Please fill in all required fields (*)")


def _update_staff(db):
    """Update existing staff member"""
    try:
        staff_members = db.get_staff()
        if staff_members:
            staff_names = {staff.id: staff.name for staff in staff_members}
            selected_staff_id = st.selectbox(
                "Select Staff to Update",
                options=list(staff_names.keys()),
                format_func=lambda x: f"{staff_names[x]} (ID: {x})"
            )
            
            selected_staff = next((s for s in staff_members if s.id == selected_staff_id), None)
            
            with st.form("update_staff_form"):
                name = st.text_input("Name", value=selected_staff.name)  # type: ignore
                age = st.number_input("Age", value=selected_staff.age, min_value=18)  # type: ignore
                gender_options = ["M", "F", "Other"]
                gender_index = gender_options.index(selected_staff.gender) if selected_staff.gender in gender_options else 0  # type: ignore
                gender = st.selectbox("Gender", gender_options, index=gender_index)
                role = st.text_input("Role/Position", value=selected_staff.role)  # type: ignore
                
                if st.form_submit_button("Update Staff", use_container_width=True):
                    try:
                        updated_staff = Staff(
                            id=selected_staff.id,  # type: ignore
                            name=name or "",  # type: ignore
                            age=int(age),  # type: ignore
                            gender=gender,
                            role=role or ""  # type: ignore
                        )
                        db.update_staff(selected_staff_id, updated_staff)
                        st.success("Staff member updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating staff: {str(e)}")
        else:
            st.info("No staff members available to update.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
