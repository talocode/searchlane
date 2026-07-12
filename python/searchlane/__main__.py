"""CLI entrypoint: `searchlane` / `python -m searchlane`."""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .client import SearchLaneClient, SearchLaneError


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="searchlane",
        description="Agent web search & research API (Talocode SearchLane)",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--base-url",
        default=None,
        help="API base URL (default: TALOCODE_BASE_URL or https://api.talocode.site)",
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="API key (default: TALOCODE_API_KEY)",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("health", help="Check API health")
    sub.add_parser("pricing", help="Show pricing")
    sub.add_parser("capabilities", help="List capabilities")

    query_p = sub.add_parser("query", help="Web search (5 credits)")
    query_p.add_argument("--query", "-q", required=True, help="Search query")
    query_p.add_argument("--limit", "-n", type=int, default=None)

    news_p = sub.add_parser("news", help="News search (8 credits)")
    news_p.add_argument("--query", "-q", required=True, help="News query")
    news_p.add_argument("--limit", "-n", type=int, default=None)

    research_p = sub.add_parser("research", help="Multi-source research (30 credits)")
    research_p.add_argument("--query", "-q", required=True, help="Research question")
    research_p.add_argument("--limit", "-n", type=int, default=None)
    research_p.add_argument(
        "--fetch-pages",
        action="store_true",
        help="Fetch page content when supported",
    )

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = SearchLaneClient(api_key=args.api_key, base_url=args.base_url)

    try:
        if args.command == "health":
            result = client.health()
        elif args.command == "pricing":
            result = client.pricing()
        elif args.command == "capabilities":
            result = client.capabilities()
        elif args.command == "query":
            result = client.query(query=args.query, limit=args.limit)
        elif args.command == "news":
            result = client.news(query=args.query, limit=args.limit)
        elif args.command == "research":
            result = client.research(
                query=args.query,
                limit=args.limit,
                fetch_pages=True if args.fetch_pages else None,
            )
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            sys.exit(1)
        print(json.dumps(result, indent=2))
    except SearchLaneError as e:
        extra = []
        if e.status is not None:
            extra.append(f"status={e.status}")
        if e.code:
            extra.append(f"code={e.code}")
        suffix = f" ({', '.join(extra)})" if extra else ""
        print(f"Error: {e}{suffix}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
