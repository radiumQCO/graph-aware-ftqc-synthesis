"""Actual strong PyZX passes, exact symbolic equivalence, on C4 controls."""
import json
import random
import time
from pathlib import Path
import numpy as np
import pyzx as zx
from optimize import as_circuit,metrics
HERE=Path(__file__).resolve().parent
rows=[]
for name,program in json.loads((HERE/'tiny_programs.json').read_text()).items():
    c,_=as_circuit(program['ops'],4)
    for method in ('basic','todd','teleport'):
        random.seed(17);np.random.seed(17);start=time.perf_counter()
        if method=='basic':opt=zx.optimize.basic_optimization(c)
        elif method=='todd':opt=zx.optimize.full_optimize(c)
        else:opt=zx.Circuit.from_graph(zx.simplify.teleport_reduce(c.to_graph())).to_basic_gates()
        elapsed=time.perf_counter()-start;cert=bool(c.verify_equality(opt))
        row=dict(case=name,method=method,before=metrics(c),after=metrics(opt),compile_seconds=elapsed,ZX_identity=cert)
        rows.append(row);print(json.dumps(row),flush=True)
        (HERE/'tiny_optimizer_results.json').write_text(json.dumps(rows,indent=2))
