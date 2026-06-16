#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pawpatrol 静态网站生成器
- 读 pawpatrol/season-*/s*.md
- 生成 site/dist/{index.html, season-XX.html, episode.html, data.json, style.css, search.js}
- 全部繁简转换 (zhconv)
"""
import os, re, json, html as htmllib, shutil, sys
from collections import defaultdict
escape = htmllib.escape

# zhconv (必须装)
sys.path.insert(0, '/tmp/simp/lib/python3.13/site-packages')
try:
    from zhconv import convert
except ImportError:
    print("❌ zhconv 未装, 请先: uv pip install --python /tmp/simp/bin/python zhconv")
    sys.exit(1)

def simp(s):
    if not s: return s
    return convert(s, 'zh-cn')

# ============ 路径 ============
ROOT = '/lytest/code/pawpatrol'
DIST = '/lytest/code/pawpatrol/site/dist'

os.makedirs(DIST, exist_ok=True)

# ============ 解析 md 文件 ============
def parse_md(path):
    """解析单个 .md 文件,返回 {frontmatter, body}"""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not fm_match:
        return {}, content
    fm_text = fm_match.group(1)
    body = fm_match.group(2).strip()

    # 简单 YAML 解析 (只处理 key: value / key: [a, b])
    fm = {}
    for line in fm_text.split('\n'):
        m = re.match(r'^(\w+):\s*(.*)', line)
        if not m: continue
        key, val = m.group(1), m.group(2).strip()
        # 去掉引号
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        # 数组
        if val.startswith('[') and val.endswith(']'):
            val = [x.strip().strip('"').strip("'") for x in val[1:-1].split(',') if x.strip()]
        fm[key] = val
    return fm, body

def extract_plot(body):
    """从 body 提取 ## 剧情简介 内容"""
    m = re.search(r'##\s*剧情简介\s*\n\n(.*?)(?=\n##\s|\Z)', body, re.DOTALL)
    if not m: return ''
    text = m.group(1).strip()
    # 移除 HTML 注释和英文占位
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'>\s*英文原文.*$', '', text, flags=re.DOTALL)
    text = re.sub(r'>\s*TODO.*$', '', text, flags=re.DOTALL)
    text = re.sub(r'\n+', ' ', text).strip()
    return text

# ============ 收集所有集 ============
SEASONS = defaultdict(list)  # season_num -> [ep_records]
all_records = []  # 全量

for sn in range(1, 14):
    sdir = f"{ROOT}/season-{sn:02d}"
    if not os.path.isdir(sdir): continue
    for fn in sorted(os.listdir(sdir)):
        if not fn.endswith('.md'): continue
        if fn == 'README.md': continue
        path = f"{sdir}/{fn}"
        fm, body = parse_md(path)
        if not fm: continue

        # 解析 episode 和 segment
        ep = int(fm.get('episode', 0))
        # 多种 segment 字段名: segment_1, segment_2, segment
        seg = 1
        for k in ['segment_1', 'segment_2', 'segment_3', 'segment']:
            if k in fm:
                v = fm[k]
                if isinstance(v, list) and v:
                    v = v[0]
                try:
                    seg = int(v)
                    break
                except (ValueError, TypeError):
                    pass

        # 从文件名推断 segment (兼容 s01e01p2.md / s01e22a.md / s01e22b.md)
        m_fn = re.match(r's\d+e(\d+)(?:p(\d+))?([a-z])?\.md', fn)
        if m_fn:
            fn_ep = int(m_fn.group(1))
            fn_seg = int(m_fn.group(2)) if m_fn.group(2) else 0
            fn_suffix = m_fn.group(3)
            # a=1, b=2 (a/b 后缀表示 segment)
            if fn_suffix == 'a' and fn_seg == 0:
                fn_seg = 1
            elif fn_suffix == 'b' and fn_seg == 0:
                fn_seg = 2
            # 如果 frontmatter 没指定或指定为 1, 用文件名
            if 'segment_1' in fm or 'segment' in fm and seg == 1:
                # 有 segment_1 (s01e01.md) 或 segment=1 (s01e22a.md) - 检查是不是 a/b
                if fn_suffix == 'a':
                    seg = 1
                elif fn_suffix == 'b':
                    seg = 2
                elif fn_seg > 0:
                    seg = fn_seg
            elif fn_seg > 0:
                seg = fn_seg

        title_en = simp(str(fm.get('title_en', '')))
        title_cn = simp(str(fm.get('title_cn', '')))
        air_date = str(fm.get('air_date', ''))
        tags = fm.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        plot = simp(extract_plot(body))

        # url: 指向真正的静态 HTML
        ep_url = f"episode-s{sn:02d}-e{ep:02d}"
        if seg > 1:
            ep_url += f"-p{seg}"
        ep_url += ".html"

        rec = {
            'file': fn,
            'season': sn,
            'episode': ep,
            'segment': seg,
            'title_en': title_en,
            'title_cn': title_cn,
            'air_date': air_date,
            'tags': tags,
            'plot': plot,
            'has_plot': bool(plot and len(plot) > 20),
            'url': ep_url,
        }
        SEASONS[sn].append(rec)
        all_records.append(rec)

print(f"✅ 解析 {len(all_records)} 个集文件, {sum(1 for r in all_records if r['has_plot'])} 有 plot")

# ============ 写入 data.json ============
data = {
    'meta': {
        'total_episodes': len(all_records),
        'translated': sum(1 for r in all_records if r['has_plot']),
        'seasons': len(SEASONS),
        'generated_at': '2026-06-16',
    },
    'seasons': {
        str(sn): {
            'season': sn,
            'count': len(SEASONS[sn]),
            'translated': sum(1 for r in SEASONS[sn] if r['has_plot']),
            'episodes': SEASONS[sn],
        }
        for sn in sorted(SEASONS.keys())
    },
}

with open(f"{DIST}/data.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print(f"✅ data.json: {len(all_records)} 集")

# ============ CSS ============
CSS = '''
:root {
  --bg: #f7f8fa;
  --card: #ffffff;
  --text: #1a1a1a;
  --muted: #6b7280;
  --accent: #ff6b35;
  --accent-dark: #e85a25;
  --border: #e5e7eb;
  --tag: #eef2ff;
  --tag-text: #4338ca;
  --highlight: #fef3c7;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}

.container { max-width: 1200px; margin: 0 auto; padding: 20px; }

/* Header */
.header {
  background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
  color: white;
  padding: 30px 0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.header h1 { font-size: 28px; margin-bottom: 8px; }
.header .subtitle { opacity: 0.9; font-size: 14px; }

/* Search */
.search-box {
  margin: 20px 0;
  position: relative;
}
.search-box input {
  width: 100%;
  padding: 14px 20px 14px 50px;
  border: 2px solid var(--border);
  border-radius: 12px;
  font-size: 16px;
  background: var(--card);
  transition: all 0.2s;
}
.search-box input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
}
.search-box .icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--muted);
}
.search-results {
  margin-top: 12px;
  display: none;
}
.search-results.active { display: block; }
.result-item {
  background: var(--card);
  padding: 14px 18px;
  margin-bottom: 8px;
  border-radius: 8px;
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.2s;
}
.result-item:hover {
  border-color: var(--accent);
  transform: translateX(4px);
}
.result-title { font-weight: 600; font-size: 15px; margin-bottom: 4px; }
.result-meta { font-size: 12px; color: var(--muted); }
.result-snippet {
  font-size: 13px;
  color: var(--muted);
  margin-top: 6px;
  line-height: 1.5;
}
mark { background: var(--highlight); color: var(--text); padding: 0 2px; }

/* Season grid */
.season-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
  margin-top: 24px;
}
.season-card {
  background: var(--card);
  border-radius: 12px;
  padding: 20px;
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  color: inherit;
}
.season-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.08);
  border-color: var(--accent);
}
.season-num {
  display: inline-block;
  background: var(--accent);
  color: white;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 8px;
}
.season-card h3 { font-size: 16px; margin-bottom: 8px; }
.season-stats {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--muted);
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

/* Episode list */
.episode-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;
  margin-top: 20px;
}
.episode-item {
  background: var(--card);
  border-radius: 10px;
  padding: 16px;
  border: 1px solid var(--border);
  text-decoration: none;
  color: inherit;
  transition: all 0.2s;
  display: block;
}
.episode-item:hover {
  border-color: var(--accent);
  transform: translateY(-1px);
}
.episode-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 6px;
}
.episode-num {
  background: var(--tag);
  color: var(--tag-text);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}
.episode-date { font-size: 12px; color: var(--muted); }
.episode-title-cn { font-weight: 600; font-size: 15px; margin-bottom: 2px; }
.episode-title-en { font-size: 13px; color: var(--muted); font-style: italic; }
.episode-tags { margin-top: 8px; display: flex; gap: 4px; flex-wrap: wrap; }
.tag {
  background: var(--tag);
  color: var(--tag-text);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
}
.no-plot {
  display: inline-block;
  background: #fef3c7;
  color: #92400e;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  margin-top: 6px;
}

/* Episode detail */
.episode-detail {
  background: var(--card);
  border-radius: 12px;
  padding: 32px;
  border: 1px solid var(--border);
  margin-top: 20px;
}
.episode-detail h1 {
  font-size: 24px;
  margin-bottom: 12px;
  color: var(--accent);
}
.episode-detail .meta {
  color: var(--muted);
  font-size: 14px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border);
}
.episode-detail h2 {
  font-size: 18px;
  margin: 20px 0 12px;
  color: var(--accent-dark);
}
.episode-detail .plot {
  font-size: 15px;
  line-height: 1.8;
  white-space: pre-wrap;
}
.episode-detail .no-content {
  color: var(--muted);
  font-style: italic;
}

/* Breadcrumb */
.breadcrumb {
  margin: 16px 0;
  font-size: 13px;
  color: var(--muted);
}
.breadcrumb a { color: var(--accent); text-decoration: none; }
.breadcrumb a:hover { text-decoration: underline; }

/* Empty state */
.empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--muted);
}

@media (max-width: 600px) {
  .container { padding: 12px; }
  .header { padding: 20px 0; }
  .header h1 { font-size: 22px; }
  .episode-detail { padding: 20px; }
  .episode-list, .season-grid { grid-template-columns: 1fr; }
}
'''

with open(f"{DIST}/style.css", 'w', encoding='utf-8') as f:
    f.write(CSS)
print("✅ style.css")

# ============ 搜索 JS ============
SEARCH_JS = '''// 客户端搜索
let DATA = null;

async function loadData() {
  if (DATA) return DATA;
  const resp = await fetch('data.json');
  DATA = await resp.json();
  return DATA;
}

function escapeHtml(s) {
  return s.replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

function highlight(text, query) {
  if (!query) return escapeHtml(text);
  const re = new RegExp('(' + query.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&') + ')', 'gi');
  return escapeHtml(text).replace(re, '<mark>$1</mark>');
}

function search(query) {
  if (!query || !DATA) return [];
  const q = query.toLowerCase().trim();
  if (q.length < 2) return [];

  const results = [];
  for (const sn of Object.keys(DATA.seasons)) {
    for (const ep of DATA.seasons[sn].episodes) {
      const haystack = [
        ep.title_cn, ep.title_en, ep.plot, ep.air_date,
        ...(ep.tags || [])
      ].join(' ').toLowerCase();

      if (haystack.includes(q)) {
        // 计算相关度 (标题命中 > plot 命中)
        let score = 0;
        if (ep.title_cn && ep.title_cn.toLowerCase().includes(q)) score += 10;
        if (ep.title_en && ep.title_en.toLowerCase().includes(q)) score += 5;
        if (ep.tags && ep.tags.some(t => t.toLowerCase().includes(q))) score += 3;
        if (ep.plot && ep.plot.toLowerCase().includes(q)) score += 1;

        results.push({...ep, score});
      }
    }
  }

  return results.sort((a, b) => b.score - a.score).slice(0, 50);
}

function renderResults(results, query) {
  const container = document.getElementById('search-results');
  if (!results.length) {
    container.innerHTML = query.length >= 2
      ? `<div class="empty">未找到 "${escapeHtml(query)}" 的结果</div>`
      : '';
    container.classList.toggle('active', query.length >= 2);
    return;
  }

  container.innerHTML = results.map(r => {
    const snippet = r.plot ? r.plot.substring(0, 120) : '';
    return `
      <a href="${r.url}" class="result-item">
        <div class="result-title">
          ${highlight(r.title_cn || r.title_en, query)}
          <span style="color:var(--muted); font-weight:normal; font-size:13px; margin-left:8px">
            S${String(r.season).padStart(2,'0')}E${String(r.episode).padStart(2,'0')}${r.segment > 1 ? ' 第' + r.segment + '段' : ''}
          </span>
        </div>
        <div class="result-meta">
          ${highlight(r.title_en, query)} · ${r.air_date}
        </div>
        ${snippet ? `<div class="result-snippet">${highlight(snippet, query)}...</div>` : ''}
      </a>
    `;
  }).join('');
  container.classList.add('active');
}

document.addEventListener('DOMContentLoaded', async () => {
  await loadData();

  const input = document.getElementById('search-input');
  if (!input) return;

  let debounce;
  input.addEventListener('input', e => {
    clearTimeout(debounce);
    debounce = setTimeout(() => {
      const q = e.target.value;
      if (q.length < 2) {
        document.getElementById('search-results').classList.remove('active');
        return;
      }
      const results = search(q);
      renderResults(results, q);
    }, 200);
  });

  // 监听 URL ?q= 参数
  const params = new URLSearchParams(location.search);
  const initial = params.get('q');
  if (initial) {
    input.value = initial;
    renderResults(search(initial), initial);
  }
});
'''

with open(f"{DIST}/search.js", 'w', encoding='utf-8') as f:
    f.write(SEARCH_JS)
print("✅ search.js")

# ============ HTML 模板 ============
def html_header(title, with_search=True):
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)} · 汪汪队立大功</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="header">
  <div class="container">
    <h1>🐾 汪汪队立大功</h1>
    <div class="subtitle">PAW Patrol 13 季全集剧情索引 · 共 {len(all_records)} 集</div>
  </div>
</div>
<div class="container">'''

def html_search_box():
    return '''
<div class="search-box">
  <span class="icon">🔍</span>
  <input type="text" id="search-input" placeholder="搜索标题、剧情、标签、英文名... (至少 2 字)" autocomplete="off">
</div>
<div class="search-results" id="search-results"></div>'''

def html_footer():
    return '''<script src="search.js"></script>
</body>
</html>'''

def html_breadcrumb(crumbs):
    """crumbs: [(text, url_or_none)]"""
    parts = []
    for i, (text, url) in enumerate(crumbs):
        if i > 0: parts.append('<span> / </span>')
        if url:
            parts.append(f'<a href="{url}">{text}</a>')
        else:
            parts.append(text)
    return f'<div class="breadcrumb">{"".join(parts)}</div>'

# ============ 首页 ============
def render_index():
    h = [html_header('首页')]
    h.append(html_search_box())

    h.append('<h2 style="margin-top:30px;">📅 全部季</h2>')
    h.append('<div class="season-grid">')
    for sn in sorted(SEASONS.keys()):
        season_data = data['seasons'][str(sn)]
        translated = season_data['translated']
        total = season_data['count']
        pct = int(translated / total * 100) if total else 0
        h.append(f'''
<a href="season-{sn:02d}.html" class="season-card">
  <span class="season-num">第 {sn} 季</span>
  <h3>PAW Patrol Season {sn}</h3>
  <div style="font-size:13px; color:var(--muted); margin-top:4px">
    翻译进度: {translated}/{total} ({pct}%)
  </div>
  <div class="season-stats">
    <span>📺 {total} 集</span>
    <span>📝 已翻译 {translated}</span>
  </div>
</a>
''')
    h.append('</div>')
    h.append(html_footer())

    with open(f"{DIST}/index.html", 'w', encoding='utf-8') as f:
        f.write('\n'.join(h))

render_index()
print("✅ index.html")

# ============ 季页 ============
def render_season(sn):
    episodes = SEASONS[sn]
    season_data = data['seasons'][str(sn)]
    translated = season_data['translated']
    total = season_data['count']

    h = [html_header(f'第 {sn} 季')]
    h.append(html_search_box())
    h.append(html_breadcrumb([('首页', 'index.html'), (f'第 {sn} 季', None)]))
    h.append(f'<h2 style="margin-top:20px">第 {sn} 季 · PAW Patrol Season {sn}</h2>')
    h.append(f'<p style="color:var(--muted); margin-top:8px">共 {total} 集,已翻译 {translated} 集 ({int(translated/total*100)}%)</p>')

    h.append('<div class="episode-list">')
    for ep in episodes:
        title_cn = ep['title_cn'] or '暂无中文标题'
        title_en = ep['title_en'] or ''
        seg_label = f" 第{ep['segment']}段" if ep['segment'] > 1 else ''
        tags_html = ''.join(f'<span class="tag">{escape(t)}</span>' for t in (ep['tags'] or []))
        no_plot_html = '' if ep['has_plot'] else '<div class="no-plot">📭 暂无剧情</div>'

        h.append(f'''
<a href="{ep['url']}" class="episode-item">
  <div class="episode-header">
    <span class="episode-num">S{str(sn).zfill(2)}E{str(ep['episode']).zfill(2)}{seg_label}</span>
    <span class="episode-date">{ep['air_date']}</span>
  </div>
  <div class="episode-title-cn">{escape(title_cn)}</div>
  {f'<div class="episode-title-en">{escape(title_en)}</div>' if title_en else ''}
  {tags_html and f'<div class="episode-tags">{tags_html}</div>'}
  {no_plot_html}
</a>
''')
    h.append('</div>')
    h.append(html_footer())

    with open(f"{DIST}/season-{sn:02d}.html", 'w', encoding='utf-8') as f:
        f.write('\n'.join(h))

for sn in sorted(SEASONS.keys()):
    render_season(sn)
print(f"✅ season-01.html ~ season-{max(SEASONS.keys()):02d}.html ({len(SEASONS)} 个)")

# ============ 单集页 ============
# 单独为每集生成 HTML (因为是静态)
EPISODE_TEMPLATE_HEADER = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="header">
  <div class="container">
    <h1>🐾 汪汪队立大功</h1>
    <div class="subtitle">第 {season} 季 · 第 {episode} 集{seg_label}</div>
  </div>
</div>
<div class="container">
<div class="search-box">
  <span class="icon">🔍</span>
  <input type="text" id="search-input" placeholder="搜索..." autocomplete="off">
</div>
<div class="search-results" id="search-results"></div>
'''

def render_episode(rec):
    seg_label = f' · 第{rec["segment"]}段' if rec['segment'] > 1 else ''
    title = rec['title_cn'] or rec['title_en']

    h = [EPISODE_TEMPLATE_HEADER.format(
        title=escape(title),
        season=rec['season'],
        episode=rec['episode'],
        seg_label=seg_label,
    )]

    h.append(html_breadcrumb([
        ('首页', 'index.html'),
        (f'第 {rec["season"]} 季', f'season-{rec["season"]:02d}.html'),
        (title or f'第{rec["episode"]}集', None),
    ]))

    h.append('<div class="episode-detail">')
    h.append(f'<h1>{escape(title)}</h1>')
    h.append(f'<div class="meta">')
    h.append(f'S{str(rec["season"]).zfill(2)}E{str(rec["episode"]).zfill(2)}')
    if rec['segment'] > 1:
        h.append(f' · 第{rec["segment"]}段')
    h.append(f' · 首播: {rec["air_date"]}')
    if rec['title_en']:
        h.append(f' · {escape(rec["title_en"])}')
    h.append('</div>')

    if rec['tags']:
        tags_html = ' '.join(f'<span class="tag">{escape(t)}</span>' for t in rec['tags'])
        h.append(f'<div style="margin-bottom:20px">{tags_html}</div>')

    h.append('<h2>剧情简介</h2>')
    if rec['plot']:
        h.append(f'<div class="plot">{escape(rec["plot"])}</div>')
    else:
        h.append('<div class="no-content">暂无剧情简介（维基尚无 plot 数据）</div>')

    h.append('</div>')

    h.append('''<script src="search.js"></script>
</body>
</html>''')

    # 文件名: episode-s01-e01.html
    fn = f"episode-s{rec['season']:02d}-e{rec['episode']:02d}"
    if rec['segment'] > 1:
        fn += f"-p{rec['segment']}"
    fn += '.html'
    path = f"{DIST}/{fn}"
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(h))

for rec in all_records:
    render_episode(rec)
print(f"✅ episode-*.html ({len(all_records)} 个单集页)")

# ============ 完成 ============
print(f"\n🎉 完成! 输出目录: {DIST}")
total_size = sum(
    os.path.getsize(f"{DIST}/{f}")
    for f in os.listdir(DIST)
    if os.path.isfile(f"{DIST}/{f}")
)
print(f"📦 总大小: {total_size/1024:.1f} KB")
print(f"📄 文件数: {len(os.listdir(DIST))}")