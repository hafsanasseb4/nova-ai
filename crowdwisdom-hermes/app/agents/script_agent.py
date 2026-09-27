from app.config import Settings
from app.hermes_runtime import HermesAgent
from app.schemas.ads import AdAnalysis
from app.schemas.research import ResearchBrief
from app.schemas.storyboard import Storyboard, StoryboardScene


def write_storyboard(topic: str, analyses: list[AdAnalysis], research: ResearchBrief) -> Storyboard:
    hook = analyses[0].hook if analyses else "The market changes quickly. Here is the context that matters."
    return Storyboard(title=f"{topic}: the signal behind the noise", target_duration_seconds=30, scenes=[
        StoryboardScene(scene_number=1, duration_seconds=5, visual="Fast-moving market headlines and clean data overlays", narration=hook, on_screen_text="What changed?", asset_prompt="Vertical editorial finance montage, credible and modern"),
        StoryboardScene(scene_number=2, duration_seconds=10, visual="Analyst highlights a single chart and compares two outcomes", narration=research.audience_insights[0] if research.audience_insights else "Start with the decision the viewer needs to make.", on_screen_text="Context before reaction", asset_prompt="Close-up of chart annotations, no logos"),
        StoryboardScene(scene_number=3, duration_seconds=10, visual="Three concise evidence cards with source labels", narration="Use current evidence, explain the trade-off, and make the next step obvious.", on_screen_text="Evidence. Clarity. Action.", asset_prompt="Three animated evidence cards, clean typography"),
        StoryboardScene(scene_number=4, duration_seconds=5, visual="Simple end card with call to action", narration="Get the next briefing and make a better-informed move.", on_screen_text="Follow for the next briefing", asset_prompt="Minimal premium finance end card"),
    ])


def build_agent(settings: Settings, demo: bool) -> HermesAgent:
    return HermesAgent("script_agent", "app/prompts/script_writer.md", lambda payload: write_storyboard(payload["topic"], payload["analyses"], payload["research"]))

