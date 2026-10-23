// Ficha dun xogo: comparador antes/despois, parcheador e emulador no navegador

(() => {
  // ---------- Comparador ----------
  document.querySelectorAll("[data-comparador]").forEach((comp) => {
    const pestanas = comp.querySelectorAll("[data-pestana]");
    const paneis = comp.querySelectorAll("[data-panel]");
    pestanas.forEach((p) => p.addEventListener("click", () => {
      pestanas.forEach((q) => q.setAttribute("aria-selected", String(q === p)));
      paneis.forEach((panel) => { panel.hidden = panel.dataset.panel !== p.dataset.pestana; });
    }));
    paneis.forEach((panel) => {
      const rango = panel.querySelector("input[type=range]");
      rango.addEventListener("input", () => panel.style.setProperty("--pos", rango.value + "%"));
    });
  });

  // ---------- Parcheador ----------
  const caixa = document.querySelector("[data-parcheador]");
  if (!caixa) return;
  const cfg = JSON.parse(caixa.dataset.parcheador);
  const zona = caixa.querySelector("[data-zona]");
  const entrada = caixa.querySelector("[data-ficheiro]");
  const pasos = caixa.querySelector("[data-pasos]");
  const resultado = caixa.querySelector("[data-resultado]");
  const mensaxe = caixa.querySelector("[data-mensaxe]");
  const descargar = caixa.querySelector("[data-descargar]");
  const xogar = caixa.querySelector("[data-xogar]");
  const outra = caixa.querySelector("[data-outra]");
  let urlDescarga = null;
  let romParcheada = null;

  const hex = (buf) => Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, "0")).join("");
  const sha1 = async (bytes) => hex(await crypto.subtle.digest("SHA-1", bytes));
  const desdeHex = (h) => new Uint8Array(h.match(/../g).map((x) => parseInt(x, 16)));

  function paso(nome, estado) {
    const li = pasos.querySelector(`[data-paso="${nome}"]`);
    li.classList.remove("facendo", "feito", "erro");
    if (estado) li.classList.add(estado);
  }

  function amosar(texto, ok) {
    mensaxe.textContent = texto;
    resultado.classList.toggle("ok", ok);
    resultado.classList.toggle("mal", !ok);
    resultado.hidden = false;
    descargar.hidden = !ok;
    if (xogar) xogar.hidden = !ok;
  }

  function reiniciar() {
    if (urlDescarga) URL.revokeObjectURL(urlDescarga);
    urlDescarga = null;
    romParcheada = null;
    entrada.value = "";
    pasos.hidden = true;
    resultado.hidden = true;
    zona.hidden = false;
    pasos.querySelectorAll("li").forEach((li) => li.classList.remove("facendo", "feito", "erro"));
  }

  // Le un .zip co propio navegador (DecompressionStream), sen bibliotecas.
  async function sacarDoZip(buf) {
    const v = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
    let fin = -1;
    for (let i = buf.length - 22; i >= Math.max(0, buf.length - 65557); i--) {
      if (v.getUint32(i, true) === 0x06054b50) { fin = i; break; }
    }
    if (fin < 0) throw new Error("O .zip parece estar danado.");
    let p = v.getUint32(fin + 16, true);
    const total = v.getUint16(fin + 10, true);
    const ext = cfg.extension.toLowerCase();
    for (let n = 0; n < total; n++) {
      if (v.getUint32(p, true) !== 0x02014b50) break;
      const metodo = v.getUint16(p + 10, true);
      const tamComprimido = v.getUint32(p + 20, true);
      const lonNome = v.getUint16(p + 28, true);
      const lonExtra = v.getUint16(p + 30, true);
      const lonComentario = v.getUint16(p + 32, true);
      const local = v.getUint32(p + 42, true);
      const nome = new TextDecoder().decode(buf.subarray(p + 46, p + 46 + lonNome));
      p += 46 + lonNome + lonExtra + lonComentario;
      if (!nome.toLowerCase().endsWith(ext)) continue;
      const inicio = local + 30 + v.getUint16(local + 26, true) + v.getUint16(local + 28, true);
      const datos = buf.subarray(inicio, inicio + tamComprimido);
      if (metodo === 0) return datos;
      if (metodo !== 8) throw new Error("Este .zip usa un método de compresión que o navegador non entende. Descomprímeo primeiro.");
      const fluxo = new Blob([datos]).stream().pipeThrough(new DecompressionStream("deflate-raw"));
      return new Uint8Array(await new Response(fluxo).arrayBuffer());
    }
    throw new Error(`Dentro do .zip non hai ningún ficheiro ${cfg.extension}.`);
  }

  // Separa a cabeceira iNES (16 bytes) do contido. Sen cabeceira, ponse a do parche.
  function separar(rom) {
    const temCabeceira = rom.length >= 16 && rom[0] === 0x4e && rom[1] === 0x45 && rom[2] === 0x53 && rom[3] === 0x1a;
    if (temCabeceira) return { cabeceira: rom.subarray(0, 16), contido: rom.subarray(16) };
    return { cabeceira: desdeHex(cfg.cabeceira), contido: rom };
  }

  function aplicarIPS(rom, ips) {
    const saida = new Uint8Array(rom);
    let datos = saida;
    const le3 = (i) => (ips[i] << 16) | (ips[i + 1] << 8) | ips[i + 2];
    if (String.fromCharCode(...ips.subarray(0, 5)) !== "PATCH") throw new Error("O parche non é un IPS válido.");
    let i = 5;
    while (i + 3 <= ips.length) {
      if (ips[i] === 0x45 && ips[i + 1] === 0x4f && ips[i + 2] === 0x46) break; // EOF
      const despraz = le3(i);
      let tam = (ips[i + 3] << 8) | ips[i + 4];
      i += 5;
      let bloque;
      if (tam === 0) {
        tam = (ips[i] << 8) | ips[i + 1];
        bloque = new Uint8Array(tam).fill(ips[i + 2]);
        i += 3;
      } else {
        bloque = ips.subarray(i, i + tam);
        i += tam;
      }
      if (despraz + tam > datos.length) {
        const maior = new Uint8Array(despraz + tam);
        maior.set(datos);
        datos = maior;
      }
      datos.set(bloque, despraz);
    }
    return datos;
  }

  async function procesar(ficheiro) {
    reiniciar();
    zona.hidden = true;
    pasos.hidden = false;
    let actual = "ler";
    try {
      paso("ler", "facendo");
      let rom = new Uint8Array(await ficheiro.arrayBuffer());
      if (/\.7z$|\.rar$/i.test(ficheiro.name)) throw new Error("Os ficheiros .7z e .rar non se poden abrir aquí. Descomprímeo primeiro e arrastra a ROM.");
      if (rom[0] === 0x50 && rom[1] === 0x4b) rom = await sacarDoZip(rom);
      paso("ler", "feito");

      actual = "comprobar";
      paso("comprobar", "facendo");
      const { cabeceira, contido } = separar(rom);
      const suma = await sha1(contido);
      if (suma === cfg.sha1Saida) {
        paso("comprobar", "feito");
        amosar("Esta ROM xa está traducida ao galego. Non hai nada que facer!", false);
        descargar.hidden = true;
        return;
      }
      if (suma !== cfg.sha1Entrada) {
        throw new Error(contido.length === cfg.tamano
          ? "Esta ROM ten o tamaño correcto pero non é a versión que precisa a tradución. Mira na ficha cal é a boa (a revisión e a rexión importan)."
          : "Esta ROM non é a que precisa a tradución. Mira na ficha o nome exacto e as sumas de comprobación.");
      }
      paso("comprobar", "feito");

      actual = "parchear";
      paso("parchear", "facendo");
      const resposta = await fetch(cfg.parche);
      if (!resposta.ok) throw new Error("Non se puido descargar o parche. Comproba a conexión e téntao de novo.");
      const ips = new Uint8Array(await resposta.arrayBuffer());
      const enteira = new Uint8Array(cabeceira.length + contido.length);
      enteira.set(cabeceira);
      enteira.set(contido, cabeceira.length);
      const parcheada = aplicarIPS(enteira, ips);
      paso("parchear", "feito");

      actual = "verificar";
      paso("verificar", "facendo");
      if ((await sha1(parcheada.subarray(16))) !== cfg.sha1Saida) throw new Error("O resultado non coincide co esperado. Non descargues nada e avísanos, por favor.");
      paso("verificar", "feito");

      romParcheada = parcheada;
      urlDescarga = URL.createObjectURL(new Blob([parcheada], { type: "application/octet-stream" }));
      descargar.href = urlDescarga;
      descargar.download = cfg.saida;
      amosar("Feito! A túa ROM xa está en galego.", true);
    } catch (e) {
      paso(actual, "erro");
      amosar(e.message || String(e), false);
    }
  }

  entrada.addEventListener("change", () => { if (entrada.files[0]) procesar(entrada.files[0]); });
  ["dragenter", "dragover"].forEach((ev) => zona.addEventListener(ev, (e) => { e.preventDefault(); zona.classList.add("enriba"); }));
  ["dragleave", "drop"].forEach((ev) => zona.addEventListener(ev, () => zona.classList.remove("enriba")));
  zona.addEventListener("drop", (e) => {
    e.preventDefault();
    const f = e.dataTransfer.files[0];
    if (f) procesar(f);
  });
  outra.addEventListener("click", reiniciar);

  // ---------- Xogar no navegador (JSNES) ----------
  const dialogo = document.querySelector("[data-dialogo-xogo]");
  if (!xogar || !dialogo) return;
  const pantalla = dialogo.querySelector("[data-pantalla-xogo]");
  let emulador = null;

  const cargarJsnes = () => new Promise((ok, mal) => {
    if (window.jsnes) return ok();
    const s = document.createElement("script");
    s.src = cfg.jsnes;
    s.onload = () => ok();
    s.onerror = () => mal(new Error("Non se puido cargar o emulador."));
    document.head.appendChild(s);
  });

  xogar.addEventListener("click", async () => {
    if (!romParcheada) return;
    try {
      await cargarJsnes();
    } catch (e) {
      amosar(e.message, false);
      return;
    }
    dialogo.showModal();
    emulador = new window.jsnes.Browser({
      container: pantalla,
      onError: (e) => console.error(e),
    });
    emulador.loadROM(romParcheada);
    // sen o recorte de 8 píxeles polos lados que JSNES fai por defecto, para ver o marcador enteiro
    // (loadROM volve poñelo, así que vai despois)
    emulador.nes.ppu.clipToTvSize = false;
    emulador.fitInParent();
    pantalla.focus();
  });

  const parar = () => {
    if (emulador) { emulador.destroy(); emulador = null; }
  };
  dialogo.querySelector("[data-pechar]").addEventListener("click", () => dialogo.close());
  dialogo.addEventListener("close", parar);
  window.addEventListener("resize", () => { if (emulador) emulador.fitInParent(); });
})();
