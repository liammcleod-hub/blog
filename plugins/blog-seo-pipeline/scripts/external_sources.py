from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


DEFAULT_TIMEOUT = 10
DEFAULT_ROUTES = {
    "external_dossier": "/content/research-dossiers/{value}",
    "external_latest_keyword": "/content/product-approvals/latest",
    "external_topic": "/content/research-dossiers?topic={value}",
}


@dataclass(frozen=True)
class LookupRequest:
    kind: str
    value: str


@dataclass
class LookupResult:
    status: str
    artifacts: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


class ExternalSourceAdapter:
    def __init__(
        self,
        base_url: str | None = None,
        api_token: str | None = None,
        routes: dict[str, str] | None = None,
        opener: Callable[..., Any] | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        self.base_url = (base_url or os.getenv("BLOG_SEO_PIPELINE_RETOOL_BASE_URL") or "").rstrip("/")
        self.api_token = api_token or os.getenv("BLOG_SEO_PIPELINE_RETOOL_API_TOKEN")
        self.routes = {**DEFAULT_ROUTES, **self._load_env_routes(), **(routes or {})}
        self.opener = opener or urlopen
        self.timeout = timeout

    def _load_env_routes(self) -> dict[str, str]:
        raw = os.getenv("BLOG_SEO_PIPELINE_RETOOL_ROUTES_JSON")
        if not raw:
            return {}
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return {}
        return {str(key): str(value) for key, value in parsed.items()}

    def lookup(self, request: LookupRequest) -> LookupResult:
        if not self.base_url:
            return LookupResult(
                status="not_configured",
                errors=["Retool base URL not configured for read-only lookup."],
            )

        route_template = self.routes.get(request.kind)
        if not route_template:
            return LookupResult(
                status="not_supported",
                errors=[f"Unsupported external lookup kind: {request.kind}"],
            )

        request_url = urljoin(f"{self.base_url}/", route_template.format(value=request.value).lstrip("/"))
        headers = {"Accept": "application/json"}
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"

        http_request = Request(request_url, headers=headers, method="GET")

        try:
            with self.opener(http_request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            status = "not_found" if exc.code == 404 else "error"
            return LookupResult(
                status=status,
                errors=[f"Retool lookup failed with HTTP {exc.code} for {request.kind}:{request.value}"],
            )
        except URLError as exc:
            return LookupResult(
                status="error",
                errors=[f"Retool lookup failed for {request.kind}:{request.value}: {exc.reason}"],
            )
        except json.JSONDecodeError:
            return LookupResult(
                status="error",
                errors=[f"Retool lookup returned invalid JSON for {request.kind}:{request.value}"],
            )

        return self._normalize_result(request, payload)

    def _normalize_result(self, request: LookupRequest, payload: dict[str, Any]) -> LookupResult:
        if request.kind == "external_dossier":
            topic = payload.get("topic") or payload.get("keyword")
            dossier = payload.get("result_json")
            if dossier is None:
                dossier = payload.get("dossier_json")
            if dossier is None:
                dossier = payload
            artifacts = {
                "dossier_id": payload.get("id") or request.value,
                "topic": topic,
                "locale": payload.get("locale"),
                "dossier": dossier,
            }
            return LookupResult(
                status="found",
                artifacts=artifacts,
                provenance={
                    "external_lookup": "external-readonly",
                    "dossier": "external-readonly",
                },
            )

        if request.kind == "external_latest_keyword":
            keyword = payload.get("keyword") or payload.get("topic")
            products = payload.get("products")
            if products is None and payload.get("product_handle"):
                products = [
                    {
                        "product_handle": payload.get("product_handle"),
                        "product_name": payload.get("product_name"),
                        "product_url": payload.get("product_url"),
                        "image_url": payload.get("image_url"),
                        "status": payload.get("status"),
                    }
                ]
            artifacts = {
                "primary_keyword": keyword,
                "topic": payload.get("topic") or keyword,
                "locale": payload.get("locale"),
                "dossier_id": payload.get("dossier_id"),
                "selected_products": products or [],
            }
            return LookupResult(
                status="found" if keyword else "not_found",
                artifacts=artifacts if keyword else {},
                provenance={
                    "external_lookup": "external-readonly",
                    "primary_keyword": "external-readonly",
                    "selected_products": "external-readonly",
                }
                if keyword
                else {},
                errors=[] if keyword else [f"No keyword payload found for {request.kind}:{request.value}"],
            )

        if request.kind == "external_topic":
            dossiers = payload.get("items") or payload.get("dossiers") or []
            chosen = dossiers[0] if dossiers else {}
            return LookupResult(
                status="found" if chosen else "not_found",
                artifacts={
                    "topic": chosen.get("topic") or request.value,
                    "locale": chosen.get("locale"),
                    "dossier_id": chosen.get("id"),
                    "dossier_summary": chosen,
                }
                if chosen
                else {},
                provenance={
                    "external_lookup": "external-readonly",
                    "dossier_summary": "external-readonly",
                }
                if chosen
                else {},
                errors=[] if chosen else [f"No dossiers found for topic {request.value}"],
            )

        return LookupResult(
            status="not_supported",
            errors=[f"Unsupported external lookup kind: {request.kind}"],
        )
