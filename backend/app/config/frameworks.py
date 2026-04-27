import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

_CONFIG_PATH = Path(__file__).parent / "competencies.json"


class FrameworkNotFoundError(KeyError):
    pass


@lru_cache(maxsize=1)
def load_frameworks() -> Dict[str, Dict[str, object]]:
    with _CONFIG_PATH.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict) or not data:
        raise RuntimeError("competencies.json is empty or malformed")
    return data


def get_framework(key: str) -> Dict[str, object]:
    frameworks = load_frameworks()
    if key not in frameworks:
        raise FrameworkNotFoundError(key)
    return frameworks[key]


def list_competencies(key: str) -> List[str]:
    fw = get_framework(key)
    competencies = fw.get("competencies", [])
    if not isinstance(competencies, list):
        raise RuntimeError(f"framework '{key}' has malformed competencies entry")
    return [str(c) for c in competencies]
