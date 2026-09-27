from __future__ import annotations

import json
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def save_json(value: BaseModel | dict[str, Any] | list[Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = value.model_dump(mode="json") if isinstance(value, BaseModel) else value
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_json(path: Path, model: type[T]) -> T:
    if not path.exists():
        raise FileNotFoundError(f"JSON artifact not found: {path}")
    return model.model_validate(json.loads(path.read_text(encoding="utf-8")))

