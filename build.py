#!/usr/bin/env python3
"""Build index.html, en/index.html and es/index.html from the content fragments.

content-en.html and content-es.html are the single source of truth. They are
inlined into each full page (so crawlers and no-JS readers get the content) and
also served as-is to HTMX when the visitor switches language.

Run after editing a fragment or the template:  python3 build.py
"""
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://rafa1771.github.io"

LANGS = {
    "en": {
        "title": "Rafael Rivlin – CV | Web Developer & Digital Systems Consultant",
        "description": "Web developer and digital systems consultant: WordPress, Next.js and Shopify sites, CRM automation and AI-assisted workflows. Based in Seville, available in Spain and remotely.",
        "locale": "en_US",
        "dark": "Dark Mode",
        "light": "Light Mode",
    },
    "es": {
        "title": "Rafael Rivlin – CV | Desarrollador Web y Consultor de Sistemas Digitales",
        "description": "Desarrollador web y consultor de sistemas digitales: sitios en WordPress, Next.js y Shopify, automatización de CRM y flujos de trabajo con IA. Desde Sevilla, disponible en España y en remoto.",
        "locale": "es_ES",
        "dark": "Modo Oscuro",
        "light": "Modo Claro",
    },
}

TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="en" href="{site}/en/">
    <link rel="alternate" hreflang="es" href="{site}/es/">
    <link rel="alternate" hreflang="x-default" href="{site}/">
    <link rel="stylesheet" href="/styles.css">

    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" itemprop="image primaryImageOfPage" content="{site}/SlackProfilePic.png">
    <meta property="og:url" content="{canonical}">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="{locale}">
    <meta property="og:locale:alternate" content="{alt_locale}">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&family=Open+Sans:ital,wght@0,300..800;1,300..800&family=Space+Mono:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.3.1/css/all.min.css" integrity="sha512-QeR2VH+lsBE5LSAe1Q5EnTBbe7XTBubt8dG93Y7gidSgdMCr8nVqKcfKAMyN96SV8KDbZVTDXChatu5G2KQGzg==" crossorigin="anonymous" referrerpolicy="no-referrer">

    <meta itemprop="image" content="{site}/SlackProfilePic.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    <link rel="manifest" href="/site.webmanifest">

</head>
<body>
    <div id="cv-container">
        <div id="mode-selector">
            <span id="toggle-mode" class="mode-btn">{dark}</span>
        </div>
        <div id="language-selector">
            <a class="lang-btn" href="/es/" hreflang="es" lang="es" data-title="{es_title}"
               hx-get="/content-es.html" hx-target="#content" hx-push-url="/es/">ES</a> |
            <a class="lang-btn" href="/en/" hreflang="en" lang="en" data-title="{en_title}"
               hx-get="/content-en.html" hx-target="#content" hx-push-url="/en/">EN</a>
        </div>
        <div id="content">
{content}
        </div>
    </div>

    <script src="https://unpkg.com/htmx.org@2.0.11/dist/htmx.min.js" integrity="sha384-2OatzQy1H+Zd/IIrjr1TcuDGqLXeHhbooAyJY1KdQMKnr4LZ22k31GBLdYKHmVjg" crossorigin="anonymous"></script>
    <script>
        const LABELS = {labels};
        const TITLES = {titles};
        const toggleMode = document.getElementById('toggle-mode');

        function currentLang() {{
            return document.documentElement.lang === 'es' ? 'es' : 'en';
        }}

        function renderModeLabel() {{
            const dark = document.body.classList.contains('dark-mode');
            toggleMode.textContent = LABELS[currentLang()][dark ? 'light' : 'dark'];
        }}

        // Keep <html lang>, <title> and the mode label in step with the swapped content.
        function syncLang(lang) {{
            document.documentElement.lang = lang;
            document.title = TITLES[lang];
            renderModeLabel();
        }}

        document.addEventListener('DOMContentLoaded', function() {{
            if ((localStorage.getItem('dark-mode') || 'light') === 'dark') {{
                document.body.classList.add('dark-mode');
            }}
            renderModeLabel();

            toggleMode.addEventListener('click', function() {{
                document.body.classList.toggle('dark-mode');
                const mode = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
                localStorage.setItem('dark-mode', mode);
                renderModeLabel();
            }});
        }});

        document.body.addEventListener('htmx:afterSwap', function(evt) {{
            const lang = evt.detail.elt.getAttribute('hreflang');
            if (lang) syncLang(lang);
        }});

        // Back/forward restores a cached page; re-derive the language from the URL.
        document.body.addEventListener('htmx:historyRestore', function() {{
            syncLang(location.pathname.startsWith('/es') ? 'es' : 'en');
        }});
    </script>
</body>
</html>
"""


def render(lang, canonical, out):
    other = "es" if lang == "en" else "en"
    meta = LANGS[lang]
    content = (ROOT / f"content-{lang}.html").read_text(encoding="utf-8").rstrip()
    labels = {k: {"dark": v["dark"], "light": v["light"]} for k, v in LANGS.items()}
    titles = {k: v["title"] for k, v in LANGS.items()}
    import json
    html = TEMPLATE.format(
        lang=lang,
        title=meta["title"],
        description=meta["description"],
        canonical=canonical,
        site=SITE,
        locale=meta["locale"],
        alt_locale=LANGS[other]["locale"],
        dark=meta["dark"],
        es_title=LANGS["es"]["title"],
        en_title=LANGS["en"]["title"],
        content=content,
        labels=json.dumps(labels, ensure_ascii=False),
        titles=json.dumps(titles, ensure_ascii=False),
    )
    path = ROOT / out
    path.parent.mkdir(exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", out)


# "/" serves the default language (English) in full; /en/ is its canonical URL.
render("en", f"{SITE}/en/", "index.html")
render("en", f"{SITE}/en/", "en/index.html")
render("es", f"{SITE}/es/", "es/index.html")
