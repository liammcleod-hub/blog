from __future__ import annotations

import json
from urllib.error import HTTPError

import pytest

from scripts.external_sources import ExternalSourceAdapter, LookupRequest


class DummyResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):  # noqa: ANN001
        return False


def test_lookup_returns_not_configured_without_base_url():
    adapter = ExternalSourceAdapter(base_url=None)

    result = adapter.lookup(LookupRequest(kind="external_dossier", value="dos_123"))

    assert result.status == "not_configured"
    assert "base url" in result.errors[0].lower()


def test_lookup_builds_dossier_request_and_normalizes_payload():
    seen = {}

    def opener(request, timeout=0):  # noqa: ANN001
        seen["url"] = request.full_url
        seen["auth"] = request.headers.get("Authorization")
        seen["accept"] = request.headers.get("Accept")
        seen["timeout"] = timeout
        return DummyResponse(
            {
                "id": "dos_123",
                "topic": "peddigrohr",
                "locale": "de-AT",
                "result_json": {"summary": "Dossier"},
            }
        )

    adapter = ExternalSourceAdapter(
        base_url="https://retool.example.com",
        api_token="secret-token",
        opener=opener,
    )

    result = adapter.lookup(LookupRequest(kind="external_dossier", value="dos_123"))

    assert result.status == "found"
    assert result.artifacts["topic"] == "peddigrohr"
    assert result.artifacts["locale"] == "de-AT"
    assert result.artifacts["dossier"]["summary"] == "Dossier"
    assert result.provenance["dossier"] == "external-readonly"
    assert seen["url"] == "https://retool.example.com/content/research-dossiers/dos_123"
    assert seen["auth"] == "Bearer secret-token"
    assert seen["accept"] == "application/json"
    assert seen["timeout"] == 10


def test_lookup_uses_route_override_for_latest_keyword():
    def opener(request, timeout=0):  # noqa: ANN001
        return DummyResponse(
            {
                "keyword": "peddigrohr",
                "locale": "de-AT",
                "dossier_id": "dos_123",
                "products": [{"product_handle": "starter-set", "product_name": "Starter Set"}],
            }
        )

    adapter = ExternalSourceAdapter(
        base_url="https://retool.example.com",
        routes={"external_latest_keyword": "/content/keywords/latest-approved"},
        opener=opener,
    )

    result = adapter.lookup(LookupRequest(kind="external_latest_keyword", value="latest_keyword"))

    assert result.status == "found"
    assert result.artifacts["primary_keyword"] == "peddigrohr"
    assert result.artifacts["selected_products"][0]["product_handle"] == "starter-set"
    assert result.artifacts["dossier_id"] == "dos_123"


def test_lookup_normalizes_legacy_dossier_fields_to_canonical_output():
    def opener(request, timeout=0):  # noqa: ANN001
        return DummyResponse(
            {
                "id": "dos_legacy",
                "keyword": "peddigrohr",
                "dossier_json": {"summary": "Legacy payload"},
            }
        )

    adapter = ExternalSourceAdapter(
        base_url="https://retool.example.com",
        opener=opener,
    )

    result = adapter.lookup(LookupRequest(kind="external_dossier", value="dos_legacy"))

    assert result.status == "found"
    assert result.artifacts["dossier_id"] == "dos_legacy"
    assert result.artifacts["topic"] == "peddigrohr"
    assert result.artifacts["dossier"]["summary"] == "Legacy payload"


def test_lookup_normalizes_product_approval_shape():
    def opener(request, timeout=0):  # noqa: ANN001
        return DummyResponse(
            {
                "keyword": "peddigrohr",
                "products": [
                    {
                        "product_handle": "starter-set",
                        "product_name": "Starter Set",
                        "product_url": "https://example.com/products/starter-set",
                        "image_url": "https://example.com/starter-set.jpg",
                        "status": "Use Product Link",
                    }
                ],
            }
        )

    adapter = ExternalSourceAdapter(
        base_url="https://retool.example.com",
        routes={"external_latest_keyword": "/content/product-approvals/latest"},
        opener=opener,
    )

    result = adapter.lookup(LookupRequest(kind="external_latest_keyword", value="latest_keyword"))

    assert result.status == "found"
    assert result.artifacts["primary_keyword"] == "peddigrohr"
    assert result.artifacts["selected_products"][0]["product_handle"] == "starter-set"
    assert result.artifacts["selected_products"][0]["status"] == "Use Product Link"


def test_lookup_returns_not_found_on_404():
    def opener(request, timeout=0):  # noqa: ANN001
        raise HTTPError(request.full_url, 404, "Not Found", hdrs=None, fp=None)

    adapter = ExternalSourceAdapter(
        base_url="https://retool.example.com",
        opener=opener,
    )

    result = adapter.lookup(LookupRequest(kind="external_dossier", value="missing"))

    assert result.status == "not_found"
    assert "404" in result.errors[0]


def test_lookup_returns_not_supported_for_unknown_kind():
    adapter = ExternalSourceAdapter(base_url="https://retool.example.com")

    result = adapter.lookup(LookupRequest(kind="external_unknown", value="x"))

    assert result.status == "not_supported"
    assert "external_unknown" in result.errors[0]
