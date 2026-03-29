from __future__ import annotations

from pathlib import Path

import pytest

from scripts.external_sources import ExternalSourceAdapter, LookupResult


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "peddigrohr-anfaenger-guide"


def test_discover_from_bundle_loads_expected_artifacts():
    from scripts.discovery import discover_from_bundle

    job_state = discover_from_bundle(FIXTURE_DIR)

    assert job_state.job_slug == "peddigrohr-anfaenger-guide-de-at"
    assert job_state.topic == "peddigrohr"
    assert job_state.locale == "de-AT"
    assert job_state.dossier is not None
    assert job_state.brief is not None
    assert len(job_state.selected_products) >= 1
    assert "Korbflechten" in job_state.article_html
    assert job_state.artifact_provenance["job.json"] == "local"


def test_discover_from_article_path_sets_job_dir():
    from scripts.discovery import discover_from_article

    article_path = FIXTURE_DIR / "article.html"
    job_state = discover_from_article(article_path)

    assert "Peddigrohr" in job_state.article_html
    assert Path(job_state.job_dir) == FIXTURE_DIR.resolve()
    assert job_state.artifact_provenance["article.html"] == "local"


def test_discover_job_accepts_local_directory():
    from scripts.discovery import discover_job

    job_state = discover_job({"type": "local_path", "value": str(FIXTURE_DIR)})

    assert job_state.job_slug == "peddigrohr-anfaenger-guide-de-at"


def test_discover_job_accepts_local_article():
    from scripts.discovery import discover_job

    job_state = discover_job({"type": "local_path", "value": str(FIXTURE_DIR / "article.html")})

    assert "Korbflechten" in job_state.article_html


def test_discover_job_uses_external_adapter_boundary():
    from scripts.discovery import discover_job

    class FoundAdapter(ExternalSourceAdapter):
        def lookup(self, request):  # noqa: ANN001
            return LookupResult(
                status="found",
                artifacts={"topic": "peddigrohr", "locale": "de-AT", "job_slug": "external-job"},
                provenance="external-readonly",
                errors=[],
            )

    job_state = discover_job({"type": "external_latest_keyword", "value": "latest_keyword"}, adapter=FoundAdapter())

    assert job_state.topic == "peddigrohr"
    assert job_state.job_slug == "external-job"
    assert job_state.artifact_provenance["external_lookup"] == "external-readonly"


def test_discover_job_raises_for_missing_target():
    from scripts.discovery import discover_job

    with pytest.raises(FileNotFoundError):
        discover_job({"type": "local_path", "value": str(FIXTURE_DIR / "missing.html")})
