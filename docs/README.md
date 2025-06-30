# Documentation

This project contains small utilities for interacting with Fibery and Slack. The scripts live under `src/`.

## Modules
- `align` – fixes missing task start times, branch names and resets disabled formula fields, including Estimate scaling intercept.
- `workflow` – generates Graphviz diagrams for active tasks.
- `slack_standup` – posts current task status to Slack.
- `slack_people` – sends a separate Slack message for each user with their tasks.
- `check_names` – scans a CSV file with tasks and reports naming issues.
- `disable_search` – disables search for selected Fibery types.
- `patch_ranks` – adjusts task ranks according to a CSV mapping.
- `fibery_userflow` – builds user flow diagrams from scenario steps.

See `config.py.example` for required configuration values.

Continuous integration runs on GitHub Actions and checks code style,
executes unit tests and reports coverage to Codecov.
