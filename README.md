# Synthetic transportation optimisation exercise

A small, deterministic linear-programming exercise for learning the transportation problem. **Every name, capacity, demand, and cost in this repository is fictional.** It is not a production planning tool and must not be used with real customer, shipment, location, pricing, or operational data.

## Model

For each origin `i` and destination `j`, the non-negative integer decision variable `x[i,j]` is the number of fictional units shipped. The model minimises:

```text
sum(unit_cost[i,j] * x[i,j])
```

subject to:

- each origin ships no more than its synthetic capacity;
- each destination receives exactly its synthetic demand;
- shipments are non-negative integers.

The bundled instance has three fictional hubs, four fictional clinics, total demand of 260 units, and total capacity of 310 units. Its deterministic optimum is an objective cost of `1000`.

## Solver and reproducibility

The project pins [PuLP 2.8.0](https://coin-or.github.io/pulp/) and uses its CBC command-line solver with solver output disabled. Inputs live in `logistics_challenge/cli.py`; no randomisation, files, network calls, or external services are used. Running the same dependency versions produces the same model and objective.

## Run

Requires Python 3.11 or later.

```bash
python -m venv .venv
# Windows Git Bash:
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m logistics_challenge.cli
```

Expected smoke-test lines include:

```text
Objective cost: 1000
All demand constraints satisfied: True
All capacity constraints satisfied: True
```

## Tests

The test suite verifies that the solved plan satisfies every demand, never exceeds an origin capacity, produces the expected minimum objective, rejects clearly infeasible capacity, and prints a reproducible CLI summary.

## Limits and non-goals

This intentionally omits real-world concerns such as time windows, vehicle routing, multiple transport modes, uncertainty, service levels, emissions, security controls, and operational data validation. It is an educational transportation LP—not a production optimiser, recommendation system, or deployment template.

See [SECURITY.md](SECURITY.md) for the data and disclosure policy.
