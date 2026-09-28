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

  /* ---------------- Contact / WhatsApp helpers ---------------- */
  function digitsOnly(str) {
    return (str || "").replace(/[^\d+]/g, "");
  }

  function buildWhatsAppLink(message) {
    const number = COMPANY.whatsapp;
    const isPlaceholder = !number || /_HERE$/.test(number);
    if (isPlaceholder) return null;
    const digits = digitsOnly(number).replace(/^\+/, "");
    const text = encodeURIComponent(message || `Hello ${COMPANY.name}, I would like more information.`);
    return `https://wa.me/${digits}?text=${text}`;
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
        .map((p) => `<a href="tel:${digitsOnly(p)}">${p}</a>`)
        .join('<span class="sep" aria-hidden="true"></span>');
    });
    $$("[data-email-list]").forEach((el) => {
      el.innerHTML = COMPANY.emails
        .map((e) => `<a href="mailto:${e}">${e.replace("@", "@<wbr>")}</a>`)
        .join('<span class="sep" aria-hidden="true"></span>');
    });
    $$("[data-whatsapp]").forEach((el) => {
      const productName = el.dataset.whatsappProduct;
      const msg = productName
        ? `Hello ${COMPANY.name}, I am interested in the ${productName}. Please provide more information.`
        : undefined;
      const link = buildWhatsAppLink(msg);
      if (link) {
        el.href = link;
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
      const modelsLine = p.models && p.models.length
        ? p.models.map((m) => m.code).join(" · ")
        : "";
      return `
      <div class="card reveal" data-category="${p.category}" data-name="${p.name.toLowerCase()}">
        <a href="product.html?slug=${p.slug}" class="card-media">
          <img src="assets/img/${p.image}.jpg" alt="${p.name}" loading="lazy">
          <span class="tag">${cat ? cat.short : ""}</span>
        </a>
        <div class="card-body">
          <span class="cat-label">${cat ? cat.name : ""}</span>
          <h3><a href="product.html?slug=${p.slug}">${p.name}</a></h3>
          ${modelsLine ? `<div class="models">${modelsLine}</div>` : ""}
        </div>
        <div class="card-foot">
          <a href="product.html?slug=${p.slug}">View Details</a>
          <a href="quote.html?product=${p.slug}" class="foot-quote">Request Quote</a>
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
        CATEGORIES.map((c) => `<button class="chip" data-cat="${c.slug}">${c.short}</button>`).join("");
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
        <div class="card-media"><img src="assets/img/${g.image}.jpg" alt="${g.name}" loading="lazy"></div>
        <div class="card-body"><h4>${g.name}</h4></div>
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
      root.innerHTML = `<div class="empty-state"><h3 class="h3">Machine not found</h3><p class="mt-2">This product may have moved. Browse the full catalogue instead.</p><a href="machinery.html" class="btn btn-dark mt-4">View All Machinery</a></div>`;
      return;
    }

    const cat = getCategoryBySlug(product.category);
    document.title = `${product.name} — ${COMPANY.name}`;
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
      featWrap.innerHTML = product.features.map((f) => `<li>${f}</li>`).join("");
    } else {
      featWrap.closest(".product-features-block")?.classList.add("hidden");
    }

    const specWrap = $("#product-specs");
    if (product.models && product.models.length) {
      specWrap.innerHTML = product.models
        .map((m) => `<tr><td>Model</td><td>${m.code}${m.spec ? ` — ${m.spec}` : ""}</td></tr>`)
        .join("");
    } else {
      specWrap.closest(".product-specs-block")?.classList.add("hidden");
    }

    $("#product-quote-link").href = `quote.html?product=${product.slug}`;
    const waBtn = $("#product-whatsapp");
    if (waBtn) waBtn.dataset.whatsappProduct = product.name;

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
            <a href="product.html?slug=${p.slug}" class="card-media">
              <img src="assets/img/${p.image}.jpg" alt="${p.name}" loading="lazy">
            </a>
            <div class="card-body">
              <h4><a href="product.html?slug=${p.slug}">${p.name}</a></h4>
            </div>
          </div>`
          )
          .join("");
      }
    }
    initContactLinks();
  }

  /* ---------------- Quote form ---------------- */
  function initQuoteForm() {
    const form = $("#quote-form");
    if (!form) return;
    const params = new URLSearchParams(location.search);
    const preselect = params.get("product");
    const productSelect = $("#qf-product");

    CATEGORIES.forEach(() => {});
    if (productSelect) {
      productSelect.innerHTML =
        `<option value="">Select a machine (optional)</option>` +
        PRODUCTS.map((p) => `<option value="${p.slug}">${p.name}</option>`).join("");
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

    function validate() {
      let ok = true;
      requiredFields.forEach((id) => {
        const el = $("#" + id);
        const field = el.closest(".field");
        if (!el.value.trim()) {
          field.classList.add("has-error");
          ok = false;
        } else {
          field.classList.remove("has-error");
        }
      });
      const emailEl = $("#qf-email");
      if (emailEl.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailEl.value)) {
        emailEl.closest(".field").classList.add("has-error");
        ok = false;
      } else {
        emailEl.closest(".field").classList.remove("has-error");
      }
      return ok;
    }

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const status = $("#quote-status");
      if (!validate()) {
        status.textContent = "Please fill in the required fields before sending.";
        status.classList.add("is-visible", "is-error");
        status.scrollIntoView({ behavior: "smooth", block: "center" });
        return;
      }
      const submitBtn = $('button[type="submit"]', form);
      submitBtn.disabled = true;
      submitBtn.textContent = "Sending…";
      status.classList.remove("is-error");

      // Integration point: replace this block with a real submission
      // (e.g. fetch('/api/quote', { method: 'POST', body: new FormData(form) }))
      // No backend is connected yet, so nothing is actually transmitted below.
      setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.textContent = "Send Enquiry";
        status.textContent =
          "Your enquiry is ready to send. This form is not yet connected to a backend or inbox — see the integration note in js/main.js, or contact the team directly below in the meantime.";
        status.classList.add("is-visible");
        form.reset();
        $("#selected-product-chip")?.classList.remove("is-visible");
      }, 700);
    });
  }

  /* ---------------- Contact page copy buttons ---------------- */
  function initCopyButtons() {
    $$("[data-copy]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(btn.dataset.copy);
          const original = btn.textContent;
          btn.textContent = "Copied";
          setTimeout(() => (btn.textContent = original), 1500);
        } catch (e) {
          /* clipboard unavailable — ignore silently */
        }
      });
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
    initLightbox();
    initMachineryFilters();
    initSparePartsGrid();
    initProductPage();
    initQuoteForm();
    initCopyButtons();
    initHero3D();
    initReveal();
  });
})();
