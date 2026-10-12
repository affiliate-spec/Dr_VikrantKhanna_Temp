# Santosh Gastro Gynae Clinic — website

Static site, no build step needed to host it. Upload everything **except `_build/`** to the web server.

## Pages
| File | Content |
|---|---|
| `index.html` | Home: hero, the two specialities, symptoms, life stages, procedures, patient education, doctors, testimonials, clinic, booking |
| `about.html` | Clinic story and both doctors' full profiles |
| `gastroenterology.html` | Dr. Vikrant Khanna: digestive, liver, biliary/pancreas, endoscopy |
| `womens-health.html` | Dr. Ritu Khanna: gynaecology, pregnancy, adolescence, PCOS, menopause |
| `procedures.html` | Endoscopy and the full facilities list from the clinic leaflet |
| `patient-education.html` | 12 Q&As (each has an anchor, e.g. `#fatty-liver`) |
| `contact.html` | Per-doctor booking (`#book`), hours, address, map |

## Editing
Pages are generated from `_build/pages/*.html` plus the shared header and footer in `_build/build.py`.
Phone, WhatsApp, address and map live at the top of `build.py`. After any edit, run:

    python3 _build/build.py

When the domain is live, set `SITE_URL` in `build.py` and rebuild. That adds the canonical and og:url tags.

## Logo (`assets/img/logo/`)
- `santosh-mark.svg`: master mark (cross, caregiver + child, teal/rose ring)
- `santosh-logo-horizontal.png` / `-reversed.png`: lockup for light / dark backgrounds
- `santosh-seal.png`: circular heritage seal for print, stamps and letterheads
- `icon-*.png`, `og-image.jpg`: favicons and the social-share image
- Re-export: open `_build/logo-render.html#lockup` (or `#seal`, `#icon`) in Chrome
