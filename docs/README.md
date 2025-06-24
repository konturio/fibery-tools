# Documentation

This project contains small utilities for interacting with Fibery and Slack. The scripts live under `src/`.

## Modules
- `align` – fixes missing task start times and branch names.
- `workflow` – generates Graphviz diagrams for active tasks.
- `slack_standup` – posts current task status to Slack.
- `queries` – constructs JSON requests for the Fibery API.

See `config.py.example` for required configuration values.

Continuous integration runs on GitHub Actions and checks code style,
executes unit tests and reports coverage to Codecov.
