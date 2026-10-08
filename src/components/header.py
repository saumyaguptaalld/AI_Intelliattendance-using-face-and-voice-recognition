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
            <h1 style="text-align:center;">
                AI<br/>Intelliatendance
            </h1>
        </div>
    """, unsafe_allow_html=True
    )
def header_dashboard():
    with open("attendance.jpg", "rb") as f:
        image = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <div style = "display:flex;
            flex-direction: row;
            align-items: center;
            justify-content:flex-start; gap:10px; margin-bottom: 60px; margin-top: 30px;">
        <img 
            src="data:image/jpeg;base64,{image}"
            style="height:70px;"
        />
        <h2 style="margin:0; text-align:left;font-family: 'Black ops one','sans-serif'; font-size:10px !important;  font-weight: bold; color:darkblue; ">AI<br/>Intelliatendance</h2>
        </div>
    """, unsafe_allow_html=True
    )
    
