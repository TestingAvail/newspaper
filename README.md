# 📰 Newspaper

[![Digest](https://img.shields.io/github/actions/workflow/status/TestingAvail/newspaper/newspaper.yml?branch=main&label=digest&logo=github-actions)](https://github.com/TestingAvail/newspaper/actions/workflows/newspaper.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Персональный дайджест новостей. GitHub Actions два раза в день собирает статьи из 20 RSS-лент за последние 48 часов и публикует их одной простой HTML-страницей. Страница намеренно минималистична, чтобы открываться даже на старых браузерах.

## 📰 Что внутри

- Статьи отсортированы по времени: сначала свежие.
- У каждой статьи есть источник, заголовок, ссылка, дата и короткий анонс.
- Оформление в стиле терминала: чёрный фон, зелёный текст, без скриптов и внешних стилей.
- Источники: Hacker News, Habr, GitHub Changelog, Cloudflare, Phoronix, Krebs on Security, Ars Technica, Linux Kernel Stable, Arch Linux News, APNIC, Schneier on Security, Troy Hunt, Dark Reading, Ubuntu Security Notices, Exploit-DB, OpenNet (программы и безопасность), LOR, FreeBSD Security, LKML.

## 🔗 Где читать

Страница публикуется через GitHub Pages. Каждый выпуск также создаётся как релиз с `index.html` и `checksums.txt`, где указаны MD5, SHA-1, SHA-256 и SHA-512.

## ⚙️ Как это работает

1. Workflow `.github/workflows/newspaper.yml` запускается в 06:00 и 18:00 UTC, при пуше в `main` и вручную.
2. `feedparser` читает все ленты. Статьи старше 48 часов отбрасываются.
3. Из анонсов удаляются HTML-теги, экранированные символы и мусорные значения вроде «comments».
4. Генерируется `public/index.html`, для него считаются контрольные суммы.
5. Создаётся релиз с тегом `digest-YYYYMMDD-HHMM` и публикуется сайт.

Чтобы добавить или убрать источник, отредактируйте список `feeds` в `newspaper.yml`.

## 🛠️ Локальный запуск

```bash
pip install feedparser
python3 - << 'EOF'
# см. блок "Generate Newspaper" в .github/workflows/newspaper.yml
EOF
```

Скрипт генерации также встроен в workflow.

## 📄 Лицензия

Распространяется под лицензией MIT. См. [LICENSE](LICENSE).
