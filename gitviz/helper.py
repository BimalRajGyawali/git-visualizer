import datetime as _dt
from typing import Dict, List, Sequence

SEPARATOR = "\x01"


def build_git_log_command(repo: str, branches: Sequence[str] | None, max_commits: int) -> List[str]:
    base_command = [
        "git",
        "-C",
        repo,
        "log",
        "--date=iso-strict",
        f"--max-count={max_commits}",
        "--pretty=format:%H"
        + SEPARATOR
        + "%P"
        + SEPARATOR
        + "%an"
        + SEPARATOR
        + "%ad"
        + SEPARATOR
        + "%s",
    ]
    if not branches:
        base_command.append("--all")
    else:
        base_command.extend(branches)
    return base_command


def parse_commit_stream(raw_output: str) -> List[dict]:
    commits: List[dict] = []
    for line in raw_output.splitlines():
        if not line.strip():
            continue
        parts = line.split(SEPARATOR)
        if len(parts) != 5:
            continue
        commit_hash, parents_field, author, date_str, subject = parts
        timestamp = parse_timestamp(date_str)
        parents = [p for p in parents_field.split(" ") if p]
        commits.append(
            {
                "hash": commit_hash,
                "parents": parents,
                "author": author,
                "timestamp": timestamp,
                "summary": subject.strip(),
            }
        )
    return commits


def parse_timestamp(raw: str) -> _dt.datetime:
    try:
        return _dt.datetime.fromisoformat(raw)
    except ValueError:
        return _dt.datetime.strptime(raw.split(" ")[0], "%Y-%m-%d")
