"""
Members management component
"""

import streamlit as st
import pandas as pd
from src.models.member import Member


def show_members():
    """Display member management interface"""
    st.markdown("# Member Management")
    
    member_tab1, member_tab2, member_tab3 = st.tabs(
        ["View Members", "Add Member", "Update"]
    )
    
    db = st.session_state.db
    
    # View Members
    with member_tab1:
        st.subheader("All Members")
        _view_members(db)
    
    # Add Member
    with member_tab2:
        st.subheader("Add New Member")
        _add_member(db)
    
    # Update Member
    with member_tab3:
        st.subheader("Update Member")
        _update_member(db)


def _view_members(db):
    """Display all members"""
    try:
        members = db.get_members()
        if members:
            members_data = []
            for member in members:
                members_data.append({
                    "ID": member.id,
                    "Name": member.name,
                    "Contact": member.contactNumber,
                    "Age": member.age,
                    "Gender": member.gender,
                    "Penalty": member.penalty if member.penalty else 0
                })
            df = pd.DataFrame(members_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No members found.")
    except Exception as e:
        st.error(f"Error loading members: {str(e)}")


def _add_member(db):
    """Form to add new member"""
    with st.form("add_member_form"):
        name = st.text_input("Member Name *", max_chars=100)
        contact = st.text_input("Contact Number *", max_chars=15)
        address = st.text_input("Address")
        age = st.number_input("Age", min_value=1, max_value=120, value=20)
        gender = st.selectbox("Gender", ["M", "F", "Other"])
        
        if st.form_submit_button("Add Member", use_container_width=True):
            if name and contact:
                try:
                    new_member = Member(
                        name=name,
                        contactNumber=contact,
                        address=address or "",  # type: ignore
                        age=age,
                        gender=gender,
                        penalty=0
                    )
                    db.add_member(new_member)
                    st.success("Member added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding member: {str(e)}")
            else:
                st.warning("Please fill in all required fields (*)")


def _update_member(db):
    """Update existing member"""
    try:
        members = db.get_members()
        if members:
            member_names = {member.id: member.name for member in members}
            selected_member_id = st.selectbox(
                "Select Member to Update",
                options=list(member_names.keys()),
                format_func=lambda x: f"{member_names[x]} (ID: {x})"
            )
            
            selected_member = next((m for m in members if m.id == selected_member_id), None)
            
            with st.form("update_member_form"):
                name = st.text_input("Name", value=selected_member.name)  # type: ignore
                contact = st.text_input("Contact Number", value=selected_member.contactNumber)  # type: ignore
                address = st.text_input("Address", value=selected_member.address if selected_member.address else "")  # type: ignore
                age = st.number_input("Age", value=selected_member.age if selected_member.age else 20, min_value=1)  # type: ignore
                gender_options = ["M", "F", "Other"]
                gender_index = gender_options.index(selected_member.gender) if selected_member.gender in gender_options else 0  # type: ignore
                gender = st.selectbox("Gender", gender_options, index=gender_index)
                
                if st.form_submit_button("Update Member", use_container_width=True):
                    try:
                        updated_member = Member(
                            id=selected_member.id,  # type: ignore
                            name=name or "",  # type: ignore
                            contactNumber=contact or "",  # type: ignore
                            address=address or "",  # type: ignore
                            age=age,  # type: ignore
                            gender=gender,
                            penalty=selected_member.penalty  # type: ignore
                        )
                        db.update_member(selected_member_id, updated_member)
                        st.success("Member updated successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating member: {str(e)}")
        else:
            st.info("No members available to update.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
