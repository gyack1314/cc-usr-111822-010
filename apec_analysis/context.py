"""按当前区域规则解释已比较的指标。"""
from .evidence import records
def decide(db,known_at,comparison):
 if comparison['status']!='可比':return {'id':comparison['id'],'status':'待核实'}
 rules=[r for r in records(db,'rule',known_at) if r['payload']['region']==comparison['region']]
 if not rules:return {'id':comparison['id'],'status':'无规则'}
 rule=rules[-1];p=rule['payload']
 if p['metric']!=comparison['metric'] or p['unit']!=comparison['unit']:return {'id':comparison['id'],'status':'口径不符'}
 hit=comparison['delta']>=p['threshold'] if p['direction']=='above' else comparison['delta']<=p['threshold']
 return {'id':comparison['id'],'status':'关注' if hit else '常态','action':p['action'] if hit else None,'sources':comparison['sources']+[rule['source']['sha256']]}
