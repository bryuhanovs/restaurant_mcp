import secrets

from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class BearerAuthMiddleware:
    """Require Authorization: Bearer on the MCP endpoint. /health stays open."""

    def __init__(self, app: ASGIApp, token: str) -> None:
        self.app = app
        self._token = token

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http" or not _protects(scope.get("path", "")):
            await self.app(scope, receive, send)
            return
        header = _header(scope, b"authorization")
        if header is None or not _bearer_matches(header, self._token):
            response = JSONResponse({"error": "unauthorized"}, status_code=401)
            await response(scope, receive, send)
            return
        await self.app(scope, receive, send)


def _protects(path: str) -> bool:
    return path == "/mcp" or path.startswith("/mcp/")


def _header(scope: Scope, name: bytes) -> str | None:
    headers: list[tuple[bytes, bytes]] = scope.get("headers", [])
    for key, value in headers:
        if key.lower() == name:
            return value.decode("latin-1")
    return None


def _bearer_matches(header: str, token: str) -> bool:
    scheme, _, presented = header.partition(" ")
    if scheme.lower() != "bearer" or not presented:
        return False
    return secrets.compare_digest(presented, token)
