"""保留决策输入的原始版本及取得时间。"""
import hashlib
import json
import sqlite3
from datetime import datetime

SCHEMA="""
CREATE TABLE IF NOT EXISTS documents (
  source TEXT NOT NULL, document_id TEXT NOT NULL, revision TEXT NOT NULL,
  received_at TEXT NOT NULL, payload_json TEXT NOT NULL, sha256 TEXT NOT NULL,
  PRIMARY KEY(source,document_id,revision)
);
CREATE TABLE IF NOT EXISTS observations (
  kind TEXT NOT NULL, record_id TEXT NOT NULL, revision TEXT NOT NULL,
  document_source TEXT NOT NULL, document_id TEXT NOT NULL,
  document_revision TEXT NOT NULL, valid_from TEXT NOT NULL,
  payload_json TEXT NOT NULL, PRIMARY KEY(kind,record_id,revision),
  FOREIGN KEY(document_source,document_id,document_revision)
    REFERENCES documents(source,document_id,revision)
);
"""

def connect(path):
    db=sqlite3.connect(path)
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript(SCHEMA)
    return db

def receive(db, doc):
    source=doc['source']; identity=doc['document_id']; revision=doc['revision']
    received=datetime.fromisoformat(doc['received_at'])
    payload=json.dumps(doc,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    sha=hashlib.sha256(payload.encode('utf-8')).hexdigest()
    key=(source,identity,revision)
    old=db.execute('SELECT sha256 FROM documents WHERE source=? AND document_id=? AND revision=?',key).fetchone()
    if old and old[0]!=sha:raise ValueError('同一来源版本内容冲突')
    records=doc.get('records',[])
    if not isinstance(records,list):raise ValueError('记录必须是列表')
    with db:
        db.execute('INSERT OR IGNORE INTO documents VALUES(?,?,?,?,?,?)',(*key,received.isoformat(),payload,sha))
        for row in records:
            if not isinstance(row.get('payload'),dict):raise ValueError('记录正文不合法')
            datetime.fromisoformat(row['valid_from'])
            rkey=(row['kind'],row['id'],row['revision'])
            existing=db.execute('SELECT payload_json,document_source,document_id,document_revision FROM observations WHERE kind=? AND record_id=? AND revision=?',rkey).fetchone()
            body=json.dumps(row['payload'],ensure_ascii=False,sort_keys=True,separators=(',',':'))
            if existing and existing!=(body,*key):raise ValueError('同一业务记录版本来源冲突')
            db.execute('INSERT OR IGNORE INTO observations VALUES(?,?,?,?,?,?,?,?)',(*rkey,*key,row['valid_from'],body))
    return sha

def records(db,kind,known_at):
    cutoff=datetime.fromisoformat(known_at)
    rows=db.execute("""SELECT o.record_id,o.revision,o.valid_from,o.payload_json,
      d.source,d.document_id,d.revision,d.received_at,d.sha256
      FROM observations o JOIN documents d ON d.source=o.document_source
       AND d.document_id=o.document_id AND d.revision=o.document_revision
      WHERE o.kind=? ORDER BY o.record_id,d.received_at,o.revision""",(kind,)).fetchall()
    latest={}
    for rid,revision,valid_from,payload,source,doc_id,doc_revision,received_at,sha in rows:
        if datetime.fromisoformat(received_at)>cutoff:continue
        marker=(received_at,revision)
        if rid not in latest or marker>latest[rid][0]:
            latest[rid]=(marker,{'id':rid,'revision':revision,'valid_from':valid_from,
                'payload':json.loads(payload),'source':{'name':source,'document':doc_id,
                'revision':doc_revision,'sha256':sha,'received_at':received_at}})
    return [item[1] for item in sorted(latest.values(),key=lambda item:item[1]['id'])]
