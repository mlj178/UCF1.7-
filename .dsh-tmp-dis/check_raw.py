
import json, urllib.request, urllib.parse
q = urllib.parse.urlencode({"dir":"maps","file":"00_练习场.json"})
d = json.load(urllib.request.urlopen("http://127.0.0.1:8765/api/raw?" + q))
print("keys:", sorted(d.keys()))
print("nodes:", len(d.get("nodes") or []), "edges:", len(d.get("edges") or []), "fp:", d["map"]["fingerprint"], "level:", d["map"]["level"])
