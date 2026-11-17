import streamlit as st
from PIL import Image


def set_photo_tab(tab):
    # update active tab (enables better click on color change)
    st.session_state.photo_tab = tab



@st.dialog("Would you like to Capture or upload class photo?")
def upload_camera():
    # to toggle between upload and camera button
    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab='camera'
    tab1, tab2 = st.columns(2)
    with tab1:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else "secondary"
        if st.button("Upload",type=type_upload,icon=":material/upload:",on_click=set_photo_tab,args=('upload',),use_container_width=True):
            st.session_state.photo_tab = 'upload'
    with tab2:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else "secondary"
        if st.button("Camera",type=type_camera,icon=":material/camera:",on_click=set_photo_tab, args=('camera',),use_container_width=True):
           st.session_state.photo_tab = 'camera'                       # on_click allows you to pass a function as an object rather than execute it immediately, args supplies positional argument

    if st.session_state.photo_tab == 'upload':
        uploaded_photo = st.file_uploader("Upload Photo",key="upload_input_{st.session_state.duplicate_key}",type=["jpg","jpeg","png","webp"],accept_multiple_files=True)
        if uploaded_photo:
            for f in uploaded_photo:
                st.session_state.attendance_images.append(Image.open(f).copy())
                st.toast("Photo Uploaded")
            st.rerun()
             
                 
                
    if st.session_state.photo_tab =='camera':
        enable = st.checkbox("Enable Camera")
        camera_photo = st.camera_input("Take Photo",key = "camera_input",disabled=not enable)
        if camera_photo:
            st.session_state.attendance_images.append(Image.open(camera_photo).copy())
            st.toast("Photo Captured")
            st.rerun()
    
    st.divider()
    if st.button("Done", type="primary", width="stretch"):
        st.rerun() 
            
         
    

                        
                