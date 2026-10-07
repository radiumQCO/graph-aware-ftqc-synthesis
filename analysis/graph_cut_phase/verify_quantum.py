"""Independent complex-amplitude verification of expanded C4 quantum gadgets."""
import cmath
import itertools
import json
import math
from pathlib import Path

from circuits import compact_c4,expanded

HERE=Path(__file__).resolve().parent

def evolve(vector,gate,qs,theta=0,coefficient=0):
    out=[0j]*len(vector)
    for i,amp in enumerate(vector):
        if gate=='CNOT':
            a,b=qs;out[i^((1<<b) if (i>>a)&1 else 0)]+=amp
        elif gate=='X':out[i^(1<<qs[0])]+=amp
        elif gate=='H':
            q=qs[0];base=i&~(1<<q)
            out[base]+=amp/math.sqrt(2);out[base|(1<<q)]+=amp*(-1 if (i>>q)&1 else 1)/math.sqrt(2)
        elif gate=='CZ':
            a,b=qs;out[i]+=amp*(-1 if ((i>>a)&1) and ((i>>b)&1) else 1)
        else:
            angle={'T':math.pi/4,'TDAG':-math.pi/4,'S':math.pi/2}.get(gate,theta*coefficient)
            out[i]+=amp*(cmath.exp(1j*angle) if (i>>qs[0])&1 else 1)
    return out

def branch(c,bits,theta,outcomes):
    index=sum(x<<i for i,x in enumerate(bits));v=[0j]*(1<<c.width);v[index]=1
    measurement=0
    for op in c.full():
        gate,qs=op[:2]
        if gate=='AND':
            for sub in expanded([op]):v=evolve(v,*sub[:2])
        elif gate=='M_AND':
            a,b,t=qs;m=(outcomes>>measurement)&1;measurement+=1
            v=evolve(v,'H',(t,));v=[amp if ((i>>t)&1)==m else 0j for i,amp in enumerate(v)]
            if m:v=evolve(v,'CZ',(a,b));v=evolve(v,'X',(t,))
        elif gate=='P':v=evolve(v,gate,qs,theta,op[2])
        else:v=evolve(v,gate,qs)
    return v,index,measurement

def main():
    worst=0.;cases=0;angles=(.137,math.sqrt(2),-.417)
    for binary in (False,True):
        c=compact_c4(binary);k=1+int(binary)
        for bits in itertools.product((0,1),repeat=4):
            target=sum(bits[j]^bits[(j+1)%4] for j in range(4))
            for theta in angles:
                for m in range(1<<k):
                    v,index,count=branch(c,bits,theta,m);assert count==k
                    wanted=cmath.exp(1j*theta*target)/(2**(k/2))
                    error=max(abs(amp-(wanted if i==index else 0)) for i,amp in enumerate(v))
                    worst=max(worst,error);cases+=1
    assert worst<1e-13
    # CCZ-state teleportation: exactly check its diagonal Kraus phase and all
    # outcome-controlled CZ/Z fixes. |CCZ> amplitude phase is abc.
    ccz_error=0.
    for m in range(8):
        ma,mb,mc=((m>>j)&1 for j in (2,1,0))
        for x in range(8):
            a,b,z=((x>>j)&1 for j in (2,1,0))
            raw=(a^ma)&(b^mb)&(z^mc)
            fix=(ma*b*z)^(mb*a*z)^(mc*a*b)^(ma*mb*z)^(ma*mc*b)^(mb*mc*a)
            ccz_error=max(ccz_error,abs((-1)**(raw^fix^(ma*mb*mc))-(-1)**(a*b*z)))
    assert ccz_error==0
    result={'expanded_C4_basis_angle_measurement_branch_cases':cases,
            'maximum_full_statevector_error':worst,'CCZ_injection_basis_branch_cases':64,'CCZ_phase_error':ccz_error,
            'scope':'Ideal 4T gadgets and projective cleanup with every branch; no noise/factory approximation.'}
    (HERE/'quantum_verification.json').write_text(json.dumps(result,indent=2),encoding='utf8', newline='\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
