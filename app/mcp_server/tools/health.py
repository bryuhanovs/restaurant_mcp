from mcp.server import MCPServer
from mcp.server.mcpserver import Context

from app.db.connection import check_connection
from app.mcp_server.context import AppContext


def register(mcp: MCPServer) -> None:
    @mcp.tool()
    async def health(ctx: Context[AppContext]) -> dict[str, str]:
        """Check that PostgreSQL accepts SELECT 1."""
        await check_connection(ctx.request_context.lifespan_context.session_factory)
        return {"status": "ok", "database": "up"}
