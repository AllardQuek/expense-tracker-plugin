from __future__ import annotations

import re
from typing import Any, Dict, Optional

from .csv_writer import normalize_decimal_string

_TAG_RE = re.compile(r"#([A-Za-z0-9_-]+)")
_COST_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?)\s*(.*)\s*$")


def parse_cost_field(text: str) -> tuple[str, str]:
    text = (text or "").strip()
    if not text:
        raise ValueError("Cost field is required")

    match = _COST_RE.match(text)
    if not match:
        raise ValueError(f"Invalid cost field: {text}")

    raw_cost, raw_currency = match.groups()
    cost = normalize_decimal_string(raw_cost)
    currency = raw_currency.strip()

    return cost, currency


def parse_tags_field(text: str) -> str:
    text = (text or "").strip()
    tags = _TAG_RE.findall(text)

    if not tags:
        raise ValueError("Invalid tags field: must contain at least one hashtag")

    leftover = _TAG_RE.sub("", text).strip()
    if leftover:
        raise ValueError(
            "Invalid tags field: only hashtags and spaces are allowed"
        )

    return ",".join(tags)


def parse_expense_command(
    raw_args: str,
    default_currency: Optional[str] = None,
    default_city: Optional[str] = None,
) -> Dict[str, str]:
    parts = [part.strip() for part in (raw_args or "").split(" - ")]
    parts = [part for part in parts if part]

    if len(parts) < 2:
        raise ValueError(
            "Usage: /expense <name> - <cost> [- <#tags...>] [- <city>] [- <cost_sgd>]"
        )

    name = parts[0]
    if not name:
        raise ValueError("Expense name is required")

    cost, parsed_currency = parse_cost_field(parts[1])
    currency = parsed_currency or (default_currency or "").strip()

    tags = ""
    city = ""
    cost_sgd = ""

    for field in parts[2:]:
        if "#" in field:
            if tags:
                raise ValueError("Tags provided more than once")
            tags = parse_tags_field(field)
            continue

        try:
            numeric_value = normalize_decimal_string(field)
            if cost_sgd:
                raise ValueError("cost_sgd provided more than once")
            cost_sgd = numeric_value
            continue
        except ValueError:
            pass

        if city:
            raise ValueError("City provided more than once")
        city = field.strip()

    if not city:
        city = (default_city or "").strip()

    return {
        "name": name.strip(),
        "tags": tags,
        "cost": cost,
        "currency": currency,
        "cost_sgd": cost_sgd,
        "city": city,
    }
