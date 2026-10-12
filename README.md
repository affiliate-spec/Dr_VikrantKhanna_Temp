# Santosh Gastro Gynae Clinic — website

A static site with no runtime dependencies or third-party requests. To deploy, upload everything **except `_build/`**.

## Pages
| File | Content |
|---|---|
| `index.html` | Home |
| `about.html` | Clinic story and both doctors' profiles |
| `gastroenterology.html` | Dr. Vikrant Khanna: digestive, liver, biliary/pancreas, endoscopy |
| `womens-health.html` | Dr. Ritu Khanna: gynaecology, pregnancy, adolescence, PCOS, menopause |
| `procedures.html` | Endoscopy and the full facilities list |
| `patient-education.html` | 12 Q&As, each with an anchor such as `#fatty-liver` |
| `contact.html` | Booking for each doctor (`#book`), hours, address, map |

## Editing
Don't edit the root `.html` files or `assets/css`/`assets/js` directly. They are generated and minified.

| Change | Edit |
|---|---|
| Page text | `_build/pages/*.html` |
| Header, footer, phone, WhatsApp, address | `_build/build.py` (top of the file) |
| Styles | `_build/src/site.css` |
| Behaviour | `_build/src/site.js` |
| Icons | `_build/partials/*-symbols.html` |

Then run:

    python3 _build/build.py

The build:
- minifies the HTML, CSS and JS,
- adds cache-busting `?v=` hashes to the CSS and JS links,
- puts only the icons each page uses into that page,
- stops with an error if a placeholder or icon is missing.

When the domain is live, set `SITE_URL` in `build.py` and rebuild. That adds the canonical and og:url tags.

## Performance notes
- **Fonts:** Fraunces and Plus Jakarta Sans are self-hosted Latin subsets in `assets/fonts/` (SIL OFL 1.1). Metric-matched fallback fonts prevent layout shift while they load.
- **Portraits:** WebP at 240, 360 and 480 px plus full size, and a 128 px thumbnail, served with `srcset`/`sizes`. The hero image is preloaded and everything below the fold is lazy-loaded.
- **Map:** Google Maps loads only when the visitor taps "Show map".
- **New photos:** to add or replace a photo, export the same widths as WebP with `cwebp -q 80 -m 6 -sharp_yuv -metadata none`.

## Logo
`assets/img/logo/santosh-mark.svg` is the master mark. To re-export the print versions (horizontal lockup, reversed lockup, seal, app icon), serve the site folder locally, for example with `python3 -m http.server`. Then open `_build/logo-render.html#lockup` in Chrome (or `#lockup-light`, `#seal`, `#icon`). The social-share image template is `_build/og-render.html`.
