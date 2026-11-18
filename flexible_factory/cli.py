"""读取业务样例并展示当前结果。"""
import argparse
import json
from pathlib import Path
from .evidence import connect, receive
from .support import plan
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('input')
    args=parser.parse_args()
    data=json.loads(Path(args.input).read_text(encoding='utf-8'))
    db=connect()
    for item in data['documents']:receive(db,item)
    print(json.dumps(plan(db,data['known_at']),ensure_ascii=False,indent=2))
    db.close()
if __name__=='__main__':main()
