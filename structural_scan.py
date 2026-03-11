import os
import ast
from collections import defaultdict

class RepoGraph:

    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(set)

    def add_edge(self, src, dst):
        self.nodes.add(src)
        self.nodes.add(dst)
        self.edges[src].add(dst)

    def next_nodes(self, node):
        return self.edges.get(node, set())

    def reachable(self, start):
        visited = set()
        stack = [start]

        while stack:
            n = stack.pop()
            if n not in visited:
                visited.add(n)
                stack.extend(self.next_nodes(n))

        return visited


def find_python_files(path):

    files = []

    for root, _, filenames in os.walk(path):
        for f in filenames:
            if f.endswith(".py"):
                files.append(os.path.join(root, f))

    return files


def build_dependency_graph(files):

    graph = RepoGraph()

    for file in files:

        with open(file, "r", encoding="utf8") as f:
            try:
                tree = ast.parse(f.read())
            except Exception:
                continue

        module = os.path.basename(file)

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for name in node.names:
                    graph.add_edge(module, name.name)

            if isinstance(node, ast.ImportFrom):

                if node.module:
                    graph.add_edge(module, node.module)

    return graph


def detect_operator_imbalance(graph):

    counts = []

    for src in graph.edges:
        counts.append(len(graph.edges[src]))

    if not counts:
        return None

    if max(counts) > 5 * max(1, min(counts)):
        return {
            "signal": "operator_imbalance",
            "severity": "medium"
        }

    return None


def detect_cascade_risk(graph):

    max_depth = 0
    origin = None

    for node in graph.nodes:

        reachable = graph.reachable(node)
        depth = len(reachable)

        if depth > max_depth:
            max_depth = depth
            origin = node

    if max_depth > 10:
        return {
            "signal": "cascade_risk",
            "origin": origin,
            "severity": "high",
            "reach": max_depth
        }

    return None


def detect_test_coupling(files):

    coupling = 0

    for file in files:

        if "test" not in file.lower():
            continue

        with open(file, "r", encoding="utf8") as f:
            content = f.read()

        if "._" in content:
            coupling += 1

    if coupling > 0:
        return {
            "signal": "implementation_coupling",
            "severity": "medium",
            "count": coupling
        }

    return None


def run_analysis(path):

    print("\nStructural Diagnostics Report\n")

    files = find_python_files(path)

    graph = build_dependency_graph(files)

    print(f"Nodes analyzed: {len(graph.nodes)}")
    print(f"Edges analyzed: {sum(len(e) for e in graph.edges.values())}\n")

    signals = []

    s1 = detect_operator_imbalance(graph)
    if s1:
        signals.append(s1)

    s2 = detect_cascade_risk(graph)
    if s2:
        signals.append(s2)

    s3 = detect_test_coupling(files)
    if s3:
        signals.append(s3)

    if not signals:
        print("No structural signals detected.\n")
        return

    print("Signals detected:\n")

    for s in signals:
        print(s)


if __name__ == "__main__":

    import sys

    if len(sys.argv) != 2:
        print("Usage: python structural_scan.py <repo_path>")
        sys.exit(1)

    run_analysis(sys.argv[1])
