from logistics_challenge.model import TransportProblem, solve_transport


def small_problem() -> TransportProblem:
    return TransportProblem(
        origins=("North Hub", "Central Hub", "South Hub"),
        destinations=("Clinic A", "Clinic B", "Clinic C", "Clinic D"),
        capacities=(100, 120, 90),
        demands=(60, 80, 70, 50),
        unit_costs=(
            (4, 6, 9, 5),
            (5, 4, 7, 6),
            (8, 5, 3, 4),
        ),
    )


def test_solution_meets_every_demand_and_respects_capacity() -> None:
    result = solve_transport(small_problem())

    assert result.total_sent_by_origin == (90, 80, 90)
    assert result.total_received_by_destination == (60, 80, 70, 50)
    assert all(sent <= capacity for sent, capacity in zip(result.total_sent_by_origin, small_problem().capacities))


def test_solution_has_expected_minimum_cost() -> None:
    result = solve_transport(small_problem())

    assert result.objective_cost == 1000


def test_insufficient_total_capacity_is_rejected_before_solving() -> None:
    problem = TransportProblem(
        origins=("Only hub",),
        destinations=("Site A", "Site B"),
        capacities=(5,),
        demands=(3, 4),
        unit_costs=((2, 3),),
    )

    try:
        solve_transport(problem)
    except ValueError as error:
        assert "Total capacity" in str(error)
    else:
        raise AssertionError("Expected insufficient capacity to be rejected")


def test_cli_prints_a_reproducible_synthetic_solution() -> None:
    from logistics_challenge.cli import main

    lines = []
    main(lines.append)

    assert lines[0] == "Synthetic transportation optimisation exercise"
    assert "Objective cost: 1000" in lines
    assert "All demand constraints satisfied: True" in lines
    assert "All capacity constraints satisfied: True" in lines
