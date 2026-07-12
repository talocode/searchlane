"""SearchLane REST client (stdlib only)."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


class SearchLaneError(Exception):
    """Raised when the SearchLane API returns an error response."""

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        status: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status = status


class SearchLaneClient:
    """Python client for Talocode SearchLane (`/v1/searchlane/*`)."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        *,
        timeout: float = 60.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("TALOCODE_API_KEY")
        self.base_url = (
            base_url
            or os.environ.get("TALOCODE_BASE_URL")
            or "https://api.talocode.site"
        ).rstrip("/")
        self.timeout = timeout

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _request(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            url,
            data=data,
            headers=self._headers(),
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                if not raw:
                    return {}
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            code: str | None = None
            msg = str(e)
            try:
                detail = json.loads(e.read().decode("utf-8"))
                if isinstance(detail, dict):
                    err = detail.get("error")
                    if isinstance(err, dict):
                        msg = err.get("message") or msg
                        code = err.get("code")
                    elif isinstance(err, str):
                        msg = err
                    code = code or detail.get("code")
            except Exception:
                pass
            raise SearchLaneError(msg, code=code, status=e.code) from e
        except urllib.error.URLError as e:
            raise SearchLaneError(f"Request failed: {e.reason}") from e

    def health(self) -> dict[str, Any]:
        return self._request("GET", "/v1/searchlane/health")

    def pricing(self) -> dict[str, Any]:
        return self._request("GET", "/v1/searchlane/pricing")

    def capabilities(self) -> dict[str, Any]:
        return self._request("GET", "/v1/searchlane/capabilities")

    def query(
        self,
        query: str | None = None,
        *,
        q: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if query is not None:
            body["query"] = query
        if q is not None:
            body["q"] = q
        if limit is not None:
            body["limit"] = limit
        return self._request("POST", "/v1/searchlane/query", body)

    def news(
        self,
        query: str | None = None,
        *,
        q: str | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if query is not None:
            body["query"] = query
        if q is not None:
            body["q"] = q
        if limit is not None:
            body["limit"] = limit
        return self._request("POST", "/v1/searchlane/news", body)

    def research(
        self,
        query: str | None = None,
        *,
        q: str | None = None,
        limit: int | None = None,
        fetch_pages: bool | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {}
        if query is not None:
            body["query"] = query
        if q is not None:
            body["q"] = q
        if limit is not None:
            body["limit"] = limit
        if fetch_pages is not None:
            body["fetchPages"] = fetch_pages
        return self._request("POST", "/v1/searchlane/research", body)


def create_searchlane_client(
    api_key: str | None = None,
    base_url: str | None = None,
    **kwargs: Any,
) -> SearchLaneClient:
    return SearchLaneClient(api_key=api_key, base_url=base_url, **kwargs)
