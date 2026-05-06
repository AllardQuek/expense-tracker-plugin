# Expense Tracker Plugin

A lightweight Hermes Agent plugin for logging expenses quickly into CSV files using slash commands.

This project is an MVP focused on one job: make it easy to capture expenses in Hermes chat, route them to the right tracker, and preserve the raw values you entered for later analysis.

## What it does

The plugin currently supports:

- Logging an expense from chat with `/expense`
- Managing multiple trackers with separate CSV files
- Setting an active tracker
- Setting default currency and city per tracker
- Listing and deleting trackers
- Writing structured rows to CSV for later analysis

Each tracker stores:
- its own CSV file path
- a default currency
- a default city

Expense rows currently support these fields:

- `name`
- `tags`
- `cost`
- `currency`
- `cost_sgd`
- `city`

`cost_sgd` is optional in MVP. The plugin preserves the original `cost` and `currency` even when SGD conversion is not available.

## Why this exists

The goal is fast, low-friction expense capture inside Hermes.

Instead of opening a spreadsheet or app, you can log expenses in a natural compact format such as:

```text
/expense coffee - 12
/expense ramen - 1200 jpy - #food - kyoto
/expense ferry - 35 jpy - #travel - osaka - 0.32
```

This keeps capture fast while still producing structured CSV output for later cleanup, analysis, or import into other tools.

## Current status

This repository is at **MVP** stage.

Working areas:
- Slash command registration
- Active tracker management
- CSV writing
- Basic parsing for expense input
- Default currency/city support
- Optional `cost_sgd`

Not prioritized yet:
- Automatic FX conversion
- Duplicate detection
- Rich reporting
- Advanced validation and normalization
- Full migration tooling for legacy tracker paths

## Commands

### Expense logging

```text
/expense <name> - <cost> [currency] - [#tags] - [city] - [cost_sgd]
```

Examples:

```text
/expense coffee - 12
/expense lunch - 15 sgd - #friends
/expense ramen - 1200 jpy - #food - kyoto
/expense ferry - 35 jpy - #travel - osaka - 0.32
```

Notes:
- `name` and `cost` are required
- `currency` is optional if the active tracker has a default currency
- `city` is optional if the active tracker has a default city
- `cost_sgd` is optional

### Tracker management

```text
/set-tracker <name>
/set-currency <currency_code>
/set-city <city_name>
/list-trackers
/delete-tracker <name>
```

## How it works

The plugin is intentionally split into a few small modules:

- `__init__.py`  
  Registers Hermes slash commands.

- `commands.py`  
  Hermes-facing command handlers. These parse raw command input, call internal helpers, and return user-facing strings.

- `parser.py`  
  Parses `/expense ...` input into a normalized structured dict.

- `csv_writer.py`  
  Ensures CSV files exist and appends normalized expense rows.

- `state.py`  
  Manages tracker state, active tracker selection, and tracker defaults.

- `plugin.yaml`  
  Basic Hermes plugin manifest.

This separation helps keep chat command wiring, state management, parsing, and CSV persistence independent.

## Data model

### Tracker state

A tracker stores metadata such as:

- `csv_path`
- `default_currency`
- `default_city`

The plugin also stores which tracker is currently active.

### CSV schema

Current CSV header:

```text
name,tags,cost,currency,cost_sgd,city
```

This schema is intentionally simple for MVP and optimized for later spreadsheet or script-based analysis.

## Installation

### 1. Place the plugin in your Hermes plugins directory

Example layout:

```text
~/.hermes/profiles/<profile>/plugins/expense_tracker/
  __init__.py
  commands.py
  csv_writer.py
  parser.py
  plugin.yaml
  state.py
```

### 2. Make sure the folder/package name is import-safe

Use:

```text
expense_tracker
```

not:

```text
expense-tracker
```

Python imports work cleanly with underscores, and this avoids package/import issues.

### 3. Restart Hermes

Hermes loads and registers plugin commands at startup, so restart Hermes after making code changes.

### 4. Verify the plugin loaded

In Hermes chat, check:

```text
/plugins
```

Then test the command flow:

```text
/set-tracker default
/expense coffee - 12
/list-trackers
```

## Example workflow

### Create or activate a tracker

```text
/set-tracker Japan-2027
/set-currency JPY
/set-city Kyoto
```

### Log expenses

```text
/expense ramen - 1200
/expense coffee - 450 - #cafe
/expense train - 230 - #transport - osaka
```

Because the tracker already has defaults, you can omit currency and city in many cases.

## Design decisions

### Why CSV?
CSV is portable, easy to inspect, easy to import into spreadsheets, and easy to process with scripts.

### Why keep `cost_sgd` optional?
FX lookup adds complexity and external dependencies. For MVP, it is more important to preserve the original amount and currency reliably than to block logging on conversion.

### Why separate commands from state?
`commands.py` handles Hermes-facing command responses, while `state.py` contains reusable tracker/state logic. This keeps the plugin easier to test and extend.

## Known limitations

- No automatic exchange rate conversion yet
- No duplicate protection yet
- No reporting or summaries yet
- Error handling is functional but still basic
- Legacy tracker paths from older folder names may need cleanup if you renamed the plugin directory during development

## Troubleshooting

### Command does not appear in Hermes
- Restart Hermes
- Check `/plugins`
- Confirm `register()` in `__init__.py` imports all command handlers correctly

### Expense says it saved but row is not where expected
- Check which tracker is active
- Check the tracker’s `csv_path`
- Confirm you are inspecting the exact file path stored in state, not just a same-named file in the current directory

### `KeyError: 'name'`
A common cause is assuming the tracker object contains its own name. In this plugin, the tracker name may live in state as the key or as `active_tracker`, not inside the tracker dict itself.

## Roadmap ideas

Possible future improvements:

- `/show-context`
- Better validation and friendlier error messages
- Duplicate detection
- SGD auto-conversion
- Historical summaries and reporting
- Export helpers or spreadsheet integrations

## Contributing

This project is currently optimized for fast iteration and personal workflow validation. Contributions, suggestions, and issue reports are welcome, especially around:

- parsing edge cases
- command UX
- CSV schema evolution
- migration and state handling
- reporting ideas

## License

Distributed under the MIT License.
