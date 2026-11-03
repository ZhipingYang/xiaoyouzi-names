"""生成好听篇精选；独立于保留的416名候选池。"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]


def render():
    rows = json.loads((ROOT / 'data/listening-top20.json').read_text())
    chars = json.loads((ROOT / 'data/characters.json').read_text())
    standard = set((ROOT / 'data/standard-characters.txt').read_text().splitlines())
    assert len(rows) == 20 and len({r['name'] for r in rows}) == 20
    parts = [
        '# 纯粹好听篇：带水、易认、好写的20名',
        '更新于2026年10月23日。女宝，杨姓，小名小柚子。按最新偏好重选：连姓顺口、明确带水、日常易认、字形清楚。以下是我的主观听感排序，先看前六名。',
        '这次水字只用清、沁、润、溪、泉：前四字带三点水，泉直接指泉水。用这条直观口径承接家里的五行水偏好；不把名字字义解释成命理效果。十月、重阳、母姓近音均为加分项，不作入选条件。',
        '用字以日常识读和书写为准：本表单字最多13画，全名最多29画。沁读qìn；溪13画，熟悉但不算笔画最少。湜、泠、洧、溱等低频认读字不进入本表。',
        '同一个字可以反复出现；不设出处数量、同首字配额或“极品”比例。各名按字义新拟或重新选入，以下解释是构名心意，不冒充古籍原句。',
        '## 按听感排序',
        '| 排名 | 姓名 | 读音 | 水字 | 简体笔画账 | 气质与心意 | 实际使用感 |\n| :---: | :--- | :--- | :---: | :--- | :--- | :--- |'
    ]
    lines = []
    for i, r in enumerate(rows, 1):
        name = r['name']
        assert len(name) == 3 and name.startswith('杨')
        assert r['water'] in '清沁润溪泉' and r['water'] in name
        assert all(c in standard for c in name)
        strokes = [chars[c]['strokes'] for c in name]
        assert max(strokes) <= 13 and sum(strokes) <= 29
        account = '＋'.join(f'{c}{n}' for c, n in zip(name, strokes)) + f'＝{sum(strokes)}画'
        lines.append(f'| {i} | 【{name}】 | {r["pinyin"]} | {r["water"]} | {account} | {r["meaning"]} | {r["note"]} |')
    parts[-1] += '\n' + '\n'.join(lines)
    parts += [
        '## 我会先拿给家人念的六个',
        '**杨清禾、杨溪宁、杨沁安、杨清悦、杨润禾、杨溪月。**',
        '清禾清新温暖，溪宁柔和舒展，沁安轻巧好写，清悦明快好叫，润禾温厚自然，溪月有水月相映的画面。偏爱简洁看沁安，偏爱温柔看溪宁，想保留十月和母姓近音看溪月或清悦。',
        '## 怎么最后挑',
        '把全名各叫几遍，再试“我是杨××”“杨××同学”“杨××女士”。请家人用莆仙话、闽南话实读；本表只做普通话听感判断。沁、予、妍虽不是刻意选的生僻字，口头报名字仍可能需要说明写法。',
        '## 本篇与原候选池',
        '本篇已从原88名展示改为20名精选，允许从其他篇重选、恢复旧候选及新增创作。原416名候选池仍保存在data/names.json，总控矩阵与原榜单属于此前版本，不能把本表当成它们的同一份排名。本表数据在data/listening-top20.json，运行python3 scripts/render_shortlist.py可重新生成；全册生成器也会调用它。',
        '[返回取名册](./README.md)'
    ]
    (ROOT / '纯粹好听篇.md').write_text('\n\n'.join(parts) + '\n')
    return len(rows)


if __name__ == '__main__':
    print(f'已生成精选{render()}名，规范字、水字与简体笔画检查通过。')
