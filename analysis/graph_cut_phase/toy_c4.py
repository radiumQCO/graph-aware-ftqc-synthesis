"""Exhaustive C4 first: Boolean arithmetic, phase identity, gate-class search.

No imports of graph scaling or literature. AND = clean-target temporary AND;
XOR/NOT are free only for multiplicative complexity, counted in circuits.
"""
import cmath
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROWS=list(itertools.product((0,1),repeat=4))
MASK=(1<<16)-1
def table(fn):
    return sum(int(fn(*z))<<i for i,z in enumerate(ROWS))
VARS=[table(lambda *z,j=j:z[j]) for j in range(4)]
def span(generators):
    values={0}
    for g in generators:values|={x^g for x in list(values)}
    return sorted(values)
AFFINE=span([MASK]+VARS)
def canonical(f):return min(f^a for a in AFFINE)
def cut(z):return sum(z[i]^z[(i+1)%4] for i in range(4))
def anf(truth):
    # Separate little-endian convention for polynomial coefficients.
    coeff=[truth(*[(i>>j)&1 for j in range(4)]) for i in range(16)]
    for j in range(4):
        for i in range(16):
            if i&(1<<j):coeff[i]^=coeff[i^(1<<j)]
    names='ABCD'
    terms=['1' if i==0 else ''.join(names[j] for j in range(4) if i&(1<<j)) for i,c in enumerate(coeff) if c]
    return {'terms':terms,'degree':max((i.bit_count() for i,c in enumerate(coeff) if c),default=0)}

def c4_predicates(z):
    a,b,c,d=z;p=a^c;q=b^d;r=a^b
    g=p&q;low=p^q^g;high=r&(1^low);s=c^d^g
    return dict(p=p,q=q,r=r,g=g,low=low,high=high,s=s)

def compatible_two_phases(a,b,values):
    # Fit F = constant + alpha*a + beta*b exactly (integer linear constraints).
    levels={}
    for i,f in enumerate(values):
        pair=((a>>i)&1,(b>>i)&1)
        if pair in levels and levels[pair]!=f:return None
        levels[pair]=f
    if len(levels)<3:return None  # C4 has 3 values; no successful pair can use <3 codes.
    if len(levels)==4 and levels[(0,0)]+levels[(1,1)]!=levels[(1,0)]+levels[(0,1)]:return None
    # Complete the missing code using the parallelogram relation.
    if len(levels)==3:
        missing=next(p for p in itertools.product((0,1),repeat=2) if p not in levels)
        diagonal={(0,0):1,(1,1):1,(1,0):-1,(0,1):-1}
        levels[missing]=-sum(diagonal[p]*f for p,f in levels.items())//diagonal[missing]
    c=levels[(0,0)];alpha=levels[(1,0)]-c;beta=levels[(0,1)]-c
    assert all(c+alpha*((a>>i)&1)+beta*((b>>i)&1)==f for i,f in enumerate(values))
    return [c,alpha,beta]

def exhaustive_synthesis():
    low=table(lambda *z:c4_predicates(z)['low'])
    high=table(lambda *z:c4_predicates(z)['high'])
    # AND of any two input affine forms. Affine modifications of its output
    # do not change the generated XOR space, so quotient representatives suffice.
    classes={}
    for a in AFFINE:
        for b in AFFINE:
            q=a&b;classes.setdefault(canonical(q),(q,a,b))
    nonlinear=[v for k,v in classes.items() if k]
    one_binary=[]
    for q,a,b in nonlinear:
        space=set(span([MASK]+VARS+[q]))
        if low in space and high in space:one_binary.append([a,b])
    assert not one_binary
    # Complete two-AND binary search: both target nonlinear cosets are
    # independent. Degree(high)=3 means first quadratic q must have low's
    # coset, since final span has only 2 nonlinear dimensions.
    witnesses=[];tested=0
    for q,a,b in nonlinear:
        if canonical(q)!=canonical(low):continue
        first=span([MASK]+VARS+[q]);first_set=set(first)
        for u in first:
            for v in first:
                tested+=1;g=u&v
                if low in first_set or (low^g) in first_set:
                    if high in first_set or (high^g) in first_set:
                        witnesses.append({'first_factors_truth_hex':[hex(a),hex(b)],'second_factors_truth_hex':[hex(u),hex(v)]})
    assert witnesses
    values=[cut(z)//2 for z in ROWS]
    zero_phase_pairs=0
    for a,b in itertools.combinations(AFFINE,2):
        zero_phase_pairs+=compatible_two_phases(a,b,values) is not None
    assert zero_phase_pairs==0
    phase_witness=None;phase_pairs_tested=0
    for q,a,b in nonlinear:
        space=span([MASK]+VARS+[q])
        for u,v in itertools.combinations(space,2):
            phase_pairs_tested+=1
            coeff=compatible_two_phases(u,v,values)
            if coeff is not None:
                phase_witness={'and_factors_truth_hex':[hex(a),hex(b)],'phase_predicates_truth_hex':[hex(u),hex(v)],'coefficients_for_cut_half':coeff}
                break
        if phase_witness:break
    assert phase_witness
    return {'affine_functions':len(AFFINE),'nonlinear_first_AND_cosets':len(nonlinear),
            'one_AND_binary_solutions':len(one_binary),'two_AND_binary_factor_pairs_tested':tested,
            'two_AND_binary_witness_count':len(witnesses),'one_witness':witnesses[0],
            'zero_AND_two_phase_solutions':zero_phase_pairs,'one_AND_phase_pairs_before_witness':phase_pairs_tested,
            'one_AND_two_phase_witness':phase_witness,
            'scope':'XOR/NOT/clean AND, arbitrary affine AND controls; phase gates P(c*theta) on computed Boolean predicates; NOT universal quantum-circuit optimality'}

def reversible_check():
    # In-place linear transform gives data [A,r,p,q]. 1 extra bit g.
    # Phase-only g is changed to s = C xor D xor g via controls p,q,r:
    # s = r xor p xor q xor g. Restore g before measured inverse.
    # Evaluate all measurement branches as Kraus amplitudes independently.
    phase_error=0.;inverse_error=0.
    angles=[.137,2**.5,3.141592653589793/7,-.417]
    for z in ROWS:
        a,b,c,d=z;p=c^a;q=d^b;r=b^a;g=p&q
        s=g^r^p^q
        assert (r+s)*2==cut(z)
        restored=g^r^p^q^r^p^q
        assert restored==g
        original=(a,r^a,p^a,q^(r^a))
        assert original==z
        for theta in angles:
            actual=cmath.exp(2j*theta*r)*cmath.exp(2j*theta*s)
            expected=cmath.exp(1j*theta*cut(z))
            phase_error=max(phase_error,abs(actual-expected))
            for measurement in (0,1):
                # X measure g gives (-1)^(m*g)/sqrt(2); CZ(p,q)^m cancels.
                branch=actual*((-1)**(measurement*g+measurement*(p&q)))/(2**.5)
                inverse_error=max(inverse_error,abs(branch-expected/(2**.5)))
    return {'basis_assignments':16,'generic_test_angles':angles,'phase_max_amplitude_error':phase_error,
            'phase_only_measured_inverse_branches':32,'inverse_max_amplitude_error':inverse_error,
            'symbolic_identity':'cut=2*(r+s), r=A xor B, s=C xor D xor ((A xor C)&(B xor D))'}

def main():
    rows=[]
    for z in ROWS:
        f=c4_predicates(z);v=cut(z)
        assert v==2*(f['low']+2*f['high'])==2*(f['r']+f['s'])
        rows.append({'ABCD':''.join(map(str,z)),'cut':v,'half_low':f['low'],'half_high':f['high'],'r':f['r'],'s':f['s']})
    anfs={'half_low':anf(lambda *z:c4_predicates(z)['low']),
          'half_high':anf(lambda *z:c4_predicates(z)['high'])}
    assert anfs['half_high']['degree']==3
    result={'status':'C4_EXHAUSTIVELY_VERIFIED_BEFORE_SCALING','truth_table':rows,'ANF':anfs,
            'binary_AND_minimum':2,'degree_lower_bound':'One AND with affine inputs has degree <=2, but high half-cut bit has degree 3.',
            'phase_only_AND_count':1,'phase_only_rotation_count':2,'search':exhaustive_synthesis(),'reversible_phase':reversible_check()}
    (HERE/'c4_results.json').write_text(json.dumps(result,indent=2),encoding='utf8', newline='\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
