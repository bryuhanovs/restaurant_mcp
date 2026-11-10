from mcp.server import MCPServer


def register(mcp: MCPServer) -> None:
    """Sales tools stay unregistered until the restaurant schema is connected."""
    del mcp
