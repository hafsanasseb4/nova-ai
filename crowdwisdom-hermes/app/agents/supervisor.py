from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from app.agents.ad_analyzer import build_agent as analyzer_agent
from app.agents.ads_manager import build_agent as ads_agent
from app.agents.research_agent import build_agent as research_agent
from app.agents.script_agent import build_agent as script_agent
from app.agents.video_agent import build_agent as video_agent
from app.config import Settings
from app.schemas.video import VideoJob
from app.tools.data_loader import save_json


@dataclass
class PipelineResult:
    run_id: str
    report_path: Path
    storyboard_path: Path
    video_job: VideoJob | None


class Supervisor:
    def __init__(self, settings: Settings, demo: bool = False) -> None:
        self.settings, self.demo = settings, demo
        settings.ensure_directories()

    def run(self, topic: str, competitors: list[str], render_video: bool = False) -> PipelineResult:
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        ads = ads_agent(self.settings, self.demo).run({"topic": topic, "competitors": competitors})
        save_json(ads, self.settings.data_dir / "ads" / f"{run_id}.json")
        analyses = analyzer_agent(self.settings, self.demo).run(ads)
        save_json({"analyses": [item.model_dump(mode="json") for item in analyses]}, self.settings.data_dir / "unique_data" / f"{run_id}_analyses.json")
        research = research_agent(self.settings, self.demo).run(topic)
        save_json(research, self.settings.data_dir / "research" / f"{run_id}.json")
        storyboard = script_agent(self.settings, self.demo).run({"topic": topic, "analyses": analyses, "research": research})
        storyboard_path = save_json(storyboard, self.settings.output_dir / "storyboards" / f"{run_id}.json")
        video_job = video_agent(self.settings, self.demo).run(storyboard) if render_video else None
        if video_job:
            save_json(video_job, self.settings.output_dir / "videos" / f"{run_id}.json")
        report = {"run_id": run_id, "topic": topic, "competitors": competitors, "ads": ads.model_dump(mode="json"), "analyses": [item.model_dump(mode="json") for item in analyses], "research": research.model_dump(mode="json"), "storyboard": storyboard.model_dump(mode="json"), "video_job": video_job.model_dump(mode="json") if video_job else None}
        report_path = save_json(report, self.settings.output_dir / "reports" / f"{run_id}.json")
        return PipelineResult(run_id, report_path, storyboard_path, video_job)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")

