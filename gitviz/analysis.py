"""Multi-pass commit analysis utilities."""

from collections import Counter, defaultdict
from typing import Dict, Sequence


def run_analysis_pipeline(commits: Sequence[dict], graph: Dict[str, dict], show_children: bool) -> Dict[str, dict]:
    activity = activity_pass(commits)
    branching = branch_pass(commits, graph, show_children)
    temporal = temporal_pass(commits)
    return {
        "activity": activity,
        "branching": branching,
        "temporal": temporal,
    }


def activity_pass(commits: Sequence[dict]) -> Dict[str, object]:
    total = len(commits)
    if total == 0:
        return {"total": 0, "authors": Counter(), "span": None, "density": 0.0}
    authors = Counter(entry["author"] for entry in commits)
    span_days = max(1, (commits[-1]["timestamp"] - commits[0]["timestamp"]).days or 1)
    density = total / span_days
    return {
        "total": total,
        "authors": authors,
        "span": (commits[0]["timestamp"], commits[-1]["timestamp"]),
        "density": density,
    }


def branch_pass(commits: Sequence[dict], graph: Dict[str, dict], show_children: bool) -> Dict[str, object]:
    merge_commits = [c for c in commits if len(c["parents"]) > 1]
    diverging_points = [h for h, node in graph.items() if len(node["children"]) > 1]
    child_counts = {
        h: len(node["children"]) for h, node in graph.items() if show_children and node["children"]
    }
    top_merges = merge_commits[:5]
    return {
        "merge_total": len(merge_commits),
        "diverging_points": diverging_points,
        "child_counts": child_counts,
        "top_merges": top_merges,
    }


def temporal_pass(commits: Sequence[dict]) -> Dict[str, object]:
    if not commits:
        return {"timeline": [], "buckets": {}}
    buckets = bucket_commits_by_week(commits)
    timeline = build_ascii_timeline(buckets)
    return {
        "timeline": timeline,
        "buckets": buckets,
    }


def bucket_commits_by_week(commits: Sequence[dict]) -> Dict[str, int]:
    per_week: Dict[str, int] = defaultdict(int)
    for item in commits:
        year, week, _ = item["timestamp"].isocalendar()
        key = f"{year}-W{week:02d}"
        per_week[key] += 1
    return dict(sorted(per_week.items()))


def build_ascii_timeline(buckets: Dict[str, int]) -> str:
    if not buckets:
        return "(no temporal signal)"
    values = list(buckets.values())
    max_val = max(values)
    width = min(60, len(values))
    scale = max_val / width if width else 1
    if scale == 0:
        scale = 1
    chars = []
    for idx, count in enumerate(values):
        height = max(1, round(count / scale))
        chars.append("█" * height)
        if (idx + 1) % 8 == 0:
            chars.append(" ")
    return "".join(chars)
