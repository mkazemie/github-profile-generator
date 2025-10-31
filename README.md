# GitHub Profile Generator

A simple, friendly **Streamlit** app that builds a polished `README.md` for your GitHub profile using fill-in templates. Add your name, links, skills, and tech stack; preview instantly; then download and drop it into your profile repo. ✨

**Live demo:** https://gitprofilegenerator.streamlit.app/

---

## 🚀 Features

- **Theme-based generator** using plain-text templates (`src/themes/*.txt`)
- **Smart placeholders**: `{{name}}`, `{{title}}`, `{{email}}`, etc.
- **Dynamic blocks**:
  - `{{skills_block}}` → bullet list from your inputs  
  - `{{tech_stack_block}}` → shields.io badges (with logos when confidently mapped)  
  - `{{github_username}}` → auto-parsed from your GitHub URL (or use manual)
- **Click-to-remove chips** for Skills & Tech Stack (no clutter)
- **Optional GitHub stats** (Top Languages & Streak) toggle
- **Live preview** and **one-click download**

---

## 🧩 How it works (in 30 seconds)

1. Pick a theme (`src/themes/default.txt` included).  
2. Fill your personal info, links, summary, skills, and tech stack.  
3. Toggle **Include GitHub stats** (optional).  
4. Click **Generate Profile** → preview appears.  
5. **Download README.md**.  
6. Create a public repo named **exactly** your username (e.g., `octocat`) and commit `README.md` to its root. Your profile page updates automatically.

---

## 📦 Install & Run

```bash
# 1) Clone
git clone https://github.com/mkazemie/github-profile-generator.git
cd github-profile-generator

# 2) (Recommended) Create a virtual environment
python -m venv .venv && source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Run the app
streamlit run src/run.py
```
---

## 🗂️ Project Structure
.
├─ images/
│  └─ logo.png                # optional logo shown at the top of the app
├─ src/
│  ├─ run.py                  # Streamlit UI
│  ├─ generate_readme.py      # Template filling & badge generation
│  └─ themes/
│     └─ default.txt          # Example theme (HTML/Markdown + {{placeholders}})
└─ requirements.txt

---

## 🖼️ Templates & Placeholders

Templates are plain text (Markdown/HTML) with {{placeholders}}.
Example from default.txt:

```bash
<h1 align="center">{{name}}</h1>
<h3 align="center">{{title}}</h3>

{{summary}}

**{{motto}}**

- 📫 How to reach me: {{email}}

### 🖥 Skills
{{skills_block}}

### ⚙️ Tech Stack
{{tech_stack_block}}

<div>
  <img width="45%" src="https://github-readme-stats.vercel.app/api/top-langs?username={{github_username}}&layout=compact" />
  <img width="50%" src="https://github-readme-streak-stats.herokuapp.com/?user={{github_username}}" />
</div>

```
---

## 📄 License

MIT License

---

## 🧑‍💻 Credits

Built with ❤️ using Streamlit by Mahdi Kazemi.

