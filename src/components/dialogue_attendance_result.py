import streamlit as st
from src.database.db import create_attendance

@st.dialog("Attendance_logs")
def attendance_result_dialog(df,logged_attendance):
    st.write("Kindly, Review Attendance Before Confirming")
    st.dataframe(df, hide_index=True,width="stretch")
    opt1,opt2 = st.columns(2)
    with opt1:
        if st.button("Discard",width="stretch",type="tertiary"):
            st.rerun()  # rerun will simply close the popup since we havent save the data
    with opt2:
        if st.button("Confirm & Save",width="stretch",type="primary"):
            try:
                create_attendance(logged_attendance)
                st.toast("Attendance_taken")
                st.session_state.attendance_images =[]
                st.rerun()
            except Exception as e:
                st.error("sync Failed!!")

          
        