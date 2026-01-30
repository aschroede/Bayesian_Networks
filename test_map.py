import json
from pathlib import Path

import pytest
from map import MAP
from read_bayesnet import BayesNet


DATA_DIR = Path(__file__).parent / "data"
NETWORK_DIR = Path(__file__).parent / "Networks"


def load_test_cases():
    """Flatten (network, query) pairs into pytest parameters."""
    with open(DATA_DIR / "queries.json") as f:
        queries_data = json.load(f)

    with open(DATA_DIR / "answers.json") as f:
        answers_data = json.load(f)

    test_cases = []

    for net in queries_data["networks"]:
        net_name = net["name"]
        net_file = NETWORK_DIR / net["file"]

        for q in net["queries"]:
            q_name = q["name"]

            expected = answers_data[net_name][q_name]

            test_cases.append(
                pytest.param(
                    net_file,
                    q,
                    expected,
                    id=f"{net_name}::{q_name}",
                )
            )

    return test_cases


@pytest.mark.parametrize(
    "network_file,query,expected",
    load_test_cases()
)
def test_map_query(network_file, query, expected):
    """
    Runs a MAP query using student code and compares
    against the pgmpy-generated oracle result.
    """

    # Values must be cleared each time since they are static
    BayesNet.values.clear()
    BayesNet.probabilities.clear()
    BayesNet.parents.clear()

    net = BayesNet(network_file)
    map = MAP(net)
    result = map.run(query["map_vars"], query.get("evidence", {}), elim_heuristic=None)

    assert isinstance(result, dict), "map_query must return a dict"

    assert result == expected, (
        f"MAP result incorrect.\n"
        f"Expected: {expected}\n"
        f"Got: {result}"
    )
