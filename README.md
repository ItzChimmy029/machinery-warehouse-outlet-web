# Machinery Warehouse Outlet website

A static website (plain HTML, CSS and JavaScript, no framework and no backend)
for Machinery Warehouse Outlet. Pages are generated from small Python
templates, so the header and footer stay identical everywhere.

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Home |
| `machinery.html` | All machines with search and category filter |
| `product.html?slug=...` | One machine: photo, description, models, enquiry buttons |
| `spare-parts.html` | Spare parts |
| `about.html` | About and head office |
| `quote.html` | Quotation form (sends to WhatsApp) |
| `contact.html` | Contact details, general enquiry form, map |
| `404.html` | Not found page |

## Where to change things

Everything customers see about the business lives in **`js/data.js`**:

- `COMPANY.whatsapp`: the WhatsApp number in international format (`2349022330011`). Every WhatsApp button, form and floating button reads this one value.
- `COMPANY.whatsappDisplay`: how that number is written on screen.
- `COMPANY.phones`: the official call numbers.
- `CATEGORIES` and `PRODUCTS`: the machines. Add or remove an entry and it appears (or disappears) in the grid, search, filters, product pages, related machines and the quote form dropdown. The homepage machine count updates itself on the next build.

After editing any template (`build.py`, `build_pages.py`) or `js/data.js`, rebuild:

```bash
python3 build_pages.py
```

## Map and GPS location

The contact page has an embedded Google map, GPS coordinates as text, and
direction buttons for Google Maps, Apple Maps and Waze. The About page and the
footer link to the same spot, and a "Show my distance from the office" button
uses the visitor's own phone location (only on their device, never sent
anywhere). All of it comes from one setting, `COMPANY.location` in
`js/data.js`.

**Status: the pin is approximate until you confirm it.** No public map listing
exists for the business, so the coordinates currently point to a verified spot
on Ezeiweka Road in Awada, not the exact door of No. 2 Ichi Street. While
`verified` is `false` the contact page tells visitors the pin marks the road
area. To make it exact:

1. Stand at the shop and open Google Maps on your phone.
2. Press and hold on the exact spot to drop a pin.
3. Tap the coordinates shown at the top of the screen to copy them.
4. Paste them into `lat` and `lng` in `js/data.js`, set `verified: true`, then run `python3 build_pages.py` and push.

## How WhatsApp enquiries work

There is no server. Every enquiry opens WhatsApp with a ready-written message
addressed to the number in `COMPANY.whatsapp`; nothing is sent until the
customer presses send in WhatsApp.

- Machine pages: **Enquire on WhatsApp** and **Check Availability** each build a different message containing the machine name, category and model codes.
- Quote form: every field the customer fills in is included, in a structured message with *Customer information*, *Machine information* and *Request details* sections. A preview of the exact message is shown on the page.
- Contact form, spare parts, machinery page, floating button: each has its own appropriate message.
- Messages are URL encoded, and the destination number can never be changed by anything typed into a form or placed in the page address.

## Run locally

```bash
python3 -m http.server 8000
```

Then open `localhost:8000` in a browser.

## Verify everything

```bash
python3 tests/static_checks.py          # no dependencies
pip install playwright && playwright install chromium
python3 tests/browser_tests.py          # behaviour, security probes, responsive sweep
```

## Deploy to GitHub Pages

Repository **Settings > Pages > Deploy from a branch > `main` / root**.
`_config.yml` keeps the build scripts, tests and docs out of the published site.

## Security

See `SECURITY.md` for the hosting limitations (GitHub Pages cannot set HTTP
security headers) and what has been done about them.
