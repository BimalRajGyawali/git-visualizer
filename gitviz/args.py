from pathlib import Path
import json
from types import SimpleNamespace


def load_config_args(config_path: Path | None = None) -> tuple[SimpleNamespace, str]:
    """Load CLI-like args from ./git_viz_config.json (fallback to defaults)."""
    if config_path is None:
        config_path = Path.cwd() / "git_viz_config.json"

    config = {}
    if config_path.exists():
        try:
            with config_path.open("r", encoding="utf-8") as fh:
                config = json.load(fh) or {}
        except Exception:
            config = {}

    args = SimpleNamespace()

    raw_repo = config.get("repo")
    repo = str(Path.cwd()) if not raw_repo else raw_repo

    branches = config.get("branches", [])
    if isinstance(branches, str):
        branches = [b.strip() for b in branches.split(",") if b.strip()]
    elif branches is None:
        branches = []
    args.branches = branches

    try:
        args.max_commits = int(config.get("max_commits", 1000))
    except (TypeError, ValueError):
        args.max_commits = 1000

    args.show_children = bool(config.get("show_children", False))

    try:
        args.summary_width = int(config.get("summary_width", 80))
    except (TypeError, ValueError):
        args.summary_width = 80

    return args, repo