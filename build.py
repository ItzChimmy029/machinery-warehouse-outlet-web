#!/usr/bin/env python3
"""Generates the static HTML pages for Machinery Warehouse Outlet from
shared header/footer partials, so every page stays in sync without a
runtime include (the site is meant to also work opened straight from
disk via file://, where fetch() of local partials would be blocked)."""

import os

OUT = os.path.dirname(os.path.abspath(__file__))

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'

FAVICON = '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 100 100%27%3E%3Crect width=%27100%27 height=%27100%27 fill=%27%23c81e22%27/%3E%3Ctext x=%2750%27 y=%2772%27 font-size=%2770%27 font-family=%27Arial Black,Arial,sans-serif%27 font-weight=%27900%27 fill=%27white%27 text-anchor=%27middle%27%3EM%3C/text%3E%3C/svg%3E">'

# Meta-deliverable security headers. GitHub Pages does not let the repo owner
# set real HTTP response headers (no server config access), so X-Frame-Options,
# Strict-Transport-Security and Permissions-Policy cannot be set here — those
# require actual headers and are silently ignored as <meta>. Content-Security-
# Policy and Referrer-Policy *are* honored via <meta> for most directives and
# are set below. See README "Security" section for the header-hosting
# limitation and the recommended mitigation if this site moves behind a host
# that supports custom headers.
CSP = (
    "default-src 'self'; "
    "script-src 'self' https://cdnjs.cloudflare.com; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data:; "
    "connect-src 'self'; "
    "frame-src https://www.google.com; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self';"
)

def head(title, desc, transparent_header=False, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title} | Machinery Warehouse Outlet</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} | Machinery Warehouse Outlet">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="robots" content="index,follow">
{FAVICON}
{FONTS}
<link rel="stylesheet" href="css/styles.css">
{extra}
</head>
<body data-transparent-header="{'true' if transparent_header else 'false'}">
"""

def header():
    links = [
        ("index.html", "Home"),
        ("machinery.html", "Machinery"),
        ("spare-parts.html", "Spare Parts"),
        ("about.html", "About"),
        ("contact.html", "Contact"),
    ]
    nav_links = "\n".join(f'<a href="{href}">{label}</a>' for href, label in links)
    mobile_links = "\n".join(f'<a href="{href}">{label}<span aria-hidden="true">&rarr;</span></a>' for href, label in links)
    return f"""
<header class="site-header">
  <div class="container nav-inner">
    <a href="index.html" class="brand"><span class="brand-mark">M</span>achinery Warehouse Outlet<span class="brand-sub">Industrial Machines &amp; Spare Parts</span></a>
    <nav class="nav-links" aria-label="Primary">
      {nav_links}
    </nav>
    <div class="nav-actions">
      <a href="quote.html" class="btn btn-primary btn-sm">Request a Quote</a>
      <button class="nav-toggle" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu">
  <div class="mobile-menu-inner">
    {mobile_links}
    <a href="quote.html" class="btn btn-primary btn-block">Request a Quote</a>
    <div class="mobile-contact">
      <a href="tel:" data-tel data-fill="text"></a>
      <a href="mailto:" data-email data-fill="text"></a>
    </div>
  </div>
</div>
"""

def mobile_actionbar():
    return """
<div class="mobile-actionbar">
  <a href="tel:" data-tel>
    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
    Call
  </a>
  <a href="machinery.html">
    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
    Machinery
  </a>
  <a href="quote.html" class="quote">
    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
    Quote
  </a>
</div>
"""

def footer():
    cat_links = "\n".join(f'<li><a href="machinery.html?category={c["slug"]}">{c["name"]}</a></li>' for c in CATEGORIES_META)
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="brand"><span class="brand-mark">M</span>achinery Warehouse Outlet</div>
        <p style="max-width:34ch;font-size:0.92rem;">Home of industrial machines and spare parts. Plastic machines, poly packaging machines and water packaging machines.</p>
      </div>
      <div>
        <h4>Machinery</h4>
        <ul>
          {cat_links}
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="about.html">About Us</a></li>
          <li><a href="spare-parts.html">Spare Parts</a></li>
          <li><a href="quote.html">Request a Quote</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><span data-phone-list></span></li>
          <li><a href="#" data-whatsapp data-whatsapp-intent="general" data-whatsapp-label></a></li>
          <li><span data-email-list></span></li>
          <li>Awada Industrial Zone, Anambra State</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span class="js-year"></span> Machinery Warehouse Outlet. All rights reserved.</span>
      <span>Home of Industrial Machines and Spare Parts</span>
    </div>
  </div>
</footer>
"""

def lightbox():
    return """
<div class="lightbox">
  <button class="lightbox-close" aria-label="Close image">&times;</button>
  <img alt="">
</div>
"""

def floating_buttons():
    return """
<a href="#" class="float-btn float-whatsapp" data-whatsapp data-whatsapp-intent="general" aria-label="Chat with us on WhatsApp" title="Chat on WhatsApp">
  <svg class="icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.79.47 3.47 1.29 4.93L2 22l5.31-1.39a9.86 9.86 0 0 0 4.73 1.2h.01c5.46 0 9.9-4.45 9.9-9.91C21.96 6.45 17.5 2 12.04 2zm5.8 14.06c-.24.68-1.4 1.3-1.93 1.36-.5.06-1.03.26-3.4-.71-2.9-1.19-4.75-4.1-4.9-4.29-.14-.19-1.17-1.55-1.17-2.96 0-1.4.74-2.08 1-2.37.26-.29.57-.36.76-.36.19 0 .38 0 .55.01.18.01.42-.07.65.5.24.58.82 2 .89 2.15.07.14.12.31.02.5-.1.19-.15.31-.29.48-.15.17-.31.38-.44.5-.15.15-.3.3-.13.6.17.29.76 1.26 1.63 2.04 1.12 1 2.07 1.31 2.36 1.46.29.14.46.12.63-.07.17-.19.72-.84.92-1.13.19-.29.38-.24.64-.14.26.1 1.66.79 1.94.93.29.14.48.21.55.33.07.12.07.68-.17 1.36z"/></svg>
</a>
<button type="button" class="float-btn float-totop" aria-label="Back to top" title="Back to top">
  <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M12 19V5"/><path d="M5 12l7-7 7 7"/></svg>
</button>
"""

def scripts():
    return """
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js" defer crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="js/data.js" defer></script>
<script src="js/main.js" defer></script>
"""

def page(title, desc, body, transparent_header=False, extra_head="", show_actionbar=True):
    html = head(title, desc, transparent_header, extra_head)
    html += header()
    html += body
    html += footer()
    if show_actionbar:
        html += mobile_actionbar()
    html += floating_buttons()
    html += lightbox()
    html += scripts()
    html += "\n</body>\n</html>\n"
    return html

CATEGORIES_META = [
    {"slug": "film-blowing", "name": "Film Blowing Machines"},
    {"slug": "bag-making", "name": "Bag Making Machines"},
    {"slug": "water-packaging", "name": "Water Packaging Machines"},
    {"slug": "recycling", "name": "Recycling & Pelletizing"},
    {"slug": "printing", "name": "Printing Machines"},
    {"slug": "moulding", "name": "Blow & Injection Moulding"},
    {"slug": "punching", "name": "Punching Machines"},
]

def count_products():
    """Counts PRODUCTS entries directly from js/data.js so the homepage
    stat never drifts out of sync with the real data when products are
    added or removed. Counts occurrences of the 'slug:' key inside the
    PRODUCTS array specifically (not CATEGORIES, which also has slugs)."""
    with open(os.path.join(OUT, "js", "data.js")) as f:
        src = f.read()
    start = src.index("const PRODUCTS")
    end = src.index("\nconst SPARE_PARTS_GROUPS")
    return src[start:end].count("slug:")

PRODUCT_COUNT = count_products()

def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
    print("wrote", name)

if __name__ == "__main__":
    print("Partials ready — page bodies are assembled in build_pages.py")
