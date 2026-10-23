// Tema, filtros da grella e comentarios

(() => {
  const raiz = document.documentElement;
  const escuroDoSistema = window.matchMedia("(prefers-color-scheme: dark)");
  const temaActual = () => raiz.dataset.theme || (escuroDoSistema.matches ? "dark" : "light");

  // ---------- Tema ----------
  document.querySelectorAll("[data-cambiar-tema]").forEach((boton) => {
    boton.addEventListener("click", () => {
      const novo = temaActual() === "dark" ? "light" : "dark";
      raiz.dataset.theme = novo;
      try { localStorage.setItem("tema", novo); } catch (e) {}
      avisarGiscus();
    });
  });
  escuroDoSistema.addEventListener("change", () => { if (!raiz.dataset.theme) avisarGiscus(); });

  // ---------- Filtros ----------
  const filtros = document.querySelector("[data-filtros]");
  const grella = document.querySelector("[data-grella]");
  if (filtros && grella) {
    const chips = filtros.querySelectorAll("[data-sistema]");
    const soProbadas = filtros.querySelector("[data-so-probadas]");
    const baleiro = document.querySelector("[data-baleiro]");
    let sistema = "";
    const aplicar = () => {
      let visibles = 0;
      grella.querySelectorAll(".tarxeta").forEach((t) => {
        const ok = (!sistema || t.dataset.sistema === sistema) && (!soProbadas.checked || t.dataset.probada === "si");
        t.hidden = !ok;
        if (ok) visibles++;
      });
      if (baleiro) baleiro.hidden = visibles > 0;
    };
    chips.forEach((chip) => chip.addEventListener("click", () => {
      sistema = chip.dataset.sistema;
      chips.forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
      aplicar();
    }));
    soProbadas.addEventListener("change", aplicar);
  }

  // ---------- Comentarios (giscus) ----------
  const caixaGiscus = document.querySelector("[data-giscus]");
  const temaGiscus = () => (temaActual() === "dark" ? "dark_dimmed" : "light");
  function avisarGiscus() {
    const marco = document.querySelector("iframe.giscus-frame");
    if (marco) marco.contentWindow.postMessage({ giscus: { setConfig: { theme: temaGiscus() } } }, "https://giscus.app");
  }
  if (caixaGiscus) {
    const d = caixaGiscus.dataset;
    const s = document.createElement("script");
    s.src = "https://giscus.app/client.js";
    s.async = true;
    s.crossOrigin = "anonymous";
    const atributos = {
      "data-repo": d.repo,
      "data-repo-id": d.repoId,
      "data-category": d.category,
      "data-category-id": d.categoryId,
      "data-mapping": "specific",
      "data-term": d.term,
      "data-strict": "1",
      "data-reactions-enabled": "1",
      "data-emit-metadata": "0",
      "data-input-position": "top",
      "data-theme": temaGiscus(),
      "data-lang": d.lang,
      "data-loading": "lazy",
    };
    Object.entries(atributos).forEach(([k, v]) => s.setAttribute(k, v));
    caixaGiscus.appendChild(s);
  }
})();
