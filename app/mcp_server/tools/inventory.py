from mcp.server import MCPServer


def register(mcp: MCPServer) -> None:
    """Inventory tools stay unregistered until the restaurant schema is connected."""
    del mcp
