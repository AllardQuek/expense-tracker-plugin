from .state import (
    set_active_tracker,
    update_tracker_defaults,
    get_active_tracker_name,
    list_trackers,
    delete_tracker,
    get_active_tracker,
)
from .parser import parse_expense_command
from .csv_writer import append_expense_row


def set_tracker(raw_args: str) -> str:
    tracker_name = raw_args.strip()
    if not tracker_name:
        return "Usage: /set-tracker <name>"

    try:
        tracker = set_active_tracker(tracker_name)
        return (
            f"Active tracker set to: {tracker_name}\n"
            f"CSV: {tracker['csv_path']}"
        )
    except Exception as e:
        return f"Error: {e}"


def set_currency(raw_args: str) -> str:
    currency_code = raw_args.strip().upper()
    if not currency_code:
        return "Usage: /set-currency <currency_code>"

    try:
        tracker = update_tracker_defaults(currency=currency_code)
        active = get_active_tracker_name()
        return (
            f"Default currency for tracker '{active}' set to: "
            f"{tracker['default_currency']}"
        )
    except Exception as e:
        return f"Error: {e}"


def set_city(raw_args: str) -> str:
    city_name = raw_args.strip()
    if not city_name:
        return "Usage: /set-city <city_name>"

    try:
        tracker = update_tracker_defaults(city=city_name)
        active = get_active_tracker_name()
        return (
            f"Default city for tracker '{active}' set to: "
            f"{tracker['default_city']}"
        )
    except Exception as e:
        return f"Error: {e}"


def list_trackers_command(raw_args: str) -> str:
    try:
        result = list_trackers()
        trackers = result["trackers"]

        if not trackers:
            return "No trackers found."

        lines = []
        for tracker in trackers:
            marker = "*" if tracker["is_active"] else "-"
            lines.append(
                f"{marker} {tracker['name']} "
                f"(currency={tracker['default_currency']}, city={tracker['default_city']})"
            )

        return "Trackers:\n" + "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def delete_tracker_command(raw_args: str) -> str:
    tracker_name = raw_args.strip()
    if not tracker_name:
        return "Usage: /delete-tracker <name>"

    try:
        result = delete_tracker(tracker_name)
        msg = f"Deleted tracker: {result['deleted_tracker']}"
        if result["was_active"]:
            msg += "\nActive tracker cleared."
        if result["deleted_file"]:
            msg += "\nCSV file deleted."
        return msg
    except Exception as e:
        return f"Error: {e}"


def handle_expense(raw_args: str) -> str:
    raw_args = raw_args.strip()
    if not raw_args:
        return (
            "Usage: /expense <name> - <cost> [currency] - [#tags] - [city] - [cost_sgd]"
        )

    try:
        tracker = get_active_tracker()
        tracker_name = get_active_tracker_name()

        parsed = parse_expense_command(
            raw_args,
            default_currency=tracker.get("default_currency", ""),
            default_city=tracker.get("default_city", ""),
        )

        append_expense_row(tracker["csv_path"], parsed)

        parts = [
            f"Saved expense to tracker '{tracker_name}':",
            f"- name: {parsed['name']}",
            f"- cost: {parsed['cost']} {parsed['currency']}",
        ]

        if parsed.get("tags"):
            parts.append(f"- tags: {parsed['tags']}")
        if parsed.get("city"):
            parts.append(f"- city: {parsed['city']}")
        if parsed.get("cost_sgd"):
            parts.append(f"- cost_sgd: {parsed['cost_sgd']}")

        return "\n".join(parts)

    except Exception as e:
        return f"Error: {e}"

