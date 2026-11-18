from .evidence import at
def demand(db, known_at):
    return [{'order':r['id'],**r['payload'],'source':r['digest']} for r in at(db,'order',known_at)]
