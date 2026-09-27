"""Small compatibility seam for the optional Hermes agent framework.

The pipeline owns typed stage contracts; this module is where a concrete
Hermes runtime can be swapped in as its installed API evolves.
"""
from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")
U = TypeVar("U")


@dataclass
class HermesAgent:
    name: str
    instruction_file: str
    handler: Callable[[T], U]

    def run(self, payload: T) -> U:
        return self.handler(payload)


def hermes_available() -> bool:
    try:
        __import__("hermes_agent")
        return True
    except ImportError:
        return False

