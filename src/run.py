import streamlit as st
from pathlib import Path
import re  # needed to strip the stats block
from generate_readme import generate_readme  # no LOGO_MAP import

# ---------------------------
# Helpers for "chips" inputs
# ---------------------------
def _norm(s: str) -> str:
    return (s or "").strip()

def _contains_case_insensitive(lst, item) -> bool:
    return _norm(item).lower() in {x.lower() for x in lst}

def _add_to_list(state_key: str, value: str):
    value = _norm(value)
    if not value:
        return
    lst = st.session_state[state_key]
    if not _contains_case_insensitive(lst, value):
        lst.append(value)

def _remove_from_list(state_key: str, index: int):
    st.session_state[state_key].pop(index)

def _render_chips(state_key: str, label: str):
    """Render compact, clickable chips that remove on click."""
    items = st.session_state[state_key]
    if not items:
        st.caption(f"No {label.lower()} added yet.")
        return

    # More, narrower columns so chips wrap nicely in a compact grid
    chip_cols = st.columns(6, gap="small")
    for i, item in enumerate(items):
        col = chip_cols[i % len(chip_cols)]
        with col:
            # Single button acts as the chip. Clicking removes the item.
            clicked = st.button(
                item,
                key=f"{state_key}_chip_{i}",
                help=f"Remove '{item}'",       # this sets title="Remove '...'"
                use_container_width=False,     # keep chips compact
            )
            if clicked:
                _remove_from_list(state_key, i)
                st.rerun()

# ---------------------------
# Layout: Left (CTA) | Center (App) | Right (Tutorial)
# ---------------------------
st.set_page_config(page_title="GitHub Profile Generator", page_icon="🐙", layout="wide")

left_col, center_col, right_col = st.columns([1, 2, 1], gap="large")

# ---------------------------
# LEFT: Contribute / Contact
# ---------------------------
with left_col:
    with st.container(border=True):
        st.subheader("🤝 Contribute")
        st.markdown(
            """
**Love this tool? Help make it better!**

- ⭐ Star the [repo](https://github.com/mkazemie/github-profile-generator)
- 🐛 [Open an Issue](https://github.com/mkazemie/github-profile-generator/issues)  
- 🔧 [Create a Pull Request](https://github.com/mkazemie/github-profile-generator/pulls)  
- 🎨 Add new themes: contribute a `*.txt` template to `src/themes/`

**Repo:** [github.com/mkazemie/github-profile-generator](https://github.com/mkazemie/github-profile-generator)

**Contact:** [mkazemiesfahani@gmail.com](mailto:mkazemiesfahani@gmail.com)
            """
        )

# ---------------------------
# CENTER: The App (your existing UI)
# ---------------------------
with center_col:
    # --- Add logo ---
    logo_path = Path("images/logo.png")  # adjust filename if needed
    if logo_path.exists():
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            # Centered + responsive
            st.image(str(logo_path), use_container_width=True)
    else:
        st.warning("Logo image not found in `images/` folder. Please add `logo.png` there.")

    st.title("GitHub Profile Generator")
    st.caption("Create a polished GitHub profile README from a theme.")

    # --- Theme discovery ---
    themes_dir = Path("src/themes")
    themes_dir.mkdir(parents=True, exist_ok=True)
    themes = sorted([p.stem for p in themes_dir.glob("*.txt")])
    if not themes:
        st.warning("No themes found in `src/themes`. Add at least one `.txt` template.")
    theme = st.radio("Select theme", themes, horizontal=True) if themes else None

    # Init session state lists/inputs
    if "skills" not in st.session_state:
        st.session_state.skills = []
    if "tech_stack" not in st.session_state:
        st.session_state.tech_stack = []
    if "skill_input" not in st.session_state:
        st.session_state.skill_input = ""
    if "tech_input" not in st.session_state:
        st.session_state.tech_input = ""

    # Predeclare variables so we don't hit NameError on other themes
    name = title = email = motto = summary = ""
    linkedin = github = instagram = website = youtube = facebook = ""
    github_username = ""  # optional; derive from URL if blank
    tech_stack_use_logos = True

    # --- Inputs ---
    if theme == "default":
        st.subheader("Enter required information:")
        with st.expander("Your personal information", expanded=False):
            st.write("Personal Information:")
            col1, col2 = st.columns(2)
            name = col1.text_input("Full name:")
            email = col2.text_input("Email address:")

            st.write("Links & Social:")
            col1, col2 = st.columns(2)
            linkedin = col1.text_input("LinkedIn profile URL:")
            github = col2.text_input("GitHub URL (https://github.com/<username>):")
            instagram = col1.text_input("Instagram URL (optional):")
            facebook = col2.text_input("Facebook URL (optional):")
            youtube = col1.text_input("YouTube URL (optional):")
            website = col2.text_input("Personal website URL (optional):")

            st.write("Summary of who you are:")
            col1, col2 = st.columns(2)
            title = col1.text_input("Title (e.g., Robotics Engineer | Vision Specialist):")
            motto = col2.text_input("Motto / tag line (optional):")
            summary = st.text_area("Short summary / bio:", height=140)

        # ------------------------
        # Skills (single input; Enter or Add)
        # ------------------------
        with st.expander("Top Skills", expanded=False):
            st.caption("Type a skill and press **Enter** or click **Add**. They’ll appear as chips below.")
            col_in, col_btn = st.columns([4, 1])

            def _on_add_skill():
                _add_to_list("skills", st.session_state.skill_input)
                st.session_state.skill_input = ""

            col_in.text_input("Add a skill", key="skill_input", placeholder="e.g., Machine Vision", on_change=_on_add_skill)
            col_btn.button("Add", key="add_skill_btn", on_click=_on_add_skill, use_container_width=True)
            _render_chips("skills", "Skills")

        # ------------------------
        # Tech Stack (single input; Enter or Add)
        # ------------------------
        with st.expander("Tech Stack", expanded=False):
            st.caption("Type a technology and press **Enter** or click **Add**. Unknown items are added as-is.")
            col_in2, col_btn2 = st.columns([4, 1])

            def _on_add_tech():
                _add_to_list("tech_stack", st.session_state.tech_input)
                st.session_state.tech_input = ""

            col_in2.text_input(
                "Add tech",
                key="tech_input",
                placeholder="e.g., Python, Docker, ROS 2, OpenGL ...",
                on_change=_on_add_tech
            )
            col_btn2.button("Add", key="add_tech_btn", on_click=_on_add_tech, use_container_width=True)

            tech_stack_use_logos = st.checkbox("Try to include logos when recognized", value=True)
            _render_chips("tech_stack", "Tech")

    st.divider()

    # ------------------------
    # Options beside the Generate button
    # ------------------------
    colA, colB, colC = st.columns([1, 1, 2])
    show_raw = colA.checkbox("Show raw README.md", value=True)
    include_stats = colB.checkbox("Include GitHub stats", value=True,
                                  help="Adds the Top Languages & Streak image widgets.")
    generate_clicked = colC.button("Generate Profile", type="primary", use_container_width=True)

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
        "github_username": github_username,
        "skills": st.session_state.skills,
        "tech_stack": st.session_state.tech_stack,
        "tech_stack_use_logos": tech_stack_use_logos,
    }

    if generate_clicked:
        if not theme:
            st.error("No theme selected. Please add a theme file to `src/themes`.")
        else:
            try:
                output = generate_readme(theme, user_data)

                # Strip the GitHub stats block if disabled
                if not include_stats:
                    output = re.sub(
                        r"<div>.*?github-readme-stats.*?github-readme-streak-stats.*?</div>",
                        "",
                        output,
                        flags=re.DOTALL | re.IGNORECASE,
                    )

                st.success("Profile generated!")
                with st.container(border=True):
                    st.markdown("#### Preview")
                    st.markdown(output, unsafe_allow_html=True)

                if show_raw:
                    st.markdown("#### Raw README.md")
                    st.code(output, language="markdown")

                with st.container(border=True):
                    st.subheader("Ready?")
                    st.download_button(
                        label="⬇️ Download README.md",
                        data=output.encode("utf-8"),
                        file_name="README.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )

            except FileNotFoundError as e:
                st.error(str(e))
            except Exception as e:
                st.exception(e)

# ---------------------------
# RIGHT: Tutorial
# ---------------------------
with right_col:
    with st.container(border=True):
        st.subheader("📘 How to use this")
        st.markdown(
            """
**Make your GitHub profile look professional in minutes:**

1. **Generate**  
   Fill the form and click **Generate Profile**, then **Download README.md**.

2. **Create a special repo**
   On GitHub, create a **public** repo **named exactly your username**.
   Example: if your username is `octocat`, name the repo **`octocat`**.
   GitHub treats this as your *profile repository*.

3. **Add the README**
   - Upload the downloaded `README.md` to the **root** of that repo.
   - Commit the file.

4. **Check your profile**
   Visit `https://github.com/<your-username>`
   You should now see your README rendered on your profile page.

5. **Fine-tune (optional)**
   - Update links (LinkedIn, website, email).
   - Tweak badges, skills, and tech stack.

6. **Keep it fresh**
   Edit your `README.md` anytime (directly on GitHub or regenerate here).  
   Commit changes to refresh your profile instantly.

- Want multiple styles? Contribute to this [repo](https://github.com/mkazemie/github-profile-generator) to create more templates!
            """
        )
