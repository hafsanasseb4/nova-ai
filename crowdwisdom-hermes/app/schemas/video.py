from pydantic import BaseModel


class VideoJob(BaseModel):
    job_id: str
    status: str
    video_url: str | None = None
    local_path: str | None = None
    provider: str = "demo"
    message: str = ""

