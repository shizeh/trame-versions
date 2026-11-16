// Onglets « Du premier mot au livre imprimé », et lien direct vers la dernière version.
(() => {
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

  // La page des versions reste le lien de secours si GitHub ne répond pas.
  fetch("https://api.github.com/repos/shizeh/trame-versions/releases/latest")
    .then((r) => (r.ok ? r.json() : Promise.reject()))
    .then((rel) => {
      const exe = (rel.assets || []).find((a) => /x64-setup\.exe$/.test(a.name));
      if (!exe) return;
      const version = rel.tag_name.replace(/^v/, "");
      const mo = Math.round(exe.size / 1e6);
      document.querySelectorAll("[data-download]").forEach((a) => (a.href = exe.browser_download_url));
      document.querySelectorAll("[data-version]").forEach((el) => (el.textContent = `Version ${version}, pour Windows 10 et 11.`));
      document.querySelectorAll("[data-size]").forEach((el) => (el.textContent = `(version ${version}, ${mo} Mo)`));
    })
    .catch(() => {});
})();
