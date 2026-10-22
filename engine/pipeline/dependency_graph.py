"""Build and sort the document dependency DAG."""

from __future__ import annotations

from collections import defaultdict

from engine.models.enums import DocID
from engine.specs import ALL_SPECS


def build_generation_order(triggered_docs: dict[DocID, bool]) -> list[DocID]:
    """Topological sort of triggered documents respecting upstream_deps.

    Returns ordered list: generate docs in this sequence.
    Docs at the same depth level could be parallelized (not implemented yet).
    """
    active = {doc_id for doc_id, on in triggered_docs.items() if on}

    # Build adjacency list (only among active docs)
    in_degree: dict[DocID, int] = {d: 0 for d in active}
    graph: dict[DocID, list[DocID]] = defaultdict(list)

    for doc_id in active:
        spec = ALL_SPECS.get(doc_id)
        if not spec:
            continue
        for dep in spec.upstream_deps:
            if dep in active:
                graph[dep].append(doc_id)
                in_degree[doc_id] += 1

    # Kahn's algorithm
    queue = sorted(
        [d for d in active if in_degree[d] == 0],
        key=lambda d: _tier_priority(d),
    )
    result: list[DocID] = []

    while queue:
        node = queue.pop(0)
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
        # Re-sort queue to maintain tier priority among same-depth docs
        queue.sort(key=lambda d: _tier_priority(d))

    # Safety: any remaining docs (circular deps or missing specs) appended at end
    remaining = active - set(result)
    if remaining:
        result.extend(sorted(remaining, key=lambda d: _tier_priority(d)))

    return result


def get_parallel_groups(triggered_docs: dict[DocID, bool]) -> list[list[DocID]]:
    """Group documents by dependency depth for potential parallel execution.

    Returns list of groups: all docs in group[i] can run in parallel,
    but must wait for all groups < i to complete.
    """
    active = {doc_id for doc_id, on in triggered_docs.items() if on}
    in_degree: dict[DocID, int] = {d: 0 for d in active}
    graph: dict[DocID, list[DocID]] = defaultdict(list)

    for doc_id in active:
        spec = ALL_SPECS.get(doc_id)
        if not spec:
            continue
        for dep in spec.upstream_deps:
            if dep in active:
                graph[dep].append(doc_id)
                in_degree[doc_id] += 1

    groups: list[list[DocID]] = []
    current = sorted([d for d in active if in_degree[d] == 0], key=lambda d: d.value)

    while current:
        groups.append(current)
        next_level = []
        for node in current:
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    next_level.append(neighbor)
        current = sorted(set(next_level), key=lambda d: d.value)

    return groups


def _tier_priority(doc_id: DocID) -> tuple[int, str]:
    """Sort key: Universal first, then BM, CH, FC, MT. Within tier, alphabetical."""
    tier_order = {"U": 0, "B": 1, "C": 2, "F": 3, "M": 4}
    prefix = doc_id.value[0]
    return (tier_order.get(prefix, 9), doc_id.value)