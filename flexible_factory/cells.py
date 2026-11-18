from .evidence import at
from .orders import demand
def workload(db, known_at):
    cells={r['id']:r for r in at(db,'cell',known_at)};out=[]
    for order in demand(db,known_at):
        cell=cells.get(order['cell'])
        if not cell:out.append({'order':order['order'],'status':'工位待核'});continue
        out.append({**order,'robot':cell['payload']['robot'],'capacity':cell['payload']['capacity'],'cell_source':cell['digest']})
    return out
