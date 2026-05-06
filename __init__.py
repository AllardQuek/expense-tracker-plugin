from .commands import (
    set_tracker,
    set_currency,
    set_city,
    list_trackers_command,
    delete_tracker_command,
    handle_expense,
)

def register(ctx):
    ctx.register_command(
        "set-tracker",
        handler=set_tracker,
        description="Create or switch the active expense tracker",
    )
    ctx.register_command(
        "set-currency",
        handler=set_currency,
        description="Set default currency for the active tracker",
    )
    ctx.register_command(
        "set-city",
        handler=set_city,
        description="Set default city for the active tracker",
    )
    ctx.register_command(
        "list-trackers",
        handler=list_trackers_command,
        description="List all expense trackers",
    )
    ctx.register_command(
        "delete-tracker",
        handler=delete_tracker_command,
        description="Delete a tracker and its CSV file",
    )
    ctx.register_command(
        "expense", 
        handler=handle_expense,
        description="Log an expense"
    )
