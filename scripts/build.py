#!/usr/bin/env python3
"""Generate both language pages from the shared bibliography and timeline.

Standard-library only. Run from any directory with: python3 scripts/build.py
"""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / 'data/publications.json').read_text())
WORKS = sorted(CATALOG['works'], key=lambda w: (w['date'], w['title']), reverse=True)
TIMELINE = json.loads((ROOT / 'data/timeline.json').read_text())
LINKS = [
    ('Google Scholar', 'Google Scholar', 'https://scholar.google.com/citations?user=YCfdAqEAAAAJ&hl=en'),
    ('Zhihu', '知乎', 'https://www.zhihu.com/people/shou-zu-ji-qiang-bing'),
    ('Xiaohongshu', '小红书', 'https://www.xiaohongshu.com/user/profile/5ce645800000000005027396'),
    ('Twitter / X', 'Twitter / X', 'https://x.com/OldSaying721'),
    ('ITRA', 'ITRA 跑者主页', 'https://itra.run/RunnerSpace/gu.zhouhong.7066773'),
]


def esc(value):
    return escape(str(value), quote=True)


def paper_id(value):
    return 'paper-' + re.sub(r'[^a-zA-Z0-9-]', '-', value)


def external(url, label, css=''):
    return f'<a class="{css}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{label}</a>'


def render_paper(w, zh):
    pub, arxiv = w['publication'], w['arxiv']
    url = pub['url'] if pub else arxiv['url']
    title = esc(w['title'])
    authors = ', '.join(f'<strong>{esc(a)}</strong>' if a in ['Zhouhong Gu', '顾洲洪'] else esc(a) for a in w['authors'])
    precision = w['date_precision']
    date_label = ('仅精确到月' if zh else 'Month only') if precision == 'month' else ('仅精确到年' if zh else 'Year only') if precision == 'year' else ('首次公开' if zh else 'First released')
    venue = esc(pub['venue']) if pub else ('arXiv 预印本' if zh else 'arXiv preprint')
    paper_links = []
    if pub and (not arxiv or pub['url'] != arxiv['url']):
        paper_links.append(external(pub['url'], '发表版本' if zh else 'Publication'))
    if arxiv:
        paper_links.append(external(arxiv['url'], 'arXiv'))
    for link in w.get('extra_links', []):
        paper_links.append(external(link['url'], esc(link['zh' if zh else 'en'])))
    extra = ''
    if pub and arxiv:
        date_prefix = '正式发表：' if zh else 'Published: '
        if pub['status'] == 'accepted' and pub.get('verification') == 'author-profile-only':
            date_prefix = '收录会议：' if zh else 'Conference: '
        extra = f'<p class="paper-extra">{date_prefix}{esc(pub["publication_date"])}</p>'
    if arxiv and w['id'] == '2403.07825':
        extra += f'<p class="paper-extra">arXiv: {esc(arxiv["title"])}</p>'
    return f'''<article class="paper" id="{paper_id(w['id'])}" data-published="{str(bool(pub)).lower()}" data-arxiv="{str(bool(arxiv)).lower()}" data-aliases="{esc(" ".join(w.get("title_aliases",[])))}">
  <div class="paper-date"><time datetime="{esc(w['date'])}">{esc(w['date'])}</time><span>{date_label}</span></div>
  <div class="paper-main"><h3 class="paper-title" lang="{'zh-CN' if w['id']=='shikumen-2011' else 'en'}">{external(url,title)}</h3><p class="paper-authors">{authors}</p><div class="paper-meta"><span class="paper-venue">{venue}</span><div class="paper-links">{' '.join(paper_links)}</div></div>{extra}</div>
</article>'''


def render_milestone(event, zh, dated=True):
    locale = 'zh' if zh else 'en'
    date = event.get('date')
    date_html = f'<time datetime="{date}">{date}</time>' if date else ('日期待补充' if zh else 'Date to add')
    note = event.get('note', {}).get(locale, '')
    references = []
    for ref in event.get('papers', []):
        references.append(f'<a href="#{paper_id(ref["id"])}">{esc(ref["label"])}</a>')
    copy = esc(event.get('description', {}).get(locale, ''))
    if references:
        copy += ('<br>' if copy else '') + ' · '.join(references)
    if event.get('link'):
        copy += ' ' + f'<a href="{esc(event["link"])}">'+('查看照片' if zh else 'View photograph')+'</a>'
    return f'<li class="timeline-item"><div class="timeline-date">{date_html}</div><div><h3 class="timeline-title">{esc(event["title"][locale])}</h3><p class="timeline-copy">{copy}</p>{f"<p class=timeline-kind>{esc(note)}</p>" if note else ""}</div></li>'


def generate(zh):
    p = '../' if zh else './'
    lang = 'zh-CN' if zh else 'en'
    title = '顾洲洪 Zhouhong Gu — 研究、摄影与越野跑' if zh else 'Zhouhong Gu — Research, Photography & Trail Running'
    description = '顾洲洪，复旦大学博士，在小红书从事大语言模型与 AI 搜索研究。论文、发表里程碑、摄影与越野跑。' if zh else 'Zhouhong Gu, Fudan Ph.D., working on large language models and AI search at Xiaohongshu. Publications, milestones, photography, and trail running.'
    canonical = 'https://mikegu721.github.io/zhgu/' + ('zh/' if zh else '')
    nav_items = [('timeline', '年表' if zh else 'Milestones'), ('research', '论文' if zh else 'Publications'), ('photography', '摄影' if zh else 'Photographs')]
    nav = ''.join(f'<a href="#{id}">{label}</a>' for id,label in nav_items)
    languages = '<a href="../" lang="en" hreflang="en">EN</a><span aria-hidden="true">/</span><span aria-current="page">中文</span>' if zh else '<span aria-current="page">EN</span><span aria-hidden="true">/</span><a href="zh/" lang="zh-CN" hreflang="zh-CN">中文</a>'
    intro = '我在小红书从事大语言模型与 AI 搜索相关研究，关注语言模型的推理、评测与智能体。' if zh else 'I work on large language models and AI search at Xiaohongshu, with interests in reasoning, evaluation, and language agents.'
    interests = '研究之外，我喜欢摄影和越野跑。这里记录我的论文、重要时刻，以及沿途值得留下的画面。' if zh else 'Outside research, I enjoy photography and trail running. This is a home for my work, milestones, and moments along the way.'
    intro_links = ' '.join(external(url,esc(cn if zh else en)) for en,cn,url in [LINKS[0],LINKS[4],LINKS[3]])
    events = sorted(TIMELINE['dated'], key=lambda e:e['date'], reverse=True)
    milestone_html = '<ul class="timeline-list">' + ''.join(render_milestone(e,zh) for e in events[:5]) + '</ul>'
    if len(events) > 5:
        older_label = f'更早的记录（{len(events)-5}）' if zh else f'Earlier milestones ({len(events)-5})'
        milestone_html += f'<details class="timeline-older"><summary>{older_label}</summary><ul class="timeline-list">' + ''.join(render_milestone(e,zh) for e in events[5:]) + '</ul></details>'
    pending = TIMELINE.get('undated', [])
    if pending:
        label = f'其他论文录用 · {len(pending)} 组日期待补充' if zh else f'Other paper acceptances · {len(pending)} groups awaiting dates'
        note = '以下录用或发表成果已确认；尚未找到可靠的录用日期，暂不放入日期序列。' if zh else 'These outcomes are confirmed, but their acceptance dates are not yet verified. They are kept outside the dated timeline.'
        milestone_html += f'<details class="timeline-older"><summary>{label}</summary><p class="section-note">{note}</p><ul class="timeline-list">'+''.join(render_milestone(e,zh,False) for e in pending)+'</ul></details>'
    rows = '\n'.join(render_paper(w,zh) for w in WORKS)
    date_note = '按首次公开日期倒序排列；同一工作的会议/期刊版与 arXiv 合并展示。arXiv 使用首次提交日期（UTC）；无法核实到日的记录保留月或年。' if zh else 'Newest first by first public release. Conference/journal and arXiv versions of the same work are combined. arXiv dates use the first submission (UTC); month or year is shown when the exact day is unavailable.'
    count = f'{len(WORKS)} 项工作' if zh else f'{len(WORKS)} works'
    all_text,published_text,arxiv_text = ('全部','已录用 / 发表','arXiv') if zh else ('All','Accepted / published','arXiv')
    photo_intro = '摄影与个人记录：既有我镜头里的世界，也有他人为我留下的重要瞬间。' if zh else 'Photographs and personal moments — what I see through my camera, and meaningful moments others have captured for me.'
    photo_noscript = '''<figure class="photo-fallback"><img src="'''+p+'''assets/photos/xihong-70km-2026-11-15.jpg" width="533" height="800" alt="'''+('顾洲洪在西宏70公里越野跑终点举起横幅' if zh else 'Zhouhong Gu raising a banner at the finish of the Xihong 70 km trail race')+'''" style="max-width:100%;height:auto"><figcaption>2026-11-15 · The Ultra-Trail Xihong 168 autumn - 70km · '''+('摄影：清补凉' if zh else 'Photo: 清补凉')+'''</figcaption></figure>'''
    social = ''.join(external(url,esc(cn if zh else en)+' <span aria-hidden="true">↗</span>','social-link') for en,cn,url in LINKS)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="theme-color" content="#f8f8f4">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{canonical}">
  <link rel="canonical" href="{canonical}">
  <link rel="alternate" hreflang="en" href="https://mikegu721.github.io/zhgu/">
  <link rel="alternate" hreflang="zh-CN" href="https://mikegu721.github.io/zhgu/zh/">
  <link rel="alternate" hreflang="x-default" href="https://mikegu721.github.io/zhgu/">
  <link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{p}assets/css/style.css">
  <script src="{p}assets/js/photos.js" defer></script>
  <script src="{p}assets/js/gallery.js" defer></script>
  <script src="{p}assets/js/publications.js" defer></script>
</head>
<body id="top" data-asset-prefix="{p}">
<a class="skip-link" href="#main">{'跳至正文' if zh else 'Skip to content'}</a>
<header><div class="wrap header-inner"><a class="wordmark" href="./" aria-label="{'顾洲洪主页' if zh else 'Zhouhong Gu home'}">zg<span>.</span></a><div class="header-right"><nav aria-label="{'主导航' if zh else 'Main navigation'}">{nav}</nav><div class="language" aria-label="{'语言' if zh else 'Language'}">{languages}</div></div></div></header>
<main id="main" class="wrap">
<section class="hero" aria-labelledby="name"><div><h1 id="name" lang="en">Zhouhong Gu</h1><p class="native-name" lang="zh-CN">顾洲洪</p><p class="affiliation">{'小红书' if zh else 'Xiaohongshu'}<span>{'复旦大学博士 · 2025 年毕业' if zh else 'Ph.D., Fudan University · Class of 2025'}</span></p></div><div class="hero-copy"><p>{intro}</p><p>{interests}</p><div class="inline-links">{intro_links}</div></div></section>
<section class="section" id="timeline" aria-labelledby="timeline-title"><div class="section-heading"><h2 id="timeline-title">{'大事年表' if zh else 'Milestones'}</h2></div><p class="section-note">{'论文事件按正式发表时间记录，保留来源提供的日、月或年精度；比赛使用完赛日期。' if zh else 'Research milestones use formal publication dates, with day, month, or year precision as available. Races use the finish date.'}</p>{milestone_html}</section>
<section class="section photography" id="photography" aria-labelledby="photography-title"><div class="section-heading"><h2 id="photography-title">{'摄影与记录' if zh else 'Photographs & moments'}</h2></div><p class="section-note">{photo_intro}</p><div id="gallery-empty" class="gallery-empty" hidden>{'更多照片陆续整理中。' if zh else 'More photographs are being collected.'}</div><p id="photo-count" hidden></p><div class="photo-grid" id="photo-grid" hidden></div><noscript>{photo_noscript}</noscript><p class="photo-hint">{'点击照片可放大查看。' if zh else 'Select a photograph to view it full size.'}</p></section>
<section class="section" id="research" aria-labelledby="research-title"><div class="section-heading"><h2 id="research-title">{'论文与预印本' if zh else 'Publications & preprints'}</h2>{external(LINKS[0][2], 'Google Scholar ↗','text-link')}</div><p class="section-note">{date_note}</p>
<div class="publication-tools" hidden><div class="filters" role="group" aria-label="{'按类型筛选' if zh else 'Filter publications'}"><button type="button" class="filter-button" data-publication-filter="all" aria-pressed="true">{all_text}</button><button type="button" class="filter-button" data-publication-filter="published" aria-pressed="false">{published_text}</button><button type="button" class="filter-button" data-publication-filter="arxiv" aria-pressed="false">{arxiv_text}</button></div><label class="search-wrap" for="publication-search">{'搜索' if zh else 'Search'}<input type="search" id="publication-search" placeholder="{'标题、作者或年份' if zh else 'Title, author, or year'}" autocomplete="off"></label></div>
<p class="publication-count" id="publication-count" role="status" aria-live="polite">{count}</p><div id="publication-list">{rows}</div><p class="empty-search" id="publication-empty" hidden>{'没有匹配的论文，请尝试其他关键词。' if zh else 'No matching publications. Try a different search.'}</p></section>
<section class="section elsewhere" id="elsewhere" aria-labelledby="elsewhere-title"><div class="section-heading"><h2 id="elsewhere-title">{'在别处找到我' if zh else 'Elsewhere'}</h2></div><div class="social-list">{social}</div></section>
</main>
<footer class="site-footer wrap"><span>© 2026 Zhouhong Gu</span><span>{'资料更新' if zh else 'Updated'} {CATALOG['updated']}</span><a href="#top">{'回到顶部' if zh else 'Back to top'} ↑</a></footer>
</body>
</html>
'''


if __name__ == '__main__':
    for work in WORKS:
        assert re.fullmatch(r'\d{4}(?:-\d{2}){0,2}', work['date']), work['id']
        assert work['title'] and work['authors'], work['id']
    for event in TIMELINE['dated']:
        assert event['date'] and event.get('date_kind') in ['race_completed', 'publication'], event
    (ROOT/'index.html').write_text(generate(False))
    (ROOT/'zh/index.html').write_text(generate(True))
    print(f'Generated English and Chinese pages: {len(WORKS)} works, {len(TIMELINE["dated"])} dated milestones.')
