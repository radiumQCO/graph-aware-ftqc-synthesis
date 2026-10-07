"""Existing C4 circuits as a small verified optimizer control, not workload substitution."""
import json
import random
from pathlib import Path
from prepare import cc,rotation,SEED
from circuits import generic,compact_c4
HERE=Path(__file__).resolve().parent
rows={}
for name,c in [('C4_generic',generic(4,[(0,1),(1,2),(2,3),(0,3)],True)),('C4_compact',compact_c4(False))]:
    rng=random.Random(SEED);ops=[]
    for op in c.full():
        g,qs=op[:2]
        if g=='AND_ZERO':continue
        if g=='P':ops+=rotation(cc.theta_for('ZZ_common')*op[2],qs[0],rng,f'{name}:phase')[0]
        else:ops.append(('UNAND' if g=='M_AND' else g,qs))
    rows[name]={'ops':ops,'data_qubits':4,'scope':'C4 control only; not the 200-qubit workload'}
(HERE/'tiny_programs.json').write_text(json.dumps(rows))
