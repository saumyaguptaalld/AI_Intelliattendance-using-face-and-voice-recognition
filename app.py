import streamlit as st

from src.components.header import header_home
from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from src.components.dialogue_quick_auto_enroll import quick_auto_enroll_dialog

st.set_page_config(
    page_title="InteliAIattendance",
    page_icon="🙋🏻‍♀️",
    layout="centered"
)


def main():

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = "home_screen"

    match st.session_state["login_type"]:

        case "teacher":
            teacher_screen()

        case "student":
            student_screen()

        case "home_screen":
            home_screen()

    # connecting the share url link to for student access
    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != "student":
           st.session_state.login_type = "student"
           st.rerun()
        if st.session_state.get('is_logged_in')== True and st.session_state.get('user_role')== "student":
             quick_auto_enroll_dialog(join_code)
        

main()