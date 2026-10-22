/* La Florería de Eva · interacción de la web */
(function () {
  "use strict";
  var doc = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* Cabecera: sólida al bajar, se esconde al seguir bajando */
  var header = $("[data-header]");
  var lastY = 0;
  function onScroll() {
    var y = window.scrollY;
    header.classList.toggle("is-solid", y > 40);
    header.classList.toggle("is-hidden", y > 500 && y > lastY && !doc.classList.contains("menu-open"));
    lastY = y;
    var top = $(".to-top");
    if (top) top.classList.toggle("is-on", y > 900);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* Menú móvil y desplegables */
  var burger = $(".burger");
  burger.addEventListener("click", function () {
    var open = doc.classList.toggle("menu-open");
    burger.setAttribute("aria-expanded", open);
    burger.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  });
  $$(".nav-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var li = btn.parentElement;
      var open = !li.classList.contains("is-open");
      $$(".has-mega").forEach(function (o) { o.classList.remove("is-open"); o.firstElementChild.setAttribute("aria-expanded", "false"); });
      li.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", open);
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".has-mega")) $$(".has-mega").forEach(function (o) { o.classList.remove("is-open"); });
  });
  $$(".nav a").forEach(function (a) {
    a.addEventListener("click", function () { doc.classList.remove("menu-open"); burger.setAttribute("aria-expanded", "false"); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { doc.classList.remove("menu-open"); $$(".has-mega").forEach(function (o) { o.classList.remove("is-open"); }); }
  });

  /* Aparición al hacer scroll y flores de tinta que se dibujan */
  var targets = $$(".reveal, .reveal-l, .reveal-r, .ink");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    targets.forEach(function (t, i) {
      if (t.classList.contains("reveal") && t.parentElement) {
        var sibs = Array.prototype.indexOf.call(t.parentElement.children, t);
        t.style.transitionDelay = Math.min(sibs % 6, 5) * 70 + "ms";
      }
      io.observe(t);
    });
  } else {
    targets.forEach(function (t) { t.classList.add("is-in"); });
  }

  /* Hero: pase de fotos y parallax suave */
  var hero = $("[data-hero]");
  if (hero) {
    var slides = $$(".hero-slide", hero);
    var dots = $$(".hero-dots button", hero);
    var cur = 0, timer;
    function show(n) {
      slides[cur].classList.remove("is-on");
      if (dots[cur]) dots[cur].classList.remove("is-on");
      cur = (n + slides.length) % slides.length;
      var pic = slides[cur];
      var img = $("img", pic);
      if (img && img.loading === "lazy") img.loading = "eager";
      pic.classList.add("is-on");
      if (dots[cur]) { dots[cur].classList.remove("is-on"); void dots[cur].offsetWidth; dots[cur].classList.add("is-on"); }
    }
    function play() { clearInterval(timer); timer = setInterval(function () { show(cur + 1); }, 6500); }
    if (slides.length > 1 && !reduce) {
      play();
      dots.forEach(function (d, i) { d.addEventListener("click", function () { show(i); play(); }); });
    }
    var media = $("[data-parallax]", hero);
    if (media && !reduce) {
      window.addEventListener("scroll", function () {
        var y = window.scrollY;
        if (y < window.innerHeight * 1.2) media.style.transform = "translate3d(0," + y * 0.22 + "px,0)";
      }, { passive: true });
    }
  }

  /* Contadores */
  $$("[data-count]").forEach(function (el) {
    function run() {
      var end = parseFloat(el.getAttribute("data-count"));
      var dec = (el.getAttribute("data-count").split(".")[1] || "").length;
      if (reduce) { el.textContent = end.toFixed(dec).replace(".", ","); return; }
      var t0 = null;
      function step(t) {
        if (!t0) t0 = t;
        var p = Math.min((t - t0) / 1600, 1);
        var v = end * (1 - Math.pow(1 - p, 3));
        el.textContent = v.toFixed(dec).replace(".", ",");
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }
    if ("IntersectionObserver" in window) {
      var o = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { run(); o.disconnect(); } }, { threshold: 0.5 });
      o.observe(el);
    } else run();
  });

  /* Años desde la apertura (22 de octubre de 2022) */
  $$("[data-years]").forEach(function (el) {
    var open = new Date(2022, 9, 22), now = new Date();
    var y = now.getFullYear() - 2022 - (now < new Date(now.getFullYear(), 9, 22) ? 1 : 0);
    el.textContent = Math.max(y, 1);
    if (el.hasAttribute("data-count")) el.setAttribute("data-count", Math.max(y, 1));
  });

  /* Abierto / cerrado (hora de Madrid): martes a sábado, 9:00 a 14:00 */
  function madridNow() {
    try {
      var parts = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Madrid", weekday: "short", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).formatToParts(new Date());
      var o = {}; parts.forEach(function (p) { o[p.type] = p.value; });
      var days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
      return { d: days[o.weekday], m: parseInt(o.hour, 10) * 60 + parseInt(o.minute, 10) };
    } catch (e) { var n = new Date(); return { d: n.getDay(), m: n.getHours() * 60 + n.getMinutes() }; }
  }
  var names = ["domingo", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado"];
  var now = madridNow();
  var openDay = now.d >= 2 && now.d <= 6;
  var isOpen = openDay && now.m >= 540 && now.m < 840;
  var statusText;
  if (isOpen) statusText = "Abierto ahora · hasta las 14:00";
  else {
    var nd = now.d, k = 0;
    if (openDay && now.m < 540) statusText = "Cerrado · abre hoy a las 9:00";
    else {
      do { nd = (nd + 1) % 7; k++; } while (!(nd >= 2 && nd <= 6));
      statusText = "Cerrado · abre " + (k === 1 ? "mañana" : "el " + names[nd]) + " a las 9:00";
    }
  }
  $$("[data-status]").forEach(function (s) {
    s.classList.toggle("is-open", isOpen);
    var t = $("[data-status-text]", s); if (t) t.textContent = statusText;
  });
  $$("[data-hours] tr").forEach(function (tr) { if (+tr.getAttribute("data-day") === now.d) tr.classList.add("is-today"); });
  $$("[data-year]").forEach(function (y) { y.textContent = new Date().getFullYear(); });

  /* Galería: filtros y visor */
  $$("[data-filters]").forEach(function (bar) {
    var gal = document.getElementById(bar.getAttribute("data-filters"));
    $$("button", bar).forEach(function (b) {
      b.addEventListener("click", function () {
        $$("button", bar).forEach(function (x) { x.classList.remove("is-on"); });
        b.classList.add("is-on");
        var f = b.getAttribute("data-f");
        $$(".g-item", gal).forEach(function (it) {
          var cats = (it.getAttribute("data-cat") || "").split(" ");
          it.classList.toggle("is-hidden", f !== "all" && cats.indexOf(f) < 0);
        });
      });
    });
  });

  var lb = $("[data-lightbox]");
  if (lb) {
    var lbImg = $("img", lb), lbCap = $("figcaption", lb), list = [], idx = 0, lastFocus;
    function open(items, i) {
      list = items; idx = i; lastFocus = document.activeElement;
      paint(); lb.hidden = false; doc.style.overflow = "hidden"; $(".lb-close", lb).focus();
    }
    function paint() {
      var a = list[idx];
      lbImg.src = a.getAttribute("href");
      lbImg.alt = a.getAttribute("data-cap") || "";
      lbCap.textContent = a.getAttribute("data-cap") || "";
    }
    function close() { lb.hidden = true; doc.style.overflow = ""; if (lastFocus) lastFocus.focus(); }
    function go(d) { idx = (idx + d + list.length) % list.length; paint(); }
    document.addEventListener("click", function (e) {
      var a = e.target.closest("[data-lb]");
      if (!a) return;
      e.preventDefault();
      var g = a.closest("[data-gallery]");
      var items = (g ? $$("[data-lb]", g) : [a]).filter(function (x) { return !x.classList.contains("is-hidden"); });
      open(items, items.indexOf(a));
    });
    $(".lb-close", lb).addEventListener("click", close);
    $(".lb-prev", lb).addEventListener("click", function () { go(-1); });
    $(".lb-next", lb).addEventListener("click", function () { go(1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") go(-1);
      if (e.key === "ArrowRight") go(1);
    });
    var sx = null;
    lb.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) go(dx < 0 ? 1 : -1);
      sx = null;
    });
  }

  /* Reseñas: avance automático suave */
  $$("[data-autoscroll]").forEach(function (q) {
    if (reduce) return;
    var paused = false;
    q.addEventListener("pointerenter", function () { paused = true; });
    q.addEventListener("pointerleave", function () { paused = false; });
    q.addEventListener("touchstart", function () { paused = true; }, { passive: true });
    setInterval(function () {
      if (paused) return;
      var card = q.firstElementChild; if (!card) return;
      var w = card.getBoundingClientRect().width + 20;
      if (q.scrollLeft + q.clientWidth >= q.scrollWidth - 10) q.scrollTo({ left: 0, behavior: "smooth" });
      else q.scrollBy({ left: w, behavior: "smooth" });
    }, 5200);
  });

  /* Formulario de encargo: prepara el mensaje de WhatsApp */
  var form = $("[data-order]");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var f = new FormData(form);
      var lines = ["¡Hola Eva! 🌸 Te escribo desde la web para un encargo:", ""];
      [["nombre", "Me llamo"], ["tipo", "Me interesa"], ["fecha", "Lo necesito para"], ["entrega", "Entrega"], ["colores", "Colores / estilo"], ["mensaje", "Detalles"]].forEach(function (p) {
        var v = (f.get(p[0]) || "").toString().trim();
        if (v) lines.push("• " + p[1] + ": " + v);
      });
      window.open("https://wa.me/34607803222?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
    });
  }

  /* Botón de volver arriba y pista del botón de WhatsApp */
  var top = $(".to-top");
  if (top) top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" }); });
  var waf = $(".wa-float");
  if (waf && !reduce) {
    setTimeout(function () { waf.classList.add("is-peek"); setTimeout(function () { waf.classList.remove("is-peek"); }, 4000); }, 6000);
  }
})();
