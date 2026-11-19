"""Graph data structure for dependencies."""

class DependencyGraph:
    """Directed graph for package dependencies."""

    def __init__(self):
        """Initialize empty graph."""
        self.nodes = set()
        self.edges = {}
        self.reverse_edges = {}

    def add_node(self, name):
        """Add a node to the graph."""
        self.nodes.add(name)
        if name not in self.edges:
            self.edges[name] = []
        if name not in self.reverse_edges:
            self.reverse_edges[name] = []

    def add_edge(self, source, target):
        """Add directed edge from source to target."""
        self.add_node(source)
        self.add_node(target)
        if target not in self.edges[source]:
            self.edges[source].append(target)
        if source not in self.reverse_edges[target]:
            self.reverse_edges[target].append(source)

    def get_dependencies(self, package):
        """Get direct dependencies of package."""
        return self.edges.get(package, [])

    def get_dependents(self, package):
        """Get packages that depend on given package."""
        return self.reverse_edges.get(package, [])
