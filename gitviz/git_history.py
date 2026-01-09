"""Pure functions for gathering git history without mutating repositories."""

import subprocess
from typing import Dict, List, Sequence

from gitviz.helper import build_git_log_command, parse_commit_stream, parse_timestamp


def ensure_git_repository(path: str) -> None:
    command = ["git", "-C", path, "rev-parse", "--is-inside-work-tree"]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Path '{path}' is not a git repository (git message: {result.stderr.strip()})"
        )


def collect_commit_history(repo: str, branches: Sequence[str] | None, max_commits: int) -> List[dict]:
    raw_output = acquire_git_stream(repo, branches, max_commits)
    commits = parse_commit_stream(raw_output)
    commits.sort(key=lambda item: item["timestamp"])
    return commits


def acquire_git_stream(repo: str, branches: Sequence[str] | None, max_commits: int) -> str:
    command = build_git_log_command(repo, branches, max_commits)
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("Failed to read git history: " + result.stderr.strip())
    return result.stdout


