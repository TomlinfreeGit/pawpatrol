# 汪汪队立大功 · 集数目录

> 索引页。每季单独一个文件夹，文件夹里是每 segment 的介绍。
> 数据来源：[英文维基百科](https://en.wikipedia.org/wiki/List_of_PAW_Patrol_episodes) + [中文维基百科](https://zh.wikipedia.org/wiki/%E6%B4%AA%E6%B3%BD%E5%85%94%E7%AB%A5%E8%A1%93)

## 数据统计

- **总季数**：13 季（S1-S13）
- **总 segment 数**：563
- **有英文 plot**：154（27.4%）
- **有中文标题**：428（76.0%）

## 全季列表

| 季 | 名称 | 首播年 | segment 数 | 有 plot | 有中文 | 文件夹 |
|---|---|---|---|---|---|---|
| 1 | PAW Patrol Season 1 | 2013 | 30 | 20 | 12 | [season-01/](./season-01/) |
| 2 | PAW Patrol Season 2 | 2014 | 48 | 8 | 48 | [season-02/](./season-02/) |
| 3 | PAW Patrol Season 3 | 2016 | 47 | 10 | 46 | [season-03/](./season-03/) |
| 4 | PAW Patrol Season 4 | 2017 | 47 | 20 | 47 | [season-04/](./season-04/) |
| 5 | PAW Patrol Season 5 | 2018 | 46 | 13 | 45 | [season-05/](./season-05/) |
| 6 | PAW Patrol Season 6 | 2019 | 49 | 15 | 49 | [season-06/](./season-06/) |
| 7 | PAW Patrol Season 7 | 2020 | 45 | 18 | 45 | [season-07/](./season-07/) |
| 8 | PAW Patrol Season 8 | 2021 | 45 | 15 | 45 | [season-08/](./season-08/) |
| 9 | PAW Patrol Season 9 | 2022 | 46 | 20 | 46 | [season-09/](./season-09/) |
| 10 | PAW Patrol Season 10 | 2023 | 47 | 6 | 45 | [season-10/](./season-10/) |
| 11 | PAW Patrol Season 11 | 2024 | 46 | 1 | 0 | [season-11/](./season-11/) |
| 12 | PAW Patrol Season 12 | 2025 | 24 | 0 | 0 | [season-12/](./season-12/) |
| 13 | PAW Patrol Season 13 | 2026 | 43 | 8 | 0 | [season-13/](./season-13/) |

## 目录结构

```
pawpatrol/
├── README.md              ← 本文件（索引）
├── season-01/             ← 第一季
│   ├── README.md          ← 季内分集列表
│   ├── s01e01.md          ← 第1集第1段
│   ├── s01e22a.md         ← 第22集第1段（S1 从 22 集开始 1 集 2 段）
│   ├── s01e22b.md         ← 第22集第2段
│   └── ...
├── season-02/
│   └── ...
└── season-13/
    └── ...
```

## 集数文件命名

- 1 集 1 段：`s{NN}e{XX}.md`（如 `s01e01.md`）
- 1 集 2 段：`s{NN}e{XX}a.md` + `s{NN}e{XX}b.md`（如 `s02e01a.md`）

## Frontmatter 字段

```yaml
---
season: 1
episode: 1
segment: 1     # 第几段（1 或 2）
pc: "101"       # Production Code
title_en: "Pups Make a Splash"
title_cn: "狗狗跳水"
air_date: "2013-08-12"
tags: []
---
```

## 翻译状态

- ✓ 已有英文 plot：**154** 个（可直接翻译成中文）
- ✗ 暂无 plot：**409** 个（待补可信来源）

