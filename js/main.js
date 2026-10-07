/* ==========================================================================
   Machinery Warehouse Outlet — Site Behaviour
   ========================================================================== */

(function () {
  "use strict";

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));

  /* ---------------- Header / nav ---------------- */
  function initHeader() {
    const header = $(".site-header");
    if (!header) return;
    const isHome = document.body.dataset.transparentHeader === "true";
    const toggle = $(".nav-toggle");
    const mobileMenu = $(".mobile-menu");

    function onScroll() {
      if (window.scrollY > 8) header.classList.add("is-scrolled");
      else if (!isHome) header.classList.add("is-scrolled");
      else header.classList.remove("is-scrolled");
    }
    if (!isHome) header.classList.add("is-solid");
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });

    if (toggle && mobileMenu) {
      toggle.addEventListener("click", () => {
        const open = mobileMenu.classList.toggle("is-open");
        header.classList.toggle("is-open", open);
        document.body.classList.toggle("menu-open", open);
        toggle.setAttribute("aria-expanded", String(open));
      });
      $$(".mobile-menu a").forEach((a) =>
        a.addEventListener("click", () => {
          mobileMenu.classList.remove("is-open");
          header.classList.remove("is-open");
          document.body.classList.remove("menu-open");
        })
      );
    }

    // mark active nav link
    const path = location.pathname.split("/").pop() || "index.html";
    $$(".nav-links a, .mobile-menu a").forEach((a) => {
      const href = a.getAttribute("href");
      if (href === path || (path === "" && href === "index.html")) a.classList.add("active");
    });
  }

  /* ---------------- Scroll reveal ---------------- */
  function initReveal() {
    const items = $$(".reveal");
    if (!items.length) return;
    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
      items.forEach((el) => el.classList.add("is-visible"));
      return;
    }
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );
    items.forEach((el, i) => {
      el.style.setProperty("--i", el.dataset.i || (i % 6));
      io.observe(el);
    });
  }

  /* ---------------- Footer year ---------------- */
  function initFooterYear() {
    $$(".js-year").forEach((el) => (el.textContent = new Date().getFullYear()));
  }

  /* ---------------- Contact / WhatsApp helpers ----------------
     Single source of truth for the WhatsApp destination: COMPANY.whatsapp
     (in js/data.js). Nothing else in this file — or anywhere on the site —
     hardcodes a phone number or builds a wa.me link independently, so a
     future number change only ever happens in one place. */
  function digitsOnly(str) {
    return (str || "").replace(/[^\d+]/g, "");
  }

  function escapeHtml(str) {
    return String(str ?? "").replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }

  // Responsive photo: lighter file for ordinary screens, full-size file for
  // large or high-density screens, so images stay sharp without every grid
  // downloading the big version.
  function imgTag(name, alt, sizes) {
    const n = encodeURIComponent(name);
    return `<img src="assets/img/${n}-sm.jpg" srcset="assets/img/${n}-sm.jpg 800w, assets/img/${n}.jpg 1600w" sizes="${sizes}" alt="${escapeHtml(alt)}" loading="lazy" decoding="async">`;
  }

  // Some phones cannot hand very long links over to WhatsApp. Normal enquiries
  // are around 1,800 characters once encoded; this limit only trips for
  // extreme input (for example a maxed-out message full of emoji). We ask the
  // visitor to shorten it rather than silently cutting any of their text.
  const MAX_WA_URL_LENGTH = 6000;
  const TOO_LONG_MESSAGE = "That message is too long to send through WhatsApp. Please shorten it a little and try again.";

  // The WhatsApp number is fixed application configuration (COMPANY.whatsapp).
  // No code path ever lets page/query-string/form input choose the
  // destination number — callers can only supply the message text.
  function buildWhatsAppLink(message) {
    const number = COMPANY.whatsapp;
    const isPlaceholder = !number || /_HERE$/.test(number);
    if (isPlaceholder) return null;
    const digits = digitsOnly(number).replace(/^\+/, "");
    const text = encodeURIComponent(message || `Hello ${COMPANY.name}, I would like more information.`);
    return `https://wa.me/${digits}?text=${text}`;
  }

  /* Contextual message builders. Each returns plain text; buildWhatsAppLink
     handles encodeURIComponent, so callers never need to encode themselves. */
  function waLineForProduct(product) {
    const cat = getCategoryBySlug(product.category);
    const lines = [`Machine: ${product.name}`];
    if (cat) lines.push(`Category: ${cat.name}`);
    if (product.models && product.models.length) {
      const codes = product.models.map((m) => m.code + (m.spec ? ` (${m.spec})` : "")).join(", ");
      lines.push(`Model(s): ${codes}`);
    }
    return lines.join("\n");
  }

  function waMessageForProduct(product, intent) {
    const info = waLineForProduct(product);
    switch (intent) {
      case "quote":
        return `Hello ${COMPANY.name}, I would like a quote for the following machine.\n\n${info}\n\nPlease send me pricing, availability and delivery information.\n\nThank you.`;
      case "availability":
        return `Hello ${COMPANY.name}, I would like to check availability for the following machine.\n\n${info}\n\nIs this currently in stock, and what is the lead time if not?\n\nThank you.`;
      case "specs":
        return `Hello ${COMPANY.name}, could you share more technical detail on this machine?\n\n${info}\n\nI am specifically interested in the full specifications and features.\n\nThank you.`;
      case "enquire":
      default:
        return `Hello ${COMPANY.name}, I am interested in the following machine.\n\n${info}\n\nPlease send me more information, current pricing and availability.\n\nThank you.`;
    }
  }

  function waMessageGeneral(intent) {
    switch (intent) {
      case "quote":
        return `Hello ${COMPANY.name}, I would like to request a quote. Could you help me with pricing and availability for a machine I'm interested in?`;
      case "spareparts":
        return `Hello ${COMPANY.name}, I'm looking for a spare part for one of your machines. Could you help me check availability?`;
      case "consult":
        return `Hello ${COMPANY.name}, I'd like to speak with someone about which machine would suit my production needs. Could we set up a time to talk?`;
      case "general":
      default:
        return `Hello ${COMPANY.name}, I have a question about your machines and would like some assistance.`;
    }
  }

  // Shows "Opening WhatsApp..." plus a manual fallback link, built with DOM
  // APIs (no innerHTML), so no message content can ever be parsed as markup.
  function showWhatsAppOpening(statusEl, link, what) {
    statusEl.textContent = "";
    statusEl.append(`Opening WhatsApp with your ${what} now. If it doesn't open automatically, `);
    const a = document.createElement("a");
    a.href = link;
    a.target = "_blank";
    a.rel = "noopener";
    a.textContent = "tap here to open WhatsApp";
    statusEl.append(a, ".");
    statusEl.classList.add("is-visible");
  }

  function initContactLinks() {
    $$("[data-tel]").forEach((el) => {
      const n = COMPANY.phones[0];
      el.href = `tel:${digitsOnly(n)}`;
      if (el.dataset.fill === "text") el.textContent = n;
    });
    $$("[data-email]").forEach((el) => {
      const e = COMPANY.emails[0];
      el.href = `mailto:${e}`;
      if (el.dataset.fill === "text") el.textContent = e;
    });
    // Full lists — every phone number / email, each as its own link.
    $$("[data-phone-list]").forEach((el) => {
      el.innerHTML = COMPANY.phones
        .map((p) => `<a href="tel:${digitsOnly(p)}">${escapeHtml(p)}</a>`)
        .join('<span class="sep" aria-hidden="true"></span>');
    });
    $$("[data-email-list]").forEach((el) => {
      el.innerHTML = COMPANY.emails
        .map((e) => `<a href="mailto:${escapeHtml(e)}">${escapeHtml(e).replace("@", "@<wbr>")}</a>`)
        .join('<span class="sep" aria-hidden="true"></span>');
    });
    $$("[data-whatsapp-label]").forEach((el) => {
      el.textContent = `WhatsApp: ${COMPANY.whatsappDisplay}`;
    });
    // Generic WhatsApp wiring for static links: data-whatsapp-product is a
    // product SLUG (looked up in our own data, never raw text) and
    // data-whatsapp-intent picks the message template. Both are optional.
    $$("[data-whatsapp]").forEach((el) => {
      const slug = el.dataset.whatsappProduct;
      const intent = el.dataset.whatsappIntent || "enquire";
      const product = slug ? getProductBySlug(slug) : null;
      const msg = product ? waMessageForProduct(product, intent) : waMessageGeneral(intent);
      const link = buildWhatsAppLink(msg);
      if (link) {
        el.href = link;
        el.target = "_blank";
        el.rel = "noopener";
        el.classList.remove("hidden");
      } else {
        el.href = "#";
        el.setAttribute("aria-disabled", "true");
        el.title = "WhatsApp number not yet configured";
        el.addEventListener("click", (e) => e.preventDefault());
      }
    });
  }

  function initMobileActionBar() {
    const bar = $(".mobile-actionbar");
    if (!bar) return;
    document.body.classList.add("has-actionbar");
  }

  /* ---------------- Lightbox ---------------- */
  function initLightbox() {
    const lb = $(".lightbox");
    if (!lb) return;
    const img = $("img", lb);
    $$("[data-lightbox]").forEach((trigger) => {
      trigger.addEventListener("click", (e) => {
        e.preventDefault();
        img.src = trigger.dataset.lightbox;
        img.alt = trigger.dataset.lightboxAlt || "";
        lb.classList.add("is-open");
      });
    });
    lb.addEventListener("click", () => lb.classList.remove("is-open"));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") lb.classList.remove("is-open");
    });
  }

  /* ---------------- Machinery listing: search + filter ---------------- */
  function initMachineryFilters() {
    const list = $("#machinery-grid");
    if (!list) return;
    const searchInput = $("#machinery-search");
    const chipWrap = $("#machinery-chips");
    const emptyState = $("#machinery-empty");
    const params = new URLSearchParams(location.search);
    let activeCategory = params.get("category") || "all";

    function cardHtml(p) {
      const cat = getCategoryBySlug(p.category);
      const slug = encodeURIComponent(p.slug);
      const modelsLine = p.models && p.models.length
        ? p.models.map((m) => escapeHtml(m.code)).join(" · ")
        : "";
      return `
      <div class="card reveal" data-category="${escapeHtml(p.category)}" data-name="${escapeHtml(p.name.toLowerCase())}">
        <a href="product.html?slug=${slug}" class="card-media">
          ${imgTag(p.image, p.name, "(max-width: 560px) 100vw, (max-width: 960px) 50vw, 400px")}
          <span class="tag">${cat ? escapeHtml(cat.short) : ""}</span>
        </a>
        <div class="card-body">
          <span class="cat-label">${cat ? escapeHtml(cat.name) : ""}</span>
          <h3><a href="product.html?slug=${slug}">${escapeHtml(p.name)}</a></h3>
          ${modelsLine ? `<div class="models">${modelsLine}</div>` : ""}
        </div>
        <div class="card-foot">
          <a href="product.html?slug=${slug}">View Details</a>
          <a href="quote.html?product=${slug}" class="foot-quote">Request Quote</a>
        </div>
      </div>`;
    }

    function render() {
      const q = (searchInput?.value || "").trim().toLowerCase();
      const filtered = PRODUCTS.filter((p) => {
        const matchesCat = activeCategory === "all" || p.category === activeCategory;
        const matchesQ = !q || p.name.toLowerCase().includes(q);
        return matchesCat && matchesQ;
      });
      list.innerHTML = filtered.map(cardHtml).join("");
      emptyState.classList.toggle("hidden", filtered.length > 0);
      requestAnimationFrame(() => {
        $$(".reveal", list).forEach((el) => el.classList.add("is-visible"));
      });
    }

    if (chipWrap) {
      chipWrap.innerHTML =
        `<button class="chip" data-cat="all">All Machinery</button>` +
        CATEGORIES.map((c) => `<button class="chip" data-cat="${escapeHtml(c.slug)}">${escapeHtml(c.short)}</button>`).join("");
      $$(".chip", chipWrap).forEach((chip) => {
        if (chip.dataset.cat === activeCategory) chip.classList.add("is-active");
        chip.addEventListener("click", () => {
          activeCategory = chip.dataset.cat;
          $$(".chip", chipWrap).forEach((c) => c.classList.remove("is-active"));
          chip.classList.add("is-active");
          const url = new URL(location.href);
          if (activeCategory === "all") url.searchParams.delete("category");
          else url.searchParams.set("category", activeCategory);
          history.replaceState({}, "", url);
          render();
        });
      });
    }
    if (searchInput) searchInput.addEventListener("input", render);
    render();
  }

  /* ---------------- Spare parts grid ---------------- */
  function initSparePartsGrid() {
    const grid = $("#spareparts-grid");
    if (!grid || typeof SPARE_PARTS_GROUPS === "undefined") return;
    grid.innerHTML = SPARE_PARTS_GROUPS.map(
      (g, i) => `
      <div class="card reveal" style="--i:${i % 4}">
        <div class="card-media">${imgTag(g.image, g.name, "(max-width: 560px) 100vw, (max-width: 960px) 50vw, 300px")}</div>
        <div class="card-body"><h4>${escapeHtml(g.name)}</h4></div>
      </div>`
    ).join("");
  }

  /* ---------------- Product detail page ---------------- */
  function initProductPage() {
    const root = $("#product-root");
    if (!root) return;
    const params = new URLSearchParams(location.search);
    const product = getProductBySlug(params.get("slug"));

    if (!product) {
      root.innerHTML = `<div class="empty-state"><h3 class="h3">Machine not found</h3><p class="mt-2">This machine may have moved. Browse all machinery instead.</p><a href="machinery.html" class="btn btn-dark mt-4">View All Machinery</a></div>`;
      return;
    }

    const cat = getCategoryBySlug(product.category);
    document.title = `${product.name} | ${COMPANY.name}`;
    const metaDesc = $('meta[name="description"]');
    if (metaDesc) metaDesc.setAttribute("content", `${product.name} from ${COMPANY.name}. ${cat.name}. Request specifications and a quote.`);

    $("#breadcrumb-cat").textContent = cat.name;
    $("#breadcrumb-cat").href = `machinery.html?category=${cat.slug}`;
    $("#product-title").textContent = product.name;
    $("#product-category").textContent = cat.name;
    $("#product-category").href = `machinery.html?category=${cat.slug}`;
    $("#product-image").src = `assets/img/${product.image}.jpg`;
    $("#product-image").alt = product.name;
    $("[data-lightbox-main]").dataset.lightbox = `assets/img/${product.image}.jpg`;
    $("[data-lightbox-main]").dataset.lightboxAlt = product.name;

    const descWrap = $("#product-description");
    if (descWrap) {
      if (product.description) {
        descWrap.textContent = product.description;
      } else {
        descWrap.closest(".product-description-block")?.classList.add("hidden");
      }
    }

    const featWrap = $("#product-features");
    if (product.features && product.features.length) {
      featWrap.innerHTML = product.features.map((f) => `<li>${escapeHtml(f)}</li>`).join("");
    } else {
      featWrap.closest(".product-features-block")?.classList.add("hidden");
    }

    const specWrap = $("#product-specs");
    if (product.models && product.models.length) {
      specWrap.innerHTML = product.models
        .map((m) => `<tr><td>Model</td><td>${escapeHtml(m.code)}${m.spec ? ` (${escapeHtml(m.spec)})` : ""}</td></tr>`)
        .join("");
    } else {
      specWrap.closest(".product-specs-block")?.classList.add("hidden");
    }

    $("#product-quote-link").href = `quote.html?product=${encodeURIComponent(product.slug)}`;
    const waBtn = $("#product-whatsapp");
    if (waBtn) {
      waBtn.dataset.whatsappProduct = product.slug;
      waBtn.dataset.whatsappIntent = "enquire";
    }
    const waAvailBtn = $("#product-whatsapp-availability");
    if (waAvailBtn) {
      waAvailBtn.dataset.whatsappProduct = product.slug;
      waAvailBtn.dataset.whatsappIntent = "availability";
    }

    // related products
    const related = getProductsByCategory(product.category).filter((p) => p.slug !== product.slug).slice(0, 3);
    const relatedWrap = $("#related-products");
    if (relatedWrap) {
      if (!related.length) {
        relatedWrap.closest(".related-block")?.classList.add("hidden");
      } else {
        relatedWrap.innerHTML = related
          .map(
            (p) => `
          <div class="card reveal is-visible">
            <a href="product.html?slug=${encodeURIComponent(p.slug)}" class="card-media">
              ${imgTag(p.image, p.name, "(max-width: 560px) 100vw, (max-width: 960px) 50vw, 400px")}
            </a>
            <div class="card-body">
              <h4><a href="product.html?slug=${encodeURIComponent(p.slug)}">${escapeHtml(p.name)}</a></h4>
            </div>
          </div>`
          )
          .join("");
      }
    }
    initContactLinks();
  }

  /* ---------------- Quote form ----------------
     No backend exists (this is a static site), so the form's job is to
     collect a clean, complete enquiry and hand it to WhatsApp — the
     destination number always comes from COMPANY.whatsapp (see the
     WhatsApp helpers above), never from anything on this page. Every
     field the visitor fills in is included in the message; nothing is
     silently dropped. */
  function initQuoteForm() {
    const form = $("#quote-form");
    if (!form) return;
    const params = new URLSearchParams(location.search);
    const preselect = params.get("product");
    const productSelect = $("#qf-product");

    if (productSelect) {
      productSelect.innerHTML =
        `<option value="">Select a machine (optional)</option>` +
        PRODUCTS.map((p) => `<option value="${encodeURIComponent(p.slug)}">${escapeHtml(p.name)}</option>`).join("");
      if (preselect && getProductBySlug(preselect)) {
        productSelect.value = preselect;
        const chip = $("#selected-product-chip");
        if (chip) {
          chip.classList.add("is-visible");
          $("#selected-product-name", chip).textContent = getProductBySlug(preselect).name;
          $("button", chip).addEventListener("click", () => {
            productSelect.value = "";
            chip.classList.remove("is-visible");
          });
        }
      }
    }

    const requiredFields = ["qf-name", "qf-phone", "qf-message"];
    // A permissive but real check: at least 7 digits, and only characters
    // that legitimately appear in phone numbers. Client-side only — this
    // is a UX convenience, not a security boundary (there is no server
    // this could protect; the only destination is a wa.me link the
    // visitor's own browser opens).
    const PHONE_RE = /^[\d+()\-.\s]{7,20}$/;
    const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    function setError(id, isError) {
      $("#" + id).closest(".field").classList.toggle("has-error", isError);
    }

    function validate() {
      let ok = true;
      requiredFields.forEach((id) => {
        const el = $("#" + id);
        if (!el.value.trim()) { setError(id, true); ok = false; }
        else setError(id, false);
      });
      const phoneEl = $("#qf-phone");
      if (phoneEl.value.trim() && !PHONE_RE.test(phoneEl.value.trim())) {
        setError("qf-phone", true); ok = false;
      }
      const emailEl = $("#qf-email");
      if (emailEl.value.trim() && !EMAIL_RE.test(emailEl.value.trim())) {
        setError("qf-email", true); ok = false;
      } else {
        setError("qf-email", false);
      }
      return ok;
    }

    // Build the full structured message from every field the visitor filled
    // in. Nothing entered is dropped; anything left blank is simply omitted
    // from its section rather than sent as an empty line.
    function buildQuoteMessage() {
      const val = (id) => $("#" + id).value.trim();
      const name = val("qf-name");
      const company = val("qf-company");
      const phone = val("qf-phone");
      const email = val("qf-email");
      const location_ = val("qf-location");
      const quantity = val("qf-quantity");
      const message = val("qf-message");
      const slug = productSelect ? productSelect.value : "";
      const product = slug ? getProductBySlug(slug) : null;

      const customerLines = [`Name: ${name}`];
      if (company) customerLines.push(`Company: ${company}`);
      customerLines.push(`Phone: ${phone}`);
      if (email) customerLines.push(`Email: ${email}`);
      if (location_) customerLines.push(`Location: ${location_}`);

      const machineLines = [];
      if (product) {
        machineLines.push(`Machine: ${product.name}`);
        const cat = getCategoryBySlug(product.category);
        if (cat) machineLines.push(`Category: ${cat.name}`);
        if (product.models && product.models.length) {
          machineLines.push(`Model(s): ${product.models.map((m) => m.code + (m.spec ? ` (${m.spec})` : "")).join(", ")}`);
        }
      }
      if (quantity) machineLines.push(`Quantity: ${quantity}`);

      const parts = [
        `Hello ${COMPANY.name},`,
        "",
        "A new quotation request has been submitted through the website.",
        "",
        "CUSTOMER INFORMATION",
        customerLines.join("\n"),
      ];
      if (machineLines.length) {
        parts.push("", "MACHINE INFORMATION", machineLines.join("\n"));
      }
      parts.push("", "REQUEST DETAILS", message);
      parts.push("", "Please provide the quotation, current availability, delivery information and any other relevant details.", "", "Thank you.");
      return parts.join("\n");
    }

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const status = $("#quote-status");
      if (!validate()) {
        status.textContent = "Please fill in the required fields correctly before sending.";
        status.classList.add("is-visible", "is-error");
        status.scrollIntoView({ behavior: "smooth", block: "center" });
        return;
      }
      const messageText = buildQuoteMessage();
      const link = buildWhatsAppLink(messageText);
      status.classList.remove("is-error");

      if (!link) {
        status.textContent = "WhatsApp isn't configured yet. Please call or email us directly using the details on this page.";
        status.classList.add("is-visible");
        return;
      }

      if (link.length > MAX_WA_URL_LENGTH) {
        status.textContent = TOO_LONG_MESSAGE;
        status.classList.add("is-visible", "is-error");
        status.scrollIntoView({ behavior: "smooth", block: "center" });
        return;
      }

      // Let the visitor see exactly what will be sent before/while WhatsApp opens.
      const previewEl = $("#quote-message-preview");
      if (previewEl) {
        previewEl.textContent = messageText;
        previewEl.closest(".wa-preview")?.classList.remove("hidden");
      }
      showWhatsAppOpening(status, link, "request");
      window.open(link, "_blank", "noopener");
    });
  }

  /* ---------------- Contact page general enquiry form ---------------- */
  function initContactForm() {
    const form = $("#contact-form");
    if (!form) return;
    const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    function validate() {
      let ok = true;
      const name = $("#cf-name"), email = $("#cf-email"), message = $("#cf-message");
      [name, message].forEach((el) => {
        const field = el.closest(".field");
        if (!el.value.trim()) { field.classList.add("has-error"); ok = false; }
        else field.classList.remove("has-error");
      });
      const emailField = email.closest(".field");
      if (!email.value.trim() || !EMAIL_RE.test(email.value.trim())) {
        emailField.classList.add("has-error"); ok = false;
      } else {
        emailField.classList.remove("has-error");
      }
      return ok;
    }

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const status = $("#contact-status");
      if (!validate()) {
        status.textContent = "Please fill in the required fields correctly before sending.";
        status.classList.remove("is-error");
        status.classList.add("is-visible", "is-error");
        return;
      }
      const name = $("#cf-name").value.trim();
      const email = $("#cf-email").value.trim();
      const message = $("#cf-message").value.trim();
      const text = `Hello ${COMPANY.name},\n\nMy name is ${name} (${email}).\n\n${message}\n\nThank you.`;
      const link = buildWhatsAppLink(text);
      status.classList.remove("is-error");
      if (!link) {
        status.textContent = "WhatsApp isn't configured yet. Please call or email us directly using the details above.";
        status.classList.add("is-visible");
        return;
      }
      if (link.length > MAX_WA_URL_LENGTH) {
        status.textContent = TOO_LONG_MESSAGE;
        status.classList.add("is-visible", "is-error");
        return;
      }
      showWhatsAppOpening(status, link, "message");
      window.open(link, "_blank", "noopener");
    });
  }

  /* ---------------- Floating WhatsApp + Back-to-top ---------------- */
  function initFloatingButtons() {
    const waBtn = $(".float-whatsapp");
    const topBtn = $(".float-totop");
    if (waBtn) {
      waBtn.dataset.whatsappIntent = "general";
      // initContactLinks() (already run) wires the href; this button just
      // needs to exist in the DOM before that pass.
    }
    if (!topBtn) return;

    function onScroll() {
      const show = window.scrollY > 480;
      topBtn.classList.toggle("is-visible", show);
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    topBtn.addEventListener("click", () => {
      window.scrollTo({ top: 0, behavior: prefersReducedMotion ? "auto" : "smooth" });
    });
  }

  /* ---------------- Hero 3D (Three.js) ---------------- */
  function initHero3D() {
    const canvas = $("#hero-canvas");
    const fallback = $(".hero-photo-fallback");
    if (!canvas) return;
    if (prefersReducedMotion || typeof THREE === "undefined") {
      canvas.classList.add("hidden");
      fallback?.classList.remove("hidden");
      return;
    }

    let renderer;
    try {
      renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    } catch (err) {
      canvas.classList.add("hidden");
      fallback?.classList.remove("hidden");
      return;
    }

    const isSmall = window.innerWidth < 760;
    const dpr = Math.min(window.devicePixelRatio || 1, isSmall ? 1.3 : 2);
    renderer.setPixelRatio(dpr);
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
    camera.position.set(0, 0.4, 9);

    const rig = new THREE.Group();
    scene.add(rig);

    const steelMat = new THREE.MeshStandardMaterial({ color: 0x6b7580, metalness: 0.85, roughness: 0.32 });
    const darkMat = new THREE.MeshStandardMaterial({ color: 0x1c2126, metalness: 0.6, roughness: 0.45 });
    const redMat = new THREE.MeshStandardMaterial({ color: 0xc81e22, metalness: 0.4, roughness: 0.4 });

    // Central die-head hub
    const hub = new THREE.Mesh(new THREE.CylinderGeometry(1.15, 1.3, 0.6, 48), steelMat);
    hub.rotation.x = Math.PI / 2;
    rig.add(hub);

    const hubRing = new THREE.Mesh(new THREE.TorusGeometry(1.28, 0.07, 16, 64), redMat);
    rig.add(hubRing);

    const core = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 2.4, 32), darkMat);
    core.rotation.x = Math.PI / 2;
    rig.add(core);

    // radiating spokes / extrusion arms
    const armGroup = new THREE.Group();
    const armCount = 8;
    for (let i = 0; i < armCount; i++) {
      const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 1.7, 12), steelMat);
      const angle = (i / armCount) * Math.PI * 2;
      arm.position.set(Math.cos(angle) * 1.65, Math.sin(angle) * 1.65, 0);
      arm.rotation.z = angle + Math.PI / 2;
      armGroup.add(arm);

      const bolt = new THREE.Mesh(new THREE.SphereGeometry(0.09, 12, 12), darkMat);
      bolt.position.set(Math.cos(angle) * 2.4, Math.sin(angle) * 2.4, 0);
      armGroup.add(bolt);
    }
    rig.add(armGroup);

    // outer guide rings (depth)
    for (let i = 0; i < 3; i++) {
      const ring = new THREE.Mesh(new THREE.TorusGeometry(2.7 + i * 0.55, 0.02, 8, 80), steelMat);
      ring.position.z = -0.6 - i * 0.5;
      ring.material = steelMat.clone();
      ring.material.opacity = 0.5 - i * 0.12;
      ring.material.transparent = true;
      rig.add(ring);
    }

    rig.rotation.set(0.15, -0.4, 0);

    const key = new THREE.DirectionalLight(0xffffff, 2.1);
    key.position.set(4, 5, 6);
    scene.add(key);
    const fill = new THREE.DirectionalLight(0xff8a8c, 0.7);
    fill.position.set(-5, -2, 3);
    scene.add(fill);
    scene.add(new THREE.AmbientLight(0x404850, 1.1));

    let targetX = 0, targetY = 0;
    window.addEventListener("pointermove", (e) => {
      targetX = (e.clientX / window.innerWidth - 0.5) * 0.6;
      targetY = (e.clientY / window.innerHeight - 0.5) * 0.4;
    });

    function resize() {
      const wrap = canvas.parentElement;
      const w = Math.min(wrap.clientWidth, window.innerWidth);
      const h = Math.max(wrap.clientHeight, 1);
      renderer.setSize(w, h, false);
      // Belt-and-suspenders: some mobile WebViews let a canvas's internal
      // drawing-buffer size leak into its layout size for a frame before
      // CSS fully applies, which can widen the page and let a horizontal
      // swipe "stick". Force the CSS box explicitly every resize so the
      // canvas can never be wider than its wrapper regardless of engine quirks.
      canvas.style.width = "100%";
      canvas.style.height = "100%";
      canvas.style.maxWidth = "100%";
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
    }
    window.addEventListener("resize", resize);
    resize();

    let raf;
    const clock = new THREE.Clock();
    function tick() {
      const t = clock.getElapsedTime();
      rig.rotation.y += 0.0022;
      rig.rotation.x = 0.15 + targetY * 0.4 + Math.sin(t * 0.2) * 0.02;
      rig.rotation.z += (targetX * 0.5 - rig.rotation.z) * 0.02;
      armGroup.rotation.z = t * 0.05;
      renderer.render(scene, camera);
      raf = requestAnimationFrame(tick);
    }
    tick();

    document.addEventListener("visibilitychange", () => {
      if (document.hidden) cancelAnimationFrame(raf);
      else tick();
    });
  }

  /* ---------------- Boot ---------------- */
  document.addEventListener("DOMContentLoaded", () => {
    initHeader();
    initFooterYear();
    initContactLinks();
    initMobileActionBar();
    initFloatingButtons();
    initContactLinks(); // re-run: wires the floating WhatsApp button added above
    initLightbox();
    initMachineryFilters();
    initSparePartsGrid();
    initProductPage();
    initQuoteForm();
    initContactForm();
    initHero3D();
    initReveal();
  });
})();
