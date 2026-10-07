"""Reconstruct paper-count proxy and literal archived Q# notebook separately.

No QEC algorithm is implemented. Angles use R_P(theta)=exp(-i theta P/2).
The paper does not fix J,g,dt or a boundary circuit. Its numeric completion
below is explicitly conditional, not the recovered original experiment.
"""
import csv
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
GAMMA = 1 / (4 - 4 ** (1 / 3))

def edge_groups(side, periodic):
    def index(r, c):
        return r * side + (c if r % 2 == 0 else side - 1 - c)
    groups = []
    for direction in ("horizontal", "vertical"):
        for parity in (0, 1):
            edges = []
            stop = side if periodic else side - 1
            for i in range(side):
                for j in range(parity, stop, 2):
                    if direction == "horizontal":
                        edges.append((index(i, j), index(i, (j + 1) % side)))
                    else:
                        edges.append((index(j, i), index((j + 1) % side, i)))
            assert len(set(q for e in edges for q in e)) == 2 * len(edges)
            groups.append(edges)
    return groups

def layers(steps, field_scale, coupling_scale, dt):
    # Expand five Strang substeps and merge ONLY adjacent identical generators.
    raw = []
    for _ in range(steps):
        for c in (GAMMA, GAMMA, 1 - 4 * GAMMA, GAMMA, GAMMA):
            raw.extend([("X", c / 2), ("ZZ", c), ("X", c / 2)])
    merged = []
    for kind, c in raw:
        if merged and merged[-1]["pauli"] == kind:
            merged[-1]["coefficient"] += c
        else:
            merged.append({"pauli": kind, "coefficient": c})
    for i, layer in enumerate(merged):
        c = layer["coefficient"]
        if layer["pauli"] == "X":
            family = "X_boundary" if math.isclose(c, GAMMA / 2) else "X_common" if math.isclose(c, GAMMA) else "X_mixed"
            scale = field_scale
        else:
            family = "ZZ_common" if math.isclose(c, GAMMA) else "ZZ_central"
            scale = coupling_scale
        layer.update(index=i, family=family, theta_radians=2 * scale * dt * c)
    return merged

def gf2_rank(rows):
    basis = {}
    for row in rows:
        while row:
            b = row.bit_length() - 1
            if b in basis:
                row ^= basis[b]
            else:
                basis[b] = row
                break
    return len(basis)

def reconstruct(name, steps, periodic, notebook_signs):
    n = 100
    edges = edge_groups(10, periodic)
    all_edges = [e for g in edges for e in g]
    assert len(set(tuple(sorted(e)) for e in all_edges)) == len(all_edges)
    seq = layers(steps, -1 if notebook_signs else 1, 1 if notebook_signs else -1, 0.25)
    rotations = []
    counts = Counter()
    last_x = {}
    last_zz = {q: [] for q in range(n)}
    for layer in seq:
        is_x = layer["pauli"] == "X"
        supports = [(q,) for q in range(n)] if is_x else all_edges
        new_zz = {q: [] for q in range(n)}
        for support in supports:
            rid = len(rotations)
            deps = sorted(set(d for q in support for d in (last_zz[q] if is_x else [last_x[q]]))) if rotations else []
            record = dict(id=rid, layer=layer["index"], pauli=layer["pauli"],
                          support=" ".join(map(str, support)), family=layer["family"],
                          theta_radians=layer["theta_radians"], predecessors=" ".join(map(str, deps)))
            rotations.append(record)
            if is_x:
                last_x[support[0]] = rid
            else:
                for q in support:
                    new_zz[q].append(rid)
            counts[layer["family"]] += 1
        if not is_x:
            last_zz = new_zz
    degrees = Counter(q for e in all_edges for q in e)
    data = {
        "case": name, "instances": 2, "work_qubits_per_instance": n,
        "steps": steps, "dt": 0.25, "evolution_time": steps * 0.25,
        "numeric_parameters_status": "literal notebook" if notebook_signs else "CONDITIONAL completion: J=g=1, dt=0.25; paper does not specify",
        "boundary": "periodic COUNTS PROXY, not recovered" if periodic else "open, recovered from notebook loops",
        "effective_hamiltonian": "-sum X + sum ZZ" if notebook_signs else "+sum X - sum ZZ",
        "edge_group_sizes": [len(g) for g in edges], "edges": all_edges,
        "edge_parity_rank_gf2": gf2_rank([(1 << a) | (1 << b) for a,b in all_edges]),
        "all_degrees_even": all(d % 2 == 0 for d in degrees.values()),
        "commuting_blocks_per_instance": len(seq),
        "rotation_layers_per_instance": sum(1 if l["pauli"] == "X" else 4 for l in seq),
        "rotations_per_instance": len(rotations), "batch_rotations": 2 * len(rotations),
        "angle_families": [{"family": family, "theta_radians": next(l["theta_radians"] for l in seq if l["family"] == family),
                            "multiplicity_per_instance": count, "batch_multiplicity": 2*count}
                           for family,count in counts.items()],
        "layers": seq,
        "dependency_edges_per_instance": sum(len(r["predecessors"].split()) for r in rotations),
    }
    (OUT / f"{name}.structure.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    with (OUT / f"{name}.rotations.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rotations[0]))
        writer.writeheader()
        writer.writerows(rotations)
    return data

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cases = [reconstruct("paper_counts_proxy", 20, True, False),
             reconstruct("notebook_literal", 80, False, True)]
    for c in cases:
        print(json.dumps({k:c[k] for k in ("case", "batch_rotations", "rotation_layers_per_instance", "edge_group_sizes", "angle_families")}, indent=2))

if __name__ == "__main__":
    main()
