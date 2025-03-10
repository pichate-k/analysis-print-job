import streamlit as st

st.title("🎈 ระบบวิเคราะห์เอกสารสำหรับการรับงานพิมพ์")
col1, col2 = st.columns(2)
with col1:
    st.header("Column 1")
    st.write("Some text or elements")
with col2:
    st.header("Column 2")
    st.write("Some other elements")
 
# Use an expander to hide details
with st.expander("See details"):
    st.write("Here are some detailed elements")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
