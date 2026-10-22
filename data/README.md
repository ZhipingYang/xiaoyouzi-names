# 数据说明

- `names.json`：416个独立推荐的唯一事实源，含声调、笔画、原典引用、编辑五关与方言待验状态。
- `sources.json`：68个已使用的来源条目，63个不同公版原典全文链接；不同章句可共用同一全文。
- `source-verification.json`：2026-10-22在线抓取核对快照，记录HTTP状态、原文短句命中及抓取文本SHA256。状态是核对当日快照，不保证网站未来永远可用；匹配成功证明引文存在，不代替语境编辑判断。
- `characters.json`：实际用字的现代简体笔画与通规序号；没有把康熙画数混入。
- `standard-characters.txt`：8105字通规底表的开源转录，来自[jaywcjlove/table-of-general-standard-chinese-characters](https://github.com/jaywcjlove/table-of-general-standard-chinese-characters)。MIT许可见同目录LICENSE.standard-characters。
- 笔画字段摘自[pwxcoo/chinese-xinhua](https://github.com/pwxcoo/chinese-xinhua)。MIT许可见同目录LICENSE.chinese-xinhua。保留来源，未复制完整辞典释文。
- `previous-names.json`：改动前基线 `71ec82453f4f7e9f26ab4c4bcdc11858546a66f1`；从该版所有Markdown抽取完整三字杨姓名，并补入字库反引号里的两字裸名示例。共228个旧名字串，含历史档案中的非推荐名，采取较保守的换血边界。
- `draft-review.json`：史传120稿与唐宋200稿的保留／落选记录；显式区分同源替字对照，不混算独立推荐。
- `rejections.json`：其余修订过程中的落选条目与理由，可能重复记录同名的不同审校阶段，不纳入推荐库查重分母。
- `rankings.json`：旗舰、十璧与Top40，只引用正文姓名。
- `library.json`：72字的615次例名回引；同一个名字可在两个构字下分别引用，不冒充615个独立姓名。

运行`python3 scripts/render_catalogue.py`生成文档，再执行`python3 scripts/audit_names.py`。两者只依赖Python标准库；拼音已人工复核并固化，无需安装字音库。审美、现代姓名感和原典正面语境是人工编辑结论；方言仍待家人实读。
