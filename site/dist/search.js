// 客户端搜索
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
  const re = new RegExp('(' + query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
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
