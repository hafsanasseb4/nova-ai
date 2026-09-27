from __future__ import annotations

from datetime import datetime, timezone
from pydantic import BaseModel, Field


class Ad(BaseModel):
    ad_id: str
    brand: str
    platform: str = "unknown"
    headline: str
    body: str = ""
    call_to_action: str = "Learn more"
    media_url: str | None = None
    landing_url: str | None = None
    captured_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: str = "demo"


class AdCollection(BaseModel):
    query: str
    ads: list[Ad] = Field(default_factory=list)
    source: str = "demo"


class AdAnalysis(BaseModel):
    ad_id: str
    brand: str
    hook: str
    audience: str
    offer: str
    creative_pattern: str
    strengths: list[str]
    risks: list[str]
    score: float = Field(ge=0, le=10)

