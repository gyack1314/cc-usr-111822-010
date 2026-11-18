"""对同口径观测和参照形成单期偏离。"""
from .evidence import records
def compare(db,known_at):
 observations=records(db,'observation',known_at);references=records(db,'reference',known_at)
 result=[]
 for obs in observations:
  p=obs['payload'];matches=[r for r in references if all(r['payload'][k]==p[k] for k in ('metric','region','unit'))]
  if not matches:result.append({'id':obs['id'],'status':'无参照'});continue
  ref=matches[-1]
  result.append({'id':obs['id'],'region':p['region'],'metric':p['metric'],'unit':p['unit'],'delta':p['value']-ref['payload']['value'],'sources':[obs['source']['sha256'],ref['source']['sha256']],'status':'可比'})
 return result
