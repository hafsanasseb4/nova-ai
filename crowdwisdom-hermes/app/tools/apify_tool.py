from __future__ import annotations

from typing import Any

from app.config import Settings
from app.schemas.ads import Ad, AdCollection


class ApifyError(RuntimeError):
    """Raised when Apify is requested but unavailable or unsuccessful."""


class ApifyTool:
    def __init__(self, settings: Settings, demo: bool = False) -> None:
        self.settings = settings
        self.demo = demo

    def collect_ads(self, query: str, brands: list[str]) -> AdCollection:
        if self.demo or not self.settings.apify_api_token:
            return AdCollection(query=query, source="demo", ads=[
                Ad(ad_id="demo-001", brand=brands[0] if brands else "Demo brand", platform="instagram", headline="Trade smarter with a clear plan", body="See what changed in the market this week and act with confidence.", call_to_action="Learn more"),
                Ad(ad_id="demo-002", brand=brands[1] if len(brands) > 1 else "Demo competitor", platform="facebook", headline="The signal investors are watching", body="A simple briefing for people who want the context behind the headlines.", call_to_action="Sign up"),
            ])
        try:
            from apify_client import ApifyClient
        except ImportError as exc:
            raise ApifyError("Install apify-client or run with --demo.") from exc
        client = ApifyClient(self.settings.apify_api_token)
        run_input: dict[str, Any] = {"searches": brands or [query], "resultsLimit": 20}
        run = client.actor(self.settings.apify_actor_id).call(run_input=run_input)
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        ads = [Ad(ad_id=str(item.get("id", index)), brand=str(item.get("ownerUsername", query)), platform="apify", headline=str(item.get("caption", ""))[:120], body=str(item.get("caption", "")), media_url=item.get("displayUrl"), source="apify") for index, item in enumerate(items)]
        return AdCollection(query=query, source="apify", ads=ads)

