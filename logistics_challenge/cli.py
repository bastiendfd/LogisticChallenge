"""Command-line entry point for the synthetic transportation exercise."""

from __future__ import annotations

from collections.abc import Callable

from .model import TransportProblem, solve_transport


SYNTHETIC_PROBLEM = TransportProblem(
    origins=("North Hub", "Central Hub", "South Hub"),
    destinations=("Clinic A", "Clinic B", "Clinic C", "Clinic D"),
    capacities=(100, 120, 90),
    demands=(60, 80, 70, 50),
    unit_costs=((4, 6, 9, 5), (5, 4, 7, 6), (8, 5, 3, 4)),
)


def main(output: Callable[[str], None] = print) -> None:
    """Solve and print the deliberately small, deterministic challenge instance."""
    result = solve_transport(SYNTHETIC_PROBLEM)
    output("Synthetic transportation optimisation exercise")
    output(f"Objective cost: {result.objective_cost}")
    output(f"All demand constraints satisfied: {result.total_received_by_destination == SYNTHETIC_PROBLEM.demands}")
    output(
        "All capacity constraints satisfied: "
        f"{all(sent <= capacity for sent, capacity in zip(result.total_sent_by_origin, SYNTHETIC_PROBLEM.capacities))}"
    )
    for origin, row in zip(SYNTHETIC_PROBLEM.origins, result.shipments):
        output(f"{origin}: {dict(zip(SYNTHETIC_PROBLEM.destinations, row))}")


if __name__ == "__main__":
    main()
