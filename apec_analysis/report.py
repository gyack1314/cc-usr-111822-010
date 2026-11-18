"""保留已知时点报告，比较区域判断变化。"""
import hashlib,json
from .metrics import compare
from .context import decide
def generate(db,known_at):
 measures=compare(db,known_at);decisions=[decide(db,known_at,row) for row in measures]
 out={'known_at':known_at,'measurements':measures,'decisions':decisions}
 out['fingerprint']=hashlib.sha256(json.dumps(out,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
 return out
def difference(a,b):
 old={r['id']:r for r in a['decisions']};new={r['id']:r for r in b['decisions']}
 return {'before':a['fingerprint'],'after':b['fingerprint'],'changed':sorted(k for k in old.keys()|new.keys() if old.get(k)!=new.get(k))}
