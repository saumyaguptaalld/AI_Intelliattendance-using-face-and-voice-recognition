import streamlit as st
from src.database.db import create_subject as db_create_subject

# create a new subject dialog in streamlit
@st.dialog("Create new subject")
def create_subject_dialog(teacher_id):
    st.write("Enter details of the new subject")
    sub_id = st.text_input("subject Code", placeholder="ML101")
    sub_name = st.text_input("Subject_name", placeholder= "Introduction to Machine learning")
    sub_section = st.text_input("Section", placeholder="A")
    st.button("Create Subject Now", type = "primary",width="stretch")
    if sub_id.strip() and sub_name.strip() and sub_section.strip():
        try:
            db_create_subject(sub_id.strip(), sub_name.strip(), sub_section.strip(),teacher_id)
            st.toast("Subject created successfully!!")
            st.rerun()
        except Exception as e:
            st.error(f"Error:{str(e)}")
    else:
        st.warning("All fields are required!!")