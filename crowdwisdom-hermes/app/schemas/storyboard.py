from pydantic import BaseModel, Field


class StoryboardScene(BaseModel):
    scene_number: int
    duration_seconds: int = Field(ge=1)
    visual: str
    narration: str
    on_screen_text: str = ""
    asset_prompt: str = ""


class Storyboard(BaseModel):
    title: str
    aspect_ratio: str = "9:16"
    target_duration_seconds: int = Field(ge=1)
    scenes: list[StoryboardScene]
    voiceover_tone: str = "clear, credible, energetic"

