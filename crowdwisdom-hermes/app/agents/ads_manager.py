from app.config import Settings
from app.hermes_runtime import HermesAgent
from app.schemas.ads import AdCollection
from app.tools.apify_tool import ApifyTool


def build_agent(settings: Settings, demo: bool) -> HermesAgent:
    tool = ApifyTool(settings, demo)
    return HermesAgent("ads_manager", "app/prompts/ads_manager.md", lambda request: tool.collect_ads(request["topic"], request["competitors"]))

