import streamlit as st
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.ui.style_base_layout import style_base_layout, style_background_dashboard
from src.database.db import create_teacher, check_teacher_exists, teacher_login

# Teacher screen 
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

# teacher dashboard
def teacher_dashboard():
    teacher_data = st.session_state["teacher_data"]
    st.header(f"Welcome, {teacher_data['name']}")

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
        if st.button("Login", key="teacher_login_from_login", type="primary",icon=":material/login:",icon_position="left", width="stretch"):
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
    
        
