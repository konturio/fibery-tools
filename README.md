# Fibery tools

Small utilities to work with Fibery tasks and Slack standups.

## Usage

1. Copy `config.py.example` to `config.py` and fill in your tokens.
2. Install dependencies from `requirements.txt`.
3. Run any script from the `src/` directory, e.g.

```bash
python src/workflow.py | dot -v -Tsvg > tasks.svg
```
Generate diagrams using Makefile helpers:

```bash
make align   # build tasks.dot
make ranks   # update ranks in Fibery
make svg     # render tasks.svg
```
Run `make diagram` to perform ranks update and render in one go.
See `docs/README.md` for more details and `docs/config.md` for configuration options.
