"""Restore the existing conditional P workload; no new quantum optimization.

Reuse verified graph arithmetic, the old X counter, and cached positive mixtures.
Expand phase catalysis via the standard majority identity, checked in verify.py.
All timestamps belong to a separate, explicitly conditional resource model.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANALYSIS = HERE.parent
sys.path.insert(0, str(ANALYSIS))
sys.path.insert(0, str(ANALYSIS / 'graph_cut_phase'))
from circuits import generic, grid_plaquettes, metrics
from scaling import grid
from hwp_schedule import macros_for

METHOD = 'hwp_global_joint_batch_in_circuit_tower_mixed_diagonal'
SEED = 20261006


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_inputs():
    files = {
        'structure': ANALYSIS / 'results/paper_counts_proxy.structure.json',
        'costs': ANALYSIS / 'results/paper_counts_proxy.costs.json',
        'synthesis': ANALYSIS / 'results/synthesis_cache.json',
        'delivery': ANALYSIS / 'results/delivered_benchmark.json',
        'factory': ANALYSIS / 'results/factory_audit.json',
        'graph_circuits': ANALYSIS / 'graph_cut_phase/circuits.json.gz',
        'graph_verification': ANALYSIS / 'graph_cut_phase/artifact_verification.json',
    }
    data = {k: json.loads(p.read_text()) for k, p in files.items() if k != 'graph_circuits'}
    data['selected'] = next(m for m in data['costs']['methods'] if m['method'] == METHOD)
    data['manifest'] = {k: {'path': str(p.relative_to(ANALYSIS.parent)), 'sha256': sha(p)} for k, p in files.items()}
    return data


def find_mixture(cache, theta, delta):
    # Match existing compiled records, never regenerate or relax synthesis.
    candidates = [v for k, v in cache.items() if k.startswith('MIX|')
                  and abs(float(v['theta']) - theta) < 1e-11
                  and abs(float(v['delta']) - delta) < 1e-14]
    assert len(candidates) == 1, (theta, delta, len(candidates))
    return candidates[0]


def rotation_program(cache, record, rng, q, label):
    branch = 0 if rng.random() < float(record['probability_first']) else 1
    twirl = rng.randrange(4)
    before = [[], [('S', (q,))], [('SDAG', (q,))], [('Z', (q,))]][twirl]
    after = [[], [('SDAG', (q,))], [('S', (q,))], [('Z', (q,))]][twirl]
    raw = cache[record['branch_keys'][branch]]
    # Gridsynth writes matrix products; execution order is the reversed string.
    ops = before + [(g, (q,)) for g in reversed(raw['gates']) if g != 'W'] + after
    info = {'label': label, 'q': q, 'theta': record['theta'], 'delta': record['delta'],
            'mixture_branch': branch, 'twirl': twirl, 'branch_key': record['branch_keys'][branch],
            'T_actual': raw['t_count'], 'T_expected': record['t_count'],
            'T_branch_max': record['branch_max_t_count'], 'diamond_bound': record['measured_diamond']}
    return ops, info


def catalysis_prefix(x, y, c, t):
    """Standard one-layer generalized phase catalysis, clean AND target.

    After c ^= x ^ y, t = majority(x,y,c) = x ^ ((x^y)&(x^c)).
    Apply P(2 theta) to t, then the suffix. The initial catalyst P(theta)|+>
    supplies P(theta) to x,y and returns unchanged. Prefix XORs on c persist.
    """
    # Canonical Clifford cancellation: do not restore controls before the seed;
    # the two x->c gates cancel. This is the existing six-CNOT CT primitive.
    return [('CNOT', (y, c)), ('CNOT', (x, y)), ('AND', (y, c, t)), ('CNOT', (x, t))]


def catalysis_suffix(x, y, c, t):
    return [('CNOT', (x, t)), ('UNAND', (y, c, t)), ('CNOT', (x, c)), ('CNOT', (x, y))]


def tower(weights, bank, seed_ops):
    assert len(weights) == 8 and len(bank) == 17
    catalysts, targets, unused = bank[:8], bank[8:16], bank[16]
    def recurse(j, x, y):
        prefix = catalysis_prefix(x, y, catalysts[j], targets[j])
        middle = seed_ops if j == 7 else recurse(j + 1, targets[j], weights[j + 1])
        return prefix + middle + catalysis_suffix(x, y, catalysts[j], targets[j])
    # The unused partner is |0>, acquires only an irrelevant global Rz phase.
    return recurse(0, weights[0], unused)


def x_arithmetic():
    n = 200; k = 197; b = 8
    wires = list(range(200)) + list(range(600, 600 + k + b))
    compute = [(g, tuple(wires[q] for q in qs)) for g, qs in macros_for(n)]
    undo = [('CNOT' if g == 'CNOT' else 'UNAND', qs) for g, qs in reversed(compute)]
    assert sum(g == 'AND' for g, _ in compute) == 197
    return compute, undo, wires[n+k:], 205


def graph_arithmetic(variant):
    edges, faces = grid(10, 10, periodic=True, copies=2)
    circuit = generic(200, edges, True, True, True) if variant == 'A' else grid_plaquettes(200, edges, faces, True, True, True)
    def snake(q):
        if q >= 200: return q
        copy, i = divmod(q, 100); r, c = divmod(i, 10)
        return 100*copy + 10*r + (c if r % 2 == 0 else 9-c)
    compute = [(g, tuple(snake(q) for q in qs)) for g, qs in circuit.compute if g != 'AND_ZERO']
    undo = [('UNAND' if g == 'AND' else g, qs) for g, qs in reversed(compute)]
    phases = sorted((coefficient, qs[0]) for _, qs, coefficient in circuit.phases)
    assert [a for a, _ in phases] == [2**j for j in range(1, 9)]
    assert metrics(circuit)['AND_compute'] == (396 if variant == 'A' else 297)
    return compute, undo, [q for _, q in phases], circuit.width-200, circuit, metrics(circuit)


def build(variant, inputs):
    rng = random.Random(SEED)  # Same rotation branches and twirls in A and B.
    structure, cache, selected = inputs['structure'], inputs['synthesis'], inputs['selected']
    families = sorted({g['family'] for g in selected['groups']})
    banks = {f: list(range(1006+17*i, 1006+17*(i+1))) for i, f in enumerate(families)}
    assert len(banks) == 5 and max(q for bank in banks.values() for q in bank) == 1090
    angles = {x['family']: x['theta_radians'] for x in structure['angle_families']}
    rotations, startup = [], []
    for family in families:
        base = angles[family]*(2 if family.startswith('ZZ') else 1)
        for j, q in enumerate(banks[family][:8]):
            mix = find_mixture(cache, base*2**j, (.002/3)/(2*40))
            ops, info = rotation_program(cache, mix, rng, q, f'catalyst:{family}:{j}')
            startup.extend([('H', (q,))] + ops); rotations.append(info)
    xc, xu, xw, xa = x_arithmetic()
    zc, zu, zw, za, graph, graph_metrics = graph_arithmetic(variant)
    blocks = [{'id': -1, 'family': 'startup', 'segments': [startup], 'arithmetic_ancillas': 0, 'tower_scratch': 0}]
    for group in selected['groups']:
        isx = group['pauli'] == 'X'; family = group['family']; bank = banks[family]
        base = angles[family]*(1 if isx else 2)
        mix = find_mixture(cache, base*2**8, (.002/3)/(2*201))
        seed_ops, info = rotation_program(cache, mix, rng, bank[15], f'seed:{group["layer"]}:{family}')
        rotations.append(info)
        outer = [('H', (q,)) for q in range(200)] if isx else []
        compute, undo, weights = (xc, xu, xw) if isx else (zc, zu, zw)
        blocks.append({'id': group['layer'], 'family': family, 'pauli': group['pauli'],
                       'segments': [outer+compute, tower(weights, bank, seed_ops), undo+list(reversed(outer))],
                       'arithmetic_ancillas': xa if isx else za, 'tower_scratch': 9})
    counts = Counter(g for block in blocks for seg in block['segments'] for g, _ in seg)
    hwp = 19897 + (39600 if variant == 'A' else 29700)
    assert counts['AND'] == counts['UNAND'] == hwp+1608
    assert counts['T'] == sum(r['T_actual'] for r in rotations)
    expected = sum(r['T_expected'] for r in rotations)
    assert abs(expected - (selected['t_count']-4*(59597+1608))) < 1e-7
    assert abs(sum(r['diamond_bound'] for r in rotations)-selected['full_diamond_synthesis_bound']) < 1e-14
    ledger = {'variant': variant, 'hwp_AND': hwp, 'X_AND': 19897,
              'ZZ_AND': 39600 if variant == 'A' else 29700, 'tower_AND': 1608,
              'total_AND': counts['AND'], 'total_CCZ': counts['AND'],
              'T_synthesis_sampled': counts['T'], 'T_synthesis_expected': expected,
              'T_synthesis_branch_maximum': sum(r['T_branch_max'] for r in rotations),
              'weighted_phase_occurrences': 1608, 'synthesized_rotation_calls': len(rotations),
              'seed_calls': 201, 'catalyst_preparations': 40,
              'catalyst_logical_qubits': 40, 'tower_bank_reserved_qubits': 85,
              'peak_compilation_ancillas': max(xa,za)+85,
              'peak_compilation_logical_qubits': 200+max(xa,za)+85,
              'logical_capacity_reserved': 1091, 'macro_counts': dict(counts),
              'graph_block': graph_metrics, 'synthesis_diamond_bound': sum(r['diamond_bound'] for r in rotations),
              'allocated_synthesis_budget': .002/3, 'arithmetic_phase_exact': True,
              'full_product_formula_exact_with_ideal_angles': 'compositional proof; not 2^200 statevector simulation',
              'synthesis_contract': 'cached positive independent mixtures; averaged channel, not every branch exact',
              'factory_resource_choice': 'same admitted clean-AND CCZ injection for HWP AND and tower AND in A/B',
              'all_phase_interfaces_expanded': True, 'blocks': len(blocks)-1}
    return {'blocks': blocks, 'ledger': ledger, 'rotations': rotations, 'banks': banks}


def write_workloads(inputs, programs):
    payload = {'status': 'FULL_CONDITIONAL_P_LOGICAL_TRACE_NO_UNTIMED_PHASE_WINDOWS',
               'manifest': inputs['manifest'], 'random_seed': SEED, 'variants': programs}
    target = HERE/'workloads.json.gz'
    with target.open('wb') as f:
        f.write(gzip.compress(json.dumps(payload, separators=(',', ':')).encode(), mtime=0))
    return sha(target)


if __name__ == '__main__':
    inp = read_inputs(); programs = {v: build(v, inp) for v in ('A','B')}
    digest = write_workloads(inp, programs)
    print(json.dumps({'trace_sha256': digest, 'ledgers': {v:p['ledger'] for v,p in programs.items()}}, indent=2))
