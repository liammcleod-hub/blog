from __future__ import annotations

import json
from pathlib import Path

from scripts.external_sources import ExternalSourceAdapter, LookupRequest
from scripts.job_state import JobState


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def discover_from_bundle(job_dir: Path) -> JobState:
    job_dir = job_dir.resolve()
    job_json = job_dir / "job.json"
    brief_path = job_dir / "brief.md"
    dossier_path = job_dir / "research-dossier.json"
    products_path = job_dir / "selected-products.json"
    article_path = job_dir / "article-revised.html"
    if not article_path.exists():
        article_path = job_dir / "article.html"

    state = JobState(job_dir=str(job_dir))

    if job_json.exists():
        job_data = _read_json(job_json)
        state.job_slug = job_data.get("job_slug")
        state.topic = job_data.get("topic")
        state.locale = job_data.get("locale")
        state.format = job_data.get("format")
        state.archetype = job_data.get("archetype")
        state.artifact_provenance["job.json"] = "local"

    if brief_path.exists():
        state.brief = _read_text(brief_path)
        state.artifact_provenance["brief.md"] = "local"

    if dossier_path.exists():
        state.dossier = _read_json(dossier_path)
        state.artifact_provenance["research-dossier.json"] = "local"

    if products_path.exists():
        state.selected_products = _read_json(products_path)
        state.artifact_provenance["selected-products.json"] = "local"

    if article_path.exists():
        state.article_html = _read_text(article_path)
        state.artifact_provenance[article_path.name] = "local"

    return state


def discover_from_article(article_path: Path) -> JobState:
    article_path = article_path.resolve()
    state = JobState(
        article_html=_read_text(article_path),
        job_dir=str(article_path.parent),
    )
    state.artifact_provenance[article_path.name] = "local"
    return state


def discover_job(seed_target: dict[str, str], adapter: ExternalSourceAdapter | None = None) -> JobState:
    target_type = seed_target["type"]
    target_value = seed_target["value"]

    if target_type.startswith("external_"):
        adapter = adapter or ExternalSourceAdapter()
        result = adapter.lookup(LookupRequest(kind=target_type, value=target_value))
        if result.status != "found":
            raise FileNotFoundError(f"External target not found: {target_type}:{target_value}")
        state = JobState(
            primary_keyword=result.artifacts.get("primary_keyword"),
            topic=result.artifacts.get("topic"),
            locale=result.artifacts.get("locale"),
            format=result.artifacts.get("format"),
            archetype=result.artifacts.get("archetype"),
            job_slug=result.artifacts.get("job_slug"),
            dossier=result.artifacts.get("dossier"),
            brief=result.artifacts.get("brief"),
            selected_products=result.artifacts.get("selected_products", []),
            article_html=result.artifacts.get("article_html"),
        )
        provenance = result.provenance
        if isinstance(provenance, str):
            state.artifact_provenance["external_lookup"] = provenance
        else:
            state.artifact_provenance.update(provenance)
        state.confidence_flags["external_lookup"] = result.status
        return state

    path = Path(target_value)
    if not path.exists():
        raise FileNotFoundError(f"Target not found: {target_value}")
    if path.is_file() and path.suffix.lower() == ".html":
        return discover_from_article(path)
    if path.is_dir():
        return discover_from_bundle(path)
    raise FileNotFoundError(f"Unsupported target: {target_value}")
