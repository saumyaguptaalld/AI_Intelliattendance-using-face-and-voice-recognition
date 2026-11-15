import streamlit as st
import time
from src.database.db import student_un_enrollment

# enrollment dialog in streamlit
@st.dialog("Un_enroll")
def un_enroll_dialog(student_id, subject_id,subject_code):
    st.warning(f"Are you sure you want to un-enroll from {subject_code}?")
    yes, no = st.columns(2)
    with yes:
        if st.button("Yes", type="primary", width= "stretch"):
            result = student_un_enrollment(student_id, subject_id)
            if result:
                st.toast(f"Successfully Un-Enrolled from {subject_code}!!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Enrollment cannot be removed")
    with no:
        if st.button("No", type="primary",width="stretch"):
            st.rerun()
         