import streamlit as st
from pathlib import Path
from generate_readme import generate_readme

# Title of the app
st.set_page_config(page_title="GitHub Profile Generator", page_icon="🐙", layout="centered")
st.title("Github Profile Generatror")
st.caption("Create a polished GitHub profile README from a theme.")

# --- Theme discovery ---
themes_dir = Path("src/themes")
themes_dir.mkdir(parents=True, exist_ok=True)  # ensure exists
themes = sorted([p.stem for p in themes_dir.glob("*.txt")])
if not themes:
    st.warning("No themes found in `src/themes`. Add at least one `.txt` template.")
theme = st.radio("Select theme", themes, horizontal=True) if themes else None

# --- Inputs ---
if theme == "default":
    st.subheader("Enter required information:")
    with st.expander("Enter you information here"):
        st.write("Personal Information:")
        col1, col2 = st.columns(2)
        name = col1.text_input("Full name:")
        email = col2.text_input("Email address:")

        st.write("Link & Social:")
        col1, col2 = st.columns(2)
        linkedin = col1.text_input("LinkedIn profile URL:")
        github = col2.text_input("GitHub URL (https://github.com/<username>):")
        instagram = col1.text_input("Instagram URL (optional):")
        facebook = col2.text_input("Facebook URL (optional):")
        youtube = col1.text_input("Youtube URL:")
        website = col2.text_input("Personal website URL (optional):")

        st.write("Summary of who you are:")
        col1, col2 = st.columns(2)
        title = col1.text_input("Title (e.g., Robotics Engineer | AI & Mechatronics Specialist):")
        motto = col2.text_input("Motto / tag line (optional):")
        summary = st.text_area("Short summary / bio:", height=140)

st.divider()

# Assemble user data for placeholder filling
user_data = {
    "name": name,
    "title": title,
    "email": email,
    "motto": motto,
    "summary": summary,
    "linkedin": linkedin,
    "github": github,
    "instagram": instagram,
    "website": website,
    "youtube": youtube,
    "Facebook": facebook,
}


st.header("Generate Profile")
colA, colB, colC = st.columns([1, 1, 2])
write_to_repo = colA.checkbox("Write to README.md", value=False, help="Writes the file into the project root.")
show_raw = colB.checkbox("Show raw markdown", value=False)
generate_clicked = colC.button("Generate Profile", type="primary")

if generate_clicked:
    if not theme:
        st.error("No theme selected. Please add a theme file to `src/themes`.")
    else:
        try:
            output = generate_readme(theme, user_data)

            st.success("Profile generated!")
            with st.container(border=True):
                st.markdown("#### Preview")
                # Render HTML inside Markdown for a better preview
                st.markdown(output, unsafe_allow_html=True)

            if show_raw:
                st.markdown("#### Raw README.md")
                st.code(output, language="markdown")

            # Download button
            st.download_button(
                label="⬇️ Download README.md",
                data=output.encode("utf-8"),
                file_name="README.md",
                mime="text/markdown",
            )

            # Optionally write to repo root
            if write_to_repo:
                Path("README.md").write_text(output, encoding="utf-8")
                st.info("`README.md` written to the project root.")

        except FileNotFoundError as e:
            st.error(str(e))
        except Exception as e:
            st.exception(e)
