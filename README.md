# 汪汪队立大功 · 集数目录

> 索引页。每季单独一个文件夹，文件夹里是每一集的介绍。

## 全季列表

| 季 | 名称 | 首播年 | 集数 | 文件夹 |
|---|---|---|---|---|
| 1 | PAW Patrol Season 1 | 2013 | 26 | [season-01/](./season-01/) |
| 2 | PAW Patrol Season 2 | 2014 | 26 | [season-02/](./season-02/) |
| 3 | PAW Patrol Season 3 | 2016 | 26 | [season-03/](./season-03/) |
| 4 | PAW Patrol Season 4 | 2017 | 26 | [season-04/](./season-04/) |
| 5 | PAW Patrol Season 5 | 2018 | 26 | [season-05/](./season-05/) |
| 6 | PAW Patrol Season 6 | 2019 | 26 | [season-06/](./season-06/) |
| 7 | PAW Patrol Season 7 | 2020 | 26 | [season-07/](./season-07/) |
| 8 | PAW Patrol Season 8 | 2021 | 26 | [season-08/](./season-08/) |
| 9 | PAW Patrol Season 9 | 2022 | 26 | [season-09/](./season-09/) |
| 10 | PAW Patrol Season 10 | 2023 | 26 | [season-10/](./season-10/) |
| 11 | PAW Patrol Season 11 | 2024 | 26 | [season-11/](./season-11/) |

## 目录结构

```
pawpatrol/
├── README.md              ← 本文件（索引）
├── season-01/             ← 第一季
│   ├── README.md          ← 季内分集列表
│   ├── s01e01.md          ← 第1集
│   ├── s01e02.md
│   └── ...
├── season-02/
│   └── ...
└── ...
```

## 集数文件模板

每集一个 `.md` 文件，命名格式 `s{季编号}e{集编号}.md`，推荐 frontmatter：

```yaml
---
season: 1
episode: 1
title_en: "Pups Make a Splash"
title_cn: "狗狗们跳水"
air_date: 2013-08-12
tags: [adventure, water]
---
```

正文部分自由发挥：剧情简介、出场狗狗、知识点、台词金句等都可以写。
