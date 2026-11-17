"""Fabrique le site de Trame en français, anglais et espagnol.

Le site reste statique (Cloudflare Pages publie le dossier site/). Ce script écrit :
  site/index.html, site/en/index.html, site/es/index.html          (accueil)
  site/nouveautes/, site/en/whats-new/, site/es/novedades/          (nouveautés)

    python3 site-src/build.py

Pour rafraîchir les nouveautés depuis l'application :
    python3 site-src/export_releases.py /chemin/vers/trame && python3 site-src/build.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SRC = Path(__file__).resolve().parent
URL = "https://trame.shizeh.workers.dev"  # adresse du site (liens canoniques, hreflang, sitemap)
SHIZEH = "https://shizeh.com"

DL = "https://github.com/shizeh/trame-versions/releases/latest"
STORE_GET = "https://get.microsoft.com/installer/download/9n85tsx3h531?referrer=appbadge"
STORE_PAGE = "https://apps.microsoft.com/detail/9n85tsx3h531"
ISSUES = "https://github.com/shizeh/trame-versions/issues/new/choose"
RELEASES = "https://github.com/shizeh/trame-versions/releases"
PRIVACY = "https://github.com/shizeh/trame-versions/blob/main/CONFIDENTIALITE.md"
INSTAGRAM = "https://www.instagram.com/baptisteshizeh/"
GITHUB = "https://github.com/shizeh"

LANGS = {
    "fr": {"home": "/", "news": "/nouveautes/", "badge": "fr-fr", "pdf": "/exemple/le-gardien-du-col.pdf", "img": "/img/"},
    "en": {"home": "/en/", "news": "/en/whats-new/", "badge": "en-us", "pdf": "/exemple/the-keeper-of-the-pass.pdf", "img": "/img/en/"},
    "es": {"home": "/es/", "news": "/es/novedades/", "badge": "es-es", "pdf": "/exemple/el-guardian-del-paso.pdf", "img": "/img/es/"},
}

T = json.loads((SRC / "texts.json").read_text(encoding="utf-8"))

DOWNLOAD_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 3a1 1 0 0 1 1 1v9.59l3.3-3.3a1 1 0 1 1 1.4 1.42l-5 5a1 1 0 0 1-1.4 0l-5-5a1 1 0 1 1 1.4-1.42l3.3 3.3V4a1 1 0 0 1 1-1Zm-8 15a1 1 0 0 1 1 1v1h14v-1a1 1 0 1 1 2 0v2a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-2a1 1 0 0 1 1-1Z"/></svg>'
INSTA_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 7.3a4.7 4.7 0 1 0 0 9.4 4.7 4.7 0 0 0 0-9.4Zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6Zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0ZM12 4.2c2.5 0 2.8 0 3.8.1 2.6.1 3.8 1.3 3.9 3.9.1 1 .1 1.3.1 3.8s0 2.8-.1 3.8c-.1 2.6-1.3 3.8-3.9 3.9-1 .1-1.3.1-3.8.1s-2.8 0-3.8-.1c-2.6-.1-3.8-1.3-3.9-3.9-.1-1-.1-1.3-.1-3.8s0-2.8.1-3.8C4.4 5.6 5.6 4.4 8.2 4.3c1-.1 1.3-.1 3.8-.1ZM12 2.5c-2.6 0-2.9 0-3.9.1-3.5.2-5.4 2.1-5.6 5.6-.1 1-.1 1.3-.1 3.8s0 2.9.1 3.9c.2 3.5 2.1 5.4 5.6 5.6 1 .1 1.3.1 3.9.1s2.9 0 3.9-.1c3.5-.2 5.4-2.1 5.6-5.6.1-1 .1-1.3.1-3.9s0-2.8-.1-3.8c-.2-3.5-2.1-5.4-5.6-5.6-1-.1-1.3-.1-3.9-.1Z"/></svg>'
GITHUB_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.2a10 10 0 0 0-3.2 19.5c.5.1.7-.2.7-.5v-1.7c-2.8.6-3.4-1.3-3.4-1.3-.5-1.2-1.1-1.5-1.1-1.5-.9-.6.1-.6.1-.6 1 .1 1.5 1 1.5 1 .9 1.6 2.4 1.1 2.9.8.1-.6.4-1.1.6-1.3-2.2-.3-4.6-1.1-4.6-5 0-1.1.4-2 1-2.7-.1-.3-.4-1.3.1-2.7 0 0 .8-.3 2.8 1a9.6 9.6 0 0 1 5 0c1.9-1.3 2.8-1 2.8-1 .5 1.4.2 2.4.1 2.7.6.7 1 1.6 1 2.7 0 3.9-2.3 4.7-4.6 5 .4.3.7.9.7 1.9v2.8c0 .3.2.6.7.5A10 10 0 0 0 12 2.2Z"/></svg>'


def e(s):
    """Texte à mettre dans le HTML. Les chaînes de texts.json peuvent déjà contenir des balises simples."""
    return s


def attr(s):
    return html.escape(s, quote=True)


def jsonld(lang):
    """Données structurées (schema.org) : l'application, le site et son auteur."""
    t = T[lang]
    L = LANGS[lang]
    try:
        version = json.loads((SRC / "releases.json").read_text(encoding="utf-8"))[0]["version"]
    except Exception:
        version = None
    author = {
        "@type": "Person",
        "@id": f"{URL}/#auteur",
        "name": "Baptiste Shizeh",
        "alternateName": "Shizeh",
        "url": SHIZEH,
        "sameAs": [SHIZEH, INSTAGRAM, GITHUB],
    }
    app = {
        "@type": "SoftwareApplication",
        "@id": f"{URL}/#app",
        "name": "Trame",
        "alternateName": ["Trame app", "Trame Shizeh"],
        "description": t["description"],
        "url": f"{URL}{L['home']}",
        "applicationCategory": "DesignApplication",
        "applicationSubCategory": t["seo_category"],
        "operatingSystem": "Windows 10, Windows 11",
        "inLanguage": ["fr", "en", "es"],
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "downloadUrl": DL,
        "installUrl": STORE_PAGE,
        "screenshot": f"{URL}/img/og.jpg",
        "image": f"{URL}/logo.svg",
        "author": {"@id": f"{URL}/#auteur"},
        "publisher": {"@id": f"{URL}/#auteur"},
    }
    if version:
        app["softwareVersion"] = version
    site = {
        "@type": "WebSite",
        "@id": f"{URL}/#site",
        "name": "Trame",
        "alternateName": "Trame app",
        "url": f"{URL}/",
        "inLanguage": lang,
        "publisher": {"@id": f"{URL}/#auteur"},
    }
    data = {"@context": "https://schema.org", "@graph": [app, site, author]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def head(lang, page, title, description):
    L = LANGS[lang]
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{URL}{LANGS[l][page]}">' for l in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{URL}{LANGS["fr"][page]}">'
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{attr(title)}</title>
<meta name="description" content="{attr(description)}">
<meta property="og:title" content="{attr(title)}">
<meta property="og:description" content="{attr(description)}">
<meta name="author" content="Baptiste Shizeh">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:site_name" content="Trame">
<meta property="og:url" content="{URL}{L[page]}">
<meta property="og:image" content="{URL}/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{attr(title)}">
<meta name="twitter:description" content="{attr(description)}">
<meta name="twitter:image" content="{URL}/img/og.jpg">
<meta property="og:locale" content="{ {'fr': 'fr_FR', 'en': 'en_US', 'es': 'es_ES'}[lang] }">
<meta name="theme-color" content="#7A2E5C">
<link rel="canonical" href="{URL}{L[page]}">
{alts}
<link rel="icon" href="/logo.svg" type="image/svg+xml">
<link rel="preload" href="/fonts/EBGaramond-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/SchibstedGrotesk-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css">
{jsonld(lang) if page == "home" else ""}
</head>
<body data-lang="{lang}">
"""


def topbar(lang, page, t, on_home):
    L = LANGS[lang]
    anchor = "" if on_home else L["home"]
    switch = "".join(
        f'<a href="{LANGS[l][page]}" hreflang="{l}" lang="{l}" data-setlang="{l}"{" aria-current=\"true\"" if l == lang else ""}>{l.upper()}</a>'
        for l in LANGS
    )
    return f"""
<header class="top">
  <a class="brand" href="{L['home']}" aria-label="{attr(t['brand_label'])}">
    <img src="/logo.svg" alt="" width="32" height="32">
    <span>trame</span>
  </a>
  <nav class="top-nav" aria-label="{attr(t['nav_label'])}">
    <a href="{anchor}#parcours">{t['nav_discover']}</a>
    <a href="{anchor}#faq">{t['nav_faq']}</a>
    <a href="{L['news']}">{t['nav_news']}</a>
    <span class="langs" role="group" aria-label="{attr(t['lang_label'])}">{switch}</span>
    <a class="top-cta" href="{DL}" data-download>{t['nav_download']}</a>
  </nav>
</header>
"""


def footer(lang, t):
    L = LANGS[lang]
    return f"""
<footer class="foot">
  <div class="foot-who">
    <p>{t['foot_by']}</p>
    <div class="social">
      <a href="{INSTAGRAM}" rel="me noopener" aria-label="Instagram @baptisteshizeh">{INSTA_ICON}<span>@baptisteshizeh</span></a>
      <a href="{GITHUB}" rel="me noopener" aria-label="GitHub @shizeh">{GITHUB_ICON}<span>@shizeh</span></a>
    </div>
  </div>
  <nav aria-label="{attr(t['foot_label'])}">
    <a href="{ISSUES}">{t['foot_issue']}</a>
    <a href="{L['news']}">{t['nav_news']}</a>
    <a href="{RELEASES}">{t['foot_releases']}</a>
    <a href="{PRIVACY}">{t['foot_privacy']}</a>
  </nav>
</footer>

<script src="/main.js" defer></script>
</body>
</html>
"""


def store_badge(lang, href, label, lazy=False):
    b = LANGS[lang]["badge"]
    return (f'<a class="store" href="{href}" aria-label="{attr(label)}">'
            f'<img src="https://get.microsoft.com/images/{b}%20dark.svg" '
            f"onerror=\"this.onerror=null;this.src='https://get.microsoft.com/images/en-us%20dark.svg'\" "
            f'width="168" height="62" alt=""{" loading=\"lazy\"" if lazy else ""}></a>')


def shot(lang, name, alt, sizes="(max-width: 900px) 100vw, 640px", lazy=True):
    d = LANGS[lang]["img"]
    return (f'<figure class="window"><img src="{d}{name}-780.webp" srcset="{d}{name}-780.webp 780w, {d}{name}.webp 1560w" '
            f'sizes="{sizes}" width="1560" height="848"{" loading=\"lazy\"" if lazy else ""} alt="{attr(alt)}"></figure>')


def home(lang):
    t = T[lang]
    L = LANGS[lang]
    tabs, panels = [], []
    for i, m in enumerate(t["modes"]):
        sel = i == 0
        tabs.append(f'<button role="tab" id="tab-{m["id"]}" aria-controls="panel-{m["id"]}" aria-selected="{str(sel).lower()}"{"" if sel else " tabindex=\"-1\""}>{m["tab"]}</button>')
        items = "".join(f"<li>{x}</li>" for x in m["items"])
        if m["id"] == "export":
            fig = ('<figure class="files" aria-hidden="true">'
                   + "".join(f'<div class="file"><span class="file-ext">{ext}</span><span class="file-name">{name}</span></div>' for ext, name in t["files"])
                   + "</figure>")
        else:
            fig = shot(lang, m["img"], m["alt"])
        panels.append(f"""
  <div class="panel" role="tabpanel" id="panel-{m['id']}" aria-labelledby="tab-{m['id']}"{"" if sel else " hidden"}>
    <div class="panel-text">
      <h3>{m['title']}</h3>
      <p>{m['text']}</p>
      <ul>{items}</ul>
    </div>
    {fig}
  </div>""")
    aussi = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in t["aussi"])
    faq = "".join(f'<details><summary>{q}</summary><div class="faq-a">{a}</div></details>' for q, a in t["faq"])
    steps = "".join(f"<li><h3>{h}</h3><p>{p}</p></li>" for h, p in t["steps"])
    steps = steps.replace("{DL}", DL)
    faq = faq.replace("{ISSUES}", ISSUES).replace("{INSTAGRAM}", INSTAGRAM).replace("{STORE}", STORE_PAGE)
    body = f"""
<main>

<section class="hero">
  <div class="hero-text">
    <h1>{t['h1']}</h1>
    <p class="lede">{t['lede']}</p>
    <div class="hero-actions">
      <a class="btn" href="{DL}" data-download>{DOWNLOAD_ICON} {t['download_windows']}</a>
      {store_badge(lang, STORE_GET, t['store_get'])}
      <p class="hero-meta">{t['hero_meta']} <span data-version>{t['windows']}</span></p>
    </div>
  </div>
  <figure class="hero-video">
    <video autoplay muted loop playsinline preload="metadata" poster="/video/trame-{lang}.webp" aria-label="{attr(t['video_label'])}">
      <source src="/video/trame-{lang}.mp4" type="video/mp4">
    </video>
  </figure>
</section>

<section class="parcours" id="parcours" aria-labelledby="parcours-h">
  <div class="section-head">
    <h2 id="parcours-h">{t['parcours_h']}</h2>
    <p>{t['parcours_p']}</p>
  </div>
  <div class="modes" role="tablist" aria-label="{attr(t['modes_label'])}">
    {''.join(tabs)}
  </div>
  {''.join(panels)}
</section>

<section class="aussi" aria-labelledby="aussi-h">
  <h2 id="aussi-h">{t['aussi_h']}</h2>
  <dl class="aussi-list">{aussi}</dl>
  <div class="aussi-shot">{shot(lang, 'carnet', t['carnet_alt'], '(max-width: 900px) 100vw, 900px')}</div>
</section>

<section class="sample" aria-labelledby="sample-h">
  <div class="sample-book" aria-hidden="true"><span>{t['sample_book']}</span></div>
  <div class="sample-text">
    <h2 id="sample-h">{t['sample_h']}</h2>
    <p>{t['sample_p']}</p>
    <a class="btn btn-light" href="{L['pdf']}" download>{DOWNLOAD_ICON} {t['sample_btn']}</a>
  </div>
</section>

<section class="prive" aria-labelledby="prive-h">
  <h2 id="prive-h">{t['prive_h']}</h2>
  <p>{t['prive_p']} <a href="{PRIVACY}">{t['prive_link']}</a></p>
</section>

<section class="faq" id="faq" aria-labelledby="faq-h">
  <h2 id="faq-h">{t['faq_h']}</h2>
  <div class="faq-list">{faq}</div>
</section>

<section class="installer" id="installer" aria-labelledby="installer-h">
  <h2 id="installer-h">{t['install_h']}</h2>
  <ol class="steps">{steps}</ol>
  <div class="store-alt">
    <p>{t['store_alt']}</p>
    {store_badge(lang, STORE_PAGE, t['store_see'], lazy=True)}
  </div>
  <p class="installer-note">{t['install_note']}</p>
</section>

</main>
"""
    return head(lang, "home", t["title"], t["description"]) + topbar(lang, "home", t, True) + body + footer(lang, t)


def news(lang):
    t = T[lang]
    rel = json.loads((SRC / "releases.json").read_text(encoding="utf-8"))
    items = []
    for i, r in enumerate(rel):
        x = r[lang]
        lis = "".join(f"<li>{html.escape(s)}</li>" for s in x["items"])
        items.append(f"""
  <article class="release">
    <p class="release-v">{t['version']} {r['version']}{f' <span class="release-new">{t["latest"]}</span>' if i == 0 else ''}</p>
    <h2>{html.escape(x['title'])}</h2>
    <ul>{lis}</ul>
  </article>""")
    body = f"""
<main class="news">
<section class="news-head">
  <h1>{t['news_h']}</h1>
  <p class="lede">{t['news_p']}</p>
  <p class="news-all"><a href="{RELEASES}">{t['news_all']}</a></p>
</section>
<section class="news-list">{''.join(items)}
</section>
<section class="news-cta">
  <a class="btn" href="{DL}" data-download>{DOWNLOAD_ICON} {t['download_windows']}</a>
  {store_badge(lang, STORE_GET, t['store_get'])}
</section>
</main>
"""
    return head(lang, "news", t["news_title"], t["news_p"]) + topbar(lang, "news", t, False) + body + footer(lang, t)


def sitemap():
    rows = []
    for page in ("home", "news"):
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{URL}{LANGS[l][page]}"/>' for l in LANGS)
        alts += f'<xhtml:link rel="alternate" hreflang="x-default" href="{URL}{LANGS["fr"][page]}"/>'
        for l in LANGS:
            rows.append(f"  <url><loc>{URL}{LANGS[l][page]}</loc>{alts}</url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(rows) + "\n</urlset>\n")


(SITE / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
(SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n", encoding="utf-8")
print("→ site/sitemap.xml, site/robots.txt")

for lang, L in LANGS.items():
    for page, fn in (("home", home), ("news", news)):
        out = SITE / L[page].strip("/") / "index.html" if L[page] != "/" else SITE / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(fn(lang), encoding="utf-8")
        print("→", out.relative_to(ROOT))
