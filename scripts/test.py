#!/usr/bin/env python3
"""Validate a graph spec JSON against the PROMPT.md output contract.

Usage: python3 test.py graph.json   (or pipe agent output via stdin;
the first ```json fenced block is extracted automatically)
"""
import json
import re
import sys

TYPES = {"agent", "validator", "merge", "human"}


def extract_json(text):
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    return json.loads(m.group(1) if m else text)


def validate(g):
    nodes = {n["id"]: n for n in g["nodes"]}
    assert len(nodes) == len(g["nodes"]), "duplicate node ids"
    for n in g["nodes"]:
        assert n["type"] in TYPES, f"bad type: {n['type']}"
        assert n.get("role") and n.get("prompt"), f"{n['id']}: missing role/prompt"
        if n["type"] == "validator":
            of = n.get("on_fail")
            assert of and "retry" in of and "then" in of, f"{n['id']}: validator missing on_fail"
            assert of["then"] == "abort" or of["then"] in nodes, f"{n['id']}: on_fail.then unknown"

    incoming, outgoing = {i: 0 for i in nodes}, {i: 0 for i in nodes}
    for e in g["edges"]:
        assert e["from"] in nodes and e["to"] in nodes, f"edge refs unknown node: {e}"
        outs = nodes[e["from"]].get("outputs", [])
        for a in e.get("carries", []):
            assert a in outs, f"edge {e['from']}->{e['to']} carries '{a}' not in outputs {outs}"
        incoming[e["to"]] += 1
        outgoing[e["from"]] += 1

    for i in g["entry"]:
        assert incoming[i] == 0, f"entry {i} has incoming edges"
    for i in g["exit"]:
        assert outgoing[i] == 0, f"exit {i} has outgoing edges"

    # Kahn: DAG check
    deg = dict(incoming)
    queue = [i for i, d in deg.items() if d == 0]
    seen = 0
    while queue:
        cur = queue.pop()
        seen += 1
        for e in g["edges"]:
            if e["from"] == cur:
                deg[e["to"]] -= 1
                if deg[e["to"]] == 0:
                    queue.append(e["to"])
    assert seen == len(nodes), "cycle detected"
    return len(nodes), len(g["edges"])


if __name__ == "__main__":
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    n, e = validate(extract_json(text))
    print(f"OK: {n} nodes, {e} edges, valid DAG")
