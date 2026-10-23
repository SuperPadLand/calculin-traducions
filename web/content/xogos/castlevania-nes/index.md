---
title: "Castlevania"
date: 2026-08-28
subtitulo: "Simon Belmont contra o castelo de Drácula, co marcador, os menús e os créditos en galego."
sistema: "NES"
plataforma: "NES"
ano: 1987
compania: "Konami"
xenero: "Acción e plataformas"
version: "1.0"
estado: "Completa"

probada: true
probada_data: 2026-08-28
probada_como: "Xogouse enteira, de principio a fin, no emulador ares, sen atopar ningún texto roto nin ningunha letra rara."

portada: "capturas/titulo-gl.png"
pixelada: true
comparacions:
  - nome: "Título"
    orixinal: "capturas/titulo-en.png"
    galego: "capturas/titulo-gl.png"
  - nome: "Marcador"
    orixinal: "capturas/marcador-en.png"
    galego: "capturas/marcador-gl.png"
  - nome: "Fin da partida"
    orixinal: "capturas/finxogo-en.png"
    galego: "capturas/finxogo-gl.png"

traducido:
  - "Pantalla de título e avisos legais (agás os nomes das empresas)"
  - "Marcador: PUNTOS, TEMPO, FASE, XOGADOR e XEFE"
  - "Fin da partida: FIN XOGO, SEGUIR e FIN"
  - "Créditos finais: as etiquetas e a despedida"
sen_traducir:
  - "Os nomes do reparto nos créditos: son parodias de actores de cine e, como nomes propios, quedan como están"

rom:
  nome: "Castlevania (USA).nes"
  nota: "A revisión 0. **Non valen** a Rev 1 nin a versión europea."
  crc32: "39C879BB"
  md5: "00d93c9f6b8aefb8b6c02b20147df4ec"
  tamano: "131 088 bytes"

parcheador:
  parche: "parches/castlevania-nes/castlevania_galego.ips"
  extension: ".nes"
  # SHA-1 do contido da ROM sen a cabeceira iNES de 16 bytes: así vale
  # calquera cabeceira (iNES clásica ou NES 2.0) e mesmo sen cabeceira.
  sha1_entrada: "ee09b857c90916edd92a20c463485a610b0a76fd"
  sha1_saida: "0d3b448914337aaf5294540fd1cb1015e018c632"
  tamano_sen_cabeceira: 131072
  cabeceira: "4e45531a080021000000000000000000"
  saida: "Castlevania (galego).nes"
  xogable: true

descargas:
  - nome: "Parche BPS"
    nota: "Recomendado se parcheas á man: avisa se a ROM non é a boa"
    ficheiro: "parches/castlevania-nes/castlevania_galego.bps"
    destacada: true
  - nome: "Parche IPS"
    nota: "Para aplicadores antigos. Non comproba nada"
    ficheiro: "parches/castlevania-nes/castlevania_galego.ips"
  - nome: "Paquete completo"
    nota: "Os dous parches e o LEME con instrucións (.zip)"
    url: "https://github.com/SuperPadLand/calculin-traducions/releases/download/v1.0/Castlevania-galego-v1.0.zip"

creditos:
  - ["Tradución", "Calculín Traducións"]
  - ["Ferramentas", "[Wave](https://github.com/sewave) (Hextractor e a súa documentación)"]
---

Simon Belmont entra no castelo de Drácula cun látego e pouco máis: dezaoito fases, seis xefes e unha das dificultades máis lendarias da NES. O texto do xogo é escaso, pero está sempre á vista, porque o marcador acompáñate de principio a fin.

O difícil foi o gráfico. A fonte de Castlevania non ten nin **X** nin **Z**, e o galego precisa as dúas (XOGADOR, XEFE, LICENZA). Debuxáronse de novo sobre letras que o xogo non usa: o X ocupa o sitio do K no marcador e o Z o do W na pantalla de título. O **É** é o que debuxou Wave para a súa tradución ao castelán, reaproveitado tal cal.

Os enderezos que documentou Wave eran doutra revisión da ROM, así que houbo que buscar cada texto orixinal na revisión 0 antes de inserir nada.
