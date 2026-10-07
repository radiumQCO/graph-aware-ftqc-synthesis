"""Download public, pinned factory sources for the cost audit; no cloud jobs."""
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen

OUT = Path(__file__).resolve().parent / "sources" / "factories"
GSJ_SHA = "871e68ff6df2f75190b1bfd6351459d1b5a037e3"
LITINSKI_SHA = "8fffa48c2e45d3bb0634559fce6b7b5b45f96966"


def fetch(url):
    return urlopen(Request(url, headers={"User-Agent": "ORCHESTRA-factory-audit"}), timeout=60).read()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    entries = []
    for repo, sha, name in [
        ("Strilanc/magic-state-cultivation", GSJ_SHA, "gsj"),
        ("litinski/magicstates", LITINSKI_SHA, "litinski"),
    ]:
        if sha is None:
            sha = json.loads(fetch(f"https://api.github.com/repos/{repo}/commits?per_page=1"))[0]["sha"]
        tree_url = f"https://api.github.com/repos/{repo}/git/trees/{sha}?recursive=1"
        tree = json.loads(fetch(tree_url))
        if tree.get("truncated"):
            raise RuntimeError("Truncated source tree")
        selected = [item for item in tree["tree"] if item["type"] == "blob"
                    and item["size"] < 1_000_000
                    and (Path(item["path"]).suffix in (".py", ".csv", ".txt", ".md") or item["path"] == "LICENSE")]
        def save(item):
            relative = Path(item["path"])
            if any(p == ".." for p in relative.parts):
                raise RuntimeError("Unsafe source path")
            target = OUT / name / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            url = f"https://raw.githubusercontent.com/{repo}/{sha}/{item['path']}"
            data = fetch(url)
            target.write_bytes(data)
            return {"file": str(target.relative_to(OUT)), "url": url, "sha256": hashlib.sha256(data).hexdigest()}
        with ThreadPoolExecutor(max_workers=8) as pool:
            entries.extend(pool.map(save, selected))
        entries.append({"repository": repo, "commit": sha, "tree_url": tree_url})
    (OUT / "manifest.json").write_text(json.dumps(entries, indent=2), encoding="utf-8")
    print(json.dumps([v for v in entries if "repository" in v], indent=2))
    print(f"Saved {len(entries)-2} public source/statistics files.")


if __name__ == "__main__":
    main()
