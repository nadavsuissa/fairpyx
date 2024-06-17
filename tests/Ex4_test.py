import pytest
import random
# Nadav Suissa

from fairpyx.algorithms.Ex4 import (
    find_proportional_allocation,
    allocate_minimal_bundles,
    bundle_is_minimal,
    total_value,
    is_envy_free,
    is_pareto_optimal,
)


@pytest.fixture
def example_instance():
    return {
        "agents": ["Alice", "Bob", "Charlie"],
        "items": {
            "Alice": {"A": 40, "B": 35, "C": 25},
            "Bob": {"A": 35, "B": 40, "C": 25},
            "Charlie": {"A": 40, "B": 25, "C": 35}
        },
        "rankings": {
            "Alice": [["A"], ["B"], ["C"]],
            "Bob": [["B"], ["A"], ["C"]],
            "Charlie": [["A"], ["C"], ["B"]]
        }
    }


def test_find_proportional_allocation(example_instance):
    allocation = find_proportional_allocation(example_instance)
    assert allocation == {'Alice': ['A'], 'Bob': ['B'], 'Charlie': ['C']}


def test_allocate_minimal_bundles(example_instance):
    allocation = allocate_minimal_bundles(example_instance)
    assert allocation == {'Alice': ['A'], 'Bob': ['B'], 'Charlie': ['C']}


def test_bundle_is_minimal(example_instance):
    minimal = bundle_is_minimal(example_instance)
    expected = {
        'Alice': {'A': True, 'B': True, 'C': True},
        'Bob': {'A': True, 'B': True, 'C': True},
        'Charlie': {'A': True, 'B': True, 'C': True}
    }
    assert minimal == expected


def test_total_value():
    instance = {
        "bundle": ['A'],
        "player": "Alice",
        "items": {
            "Alice": {"A": 40, "B": 35, "C": 25},
            "Bob": {"A": 35, "B": 40, "C": 25},
            "Charlie": {"A": 40, "B": 25, "C": 35}
        }
    }
    value = total_value(instance)
    assert value == 40


def test_is_envy_free():
    instance = {
        "allocation": {'Alice': ['A'], 'Bob': ['B'], 'Charlie': ['C']},
        "agents": ["Alice", "Bob", "Charlie"],
        "items": {
            "Alice": {"A": 40, "B": 35, "C": 25},
            "Bob": {"A": 35, "B": 40, "C": 25},
            "Charlie": {"A": 40, "B": 25, "C": 35}
        },
        "rankings": {
            "Alice": [["A"], ["B"], ["C"]],
            "Bob": [["B"], ["A"], ["C"]],
            "Charlie": [["A"], ["C"], ["B"]]
        }
    }
    assert is_envy_free(instance)


def test_is_pareto_optimal():
    instance = {
        "allocation": {'Alice': ['A'], 'Bob': ['B'], 'Charlie': ['C']},
        "agents": ["Alice", "Bob", "Charlie"],
        "items": {
            "Alice": {"A": 40, "B": 35, "C": 25},
            "Bob": {"A": 35, "B": 40, "C": 25},
            "Charlie": {"A": 40, "B": 25, "C": 35}
        }
    }
    assert is_pareto_optimal(instance)





if __name__ == "__main__":
    pytest.main()
