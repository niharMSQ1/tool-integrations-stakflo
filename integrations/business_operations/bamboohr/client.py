from __future__ import annotations

from dataclasses import dataclass

from .auth import get_auth_headers


@dataclass(frozen=True)
class ApiRequest:
    method: str
    url: str
    params: dict | None = None
    json: dict | None = None


class ToolClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')

    def request(self, req: ApiRequest) -> dict:
        """Execute an API request and return JSON."""
        _headers = get_auth_headers()
        raise NotImplementedError()
