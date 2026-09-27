from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.agents.supervisor import Supervisor
from app.config import Settings
from app.schemas.storyboard import Storyboard
from app.tools.openmontage_tool import OpenMontageTool
from app.tools.data_loader import load_json, save_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the CrowdWisdomTrading Hermes pipeline.")
    parser.add_argument("--topic", default="AI trading education")
    parser.add_argument("--competitors", default="Trade Ideas,Finimize")
    parser.add_argument("--demo", action="store_true", help="Use deterministic local data and skip external APIs.")
    parser.add_argument('--mode', choices=['demo', 'live'], help='Explicitly select demo or live mode.')
    parser.add_argument("--video", action="store_true", help="Submit the storyboard to OpenMontage when configured.")
    parser.add_argument("--storyboard", type=Path, help="Render an existing storyboard JSON instead of running the full pipeline.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    settings = Settings.from_env()
    demo = args.demo or settings.app_env.lower() == "demo"
    settings.ensure_directories()
    if args.storyboard:
        storyboard = load_json(args.storyboard, Storyboard)
        job = OpenMontageTool(settings, demo).render(storyboard)
        print(json.dumps(job.model_dump(mode="json"), indent=2))
        return 0
    competitors = [item.strip() for item in args.competitors.split(",") if item.strip()]
    result = Supervisor(settings, demo=demo).run(args.topic, competitors, render_video=args.video)
    print(json.dumps({"run_id": result.run_id, "report": str(result.report_path), "storyboard": str(result.storyboard_path), "video_job": result.video_job.model_dump(mode="json") if result.video_job else None}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

