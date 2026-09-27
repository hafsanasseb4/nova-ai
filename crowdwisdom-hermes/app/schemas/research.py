from pydantic import BaseModel, Field


class ResearchSource(BaseModel):
    title: str
    url: str
    snippet: str = ""
    published_date: str | None = None


class ResearchBrief(BaseModel):
    topic: str
    key_trends: list[str] = Field(default_factory=list)
    audience_insights: list[str] = Field(default_factory=list)
    claims_to_verify: list[str] = Field(default_factory=list)
    sources: list[ResearchSource] = Field(default_factory=list)

