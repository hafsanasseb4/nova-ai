from __future__ import annotations

import httpx

from app.config import Settings


class LLMConfigurationError(RuntimeError):
    """Raised when a live LLM call is requested without credentials."""


def complete(prompt: str, settings: Settings) -> str:
    api_key = settings.llm_api_key()
    if not api_key:
        raise LLMConfigurationError("Set OPENROUTER_API_KEY or NVIDIA_API_KEY in .env, or run with --demo.")
    base_url = "https://integrate.api.nvidia.com/v1" if settings.llm_provider.lower() == "nvidia" else settings.openai_base_url
    response = httpx.post(f"{base_url.rstrip('/')}/chat/completions", headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json={"model": settings.llm_model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.4}, timeout=60)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

