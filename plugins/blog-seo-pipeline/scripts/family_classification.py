from __future__ import annotations

from scripts.job_state import JobState


def classify_family(job_state: JobState) -> tuple[str, str]:
    fmt = (job_state.format or "").lower()
    archetype = (job_state.archetype or "").lower()
    brief = (job_state.brief or "").lower()

    if "compare" in fmt or "vergleich" in brief or "comparison" in archetype:
        return "product-comparison", "high"
    if "list" in fmt or "listicle" in fmt or "rank" in brief:
        return "curation-listicle", "high"
    if "deep" in fmt or "guide" in fmt or "anfaenger" in brief:
        return "deep-dive-guide", "high"
    return "deep-dive-guide", "low"
