#!/usr/bin/env python3
from gitviz.analysis import run_analysis_pipeline
from gitviz.git_history import collect_commit_history, ensure_git_repository
from gitviz.graph import build_commit_graph
from gitviz.render import render_summary
from pathlib import Path
import json
from gitviz.args import load_config_args


def load_and_ensure_repo():
    args, repo = load_config_args()
    ensure_git_repository(repo)
    return args, repo


def analyze_git_repo(repo, branches, max_commits, show_children, summary_width):
    commits = collect_commit_history(repo, branches, max_commits)
    graph = build_commit_graph(commits)
    analysis = run_analysis_pipeline(commits, graph, show_children)
    summary = render_summary(commits, graph, analysis, summary_width)
    return summary