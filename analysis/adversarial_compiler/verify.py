"""Independent integer checks on all weight values and actual mapped graphs."""
import json
import math
import random
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent),str(HERE.parent/'graph_cut_phase')]
from circuits import generic,grid_plaquettes,expanded
from scaling import grid
from hwp_schedule import macros_for
from verify_quantum import evolve

def classical_weight(n,w):
    ops=macros_for(n); k=n-n.bit_count(); b=n.bit_length()
    state=[int(i<w) for i in range(n)]+[0]*(k+b)
    before=state[:n]
    for g,qs in ops:
        if g=='CNOT':state[qs[1]]^=state[qs[0]]
        else:
            a,c,t=qs;assert state[t]==0;state[t]=state[a]&state[c]
    out=sum(state[n+k+j]<<j for j in range(b));assert out==w
    for g,qs in reversed(ops):
        if g=='CNOT':state[qs[1]]^=state[qs[0]]
        else:
            a,c,t=qs;assert state[t]==state[a]&state[c];state[t]=0
    assert state[:n]==before and not any(state[n:])

def main():
    rng=random.Random(17);cases=0
    for n in (200,400):
        for w in range(n+1):classical_weight(n,w);cases+=1
    edges,faces=grid(10,10,periodic=True,copies=2)
    a=generic(200,edges,False,False,False);a.phase(600,1)
    b=generic(200,edges,True,True,True)
    c=grid_plaquettes(200,edges,faces,True,True,True)
    samples=[[0]*200,[1]*200,[(i//10+i%10)%2 for i in range(200)]]
    samples += [[rng.randrange(2) for i in range(200)] for _ in range(500)]
    for bits in samples:
        target=sum(bits[i]^bits[j] for i,j in edges)
        assert target%2==0
        assert a.verify(bits)==b.verify(bits)==c.verify(bits)==target
    # Verify the unitary-lift primitive and its inverse independently in amplitudes.
    forward=expanded([('AND',(0,1,2))]);inverse=[]
    for g,qs in reversed(forward):inverse.append(({'T':'TDAG','TDAG':'T','S':'SDAG'}.get(g,g),qs))
    worst=0
    for i in range(8):
        v=[0j]*8;v[i]=1
        for g,qs in forward+inverse:
            if g=='SDAG':v=evolve(v,'P',qs,-math.pi/2,1)
            else:v=evolve(v,g,qs)
        worst=max(worst,max(abs(x-int(j==i)) for j,x in enumerate(v)))
    assert worst<1e-12
    result=dict(HWC_all_integer_weight_cases=cases,graph_cases=len(samples),
                lift_full_unitary_basis_cases=8,lift_inverse_max_error=worst,
                graph_contract='exact integer phase exponent; all inputs admitted, no symmetry sector',
                full_200_qubit_statevector='not attempted; compositional proof and Boolean simulation')
    (HERE/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8',newline='\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
