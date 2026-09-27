# Machinery Warehouse Outlet — Website

A production-ready marketing and catalogue website for Machinery Warehouse
Outlet, built from the company's own catalogue. Every product name, model
code, working-width spec, address, phone number and email in this site is
taken directly from that catalogue — nothing has been invented. Product
photography is sourced from real photos of the physical printed catalogue
supplied directly by the client, cropped and lightly enhanced (contrast,
sharpening) but not otherwise altered.

**Revision note:** this build replaces the initial version's product
photography (originally cropped from a lower-quality PDF scan) with 23
high-resolution photos supplied directly, adds a persuasive-but-factual
description to every product page, and fixes horizontal-overflow issues
that affected some laptop widths and narrower Android phones. See section
9 below for the full list of what changed.

## 1. What this is (and isn't)

This is a **static HTML/CSS/JavaScript site** — no React, no Vite, no build
step, no `npm install`. That was a deliberate call: the environment this
was built in has no package-registry access, so a real Vite/React project
could not actually be compiled and verified here. A framework build would
have meant handing you unverified code. This does the same job — every
page is real, interactive, responsive and tested — using plain web
technology that runs anywhere, forever, with zero dependencies to install
or go stale.

If you (or a developer) later want to port this into React/Next.js, the
`js/data.js` file is already a clean, framework-agnostic data layer
(products, categories, company info) that will drop straight into any
component structure.

## 2. Project structure

```
site/
├── index.html              Home
├── machinery.html           Full catalogue, search + category filter
├── product.html              Product detail (reads ?slug=... from data.js)
├── spare-parts.html          Spare parts & accessories
├── about.html                 About / company info
├── catalogue.html             Embedded + downloadable PDF catalogue
├── quote.html                  Request-a-quote form (reads ?product=... )
├── contact.html                Contact page + enquiry form + map
├── 404.html                     Not-found page
├── css/
│   └── styles.css              Full design system (colors, type, components)
├── js/
│   ├── data.js                  ALL product/company data — edit this to add machines
│   └── main.js                   Nav, forms, filters, lightbox, 3D hero
├── assets/
│   ├── img/                       Product photography (cropped from the catalogue)
│   └── machinery-warehouse-outlet-catalogue.pdf   The original catalogue, served as-is
├── build.py / build_pages.py    The Python scripts that generated the HTML
│                                  (keeps header/footer identical across every
│                                  page — re-run `python3 build_pages.py` after
│                                  editing a page body inside build_pages.py)
└── README.md                    This file
```

## 3. Running it locally

No install needed. From inside the `site/` folder:

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080`. (Opening `index.html` directly by
double-clicking also works for browsing, but a local server is
recommended for testing the PDF embed and any future backend wiring.)

## 4. Deploying it

This is a static site — it deploys to **any** static host with zero
configuration:

- **Netlify / Vercel**: drag-and-drop the `site/` folder, or connect a
  Git repo. Add a `_redirects` file (Netlify) with `/* /404.html 404` if
  you want the 404 page to serve automatically on unmatched routes.
- **GitHub Pages**: push `site/` to a repo and enable Pages on the
  branch.
- **Any shared hosting / cPanel**: upload the contents of `site/` to
  `public_html/`.

## 5. Before you launch — things to configure

### WhatsApp number (required for the WhatsApp buttons to work)
The catalogue did not state a WhatsApp number, so `COMPANY.whatsapp` in
`js/data.js` is currently the placeholder `"WHATSAPP_NUMBER_HERE"`. Until
you replace it with a real number (international format, no `+`, e.g.
`2348012345678`), every "Chat on WhatsApp" button on the site will be
visibly disabled rather than broken.

```js
// js/data.js
const COMPANY = {
  ...
  whatsapp: "2348012345678", // <-- put the real number here
};
```

### Quote form & contact form — not yet connected to a backend
Both forms validate correctly and show a "ready to send" confirmation,
but **nothing is actually transmitted anywhere yet** — there is no server
to send it to. The integration point is clearly marked in
`js/main.js` inside `initQuoteForm()`:

```js
// Integration point: replace this block with a real submission
// (e.g. fetch('/api/quote', { method: 'POST', body: new FormData(form) }))
```

The simplest options: point it at a form backend (Formspree, Netlify
Forms, Getform), or stand up a small serverless function that emails
`machines.warehouse@juninet.com`. The contact page's inline form (bottom
of `contact.html`) has an equivalent stub.

### Social media links
`COMPANY.socials` in `js/data.js` is empty — the catalogue did not list
any social media handles. Add them there if you have them; the footer
doesn't currently render social icons since none were supplied, but the
data slot is ready.

## 6. Adding or editing machines

Everything product-related lives in **`js/data.js`** — nothing is
hardcoded into the HTML. To add a machine:

```js
// in PRODUCTS array
{
  slug: "your-machine-slug",              // used in the URL
  name: "Full Machine Name",
  category: "film-blowing",                // must match a CATEGORIES slug
  image: "prod-your-image",                 // filename in assets/img/ (no .jpg)
  gallery: ["prod-your-image"],
  features: ["Feature one", "Feature two"],
  models: [{ code: "MW-100", spec: "500-800mm" }],
}
```

It will automatically appear in the machinery grid, its category page,
search results, the quote-form product dropdown, and get a working
product detail page at `product.html?slug=your-machine-slug` — no other
file needs to change.

To add a new **category**, add an entry to the `CATEGORIES` array the
same way; it will appear in the homepage grid, filter chips, and footer
automatically.

## 7. Images

Product photography is sourced from real photos of the physical printed
catalogue, auto-trimmed, contrast-corrected and sharpened, then treated
with a grayscale/duotone filter (in CSS, not baked into the files) for a
consistent, premium look across photos of varying original lighting. A
few source photos covered more than one machine on the same page (e.g.
"double stage" and "single stage" recycling machines on one photo) and
were split into separate files during processing. If higher-resolution
or studio photography becomes available for any machine, just replace
the matching file in `assets/img/` (same filename) — no code changes
needed. The full-resolution PDF catalogue is still served as-is at
`assets/machinery-warehouse-outlet-catalogue.pdf` for the Catalogue page.

## 8. The 3D hero

The homepage hero includes a small Three.js scene (an abstract die-head /
extrusion-arm assembly, not a literal machine model) that responds to
mouse movement. It:
- Loads Three.js from a CDN (`cdnjs.cloudflare.com`) — requires an
  internet connection to render; falls back automatically to a static
  photo background if the library fails to load, WebGL isn't available,
  or the visitor has "reduce motion" turned on.
- Uses a lighter setup on small/mobile screens automatically.

## 9. Known environment limitations (from where this was built)

- This was built and tested in a sandboxed environment with no outbound
  network access, so Google Fonts, Three.js (CDN), and the embedded
  Google Map on the contact page could not be *rendered* during testing
  here — only verified structurally. They are standard, valid
  integrations and will work normally on any real server with internet
  access reaching the visitor's browser (which is what actually matters
  — these all load in the *visitor's* browser, not the server).
- The PDF catalogue viewer (`catalogue.html`) uses a plain `<embed>` tag,
  which every mainstream desktop browser renders natively. Some mobile
  browsers don't support inline PDF embeds — that's why "Open in New
  Tab" and "Download" buttons sit right above it as the reliable fallback.

## 9. What changed in this revision

- **Photography**: every product now uses a real, correctly-matched photo
  from the client-supplied catalogue photos instead of the earlier PDF-scan
  crops (several of which had mistakenly shown title text instead of the
  machine, or the wrong machine entirely).
- **Descriptions**: every product detail page now has a short, benefit-focused
  description above the spec table — written to explain what the listed
  features mean for a buyer, without adding any spec, number or claim beyond
  what the catalogue itself states.
- **All phone numbers & both emails, everywhere it matters**: the footer
  (every page), the Catalogue page, the Contact page, and the Request-a-Quote
  sidebar now list all four phone numbers and both email addresses, each as
  its own tappable link — previously some of these spots only showed the
  first number/email.
- **Layout overflow fixed**: the site previously could scroll horizontally
  on some laptop widths (roughly 960–1200px, where the nav links and the
  "Request a Quote" button could overlap) and on some narrower Android
  phones (long email addresses forcing extra width). Both are fixed: the nav
  now switches to the mobile menu earlier (below 1280px) so it never runs
  out of room, and long text (emails especially) now wraps at sensible
  points instead of forcing the page wider than the screen. Verified with
  no horizontal overflow from 320px up to 1920px wide, across every page.
- **Spare Parts page** now shows all six part categories (two more than
  before) since two additional clean part photos came out of the new source
  images.

## 10. Accessibility & performance notes

- Semantic HTML throughout (`<nav>`, `<header>`, `<footer>`, proper
  heading order), visible focus states, alt text on every image,
  `prefers-reduced-motion` respected site-wide.
- Images are lazy-loaded below the fold.
- No build step means no bundle size to worry about — the heaviest asset
  is the catalogue PDF itself, loaded only on the catalogue page.
