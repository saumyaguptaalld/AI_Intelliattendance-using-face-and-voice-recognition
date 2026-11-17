import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
import numpy as np

@st.dialog("Voice Attendance")
def voice_attendance_dialog(selected_subjects):
    st.write("Record audio of students saying 'Iam Present', for AI based attendance analysis!")
    audio_data = st.audio_input("Record students voice",key="voice_attendance_audio")
    if audio_data is not None:
        st.audio(audio_data)
        st.success("Audio recorded sucessfully!!")
        if st.button("Analyze audio",use_container_width=True):
            with st.spinner("Analysing voice and Identifying Student..."):
                try:
                    #obtain the enrolled students voice
                    audio_bytes = audio_data.getvalue()
                    process_bulk_audio(audio_bytes,get_voice_candidates(selected_subjects))
                    st.success("Voice analysis completed")
                except Exception as e:
                    st.error(f"Voice Analysis failed:{e}")


def get_voice_candidates(subject_id):
    response = supabase.table("subject_students").select('student_id,students(voice_embedding)').eq("subject_id",subject_id).execute()
    enrolled_students = response.data
    candidates_dict={}
    for student in enrolled_students:
        student_id = student['student_id']
        student_data = student.get("students")
        if not student_data:
            continue
        embedding = student_data.get("voice_embedding")
        if embedding is not None:
            candidates_dict[student_id]=np.asarray(embedding,dtype=np.float32)
    return candidates_dict
