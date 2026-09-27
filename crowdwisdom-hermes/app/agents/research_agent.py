from app.config import Settings
from app.hermes_runtime import HermesAgent
from app.schemas.research import ResearchBrief
from app.tools.exa_tool import ExaTool
from app.tools.tavily_tool import TavilyTool


def build_agent(settings: Settings, demo: bool) -> HermesAgent:
    tavily = TavilyTool(settings, demo)
    exa = ExaTool(settings)

    def run(topic: str) -> ResearchBrief:
        brief = tavily.search(topic)
        if not brief.sources:
            brief.sources.extend(exa.search(topic))
        return brief

    return HermesAgent("research_agent", "app/prompts/researcher.md", run)

