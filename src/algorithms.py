"""Graph traversal algorithms."""

def bfs_recursive(graph, start, max_depth, visited=None, depth=0):
    """BFS with recursion to build dependency tree."""
    if visited is None:
        visited = set()
    if depth > max_depth or start in visited:
        return []
    
    visited.add(start)
    result = [(start, depth)]
    
    for dep in graph.get_dependencies(start):
        sub = bfs_recursive(graph, dep, max_depth, visited, depth + 1)
        result.extend(sub)
    return result

def get_reverse_dependencies(graph, package):
    """Get all packages that depend on given package."""
    visited = set()
    result = []
    _collect_reverse(graph, package, visited, result)
    return result

def _collect_reverse(graph, package, visited, result):
    """Recursively collect reverse dependencies."""
    for dep in graph.get_dependents(package):
        if dep not in visited:
            visited.add(dep)
            result.append(dep)
            _collect_reverse(graph, dep, visited, result)

def filter_packages(packages, substring):
    """Filter out packages containing substring."""
    if not substring:
        return packages
    sub_lower = substring.lower()
    return [p for p in packages if sub_lower not in p.lower()]

def detect_cycles(graph, start):
    """Detect cycles in dependency graph from start."""
    visited = set()
    rec_stack = set()
    cycles = []
    _dfs_cycle(graph, start, visited, rec_stack, [], cycles)
    return cycles

def _dfs_cycle(graph, node, visited, stack, path, cycles):
    """DFS helper for cycle detection."""
    visited.add(node)
    stack.add(node)
    path.append(node)
    
    for dep in graph.get_dependencies(node):
        if dep not in visited:
            _dfs_cycle(graph, dep, visited, stack, path, cycles)
        elif dep in stack:
            idx = path.index(dep)
            cycles.append(path[idx:] + [dep])
            
    path.pop()
    stack.remove(node)
