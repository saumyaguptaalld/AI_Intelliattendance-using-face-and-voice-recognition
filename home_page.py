import streamlit as st

st.set_page_config(
    page_title="Inteliatendance",
    page_icon ="🙋🏻‍♀️",
    layout="centered"
)
st.markdown("""
            <style>
              div.stButton > button{
                    background-color: blue;
                    border-radius: 30px;
                    width: 100%;
                    height: 60px;
                    font-size: 30px;
                    color: white;
                    font-weight: bold;
                }
                div.stButton > button:hover{
                    background-color: Darkblue;
                    color: black;              
                }
                img {
                    border-radius: 30px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                }
            </style>
            """, unsafe_allow_html=True)
def main():
    st.title("🙋🏻‍♀️ Inteliatendance")
   
    col1, col2 = st.columns(2, gap = "small")
    with col1:
        st.image("student.png")
        if st.button("Iam a Student", key ="student", width = "stretch"):
            print("Hi Student")
    with col2:
        
        st.image("teacher.png")
        if st.button("Iam a Teacher", key ="teacher", width = "stretch"):
                print("Hi Teacher")
    
main()

