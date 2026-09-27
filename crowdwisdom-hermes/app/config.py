"""Environment-backed configuration with safe defaults."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    app_env: str = "demo"
    llm_provider: str = "openrouter"
    llm_model: str = "openai/gpt-4o-mini"
    openrouter_api_key: str | None = None
    nvidia_api_key: str | None = None
    openai_base_url: str = "https://openrouter.ai/api/v1"
    apify_api_token: str | None = None
    apify_actor_id: str = "apify/instagram-scraper"
    tavily_api_key: str | None = None
    exa_api_key: str | None = None
    openmontage_api_key: str | None = None
    openmontage_base_url: str | None = None
    output_dir: Path = Path("outputs")
    data_dir: Path = Path("data")

    @classmethod
    def from_env(cls, env_file: str | Path = ".env") -> "Settings":
        load_dotenv(env_file)
        return cls(
            app_env=os.getenv("APP_ENV", "demo"),
            llm_provider=os.getenv("LLM_PROVIDER", "openrouter"),
            llm_model=os.getenv("LLM_MODEL", "openai/gpt-4o-mini"),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY") or None,
            nvidia_api_key=os.getenv("NVIDIA_API_KEY") or None,
            openai_base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
            apify_api_token=os.getenv("APIFY_API_TOKEN") or None,
            apify_actor_id=os.getenv("APIFY_ACTOR_ID", cls.apify_actor_id),
            tavily_api_key=os.getenv("TAVILY_API_KEY") or None,
            exa_api_key=os.getenv("EXA_API_KEY") or None,
            openmontage_api_key=os.getenv("OPENMONTAGE_API_KEY") or None,
            openmontage_base_url=os.getenv("OPENMONTAGE_BASE_URL") or None,
            output_dir=Path(os.getenv("OUTPUT_DIR", "outputs")),
            data_dir=Path(os.getenv("DATA_DIR", "data")),
        )

    def ensure_directories(self) -> None:
        for directory in (self.output_dir, self.data_dir):
            directory.mkdir(parents=True, exist_ok=True)
        for name in ("ads", "research", "scripts", "unique_data"):
            (self.data_dir / name).mkdir(parents=True, exist_ok=True)
        for name in ("videos", "storyboards", "reports"):
            (self.output_dir / name).mkdir(parents=True, exist_ok=True)

    def llm_api_key(self) -> str | None:
        return self.nvidia_api_key if self.llm_provider.lower() == "nvidia" else self.openrouter_api_key

