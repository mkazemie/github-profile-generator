import streamlit as st
from pathlib import Path

# Title of the app
st.title("Github Profile Generatror")

st.subheader("Select desired theme:")
themes = list(Path("src/themes").iterdir())
themes = [theme.stem for theme in themes]

theme = st.radio("Info are requested based on the selected theme", themes)

if theme == "default":
    st.subheader("Enter required information:")
    with st.expander("Enter you information here"):
        st.write("Personal Information:")
        col1, col2 = st.columns(2)
        name = col1.text_input("Full name:")
        email = col2.text_input("Email address:")
        github_handle = col1.text_input("Github username (not URL):")

        st.write("Social Media:")
        col1, col2 = st.columns(2)
        linkedin = col1.text_input("LinkedIn profile URL:")
        github = col2.text_input("itHub profile URL:")
        instagram = col1.text_input("Instagram URL:")
        Facebook = col2.text_input("Facebook URL:")
        youtube = col1.text_input("Youtube URL:")
        website = col2.text_input("Personal website URL:")

        st.write("Summary of who you are:")
        col1, col2 = st.columns(2)
        title = col1.text_input("Title:")
        motto = col2.text_input("Enter your motto:")
        summary = st.text_area("Enter a brief summary about yourself:")


st.header("Generate Profile")
if st.button("Generate Profile"):
    st.success("Profile generated successfully!")
    st.info("This is a placeholder for the profile generation logic.")
    # Here you would add the logic to generate the profile based on the input data

