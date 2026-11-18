(() => {
  'use strict';
  const root = document.getElementById('publication-list');
  const input = document.getElementById('publication-search');
  const count = document.getElementById('publication-count');
  const empty = document.getElementById('publication-empty');
  if (!root || !input || !count) return;
  const zh = document.documentElement.lang.startsWith('zh');
  const papers = [...root.querySelectorAll('.paper')];
  const buttons = [...document.querySelectorAll('[data-publication-filter]')];
  let mode = 'all';
  function update() {
    const query = input.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const paper of papers) {
      const matchesType = mode === 'all' || paper.dataset[mode] === 'true';
      const matchesQuery = !query || (paper.textContent + ' ' + (paper.dataset.aliases || '')).toLocaleLowerCase().includes(query);
      paper.hidden = !(matchesType && matchesQuery);
      if (!paper.hidden) visible++;
    }
    count.textContent = zh ? `显示 ${visible} / ${papers.length} 项工作` : `Showing ${visible} of ${papers.length} works`;
    if (empty) empty.hidden = visible !== 0;
  }
  for (const button of buttons) {
    button.addEventListener('click', () => {
      mode = button.dataset.publicationFilter;
      for (const item of buttons) item.setAttribute('aria-pressed', String(item === button));
      update();
    });
  }
  input.addEventListener('input', update);
  // Timeline links should still work after a filter or search hides a paper.
  for (const link of document.querySelectorAll('a[href^="#paper-"]')) {
    link.addEventListener('click', () => {
      const target = document.getElementById(link.getAttribute('href').slice(1));
      if (target && target.hidden) {
        mode = 'all';
        input.value = '';
        for (const button of buttons) {
          button.setAttribute('aria-pressed', String(button.dataset.publicationFilter === 'all'));
        }
        update();
      }
    });
  }
  document.querySelector('.publication-tools').hidden = false;
  update();
})();
