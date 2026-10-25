import streamlit as st
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.ui.style_base_layout import style_base_layout, style_background_dashboard
from PIL import Image
import numpy as np
def student_screen():
    style_base_layout()
    style_background_dashboard()
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
    picture = st.camera_input("Position your face in the center", disabled=not enable)
    if picture:
          
        np.array(Image.open(picture))            
    footer_dashboard()
