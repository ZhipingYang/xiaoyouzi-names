"""生成好听篇。"""
import json,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
def render():
 rows=json.loads((ROOT/'data/listening-top20.json').read_text());chars=json.loads((ROOT/'data/characters.json').read_text());standard=set((ROOT/'data/standard-characters.txt').read_text().splitlines());notes=json.loads((ROOT/'data/name-notes.json').read_text())
 assert rows and len({x['name'] for x in rows})==len(rows)
 lines=[f'# 纯粹好听篇（{len(rows)}名）','先看现代、自然、日常好叫的名字。', '## 名字','| 姓名 | 拼音 | 简体笔画 | 一句话 |','| :--- | :--- | :--- | :--- |']
 for x in rows:
  n=x['name'];assert x['water'] in n and x['water'] in '清沁润溪泉洛沛雨雪冰淇沂泓' and all(c in standard for c in n)
  st=[chars[c]['strokes'] for c in n];assert max(st)<=13 and sum(st)<=30
  account='＋'.join(str(v) for v in st)+'＝'+str(sum(st))
  lines.append(f'| 【{n}】 | {x["pinyin"]} | {account} | {x["meaning"].rstrip("。 ")}'+('；'+notes[n] if n in notes else '')+' |')
 lines+=['','笔画依次为杨、名字首字、末字。莆仙与闽南方言请家人连读。']
 (ROOT/'纯粹好听篇.md').write_text('\n\n'.join(lines[:3])+'\n\n'+'\n'.join(lines[3:])+'\n');return len(rows)
if __name__=='__main__':print(f'已生成{render()}名。')
