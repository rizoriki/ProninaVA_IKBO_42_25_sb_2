"""Visualization modules for dependency graph."""
import subprocess

def generate_d2(graph, packages, filename):
    """Generate D2 diagram and save as PNG."""
    d2_content = _build_d2_content(graph, packages)
    d2_file = filename.replace(".png", ".d2")
    with open(d2_file, "w", encoding="utf-8") as file:
        file.write(d2_content)
    print(f"D2 diagram saved to {d2_file}")
    _render_d2_to_png(d2_file, filename)

def _build_d2_content(graph, packages):
    """Build D2 language content."""
    pkg_set = set(packages)
    lines = []
    for pkg in packages:
        for dep in graph.get_dependencies(pkg):
            if dep in pkg_set:
                lines.append(f"{pkg} -> {dep}")
    return "\n".join(lines)

def _render_d2_to_png(d2_file, png_file):
    """Render D2 file to PNG using d2 CLI."""
    try:
        subprocess.run(
            ["d2", d2_file, png_file],
            check=True, capture_output=True
        )
        print(f"PNG saved to {png_file}")
    except FileNotFoundError:
        print("Warning: d2 CLI not found")
    except subprocess.CalledProcessError as err:
        print(f"Warning: d2 render failed: {err}")

def print_ascii_tree(graph, package, max_depth):
    """Print dependency tree in ASCII format."""
    visited = set()
    _print_tn(graph, package, "", True, 0, max_depth, visited)

def _print_tn(graph, pkg, prefix, is_last, depth, max_depth, visited):
    """Print single node in ASCII tree."""
    if depth > max_depth or pkg in visited:
        return
    visited.add(pkg)
    
    connector = "└── " if is_last else "├── "
    if depth == 0:
        print(pkg)
    else:
        print(f"{prefix}{connector}{pkg}")
        
    deps = graph.get_dependencies(pkg)
    for i, dep in enumerate(deps):
        is_last_dep = (i == len(deps) - 1)
        new_prefix = prefix + ("    " if is_last else "│   ")
        _print_tn(graph, dep, new_prefix, is_last_dep, depth + 1, max_depth, visited)
