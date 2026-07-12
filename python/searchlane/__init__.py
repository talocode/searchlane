"""SearchLane — agent web search & research API client."""

__version__ = "0.1.0"

from .client import SearchLaneClient, SearchLaneError, create_searchlane_client

__all__ = [
    "SearchLaneClient",
    "SearchLaneError",
    "create_searchlane_client",
    "__version__",
]
