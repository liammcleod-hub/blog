from __future__ import annotations

from pathlib import Path


def write_revised_article(job_dir: Path, revised_html: str, mode: str) -> Path | None:
    if mode != "revise-article":
        return None
    target = job_dir / "article-revised.plugin.html"
    target.write_text(revised_html, encoding="utf-8")
    return target
