# Git Visualizer CLI

A constraints-aware, read-only command-line utility for interpreting git history through multiple analytical passes without mutating the repository.

## Features

- Streams commit history via `git log` (no custom plumbing).
- Builds an in-memory commit graph with parent/child relationships.
- Runs three analysis passes (activity, branching, temporal) before composing the summary.
- Produces ASCII timelines and structured bullet overviews suitable for research narratives.
- Obeys strict constraints: no filesystem writes, no caching, no third-party libraries.

## Usage

```bash
python3 git_viz_cli.py --max-commits 200 --show-children
```

Optional flags:

- `repo` positional argument to analyze another repository.
- `--branches <ref ...>` to limit history to specific refs.
- `--summary-width` to tune printed line width.
- `--show-children` to surface per-commit child counts.

## Development Notes

- Requires Python 3.9+ for `datetime.fromisoformat` support.
- Relies solely on the standard library (`argparse`, `subprocess`, `collections`, `statistics`).
- Organized as a lightweight module suite (`gitviz/`) with function-only components (no classes or async code).
- Safe to run in research environments thanks to its read-only interaction model.

## Module layout

- `gitviz/args.py` – argparse wiring and validation helpers.
- `gitviz/git_history.py` – pure functions for streaming and parsing git log data.
- `gitviz/graph.py` – parent/child graph construction plus acyclicity enforcement.
- `gitviz/analysis.py` – multi-pass commit interpretation (activity, branching, temporal).
- `gitviz/render.py` – textual summary composers and ASCII timeline helpers.
