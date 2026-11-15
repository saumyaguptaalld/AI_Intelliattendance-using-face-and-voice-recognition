import streamlit as st
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.ui.style_base_layout import style_base_layout, style_background_dashboard
from PIL import Image
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding

from src.database.db import get_all_students, create_student, get_student_attendance, get_student_subjects
from src.components.dialogue_create_enroll import enroll_dialog
from src.components.subject_card import subject_card
from src.components.unenroll_dialog_warning import un_enroll_dialog
import numpy as np
import time

def student_dashboard():
    st.header("Welcome to student dashboard")
    # get student info
    student_data = st.session_state["student_data"]
    student_id = student_data['student_id']
    btn1, btn2 = st.columns([6,4])
    with btn1:
        header_dashboard()
    with btn2:
        st.markdown(
        """<div style="padding-top: 50px;"></div>
           <style>.student_dashboard{whitespace: nowrap; width: max-content; max-width: none;}</style>
        """,
        unsafe_allow_html=True
        )   
        # logout button
        st.markdown(f"<h3 class='student_dashboard'>Welcome, {student_data['full_name']}</h3>",unsafe_allow_html=True)   
        if st.button("Logout", key="student_logout", type="primary",icon=":material/home:",icon_position="right", width="stretch",shortcut="control+space"):                                                                          
           st.session_state['is_logged_in'] = False
           st.session_state.pop('student_data',None) 
           st.rerun()
    st.space()
    btn3, btn4 = st.columns([6,4])
    with btn3:
        st.header("Your Enrolled Subjects")
    with btn4:
        if st.button("Enroll in Subject", key="student_enroll", type="primary",icon=":material/home:",icon_position="right", width="stretch",shortcut="enter"):
           enroll_dialog()
    st.divider()
    # Fetch student data
    with st.spinner('Loading enrolled students...'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)
    # Attendance statistics
    status_map = {}   # total classes enrolled and their attendance for the respective class
    for log in logs:  # iterate through attendance logs
        sub_id = log['subject_id']  # obtain subject id from attendance logs
        if sub_id not in status_map:  # if sub_id not in status map 
            status_map[sub_id] = {"Total":0, "Attendance":0}  # initialize with 0
        # count total classes
        status_map[sub_id]["Total"] +=1  # if sub_id exists in logs means class happened , we might have not attended , so total is increasd by 1
        if log.get("is_present"):
            status_map[sub_id]['Attendance'] +=1
    cols = st.columns(2)
    for i , sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sub_id = sub_node['subject_id']
        status = status_map.get(sub_id,{"Total":0, "Attendance":0})
        
        def unenroll_btn(subject_id = sub_id):
            if st.button("Un-enroll now!!",type="tertiary",width="stretch",key=f"unenroll_{subject_id}"):
                un_enroll_dialog(student_id,subject_id,sub["subject_code"])
        with cols[i%2]:
            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = [('🗓️','Total',status['Total']),
                         ('✅','Attendance',status['Attendance'])],
                footer_callback = unenroll_btn
                )



    footer_dashboard()

def student_screen():
    style_base_layout()
    style_background_dashboard()
    if "student_data" in st.session_state:
        student_dashboard()
        return 

    # Main header in Student screen
    btn1, btn2 = st.columns([5.5,4])
    with btn1:
        header_dashboard()
    with btn2:
        st.markdown(
        """<div style="padding-top: 50px;"></div>""",
        unsafe_allow_html=True
        )   
        if st.button("Go back to Home", key="Teacher_back_home_login", type="secondary",icon=":material/home:",icon_position="right", width="stretch",shortcut="control+space"):                                                                          
            st.session_state['login_type'] = 'home_screen'
            st.rerun()
    st.header("Login using FaceID",text_alignment="center")
    st.space()
    st.space()
    enable = st.checkbox("Enable camera")
    show_registration = False
    picture = st.camera_input("Position your face in the center", disabled=not enable)
    if picture:
        img = np.array(Image.open(picture)) 
        with st.spinner("AI is scanning 🔎"):
            detected_student, all_student_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("😅Face not found")
            elif num_faces > 1:
                 st.warning("👥 Multiple faces detected")
            else:
                if detected_student:
                   student_id = list(detected_student.keys())[0]
                   all_student_ids = get_all_students()
                   student = next((student for student in all_student_ids if student['student_id']== student_id),None)
                   if student:
                       st.session_state.is_logged_in = True
                       st.session_state.user_role ="student"
                       st.session_state.student_data = student
                       st.toast(f"Welcome back {student['full_name']}✨")
                       time.sleep(1)
                       st.rerun()
                else:
                    st.info("Face not registered! You might be a new student 🧑‍🎓!")
                    show_registration = True
    if show_registration:
        with st.container(border = True):
            st.header("🪪Register new student profile")
            new_name = st.text_input("Enter your name", placeholder=" Saumya Gupta")
            st.subheader('optional: Voice Enrollment')
            st.info("🗣️ Enroll for voice only attendance")
            audio_data = None
            try:
                audio_data = st.audio_input("Record a short phrase, Example: Iam present, my name is Saumya Gupta")
            except Exception as e:
                st.error("😞Audio data failed to record!")
            if st.button("Create Account", type="primary"):
                if new_name:
                    with st.spinner("Creating profile👤..."):
                        img = np.array(Image.open(picture))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_embedding = encodings[0].tolist()
                            voice_embedding = None
                            if audio_data:
                                voice_embedding = get_voice_embedding(audio_data.read())

                            response_data = create_student(new_name, face_embedding= face_embedding, voice_embedding = voice_embedding)
                            if response_data:
                                train_classifier()  # clears cache and add student for training
                                st.session_state.is_logged_in = True
                                st.session_state.user_role ="student"
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile created successfully ✅!!{new_name}")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error("Couldn't capture your facial features for Registration")
                else:
                    st.warning("Enter your Full Name")
    footer_dashboard()
