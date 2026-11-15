import streamlit as st
from src.database.config import supabase
import time
from src.database.db import student_enrollment

# enrollment dialog in streamlit
@st.dialog("Enroll in Subject",icon=":material/bolt:")
def enroll_dialog():
    st.write("Enter subject code to enroll in subject")
    join_code = st.text_input('Subject Code', placeholder='Eg. ML101')
    if st.button('Enroll Now', type='primary', width= "stretch"):
        if not join_code.strip():
            st.warning("Enter a valid Subject Code!!")
        else:
            res = supabase.table('subjects').select('subject_id,name,subject_code').eq('subject_code',join_code.strip()).execute()
            if res.data:
                subject = res.data[0]
                subject_code = subject['subject_code']
                subject_id = subject['subject_id']
                student_id = st.session_state.student_data['student_id']
                check = supabase.table('subject_students').select('*').eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()
                # if student id and subject id already exist inn the subject_students table
                if check.data:
                    # warn the user
                    st.warning(f"You are already enrolled in {subject_code}!")
                else:
                    student_enrollment(student_id, subject_id)
                    st.success("Successfully Enrolled!!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("Invalid Subject Code!!")
            
                