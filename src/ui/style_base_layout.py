import streamlit as st
def style_background_home():
    st.markdown("""
              <style>
                .stApp{
                  background: #d3e3fdff !important;}
                .stApp div[data-testid="stColumn"]{
                   background-color: white !important;
                   padding: 2.5rem !important;
                   border-radius: 2.5rem !important;
                   box-shadow: 5px 5px 12px rgba(0,0,0,0.2);
                }
            """,unsafe_allow_html=True)
def style_background_dashboard():
    st.markdown("""
              <style>
                .stApp{
                background: #c2e7ff !important;}
            """,unsafe_allow_html=True)

def style_base_layout():
    st.markdown("""
          <style>   
            @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Public+Sans:ital,wght@0,100..900;1,100..900&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Black+Ops+One&family=Isometra&family=Public+Sans:ital,wght@0,100..900;1,100..900&display=swap');
            
            /* Hide top bar of streamlit 

            #MainMenu, footer, header{
                visibility: hidden;
            } 
            */
            .block-container{
                padding-top: 4.0rem !important
            }

            /* Headings  */

            h1{
               font-family: 'Black Ops One','Public Sans', sans-serif !important;
               font-size: 3.0rem !important;  
               line-height: 0.9  !important;
               margin-bottom: 0rem !important;
            
            }
            h2{
               font-family: 'Black Ops One', 'Public Sans', sans-serif !important;
               font-size: 1.8rem !important;  
               line-height: 0.8  !important;
               margin-bottom: 0rem !important;
                        
            }
            h3,h4,p{
                font-family: 'Public Sans'!important; 
            }

            /* primary homepage buttons */
            button[kind="primary"]{
               background-color: darkblue !important;
               color: white !important;
               font-size: 30px !important;
               border-radius: 30px !important;
               outline: yellow !important;
               font-weight: Bold !important;
               
               transition: all 0.3s ease;
            }
            button[kind="primary"]:hover{
                transform: scale(1.08) !important;
            }
            
            div[data-testid="stImage"] {
                text-align: center !important;
            }

            /* Secondary and Tertiary buttons for all other buttons */
            button[kind="secondary"]{
                border-radius: 1.5rem !important;
                background: maroon !important;
                font-weight: bold !important;
                color: white !important;
                outline: none !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }
                      
          

            button[kind="tertiary"]{
                border-radius: 1.5rem !important;
                background: black !important;
                color: white !important;
                outline: none !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }
          </style>
    """,unsafe_allow_html=True)