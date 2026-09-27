#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import page, write, CATEGORIES_META

# ---------------------------------------------------------------- HOME -----
category_cards = ""
for c in CATEGORIES_META:
    category_cards += f"""
      <a href="machinery.html?category={c['slug']}" class="cat-card reveal">
        <img src="assets/img/{{IMG_MAP}}{c['slug']}.jpg" alt="{c['name']}" loading="lazy">
        <div class="cat-card-body">
          <h3>{c['name']}</h3>
        </div>
      </a>"""

CAT_IMAGE = {
    "film-blowing": "cat-film-blowing",
    "bag-making": "cat-bag-making",
    "water-packaging": "prod-sachet-water",
    "recycling": "cat-recycling",
    "printing": "cat-printing",
    "moulding": "cat-moulding",
    "punching": "cat-punching",
    "fuel-dispensing": "cat-fuel",
}
category_cards = ""
for i, c in enumerate(CATEGORIES_META):
    category_cards += f"""
      <a href="machinery.html?category={c['slug']}" class="cat-card reveal" style="--i:{i % 4}">
        <img src="assets/img/{CAT_IMAGE[c['slug']]}.jpg" alt="{c['name']}" loading="lazy">
        <div class="cat-card-body">
          <h3>{c['name']}</h3>
        </div>
      </a>"""

FEATURED_SLUGS = [
    "ibc-rotary-film-blowing-machine",
    "six-lines-bag-making-machine",
    "sachet-water-filling-sealing-packing-machine",
    "flexo-printing-machine-series",
    "blow-moulding-machine",
    "double-pump-fuel-dispenser",
]
FEATURED_IMG = {
    "ibc-rotary-film-blowing-machine": "prod-ibc-tower",
    "six-lines-bag-making-machine": "prod-bag-6line",
    "sachet-water-filling-sealing-packing-machine": "prod-sachet-water",
    "flexo-printing-machine-series": "prod-flexo",
    "blow-moulding-machine": "prod-blow-mould",
    "double-pump-fuel-dispenser": "prod-fuel-double",
}
FEATURED_NAME = {
    "ibc-rotary-film-blowing-machine": "Three-Layer Co-Extrusion IBC Film Blowing Machine",
    "six-lines-bag-making-machine": "Six Lines Bag Making Machine",
    "sachet-water-filling-sealing-packing-machine": "Sachet Water Filling &amp; Packing Machine",
    "flexo-printing-machine-series": "Flexo Printing Machine Series",
    "blow-moulding-machine": "Blow Moulding Machine",
    "double-pump-fuel-dispenser": "Double Pump Fuel Dispenser",
}
FEATURED_CAT = {
    "ibc-rotary-film-blowing-machine": "Film Blowing",
    "six-lines-bag-making-machine": "Bag Making",
    "sachet-water-filling-sealing-packing-machine": "Water Packaging",
    "flexo-printing-machine-series": "Printing",
    "blow-moulding-machine": "Moulding",
    "double-pump-fuel-dispenser": "Fuel Dispensing",
}

featured_cards = ""
for i, slug in enumerate(FEATURED_SLUGS):
    featured_cards += f"""
      <div class="card reveal" style="--i:{i % 3}">
        <a href="product.html?slug={slug}" class="card-media">
          <img src="assets/img/{FEATURED_IMG[slug]}.jpg" alt="{FEATURED_NAME[slug]}" loading="lazy">
          <span class="tag">{FEATURED_CAT[slug]}</span>
        </a>
        <div class="card-body">
          <span class="cat-label">{FEATURED_CAT[slug]}</span>
          <h3><a href="product.html?slug={slug}">{FEATURED_NAME[slug]}</a></h3>
        </div>
        <div class="card-foot">
          <a href="product.html?slug={slug}">View Details</a>
          <a href="quote.html?product={slug}" class="foot-quote">Request Quote</a>
        </div>
      </div>"""

home_body = f"""
<section class="hero">
  <div class="hero-canvas-wrap">
    <canvas id="hero-canvas"></canvas>
    <div class="hero-photo-fallback hidden" style="background-image:url('assets/img/hero-ibc-tower.jpg')"></div>
  </div>
  <div class="container hero-content">
    <div class="kicker">MACHINERY WAREHOUSE OUTLET</div>
    <h1 class="reveal is-visible">Industrial Machines &amp; Spare Parts, Ready for Your Production Line</h1>
    <p class="lede reveal is-visible" style="transition-delay:120ms">Plastic machines, poly packaging machines, water packaging machines and fuel dispensing machines &mdash; quality guaranteed, backed by spare parts and technical support.</p>
    <div class="hero-ctas reveal is-visible" style="transition-delay:200ms">
      <a href="machinery.html" class="btn btn-primary">Explore Machinery</a>
      <a href="quote.html" class="btn btn-outline-light">Request a Quote</a>
    </div>
    <div class="hero-meta reveal is-visible" style="transition-delay:280ms">
      <div><strong>8</strong>Machine Categories</div>
      <div><strong>27+</strong>Machine Models</div>
      <div><strong>2</strong>Branch Locations</div>
      <div><strong>100%</strong>Quality Guaranteed</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <div>
        <div class="kicker reveal">WHAT WE SUPPLY</div>
        <h2 class="h2 reveal">Machinery Organised by Category</h2>
      </div>
      <a href="machinery.html" class="btn-ghost reveal">View All Machinery</a>
    </div>
    <div class="grid grid-4">
      {category_cards}
    </div>
  </div>
</section>

<section class="section bg-ink">
  <div class="container">
    <div class="grid grid-2" style="align-items:center;gap:var(--sp-6)">
      <div class="reveal">
        <div class="kicker">HOME OF INDUSTRIAL MACHINES AND SPARE PARTS</div>
        <h2 class="h2">Built for Nigeria's Manufacturing Floor</h2>
        <p class="lede mt-3">Machinery Warehouse Outlet supplies plastic machines, poly packaging machines, water packaging machines and fuel dispensing machines, together with the spare parts and accessories that keep them running.</p>
        <p class="lede mt-3" style="opacity:0.8">Pictures in our catalogue may slightly differ from the physical machine, but the quality and specifications are the same.</p>
        <div class="flex gap-3 mt-4 flex-wrap">
          <a href="about.html" class="btn btn-outline-light">About Us</a>
          <a href="spare-parts.html" class="btn btn-outline-light">Spare Parts</a>
        </div>
      </div>
      <div class="reveal" style="transition-delay:120ms">
        <img src="assets/img/brand-catalogue-cover.jpg" alt="The Machinery Warehouse Outlet catalogue" style="filter:grayscale(0.3) contrast(1.08);border:1px solid rgba(255,255,255,0.15)">
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <div>
        <div class="kicker reveal">FEATURED MACHINERY</div>
        <h2 class="h2 reveal">A Closer Look at the Range</h2>
      </div>
    </div>
    <div class="grid grid-3">
      {featured_cards}
    </div>
  </div>
</section>

<section class="section-tight bg-white">
  <div class="container">
    <div class="grid grid-3" style="border:1px solid var(--line)">
      <a href="catalogue.html" class="reveal" style="padding:var(--sp-4);border-right:1px solid var(--line)">
        <div class="kicker">FULL CATALOGUE</div>
        <h3 class="h4">View or Download Our Catalogue</h3>
        <p class="text-steel mt-2">Browse every machine in one document.</p>
      </a>
      <a href="quote.html" class="reveal" style="padding:var(--sp-4);border-right:1px solid var(--line)">
        <div class="kicker">GET PRICING</div>
        <h3 class="h4">Request a Quote</h3>
        <p class="text-steel mt-2">Tell us what you need — we'll respond with details.</p>
      </a>
      <a href="contact.html" class="reveal" style="padding:var(--sp-4)">
        <div class="kicker">SPEAK TO US</div>
        <h3 class="h4">Contact Our Team</h3>
        <p class="text-steel mt-2">Call, WhatsApp or visit a branch near you.</p>
      </a>
    </div>
  </div>
</section>
"""
write("index.html", page(
    "Home",
    "Machinery Warehouse Outlet — home of industrial machines and spare parts. Plastic machines, poly packaging machines, water packaging machines and fuel dispensing machines.",
    home_body,
    transparent_header=True,
))

# ------------------------------------------------------------ MACHINERY ----
machinery_body = """
<section class="page-head">
  <div class="container">
    <div class="breadcrumb mb-3"><a href="index.html">Home</a><span>/</span><span>Machinery</span></div>
    <div class="kicker">FULL RANGE</div>
    <h1 class="h1">Machinery Catalogue</h1>
    <p class="lede mt-3">Search or filter by category to find the right machine, then request a quote directly from its product page.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="filter-bar">
      <div class="chips" id="machinery-chips"></div>
      <div class="search-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input type="search" id="machinery-search" placeholder="Search machines…" aria-label="Search machinery">
      </div>
    </div>
    <div class="grid grid-3" id="machinery-grid"></div>
    <div class="empty-state hidden" id="machinery-empty">
      <h3 class="h3">No machines match your search</h3>
      <p class="mt-2">Try a different keyword, or browse spare parts instead.</p>
      <a href="spare-parts.html" class="btn btn-dark mt-4">View Spare Parts</a>
    </div>
  </div>
</section>
<section class="section-tight bg-ink">
  <div class="container text-center">
    <h2 class="h3">Can't find the exact machine?</h2>
    <p class="lede mt-2" style="margin:0 auto">Our full printed catalogue covers the complete range, or contact the team directly.</p>
    <div class="flex gap-3 justify-between" style="justify-content:center;margin-top:var(--sp-4)">
      <a href="catalogue.html" class="btn btn-outline-light">View Catalogue</a>
      <a href="contact.html" class="btn btn-primary">Contact Us</a>
    </div>
  </div>
</section>
"""
write("machinery.html", page(
    "Machinery Catalogue",
    "Browse film blowing machines, bag making machines, recycling lines, printing machines, moulding machines, punching machines and fuel dispensers.",
    machinery_body,
))

# ------------------------------------------------------------- PRODUCT -----
product_body = """
<section class="page-head" style="padding-bottom:var(--sp-4)">
  <div class="container">
    <div class="breadcrumb">
      <a href="index.html">Home</a><span>/</span>
      <a href="machinery.html" id="breadcrumb-cat">Machinery</a><span>/</span>
      <span id="product-title-crumb">Product</span>
    </div>
  </div>
</section>
<section class="section" style="padding-top:var(--sp-4)">
  <div class="container" id="product-root">
    <div class="grid grid-2" style="gap:var(--sp-6);align-items:flex-start">
      <div>
        <button data-lightbox-main class="card-media" style="border:1px solid var(--line);cursor:zoom-in;display:block;width:100%">
          <img id="product-image" src="" alt="" style="width:100%;aspect-ratio:4/3;object-fit:cover;filter:grayscale(0.15) contrast(1.05)">
        </button>
        <p class="text-steel mt-2" style="font-size:0.85rem">Click image to enlarge. Pictures may slightly differ from the physical machine, but quality and specifications are the same.</p>
      </div>
      <div>
        <a href="#" id="product-category" class="cat-label" style="font-family:var(--f-mono);color:var(--red);text-transform:uppercase;font-size:0.8rem;letter-spacing:0.04em"></a>
        <h1 class="h1 mt-2" id="product-title" style="font-size:clamp(1.8rem,3.5vw,2.6rem)"></h1>

        <div class="product-description-block mt-3">
          <p class="lede" id="product-description" style="max-width:none"></p>
        </div>

        <div class="product-features-block mt-4">
          <h3 class="h4 mb-3">Key Features</h3>
          <ul id="product-features" class="feature-list"></ul>
        </div>

        <div class="product-specs-block mt-4">
          <h3 class="h4 mb-3">Models &amp; Specifications</h3>
          <table class="spec-table"><tbody id="product-specs"></tbody></table>
        </div>

        <div class="flex gap-3 flex-wrap mt-5">
          <a href="#" id="product-quote-link" class="btn btn-primary">Request a Quote</a>
          <a href="#" id="product-whatsapp" data-whatsapp class="btn btn-outline">Chat on WhatsApp</a>
          <a href="contact.html" class="btn btn-outline">Contact Sales</a>
        </div>
      </div>
    </div>

    <div class="related-block section-tight">
      <h3 class="h3 mb-4">Related Machines</h3>
      <div class="grid grid-3" id="related-products"></div>
    </div>
  </div>
</section>
"""
write("product.html", page(
    "Product",
    "Machine details, model specifications and a direct path to request a quote from Machinery Warehouse Outlet.",
    product_body,
))

# --------------------------------------------------------- SPARE PARTS -----
spare_parts_body = """
<section class="page-head">
  <div class="container">
    <div class="breadcrumb mb-3"><a href="index.html">Home</a><span>/</span><span>Spare Parts</span></div>
    <div class="kicker">KEEP YOUR LINE RUNNING</div>
    <h1 class="h1">Spare Parts &amp; Accessories</h1>
    <p class="lede mt-3">Machinery Warehouse Outlet stocks spare parts and accessories for the machines we supply, including gearboxes, screw shafts, control panels and rollers.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="grid grid-4" id="spareparts-grid"></div>
  </div>
</section>
<section class="section-tight bg-ink">
  <div class="container text-center">
    <h2 class="h3">Need a specific part?</h2>
    <p class="lede mt-2" style="margin:0 auto">Tell us the machine and part you're looking for and our team will confirm availability.</p>
    <div class="flex gap-3" style="justify-content:center;margin-top:var(--sp-4)">
      <a href="quote.html" class="btn btn-primary">Request a Quote</a>
      <a href="contact.html" class="btn btn-outline-light">Contact Us</a>
    </div>
  </div>
</section>
"""
write("spare-parts.html", page(
    "Spare Parts & Accessories",
    "Spare parts and accessories for industrial machinery, including gearboxes, screw shafts, control panels and rollers.",
    spare_parts_body,
))

# --------------------------------------------------------------- ABOUT -----
about_body = """
<section class="page-head">
  <div class="container">
    <div class="breadcrumb mb-3"><a href="index.html">Home</a><span>/</span><span>About</span></div>
    <div class="kicker">ABOUT US</div>
    <h1 class="h1">Machinery Warehouse Outlet</h1>
    <p class="lede mt-3">Home of industrial machines and spare parts.</p>
  </div>
</section>
<section class="section">
  <div class="container grid grid-2" style="gap:var(--sp-6);align-items:flex-start">
    <div class="reveal">
      <h2 class="h2">What We Provide</h2>
      <p class="lede mt-3">Machinery Warehouse Outlet supplies plastic machines, poly packaging machines, water packaging machines and fuel dispensing machines, backed by spare parts and accessories to keep them running.</p>
      <p class="lede mt-3">Our range spans film blowing machines, bag making machines, recycling and pelletizing lines, printing machines, blow and injection moulding machines, and punching machines &mdash; each shown in our catalogue with the models and working widths available.</p>
      <p class="lede mt-3">Quality Guaranteed.</p>
      <div class="flex gap-3 flex-wrap mt-4">
        <a href="machinery.html" class="btn btn-dark">Explore Machinery</a>
        <a href="catalogue.html" class="btn btn-outline">View Catalogue</a>
      </div>
    </div>
    <div class="reveal" style="transition-delay:120ms">
      <img src="assets/img/hero-ibc-tower.jpg" alt="Machinery Warehouse Outlet machinery" style="filter:grayscale(1) contrast(1.1);border:1px solid var(--line)">
    </div>
  </div>
</section>
<section class="section bg-white">
  <div class="container">
    <div class="section-head">
      <div>
        <div class="kicker reveal">WHERE TO FIND US</div>
        <h2 class="h2 reveal">Head Office &amp; Branches</h2>
      </div>
    </div>
    <div class="grid grid-3">
      <div class="card reveal" style="padding:var(--sp-4)">
        <span class="cat-label">Head Office</span>
        <h3 class="h4 mt-2">Awada, Anambra State</h3>
        <p class="text-steel mt-2">Awada Industrial Zone, 2 Ichi Street, Off Ezeiweka Road, Awada-Obosi, Anambra State.</p>
      </div>
      <div class="card reveal" style="padding:var(--sp-4);--i:1">
        <span class="cat-label">Branch</span>
        <h3 class="h4 mt-2">Lagos</h3>
      </div>
      <div class="card reveal" style="padding:var(--sp-4);--i:2">
        <span class="cat-label">Branch</span>
        <h3 class="h4 mt-2">Abuja</h3>
      </div>
    </div>
  </div>
</section>
"""
write("about.html", page(
    "About Us",
    "Machinery Warehouse Outlet is home of industrial machines and spare parts, with branches in Lagos and Abuja.",
    about_body,
))

# ----------------------------------------------------------- CATALOGUE -----
catalogue_body = """
<section class="page-head">
  <div class="container">
    <div class="breadcrumb mb-3"><a href="index.html">Home</a><span>/</span><span>Catalogue</span></div>
    <div class="kicker">THE FULL RANGE, IN ONE DOCUMENT</div>
    <h1 class="h1">Product Catalogue</h1>
    <p class="lede mt-3">View our catalogue below, open it in a new tab, or download it to share with your team.</p>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="flex gap-3 flex-wrap mb-4">
      <a href="assets/machinery-warehouse-outlet-catalogue.pdf" target="_blank" rel="noopener" class="btn btn-dark">Open in New Tab</a>
      <a href="assets/machinery-warehouse-outlet-catalogue.pdf" download class="btn btn-outline">Download Catalogue (PDF)</a>
    </div>
    <div style="border:1px solid var(--line);background:var(--white);padding:var(--sp-2)">
      <embed src="assets/machinery-warehouse-outlet-catalogue.pdf" type="application/pdf" style="width:100%;height:80vh" />
      <noscript>Your browser cannot preview PDFs inline &mdash; use the links above to open or download the catalogue.</noscript>
    </div>
    <p class="text-steel mt-3" style="font-size:0.9rem">If the catalogue does not display above (common on some mobile browsers), use "Open in New Tab" instead.</p>
  </div>
</section>
<section class="section-tight bg-white">
  <div class="container">
    <div class="grid grid-3" style="border:1px solid var(--line)">
      <div style="padding:var(--sp-4);border-right:1px solid var(--line)">
        <div class="kicker">CALL US</div>
        <div class="val" data-phone-list style="font-size:1rem;font-weight:500"></div>
      </div>
      <div style="padding:var(--sp-4);border-right:1px solid var(--line)">
        <div class="kicker">EMAIL US</div>
        <div class="val" data-email-list style="font-size:1rem;font-weight:500"></div>
      </div>
      <div style="padding:var(--sp-4)">
        <div class="kicker">VISIT US</div>
        <p style="font-size:1rem;font-weight:500">Awada Industrial Zone, Anambra State &mdash; Branches: Lagos &middot; Abuja</p>
      </div>
    </div>
  </div>
</section>
"""
write("catalogue.html", page(
    "Catalogue",
    "View or download the full Machinery Warehouse Outlet product catalogue.",
    catalogue_body,
))

# ---------------------------------------------------------------- QUOTE ----
quote_body = """
<section class="page-head">
  <div class="container">
    <div class="breadcrumb mb-3"><a href="index.html">Home</a><span>/</span><span>Request a Quote</span></div>
    <div class="kicker">TELL US WHAT YOU NEED</div>
    <h1 class="h1">Request a Quote</h1>
    <p class="lede mt-3">Fill in the form and our team will get back to you with details on the machine you need.</p>
  </div>
</section>
<section class="section">
  <div class="container grid grid-2" style="gap:var(--sp-6);align-items:flex-start">
    <div>
      <div class="form-status" id="quote-status"></div>
      <div class="selected-product-chip" id="selected-product-chip">
        <span>Enquiring about: <strong id="selected-product-name"></strong></span>
        <button type="button">Remove</button>
      </div>
      <form id="quote-form" novalidate>
        <div class="form-row">
          <div class="field">
            <label for="qf-name">Full Name <span class="req">*</span></label>
            <input type="text" id="qf-name" name="name" autocomplete="name">
            <div class="error-msg">Please enter your name.</div>
          </div>
          <div class="field">
            <label for="qf-company">Company</label>
            <input type="text" id="qf-company" name="company" autocomplete="organization">
          </div>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="qf-phone">Phone Number <span class="req">*</span></label>
            <input type="tel" id="qf-phone" name="phone" autocomplete="tel">
            <div class="error-msg">Please enter a phone number we can reach you on.</div>
          </div>
          <div class="field">
            <label for="qf-email">Email Address</label>
            <input type="email" id="qf-email" name="email" autocomplete="email">
            <div class="error-msg">Please enter a valid email address.</div>
          </div>
        </div>
        <div class="form-row">
          <div class="field">
            <label for="qf-location">Country / Location</label>
            <input type="text" id="qf-location" name="location" autocomplete="country-name">
          </div>
          <div class="field">
            <label for="qf-quantity">Quantity</label>
            <input type="text" id="qf-quantity" name="quantity" placeholder="e.g. 1 unit">
          </div>
        </div>
        <div class="field">
          <label for="qf-product">Product / Machine</label>
          <select id="qf-product" name="product"></select>
        </div>
        <div class="field">
          <label for="qf-message">Message <span class="req">*</span></label>
          <textarea id="qf-message" name="message" placeholder="Tell us more about your requirements…"></textarea>
          <div class="error-msg">Please add a short message.</div>
        </div>
        <button type="submit" class="btn btn-primary btn-block">Send Enquiry</button>
        <p class="form-note">Fields marked <span class="req">*</span> are required.</p>
      </form>
    </div>
    <div>
      <div class="card" style="padding:var(--sp-4)">
        <h3 class="h4 mb-3">Prefer to talk directly?</h3>
        <div class="contact-item">
          <div style="width:100%">
            <div class="label">Call</div>
            <div class="val" data-phone-list></div>
          </div>
        </div>
        <div class="contact-item">
          <div>
            <div class="label">WhatsApp</div>
            <a class="val" href="#" data-whatsapp>Chat on WhatsApp</a>
          </div>
        </div>
        <div class="contact-item" style="border-bottom:none">
          <div style="width:100%">
            <div class="label">Email</div>
            <div class="val" data-email-list></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
"""
write("quote.html", page(
    "Request a Quote",
    "Request a quote for any machine from Machinery Warehouse Outlet.",
    quote_body,
))

# -------------------------------------------------------------- CONTACT ----
contact_body = """
<section class="page-head">
  <div class="container">
    <div class="breadcrumb mb-3"><a href="index.html">Home</a><span>/</span><span>Contact</span></div>
    <div class="kicker">HAVE A MACHINERY ENQUIRY?</div>
    <h1 class="h1">Contact Our Team</h1>
    <p class="lede mt-3">Reach us by phone, WhatsApp or email, or visit one of our locations.</p>
  </div>
</section>
<section class="section">
  <div class="container grid grid-2" style="gap:var(--sp-6);align-items:flex-start">
    <div>
      <div class="contact-item">
        <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
        <div style="width:100%">
          <div class="label">Telephone</div>
          <div class="val" data-phone-list></div>
        </div>
      </div>
      <div class="contact-item">
        <svg class="ico" viewBox="0 0 24 24" fill="currentColor"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.79.47 3.47 1.29 4.93L2 22l5.31-1.39a9.86 9.86 0 0 0 4.73 1.2h.01c5.46 0 9.9-4.45 9.9-9.91C21.96 6.45 17.5 2 12.04 2zm5.8 14.06c-.24.68-1.4 1.3-1.93 1.36-.5.06-1.03.26-3.4-.71-2.9-1.19-4.75-4.1-4.9-4.29-.14-.19-1.17-1.55-1.17-2.96 0-1.4.74-2.08 1-2.37.26-.29.57-.36.76-.36.19 0 .38 0 .55.01.18.01.42-.07.65.5.24.58.82 2 .89 2.15.07.14.12.31.02.5-.1.19-.15.31-.29.48-.15.17-.31.38-.44.5-.15.15-.3.3-.13.6.17.29.76 1.26 1.63 2.04 1.12 1 2.07 1.31 2.36 1.46.29.14.46.12.63-.07.17-.19.72-.84.92-1.13.19-.29.38-.24.64-.14.26.1 1.66.79 1.94.93.29.14.48.21.55.33.07.12.07.68-.17 1.36z"/></svg>
        <div style="width:100%">
          <div class="label">WhatsApp</div>
          <a class="val" href="#" data-whatsapp>Chat on WhatsApp</a>
        </div>
      </div>
      <div class="contact-item">
        <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 5L2 7"/></svg>
        <div style="width:100%">
          <div class="label">Email</div>
          <div class="val" data-email-list></div>
        </div>
      </div>
      <div class="contact-item" style="border-bottom:none">
        <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        <div>
          <div class="label">Head Office</div>
          <div class="val">Awada Industrial Zone, 2 Ichi Street, Off Ezeiweka Road, Awada-Obosi, Anambra State</div>
          <div class="text-steel mt-2">Branches: Lagos &middot; Abuja</div>
        </div>
      </div>

      <h3 class="h4 mt-5 mb-3">Send an Enquiry</h3>
      <div class="form-status" id="contact-status"></div>
      <form id="contact-form" novalidate>
        <div class="form-row">
          <div class="field">
            <label for="cf-name">Full Name <span class="req">*</span></label>
            <input type="text" id="cf-name" autocomplete="name">
            <div class="error-msg">Please enter your name.</div>
          </div>
          <div class="field">
            <label for="cf-email">Email Address <span class="req">*</span></label>
            <input type="email" id="cf-email" autocomplete="email">
            <div class="error-msg">Please enter a valid email address.</div>
          </div>
        </div>
        <div class="field">
          <label for="cf-message">Message <span class="req">*</span></label>
          <textarea id="cf-message" placeholder="How can we help?"></textarea>
          <div class="error-msg">Please add a short message.</div>
        </div>
        <button type="submit" class="btn btn-primary">Send Message</button>
      </form>
    </div>
    <div>
      <h3 class="h4 mb-3">Find Us</h3>
      <div style="border:1px solid var(--line);aspect-ratio:4/3">
        <iframe title="Map to Machinery Warehouse Outlet" src="https://www.google.com/maps?q=Awada+Industrial+Zone,+2+Ichi+Street,+Off+Ezeiweka+Road,+Awada-Obosi,+Anambra+State,+Nigeria&output=embed" style="width:100%;height:100%;border:0;filter:grayscale(0.4) contrast(1.05)" loading="lazy"></iframe>
      </div>
    </div>
  </div>
</section>
<script>
  document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('contact-form');
    if (form) form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = document.getElementById('cf-name');
      var email = document.getElementById('cf-email');
      var message = document.getElementById('cf-message');
      var ok = true;
      [name, message].forEach(function (el) {
        var field = el.closest('.field');
        if (!el.value.trim()) { field.classList.add('has-error'); ok = false; }
        else field.classList.remove('has-error');
      });
      var emailField = email.closest('.field');
      if (!email.value.trim() || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(email.value)) { emailField.classList.add('has-error'); ok = false; }
      else emailField.classList.remove('has-error');

      var status = document.getElementById('contact-status');
      if (!ok) {
        status.textContent = 'Please fill in the required fields before sending.';
        status.classList.add('is-visible', 'is-error');
        return;
      }
      status.classList.remove('is-error');
      status.textContent = 'Your message is ready to send. This form is not yet connected to a backend or inbox — please call, WhatsApp or email us directly in the meantime.';
      status.classList.add('is-visible');
      form.reset();
    });
  });
</script>
"""
write("contact.html", page(
    "Contact Us",
    "Contact Machinery Warehouse Outlet by phone, WhatsApp or email, or visit our head office in Awada, Anambra State.",
    contact_body,
))

# ---------------------------------------------------------------- 404 ------
error_body = """
<section class="error-page">
  <div>
    <div class="code">404</div>
    <h1 class="h2 mt-3">This page has moved or doesn't exist</h1>
    <p class="lede mt-3" style="margin:0 auto">Check the address, or head back to the machinery catalogue.</p>
    <div class="flex gap-3 mt-5" style="justify-content:center">
      <a href="index.html" class="btn btn-dark">Back to Home</a>
      <a href="machinery.html" class="btn btn-outline">View Machinery</a>
    </div>
  </div>
</section>
"""
write("404.html", page(
    "Page Not Found",
    "This page could not be found.",
    error_body,
    show_actionbar=False,
))

print("\\nAll pages generated.")
