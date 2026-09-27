from __future__ import annotations

import httpx

from app.config import Settings
from app.schemas.research import ResearchBrief, ResearchSource


class TavilyTool:
    def __init__(self, settings: Settings, demo: bool = False) -> None:
        self.settings, self.demo = settings, demo

    def search(self, topic: str) -> ResearchBrief:
        if self.demo or not self.settings.tavily_api_key:
            return ResearchBrief(topic=topic, key_trends=["Audiences reward specific, evidence-backed explanations.", "Short vertical video favors one clear promise and fast proof."], audience_insights=["Lead with the viewer's decision or fear, then add context.", "Trust improves when claims include a source or timeframe."], claims_to_verify=["Use current market data only after checking publication date."], sources=[ResearchSource(title="Demo research source", url="https://example.com/research", snippet="Demo-only source; replace with Tavily results in live mode.")])
        response = httpx.post("https://api.tavily.com/search", json={"api_key": self.settings.tavily_api_key, "query": topic, "search_depth": "advanced", "max_results": 5, "include_answer": False}, timeout=30)
        response.raise_for_status()
        results = response.json().get("results", [])
        sources = [ResearchSource(title=item.get("title", "Untitled"), url=item.get("url", ""), snippet=item.get("content", ""), published_date=item.get("published_date")) for item in results]
        return ResearchBrief(topic=topic, sources=sources, key_trends=[s.snippet[:180] for s in sources[:3]])

