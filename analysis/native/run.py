"""Project-local native Windows toolchain; bounded and logged external jobs.

Use the pinned official sources. No global PATH, registry, Windows policy,
or optimizer algorithm is changed by this script.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent.parent
SOURCES=PROJECT/'analysis/sources/compilers'


def environment():
    env=os.environ.copy()
    env['CARGO_HOME']=str(HERE/'cargo')
    env['RUSTUP_HOME']=str(HERE/'rustup')
    env['CABAL_DIR']=str(HERE/'cabal')
    ghcs=sorted(HERE.glob('ghc-*/bin/ghc.exe'))
    paths=[HERE/'bin',HERE/'cargo/bin']
    if ghcs:
        root=ghcs[0].parent.parent
        paths[:0]=[root/'bin',root/'mingw/bin',root/'mingw/x86_64-w64-mingw32/bin']
        rust_lib=HERE/'rustup/toolchains/1.90.0-x86_64-pc-windows-gnu/lib/rustlib/x86_64-pc-windows-gnu'
        env['CARGO_ENCODED_RUSTFLAGS']='\x1f'.join(['-C','dlltool='+str(root/'mingw/bin/llvm-dlltool.exe'),
                                                  '-C','linker='+str(rust_lib/'bin/self-contained/x86_64-w64-mingw32-gcc.exe'),
                                                  '-C','link-self-contained=yes'])
    rust_helpers=HERE/'rustup/toolchains/1.90.0-x86_64-pc-windows-gnu/lib/rustlib/x86_64-pc-windows-gnu/bin/self-contained'
    if rust_helpers.exists():paths.append(rust_helpers)
    env['PATH']=';'.join(map(str,paths))+';'+env.get('PATH','')
    return env


def job(name,command,cwd,limit=900):
    log=HERE/'logs'/f'{name}.log'
    log.parent.mkdir(exist_ok=True)
    start=time.perf_counter()
    result={'name':name,'command':list(map(str,command)),'cwd':str(cwd),'timeout_seconds':limit}
    try:
        with log.open('w',encoding='utf8') as out:
            p=subprocess.run(result['command'],cwd=cwd,env=environment(),stdout=out,stderr=subprocess.STDOUT,timeout=limit)
        result.update(status='COMPLETE' if p.returncode==0 else 'ERROR',exit_code=p.returncode)
    except subprocess.TimeoutExpired:
        result.update(status='TIMEOUT',exit_code=None)
    except OSError as e:
        result.update(status='HOST_EXECUTION_ERROR',exit_code=None,error=str(e))
        log.write_text(str(e))
    result.update(elapsed_seconds=time.perf_counter()-start,log=str(log))
    (HERE/'logs'/f'{name}.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result),flush=True)
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=['versions','rust-pin','rust-build','cabal-init','cabal-update','haskell-build','haskell-rts','haskell-install','smoke','hashes'])
    action=parser.parse_args().action
    if action=='haskell-rts':
        cabal_file=SOURCES/'feynman/Feynman.cabal'
        original=cabal_file.read_bytes()
        start=original.index(b'executable feynopt')
        old=b'ghc-options:         -O2'
        modified=original[:start]+original[start:].replace(old,old+b' -rtsopts -fforce-recomp',1)
        try:
            cabal_file.write_bytes(modified)
            result=job('haskell_rts_build',[HERE/'bin/cabal.exe','--config-file='+str(HERE/'cabal.config'),
                                          'build','exe:feynopt','-j2'],SOURCES/'feynman',1200)
            if result['status']=='COMPLETE':
                built=SOURCES/'feynman/dist-newstyle/build/x86_64-windows/ghc-9.4.8/Feynman-0.1.0.0/x/feynopt/build/feynopt/feynopt.exe'
                shutil.copyfile(built,HERE/'bin/feynopt.exe')
        finally:
            cabal_file.write_bytes(original)
        return
    if action=='versions':
        ghcs=sorted(HERE.glob('ghc-*/bin/ghc.exe'))
        for name,path in [('cabal',HERE/'bin/cabal.exe'),('rustc',HERE/'cargo/bin/rustc.exe'),('cargo',HERE/'cargo/bin/cargo.exe')]+([('ghc',ghcs[0])] if ghcs else []):
            job(name+'_version',[path,'--version'],PROJECT,30)
    if action=='rust-build':
        job('fasttodd_build',[HERE/'cargo/bin/cargo.exe','build','--release','--target-dir',HERE/'fasttodd-target'],SOURCES/'FastTODD',600)
    if action=='rust-pin':
        job('fasttodd_dependency_pin',[HERE/'cargo/bin/cargo.exe','update','-p','ahash','--precise','0.8.11'],SOURCES/'FastTODD',180)
    if action=='smoke':
        src=HERE/'benchmark/inputs/smoke.qc'
        job('feynman_ppf_smoke',[HERE/'bin/feynopt.exe','-ppf','-verify',src],PROJECT,60)
        job('fasttodd_smoke',[HERE/'fasttodd-target/release/quantum_circuit_optimization.exe','FastTODD',src],SOURCES/'FastTODD',60)
        job('fasttodd_smoke_equivalence',[HERE/'bin/feynver.exe',src,SOURCES/'FastTODD/circuits/outputs/smoke.qc'],PROJECT,60)
    if action.startswith('cabal') or action.startswith('haskell'):
        args=[HERE/'bin/cabal.exe','--config-file='+str(HERE/'cabal.config')]
        if action=='cabal-init':args+=['user-config','init','--force']
        if action=='cabal-update':args+=['update']
        if action=='haskell-build':args+=['build','exe:feynopt','exe:feynver','-j2']
        if action=='haskell-install':args+=['install','exe:feynopt','exe:feynver','--installdir='+str(HERE/'bin'),'--install-method=copy','--overwrite-policy=always','-j2']
        job(action,args,SOURCES/'feynman',1200)
    if action=='hashes':
        result={}
        for path in sorted((HERE/'downloads').glob('*')):
            if path.is_file():result[path.name]={'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        (HERE/'download_hashes.json').write_text(json.dumps(result,indent=2))
        print(json.dumps(result,indent=2))


if __name__=='__main__':main()
