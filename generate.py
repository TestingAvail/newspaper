import feedparser
import time
import os
import re
import html
from datetime import datetime, timezone

update_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

feeds = [
    {"name": "Hacker News", "url": "https://news.ycombinator.com/rss"},
    {"name": "Habr (Главная)", "url": "https://habr.com/ru/rss/all/"},
    {"name": "GitHub Changelog", "url": "https://github.blog/changelog/feed/"},
    {"name": "Cloudflare Blog", "url": "https://blog.cloudflare.com/rss/"},
    {"name": "Phoronix (Linux)", "url": "https://www.phoronix.com/rss.php"},
    {"name": "Krebs on Security", "url": "https://krebsonsecurity.com/feed/"},
    {"name": "Ars Technica", "url": "https://arstechnica.com/feed/"},
    {"name": "Linux Kernel Stable", "url": "https://www.kernel.org/feeds/kdist.xml"},
    {"name": "Arch Linux News", "url": "https://archlinux.org/feeds/news/"},
    {"name": "APNIC Blog", "url": "https://blog.apnic.net/feed/"},
    {"name": "Schneier on Security", "url": "https://www.schneier.com/blog/atom.xml"},
    {"name": "Troy Hunt", "url": "https://www.troyhunt.com/rss/"},
    {"name": "Dark Reading", "url": "https://www.darkreading.com/rss.xml"},
    {"name": "Ubuntu Security Notices", "url": "https://ubuntu.com/security/notices/rss.xml"},
    {"name": "Exploit-DB RSS", "url": "https://www.exploit-db.com/rss.xml"},
    {"name": "OpenNet (Программы)", "url": "https://www.opennet.ru/opennews/opennews_prog.rss"},
    {"name": "OpenNet (Безопасность)", "url": "https://www.opennet.ru/opennews/opennews_sec.rss"},
    {"name": "LOR", "url": "https://www.linux.org.ru/section-rss.jsp?section=1"},
    {"name": "FreeBSD Security", "url": "https://www.freebsd.org/security/feed.xml"},
    {"name": "LKML (Linux Kernel Mailing List)", "url": "https://lore.kernel.org/lkml/new.atom"}
]

articles = []
now = time.time()
cutoff = now - (48 * 3600)

for feed in feeds:
    print(f"Fetching {feed['name']}...")
    try:
        parsed = feedparser.parse(feed['url'])
        for entry in parsed.entries:
            dt_struct = getattr(entry, 'published_parsed', None) or getattr(entry, 'updated_parsed', None)
            timestamp = time.mktime(dt_struct) if dt_struct else now

            if dt_struct and timestamp < cutoff:
                continue

            raw_summary = getattr(entry, 'summary', getattr(entry, 'description', ''))
            clean_summary = re.sub(r'<[^<]+?>', '', raw_summary)
            clean_summary = html.unescape(clean_summary)
            clean_summary = ' '.join(clean_summary.split()).strip()
            if clean_summary.lower() in ['comments', 'discussion', '']:
                clean_summary = ''

            articles.append({
                "source": feed['name'],
                "title": getattr(entry, 'title', 'No Title'),
                "link": getattr(entry, 'link', '#'),
                "date": getattr(entry, 'published', getattr(entry, 'updated', '')),
                "summary": clean_summary,
                "timestamp": timestamp
            })
    except Exception as e:
        print(f"Error fetching {feed['name']}: {e}")

articles.sort(key=lambda x: x['timestamp'], reverse=True)
print(f"Всего отобрано свежих статей: {len(articles)}")

html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Digest</title>
    <style>
        body {{ background-color: #000; color: #0f0; font-family: monospace; margin: 10px; }}
        a {{ color: #0ff; text-decoration: underline; }}
        .article {{ margin-bottom: 15px; border-bottom: 1px dashed #333; padding-bottom: 10px; }}
        .source {{ font-size: 11px; color: #ff0; text-transform: uppercase; }}
        .snippet {{ font-size: 11px; color: #aaa; margin-top: 4px; }}
        .time {{ font-size: 10px; color: #888; margin-top: 4px; }}
        .digest-time {{ font-size: 11px; color: #888; font-weight: normal; }}
    </style>
</head>
<body>
    <h2>== CYBERNEWS DIGEST == <span class="digest-time">[{update_time}]</span></h2>
"""

for art in articles:
    snippet_div = f'<div class="snippet">{html.escape(art["summary"])}</div>' if art['summary'] else ''
    html_content += f"""
    <div class="article">
        <div class="source">[{html.escape(art['source'])}]</div>
        <div><a href="{html.escape(art['link'], quote=True)}">{html.escape(art['title'])}</a></div>
        {snippet_div}
        <div class="time">{html.escape(str(art['date']))}</div>
    </div>
"""

html_content += """
</body>
</html>
"""

os.makedirs("public", exist_ok=True)
with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("Newspaper generated successfully.")
