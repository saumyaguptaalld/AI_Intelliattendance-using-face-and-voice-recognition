import streamlit as st
import base64
def header_home():
    with open("attendance.jpg", "rb") as f:
        image = base64.b64encode(f.read()).decode()
    st.markdown(f"""
       <div style = "display:flex;
                       flex-direction: column;
                       align-items: center;
                       justify-content:center; margin-bottom: 60px; margin-top: 30px;">
            <img 
                src="data:image/jpeg;base64,{image}"
                style="height:100px;"
            />
            <h2 style="text-align:center;">
                AI<br/>Intelliatendance
            </h2>
        </div>
    """, unsafe_allow_html=True
    )
    