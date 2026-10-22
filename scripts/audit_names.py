# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""离线校验本轮推荐库；不把审美评分或方言实读伪装成程序证明。"""
import collections,json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
def read(n): return json.loads((ROOT/'data'/n).read_text())
TARGETS={'史传经世':60,'唐宋诗词':100,'诗经楚辞':48,'孔孟儒家':36,'老庄魏晋':40,'纯粹好听':88,'双姓':44}
BAN=set('梓宸轩泽睿浩宇辰奕诺汐霖涵沫沐')
def audit():
 rows=read('names.json');sources=read('sources.json');chars=read('characters.json');old=set(read('previous-names.json'));standard=(ROOT/'data/standard-characters.txt').read_text().splitlines();errors=[]
 def check(ok,msg):
  if not ok:errors.append(msg)
 names=[r['name'] for r in rows]
 check(len(names)==len(set(names)),'跨篇完整姓名重复')
 check(len(standard)==8105 and len(set(standard))==8105,'通规底表应为8105个不同字')
 seeds=[r for r in rows if r['name'] in old];check(len(seeds)<=14,'火种超过14')
 for r in rows:
  n=r['name'];check(len(n)==3 and n[0]=='杨',n+'：非三字杨姓名')
  check(r['source'] in sources,n+'：来源缺失');check(len(r['meaning'])>=8,n+'：意蕴缺失')
  check(all(c in standard for c in n),n+'：非通规字');check(not BAN.intersection(n),n+'：禁字')
  strokes=[chars[c]['strokes'] for c in n];check(strokes==r['strokes'] and sum(strokes)==r['total'],n+'：笔画账错')
  if n!='杨伊露':
   check(all(v<=13 or (c=='澜' and v==15) for c,v in zip(n,strokes)),n+'：单字超画')
   check(sum(strokes)<=30,n+'：全名超30画')
  check(len(set(r['tones']))>1,n+'：三连同调');check(r['tones'][0]==2 and all(t in range(1,5) for t in r['tones']),n+'：声调非法')
  check('叶' not in n or n.endswith('叶'),n+'：叶必须收尾')
  check(r['seed']==(n in old),n+'：火种标记与快照不一致')
  check(all(c in n for c in r['water']),n+'：水字备注与姓名不一致')
  check(len(r['gates'])==5,n+'：五关记录缺失');check('待家人' in r['dialect'],n+'：方言状态误标')
  check(bool(r['water']) or r.get('water_note'),n+'：水德依据缺失')
 for ch,target in TARGETS.items():
  a=[r for r in rows if r['chapter']==ch];check(len(a)==target,ch+'：数量不足或统计漂移')
  first=collections.Counter(r['name'][1] for r in a);check(max(first.values())<=2,ch+'：同首字超过2')
  check(sum('清' in r['name'] for r in a)<=2,ch+'：清字超过2')
  check(sum(r['rating']=='极品' for r in a)/len(a)>=.4,ch+'：极品不足40%')
 # 旗舰、Top40为索引不算新增；同首字与清限额也独立检查。
 for label,key,count in [('十璧','alternatives',10),('总榜','top40',40)]:
  if (ROOT/'data/rankings.json').exists():
   selected=read('rankings.json')[key];check(len(selected)==count and len(set(selected))==count,label+'：数量或去重失败')
   check(set(selected)<=set(names),label+'：引用库外名字')
   check(max(collections.Counter(n[1] for n in selected).values())<=2,label+'：首字超限')
   check(sum('清' in n for n in selected)<=2,label+'：清字超限')
 if (ROOT/'data/library.json').exists():
  library=read('library.json');check(len(library)==72 and len({x['character'] for x in library})==72,'字库不是72个不同字')
  check(sum(len(x['examples']) for x in library)>=504,'字库例名回引不足旧版三倍')
  for x in library:
   check(all(n in names and x['character'] in n[1:] for n in x['examples']),'字库回引不一致：'+x['character'])
 if (ROOT/'data/draft-review.json').exists():
  draft=read('draft-review.json')
  for ch,amount in [('史传经世',120),('唐宋诗词',200)]:
   a=[x for x in draft if x['chapter']==ch];check(len(a)>=amount and len({x['name'] for x in a})==len(a),ch+'：草稿不足2倍或重复计数')
   check({x['name'] for x in a if x['decision']=='保留'}=={x['name'] for x in rows if x['chapter']==ch},ch+'：草稿保留记录与终稿不一致')
 if (ROOT/'data/source-verification.json').exists():
  proof=read('source-verification.json');check({x['source'] for x in proof}==set(sources),'来源快照不全')
  check(all(x['status']==200 and x['quote_found'] for x in proof),'原典快照存在未命中引文')
 if errors:
  print('\n'.join(errors));return 1
 print(f'PASS：{len(rows)}个独立推荐，{len(seeds)}个火种，{len(rows)-len(seeds)}个新名；字画、通规、禁字、分篇配额、声调、查重全部通过。')
 for ch in TARGETS:
  a=[r for r in rows if r['chapter']==ch];print(f'{ch}：{len(a)}名，极品{sum(r["rating"]=="极品" for r in a)}名')
 print('五关含人工编辑判断；方言尚待家人实读。')
 return 0
if __name__=='__main__':sys.exit(audit())
