"""Accounting of existing factories. Never a new quantum protocol or accuracy MC.

Published density-matrix equations are evaluated with NumPy instead of mpmath.
The quantum operation order, noise probabilities, and distances are unchanged.
Cultivation uses the published S-proxy circuit and an explicitly fixed final
acceptance; the sample only measures early rejection, not rare logical errors.
"""
import argparse
import collections
import hashlib
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "sources" / "factories"


def distillation_audit(scan=False):
    import numpy as np
    from mpmath import mp
    mp.dps = 40
    sys.path.insert(0, str(SRC / "litinski" / "Python"))
    import definitions as d
    # Independent check of the numerical adapter against the published primitive.
    axis = [d.z, d.one, d.z, d.one]
    ref = d.apply_rot(d.kron(*([d.plusstate] * 4)), axis, mp.mpf('.003'), mp.mpf('.001'), mp.mpf('.002'))

    class Dense(np.matrix):
        def transpose_conj(self):
            return self.H

    def matrix(x):
        return Dense([[complex(x[i, j]) for j in range(x.cols)] for i in range(x.rows)])

    def kron(*args):
        out = Dense([[1.0 + 0j]])
        for arg in args:
            out = Dense(np.asarray(np.kron(out, arg)))
        return out

    def rotation(state, axis, p1, p2, p3):
        p1, p2, p3 = map(float, (p1, p2, p3))
        p = np.asarray(kron(*axis))
        rho = np.asarray(state)
        out = np.zeros_like(rho)
        for probability, angle in [(1-p1-p2-p3, math.pi/8), (p1, 5*math.pi/8), (p2, -math.pi/8), (p3, 3*math.pi/8)]:
            u = math.cos(angle)*np.eye(len(p)) + 1j*math.sin(angle)*p
            out += probability * (u @ rho @ u.conj().T)
        return Dense(out)

    def pauli(state, axis, probability):
        p = np.asarray(kron(*axis))
        rho = np.asarray(state)
        probability = float(probability)
        return Dense((1-probability)*rho + probability*(p @ rho @ p))

    converted_axis = [matrix(a) for a in axis]
    adapter_error = float(np.max(np.abs(np.asarray(rotation(matrix(d.kron(*([d.plusstate]*4))), converted_axis, .003, .001, .002)) - np.asarray(matrix(ref)))))
    assert adapter_error < 1e-13
    for key, value in list(vars(d).items()):
        if isinstance(value, mp.matrix):
            setattr(d, key, matrix(value))
    d.kron, d.apply_rot, d.apply_pauli = kron, rotation, pauli
    d.trace = lambda x: np.trace(np.asarray(x))
    import onelevel15to1 as l1
    import twolevel20to4 as m2
    import smallfootprint as sf
    os.environ['PYTHONBREAKPOINT'] = '0'  # Pinned public source contains a debugging breakpoint.
    captures = {}

    def profile(frame, event, arg):
        if event == 'return' and frame.f_code.co_name in ('cost_of_two_level_20to4', 'cost_of_two_level_15to1_small_footprint'):
            captures[frame.f_code.co_name] = {key: float(frame.f_locals[key]) for key in ('pfail', 'pfail2', 'pl1', 'l1time') if key in frame.f_locals}

    sys.setprofile(profile)
    try:
        a = m2.cost_of_two_level_20to4(.001, 13, 5, 5, 23, 11, 13, 6)
        b = sf.cost_of_two_level_15to1_small_footprint(.001, 9, 5, 5, 21, 9, 11)
    finally:
        sys.setprofile(None)
    rows = {}
    for label, factory, capture, regions, raw_per_batch in [
        ('M2_15_to_20', a, captures['cost_of_two_level_20to4'], {'L1_core': 15564, 'L2_core': 17250, 'internal_transfer_and_ancillas': 10530}, 300),
        ('small_15_to_15', b, captures['cost_of_two_level_15to1_small_footprint'], {'L1_core': 1586, 'L2_core': 4788, 'internal_transfer_and_ancillas': 1408}, 225),
    ]:
        q = factory.qubits
        assert sum(regions.values()) == q
        cycles = factory.distillation_time_in_cycles
        outputs = factory.n_t_gates_produced_per_distillation
        rows[label] = {
            'physical_qubits_including_measurement_ancillas': q,
            'expected_cycles_per_accepted_batch': cycles, 'outputs_per_batch': outputs,
            'published_equations_output_error_proxy': factory.distilled_magic_state_error_rate,
            **capture,
            'raw_T_equivalent_per_output_no_retry': raw_per_batch/outputs,
            'raw_T_equivalent_per_output_with_retry': raw_per_batch/outputs/(1-capture['pfail'])/(1-capture['pfail2']),
            'qubitcycles_per_output': q*cycles/outputs,
            'regions': {key: {'qubits': val, 'percent_reserved_factory_volume': 100*val/q, 'qubitcycles_per_output': val*cycles/outputs} for key, val in regions.items()},
        }
    result = {'numerical_adapter_max_error': adapter_error, 'method': 'published logical-Pauli channel equations, double precision; not circuit-level validation', 'factories': rows}
    if scan:
        candidates = []
        sys.setprofile(profile)
        try:
            for dx2 in (19,21,23):
                for dz2 in (7,9,11):
                    for dm2 in (11,13):
                        for nl1 in (4,6):
                            f = m2.cost_of_two_level_20to4(.001,13,5,5,dx2,dz2,dm2,nl1)
                            c = captures['cost_of_two_level_20to4']
                            candidates.append({'distances': [13,5,5,dx2,dz2,dm2,nl1], 'qubits': f.qubits, 'expected_cycles_per_accepted_batch': f.distillation_time_in_cycles, 'output_error_proxy': f.distilled_magic_state_error_rate, 'qubitcycles_per_output': f.qubits*f.distillation_time_in_cycles/4, **c})
        finally:
            sys.setprofile(None)
        result['limited_existing_parameter_scan'] = candidates
        target = .002/3/253617/2  # Explicit reserve: at least half remains for delivery.
        admitted = [r for r in candidates if 0 < r['output_error_proxy'] <= target]
        best = min(admitted, key=lambda r:r['qubitcycles_per_output']).copy()
        dx,dz,dm,dx2,dz2,dm2,nl1 = best['distances']
        q1 = nl1*2*((dx+4*dz)*3*dx+2*dm)
        q2 = 2*(4*dx2+3*dz2)*3*dx2
        regions = {'L1_core':q1,'L2_core':q2,'internal_transfer_and_ancillas':best['qubits']-q1-q2}
        best['produced_error_limit_with_half_delivery_reserve'] = target
        best['scan_scope'] = '36 points, L1 fixed (13,5,5); not global factory optimum'
        best['regions'] = {key:{'qubits':val,'percent_reserved_factory_volume':100*val/best['qubits'],'qubitcycles_per_output':val*best['expected_cycles_per_accepted_batch']/4} for key,val in regions.items()}
        best['whole_demand_intrinsic_qubitseconds_400ns_cycle'] = best['qubitcycles_per_output']*253617*400e-9
        best['relative_intrinsic_volume_reduction_from_original_M2'] = 1-best['qubitcycles_per_output']/rows['M2_15_to_20']['qubitcycles_per_output']
        result['best_within_limited_scan'] = best
    return result


def cultivation_audit(shots):
    import numpy as np
    import stim
    sys.path.insert(0, str(SRC / 'gsj' / 'src'))
    import cultiv
    import gen
    from cultiv.make_lifetime_plot import circuit_to_layers
    clean = cultiv.make_end2end_cultivation_circuit(dcolor=5, dsurface=15, basis='Y', r_growing=5, r_end=10, inject_style='unitary')
    circuit = gen.NoiseModel.uniform_depolarizing(.001).noisy_circuit_skipping_mpp_boundaries(clean)
    (ROOT / 'results' / 'factory_gsj_d5_s_proxy.stim').write_text(str(circuit), encoding='utf-8')
    layers = circuit_to_layers(circuit)
    # Ideal terminal observable/stabilizer readout is a simulation boundary.
    assert any(inst.name == 'MPP' for inst in layers[-1])
    terminal_physical = stim.Circuit()
    for inst in layers[-1]:
        if inst.name == 'MPP':
            break
        terminal_physical.append(inst)
    physical_layers = layers[:-1] + [terminal_physical]
    # Check actual source layering rather than guessing figure-label alignment.
    assert len(physical_layers) == 25, len(physical_layers)
    selected = set()
    for det, coord in circuit.get_detector_coordinates().items():
        if len(coord) == 3 or coord[-1] == -9 or (len(coord)>4 and coord[4] in (0,4)):
            selected.add(det)
    q_active, used = [], set()
    layer_counts = []
    for layer in physical_layers:
        counts = collections.Counter()
        for inst in layer:
            if inst.name in ('R','RX'):
                used.update(t.qubit_value for t in inst.targets_copy() if t.is_qubit_target)
            if inst.name in ('S','S_DAG'):
                counts['raw_T_equivalent_proxy_gates'] += len(inst.targets_copy())
            if inst.name == 'CX':
                counts['CX_pairs'] += sum(t.is_qubit_target for t in inst.targets_copy())//2
            if inst.name in ('M','MX','MR','MRX'):
                counts['physical_measurements'] += len(inst.targets_copy())
        q_active.append(len(used))
        layer_counts.append(dict(counts))
    sim = stim.FlipSimulator(batch_size=1024, num_qubits=circuit.num_qubits, seed=20261006)
    entering = np.zeros(len(physical_layers), dtype=np.int64)
    exiting = np.zeros_like(entering)
    assert shots % 1024 == 0
    for _ in range(shots//1024):
        sim.clear()
        survivor = np.ones(1024, dtype=np.bool_)
        next_det = 0
        for k, layer in enumerate(physical_layers):
            entering[k] += np.count_nonzero(survivor)
            sim.do(layer)
            while next_det < sim.num_detectors:
                if next_det in selected:
                    survivor &= ~sim.get_detector_flips(detector_index=next_det)
                next_det += 1
            exiting[k] += np.count_nonzero(survivor)
    success = .01  # Paper d5 p=.001, gap-conditioned endpoint, not estimated here.
    rows = []
    # Labels are author figure 15: 9 cultivation rounds, 5 graft stabilization,
    # 1 transition, and 10 final rounds. Source round definitions vary gate depth.
    stages = ['injection'] + ['cultivation']*8 + ['graft_stabilization']*5 + ['matchable_transition'] + ['gap_wait']*10
    for k, stage in enumerate(stages):
        rows.append({'layer': k+1, 'stage': stage, 'active_qubits': q_active[k], 'survival_entering': float(entering[k]/shots), 'survival_exiting': float(exiting[k]/shots), 'expected_qubitrounds_per_accepted_output': float(q_active[k]*entering[k]/shots/success), **layer_counts[k]})
    total = sum(row['expected_qubitrounds_per_accepted_output'] for row in rows)
    grouped = {}
    for stage in dict.fromkeys(stages):
        subset = [row for row in rows if row['stage']==stage]
        value = sum(row['expected_qubitrounds_per_accepted_output'] for row in subset)
        reserved = sum(circuit.num_qubits*row['survival_entering']/success for row in subset)
        reserved_total = sum(circuit.num_qubits*row['survival_entering']/success for row in rows)
        grouped[stage] = {'rounds_on_surviving_attempt': len(subset), 'active_qubits_min': min(row['active_qubits'] for row in subset), 'active_qubits_max': max(row['active_qubits'] for row in subset), 'expected_qubitrounds_per_accepted_output': value, 'percent_of_active_attempt_cost': 100*value/total, 'reserved_peak_qubitrounds_per_accepted_output': reserved, 'percent_of_fixed_cell_cost': 100*reserved/reserved_total, 'raw_T_equivalent_proxy_gates_on_full_attempt': sum(row.get('raw_T_equivalent_proxy_gates',0) for row in subset), 'CX_pairs_on_full_attempt': sum(row.get('CX_pairs',0) for row in subset), 'measurements_on_full_attempt': sum(row.get('physical_measurements',0) for row in subset)}
    return {'commit': '871e68ff6df2f75190b1bfd6351459d1b5a037e3', 'stim_version': stim.__version__, 'seed': 20261006, 'shots': shots, 'circuit_sha256': hashlib.sha256(str(circuit).encode()).hexdigest(), 'code_qubits_peak': circuit.num_qubits, 'physical_measurement_rounds': len(physical_layers), 'ideal_terminal_MPP_excluded': True, 'source_fixed_final_acceptance': success, 'early_postselection_survival': float(exiting[-1]/shots), 'quality_status': 'S proxy cost MC only; published d5 T-quality conjecture and erratum remain unvalidated', 'expected_active_qubitrounds_per_output': total, 'reserved_peak_qubitrounds_per_output': float(sum(circuit.num_qubits*row['survival_entering']/success for row in rows)), 'expected_raw_T_equivalent_gates_per_output': sum(row.get('raw_T_equivalent_proxy_gates',0)*row['survival_entering']/success for row in rows), 'stages': grouped, 'layers': rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cultivation', action='store_true')
    parser.add_argument('--scan', action='store_true')
    parser.add_argument('--shots', type=int, default=1024*1000)
    args = parser.parse_args()
    inp = json.loads((ROOT/'results'/'paper_counts_proxy.costs.json').read_text())
    method = next(m for m in inp['methods'] if m['method']=='hwp_global_joint_batch_in_circuit_tower_mixed_diagonal')
    n = method['t_count_branch_maximum']
    budget = inp['total_execution_target']/3
    result = {'workload': {'method': method['method'], 'T_branch_maximum': n, 'T_expected': method['t_count'], 'CCZ_current_demand': method['ccz_consumption'], 'total_failure_target': inp['total_execution_target'], 'magic_state_plus_delivery_budget': budget, 'maximum_per_delivered_state_error': budget/n, 'GSJ_2e_9_output_budget_used': 2e-9*n, 'GSJ_delivery_error_margin_per_output': budget/n-2e-9, 'historical_65_percent_not_transferred': True}, 'distillation': distillation_audit(args.scan)}
    output = ROOT/'results'/'factory_audit.json'
    output.write_text(json.dumps(result, indent=2), encoding='utf-8')
    if args.cultivation:
        result['cultivation'] = cultivation_audit(args.shots)
    for row in result['distillation']['factories'].values():
        row['whole_demand_intrinsic_qubitseconds_400ns_cycle'] = row['qubitcycles_per_output']*n*400e-9
        row['total_produced_error_union_proxy'] = row['published_equations_output_error_proxy']*n
    output.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({'result':str(output), 'T_maximum':n, 'scan_points':len(result['distillation'].get('limited_existing_parameter_scan',[])), 'best_existing_point':result['distillation'].get('best_within_limited_scan'), 'cultivation_active_qubitrounds':result.get('cultivation',{}).get('expected_active_qubitrounds_per_output'), 'cultivation_fixed_qubitrounds':result.get('cultivation',{}).get('reserved_peak_qubitrounds_per_output')}, indent=2))


if __name__ == '__main__':
    main()
