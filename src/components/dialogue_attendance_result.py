import streamlit as st
from src.database.db import create_attendance


def show_voice_attendance(df,logged_attendance):
    st.write("Kindly, Review Attendance Before Confirming")
    st.dataframe(df, hide_index=True,width="stretch")
    opt1,opt2 = st.columns(2)
    with opt1:
        if st.button("Discard",width="stretch",type="tertiary"):
            st.session_state.attendance_images =[]
            st.session_state.voice_attendance_results = None
            st.rerun()  # rerun will simply close the popup since we havent save the data
    with opt2:
        if st.button("Confirm & Save",width="stretch",type="primary"):
            try:
                create_attendance(logged_attendance)
                st.toast("Attendance_taken")
                st.session_state.attendance_images =[]
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error("sync Failed!!")
                
@st.dialog("Attendance_logs")
def attendance_result_dialog(df, logs):  
    show_voice_attendance(df,logs)
        