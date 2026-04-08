from __future__ import annotations


class AuthError(Exception):
    pass


def get_auth_headers() -> dict[str, str]:
    """Return headers for the tool API client."""
    raise NotImplementedError()
