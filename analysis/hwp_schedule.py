"""ASAP depth of the published Qualtran HammingWeightCompute decomposition.

Transcribes its three-to-two adders and Gidney AND (Apache-2.0 source linked
in the report). This is ordinary dependency scheduling, no new synthesis rule.
Connectivity and feedback duration are not modelled.
"""
from collections import defaultdict

def macros_for(n):
    """Published compute network, exposed for a separate basis-state audit."""
    if n < 1:
        raise ValueError("Hamming-weight input must have at least one bit")
    junk=list(range(n,n+n-n.bit_count()))
    out=list(range(n+len(junk),n+len(junk)+n.bit_length()))
    x=list(range(n))
    macros=[]
    def cnot(a,b):
        macros.append(("CNOT",(a,b)))
    def adder(a,b,c,t):
        cnot(a,b);cnot(a,c)
        macros.append(("AND",(b,c,t)))
        cnot(a,b);cnot(a,t);cnot(b,c)
    for output in out:
        y=[]
        for idx in range(0,len(x)-2,2):
            t=junk.pop(); y.append(t)
            adder(x[idx],x[idx+1],x[idx+2],t)
        if len(x)%2:
            cnot(x[-1],output)
        else:
            t=junk.pop(); y.append(t)
            adder(x[-2],x[-1],output,t)
        x=y
    assert not junk and sum(k=="AND" for k,_ in macros)==n-n.bit_count()
    return macros

def schedule(n):
    macros = macros_for(n)
    def expanded(reverse=False):
        for gate,qs in (reversed(macros) if reverse else macros):
            if gate=="CNOT":
                yield gate,qs
                continue
            a,b,t=qs
            if reverse:
                yield "H",(t,)
                yield "M",(t,)
                # Include measured t as a classical predecessor of conditional CZ.
                yield "classically_controlled_CZ",(a,b,t)
                yield "reset",(t,)
            else:
                yield "H",(t,); yield "T",(t,)
                yield "CNOT",(a,t);yield "CNOT",(b,t)
                yield "CNOT",(t,a);yield "CNOT",(t,b)
                yield "T",(a,);yield "T",(b,);yield "T",(t,)
                yield "CNOT",(t,a);yield "CNOT",(t,b)
                yield "H",(t,);yield "S",(t,)
    def depth(ops,t_only=False):
        last=defaultdict(int)
        for gate,qs in ops:
            end=max(last[q] for q in qs)+(int(gate=="T") if t_only else 1)
            for q in qs:
                last[q]=end
        return max(last.values())
    return dict(compute_t_depth=depth(expanded(),True),
                compute_primitive_depth=depth(expanded()),
                uncompute_primitive_depth=depth(expanded(True)))

if __name__=="__main__":
    for n in (40,50,100,180,200,360,400):
        print(n,schedule(n))
