"""Check local Markdown destinations and indexed upstream source paths offline."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import json,re
ROOT=Path(__file__).resolve().parents[1]
def main():
    checked=0
    for p in ROOT.rglob('*.md'):
        if '.git' in p.parts:continue
        for target in re.findall(r'\]\(([^\s)]+)\)',p.read_text(encoding='utf-8')):
            u=urlsplit(target)
            if u.scheme or not u.path:continue
            path=(p.parent/unquote(u.path)).resolve()
            assert path.is_relative_to(ROOT) and path.exists(),(p.relative_to(ROOT),target)
            checked+=1
    paths=json.loads((ROOT/'resources/classic_source_paths.json').read_text(encoding='utf-8'))
    available={f'https://github.com/{r["repo"]}/blob/{r["branch"]}/{p}' for r in paths for p in r['paths']}
    code=(ROOT/'docs/CLASSIC_CODE_INDEX_CN.md').read_text(encoding='utf-8')
    urls=re.findall(r'https://github.com/[^\s)]+/blob/[^\s)]+',code)
    assert len(urls)==18 and set(urls).issubset(available)
    print(json.dumps({'status':'PASS','local_links_checked':checked,'upstream_source_paths_matched_to_verified_tree':len(urls)}))
if __name__=='__main__':main()
