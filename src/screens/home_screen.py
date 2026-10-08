import streamlit as st
from src.components.header import header_home
from src.ui.style_base_layout import style_base_layout, style_background_home
from src.components.footer import footer_home
def home_screen():
    style_base_layout()  # for styling of home page
    style_background_home()
    header_home()    # For header of home page
    
    col1, col2 = st.columns(2, gap = "large")
    with col1:
        st.header("Iam a Student")
        st.image("student.png",width = 145)
        if st.button("Student Portal", width = "stretch", type="primary", icon=":material/open_in_new:",icon_position = "right"):
            st.session_state['login_type']='student'
            st.rerun()
    with col2:
        st.header("Iam a Teacher")
        st.image("teacher.png",width = 145)
        if st.button("Teacher Portal", type="primary", width = "stretch", icon=":material/open_in_new:",icon_position = "right"):
            st.session_state['login_type']='teacher'
            st.rerun()
            
    footer_home()