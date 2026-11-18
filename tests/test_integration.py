"""验证来源、指标、区域规则和报告的调用链。"""
import json,unittest
from pathlib import Path
from apec_analysis.evidence import connect,receive
from apec_analysis.report import generate,difference
DATA=json.loads((Path(__file__).resolve().parents[1]/'data/example.json').read_text(encoding='utf8'))
class Chain(unittest.TestCase):
 def setUp(self):self.db=connect(':memory:')
 def tearDown(self):self.db.close()
 def test_report(self):
  for doc in DATA['documents']:receive(self.db,doc)
  a,b=[generate(self.db,t) for t in DATA['known_at']]
  self.assertEqual(a['decisions'][0]['status'],'常态');self.assertEqual(b['decisions'][0]['status'],'关注')
  self.assertEqual(difference(a,b)['changed'],['obs-1']);self.assertEqual(len(b['decisions'][0]['sources']),3)
 def test_repeat_and_conflict(self):
  doc=DATA['documents'][0];self.assertEqual(receive(self.db,doc),receive(self.db,doc))
  changed=json.loads(json.dumps(doc));changed['records'][0]['payload']['value']+=1
  with self.assertRaises(ValueError):receive(self.db,changed)
