"""保存外部业务资料的已知时间和不可覆盖的版本。"""
import hashlib
import json
import sqlite3
from datetime import datetime

def connect(path=':memory:'):
    db = sqlite3.connect(path)
    db.execute('CREATE TABLE IF NOT EXISTS documents (kind TEXT, identity TEXT, revision TEXT, received_at TEXT, body TEXT, digest TEXT, PRIMARY KEY(kind,identity,revision))')
    return db

def receive(db, document):
    for key in ('kind', 'id', 'revision', 'received_at', 'payload'):
        if key not in document:
            raise ValueError('资料缺少字段: ' + key)
    datetime.fromisoformat(document['received_at'])
    if not isinstance(document['payload'], dict):
        raise ValueError('资料正文必须为对象')
    body = json.dumps(document['payload'], ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    digest = hashlib.sha256(body.encode()).hexdigest()
    key = (document['kind'], document['id'], document['revision'])
    found = db.execute('SELECT digest FROM documents WHERE kind=? AND identity=? AND revision=?', key).fetchone()
    if found and found[0] != digest:
        raise ValueError('同一资料版本内容冲突')
    with db:
        db.execute('INSERT OR IGNORE INTO documents VALUES (?,?,?,?,?,?)', (*key, document['received_at'], body, digest))
    return digest

def at(db, kind, known_at):
    cutoff = datetime.fromisoformat(known_at)
    latest = {}
    for identity, revision, received, body, digest in db.execute('SELECT identity,revision,received_at,body,digest FROM documents WHERE kind=? ORDER BY identity,received_at,revision', (kind,)):
        if datetime.fromisoformat(received) > cutoff:
            continue
        marker = (received, revision)
        if identity not in latest or marker > latest[identity][0]:
            latest[identity] = (marker, {'id': identity, 'revision': revision, 'received_at': received, 'payload': json.loads(body), 'digest': digest})
    return [value[1] for _, value in sorted(latest.items())]
