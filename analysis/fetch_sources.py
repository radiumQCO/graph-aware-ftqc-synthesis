"""Fetch immutable public inputs used by the TFIM audit (no cloud job)."""
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "sources"
SOURCES = {
    "microsoft_dynamics_2022.ipynb": "https://raw.githubusercontent.com/microsoft/Quantum/d78c2c0348048a13c04da5f69aba3810914f268f/samples/azure-quantum/resource-estimation/estimation-dynamics.ipynb",
    "microsoft_dynamics_2023.ipynb": "https://raw.githubusercontent.com/microsoft/Quantum/f92f2074507696224fae440e4164d2751754fa2c/samples/azure-quantum/resource-estimation/estimation-dynamics.ipynb",
}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, url in SOURCES.items():
        raw = urlopen(Request(url, headers={"User-Agent": "ORCHESTRA-literature-audit"}), timeout=60).read()
        (OUT / name).write_bytes(raw)
        manifest.append({"file": name, "url": url, "sha256": hashlib.sha256(raw).hexdigest()})
        nb = json.loads(raw)
        text = "\n\n".join("".join(c["source"]) for c in nb["cells"])
        (OUT / name.replace(".ipynb", ".txt")).write_text(text, encoding="utf-8")
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
