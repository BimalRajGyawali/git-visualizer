#!/usr/bin/env python3
"""Entry point for the modular git visualizer CLI."""

from gitviz.analysis import run_analysis_pipeline
from gitviz.git_history import collect_commit_history, ensure_git_repository
from gitviz.graph import build_commit_graph
from gitviz.render import render_summary
from pathlib import Path
import json
from analyzer import load_and_ensure_repo, analyze_git_repo


def main():
    args, repo = load_and_ensure_repo()
    summary = analyze_git_repo(repo, args.branches, args.max_commits, args.show_children, args.summary_width)
    print(summary)
    
if __name__ == "__main__":
    main()
