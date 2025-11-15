class MCPError(Exception):
    """Base class for all custom MCP server errors."""
    pass


class InvalidExchangeError(MCPError):
    """Raised when the exchange ID is missing or invalid."""
    pass


class InvalidSymbolError(MCPError):
    """Raised when a symbol is invalid or malformed."""
    pass


class ExchangeError(MCPError):
    """Raised when an exchange returns an error or fails."""
    pass
