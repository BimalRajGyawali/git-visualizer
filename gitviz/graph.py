"""Commit graph construction and validation utilities."""

from typing import Dict, List, Sequence


def build_commit_graph(commits: Sequence[dict]) -> Dict[str, dict]:
    graph = initialize_graph_nodes(commits)
    link_graph_edges(graph, commits)
    enforce_acyclic_flow(graph)
    return graph


def initialize_graph_nodes(commits: Sequence[dict]) -> Dict[str, dict]:
    graph: Dict[str, dict] = {}
    for entry in commits:
        graph[entry["hash"]] = {
            "parents": list(entry["parents"]),
            "children": [],
            "author": entry["author"],
            "timestamp": entry["timestamp"],
        }
    return graph


def link_graph_edges(graph: Dict[str, dict], commits: Sequence[dict]) -> None:
    for entry in commits:
        child = entry["hash"]
        for parent in entry["parents"]:
            if parent not in graph:
                continue
            graph[parent]["children"].append(child)




def _visit_node(graph: Dict[str, dict], visited: Dict[str, str], node: str, stack: List[str]) -> None:
    state = visited.get(node)
    if state == "perm":
        return
    if state == "temp":
        cycle = " -> ".join(stack + [node])
        raise RuntimeError(
            "Commit flow formed a cycle, which is unexpected in git history: " + cycle
        )
    visited[node] = "temp"
    stack.append(node)
    for parent in graph[node]["parents"]:
        if parent in graph:
            _visit_node(graph, visited, parent, stack)
    stack.pop()
    visited[node] = "perm"


def enforce_acyclic_flow(graph: Dict[str, dict]) -> None:
    visited: Dict[str, str] = {}
    for node in graph:
        if visited.get(node) != "perm":
            _visit_node(graph, visited, node, [])
