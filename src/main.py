"""Main entry point for dependency visualizer."""
import sys
from src.cli import parse_args, validate_args, dump_config
from src.graph import DependencyGraph
from src.test_repo import load_test_repo, build_graph_from_test
from src.algorithms import (
    bfs_recursive, get_reverse_dependencies,
    filter_packages, detect_cycles
)
from src.visualization import generate_d2, print_ascii_tree

def build_product_graph(package, max_depth, substring):
    """Build graph from NuGet repository."""
    graph = DependencyGraph()
    visited = set()
    _bfs_nuget(package, graph, visited, 0, max_depth, substring)
    return graph

def _bfs_nuget(package, graph, visited, depth, max_depth, substring):
    """BFS traversal of NuGet dependencies."""
    if depth > max_depth or package in visited:
        return
    if substring and substring.lower() in package.lower():
        return
        
    visited.add(package)
    graph.add_node(package)
    
    try:
        from src.nuget import get_direct_dependencies
        deps = get_direct_dependencies(package)
    except Exception as err:
        print(f"Warning: {err}")
        return
        
    for dep in deps:
        if substring and substring.lower() in dep.lower():
            continue
        graph.add_edge(package, dep)
        _bfs_nuget(dep, graph, visited, depth + 1, max_depth, substring)

def main():
    """Main function."""
    try:
        args = parse_args()
        validate_args(args)
        dump_config(args)
    except (ValueError, FileNotFoundError) as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    if args.test_mode:
        data = load_test_repo(args.repo)
        graph = build_graph_from_test(data)
    else:
        graph = build_product_graph(args.package, args.max_depth, args.filter)

    cycles = detect_cycles(graph, args.package)
    if cycles:
        print(f"Detected {len(cycles)} cycles")

    deps = bfs_recursive(graph, args.package, args.max_depth)
    packages = [p for p, _ in deps]
    packages = filter_packages(packages, args.filter)

    if args.ascii_tree:
        print("\nDependency tree:")
        print_ascii_tree(graph, args.package, args.max_depth)

    reverse = get_reverse_dependencies(graph, args.package)
    if reverse:
        print(f"\nReverse deps: {reverse}")

    generate_d2(graph, packages, args.output)

if __name__ == "__main__":
    main()
