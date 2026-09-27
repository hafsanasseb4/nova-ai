from pathlib import Path

from app.agents.supervisor import Supervisor
from app.config import Settings
from app.schemas.storyboard import Storyboard
from app.tools.data_loader import load_json


def test_demo_pipeline_writes_intermediate_json(tmp_path: Path) -> None:
    settings = Settings(output_dir=tmp_path / "outputs", data_dir=tmp_path / "data")
    result = Supervisor(settings, demo=True).run("AI trading education", ["Example brand"], render_video=True)
    assert result.report_path.exists()
    assert result.storyboard_path.exists()
    storyboard = load_json(result.storyboard_path, Storyboard)
    assert len(storyboard.scenes) == 4
    assert result.video_job is not None
    assert result.video_job.status == "storyboard_ready"

