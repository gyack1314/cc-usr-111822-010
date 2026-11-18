from .evidence import at
from .cells import workload
def plan(db, known_at):
    technicians={r['payload']['cell']:r for r in at(db,'technician',known_at)};out=[]
    for row in workload(db,known_at):
        tech=technicians.get(row.get('cell'))
        if not tech or 'capacity' not in row:out.append({'order':row['order'],'status':'支援或工位待核'});continue
        out.append({'order':row['order'],'cell':row['cell'],'deliverable':min(row['units'],row['capacity']),'technician':tech['payload']['person']})
    return out
