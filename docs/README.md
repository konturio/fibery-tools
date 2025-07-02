# Documentation

This project contains small utilities for interacting with Fibery and Slack. The scripts live under `src/`.

## Modules
- `align` – fixes missing task start times, branch names and resets disabled formula fields, including Estimate scaling intercept. When Fibery returns an unexpected response the script logs the raw body at error level and exits.
- `workflow` – generates Graphviz diagrams for active tasks and breaks circular dependencies. When no tasks are returned from the API the script logs the raw response and a warning. The script logs how many tasks and user stories were loaded and their JSON size. Fibery wraps entity lists in a top level ``data`` key and `workflow` unwraps it automatically.
- `slack_standup` – posts current task status to Slack.
- `slack_people` – sends a separate Slack message for each user with their tasks.
- `check_names` – scans a CSV file with tasks and reports naming issues.
- `disable_search` – disables search for selected Fibery types.
- `patch_ranks` – adjusts task ranks according to a CSV mapping.
- `fibery_userflow` – builds user flow diagrams from scenario steps.

See `config.py.example` for required configuration values.
All scripts load configuration from `config.py` in the repository root and exit if this file is missing.

Logs are emitted using structlog at info level by default and written to
stderr, keeping stdout clean for script output.

Continuous integration runs on GitHub Actions and checks code style,
executes unit tests and reports coverage to Codecov.

## Generating task diagram

Update ranks and render a diagram using Makefile targets:

```bash
make dot
make ranks
make svg
```
The `diagram` target combines ranks update with rendering in one step.
Run it directly when you need both actions in one command:

```bash
make diagram
```
