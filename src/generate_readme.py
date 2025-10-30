# generate_readme.py
from pathlib import Path
import re
from urllib.parse import urlparse

TEMPLATES_DIR = Path("src/themes")

_PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")

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

def generate_readme(theme: str, user_data: dict) -> str:
    """
    Read <theme>.txt from src/themes, fill placeholders, patch GH stats,
    and return the final README markdown/HTML string.
    """
    theme_path = (TEMPLATES_DIR / f"{theme}.txt")
    if not theme_path.exists():
        raise FileNotFoundError(f"Theme file not found: {theme_path}")

    template = theme_path.read_text(encoding="utf-8")

    # First pass: placeholder fill
    filled = _fill_placeholders(template, user_data)

    # Derive github_username automatically if not provided
    gh_user = _or_empty(user_data.get("github_username"))
    if not gh_user:
        gh_user = _github_username_from_url(_or_empty(user_data.get("github"))) or ""

    # Patch GitHub stats widgets if we have a username
    filled = _patch_github_stats_handles(filled, gh_user or None)

    return filled
