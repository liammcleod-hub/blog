from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class JobState:
    topic: str | None = None
    locale: str | None = None
    primary_keyword: str | None = None
    format: str | None = None
    archetype: str | None = None
    family: str | None = None
    subformat: str | None = None
    awareness_level: str | None = None
    cluster_role: str | None = None
    dossier: dict[str, Any] | None = None
    brief: str | None = None
    selected_products: list[dict[str, Any]] = field(default_factory=list)
    article_html: str | None = None
    artifact_provenance: dict[str, str] = field(default_factory=dict)
    confidence_flags: dict[str, str] = field(default_factory=dict)
    mode: str | None = None
    job_slug: str | None = None
    job_dir: str | None = None


def new_job_state() -> JobState:
    return JobState()
