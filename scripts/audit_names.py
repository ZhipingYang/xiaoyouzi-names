# -*- coding: utf-8 -*-
"""验证现行推荐的数据一致性；审美与方言不能自动证明。"""
import json,pathlib,sys,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(name): return json.loads((ROOT/'data'/name).read_text())
TARGETS={'史传经世':None,'唐宋诗词':None,'诗经楚辞':None,'孔孟儒家':None,'老庄魏晋':None,'纯粹好听':None,'双姓':None}
def audit():
 rows=read('names.json'); shortlist=read('listening-top20.json'); chars=read('characters.json'); sources=read('sources.json'); standard=set((ROOT/'data/standard-characters.txt').read_text().splitlines()); ranks=read('rankings.json'); errors=[]
 def check(ok,msg):
  if not ok: errors.append(msg)
 names=[r['name'] for r in rows];check(len(names)==len(set(names)),'正文姓名重复')
 for r in rows:
  n=r['name'];check(len(n)==3 and n.startswith('杨'),n+'格式');check(all(c in standard and c in chars for c in n),n+'规范字')
  check(r['citation_kind']=='自由新拟' or r.get('source') in sources,n+'来源缺失');check(r['strokes']==[chars[c]['strokes'] for c in n] and r['total']==sum(r['strokes']),n+'笔画')
  if n!='杨伊露':check(max(r['strokes'])<=13 and r['total']<=30,n+'笔画超限')
  check(len(r['tones'])==3 and r['tones'][0]==2 and len(set(r['tones']))>1,n+'声调')
  if r.get('citation_kind')=='原句直取':check(n[1:] in sources[r['source']]['quote'],n+'并非原句连词')
  check(r['chapter'] in TARGETS,n+'篇目无效')
 shortlist_names=[r['name'] for r in shortlist];check(len(shortlist_names)==len(set(shortlist_names)),'听感精选重复')
 for r in shortlist:
  n=r['name'];check(all(c in standard and c in chars for c in n),n+'精选规范字');check(r['water'] in n,n+'精选水字')
  check(sum(chars[c]['strokes'] for c in n)<=30 and max(chars[c]['strokes'] for c in n)<=13,n+'精选笔画')
 for ch in TARGETS:
  subset=shortlist if ch=='纯粹好听' else [x for x in rows if x['chapter']==ch]
  check(any('洛' in x['name'] for x in subset) and any('沛' in x['name'] for x in subset),ch+'：缺少洛或沛')
 available=set(names)|set(shortlist_names)
 for n in [ranks['flagship']]+ranks['alternatives']+ranks['top40']:check(n in available,n+'榜单引用未收录姓名')
 library=read('library.json')
 for item in library:
  for n in item['examples']:check(n in available and item['character'] in n,n+'字库引用错误')
 if errors:print('\n'.join(errors));return 1
 print('通过：正文',len(rows),'名；听感精选',len(shortlist),'名；合并去重',len(available),'名。')
 for ch in TARGETS:
  if ch!='纯粹好听':print(ch,sum(x['chapter']==ch for x in rows),'名')
 print('规范字、简体笔画、声调、引用和去重已检查；审美及莆仙／闽南实读仍需家人判断。')
 return 0
if __name__=='__main__':sys.exit(audit())
