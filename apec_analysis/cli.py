"""从本地合成资料形成两个已知时间的报告。"""
import argparse,json
from pathlib import Path
from .evidence import connect,receive
from .report import generate,difference
def main():
 p=argparse.ArgumentParser();p.add_argument('command',choices=['inspect']);p.add_argument('input');args=p.parse_args()
 data=json.loads(Path(args.input).read_text(encoding='utf8'));db=connect(':memory:')
 for doc in data['documents']:receive(db,doc)
 a,b=[generate(db,t) for t in data['known_at']]
 print(json.dumps({'before':a,'after':b,'change':difference(a,b)},ensure_ascii=False,indent=2));db.close()
if __name__=='__main__':main()
