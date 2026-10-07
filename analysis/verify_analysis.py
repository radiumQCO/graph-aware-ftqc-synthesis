"""Independent mathematical checks for recovered structure and known transforms."""
import csv
import hashlib
import json
import math
import random
from pathlib import Path

import numpy as np
import mpmath as mp
from tfim_structure import layers, GAMMA

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"

def apply(state,pauli,support,theta):
    n=int(round(math.log2(len(state))))
    ids=np.arange(2**n)
    if pauli=="X":
        pstate=state[ids^(1<<support[0])]
    else:
        parity=((ids>>support[0])^(ids>>support[1]))&1
        pstate=(1-2*parity.astype(float))*state
    return math.cos(theta/2)*state-1j*math.sin(theta/2)*pstate

def main():
    checks=[]
    # Source bytes immutable and reproducible.
    for item in json.loads((ROOT/"sources/manifest.json").read_text()):
        assert hashlib.sha256((ROOT/"sources"/item["file"]).read_bytes()).hexdigest()==item["sha256"]
    checks.append("source hashes")
    for name,expected in (("paper_counts_proxy",60200),("notebook_literal",224200)):
        data=json.loads((OUT/f"{name}.structure.json").read_text())
        rows=list(csv.DictReader((OUT/f"{name}.rotations.csv").open(encoding="utf-8")))
        assert len(rows)*2==expected==data["batch_rotations"]
        assert sum(a["batch_multiplicity"] for a in data["angle_families"])==expected
        assert data["edge_parity_rank_gf2"]==99
        for r in rows:
            for pred in r["predecessors"].split():
                p=rows[int(pred)]
                assert int(pred)<int(r["id"])
                assert p["pauli"]!=r["pauli"]
                assert set(p["support"].split())&set(r["support"].split())
        rng=random.Random(19)
        # HWP identity on arbitrary computational-basis components, including
        # correlated edge parities. Check random100-spin cuts and exhaustive8bits.
        worst=0.0
        for _ in range(1000):
            x=[rng.randrange(2) for _ in range(100)]
            parities=[x[a]^x[b] for a,b in data["edges"]]
            w=sum(parities); m=len(parities)
            theta=next(a["theta_radians"] for a in data["angle_families"] if a["family"]=="ZZ_common")
            direct=np.exp(-.5j*theta*sum(1-2*p for p in parities))
            binary=np.exp(-.5j*theta*m)*np.exp(1j*theta*sum(((w>>k)&1)*2**k for k in range(m.bit_length())))
            worst=max(worst,abs(direct-binary))
            if data["all_degrees_even"]:
                assert w%2==0
        assert worst<1e-12
        costs=json.loads((OUT/f"{name}.costs.json").read_text())
        for method in costs["methods"]:
            assert method["full_diamond_synthesis_bound"]<=.002/3
            if "t_count_branch_maximum" in method:
                assert method["t_count"]<=method["t_count_branch_maximum"]+1e-7
        checks.append(dict(case=name,rotations=expected,hwp_phase_max_error=worst,dependency_edges=data["dependency_edges_per_instance"]))
    # Compare merged construction to unmerged fourth-order formula on a random
    # entangled four-spin state, both effective notebook signs and intended signs.
    rng=np.random.default_rng(29)
    for sign in (-1,1):
        state=rng.normal(size=16)+1j*rng.normal(size=16)
        state/=np.linalg.norm(state)
        def evolution(seq):
            s=state.copy()
            for kind,c in seq:
                supports=[(q,) for q in range(4)] if kind=="X" else [(0,1),(1,2),(2,3)]
                theta=.5*c*(sign if kind=="X" else -sign)
                for support in supports:
                    s=apply(s,kind,support,theta)
            return s
        raw=[]
        for _ in range(3):
            for c in (GAMMA,GAMMA,1-4*GAMMA,GAMMA,GAMMA):
                raw.extend([("X",c/2),("ZZ",c),("X",c/2)])
        merged=[(l["pauli"],l["coefficient"]) for l in layers(3,sign,-sign,.25)]
        error=np.linalg.norm(evolution(raw)-evolution(merged))
        assert error<1e-12
        checks.append(dict(merged_strang_statevector_error=float(error)))
    cache=json.loads((OUT/"synthesis_cache.json").read_text())
    mp.mp.dps=90
    def unitary_from_string(gates):
        # Independent standard matrix multiplication, no number-theory backend.
        a,b,c,d=mp.mpc(1),mp.mpc(0),mp.mpc(0),mp.mpc(1)
        rt=mp.sqrt(2)
        for gate in reversed(gates):
            if gate=="H":
                a,b,c,d=(a+c)/rt,(b+d)/rt,(a-c)/rt,(b-d)/rt
            elif gate in ("T","S"):
                phase=mp.exp(1j*mp.pi/(4 if gate=="T" else 2))
                c,d=phase*c,phase*d
            elif gate=="X":
                a,b,c,d=c,d,a,b
            elif gate=="W":
                pass  # global phase; irrelevant for a channel
            else:
                raise AssertionError(gate)
        return a,b,c,d
    decoded={}
    deterministic=0
    for key,r in cache.items():
        if key.startswith("MIX|"):
            continue
        a,b,c,d=unitary_from_string(r["gates"])
        decoded[key]=(a,b,c,d)
        theta=mp.mpf(r["theta"])
        overlap=abs(mp.exp(1j*theta/2)*a+mp.exp(-1j*theta/2)*d)/2
        err=2*mp.sqrt(max(mp.mpf(0),1-overlap**2))
        assert err<=mp.mpf(r["delta"])
        assert abs(float(err)-r["measured_diamond"])<1e-18
        assert r["gates"].count("T")==r["t_count"]
        deterministic+=1
    mixtures=[r for k,r in cache.items() if k.startswith("MIX|")]
    for r in mixtures:
        p=r["residual_pauli_probabilities"]
        assert min(p)>=-1e-14 and abs(sum(p)-1)<1e-12
        assert abs(2*(1-p[0])-r["measured_diamond"])<1e-12
        vals=[]
        for key in r["branch_keys"]:
            a,b,c,d=decoded[key]
            determinant=mp.sqrt(a*d-b*c)
            a,c=a/determinant,c/determinant
            vals.append((mp.exp(1j*mp.mpf(r["theta"]))*a*a,abs(c)**2))
        probability=mp.mpf(r["probability_first"])
        z=probability*vals[0][0]+(1-probability)*vals[1][0]
        s=probability*vals[0][1]+(1-probability)*vals[1][1]
        err=1-mp.re(z)+s
        assert abs(mp.im(z))<mp.mpf("1e-70")
        assert 0<=err<=mp.mpf(r["delta"])
        assert abs(float(err)-r["measured_diamond"])<1e-18
    checks.append(dict(independently_multiplied_deterministic_sequences=deterministic,
                       certified_positive_mixtures=len(mixtures),synthesis_cache_entries=len(cache)))
    (OUT/"verification.json").write_text(json.dumps(checks,indent=2),encoding="utf-8")
    print(json.dumps(checks,indent=2))

if __name__=="__main__":
    main()
