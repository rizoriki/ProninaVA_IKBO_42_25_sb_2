"""Test repository loader."""
import json
from src.graph import DependencyGraph

def load_test_repo(filepath):
    """Load test repository from JSON file."""
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def build_graph_from_test(data):
    """Build dependency graph from test data."""
    graph = DependencyGraph()
    for package, deps in data.items():
        graph.add_node(package)
        for dep in deps:
            graph.add_edge(package, dep)
    return graph
