from app.config import Settings
from app.hermes_runtime import HermesAgent
from app.schemas.storyboard import Storyboard
from app.tools.openmontage_tool import OpenMontageTool


def build_agent(settings: Settings, demo: bool) -> HermesAgent:
    tool = OpenMontageTool(settings, demo)
    return HermesAgent("video_agent", "app/prompts/video_director.md", tool.render)

