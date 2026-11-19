"""Command-line interface and configuration."""
import argparse
import os
MAX_DEPTH_DEFAULT = 10
DEFAULT_OUTPUT = "graph.png"
def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Dependency graph visualizer"
    )
    parser.add_argument("--package", type=str, required=True)
    parser.add_argument("--repo", type=str, required=True)
    parser.add_argument("--test-mode", action="store_true")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT)
    parser.add_argument("--ascii-tree", action="store_true")
    parser.add_argument("--max-depth", type=int, default=MAX_DEPTH_DEFAULT)
    parser.add_argument("--filter", type=str, default="")
    return parser.parse_args()
def validate_args(args):
    """Validate parsed arguments."""
    if args.max_depth < 1:
        raise ValueError("Max depth must be positive")
    if not args.test_mode and not args.repo.startswith("http"):
        raise ValueError("Repo must be URL in non-test mode")
    if args.test_mode and not os.path.exists(args.repo):
        raise FileNotFoundError(f"Test file not found: {args.repo}")
def dump_config(args):
    """Print configuration in key-value format."""
    config = {
        "package": args.package,
        "repo": args.repo,
        "test_mode": args.test_mode,
        "output": args.output,
        "ascii_tree": args.ascii_tree,
        "max_depth": args.max_depth,
        "filter": args.filter,
    }
    for key, value in config.items():
        print(f"{key}={value}")
