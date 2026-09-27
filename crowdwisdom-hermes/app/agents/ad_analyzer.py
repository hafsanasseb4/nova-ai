from app.config import Settings
from app.hermes_runtime import HermesAgent
from app.schemas.ads import AdAnalysis, AdCollection


def analyze(collection: AdCollection) -> list[AdAnalysis]:
    return [AdAnalysis(ad_id=ad.ad_id, brand=ad.brand, hook=ad.headline, audience="People seeking clearer, lower-friction financial decisions", offer=ad.call_to_action, creative_pattern=f"{ad.platform} short-form: promise -> context -> CTA", strengths=["Clear promise", "Action-oriented CTA"], risks=["Financial claims require careful sourcing", "Generic language may reduce differentiation"], score=7.5) for ad in collection.ads]


def build_agent(settings: Settings, demo: bool) -> HermesAgent:
    return HermesAgent("ad_analyzer", "app/prompts/analyzer.md", analyze)

