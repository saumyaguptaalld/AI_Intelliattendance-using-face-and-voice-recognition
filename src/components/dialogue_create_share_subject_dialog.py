import streamlit as st
import io   # to handle binary data and use everything in same RAM
import segno
from st_copy import copy_button
# create a new subject dialog in streamlit
@st.dialog("Share class link")
def create_share_subject_dialog(sub_name, sub_code):
    app_domain = "ai-inteli-attendance-main.streamlit.app"
    join_url = f"{app_domain}/?join-code={sub_code}"
    st.header("Scan to Join!!")
    tab1, tab2 = st.columns([2,1],vertical_alignment="center")
    with tab1:
        st.write(f"**Subject Code:** `{sub_code}`") 
        col3, col4= st.columns([0.95,0.65],vertical_alignment="center",gap="small")
        with col3:
            st.write(join_url)
        with col4:
            copy_button(f"{join_url}",copied_label="copied!") 
        st.info("Copy link to share on Whatsapp or Email!!")
    with tab2:
        st.write("Scan code")
        # create QR code object
        qr = segno.make(join_url)
        # save QR to in-memory buffer
        buffer= io.BytesIO()
        qr.save(buffer, kind='png',scale=10, border=1)
        st.image(buffer.getvalue(),caption="Generated QR code")
