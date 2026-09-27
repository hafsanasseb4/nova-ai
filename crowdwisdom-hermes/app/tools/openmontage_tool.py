from __future__ import annotations

import uuid

import httpx

from app.config import Settings
from app.schemas.storyboard import Storyboard
from app.schemas.video import VideoJob


class OpenMontageTool:
    def __init__(self, settings: Settings, demo: bool = False) -> None:
        self.settings, self.demo = settings, demo

    def render(self, storyboard: Storyboard) -> VideoJob:
        job_id = str(uuid.uuid4())
        if self.demo or not self.settings.openmontage_api_key or not self.settings.openmontage_base_url:
            return VideoJob(job_id=job_id, status="storyboard_ready", provider="demo", message="No OpenMontage credentials configured; storyboard is ready for rendering.")
        response = httpx.post(f"{self.settings.openmontage_base_url.rstrip('/')}/videos", headers={"Authorization": f"Bearer {self.settings.openmontage_api_key}"}, json=storyboard.model_dump(mode="json"), timeout=60)
        response.raise_for_status()
        data = response.json()
        return VideoJob(job_id=data.get("id", job_id), status=data.get("status", "submitted"), video_url=data.get("url"), provider="openmontage", message="OpenMontage render submitted.")

