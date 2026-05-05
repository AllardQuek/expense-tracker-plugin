from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional
import json

def resolve_data_dir() -> Path:
    override = os.getenv("EXPENSE_TRACKER_DATA_DIR")
    if override:
        return Path(override).expanduser()

    return Path.home() / ".hermes" / "plugins-data" / "expense-tracker"

DATA_DIR = resolve_data_dir()
OUTPUT_DIR = DATA_DIR / "output"
TRACKERS_FILE = DATA_DIR / "trackers.json"


def ensure_data_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not TRACKERS_FILE.exists():
        with TRACKERS_FILE.open("w", encoding="utf-8") as f:
            json.dump(
                {
                    "active_tracker": None,
                    "trackers": {},
                },
                f,
                indent=2,
                ensure_ascii=False,
            )


def load_state() -> Dict[str, Any]:
    ensure_data_dirs()

    try:
        with TRACKERS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {}

    if not isinstance(data, dict):
        data = {}

    data.setdefault("active_tracker", None)
    data.setdefault("trackers", {})

    if not isinstance(data["trackers"], dict):
        data["trackers"] = {}

    return data


def save_state(state: Dict[str, Any]) -> None:
    ensure_data_dirs()

    with TRACKERS_FILE.open("w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def _tracker_csv_path(tracker_name: str) -> Path:
    safe_name = tracker_name.strip().replace("/", "-")
    return OUTPUT_DIR / f"{safe_name}.csv"


def create_tracker_if_missing(tracker_name: str) -> Dict[str, Any]:
    tracker_name = tracker_name.strip()
    if not tracker_name:
        raise ValueError("tracker_name cannot be empty")

    state = load_state()
    trackers = state["trackers"]

    if tracker_name not in trackers:
        csv_path = _tracker_csv_path(tracker_name)

        trackers[tracker_name] = {
            "csv_path": str(csv_path),
            "default_currency": None,
            "default_city": None,
        }

        if not csv_path.exists():
            csv_path.write_text(
                "date,amount,currency,category,city,description\n",
                encoding="utf-8",
            )

        save_state(state)

    return trackers[tracker_name]


def set_active_tracker(tracker_name: str) -> Dict[str, Any]:
    tracker_name = tracker_name.strip()
    if not tracker_name:
        raise ValueError("tracker_name cannot be empty")

    state = load_state()

    if tracker_name not in state["trackers"]:
        create_tracker_if_missing(tracker_name)
        state = load_state()

    state["active_tracker"] = tracker_name
    save_state(state)

    return state["trackers"][tracker_name]


def get_active_tracker_name() -> Optional[str]:
    state = load_state()
    return state.get("active_tracker")


def get_active_tracker() -> Optional[Dict[str, Any]]:
    state = load_state()
    active_name = state.get("active_tracker")
    if not active_name:
        return None
    return state.get("trackers", {}).get(active_name)


def update_tracker_defaults(
    currency: Optional[str] = None,
    city: Optional[str] = None,
) -> Dict[str, Any]:
    state = load_state()
    active_name = state.get("active_tracker")

    if not active_name:
        raise ValueError("No active tracker set. Use /set-tracker <name> first.")

    tracker = state["trackers"].get(active_name)
    if not tracker:
        raise ValueError(f"Active tracker '{active_name}' not found.")

    if currency is not None:
        tracker["default_currency"] = currency.strip().upper() or None

    if city is not None:
        tracker["default_city"] = city.strip() or None

    save_state(state)
    return tracker
