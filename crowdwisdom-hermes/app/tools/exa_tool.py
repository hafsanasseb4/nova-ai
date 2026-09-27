from __future__ import annotations

import httpx

from app.config import Settings
from app.schemas.research import ResearchSource


class ExaTool:
    """Optional fallback search provider."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def search(self, query: str) -> list[ResearchSource]:
        if not self.settings.exa_api_key:
            return []
        response = httpx.post("https://api.exa.ai/search", headers={"x-api-key": self.settings.exa_api_key, "Content-Type": "application/json"}, json={"query": query, "numResults": 5, "contents": {"highlights": {}}}, timeout=30)
        response.raise_for_status()
        return [ResearchSource(title=item.get("title", "Untitled"), url=item.get("url", ""), snippet=" ".join(item.get("highlights", []))) for item in response.json().get("results", [])]

