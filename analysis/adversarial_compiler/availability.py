"""Capture public source revisions and local toolchain evidence."""
import hashlib
import json
import shutil
import subprocess
import urllib.request
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'sources/compilers'

def command(args,cwd=None):
    p=subprocess.run(args,cwd=cwd,capture_output=True,text=True,errors='replace',timeout=25)
    return dict(exit_code=p.returncode,stdout=p.stdout.strip(),stderr=p.stderr.strip())

def main():
    result={'tools':{t:shutil.which(t) for t in ('ghc','cabal','stack','rustc','cargo','gcc','cl','java','wsl')},
            'sources':{},'public_api':{}}
    for name in ('feynman','FastTODD','TopoLS','wisq'):
        root=SOURCE/name
        result['sources'][name]={'revision':command(['git','rev-parse','HEAD'],root),
                                'last_commit':command(['git','log','-1','--format=%cI'],root),
                                'origin':command(['git','remote','get-url','origin'],root)}
    for key,url in {
        'Feynman_releases':'https://api.github.com/repos/meamy/feynman/releases',
        'FastTODD_releases':'https://api.github.com/repos/VivienVandaele/quantum-circuit-optimization/releases',
        'FlowRouter_repository_search':'https://api.github.com/search/repositories?q=FlowRouter+quantum',
    }.items():
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'ORCHESTRA-compiler-audit'})
            with urllib.request.urlopen(req,timeout=25) as f:
                obj=json.load(f)
            result['public_api'][key]={'url':url,'response':obj}
        except Exception as e: result['public_api'][key]={'url':url,'error':str(e)}
    (HERE/'availability.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
