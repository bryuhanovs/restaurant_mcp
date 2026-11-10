from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server import MCPServer
from mcp.server.transport_security import TransportSecuritySettings

from app.config import Settings
from app.db.connection import create_engine, create_session_factory
from app.mcp_server.context import AppContext
from app.mcp_server.tools import health


def build_server(settings: Settings) -> MCPServer:
    @asynccontextmanager
    async def lifespan(_server: MCPServer) -> AsyncIterator[AppContext]:
        engine = create_engine(settings)
        session_factory = create_session_factory(engine)
        try:
            yield AppContext(session_factory=session_factory, settings=settings)
        finally:
            await engine.dispose()

    mcp = MCPServer(
        "restaurant-mcp",
        instructions=(
            "Read-only access to restaurant data. "
            "Tools accept fixed arguments and never raw SQL."
        ),
        lifespan=lifespan,
        log_level=settings.log_level,
    )
    health.register(mcp)
    return mcp


def build_transport_security(settings: Settings) -> TransportSecuritySettings | None:
    if not settings.allowed_hosts:
        return None
    return TransportSecuritySettings(
        allowed_hosts=settings.allowed_hosts,
        allowed_origins=settings.allowed_origins,
    )
