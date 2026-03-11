# structural-scan

Structural diagnostics for software systems.

Detect structural signals in codebases by analyzing dependency relationships, module structure, and propagation risks.


# -structural-analyzer
 It gives developers an immediate answer to:  “Where is my system structurally fragile?”
structural-scan

Structural diagnostics for software repositories.

structural-scan is a small command-line tool that analyzes a codebase as a structural system rather than just a collection of files.

Instead of asking:

Does the code compile?

Do the tests pass?

This tool asks:

Where are structural dependencies concentrating?

Which modules could trigger failure cascades?

Are tests verifying behavior or implementation details?

It produces a simple structural diagnostics report highlighting signals such as dependency imbalance, cascade risk, and brittle tests.

Why this exists

Most developer tooling focuses on:

Category	Tools
correctness	unit tests, type systems
runtime	logging, tracing
performance	profilers

But software failures are often structural, not just functional.

Examples:

a dependency hub that silently becomes critical infrastructure

a test suite tightly coupled to internal implementation

a module whose change cascades across the system

structural-scan explores these questions by modeling a repository as a transition graph and looking for structural signals.

Installation

Clone the repository:

git clone https://github.com/YOUR_ORG/structural-scan.git
cd structural-scan

No dependencies required beyond Python 3.9+.

Usage

Run the scanner against a repository:

python structural_scan.py /path/to/repository

Example:

python structural_scan.py .
Example Output
Structural Diagnostics Report

Nodes analyzed: 184
Edges analyzed: 712

Signals detected:

operator_imbalance
  module: data_loader
  severity: medium

implementation_coupling
  tests referencing private attributes: 12

cascade_risk
  dependency chain length: 8
  origin: core/config
Signals Explained
Operator Imbalance

A module or component has significantly more outgoing dependencies than others.

Possible implications:

hidden coordination hub

fragile architectural boundary

Cascade Risk

A dependency chain is unusually long.

Possible implications:

a change in the root module could trigger widespread breakage

difficult refactoring surface

Implementation Coupling

Tests reference private attributes or internal structures.

Example:

assert graph._adjacency["A"] == ["B"]

This suggests the test suite may be detecting implementation changes rather than behavioral regressions.

Conceptual Model

The tool models a repository as a graph:

module → dependency → module

From this graph it derives:

structure
↓
signals
↓
cascade risk

This approach is inspired by research in:

network science

system dynamics

failure cascade modeling

but applied to software repositories.

What This Tool Is (and Is Not)
This tool is

a structural analysis experiment

a simple diagnostic CLI

a demonstration of structural observability for software systems

This tool is not

a replacement for test suites

a static type checker

a linter

a security scanner

It complements existing tools by analyzing system structure.

Roadmap

Planned improvements include:

richer dependency graph extraction

test behavior vs implementation analysis

visualization of cascade paths

structural drift analysis across commits

Example Use Cases

Developers might use this tool to:

understand hidden dependency hubs

detect fragile test suites

evaluate refactoring risk

explore structural stability of a system

Philosophy

Most tooling answers:

What is happening right now?

Structural diagnostics asks:

What forces are pushing this system toward stability or collapse?

License

MIT License.

Contributing

Contributions are welcome.

Areas especially useful:

improved dependency analysis

language support beyond Python

structural signal detection algorithms

visualization tools

A Note on Scope

This repository intentionally starts small.

The goal is to explore a simple idea:

Software systems have structure, and that structure can be analyzed.

If the idea proves useful, the tooling will evolve.

# Related Tools

This project is part of a small family of tools exploring structural diagnostics for software systems.

structural-scan — detects structural signals in codebases

test-audit — analyzes the structural health of test suites

cascade-map — visualizes dependency cascade paths

Each tool examines a different structural layer of a system:

codebase structure  →  structural-scan
test architecture   →  test-audit
dependency geometry →  cascade-map

Together they explore a simple idea:

software systems have structure, and that structure can be analyzed.

If you want to make the connection even clearer across repos, you can optionally add one closing line like this:

These tools are intentionally small and independent, but they share a common goal: making structural properties of software systems visible.
