"""Explicit XOR/clean-AND/P(theta) circuits, including measured cleanup.

Angles are symbolic integer multiples of generic theta. Depths are abstract
logical-gate depths with all-to-all CNOTs, not surface-code latency.
"""
from collections import Counter,defaultdict

class Circuit:
    def __init__(self,n,name):
        self.n=n;self.width=n;self.name=name;self.compute=[];self.phases=[];self._full_cache=None
    def fresh(self):
        q=self.width;self.width+=1;return q
    def emit(self,kind,*qs):self.compute.append((kind,tuple(qs)));self._full_cache=None
    def phase(self,q,coefficient):self.phases.append(('P',(q,),coefficient));self._full_cache=None
    def full(self):
        if self._full_cache is not None:return self._full_cache
        inverse=[]
        for gate,qs in reversed(self.compute):
            inverse.append(('M_AND' if gate=='AND' else gate,qs))
        self._full_cache=self.compute+self.phases+inverse
        return self._full_cache
    def verify(self,bits,measurements=None):
        initial=list(bits);state=initial+[0]*(self.width-self.n)
        exponent=0;measured=0;branch_sign=1
        for op in self.full():
            kind,qs=op[:2]
            if kind=='CNOT':state[qs[1]]^=state[qs[0]]
            elif kind=='X':state[qs[0]]^=1
            elif kind=='AND':
                a,b,t=qs;assert state[t]==0
                state[t]=state[a]&state[b]
            elif kind=='AND_ZERO':
                a,b,t=qs;assert state[t]==0 and (state[a]&state[b])==0
            elif kind=='M_AND':
                a,b,t=qs;assert state[t]==(state[a]&state[b]),(self.name,qs)
                m=(measurements>>measured)&1 if measurements is not None else measured%2
                # X-measurement Kraus sign and outcome-controlled CZ sign.
                branch_sign*=(-1)**(m*state[t]+m*(state[a]&state[b]))
                state[t]=0;measured+=1
            elif kind=='P':exponent+=op[2]*state[qs[0]]
            else:raise ValueError(kind)
        assert state[:self.n]==initial and not any(state[self.n:])
        assert branch_sign==1
        return exponent

def weighted_popcount(c,seeds,even_first_column=False,first_only=False):
    """Existing three-to-two-adder network, with inputs in weighted columns.

    Removing a known-zero product in the last LSB half-adder is valid only
    when the whole LSB seed XOR is zero. This is verified during simulation.
    """
    column=0;carry=[];outputs=[];maximum=sum((1<<j)*len(v) for j,v in seeds.items())
    while (1<<column)<=maximum or carry:
        x=carry+list(seeds.get(column,()));y=[]
        if x:
            output=c.fresh()
            def adder(a,b,z,known_zero=False):
                t=c.fresh();c.emit('CNOT',a,b);c.emit('CNOT',a,z)
                c.emit('AND_ZERO' if known_zero else 'AND',b,z,t)
                c.emit('CNOT',a,b);c.emit('CNOT',a,t);c.emit('CNOT',b,z)
                y.append(t)
            for i in range(0,len(x)-2,2):adder(x[i],x[i+1],x[i+2])
            if len(x)%2:c.emit('CNOT',x[-1],output)
            else:adder(x[-2],x[-1],output,even_first_column and column==0)
            outputs.append((column,output))
        carry=y;column+=1
        if first_only:return outputs,carry
    return outputs

def carry_save_reduce(c,seeds,target_count):
    """Standard full-/half-adder compression, stopped at a phase-bit budget."""
    columns=defaultdict(list,{j:list(v) for j,v in seeds.items()})
    def total():return sum(map(len,columns.values()))
    while total()>target_count:
        triples=[j for j,v in columns.items() if len(v)>=3]
        if triples:
            j=min(triples);a,b,z=[columns[j].pop(0) for _ in range(3)];t=c.fresh()
            c.emit('CNOT',a,b);c.emit('CNOT',a,z);c.emit('AND',b,z,t)
            c.emit('CNOT',a,b);c.emit('CNOT',a,t);c.emit('CNOT',b,z)
            columns[j].append(z);columns[j+1].append(t)
        else:
            pairs=[j for j,v in columns.items() if len(v)>=2]
            assert pairs,(total(),target_count)
            j=min(pairs);a,b=[columns[j].pop(0) for _ in range(2)];t=c.fresh()
            c.emit('AND',a,b,t);c.emit('CNOT',a,b)
            columns[j].append(b);columns[j+1].append(t)
    return [(j,q) for j,v in sorted(columns.items()) for q in v]

def balanced_lsb(c,raw,even=False):
    """Balanced full-adder tree for the first weight column, same AND count."""
    active=list(raw);carry=[]
    while len(active)>=3:
        nxt=[]
        for i in range(0,len(active)-2,3):
            a,b,z=active[i:i+3];t=c.fresh()
            c.emit('CNOT',a,b);c.emit('CNOT',a,z);c.emit('AND',b,z,t)
            c.emit('CNOT',a,b);c.emit('CNOT',a,t);c.emit('CNOT',b,z)
            nxt.append(z);carry.append(t)
        nxt.extend(active[len(active)//3*3:]);active=nxt
    if len(active)==2:
        a,b=active;t=c.fresh()
        if even:
            # Final two parity bits are identical, so their integer carry is a.
            c.emit('CNOT',a,t)
        else:c.emit('AND',a,b,t)
        c.emit('CNOT',a,b);carry.append(t);active=[b]
    return [(0,active[0])] if active else [],carry

def weighted_phase(c,raw,bits,maximum,even=False,partial=False,balanced=False):
    if not partial:return weighted_popcount(c,{0:raw,1:bits},even and bool(raw))
    if balanced:low,carry=balanced_lsb(c,raw,even)
    else:low,carry=weighted_popcount(c,{0:raw},even and bool(raw),first_only=True) if raw else ([],[])
    low=[] if even else low
    target=maximum.bit_length()-int(even)
    remaining=carry_save_reduce(c,{1:carry+list(bits)},target-len(low))
    return low+remaining

def generic(n,edges,parity_aware=False,partial=False,balanced=False):
    c=Circuit(n,'generic_balanced_partial' if balanced else 'generic_partial' if partial else 'generic_even' if parity_aware else 'generic')
    parities=[]
    for a,b in edges:
        q=c.fresh();c.emit('CNOT',a,q);c.emit('CNOT',b,q);parities.append(q)
    even=all(sum(v in edge for edge in edges)%2==0 for v in range(n))
    assert not parity_aware or even
    outputs=weighted_phase(c,parities,[],len(edges),even if parity_aware else False,partial,balanced)
    for j,q in outputs:
        if not (even and j==0):c.phase(q,1<<j)
    return c

def predicates(c,face,first_linear=None):
    a,b,z,d=face;p=c.fresh();q=c.fresh()
    c.emit('CNOT',a,p);c.emit('CNOT',z,p)
    c.emit('CNOT',b,q);c.emit('CNOT',d,q)
    s=c.fresh();c.emit('AND',p,q,s)
    c.emit('CNOT',z,s);c.emit('CNOT',d,s)
    if first_linear is None:
        r=c.fresh();c.emit('CNOT',a,r);c.emit('CNOT',b,r)
    else:r=first_linear
    return r,s

def cycle_fan(n,aggregate=False,partial=False):
    assert n>=4 and n%2==0
    c=Circuit(n,'cycle_fan_partial' if partial else 'cycle_fan_aggregate' if aggregate else 'cycle_fan_direct')
    r=c.fresh();c.emit('CNOT',0,r);c.emit('CNOT',1,r)
    bits=[r]
    for j in range(n//2-1):
        _,s=predicates(c,(0,2*j+1,2*j+2,2*j+3),r);bits.append(s)
    if aggregate:
        outputs=carry_save_reduce(c,{0:bits},(n//2).bit_length()) if partial else weighted_popcount(c,{0:bits})
        for j,q in outputs:c.phase(q,2<<j)
    else:
        for q in bits:c.phase(q,2)
    return c

def grid_plaquettes(n,edges,faces,aggregate=True,partial=False,balanced=False):
    c=Circuit(n,'plaquette_balanced_partial' if balanced else 'plaquette_partial' if partial else 'plaquette_aggregate' if aggregate else 'plaquette_direct')
    covered=set();bits=[]
    for face in faces:
        es={tuple(sorted((face[i],face[(i+1)%4]))) for i in range(4)}
        assert len(es)==4 and es<=set(edges) and not (es&covered)
        covered|=es;bits.extend(predicates(c,face))
    raw=[]
    for a,b in edges:
        if (a,b) not in covered:
            q=c.fresh();c.emit('CNOT',a,q);c.emit('CNOT',b,q);raw.append(q)
    if aggregate:
        even=all(sum(v in edge for edge in edges)%2==0 for v in range(n))
        for j,q in weighted_phase(c,raw,bits,len(edges),even,partial,balanced):
            if not (even and j==0):c.phase(q,1<<j)
    else:
        for q in raw:c.phase(q,1)
        for q in bits:c.phase(q,2)
    return c

def compact_c4(binary=False):
    c=Circuit(4,'C4_compact_binary' if binary else 'C4_compact_phase')
    # Data becomes [A, A xor B, A xor C, B xor D].
    c.emit('CNOT',0,2);c.emit('CNOT',1,3);c.emit('CNOT',0,1)
    g=c.fresh();c.emit('AND',2,3,g)
    if binary:
        c.emit('CNOT',2,g);c.emit('CNOT',3,g) # g = OR(p,q)
        c.emit('X',g);h=c.fresh();c.emit('AND',1,g,h);c.emit('X',g)
        c.phase(g,2);c.phase(h,4)
    else:
        for q in (1,2,3):c.emit('CNOT',q,g)
        c.phase(1,2);c.phase(g,2)
    return c

def direct_edge_phases(n,edges):
    # Phase gadgets are interleaved, so use a dedicated object with full override.
    c=Circuit(n,'direct_edges');ops=[]
    colors=[]
    for a,b in edges:
        chosen=next((i for i,v in enumerate(colors) if a not in v[0] and b not in v[0]),None)
        if chosen is None:chosen=len(colors);colors.append((set(),[]))
        colors[chosen][0].update((a,b));colors[chosen][1].append((a,b))
    for _,pairs in colors:
        for a,b in pairs:ops.extend([('CNOT',(a,b)),('P',(b,),1),('CNOT',(a,b))])
    c.full=lambda:ops
    return c

def depth(ops,metric='logical'):
    last=defaultdict(int)
    for op in ops:
        kind,qs=op[:2]
        duration=int(kind in ('T','TDAG')) if metric=='T' else int(kind=='AND') if metric=='AND' else 1
        if kind=='AND_ZERO':continue
        end=max(last[q] for q in qs)+duration
        for q in qs:last[q]=end
    return max(last.values(),default=0)

def expanded(ops):
    result=[]
    for op in ops:
        kind,qs=op[:2]
        if kind=='AND':
            a,b,t=qs
            result.extend([('H',(t,)),('T',(t,)),('CNOT',(a,t)),('CNOT',(b,t)),
                           ('CNOT',(t,a)),('CNOT',(t,b)),('TDAG',(a,)),('TDAG',(b,)),('T',(t,)),
                           ('CNOT',(t,a)),('CNOT',(t,b)),('H',(t,)),('S',(t,))])
        elif kind=='M_AND':
            a,b,t=qs
            result.extend([('H',(t,)),('M',(t,)),('classical_CZ',(a,b,t)),('reset',(t,))])
        elif kind!='AND_ZERO':result.append(op)
    return result

def metrics(c):
    ops=c.full();counts=Counter(g[0] for g in ops);k=counts['AND']
    return {'name':c.name,'AND_compute':k,'CCZ_resource_compute':k,'fixed_T_compute':4*k,
            'AND_uncompute_unitary_if_used':k,'fixed_T_unitary_inverse_if_used':4*k,
            'cleanup_X_measurements':counts['M_AND'],'cleanup_conditional_CZ':counts['M_AND'],
            'rotation_count':counts['P'],'angle_multipliers':[g[2] for g in ops if g[0]=='P'],
            'clean_ancillas_excluding_magic_injection':c.width-c.n,'CNOT_full_sandwich_macro':counts['CNOT'],
            'X_full_sandwich':counts['X'],'CNOT_including_4T_AND_gadgets':counts['CNOT']+6*k,
            'compute_AND_depth':depth(c.compute,'AND'),'full_4T_gadget_T_depth_excluding_rotations':depth(expanded(ops),'T'),
            'logical_macro_depth':depth(ops),'expanded_logical_depth':depth(expanded(ops)),
            'depth_scope':'all-to-all logical unit gate duration; cleanup includes H/M/CZ/reset; no factory/injection/routing/feedforward latency',
            'T_scope':'only fixed temporary-AND T; exact generic-angle P is a separate resource, not free Clifford+T'}
