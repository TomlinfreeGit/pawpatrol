# 汪汪队立大功 · 集数目录

> 索引页。每季单独一个文件夹,文件夹里是每集(每段)的剧情介绍。
> 数据来源:[英文维基百科](https://en.wikipedia.org/wiki/List_of_PAW_Patrol_episodes) + [中文维基百科](https://zh.wikipedia.org/wiki/%E6%B4%AA%E6%B3%BD%E5%85%94%E7%AB%A5%E8%A1%93)

## 数据统计(2026-06-16 更新)

- **总季数**:13 季(S1-S13)
- **总 segment 数**:573
- **有英文 plot**:162
- **已翻译成中文并填入**:162(100%)
- **剩余无 plot(占位)**:411

## 全季列表

| 季 | 名称 | 首播年 | segment 数 | 有 plot | 已翻译 | 文件夹 |
|---|---|---|---|---|---|---|
| 1 | PAW Patrol Season 1 | 2013 | 48 | 35 | 35 | [season-01/](./season-01/) |
| 2 | PAW Patrol Season 2 | 2014 | 48 | 8 | 8 | [season-02/](./season-02/) |
| 3 | PAW Patrol Season 3 | 2016 | 48 | 10 | 10 | [season-03/](./season-03/) |
| 4 | PAW Patrol Season 4 | 2017 | 47 | 20 | 20 | [season-04/](./season-04/) |
| 5 | PAW Patrol Season 5 | 2018 | 47 | 14 | 14 | [season-05/](./season-05/) |
| 6 | PAW Patrol Season 6 | 2019 | 49 | 15 | 15 | [season-06/](./season-06/) |
| 7 | PAW Patrol Season 7 | 2020 | 45 | 18 | 18 | [season-07/](./season-07/) |
| 8 | PAW Patrol Season 8 | 2021 | 53 | 15 | 15 | [season-08/](./season-08/) |
| 9 | PAW Patrol Season 9 | 2022 | 46 | 20 | 20 | [season-09/](./season-09/) |
| 10 | PAW Patrol Season 10 | 2023 | 47 | 6 | 6 | [season-10/](./season-10/) |
| 11 | PAW Patrol Season 11 | 2024 | 46 | 1 | 1 | [season-11/](./season-11/) |
| 12 | PAW Patrol Season 12 | 2025 | 24 | 0 | 0 | [season-12/](./season-12/) |
| 13 | PAW Patrol Season 13 | 2026 | 25 | 0 | 0 | [season-13/](./season-13/) |

## 文件命名规则

- 单段集:`s{SS}e{NN}.md` 例如 `s01e22.md`
- 双段集:`s{SS}e{NN}a.md` + `s{SS}e{NN}b.md` 例如 `s01e22a.md` / `s01e22b.md`
- S1 特殊:`s01e01p2.md` 这种命名仅在 S1 前 17 集使用(早期 commit 的旧格式)

## 集文件模板

每个集文件包含:

```yaml
---
season: 1
episode: 1
segment: 1
title_en: "Pups Make a Splash"
title_cn: "海上救援"
air_date: 2013-11-14
tags: [水上救援, 冒险]
---
```

正文部分:
- `# 第 N 集 · 中文标题`
- 英文标题 + 首播日期
- ## 剧情简介(150-250 字中文翻译,基于英文维基 plot)
- ## 出场角色(目前留空)
- ## 知识点 / 备注(目前留空)

## 数据来源说明

- **剧情(plot)**:全部来自英文维基百科 `List of PAW Patrol episodes` 页面的 plot 描述,翻译为中文,**未做剧情扩展或编造**
- **中文标题(title_cn)**:S1-S10 来自中文维基,已统一为简体字;S11+ 中文维基暂未收录,标题由英文翻译
- **首播日期(air_date)**:来自英文维基(美国首播)
- **tags**:根据剧情主题手动分类

## TODO

- S12-S13 维基暂无 plot(2025-2026 新季),等待维基补充
- 无 plot 的 411 个 segment 文件保留为占位(标题+日期有,但剧情简介为空)

## Git 历史

```
6fcc298 fill: S11 第44段 集内容 (新建 s11e44.md)
dc65fe9 fill: S8-S11 集内容
082c041 fill: S5-S7 集内容
c9c19ec fill: S2-S4 集内容
3b69879 fill: S1 集内容
9110cca rebuild: 汪汪队目录重建为 13 季 × 563 segment
c2da5cf init: 汪汪队立大功 集数目录骨架
```
