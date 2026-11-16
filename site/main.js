// Onglets « Du premier mot au livre imprimé », langue du site, et lien direct vers la dernière version.
(() => {
  const lang = document.body.dataset.lang || "fr";
  const HOME = { fr: "/", en: "/en/", es: "/es/" };

  // Langue : le choix fait avec FR / EN / ES est retenu ; sinon, à la première visite
  // de l'accueil français, on suit la langue du navigateur.
  const remember = (l) => { try { localStorage.setItem("trame.site.lang", l); } catch {} };
  document.querySelectorAll("[data-setlang]").forEach((a) => a.addEventListener("click", () => remember(a.dataset.setlang)));
  if (location.pathname === "/" && lang === "fr" && !/bot|crawl|spider|slurp/i.test(navigator.userAgent)) {
    let saved = null;
    try { saved = localStorage.getItem("trame.site.lang"); } catch {}
    const nav = (navigator.languages || [navigator.language || "fr"]).map((l) => l.slice(0, 2).toLowerCase());
    const wanted = saved || nav.find((l) => l in HOME) || "en";
    if (wanted !== "fr" && HOME[wanted]) { location.replace(HOME[wanted] + location.hash); return; }
  }

  const tabs = [...document.querySelectorAll('.modes [role="tab"]')];
  const select = (tab, focus) => {
    for (const t of tabs) {
      const on = t === tab;
      t.setAttribute("aria-selected", String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    }
    if (focus) tab.focus();
  };
  tabs.forEach((tab, i) => {
    tab.addEventListener("click", () => select(tab));
    tab.addEventListener("keydown", (e) => {
      const n = tabs.length;
      const next = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: n - 1 }[e.key];
      if (next === undefined) return;
      e.preventDefault();
      select(tabs[(next + n) % n], true);
    });
  });

  // Vidéo : pas d'animation pour qui l'a demandé au système.
  const video = document.querySelector(".hero-video video");
  if (video && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    video.removeAttribute("autoplay");
    video.pause();
    video.controls = true;
  }

  // La page des versions reste le lien de secours si GitHub ne répond pas.
  const TXT = {
    fr: { v: (v) => `Version ${v}, pour Windows 10 et 11.`, s: (v, mo) => `(version ${v}, ${mo} Mo)` },
    en: { v: (v) => `Version ${v}, for Windows 10 and 11.`, s: (v, mo) => `(version ${v}, ${mo} MB)` },
    es: { v: (v) => `Versión ${v}, para Windows 10 y 11.`, s: (v, mo) => `(versión ${v}, ${mo} MB)` },
  }[lang];
  fetch("https://api.github.com/repos/shizeh/trame-versions/releases/latest")
    .then((r) => (r.ok ? r.json() : Promise.reject()))
    .then((rel) => {
      const exe = (rel.assets || []).find((a) => /x64-setup\.exe$/.test(a.name));
      if (!exe) return;
      const version = rel.tag_name.replace(/^v/, "");
      const mo = Math.round(exe.size / 1e6);
      document.querySelectorAll("[data-download]").forEach((a) => (a.href = exe.browser_download_url));
      document.querySelectorAll("[data-version]").forEach((el) => (el.textContent = TXT.v(version)));
      document.querySelectorAll("[data-size]").forEach((el) => (el.textContent = TXT.s(version, mo)));
    })
    .catch(() => {});
})();
