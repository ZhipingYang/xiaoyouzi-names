# 数据说明

- `names.json`：本轮审校后，五篇文脉与双姓正文的51名。每名保留读音、简体笔画、意义与是否使用原典的说明。
- `listening-top20.json`：最新好听篇21名。文件名沿用历史名称；可与正文有交集，合并去重65名。
- `review-history.json`、`review-poetry.json`、`review-other.json`：对上轮416条逐一给出取舍理由。`草稿淘汰记录.md`提供历史审校摘要。
- `rankings.json`、`library.json`：只引用上述现行候选；榜单为编辑推荐，非定案。
- `sources.json`：原典与上下文数据；自由新拟名不标出处；可核实的原典注明取法。
- `characters.json`与`standard-characters.txt`：简体笔画及规范字表底稿。字表来自[jaywcjlove/table-of-general-standard-chinese-characters](https://github.com/jaywcjlove/table-of-general-standard-chinese-characters)，笔画来自[pwxcoo/chinese-xinhua](https://github.com/pwxcoo/chinese-xinhua)；对应MIT许可在本目录。
- `previous-names.json`、`draft-review.json`、`rejections.json`、`source-verification.json`：历史版本的旧库、草稿和2026年10月原典引文快照。它们不是现行推荐，也不因本次审校而自动更新成新的核验报告。

`python3 scripts/render_catalogue.py`生成文档；`python3 scripts/audit_names.py`核对现行结构。审美、出处关联和方言不能仅靠程序证明。
