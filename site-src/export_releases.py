"""Exporte les nouveautés de l'application (src/model/whatsnew.ts) en fr / en / es
vers releases.json, pour la page « Nouveautés » du site.

    python3 site-src/export_releases.py /chemin/vers/trame
"""
import json, re, sys
from pathlib import Path

app = Path(sys.argv[1])
src = (app / "src/model/whatsnew.ts").read_text(encoding="utf-8")
STR = r'"((?:[^"\\]|\\.)*)"'

def dictionary(lang):
    d = {}
    for m in re.finditer(r'^\s*' + STR + r':\s*' + STR + r',?\s*$', (app / f"src/i18n/{lang}.ts").read_text(encoding="utf-8"), re.M):
        d[json.loads(f'"{m.group(1)}"')] = json.loads(f'"{m.group(2)}"')
    return d

tr = {"en": dictionary("en"), "es": dictionary("es")}
releases = []
for block in re.findall(r'\{\s*version:\s*"([^"]+)",\s*title:\s*t\(' + STR + r'\),\s*items:\s*\[(.*?)\]\s*,?\s*\}', src, re.S):
    version, title, items = block[0], json.loads(f'"{block[1]}"'), [json.loads(f'"{x}"') for x in re.findall(r't\(' + STR + r'\)', block[2])]
    entry = {"version": version}
    for lang in ("fr", "en", "es"):
        f = (lambda s: s) if lang == "fr" else (lambda s, l=lang: tr[l].get(s, s))
        entry[lang] = {"title": f(title), "items": [f(i) for i in items]}
    releases.append(entry)
out = Path(__file__).with_name("releases.json")
out.write_text(json.dumps(releases, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(releases), "versions →", out)
