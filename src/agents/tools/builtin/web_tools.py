"""Web search/fetch tools using ``httpx`` (installed with the OpenAI SDK)."""

from __future__ import annotations

import os
import re

import httpx

from ...tool import function_tool


@function_tool
async def web_search(query: str, num_results: int = 5) -> str:
    """Search the web via the Brave Search API (requires ``BRAVE_SEARCH_API_KEY``)."""
    key = os.environ.get("BRAVE_SEARCH_API_KEY")
    if not key:
        return "web_search: set BRAVE_SEARCH_API_KEY to enable Brave Search."
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.search.brave.com/res/v1/web/search",
            params={"q": query, "count": num_results},
            headers={
                "X-Subscription-Token": key,
                "Accept": "application/json",
            },
            timeout=20.0,
        )
        resp.raise_for_status()
        data = resp.json()
    results = data.get("web", {}).get("results", [])
    formatted: list[str] = []
    for r in results[:num_results]:
        formatted.append(
            f"**{r.get('title', 'No title')}**\n"
            f"{r.get('url', '')}\n"
            f"{r.get('description', 'No description')}"
        )
    return "\n\n---\n\n".join(formatted) if formatted else "No results found."


@function_tool
async def web_fetch(url: str, max_chars: int = 10000) -> str:
    """Fetch a URL and return plain text (best-effort HTML stripping)."""
    async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
        resp = await client.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; MycelAgentSDK/1.0)"},
        )
    content_type = resp.headers.get("content-type", "")
    text = resp.text
    if "text/html" in content_type:
        text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_chars:
        text = text[:max_chars] + f"\n\n[Truncated at {max_chars} chars]"
    return f"URL: {url}\nStatus: {resp.status_code}\n\n{text}"
