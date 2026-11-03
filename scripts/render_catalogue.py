# -*- coding: utf-8 -*-
"""从逐名审校后的数据生成现行文档。"""
import collections,json,pathlib
from audit_names import audit
from render_shortlist import render as render_shortlist
P=pathlib.Path(__file__).resolve().parents[1]
def load(name):return json.loads((P/'data'/name).read_text())
def save(name,text):(P/name).write_text(text.strip()+'\n')
rows=load('names.json');sources=load('sources.json');chars=load('characters.json');short=load('listening-top20.json');rank=load('rankings.json');notes=load('name-notes.json');byname={r['name']:r for r in rows};unique=set(byname)|{x['name'] for x in short}
files={'史传经世':'史传经世篇.md','唐宋诗词':'唐宋诗词篇.md','诗经楚辞':'诗经楚辞篇.md','孔孟儒家':'孔孟儒家篇.md','老庄魏晋':'老庄魏晋篇.md','双姓':'杨X叶与双姓谐音专篇.md'}
def account(r):return '＋'.join(f'{c}{n}' for c,n in zip(r['name'],r['strokes']))+f'＝{r["total"]}画'
def source_text(r):
 if r['citation_kind']=='自由新拟':return ' · 新拟'
 source=sources[r['source']]
 return f' · [{source["title"]}]({source["url"]})（{r["citation_note"]}）'
def table(items):
 result=['| 姓名 | 拼音 | 简体笔画 | 简意 / 出处 |','| :--- | :--- | :--- | :--- |']
 for r in items:
  note=('；'+notes[r['name']]) if r['name'] in notes else ''
  account='＋'.join(str(n) for n in r['strokes'])+'＝'+str(r['total'])
  result.append(f'| 【{r["name"]}】 | {r["pinyin"]} | {account} | {r["meaning"]}{source_text(r)}{note} |')
 return '\n'.join(result)
for ch,file in files.items():
 group=[r for r in rows if r['chapter']==ch]
 front={
  '史传经世':['杨洛安','杨沛安','杨润禾','杨沛文'],
  '唐宋诗词':['杨洛兰','杨沛欣','杨沛晴','杨洛星','杨溪音'],
  '诗经楚辞':['杨洛妍','杨沛柔','杨沛茹','杨清婉'],
  '孔孟儒家':['杨洛心','杨沛思','杨洛思','杨时雨'],
  '老庄魏晋':['杨洛宁','杨沛宁','杨洛雯','杨沛宜'],
  '双姓':['杨清叶','杨沛悦','杨沁悦','杨洛玥'],
 }.get(ch,[])
 position={name:i for i,name in enumerate(front)}
 mixed=sorted(group,key=lambda r:position.get(r['name'],len(position)))
 intro='篇目按气质分组；“新拟”并非典出本篇。笔画依次为杨、名字首字、末字。'
 if ch=='双姓':intro+=' 悦、玥与叶为近音。'
 save(file,'\n\n'.join([f'# {ch}篇（{len(group)}名）',intro,'## 名字',table(mixed)]))
render_shortlist()
# 精选榜保留现有推荐，重叠姓名不重复计入。
lines=['# 补水女名精选','先看现代、自然的名字，洛、沛也在其中。' ,'## 先比较的名字','| 姓名 | 简体笔画 | 值得看看 |\n| :--- | :--- | :--- |']
S={x['name']:x for x in short}
for n in rank['top40']:
 if n in S:x=S[n];desc=x['meaning'];ct='＋'.join(f'{c}{chars[c]["strokes"]}' for c in n)+'＝'+str(sum(chars[c]['strokes'] for c in n))+'画'
 else:x=byname[n];desc=x['meaning'];ct=account(x)
 lines.append(f'| 【{n}】 | {ct} | {desc.rstrip("。")}'+('；'+notes[n] if n in notes else '')+' |')
lines+=['## 使用提醒','伊露34画为此前指定的例外；方言请家人实读。']
save('五行补水女名专篇.md','\n\n'.join(lines[:3])+'\n\n'+'\n'.join(lines[3:-2])+'\n\n'+'\n\n'.join(lines[-2:]))
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
b=['# 历史审校记录','上轮对416个候选逐名筛选，移除了生硬拼字及牵强附会。','## 保留记录','逐名意见保存在 `data/review-history.json`、`data/review-poetry.json` 与 `data/review-other.json`；本轮新拟洛、沛候选不属于该历史记录。','[查看现行名单](./README.md)']
save('草稿淘汰记录.md','\n\n'.join(b))
# 导航数量来自实际数据。
import re
html=(P/'index.html').read_text()
labels={'史传经世篇.md':f'史传经世 · {counts["史传经世"]}名','唐宋诗词篇.md':f'唐宋诗词 · {counts["唐宋诗词"]}名','诗经楚辞篇.md':f'诗经楚辞 · {counts["诗经楚辞"]}名','孔孟儒家篇.md':f'孔孟儒家 · {counts["孔孟儒家"]}名','老庄魏晋篇.md':f'老庄魏晋 · {counts["老庄魏晋"]}名','纯粹好听篇.md':f'好听易写 · 精选{len(short)}名','杨X叶与双姓谐音专篇.md':f'杨X叶双姓 · {counts["双姓"]}名','单字精选-字库篇.md':f'单字精选 · {len(lib)}字'}
for filename,label in labels.items():
 pattern=r"(\['"+re.escape(filename)+r"', ')[^']*('\])"
 html,n=re.subn(pattern,lambda m:m.group(1)+label+m.group(2),html)
 assert n==1,(filename,n)
save('index.html',html)
readme=['# 小柚子的取名册','杨姓女宝，小名小柚子。先看现代、自然、日常好叫的名字；洛、沛已融入各篇。','[打开在线取名册](https://zhipingyang.github.io/xiaoyouzi-names/)','## 各篇','| 篇目 | 候选 |','| :--- | :---: |']
for ch,file in files.items():readme.append(f'| [{ch}](./{file}) | {counts[ch]} |')
readme.append(f'| [纯粹好听](./纯粹好听篇.md) | {len(short)} |')
readme+=['',f'合并去重 **{len(unique)} 名**。篇目按气质分组；没有标注出处的名字是自由新拟。现行名字已逐条复核，必要的同音与语境提示附在名字旁。','[综合精选](./五行补水女名专篇.md) · [字库](./单字精选-字库篇.md) · [总控矩阵](./总控矩阵.md)','', '笔画按现代简体计算；伊露34画按此前约定保留。莆仙、闽南方言请家人实读。','', '更新：`python3 scripts/render_catalogue.py`；检查：`python3 scripts/audit_names.py`。']
save('README.md',blocks([part for part in readme if part]))
if __name__=='__main__':raise SystemExit(audit())
