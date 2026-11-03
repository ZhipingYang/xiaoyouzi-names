# -*- coding: utf-8 -*-
"""从逐名审校后的数据生成现行文档。"""
import collections,json,pathlib
from audit_names import audit
from render_shortlist import render as render_shortlist
P=pathlib.Path(__file__).resolve().parents[1]
def load(name):return json.loads((P/'data'/name).read_text())
def save(name,text):(P/name).write_text(text.strip()+'\n')
rows=load('names.json');sources=load('sources.json');chars=load('characters.json');short=load('listening-top20.json');rank=load('rankings.json');byname={r['name']:r for r in rows};unique=set(byname)|{x['name'] for x in short}
files={'史传经世':'史传经世篇.md','唐宋诗词':'唐宋诗词篇.md','诗经楚辞':'诗经楚辞篇.md','孔孟儒家':'孔孟儒家篇.md','老庄魏晋':'老庄魏晋篇.md','双姓':'杨X叶与双姓谐音专篇.md'}
def account(r):return '＋'.join(f'{c}{n}' for c,n in zip(r['name'],r['strokes']))+f'＝{r["total"]}画'
def source_text(r):
 if r['citation_kind']=='自由新拟':return '自由新拟，无确切典源'
 s=sources[r['source']];quote=r.get('citation_quote',s['quote'])
 return f'[{s["title"]}]({s["url"]})：“{quote}”<br>{r["citation_note"]}'
def table(items):
 result=['| 姓名 | 拼音与声调 | 笔画账 | 意象与出处 | 使用时考虑 |','| :--- | :--- | :--- | :--- | :--- |']
 for r in items:
  note=''
  if r['name']=='杨伊露':note='用户指定保留：34画；《蒹葭》有追寻未得的情绪。'
  elif r['name']=='杨兰溪':note='兰溪也是地名，可看是否介意。'
  elif r['name']=='杨春洧':note='洧读wěi，认读成本较高。'
  elif r['name']=='杨溪玥':note='玥近音叶；溪玥与西岳同音，可由家人权衡。'
  elif r['name']=='杨汀玥':note='玥近音叶，汀字常需说明写法。'
  elif r['name']=='杨洵美':note='洵读xún；原文中作“诚然”解，水旁是字形，并非原句写水。'
  elif '汀' in r['name']:note='汀读tīng，字义为水边平地，报名字时可能需说明。'
  else:note='普通话连读后建议家人再以常用方言实读。'
  result.append(f'| 【{r["name"]}】 | {r["pinyin"]}（'+ '-'.join(map(str,r['tones']))+f'） | {account(r)} | {r["meaning"]}。<br>{source_text(r)} | {note} |')
 return '\n'.join(result)
for ch,file in files.items():
 group=[r for r in rows if r['chapter']==ch]
 b=[f'# 三字姓名：{ch}篇（{len(group)}名）','本篇重新逐名审校，优先保留读起来像姓名、两个字之间有自然联系的组合。出处关联不足的条目不再附典。本轮也减少古风和生僻感较重的组合，审美有主观性，排序只供家人比较。','## 本篇候选',table(group)]
 if ch=='双姓':b.insert(1,'叶读yè，悦、玥读yuè，属于近音而非普通话同音；母姓是纪念，不强行解释每个名字。')
 b+=['## 最后再听一遍','请把“杨＋名字”连读，也试着在课堂、工作和日常介绍中使用；莆仙、闽南方言仍需家人按本地口音实读。','[查看总览](./README.md) · [查看审校记录](./草稿淘汰记录.md)']
 save(file,'\n\n'.join(b))
render_shortlist()
# 精选榜保留现有推荐，重叠姓名不重复计入。
lines=['# 补水女名精选','根据本轮听感和字义重排；这些候选来自各篇及好听篇，重复出现只计一个。水字是家庭的文化取向，名字本身不保证五行效果。','## 先比较的名字','| 姓名 | 简体笔画 | 值得看看 |\n| :--- | :--- | :--- |']
S={x['name']:x for x in short}
for n in rank['top40']:
 if n in S:x=S[n];desc=x['meaning'];ct='＋'.join(f'{c}{chars[c]["strokes"]}' for c in n)+'＝'+str(sum(chars[c]['strokes'] for c in n))+'画'
 else:x=byname[n];desc=x['meaning'];ct=account(x)
 lines.append(f'| 【{n}】 | {ct} | {desc} |')
lines+=['## 关于杨汀兰','“汀兰”见范仲淹《岳阳楼记》，水岸兰草的画面完整，全名17画。它依然是一个值得留在名单中的候选；最终选择交给家人，不再写成已替孩子定案。','## 终选提醒','如看重文学出处，可先读对应原典上下文；自由新拟的名字不强加典故。伊露按此前约定单独保留，其34画与原诗追寻未得的语境请一并考虑。方言仍需家人实读。']
save('五行补水女名专篇.md','\n\n'.join(lines[:3])+'\n\n'+'\n'.join(lines[3:-4])+'\n\n'+'\n\n'.join(lines[-4:]))
# 字库只引用现行候选，不再为数量制造例名。
all_names=sorted(unique);lib=[]
for c in sorted(set(''.join(n[1:] for n in all_names))):
 ex=[n for n in all_names if c in n[1:]]
 lib.append({'character':c,**chars[c],'examples':ex})
(P/'data/library.json').write_text(json.dumps(lib,ensure_ascii=False,indent=2)+'\n')
b=['# 单字精选与现行例名',f'从现行候选实际使用的字中整理出{len(lib)}字。下列姓名是回引，同一个名字可能出现在两个字下。','## 选字表','| 字 | 简体画数 | 当前候选举例 |\n| :--- | :---: | :--- |']
for x in lib:b.append(f'| {x["character"]} | {x["strokes"]} | '+'、'.join(x['examples'])+' |')
b+=['## 书写说明','按现代简体计算，杨7画；伊露是此前指定的例外。洵、洧、汀等字虽然是规范字，但可能需要向他人说明读法或写法。']
save('单字精选-字库篇.md','\n\n'.join(b[:3])+'\n\n'+'\n'.join(b[3:-2])+'\n\n'+'\n\n'.join(b[-2:]))
# 审校记录与总控，明确历史草稿已经过时。
review={}
for file in ['review-history.json','review-poetry.json','review-other.json']:review.update(load(file))
oldnames=load('rejections.json')
counts=collections.Counter(x['chapter'] for x in rows)
b=['# 总控矩阵：本轮现行候选',f'五篇文脉与双姓正文共{len(rows)}名；好听篇{len(short)}名，合并去重后共{len(unique)}名。上轮416名与倍率目标不再作为现行数字。','## 各篇','| 篇目 | 当前推荐 |\n| :--- | :---: |']
for ch,file in files.items():b.append(f'| [{ch}](./{file}) | {counts[ch]} |')
b+=['| [纯粹好听](./纯粹好听篇.md) | '+str(len(short))+' |','## 普通话声调矩阵（六篇正文）','| 中字＼末字 | 1声 | 2声 | 3声 | 4声 |\n| :--- | :---: | :---: | :---: | :---: |']
for i in range(1,5):b.append('| '+str(i)+'声 | '+' | '.join(str(sum(x['tones'][1:]==[i,j] for x in rows)) for j in range(1,5))+' |')
b+=['## 判定边界','读音、姓名感和意象是编辑判断；自动校验只核对字形、笔画、声调、去重和引用，不能证明审美好坏、全国重名情况或方言无谐音。伊露34画且原诗有追寻未得的情绪，按此前指定保留。','[逐名审校记录](./草稿淘汰记录.md) · [方法说明](./参考方法与评价框架.md)']
def blocks(parts):
 out=''
 for part in parts:out+= ('\n' if out.rstrip().endswith('|') and part.startswith('|') else '\n\n')+part if out else part
 return out
save('总控矩阵.md',blocks(b))
b=['# 逐名审校记录','对上轮416名逐名复核。现行正文只保留通过本轮筛选的文史与双姓名字；旧音律池统一交给最新好听篇重选。理由为编辑判断，不代表名字本身有绝对好坏。','## 各篇审校','| 姓名 | 本轮处理 | 具体理由 |\n| :--- | :--- | :--- |']
# Preserve individual dispositions even for the formerly hidden sound pool.
for n,x in review.items():
 current='保留' if n in byname else ('好听篇重选' if n in {z['name'] for z in short} else '移出推荐')
 reason=x['reason'].replace('|','／')
 if current=='移出推荐' and x['decision']=='keep': reason='名字可再比较；旧音律池不单独展示，未进入本轮好听精选。'+reason
 b.append(f'| {n} | {current} | {reason} |')
b+=['## 旧草稿','早期120稿／200稿及替字对照保留在data/draft-review.json，属于历史过程，不是当前推荐或本轮评级。']
save('草稿淘汰记录.md',blocks(b))
if __name__=='__main__':raise SystemExit(audit())
