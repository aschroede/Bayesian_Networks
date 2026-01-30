import json
from pathlib import Path
from pgmpy.readwrite import BIFReader
from pgmpy.inference import VariableElimination

# NOTE You shouldn't change any code in this file. It is only for testing your implementation. See the README for details.

def solve_queries(query_file, output_file):
    query_file = Path(query_file)
    output_file = Path(output_file)

    with open(query_file, "r") as f:
        query_data = json.load(f)

    answers = {}

    for net in query_data["networks"]:
        net_name = net["name"]
        bif_path = query_file.parent.parent / "Networks" / net["file"]
        print(str(bif_path))

        print(f"Loading network: {net_name} ({bif_path})")

        reader = BIFReader(str(bif_path))
        model = reader.get_model()

        infer = VariableElimination(model)
        answers[net_name] = {}

        for q in net["queries"]:
            q_name = q["name"]
            map_vars = q["map_vars"]
            evidence = q.get("evidence", {})

            print(f"  Solving {q_name}")

            result = infer.map_query(
                variables=map_vars,
                evidence=evidence,
                show_progress=False
            )

            # pgmpy returns a dict: {var: state}
            answers[net_name][q_name] = result

    with open(output_file, "w") as f:
        json.dump(answers, f, indent=2)

    print(f"\nAnswers written to {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate MAP answers using pgmpy")
    parser.add_argument("queries", help="Path to queries.json")
    parser.add_argument("answers", help="Path to output answers.json")

    args = parser.parse_args()

    solve_queries(args.queries, args.answers)
