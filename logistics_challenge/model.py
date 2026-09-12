"""A small, deterministic transportation linear-programming model."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from pulp import LpMinimize, LpProblem, LpStatusOptimal, LpVariable, PULP_CBC_CMD, lpSum, value


@dataclass(frozen=True)
class TransportProblem:
    """Synthetic inputs for one transportation optimisation exercise."""

    origins: Tuple[str, ...]
    destinations: Tuple[str, ...]
    capacities: Tuple[int, ...]
    demands: Tuple[int, ...]
    unit_costs: Tuple[Tuple[int, ...], ...]


@dataclass(frozen=True)
class TransportResult:
    """A feasible minimum-cost shipment plan."""

    shipments: Tuple[Tuple[int, ...], ...]
    objective_cost: int
    total_sent_by_origin: Tuple[int, ...]
    total_received_by_destination: Tuple[int, ...]


def _validate(problem: TransportProblem) -> None:
    if not problem.origins or not problem.destinations:
        raise ValueError("At least one origin and destination are required")
    if len(problem.origins) != len(problem.capacities):
        raise ValueError("Each origin needs one capacity")
    if len(problem.destinations) != len(problem.demands):
        raise ValueError("Each destination needs one demand")
    if len(problem.unit_costs) != len(problem.origins) or any(
        len(row) != len(problem.destinations) for row in problem.unit_costs
    ):
        raise ValueError("Unit costs must have one row per origin and one column per destination")
    if any(quantity < 0 for quantity in (*problem.capacities, *problem.demands)):
        raise ValueError("Capacities and demands must be non-negative")
    if any(cost < 0 for row in problem.unit_costs for cost in row):
        raise ValueError("Unit costs must be non-negative")
    if sum(problem.capacities) < sum(problem.demands):
        raise ValueError("Total capacity must be at least total demand")


def solve_transport(problem: TransportProblem) -> TransportResult:
    """Solve the integer transportation model with PuLP's bundled CBC solver."""
    _validate(problem)
    origin_count, destination_count = len(problem.origins), len(problem.destinations)
    model = LpProblem("synthetic_transportation_exercise", LpMinimize)
    shipment = {
        (origin, destination): LpVariable(
            f"shipment_{origin}_{destination}", lowBound=0, cat="Integer"
        )
        for origin in range(origin_count)
        for destination in range(destination_count)
    }

    model += lpSum(
        problem.unit_costs[origin][destination] * shipment[origin, destination]
        for origin in range(origin_count)
        for destination in range(destination_count)
    )
    for origin in range(origin_count):
        model += lpSum(shipment[origin, destination] for destination in range(destination_count)) <= problem.capacities[origin]
    for destination in range(destination_count):
        model += lpSum(shipment[origin, destination] for origin in range(origin_count)) == problem.demands[destination]

    status = model.solve(PULP_CBC_CMD(msg=False))
    if status != LpStatusOptimal:
        raise RuntimeError("CBC did not find an optimal solution")

    shipments = tuple(
        tuple(int(value(shipment[origin, destination])) for destination in range(destination_count))
        for origin in range(origin_count)
    )
    sent = tuple(sum(row) for row in shipments)
    received = tuple(sum(shipments[origin][destination] for origin in range(origin_count)) for destination in range(destination_count))
    return TransportResult(shipments, int(value(model.objective)), sent, received)
