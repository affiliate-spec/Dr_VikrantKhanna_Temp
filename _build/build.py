#!/usr/bin/env python3
"""
Assemble the Santosh Gastro Gynae Clinic site.

Each file in _build/pages/ is a page body. Its first line is a JSON comment:
    <!-- {"file": "index.html", "title": "...", "desc": "...", "nav": "home"} -->
The shared head, header, drawer, footer and floating actions are added around it
and the finished page is written to the site root.

Placeholders available inside page bodies:
    {{i:name}}   Font Awesome icon from the sprite (#i-name)
    {{l:name}}   Line icon from the sprite (#l-name)
    {{PHONE}} {{TEL}} {{WA}} {{WA_VK}} {{WA_RK}} {{MAP}} {{MAP_EMBED}} {{ADDR}} {{BOOK}}

It also minifies _build/src/site.css and _build/src/site.js into assets/, adds
cache-busting versions, and inlines only the icon symbols each page uses.

Run:  python3 _build/build.py
"""

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

# --- Practice details (edit here, then rebuild) -------------------------------

SITE_URL = ""  # e.g. "https://www.santoshgastrogynae.com" — leave empty until the domain is live
PHONE = "8090935545"
TEL = "tel:+918090935545"
WA_NUMBER = "918090935545"   # confirm this number is on WhatsApp
ADDR_LINES = ["M-324, Sector-D1, LDA Colony, Kanpur Road", "Opp. Police Adhikari Awas, Parag Chauraha", "Lucknow, Uttar Pradesh"]
ADDR = ", ".join(ADDR_LINES)
MAP = "https://www.google.com/maps/search/?api=1&query=" + quote("Santosh Gastro Gynae Clinic, M-324, Sector D1, LDA Colony, Lucknow")
MAP_EMBED = "https://www.google.com/maps?q=" + quote("M-324, Sector D1, LDA Colony, Kanpur Road, Lucknow") + "&output=embed"


def wa(text):
    return f"https://wa.me/{WA_NUMBER}?text={quote(text)}"


WA = wa("Hello, I would like to book an appointment at Santosh Gastro Gynae Clinic.")
WA_VK = wa("Hello, I would like to book an appointment with Dr. Vikrant Khanna (Gastroenterology & Liver) at Santosh Gastro Gynae Clinic.")
WA_RK = wa("Hello, I would like to book an appointment with Dr. Ritu Khanna (Obstetrics & Gynaecology) at Santosh Gastro Gynae Clinic.")
BOOK = "contact.html#book"

NAV = [
    ("home", "index.html", "Home"),
    ("about", "about.html", "About Us"),
    ("gastro", "gastroenterology.html", "Gastroenterology &amp; Liver"),
    ("women", "womens-health.html", "Women&rsquo;s Health"),
    ("procedures", "procedures.html", "Procedures"),
    ("education", "patient-education.html", "Patient Education"),
    ("contact", "contact.html", "Contact"),
]


def icon(name):
    return f'<svg class="sg-ic" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'


def line(name):
    return f'<svg class="sg-ic sg-ic--line" aria-hidden="true" focusable="false"><use href="#l-{name}"/></svg>'


def head(meta):
    title = meta["title"]
    desc = meta["desc"]
    url = f'{SITE_URL}/{"" if meta["file"] == "index.html" else meta["file"]}' if SITE_URL else ""
    og_img = f"{SITE_URL}/assets/img/logo/og-image.jpg" if SITE_URL else "assets/img/logo/og-image.jpg"
    canonical = f'\n  <link rel="canonical" href="{url}">\n  <meta property="og:url" content="{url}">' if url else ""
    schema = SCHEMA if meta["file"] == "index.html" else ""
    preload = ""
    if meta.get("preload"):  # e.g. "vikrant|(max-width: 680px) 46vw, 270px" — mirrors the <img> srcset/sizes
        who, sizes = meta["preload"].split("|")
        full = {"vikrant": 588, "ritu": 580}[who]
        srcset = ", ".join(f"assets/img/doctors/dr-{who}-{w}.webp {w}w" for w in (240, 360, 480, full))
        preload = f'\n  <link rel="preload" as="image" imagesrcset="{srcset}" imagesizes="{sizes}" fetchpriority="high">'
    return f"""<!doctype html>
<html lang="en-IN" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#1C2F4D">{canonical}
  <meta property="og:site_name" content="Santosh Gastro Gynae Clinic">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_IN">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{og_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">

  <link rel="icon" type="image/svg+xml" href="assets/img/logo/santosh-mark.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="assets/img/logo/icon-32.png">
  <link rel="icon" type="image/png" sizes="192x192" href="assets/img/logo/icon-192.png">
  <link rel="apple-touch-icon" sizes="180x180" href="assets/img/logo/icon-180.png">

{preload}
  <link rel="stylesheet" href="assets/css/site.css?v={CSS_V}">{schema}
</head>
"""


SCHEMA = f"""
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "MedicalClinic",
    "name": "Santosh Gastro Gynae Clinic",
    "description": "Specialist care for Digestive Health & Women's Health in Lucknow — Gastroenterology, Hepatology, Endoscopy, Obstetrics and Gynaecology.",
    "telephone": "+91{PHONE}",
    "medicalSpecialty": ["Gastroenterologic", "Obstetric", "Gynecologic"],
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "M-324, Sector-D1, LDA Colony, Kanpur Road, opp. Police Adhikari Awas, Parag Chauraha",
      "addressLocality": "Lucknow",
      "addressRegion": "Uttar Pradesh",
      "addressCountry": "IN"
    }},
    "openingHoursSpecification": [
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "12:00", "closes": "17:00" }},
      {{ "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"], "opens": "19:00", "closes": "21:00" }}
    ],
    "employee": [
      {{ "@type": "Physician", "name": "Dr. Vikrant Khanna", "description": "MBBS, MD, PDCC, DM (SGPGI) — Gastroenterologist & Hepatologist" }},
      {{ "@type": "Physician", "name": "Dr. Ritu Khanna", "description": "MBBS, MS (Obstetrics & Gynaecology) — Obstetrician & Gynaecologist" }}
    ]
  }}
  </script>"""


def brand(tag="a"):
    inner = """<img src="assets/img/logo/santosh-mark.svg" width="50" height="50" alt="">
        <span class="sg-brand__text">
          <span class="sg-brand__name">SANTOSH</span>
          <span class="sg-brand__sub"><b>Gastro</b> · <i>Gynae</i> · Clinic</span>
        </span>"""
    if tag == "a":
        return f'<a class="sg-brand" href="index.html" aria-label="Santosh Gastro Gynae Clinic — home">\n        {inner}\n      </a>'
    return f'<span class="sg-brand">\n        {inner}\n      </span>'


def header(active):
    active_attr = ' class="active" aria-current="page"'
    nav = "\n".join(
        f'        <a href="{href}"{active_attr if key == active else ""}>{label}</a>'
        for key, href, label in NAV
    )
    dnav = "\n".join(
        f'        <a href="{href}"{active_attr if key == active else ""}>{label} {icon("chevron-right")}</a>'
        for key, href, label in NAV
    )
    return f"""
<body>
  <a class="sg-skip" href="#main">Skip to content</a>
  <svg class="sg-sprite" aria-hidden="true" focusable="false">
    <!-- Solid icons: Font Awesome Free 6, CC BY 4.0, https://fontawesome.com/license/free -->
{{{{SPRITE}}}}
  </svg>

  <div class="sg-topbar">
    <div class="sg-container sg-topbar__in">
      <div class="sg-topbar__list">
        <a href="{MAP}" target="_blank" rel="noopener">{icon("location-dot")} M-324, Sector-D1, LDA Colony, Lucknow</a>
        <span class="sg-topbar__hide">{icon("clock")} Monday – Saturday · Sunday closed</span>
      </div>
      <div class="sg-topbar__list">
        <a href="{TEL}">{icon("phone")} {PHONE}</a>
        <a class="sg-topbar__hide" href="{WA}" target="_blank" rel="noopener">{icon("whatsapp")} WhatsApp</a>
      </div>
    </div>
  </div>

  <header class="sg-header">
    <div class="sg-container sg-header__in">
      {brand()}
      <nav class="sg-nav" aria-label="Primary">
{nav}
      </nav>
      <div class="sg-header__cta">
        <a class="sg-header__call" href="{TEL}" aria-label="Call {PHONE}">{icon("phone")}</a>
        <a class="sg-header__call sg-header__call--wa" href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp the clinic">{icon("whatsapp")}</a>
        <a class="sg-btn sg-btn--primary" href="{BOOK}">{icon("calendar-check")} Book Appointment</a>
        <button class="sg-burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="sgDrawer">{icon("bars")}</button>
      </div>
    </div>
  </header>

  <div class="sg-drawer-wrap">
    <div class="sg-overlay"></div>
    <aside class="sg-drawer" id="sgDrawer" aria-label="Menu">
      <div class="sg-drawer__head">
        {brand("span")}
        <button class="sg-drawer__close" type="button" aria-label="Close menu">{icon("xmark")}</button>
      </div>
      <nav aria-label="Mobile">
{dnav}
      </nav>
      <div class="sg-drawer__cta">
        <a class="sg-btn sg-btn--primary" href="{BOOK}">{icon("calendar-check")} Book Appointment</a>
        <a class="sg-btn sg-btn--wa" href="{WA}" target="_blank" rel="noopener">{icon("whatsapp")} WhatsApp the Clinic</a>
        <a class="sg-btn sg-btn--outline" href="{TEL}">{icon("phone")} Call {PHONE}</a>
      </div>
      <div class="sg-drawer__meta">
        <div>{icon("location-dot")}<span>{ADDR}</span></div>
        <div>{icon("clock")}<span>Monday – Saturday · Sunday closed</span></div>
      </div>
    </aside>
  </div>

  <main id="main">
"""


def footer():
    links = "\n".join(f'          <a href="{href}">{label}</a>' for _, href, label in NAV)
    return f"""  </main>

  <footer class="sg-footer">
    <div class="sg-container">
      <div class="sg-footer__grid">
        <div>
          <div class="sg-footer__brand">
            <img src="assets/img/logo/santosh-mark.svg" width="58" height="58" alt="">
            <div>
              <strong>Santosh Gastro Gynae Clinic</strong>
              <span>Lucknow</span>
            </div>
          </div>
          <p class="sg-footer__tag">Specialist care for Digestive Health &amp; Women&rsquo;s Health.</p>
          <div class="sg-footer__docs">
            <span><i></i> Dr. Vikrant Khanna — Gastroenterologist &amp; Hepatologist</span>
            <span><i></i> Dr. Ritu Khanna — Obstetrician &amp; Gynaecologist</span>
          </div>
        </div>
        <div>
          <h3>Explore</h3>
          <nav class="sg-footer__links" aria-label="Footer">
{links}
          </nav>
        </div>
        <div>
          <h3>Consultation Hours</h3>
          <div class="sg-footer__links">
            <span><strong style="color:#fff;font-weight:600">Dr. Vikrant Khanna</strong><br>12:00 – 5:00 pm · 7:00 – 9:00 pm</span>
            <span><strong style="color:#fff;font-weight:600">Dr. Ritu Khanna</strong><br>12:00 – 1:00 pm · 7:00 – 8:00 pm</span>
            <span>Monday – Saturday · Sunday closed</span>
          </div>
        </div>
        <div>
          <h3>Visit &amp; Contact</h3>
          <div class="sg-footer__contact">
            <div>{icon("location-dot")}<a href="{MAP}" target="_blank" rel="noopener">{"<br>".join(ADDR_LINES)}</a></div>
            <div>{icon("phone")}<a href="{TEL}">{PHONE}</a></div>
            <div>{icon("whatsapp")}<a href="{WA}" target="_blank" rel="noopener">WhatsApp the clinic</a></div>
          </div>
        </div>
      </div>
      <div class="sg-footer__bottom">
        <span>&copy; <span data-year>2026</span> Santosh Gastro Gynae Clinic, Lucknow. All rights reserved.</span>
        <span>Information on this website is for general education and is not a substitute for a medical consultation.</span>
      </div>
    </div>
  </footer>

  <div class="sg-float">
    <button class="sg-float__top" type="button" aria-label="Back to top">{icon("arrow-up")}</button>
    <a class="sg-float__wa" href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp the clinic">{icon("whatsapp")}</a>
  </div>
  <nav class="sg-mbar" aria-label="Quick contact">
    <a class="sg-mbar__call" href="{TEL}">{icon("phone")} Call</a>
    <a class="sg-mbar__wa" href="{WA}" target="_blank" rel="noopener">{icon("whatsapp")} WhatsApp</a>
    <a class="sg-mbar__book" href="{BOOK}">{icon("calendar-check")} Book</a>
  </nav>

  <script src="assets/js/site.js?v={JS_V}" defer></script>
</body>
</html>
"""


SYMBOLS = {
    m.group(1): m.group(0)
    for part in ("partials/fa-symbols.html", "partials/line-symbols.html")
    for m in re.finditer(r'<symbol id="([^"]+)".*?</symbol>', (HERE / part).read_text(), re.S)
}


def sprite_for(html):
    """Only the symbols this page actually references."""
    used = sorted(set(re.findall(r'href="#([il]-[a-z0-9-]+)"', html)))
    missing = [u for u in used if u not in SYMBOLS]
    if missing:
        raise SystemExit(f"Missing icon symbols: {missing}")
    return "\n".join(SYMBOLS[u] for u in used)


def minify_css(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = re.sub(r":\s+", ":", css)
    css = css.replace(";}", "}")
    return css.strip() + "\n"


def minify_js(js):
    js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    lines = [ln.strip() for ln in js.splitlines()]
    return "\n".join(ln for ln in lines if ln and not ln.startswith("//")) + "\n"


def minify_html(html):
    html = re.sub(r"<!--(?!\s*Solid icons).*?-->", "", html, flags=re.S)
    return re.sub(r"\s*\n\s*", "\n", html).strip() + "\n"


def build_asset(src, dest, fn):
    out = fn((HERE / src).read_text())
    (ROOT / dest).write_text(out)
    return hashlib.md5(out.encode()).hexdigest()[:8]


CSS_V = build_asset("src/site.css", "assets/css/site.css", minify_css)
JS_V = build_asset("src/site.js", "assets/js/site.js", minify_js)

TOKENS = {
    "{{PHONE}}": PHONE, "{{TEL}}": TEL, "{{WA}}": WA, "{{WA_VK}}": WA_VK, "{{WA_RK}}": WA_RK,
    "{{MAP}}": MAP, "{{MAP_EMBED}}": MAP_EMBED, "{{ADDR}}": ADDR, "{{BOOK}}": BOOK,
}


CTA = (HERE / "partials/cta.html").read_text()


def render(body):
    body = body.replace("{{CTA}}", CTA)
    body = re.sub(r"\{\{i:([a-z0-9-]+)\}\}", lambda m: icon(m.group(1)), body)
    body = re.sub(r"\{\{l:([a-z0-9-]+)\}\}", lambda m: line(m.group(1)), body)
    for k, v in TOKENS.items():
        body = body.replace(k, v)
    left = re.findall(r"\{\{[^}]*\}\}", body)
    if left:
        raise SystemExit(f"Unknown placeholders: {sorted(set(left))}")
    return body


def main():
    for src in sorted((HERE / "pages").glob("*.html")):
        text = src.read_text()
        first, _, body = text.partition("\n")
        meta = json.loads(first.strip()[4:-3])
        html = head(meta) + header(meta["nav"]) + render(body) + footer()
        html = html.replace("{{SPRITE}}", sprite_for(html))
        (ROOT / meta["file"]).write_text(minify_html(html))
        print(f"built {meta['file']}")


if __name__ == "__main__":
    main()
