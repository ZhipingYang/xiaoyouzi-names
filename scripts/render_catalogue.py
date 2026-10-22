# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""由已审校数据生成正文、旗舰、字库和总控矩阵；仅使用Python标准库。"""
import collections,json,pathlib
from audit_names import audit,TARGETS
P=pathlib.Path(__file__).resolve().parents[1]
def load(n):return json.loads((P/'data'/n).read_text())
def save(n,text): (P/n).write_text(text.rstrip()+'\n')
def blocks(parts):
 out=''
 for part in parts:
  sep='\n' if out.rstrip().endswith('|') and part.startswith('|') else '\n\n'
  out+=(sep if out else '')+part
 return out
R=load('names.json');S=load('sources.json');C=load('characters.json');K=load('rankings.json');BY={x['name']:x for x in R}
FILES={ch:ch+'篇.md' for ch in TARGETS};FILES['双姓']='杨X叶与双姓谐音专篇.md'
INTRO={'史传经世':'先取有根、有度、能润物的经世气质。书泉见学养，淑则见分寸，知津见通达；少用宏大江海和功名口号。','唐宋诗词':'以泉声、水岸、芳草和明丽田园为主。诗意在画面里，名字仍按现代姓名来读；不再以天气句和离愁美句凑数。','诗经楚辞':'《诗经》取礼乐、相悦、草木繁盛与祝福；《楚辞》集中取《橘颂》的独立无私。原诗未讲水的条目，明说水字是新拟，不倒推成古人原句。','孔孟儒家':'以浴沂咏归、知者乐水、时雨化育和原泉有本为纲。德性藏在水的行为里，减少训诫和口号感。','老庄魏晋':'以利物不争、止水可鉴、自然自适为底。柔和同时有界限，清净同时能生长，不把消极退避写成孩子必须接受的人生。','纯粹好听':'先读“杨＋双字”的整体，再看故事。清亮、温润、短促有节是听感目标；出处作为支点，不冒称所有组合均为古典成词。','双姓':'只用“杨X叶”正向结构，或以悦、越、玥作母姓的近音纪念。叶为yè，悦／越／玥为yuè，韵母相近但不是普通话同音；不以烨、晔火象替代补水。'}
COMMON='笔画一律按现代简体字形，杨计7画；单字≤13画，澜15画只豁免单字上限，全名仍≤30画。伊露是唯一整名笔画与原典情绪的显式保留例外：7＋6＋21＝34画。五行水德沿用家庭文化偏好，不作效果测量。'
def account(x):return '＋'.join(f'{c}{v}' for c,v in zip(x['name'],x['strokes']))+'＝'+str(x['total'])+'画'
def tone(x):return x['pinyin']+'（'+'-'.join(map(str,x['tones']))+'）'
def source(x):
 s=S[x['source']];return f'[{s["title"]}]({s["url"]})：“{s["quote"]}”<br>{x["method"]}'
def table(rows,ranking=False):
 a=['| '+('榜位 | ' if ranking else '')+'姓名 | 评级 | 拼音与声调 | 笔画账 | 真典与取法 | 意蕴与水德 |','| '+(':---: | ' if ranking else '')+':--- | :---: | :--- | :--- | :--- | :--- |']
 for i,x in enumerate(rows,1):a.append('| '+(str(i)+' | ' if ranking else '')+f'【{x["name"]}】 | {x["rating"]} | {tone(x)} | {account(x)} | {source(x)} | {x["meaning"]}。<br>{x["water_note"]} |')
 return '\n'.join(a)
def source_notes(rows):
 a=['## 原典上下文与异文']
 for k in dict.fromkeys(x['source'] for x in rows):
  s=S[k];a.append(f'- [{s["title"]}]({s["url"]})：{s["context"]}'+(' '+s['variant'] if s.get('variant') else ''))
 return '\n\n'.join(a)
for ch,n in TARGETS.items():
 a=[x for x in R if x['chapter']==ch];premium=sum(x['rating']=='极品' for x in a)
 # 精选作阅读入口，完整名单只出现一次，避免把榜单引用算成增量。
 heads={'史传经世':['杨润禾','杨育泉','杨知津','杨淑则','杨泉婉','杨书泉'],'唐宋诗词':['杨汀兰','杨溪音','杨月汀','杨兰溪','杨雨知','杨芷汀']}.get(ch,[x['name'] for x in a if x['rating']=='极品'][:6])
 b=[f'# 三字姓名：{ch}篇（{n}名）',INTRO[ch],f'本篇 {n} 个独立名，极品 {premium} 个（{premium/len(a):.1%}）。同首字最多2个，含“清”最多2个；全库完整姓名零重复。评级是本项目审美分级，不是客观鉴定。','## 本篇先看',' · '.join('【'+v+'】' for v in heads),'## 五关与书写口径',COMMON,'听感按普通话连姓做编辑筛；水德逐名列明；原典附可回查全文与上下文；红线核对通规、禁字、字画和声调；终身关以入学、署名和正式称呼做语用筛。上述五关为本库编辑判断。**莆仙、闽南方言仍待家人实际连读；不声称已通过母语实测。**','## 完整推荐名单',table(a),source_notes(a),'## 怎么继续缩小范围','先从“本篇先看”挑出能自然叫出口的三四个，再请家人连读全名、模拟点名和正式称呼。保留名字、删除名字都回写总数据，以免各表出现不同版本。','[查看总控矩阵](./总控矩阵.md) · [查看全库Top40与旗舰](./五行补水女名专篇.md)']
 if ch=='双姓':b.insert(2,'本篇清叶、汀叶为火种；其余为本轮新拟。双姓是纪念关系，不强称每个组合是古籍里的现成词；用叶字的名字必须有水字或源句明确的水岸关系。')
 save(FILES[ch],'\n\n'.join(b))
# 旗舰、十璧、Top40都是对正文的引用，避免虚增独立数。
flag=BY[K['flagship']];alts=[BY[n] for n in K['alternatives']];top=[BY[n] for n in K['top40']]
b=['# 五行补水女名专篇：旗舰、十璧与总榜Top40','小名仍为**小柚子**。家庭偏好仍以水润双木为纲；本轮的取名建议以实际读写、字义与审美为据。全库416个独立名，本篇只作索引，不新增第二套候选。','## 旗舰：杨汀兰',table([flag]),'汀为水边平地，兰为芳草；“岸芷汀兰”是原句直取。杨7＋汀5＋兰5＝17画，2-1-2，字形轻、意象完整；保留为总体旗舰。史传优先看【杨润禾】与【杨育泉】，诗词优先看【杨溪音】与【杨月汀】。','## 备选十璧',table(alts),'## 全库总榜Top40',table(top,True),'## 旧榜如何处理','清嘉：杨7＋清11＋嘉14＝32画；微澜：杨7＋微13＋澜15＝35画。两者均退出推荐，澜的豁免不连带豁免全名。澄、漪、霁、露等字也不再作为普通新增组合的用字。伊露按用户点名保留，34画和《蒹葭》的追寻未得语境均明列，不美化为全无例外。','## 五关与终选',COMMON,'普通话及终身语用已经编辑筛；莆仙、闽南母语实读仍待家人终验。Top40是偏好排序，优先史传与诗词，再兼顾其他文脉；不可把“极品”理解为对全国重名率或方言零谐音的保证。','[查看总控矩阵](./总控矩阵.md)']
save('五行补水女名专篇.md','\n\n'.join(b))
# 字库72字，以正文回引作例，共超过旧版168例的三倍；不虚增成新的推荐。
freq=collections.Counter(''.join(x['name'][1:] for x in R));chars=[c for c,v in freq.most_common() if c not in '叶露'][:71];chars.append('澜')
# 清字仅回引两个，其他字的例子不再展开清字名，控制本页清字姓名种类。
examples={c:[x for x in R if c in x['name'][1:] and (('清' not in x['name']) or x['name'] in ['杨清越','杨清叶'])] for c in chars}
assert len(chars)==72
count=sum(len(a) for a in examples.values());assert count>=504
library=[]
water=set('汀泉沁津涓溪沂泠雨润泓淑川冰雪池洧泗渊洵溱洄澜清源')
for c in chars:
 vals=examples[c];library.append({'character':c,**C[c],'kind':'水字／水物' if c in water else '与水字配合的声义字','examples':[x['name'] for x in vals]})
save('data/library.json',json.dumps(library,ensure_ascii=False,indent=2))
b=['# 单字精选：72字构名库',f'72字，正文回引示例共{count}例（同一姓名可因两个构字分别回引；不是{count}个新增姓名）。旧版56字各3例、约168例，本轮回引数量超过三倍。全库独立推荐仍为416名。','## 用字与组合规则',COMMON,'字库分水字／水物与配合字；兰、芳、玉等配合字不单独宣称补水。回引只是找名字的索引，首字配额适用于独立推荐表；字库不设新的独立候选表，也不以重复引用凑正文数量。例名的出处、声调、笔画与五关均回查原篇。','## 72字与搭配回引','| 字 | 笔画／通规序号 | 构名作用 | 已审校姓名示例 |\n| :--- | :--- | :--- | :--- |']
for x in library:
 c=x['character'];b.append(f'| {c} | {x["strokes"]}画／{x["standard_index"]} | {x["kind"]}；'+('15画仅豁免单字，仍须全名≤30画' if c=='澜' else '具体意蕴随两字关系成立')+' | '+'、'.join(x['examples'])+' |')
b+=['## 读音与边界','溱在溱洧水名中读zhēn，不读qín；洧读wěi，泠读líng，乐在本册读lè。伊露不是字库推荐字例，单列存量豁免。凡改动组合都须重新计算笔画与三字声调，不能因为两个字各自合格就推定整名合格。','## 数据依据','通规底表采用[《通用规范汉字表》8105字的开源转录](https://github.com/jaywcjlove/table-of-general-standard-chinese-characters)，对应[2013年原表发布材料](https://www.unicode.org/L2/L2014/14082-n4508-china.pdf)。简体字画采用[新华字典开源数据](https://github.com/pwxcoo/chinese-xinhua)的strokes字段，按本轮实际用字截取存档；不使用康熙繁体画数。拼音采用pypinyin初值并对溱、洧、泠等字人工覆核。','[回到总控矩阵](./总控矩阵.md)']
save('单字精选-字库篇.md',blocks(b))
# 草稿审校记录：2倍只是优先两篇，明确变体类型和淘汰理由。
d=load('draft-review.json');b=['# 优先两篇：草稿与五关淘汰记录','史传120稿→60名；唐宋200稿→100名。记录包含初稿、修订稿及同源替字对照；对照稿是检验字画和音义的变体，不冒称每一稿都是独立的优质创作。落选稿不是推荐，不受终稿用字上限保护。','听感与终身为编辑判断，水德与原典需结合对应来源查看，红线为可离线复核的硬项；方言全体待家人实读。']
for ch in ['史传经世','唐宋诗词']:
 a=[x for x in d if x['chapter']==ch];b+=['## '+ch,'| 草稿姓名 | 阶段／结论 | 听感／水德／原典／红线／终身 | 理由 |\n| :--- | :--- | :--- | :--- |']
 for x in a:b.append(f'| {x["name"]} | {x["stage"]}／{x["decision"]} | '+ '／'.join(x['gates'])+f' | {x["reason"]} |')
save('草稿淘汰记录.md',blocks(b))
# 总控矩阵：名额、火种、全库声调、逐名声调便于查验。
b=['# 总控矩阵：416名、72字与五关复核','更新日期：2026-10-22。独立推荐只按七篇正文的完整三字姓名计数；旗舰、十璧、Top40、字库均回引，不重复计数。','## 配额与交付','| 篇目 | 前版 | 最低目标 | 本轮独立名 | 倍数 | 极品 | 含清 | 同首字上限 |\n| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |']
base=[10,18,15,11,12,28,13];minimum=[55,95,45,33,36,85,40]
for i,(ch,n) in enumerate(TARGETS.items()):
 a=[x for x in R if x['chapter']==ch];pr=sum(x['rating']=='极品' for x in a)
 b.append(f'| [{ch}](./{FILES[ch]}) | {base[i]} | {minimum[i]} | {len(a)} | {len(a)/base[i]:.2f}倍 | {pr}／{pr/len(a):.1%} | {sum("清" in x["name"] for x in a)} | {max(collections.Counter(x["name"][1] for x in a).values())} |')
b+=['## 火种与换血边界','保留14个火种：'+'、'.join(x['name'] for x in R if x['seed'])+'。其余402个均未命中前版完整姓名和字库裸名示例。前版快照保存在data/previous-names.json；纪事档案为历史材料，不重新纳入推荐。','伊露34画与情绪语境明确例外；澜15画只豁免单字。清嘉、微澜、听雨、秋池、濯缨等旧名不再沿用高位推荐。','## 五关标准与可验证边界','| 关卡 | 本轮执行 | 边界 |\n| :--- | :--- | :--- |\n| 听感 | 普通话连姓、三字声调、近音与姓名语用编辑筛 | 莆仙／闽南待家人实读 |\n| 水德 | 水旁、水物或原典明确水景，逐名列说明 | 配合字不独立宣称属水；家庭文化偏好 |\n| 真典正面 | 原文链接、语境、异文、直取与拟字分别标明 | 不把新拟词伪装成古人成词；伊露明确例外 |\n| 红线 | 通规、禁字、笔画、重复、清字、首字、同调 | 程序检查结构，不能证明全国无人同名 |\n| 终身 | 点名、署名、成年正式称呼的编辑判断 | 评级是审美选择 |','## 总声调矩阵','| 姓名第二字声调→／末字声调↓ | 末字1 | 末字2 | 末字3 | 末字4 |\n| :--- | :---: | :---: | :---: | :---: |']
for t in range(1,5):b.append('| 中字'+str(t)+' | '+' | '.join(str(sum(x['tones'][1:]==[t,u] for x in R)) for u in range(1,5))+' |')
b+=['2-2-2为零；所有三字声调均带姓杨的2声计算。声调频数只是音律检查，不以比例机械决定美感。','## 分篇逐名声调与笔画']
for ch in TARGETS:
 b+=['### '+ch,'| 姓名 | 声调 | 笔画 | 五关结论 |\n| :--- | :--- | :--- | :--- |']
 for x in R:
  if x['chapter']==ch:b.append(f'| {x["name"]} | '+ '-'.join(map(str,x['tones']))+f' | {account(x)} | '+('伊露显式例外，其余编辑筛通过' if x['name']=='杨伊露' else '五关编辑筛通过；方言待实读')+' |')
b+=['## 复核入口','[2倍草稿与淘汰记录](./草稿淘汰记录.md) · [原典与方法](./参考方法与评价框架.md)。离线运行 `python3 scripts/audit_names.py`；由 `python3 scripts/render_catalogue.py` 重新生成正文。源数据在data/names.json，来源在data/sources.json。','字库72字、示例'+str(count)+'例；同名因两个构字分别回引，不重复计入416。旗舰1名、备选10璧与Top40均引用正文。']
save('总控矩阵.md',blocks(b))
if __name__=='__main__':raise SystemExit(audit())
