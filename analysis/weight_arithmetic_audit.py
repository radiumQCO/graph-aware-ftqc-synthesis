"""Audit existing P Hamming-weight circuits; no new compilation algorithm.

Uses the published Qualtran network transcribed in hwp_schedule.py. Verifies
its classical permutation, clean-target four-T AND isometry, and measured
inverse. Comparison numbers are labelled textbook upper bounds, not optima.
Run from the repository: analysis/.venv/Scripts/python.exe analysis/weight_arithmetic_audit.py
"""
import cmath
import hashlib
import json
import math
import random
from collections import Counter
from pathlib import Path

from hwp_schedule import macros_for, schedule

ROOT = Path(__file__).resolve().parent
METHOD = "hwp_global_joint_batch_in_circuit_tower_mixed_diagonal"


def basis_audit(n, patterns):
    ops = macros_for(n)
    k, b = n - n.bit_count(), n.bit_length()
    checks = 0
    for original in patterns:
        state = [(original >> i) & 1 for i in range(n)] + [0] * (k + b)
        initial = state[:]
        for gate, qs in ops:
            if gate == "CNOT":
                a, target = qs
                state[target] ^= state[a]
            else:
                a, c, target = qs
                assert state[target] == 0
                state[target] ^= state[a] & state[c]
        weight = sum(state[n + k + i] << i for i in range(b))
        assert weight == original.bit_count(), (n, original, weight)
        for gate, qs in reversed(ops):
            if gate == "CNOT":
                a, target = qs
                state[target] ^= state[a]
            else:
                a, c, target = qs
                # The controls are restored before the measured AND inverse.
                assert state[target] == (state[a] & state[c])
                state[target] ^= state[a] & state[c]
        assert state == initial
        checks += 1
    return checks


def and_isometry_audit():
    """Independent amplitudes, bit order controls a,b then target t (LSB)."""
    def apply(vec, kind, qs):
        out = [0j] * 8
        for index, amp in enumerate(vec):
            if kind == "CNOT":
                a, target = qs
                out[index ^ ((1 << target) if index & (1 << a) else 0)] += amp
            elif kind == "H":
                q = qs[0]
                base = index & ~(1 << q)
                out[base] += amp / math.sqrt(2)
                out[base | (1 << q)] += amp * (-1 if index & (1 << q) else 1) / math.sqrt(2)
            else:
                q = qs[0]
                angle = {"T": math.pi/4, "TDAG": -math.pi/4, "S": math.pi/2}[kind]
                out[index] += amp * (cmath.exp(1j*angle) if index & (1 << q) else 1)
        return out
    ops = [("H", (0,)), ("T", (0,)),
           ("CNOT", (2, 0)), ("CNOT", (1, 0)),
           ("CNOT", (0, 2)), ("CNOT", (0, 1)),
           ("TDAG", (2,)), ("TDAG", (1,)), ("T", (0,)),
           ("CNOT", (0, 2)), ("CNOT", (0, 1)), ("H", (0,)), ("S", (0,))]
    max_error = 0.0
    for a in (0, 1):
        for b in (0, 1):
            vec = [0j] * 8
            index = 4*a + 2*b
            vec[index] = 1
            for kind, qs in ops:
                vec = apply(vec, kind, qs)
            expected = [0j] * 8
            expected[index + (a & b)] = 1
            max_error = max(max_error, max(abs(v-e) for v,e in zip(vec, expected)))
            vec = apply(vec, "H", (0,))
            for outcome in (0, 1):
                # Projective branch + classically controlled CZ + reset.
                branch = [0j]*8
                for i, amp in enumerate(vec):
                    if i & 1 == outcome:
                        branch[i & ~1] += amp * (-1 if outcome and a and b else 1)
                expected_branch = [0j]*8
                expected_branch[index] = 1/math.sqrt(2)
                max_error = max(max_error, max(abs(v-e) for v,e in zip(branch, expected_branch)))
    assert max_error < 1e-14
    return {"clean_control_basis_cases": 4, "measured_inverse_branches": 8,
            "maximum_amplitude_error": max_error,
            "scope": "Gadget linearity verifies all superpositions; not a physical noise simulation"}


def cut_support_audit(edges):
    """Existing graph properties, constructive witnesses, not a cut algorithm."""
    neighbours = {i: set() for i in range(100)}
    for a, b in edges:
        neighbours[a].add(b); neighbours[b].add(a)
    colors = {0: 0}
    stack = [0]
    while stack:
        a = stack.pop()
        for b in neighbours[a]:
            if b not in colors:
                colors[b] = 1-colors[a]; stack.append(b)
            assert colors[b] != colors[a]
    black = sorted(i for i in colors if colors[i] == 0)
    assert len(black) == 50 and all(len(ns) == 4 for ns in neighbours.values())
    a = black[0]
    white = min(neighbours[a])
    other_black = sorted(set(black) - neighbours[white])
    assert len(other_black) == 46
    def cut(flips):
        return sum((a in flips) != (b in flips) for a, b in edges)
    multiples = set()
    for count in range(101):
        value = cut(set(black[:min(count,50)])) + cut(set(black[:max(0,count-50)]))
        assert value == 4*count
        multiples.add(value)
    offset = set()
    complements = set()
    for count in range(97):
        flips1 = {a, white} | set(other_black[:min(count,46)])
        flips2 = set(black[:max(0,count-46)])
        value = cut(flips1) + cut(flips2)
        assert value == 6+4*count
        offset.add(value)
        complement_value = cut(set(black) ^ flips1) + cut(set(black) ^ flips2)
        assert complement_value == 400-value
        complements.add(complement_value)
    witnessed = multiples | offset | complements
    allowed = set(range(0,401,2)) - {2,398}
    assert witnessed == allowed and len(witnessed) == 199
    return {"witnessed_joint_cut_weights": sorted(witnessed), "number_distinct": 199,
            "output_bits_lower_bound": math.ceil(math.log2(len(witnessed))),
            "exactness_condition": "Evenness + torus min cut 4 + bipartite complement exclude only 2 and 398; proof in report",
            "xor_and_lower_bound_by_black_sublattice_restriction": 100-(100).bit_count()}


def main():
    path = ROOT/"results/paper_counts_proxy.costs.json"
    costs = json.loads(path.read_text(encoding="utf-8"))
    selected = next(x for x in costs["methods"] if x["method"] == METHOD)
    assert selected["t_count"] == min(x["t_count"] for x in costs["methods"] if "t_count" in x)
    data = json.loads((ROOT/"results/paper_counts_proxy.structure.json").read_text(encoding="utf-8"))
    groups = selected["groups"]
    families = []
    for family, count in Counter(g["family"] for g in groups).items():
        g = next(g for g in groups if g["family"] == family)
        n = g["n"]
        assert n in (200,400) and g["and_count"] == n-n.bit_count()
        families.append(dict(family=family,blocks=count,input_bits=n,
            carry_creations_per_block=g["and_count"],carry_creations=count*g["and_count"],
            carry_uncomputations=count*g["and_count"],carry_t_count=4*count*g["and_count"]))
    per_kind = {}
    for kind, n in (("X",200),("ZZ",400)):
        count = sum(x["blocks"] for x in families if x["family"].startswith(kind))
        k, b = n-n.bit_count(), n.bit_length()
        column_counts = [n >> j for j in range(1,b+1)]
        assert sum(column_counts) == k
        hd = schedule(n)
        per_kind[kind] = dict(input_bits=n,blocks=count,weight_bits_allocated=b,
            column_carry_creations=column_counts,carry_creations_per_block=k,
            carry_creations=count*k,carry_uncomputations=count*k,t_count=count*k*4,
            measurement_count=count*k,hwp_scratch=k+b,parity_carriers=n if kind=="ZZ" else 0,
            algorithm_scratch_before_towers=k+b+(n if kind=="ZZ" else 0),
            macro_cnot_compute=count*(5*k+n.bit_count()),
            macro_cnot_uncompute=count*(5*k+n.bit_count()),
            internal_and_cnot_compute=6*count*k,
            conditional_cz_max=count*k,
            outer_hadamards=2*n*count if kind=="X" else 0,
            outer_parity_cnot=4*n*count if kind=="ZZ" else 0,
            per_block_depth=hd,
            total_hwp_t_depth=count*hd["compute_t_depth"],
            total_hwp_primitive_depth=count*(hd["compute_primitive_depth"]+hd["uncompute_primitive_depth"]))
    assert sum(x["carry_creations"] for x in families) == selected["hwp_and_count"] == 59597
    assert sum(x["carry_t_count"] for x in families) == 238388
    rng = random.Random(20261005)
    tested = {str(n): basis_audit(n,range(1<<n)) for n in range(1,13)}
    for n in (200,400):
        patterns = [0,(1<<n)-1] + [(1<<w)-1 for w in range(n+1)]
        patterns += [rng.getrandbits(n) for _ in range(512)]
        tested[str(n)] = basis_audit(n, patterns)
    alternatives = {}
    for n in (200,400):
        b = n.bit_length()
        padded = 1 << (n-1).bit_length()
        log = padded.bit_length()-1
        comparators = padded*log*(log+1)//4
        alternatives[str(n)] = dict(
            textbook_controlled_increment=dict(forward_toffoli=n*(b-1)**2,
                compute_phase_uncompute_toffoli=2*n*(b-1)**2,
                seven_t_unitary_upper=14*n*(b-1)**2,workspace_plus_output=b+max(0,b-2),
                status="Unoptimized textbook ladder; not best ripple-carry implementation"),
            padded_bitonic_sort=dict(padded_width=padded,comparators=comparators,
                comparator_layers=log*(log+1)//2,history_ancillas=comparators,
                compute_phase_unsort_toffoli=4*comparators,
                seven_t_unitary_upper=28*comparators,
                clean_flag_measured_inverse_with_seven_t_fredkin_upper=18*comparators,
                four_t_measurement_assisted_toffoli_upper=12*comparators,
                four_t_variant_parallel_helper_qubits_upper=padded//2,
                status="Standard compare flag + Fredkin; no constant/promise optimization"),
            literal_fourier_counter=dict(counter_bits=b,
                controlled_phase_compute=n*b+b*(b-1)//2,
                controlled_s_gates_compute=n+(b-1),
                controlled_phase_below_s_compute=n*(b-2)+(b-1)*(b-2)//2,
                status="Compute-only Fourier preparation+inverse QFT; twice for phase sandwich, not FT T count"))
    gadget = and_isometry_audit()
    for n_key, entry in alternatives.items():
        fourier = entry["literal_fourier_counter"]
        assert fourier["controlled_phase_compute"] == (
            int(n_key) + fourier["controlled_s_gates_compute"]
            + fourier["controlled_phase_below_s_compute"])
    result = dict(schema_version=1,case=data["case"],selected_method=METHOD,
        baseline_cost_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        baseline_expected_total_t=selected["t_count"],baseline_maximum_total_t=selected["t_count_branch_maximum"],
        families=families,by_kind=per_kind,carry_total_t=238388,carry_total_and=59597,
        carry_uncompute_t=0,exact_xor_and_lower_bounds=dict(x_per_fresh_oracle=197,
            arbitrary_400_bit_hw_per_fresh_oracle=397,restricted_joint_cut_proven_lower=97,
            scope="NOT a universal Clifford+T or full-program lower bound"),
        cut_support=cut_support_audit(data["edges"]),textbook_comparison_bounds=alternatives,
        verification=dict(basis_cases_by_size=tested,basis_cases=sum(tested.values()),temporary_and=gadget))
    target = ROOT/"results/weight_arithmetic_audit.json"
    target.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps({"carry_t":result["carry_total_t"],"by_kind_t":{k:v["t_count"] for k,v in per_kind.items()},
                      "basis_cases":result["verification"]["basis_cases"],"and_max_error":gadget["maximum_amplitude_error"],
                      "joint_cut_support":result["cut_support"]["number_distinct"],"output":str(target)},indent=2))


if __name__ == "__main__":
    main()
