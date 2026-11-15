import streamlit as st
from src.database.config import supabase
import time
from src.database.db import student_enrollment

# enrollment dialog in streamlit
@st.dialog("Quick Enrollment",icon=":material/bolt:",position="center")
def quick_auto_enroll_dialog(subject_code):
    student_id = st.session_state.student_data['student_id']
    res = supabase.table('subjects').select('*').eq('subject_code',subject_code).execute()
    if not res.data:
        st.error("Subject code not found!!")
        if st.button('Close'):
            st.query_params.clear()
            st.rerun()
    else:
        subject = res.data[0]
        subject_name = subject['name']
        subject_id = subject['subject_id']
        subject_code = subject['subject_code']
        check = supabase.table('subject_students').select('*').eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()
        # if student id and subject id already exist inn the subject_students table
        if check.data:
            # warn the user
            st.warning(f"You are already enrolled in {subject_code}!")
            if st.button("Got it!!"):
                st.query_params.clear()
                st.rerun()
        else:
            st.write(f"Would you like to enroll in {subject_name}({subject_code})?")
            tab1, tab2 = st.columns(2)
            with tab1:
                if st.button('No Thanks', type='primary', width= "stretch"):
                    st.query_params.clear()
                    st.rerun()
            with tab2:
                if st.button("Yes, Enroll Now!!"):
                    student_enrollment(student_id, subject_id)
                    st.toast(f"Enrolled Successfully in {subject_name}({subject_code})!!")
                    st.query_params.clear()
                    time.sleep(2)
                    st.rerun()
                    
                    
                        