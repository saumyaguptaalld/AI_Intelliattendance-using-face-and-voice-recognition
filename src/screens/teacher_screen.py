import streamlit as st
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.ui.style_base_layout import style_base_layout, style_background_dashboard

def teacher_screen():
    style_base_layout()
    style_background_dashboard()
    if 'teacher_login_type' not in st.session_state:
        st.session_state["teacher_login_type"] = "login"
    if st.session_state["teacher_login_type"]=="login":
        teacher_screen_login()
    elif st.session_state["teacher_login_type"] == "register":
        teacher_screen_register()

    
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
    teacher_username = st.text_input("Enter Username",placeholder="enter name")
    teacher_password = st.text_input("Enter Password",type="password",placeholder="enter password")
    st.divider()
    btn3, btn4 = st.columns([2,2])
    with btn3:
        if st.button("Register Now", key="teacher_registration_from_login", type="primary",icon=":material/passkey:",icon_position="left", width="stretch"):
            st.session_state["teacher_login_type"] == "register"
            st.rerun()
    with btn4:
        if st.button("Login instead", key="teacher_login_from_login", type="primary",icon=":material/login:",icon_position="left", width="stretch"):
           st.session_state["teacher_login_type"] == "login"
           st.rerun()
    footer_dashboard()

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
    st.header("Register your teacher profile")
    teacher_username = st.text_input("Enter Username")
    teacher_fullname = st.text_input("Enter Full Name")
    teacher_password = st.text_input("Enter Password",type="password")
    teacher_confirm_password = st.text_input("Confirm Password",type="password")
    st.divider()
    col3, col4 = st.columns([2,2])
    with col3:
        if st.button("Register Now", key="teacher_registration_from_register", type="primary",icon=":material/passkey:",icon_position="left", width="stretch"):
            st.write("Registeration submitted")
    with col4:
        if st.button("Login instead", key="teacher login", type="primary",icon=":material/login:",icon_position="left", width="stretch"):
           st.session_state["teacher_login_type"] == "login"
           st.rerun()
    footer_dashboard()
    
        
