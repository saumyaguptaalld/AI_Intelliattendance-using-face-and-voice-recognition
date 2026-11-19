import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
import numpy as np
import pandas as pd
from datetime import datetime
from src.components.dialogue_attendance_result import show_voice_attendance

@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write("Record audio of students saying 'Iam Present', for AI based attendance analysis!")
    audio_data = None
    audio_data = st.audio_input("Record students voice",key="voice_attendance_audio")
    if audio_data is not None:
        st.audio(audio_data)
        st.success("Audio recorded sucessfully!!")
        if st.button("Analyze audio",use_container_width=True,type="primary"):
            with st.spinner("Analysing voice and Identifying Student..."):
                response = supabase.table("subject_students").select('*,students(*)').eq("subject_id",selected_subject_id).execute()
                enrolled_students = response.data
                if not enrolled_students:
                    st.warning("No students enrolled in the course")
                    return
                candidates_dict={s['students']['student_id']:s['students']['voice_embedding'] 
                                     for s in enrolled_students if s['students'].get('voice_embedding')}
                if not candidates_dict:
                    st.error("No enrolled students have their voice registered")
                    return
                #obtain the enrolled students voice
                audio_bytes = audio_data.read()
                detected_score = process_bulk_audio(audio_bytes,candidates_dict)
    
                results, logged_attendance = [],[]   # results is it to show user on website and logged_attendance is created to conert it to pandas later 
                # get the current timestamp for attendance
                current_timestamp = datetime.now().isoformat()
                # Match detected students with enrolled students
                for stu in enrolled_students:
                    student = stu["students"]
                    # student detected is from which voice, is stored in sources
                    score= detected_score.get(student['student_id'],0.0)
                    is_present = bool(score>0)
                    results.append({
                        "Name":student['full_name'],
                        "ID":student['student_id'],
                        "Score":score if is_present else "-",
                        "Status":"✅Present" if is_present else "❌Absent"
                    })
                    logged_attendance.append({
                        "student_id":student['student_id'],
                        "subject_id":selected_subject_id,
                        "timestamp":current_timestamp,
                        "is_present":bool(is_present)
                    })
                # saving results in session_state
                st.session_state.voice_attendance_results = (pd.DataFrame(results),logged_attendance)
                if st.session_state.voice_attendance_results is not None:
                    st.divider()
                    df_results, logs = st.session_state.voice_attendance_results
                    show_voice_attendance(df_results, logs)     