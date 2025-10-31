# generate_readme.py
from pathlib import Path
import re
from urllib.parse import urlparse, quote

TEMPLATES_DIR = Path("src/themes")

_PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")

# Known logo names for shields.io (only add logo when confident)
LOGO_MAP = {
    # --- Programming Languages ---
    "python": "Python",
    "c": "C",
    "c++": "C%2B%2B",
    "cpp": "C%2B%2B",
    "c#": "C%23",
    "java": "Java",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "go": "Go",
    "rust": "Rust",
    "ruby": "Ruby",
    "php": "PHP",
    "swift": "Swift",
    "kotlin": "Kotlin",
    "r": "R",
    "matlab": "Mathworks",
    "simulink": "Mathworks",
    "fortran": "Fortran",
    "vhdl": "VHDL",
    "verilog": "Verilog",
    "bash": "GNU-Bash",
    "shell": "GNU-Bash",
    "powershell": "PowerShell",

    # --- Robotics & Embedded ---
    "ros": "ROS",
    "ros2": "ROS",
    "arduino": "Arduino",
    "raspberry pi": "Raspberry-Pi",
    "nvidia jetson": "NVIDIA",
    "jetson": "NVIDIA",
    "stm32": "STMicroelectronics",
    "esp32": "Espressif",
    "canopen": "CANopen",
    "ethercat": "EtherCAT",
    "labview": "LabVIEW",
    "ni": "National-Instruments",
    "vrep": "CoppeliaSim",
    "coppeliasim": "CoppeliaSim",
    "gazebo": "Gazebo",
    "moveit": "MoveIt",
    "robodk": "RoboDK",

    # --- AI / ML / Data Science ---
    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",
    "keras": "Keras",
    "scikit learn": "Scikit-Learn",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "matplotlib": "Matplotlib",
    "seaborn": "Seaborn",
    "opencv": "OpenCV",
    "mlflow": "MLflow",
    "huggingface": "Hugging-Face",
    "openai": "OpenAI",
    "langchain": "LangChain",
    "jupyter": "Jupyter",
    "anaconda": "Anaconda",
    "colab": "Google-Colab",
    "cuda": "NVIDIA",
    "nvidia": "NVIDIA",
    "skimage": "Scikit-Image",

    # --- Web / Frameworks ---
    "flask": "Flask",
    "django": "Django",
    "fastapi": "FastAPI",
    "streamlit": "Streamlit",
    "dash": "Plotly",
    "vue": "Vue.js",
    "react": "React",
    "nextjs": "Next.js",
    "nodejs": "Node.js",
    "express": "Express",
    "bootstrap": "Bootstrap",
    "jquery": "jQuery",
    "html": "HTML5",
    "css": "CSS3",
    "sass": "Sass",
    "tailwind": "Tailwind-CSS",

    # --- Databases / Storage ---
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "sqlite": "SQLite",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "elasticsearch": "Elasticsearch",
    "influxdb": "InfluxDB",
    "dynamodb": "Amazon-DynamoDB",
    "firebase": "Firebase",
    "supabase": "Supabase",

    # --- DevOps / Cloud ---
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "helm": "Helm",
    "terraform": "Terraform",
    "ansible": "Ansible",
    "jenkins": "Jenkins",
    "github actions": "GitHub-Actions",
    "gitlab ci": "GitLab",
    "circleci": "CircleCI",
    "azure": "Microsoft-Azure",
    "aws": "Amazon-AWS",
    "amazon web services": "Amazon-AWS",
    "gcp": "Google-Cloud",
    "google cloud": "Google-Cloud",
    "heroku": "Heroku",
    "vercel": "Vercel",
    "netlify": "Netlify",
    "digitalocean": "DigitalOcean",
    "nginx": "NGINX",
    "apache": "Apache",
    "rabbitmq": "RabbitMQ",
    "kafka": "Apache-Kafka",
    "prometheus": "Prometheus",
    "grafana": "Grafana",
    "vagrant": "Vagrant",
    "vault": "HashiCorp",
    "packer": "HashiCorp",

    # --- Tools / Utilities ---
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "bitbucket": "Bitbucket",
    "vscode": "Visual-Studio-Code",
    "visual studio code": "Visual-Studio-Code",
    "pycharm": "PyCharm",
    "intellij": "IntelliJ-IDEA",
    "sublime": "Sublime-Text",
    "notepad++": "Notepad%2B%2B",
    "linux": "Linux",
    "ubuntu": "Ubuntu",
    "debian": "Debian",
    "arch": "Arch-Linux",
    "fedora": "Fedora",
    "windows": "Windows",
    "macos": "macOS",
    "ssh": "OpenSSH",
    "tmux": "tmux",
    "zsh": "Zsh",
    "bashrc": "GNU-Bash",
    "conda": "Anaconda",
    "poetry": "Poetry",
    "pip": "Pypi",
    "make": "GNU-Make",
    "cmake": "CMake",
    "bazel": "Bazel",
    "qemu": "QEMU",
    "virtualbox": "VirtualBox",
    "docker compose": "Docker",
    "podman": "Podman",

    # --- Design / Documentation ---
    "latex": "LaTeX",
    "markdown": "Markdown",
    "figma": "Figma",
    "canva": "Canva",
    "photoshop": "Adobe-Photoshop",
    "illustrator": "Adobe-Illustrator",
    "blender": "Blender",
    "solidworks": "SolidWorks",
    "autocad": "AutoCAD",
    "fusion 360": "Autodesk",
    "onshape": "Onshape",

    # --- Cloud/AI integrations ---
    "openai api": "OpenAI",
    "anthropic": "Anthropic",
    "replicate": "Replicate",
    "hugging face": "Hugging-Face",
    "comfyui": "ComfyUI",
    "stability ai": "Stability-AI",

    # --- Misc / Other ---
    "qt": "Qt",
    "opengl": "OpenGL",
    "unity": "Unity",
    "unreal": "Unreal-Engine",
    "gazebo": "Gazebo",
    "openvino": "OpenVINO",
    "llvm": "LLVM",
}

def _or_empty(s: str | None) -> str:
    return (s or "").strip()

def _github_username_from_url(url: str | None) -> str | None:
    """
    Extracts a GitHub username from a URL like:
      https://github.com/mkazemie/   -> mkazemie
      https://github.com/mkazemie     -> mkazemie
    Returns None if not parseable.
    """
    if not url:
        return None
    try:
        p = urlparse(url)
        if "github.com" not in (p.netloc or ""):
            return None
        parts = [seg for seg in (p.path or "").split("/") if seg]
        return parts[0] if parts else None
    except Exception:
        return None

def _patch_github_stats_handles(text: str, gh_user: str | None) -> str:
    """
    Many templates hardcode someone else's username/handle in the stats images.
    This tries to fix common patterns if we know the target username.
    """
    if not gh_user:
        return text

    # Replace username=<anything> in GitHub top-langs widget URLs
    text = re.sub(r"(username=)[^&\"']+", r"\1" + gh_user, text)

    # Replace user=<anything> in streak-stats URLs
    # Handles '?user=foo&' or '?user=foo"' etc.
    text = re.sub(r"([?&]user=)[^&\"']+", r"\1" + gh_user, text)

    # Also swap any obvious occurrences of a previous handle inside alt texts/links if needed
    # (safe best-effort: only if it appears in the same URL structures)
    return text

def _fill_placeholders(template_text: str, user_data: dict) -> str:
    """
    Replace {{var}} placeholders in the template with user-provided values.
    If a variable is missing/empty, replace with a single space (as requested).
    Unknown placeholders are also replaced with a space.
    """
    def repl(match):
        key = match.group(1)
        return _or_empty(user_data.get(key, " ")) or " "
    return _PLACEHOLDER_RE.sub(repl, template_text)

def _make_skills_block(skills: list[str]) -> str:
    lines = [f"- {s.strip()}" for s in skills if _or_empty(s)]
    return "\n".join(lines) if lines else "- "  # keep a single bullet if empty

def _badge_for(name: str, use_logo: bool) -> str:
    """
    Build a shields.io badge. Add logo param only when we have a confident mapping.
    """
    label = name.strip()
    if not label:
        return ""
    url_text = quote(label, safe="")
    logo_param = ""
    if use_logo:
        key = label.lower()
        if key in LOGO_MAP:
            logo_param = f"&logo={LOGO_MAP[key]}"
    return f"![{label}](https://img.shields.io/badge/-{url_text}-05122A?style=flat-square{logo_param}&color=353535)"

def _make_tech_stack_block(techs: list[str], use_logos: bool) -> str:
    badges = [_badge_for(t, use_logos) for t in techs if _or_empty(t)]
    badges = [b for b in badges if b]
    return "\n".join(badges) if badges else ""

def generate_readme(theme: str, user_data: dict) -> str:
    """
    Read <theme>.txt from src/themes, fill placeholders, and return the README.
    Supports:
      - {{skills_block}}: rendered bullet list of skills
      - {{tech_stack_block}}: rendered badges for tech stack (logos only if mapped)
      - {{github_username}}: explicit username use
    """
    theme_path = (TEMPLATES_DIR / f"{theme}.txt")
    if not theme_path.exists():
        raise FileNotFoundError(f"Theme file not found: {theme_path}")

    template = theme_path.read_text(encoding="utf-8")

    # Derive github_username if not supplied
    gh_user = _or_empty(user_data.get("github_username"))
    if not gh_user:
        gh_user = _github_username_from_url(_or_empty(user_data.get("github"))) or ""
    user_data["github_username"] = gh_user

    # Compose dynamic blocks
    skills = user_data.get("skills", []) or []
    techs  = user_data.get("tech_stack", []) or []
    use_logos = bool(user_data.get("tech_stack_use_logos", True))

    user_data["skills_block"] = _make_skills_block(skills)
    user_data["tech_stack_block"] = _make_tech_stack_block(techs, use_logos)

    # Fill placeholders
    filled = _fill_placeholders(template, user_data)

    # Final pass: patch any lingering hard-coded usernames in theme assets (safety)
    filled = _patch_github_stats_handles(filled, gh_user or None)

    return filled
