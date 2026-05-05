"""Expense tracker plugin registration."""

def set_tracker(raw_args: str) -> str:
    tracker_name = raw_args.strip()
    if not tracker_name:
        return "Usage: /set-tracker <tracker_name>"
    return f"Tracker set to: {tracker_name}"

def set_currency(raw_args: str) -> str:
    currency_code = raw_args.strip().upper()
    if not currency_code:
        return "Usage: /set-currency <currency_code>"
    return f"Currency set to: {currency_code}"

def set_city(raw_args: str) -> str:
    city_name = raw_args.strip()
    if not city_name:
        return "Usage: /set-city <city_name>"
    return f"City set to: {city_name}"

def add_expense(raw_args: str) -> str:
    parts = raw_args.strip().split(maxsplit=1)
    if len(parts) < 2:
        return "Usage: /add-expense <amount> <category>"

    amount, category = parts
    return f"Expense added: {amount} in category {category}"

def register(ctx):
    ctx.register_command(
        "set-tracker",
        handler=set_tracker,
        description="Set the active expense tracker"
    )
    ctx.register_command(
        "set-currency",
        handler=set_currency,
        description="Set the default currency"
    )
    ctx.register_command(
        "set-city",
        handler=set_city,
        description="Set the current city"
    )
    ctx.register_command(
        "add-expense",
        handler=add_expense,
        description="Add an expense: /add-expense <amount> <category>"
    )
