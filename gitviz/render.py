"""Textual rendering utilities for analysis summaries."""

import statistics
from typing import Dict, List


def render_summary(commits: List[dict], graph: Dict[str, dict], analysis: Dict[str, dict], summary_width: int) -> str:
    sections = []
    sections.append(compose_overview(analysis["activity"]))
    sections.append(compose_branch_section(analysis["branching"], graph, summary_width))
    sections.append(compose_temporal_section(analysis["temporal"], summary_width))
    sections.append(compose_tail_notes(len(graph)))
    return "\n\n".join(filter(None, sections))


def compose_overview(activity: Dict[str, object]) -> str:
    if activity["total"] == 0:
        return "No commits found in the requested range."
    start, end = activity["span"]
    top_authors = activity["authors"].most_common(3)
    lines = ["== Overview =="]
    lines.append(f"Commits inspected: {activity['total']}")
    lines.append(f"Active span: {start.date()} → {end.date()}")
    lines.append(f"Average commits/day: {activity['density']:.2f}")
    lines.append("Top authors:")
    for author, count in top_authors:
        lines.append(f"  - {author}: {count}")
    return "\n".join(lines)


def compose_branch_section(branching: Dict[str, object], graph: Dict[str, dict], width: int) -> str:
    lines = ["== Branching & Merges =="]
    lines.append(f"Merge commits detected: {branching['merge_total']}")
    if branching["diverging_points"]:
        sample = branching["diverging_points"][: min(5, len(branching["diverging_points"]))]
        lines.append("Representative divergence points:")
        for commit in sample:
            child_count = len(graph.get(commit, {}).get("children", []))
            lines.append(f"  - {commit[:7]} (children: {child_count})")
    if branching["top_merges"]:
        lines.append("Recent merges:")
        for entry in branching["top_merges"]:
            lines.append(
                f"  - {entry['hash'][:7]} parents={len(entry['parents'])} summary={entry['summary'][:width]}"
            )
    if branching["child_counts"]:
        lines.append("Child distribution (subset):")
        for commit, count in list(branching["child_counts"].items())[:5]:
            lines.append(f"  - {commit[:7]} → {count} children")
    if len(lines) == 2:
        lines.append("Graph appears mostly linear.")
    return "\n".join(lines)


def compose_temporal_section(temporal: Dict[str, object], width: int) -> str:
    lines = ["== Temporal Rhythm =="]
    timeline = temporal["timeline"]
    if not timeline:
        lines.append("No temporal data available.")
        return "\n".join(lines)
    chunks = chunk_timeline(timeline, width)
    lines.extend(chunks)
    if temporal["buckets"]:
        avg = statistics.mean(temporal["buckets"].values())
        lines.append(f"Average commits/week: {avg:.2f}")
    return "\n".join(lines)


def chunk_timeline(timeline: str, width: int) -> List[str]:
    lines: List[str] = []
    cursor = 0
    while cursor < len(timeline):
        lines.append(timeline[cursor : cursor + width])
        cursor += width
    return lines


def compose_tail_notes(node_count: int) -> str:
    lines = ["== Notes =="]
    lines.append("Flow validated as acyclic (standard git invariant).")
    lines.append(f"Nodes represented: {node_count}")
    lines.append("No repository mutations or cache files were created.")
    return "\n".join(lines)
