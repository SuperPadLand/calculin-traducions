# Calculín Traducións

Traducións de videoxogos retro ao **galego** (norma RAG).
Aquí só se distribúen **parches**: as ROMs non se inclúen nin se van incluír.

*Traducciones de videojuegos retro al **gallego** (norma RAG). Aquí solo se
distribuyen **parches**: las ROMs no se incluyen ni se van a incluir.*

---

## Agradecementos · Agradecimientos

Este proxecto apóiase enteiramente no traballo que **Wave** (Sergio López
Cantero, *Traduccións Wave*) liberou para todo o mundo. Úsanse as súas
**ferramentas** e mais a súa **documentación**:

- [**Hextractor**](https://github.com/sewave/hextractor) — a ferramenta de
  extracción e inserción de texto, con licenza MIT.
- [**sewave/translations**](https://github.com/sewave/translations) — as táboas
  de caracteres (`.tbl`), os offsets (`.off`) e os tiles dos acentos. Iso é a
  parte máis traballosa do romhacking e el deixouna aberta.

Moitas grazas por publicalo todo. Sen ese traballo previo, cada un destes
xogos serían meses de enxeñaría inversa en vez de días de tradución.

> *Este proyecto se apoya enteramente en el trabajo que **Wave** (Sergio López
> Cantero, Traducciones Wave) liberó para todo el mundo: sus **herramientas**
> (Hextractor, licencia MIT) y su **documentación** (tablas de caracteres,
> offsets y tiles de los acentos). Muchas gracias por publicarlo todo.*

---

## Traducións dispoñibles · Traducciones disponibles

| Xogo | Sistema | Versión | Estado |
|---|---|---|---|
| [Castlevania (USA)](castlevania-nes/) | NES | v0.1 | Xogable, probado só nas primeiras pantallas |

---

## Como aplicar un parche · Cómo aplicar un parche

1. Consigue a túa copia da ROM e comproba o seu **MD5** co que indica o
   `LEME.txt` da carpeta. A revisión importa: un parche aplicado sobre a ROM
   equivocada dá un xogo roto.
2. Aplica o ficheiro **`.bps`** cun aplicador calquera
   ([Flips](https://www.smwcentral.net/?p=section&s=tools), beat, ou un
   aplicador web). O formato BPS leva sumas de comprobación e avisa se a ROM
   non é a correcta.
3. Se o teu aplicador é antigo e só entende IPS, tes tamén o `.ips`. **Ollo**:
   o IPS non comproba nada e non che vai avisar de nada.

> *1. Consigue tu copia de la ROM y comprueba su MD5 con el que indica el
> `LEME.txt` de la carpeta. 2. Aplica el `.bps` con Flips, beat o un aplicador
> web: el formato BPS lleva sumas de comprobación y avisa si la ROM no es la
> correcta. 3. Si tu aplicador solo entiende IPS, tienes también el `.ips`,
> pero ese no comprueba nada.*

---

## Erros e suxestións · Errores y sugerencias

Se atopas un texto cortado, unha letra rara ou algo que non se traduciu, abre
unha **incidencia** (*issue*) indicando o xogo, a pantalla e, se podes, unha
captura.

---

## Licenza · Licencia

As traducións (textos e tiles novos) distribúense para uso libre e non
comercial. Os xogos son propiedade das súas respectivas empresas; este
proxecto non ten relación ningunha con elas e **non distribúe ningún xogo**.

*Las traducciones (textos y tiles nuevos) se distribuyen para uso libre y no
comercial. Los juegos son propiedad de sus respectivas empresas; este proyecto
no tiene ninguna relación con ellas y **no distribuye ningún juego**.*
