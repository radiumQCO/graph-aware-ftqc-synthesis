"""Bounded, logged attempts; a timeout is NOT an optimizer result."""
import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import time
from pathlib import Path
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parent.parent
PYTHON=PROJECT/'analysis/.compiler_venv/Scripts/python.exe'
ENV=os.environ.copy()
ENV['PYTHONPATH']=str(PROJECT/'analysis/sources/compilers/wheel_runtime')+';'+str(Path(sys.base_prefix)/'Lib/site-packages')

def run(job):
    start=time.perf_counter(); out=HERE/'logs'/f'{job["id"]}.log';out.parent.mkdir(exist_ok=True)
    env=ENV.copy()
    if job.get('python_path_prefix'):env['PYTHONPATH']=job['python_path_prefix']+';'+env['PYTHONPATH']
    try:
        with out.open('w',encoding='utf8') as f:
            p=subprocess.run(job['command'],cwd=PROJECT,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=job['timeout'])
        status='COMPLETE' if p.returncode==0 else 'ERROR'
        code=p.returncode
    except subprocess.TimeoutExpired: status='TIMEOUT';code=None
    except OSError as e:
        status='HOST_EXECUTION_ERROR';code=None
        out.write_text(repr(e))
    result=dict(job,status=status,exit_code=code,elapsed_seconds=time.perf_counter()-start,log=str(out))
    (HERE/'logs'/f'{job["id"]}.json').write_text(json.dumps(result,indent=2))
    print(job['id'],status,round(result['elapsed_seconds'],2),flush=True)
    return result

def jobs(kind):
    script=str(HERE/'optimize.py')
    if kind=='basic':
        for mode in ('qualtran_literal','even_tower','graph_tower'):
            for family in ('X_boundary','X_common','X_mixed','ZZ_common','ZZ_central'):
                yield dict(id=f'basic_{mode}_{family}',command=[str(PYTHON),'-u',script,'--mode',mode,'--family',family,'--method','basic','--skip-verify'],timeout=120)
    if kind=='strong':
        for mode in ('qualtran_literal','even_tower','graph_tower'):
            for method in ('todd','teleport'):
                yield dict(id=f'{method}_{mode}_ZZ_common',command=[str(PYTHON),'-u',script,'--mode',mode,'--method',method,'--skip-verify'],timeout=180)
    if kind=='full':
        for mode in ('even_tower','graph_tower'):
            for method in ('basic','todd','teleport'):
                yield dict(id=f'full_{method}_{mode}',command=[str(PYTHON),'-u',script,'--mode',mode,'--method',method,'--scope','full','--skip-verify'],timeout=180)
    if kind=='feynman':
        exe=PROJECT/'analysis/sources/compilers/feynman-windows-0.1.0/bin/feynopt.exe'
        for mode in ('qualtran_literal','even_tower','graph_tower'):
            src=HERE/'circuits'/f'{mode}__full.input.qasm'
            yield dict(id=f'feynman2019_full_{mode}',command=[str(exe),'-O2',str(src)],timeout=180)
    if kind=='surgery':
        env_runtime=PROJECT/'analysis/sources/compilers/topols_runtime'
        for mode in ('even_tower','graph_tower'):
            for variant in ('input','optimized'):
                yield dict(id=f'topols_{mode}_{variant}',command=[str(PYTHON),'-u',str(HERE/'surgery.py'),'topols','--mode',mode,'--variant',variant],timeout=240,
                           python_path_prefix=str(env_runtime))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('kind',choices=['basic','strong','full','feynman','surgery']);p.add_argument('--workers',type=int,default=2)
    a=p.parse_args()
    with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
        results=list(pool.map(run,jobs(a.kind)))
    (HERE/f'{a.kind}_attempts.json').write_text(json.dumps(results,indent=2))
