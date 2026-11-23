import streamlit as st
import numpy as np
from src.database.config import supabase
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.ui.style_base_layout import style_base_layout, style_background_dashboard
from src.database.db import create_teacher, check_teacher_exists, teacher_login, get_teacher_subjects,get_attendance_for_teacher
from src.components.dialogue_create_subject_teacher import create_subject_dialog
from src.components.dialogue_create_share_subject_dialog import create_share_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialogue_upload_camera_teacher import upload_camera
from src.pipelines.face_pipeline import predict_attendance
from datetime import datetime
import pandas as pd
from src.components.dialogue_attendance_result import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog

# Teacher screen:  initial login and register session state 
def teacher_screen():
    style_base_layout()
    style_background_dashboard()
    if 'teacher_login_type' not in st.session_state:
        st.session_state["teacher_login_type"] = "login"
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif st.session_state["teacher_login_type"]=="login":
        teacher_screen_login()
    elif st.session_state["teacher_login_type"] == "register":
        teacher_screen_register()

# teacher dashboard (when session state has teacher_data means logged in)
def teacher_dashboard():
    teacher_data = st.session_state["teacher_data"]
    btn1, btn2 = st.columns([6,4])
    with btn1:
        header_dashboard()
    with btn2:
        st.markdown(
        """<div style="padding-top: 50px;"></div>
           <style>.teacher_dashboard{whitespace: nowrap; width: max-content; max-width: none;}</style>
        """,
        unsafe_allow_html=True
        )   
        # logout button
        st.markdown(f'<h3 class="teacher_dashboard">Welcome, {teacher_data['name']}</h3>',unsafe_allow_html=True)   
        if st.button("Logout", key="Teacher_logout", type="secondary",icon=":material/home:",icon_position="right", width="stretch",shortcut="control+space"):                                                                          
           st.session_state['is_logged_in'] = False
           del st.session_state.teacher_data 
           st.rerun()
    st.space()
    #  create a variable inorder to choose: attendance, manage subject or attendance records
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"
    # create the three buttons
    tab1, tab2, tab3 = st.columns(3)
    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        if st.button("Take Attendance",type=type1, width="stretch", icon=":material/check_box:"):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()
            
    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "Manage_Subjects" else "tertiary"
        if st.button("Manage Subjects",type=type2, width="stretch", icon=":material/library_books:"):
            st.session_state.current_teacher_tab = "Manage_Subjects"
            st.rerun()
    with tab3:
            type3 = "primary" if st.session_state.current_teacher_tab == "Attendance_Records" else "tertiary"
            if st.button("Attendance Records",type=type3, width="stretch", icon=":material/database:"):
                st.session_state.current_teacher_tab = "Attendance_Records"
                st.rerun()

   # call functions for each choosen button
    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "Manage_Subjects":
        teacher_tab_Manage_Subjects()
    if st.session_state.current_teacher_tab == "Attendance_Records":
        teacher_tab_Attendance_Records()
    st.space()
    st.divider()
    footer_dashboard()

# define functions for clicked buttons

def teacher_tab_take_attendance():
    st.divider()
    st.markdown(f'<h1 class="headline_take_ai_attendance">Take AI Attendance</h1>',unsafe_allow_html=True)   
    # state for storing images
    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []
   # get teacher_id
    teacher_id = st.session_state.teacher_data["teacher_id"]
    # get teacher subjects
    subjects = get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning("No Subjects found! Please create subject")
        return 
    options = {f"{row['name']} - {row["subject_code"]}" : row['subject_id'] for row in subjects} if subjects else []
    col1, col2 = st.columns([0.75,0.25], vertical_alignment="bottom")
    with col1: 
         selected_subjects = st.selectbox("Select subjects for attendance", options = options.keys(),index=None,placeholder="Select subjects....")
    with col2:
        if st.button("Add Photos",type="primary",icon=":material/photo_prints:",width="stretch"):
            upload_camera()  # add photo dialog
    selected_subject_id = options[selected_subjects] if selected_subjects is not None else None
    
    if st.session_state.attendance_images:
        st.divider()
        st.header("Added photos")
        gallery = st.columns(4)
        for idx,img in enumerate(st.session_state.attendance_images):
            with gallery[idx % 4]:  # first photo goes to col1, 2nd goes to col2 and so on
                st.image(img,width="stretch",caption=f"Photo {idx+1}")
        
    st.divider()
    opt1, opt2, opt3 = st.columns(3)
    has_photos = bool(st.session_state.attendance_images)
    with opt1:
        if st.button("Clear All Photos",type="tertiary",width="stretch",icon=":material/delete:",disabled=not has_photos):
            st.session_state.attendance_images= []
            st.toast("Images cleared")
            st.rerun()
    with opt2:
        
        if st.button("Run Face Analysis",width="stretch",type="tertiary",icon=":material/person_search:",disabled=not has_photos):
            if selected_subject_id is None:
                st.warning("Please select a subject first")
            elif not has_photos:
                st.error("No photos found for analysis")
            else:
                with st.spinner("Running analysis..."):
                        all_detected_id = {}
                        # Analyse all uploaded images
                        for idx,img in enumerate(st.session_state.attendance_images):
                            img_np = np.array(img.convert("RGB")) # while capturing and uploading image we saved the image using (Image.open(img)) (imported Image fro pillow library)(now, for better analysis we convert the imag eto RGB)
                            # the predict_attendance function can take in both single and group photo and return detected_student, all_students, len(encodings)
                            detected,_,_ = predict_attendance(img_np)
                            if detected is not None:
                                for sid in detected.keys():
                                    student_id = int(sid)
                                    all_detected_id.setdefault(student_id,[]).append(f"Photo {idx+1}")
                        # obtain the student data of the selected subject, which students are enrolled in that particular subject
                        enrolled_resp = supabase.table('subject_students').select("*,students(*)").eq('subject_id',selected_subject_id).execute()
                        enrolled_students = enrolled_resp.data
                        if not enrolled_students:
                            st.warning(f"No students enrolled for {selected_subjects}")
                        else:
                            results, logged_attendance = [],[]   # results is it to show user on website and logged_attendance is created to conert it to pandas later 
                            # get the current timestamp for attendance
                            current_timestamp = datetime.now().isoformat()
                            # Match detected students with enrolled students
                            for stu in enrolled_students:
                                student = stu["students"]
                                # student detected is from which photo, is stored in sources
                                sources= all_detected_id.get(int(student['student_id']),[])
                                is_present = len(sources)>0
                                results.append({
                                    "Name":student['full_name'],
                                    "ID":student['student_id'],
                                    "Source":",".join(sources) if is_present else "-",
                                    "Status":"✅Present" if is_present else "❌Absent"
                                })
                                logged_attendance.append({
                                    "student_id":student['student_id'],
                                    "subject_id":selected_subject_id,
                                    "timestamp":current_timestamp,
                                    "is_present":bool(is_present)
                                })
                        attendance_result_dialog(pd.DataFrame(results),logged_attendance)
    with opt3:
        if st.button("🎤Use Voice Attendance",type="primary",width="stretch"):
           voice_attendance_dialog(selected_subject_id)
           # This function returns identified speakers
           # show the identified speakers here, with thier attendance table
               
   
def teacher_tab_Manage_Subjects():
    st.divider()
    teacher_id = st.session_state.teacher_data["teacher_id"]
    # obtain teacher_id as we create subjects for the corresponding teachers
    head1, head2 = st.columns(2)
    with head1:
        st.markdown(f'<h1 class="headline_manage_subjects">Manage<br>Subjects</h1>',unsafe_allow_html=True)   
    with head2:
        st.markdown(
            """<div style="padding-top: 50px;"></div>
            """,
            unsafe_allow_html=True
        )   
        if st.button("Create New Subject", key="Teacher_subject_creation", type="primary", width="stretch",shortcut="enter"):                                                                          
            create_subject_dialog(teacher_id)
    # List all subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats= [
            ("👥","Students",sub.get('total_students',0)),   # icon, label, value, default value
            ("📚","Classes",sub.get('total_classes',0))
            ]
            def share_btn():
                if st.button(f"Share code: {sub['name']}",key=f"share_{sub['subject_code']}",icon=":material/send:"):
                    create_share_subject_dialog(sub['name'], sub['subject_code'])
                    st.space()

            # creating subject card
            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats = stats,
                footer_callback = share_btn
            )
    else:
        st.info("No subject found!! Create new subject")

    
def teacher_tab_Attendance_Records():
    st.header("Teacher Attendance Records")
    teacher_id = st.session_state.teacher_data['teacher_id']
    records = get_attendance_for_teacher(teacher_id)
    if records is None:
        return
    # Showing data in pretty format
    data  = []
    for r in records:
        time_stamp = r.get('timestamp')
        data.append({
            "ts_group":time_stamp.split(".")[0] if time_stamp else None,
            "Time":datetime.fromisoformat(time_stamp).strftime("%Y-%m-%d %I:%M %p") if time_stamp else "N'A",
            "Subject":r['subjects']['name'],
            "Subject_code":r['subjects']['subject_code'],
            "is_present":bool(r.get('is_present',False))
        })
    df = pd.DataFrame(data)
    summary = (
        df.groupby(['ts_group','Time','Subject','Subject_code'])
                   .agg(
                       Present_count = ('is_present',sum),  # counts the number of students present
                       Total_count = ('is_present','count')) # counts the number of classes no matter if the student was absent or present , the class happened
                    .reset_index()
                )
    summary['Attendance_stats'] = (
        summary['Present_count'].astype(str) + "/" 
        + summary['Total_count'].astype(str) +"   " +'Students'
    )
    display_df = (summary.sort_values(by='ts_group',ascending=False)
                  [['Time','Subject','Subject_code','Attendance_stats']]
                  )
    st.dataframe(display_df,width="stretch",hide_index=True)
# validate inputs 
def login_teacher(username, password):
    if not username or not password:
        return False, "All Fields are required!"
    try: 
        teacher = teacher_login(username, password)
        if teacher:
            st.session_state["user_role"] = "teacher"
            st.session_state["teacher_data"] = teacher
            st.session_state["is_logged_in"] = True
            return True, "Welcome!"
        return False, "Invalid username or password"
    except Exception:
        return False, "Login failed. Please try again."


# Teacher screen login 

def teacher_screen_login():
    # main header in teacher screen
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
    st.header("Login with credentials",text_alignment="center")
    st.space()
    teacher_username = st.text_input("Enter Username",placeholder="Enter name")
    teacher_password = st.text_input("Enter Password",type="password",placeholder="Enter password")
    st.divider()
    btn3, btn4 = st.columns([2,2])
    with btn3:
        if st.button("Login", key="teacher_login_from_login", type="primary",icon=":material/login:",icon_position="left", width="stretch",shortcut="enter"):
                   # check credentials
                   success, message = login_teacher(teacher_username, teacher_password)
                   if success:
                        st.toast("Welcome Back!", icon="✋")
                        import time
                        time.sleep(1)
                        st.session_state["teacher_login_type"]="login"
                        st.rerun()
                   else:
                        st.error(message)        
    with btn4:
        if st.button("Register instead", key="teacher_registration_from_login", type="primary",icon=":material/passkey:",icon_position="left", width="stretch"):
                    st.session_state["teacher_login_type"] = "register"
                    st.rerun()
    footer_dashboard()

# Register teacher

def register_teacher(teacher_username, teacher_fullname, teacher_pass, teacher_pass_confirm):
    if not all([teacher_username.strip(),teacher_fullname.strip(),teacher_pass,teacher_pass_confirm,]):
        return False, "All Fields are required!"
    if check_teacher_exists(teacher_username.strip()):
        return False, "Username already taken"
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match"

    try:
        if check_teacher_exists(teacher_username.strip()):
            return False, "Username already taken!"
        
        create_teacher(teacher_username.strip(), teacher_pass, teacher_fullname.strip())
        return True, "Sucessfully registered! Login now"
        
    except Exception as e:
        st.exception(e)
        return False, "Registration failed. Check the error above."


def teacher_screen_register():
     # main header in teacher screen
    btn1, btn2 = st.columns([5.5,4])
    with btn1:
        header_dashboard()
    with btn2:
        st.markdown(
        """<div style="padding-top: 50px;"></div>""",
        unsafe_allow_html=True
        )   
        if st.button("Go back to Home", key="Teacher_back_home_register", type="secondary",icon=":material/home:",icon_position="right", width="stretch",shortcut="control+space"):                                                                          
           st.session_state['login_type'] = 'home_screen'
           st.rerun()
    st.header("Register your teacher profile",text_alignment="center")
    teacher_username = st.text_input("Enter Username")
    teacher_fullname = st.text_input("Enter Full Name")
    teacher_password = st.text_input("Enter Password",type="password")
    teacher_confirm_password = st.text_input("Confirm Password",type="password")
    st.divider()
    col3, col4 = st.columns([2,2])
    with col3:
        if st.button("Register Now", key="teacher_registration_from_register", type="primary",icon=":material/passkey:",icon_position="left", width="stretch"):
            success, message = register_teacher(
                                               teacher_username,
                                               teacher_fullname,
                                               teacher_password,
                                               teacher_confirm_password)
            if success:
                st.success("Registration submitted")
                import time
                time.sleep(1)
                st.session_state["teacher_login_type"]="login"
                st.rerun()
            else:
                st.error(message)

    with col4:
        if st.button("Login instead", key="teacher_login", type="primary",icon=":material/login:",icon_position="left", width="stretch"):
           st.session_state["teacher_login_type"] = "login"
           st.rerun()
    footer_dashboard()
    
        
