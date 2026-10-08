import streamlit as st

def footer_home():
    st.markdown(f"""
       <div style="margin-top: 6rem; display: flex; gap: 8px; justify-content: center; items-align: center">
          <p> Created with ♡ by सौम्या</p>
       </div>
       
       
""", unsafe_allow_html=True)


def footer_dashboard():
    st.markdown(f"""
       <div style="margin-top: 6rem; display: flex; gap: 8px; justify-content: center; items-align: center; color:green;">
          <p> Created with ♡ by सौम्या</p>
       </div>      
      """, unsafe_allow_html=True)