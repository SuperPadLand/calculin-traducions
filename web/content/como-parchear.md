---
title: "Como parchear un xogo"
antetitulo: "Guía"
subtitulo: "Un parche só leva os cambios da tradución. Ponse enriba da túa copia do xogo e convértea na versión en galego."
---

## A vía rápida: o parcheador da web

Nos xogos de consola, cada ficha ten un parcheador:

1. Arrastra a túa ROM ao recadro (vale tamén dentro dun `.zip`).
2. A web comproba que é exactamente a versión que precisa a tradución.
3. Se o é, devólvecha xa traducida para descargala. Nos xogos de NES podes xogala alí mesmo.

Todo pasa no teu navegador: **a ROM non se envía a ningures**. A web só descarga o parche, que é un ficheiro pequeno cos cambios.

## Por que importa a versión?

Un parche escribe en posicións concretas da ROM. Se a túa copia é doutra revisión ou doutra rexión, eses cambios caen onde non deben e o xogo sae roto ou nin arranca. Por iso cada ficha indica o nome exacto da ROM e as súas sumas de comprobación (CRC32 e MD5).

O parcheador da web compara o **contido** da ROM, non a cabeceira de 16 bytes que levan as ROMs de NES. Se a túa copia ten outra cabeceira (por exemplo, NES 2.0) pero o xogo é o mesmo, vale igual.

## A vía clásica: parchear á man

Se o prefires, descarga o parche desde a ficha e aplícao cun programa:

- **Ficheiros `.bps`**: [Flips](https://github.com/Alcaro/Flips) ou calquera aplicador moderno. O formato BPS comproba a ROM antes e despois, e avisa se non é a correcta. É o recomendado.
- **Ficheiros `.ips`**: valen os mesmos programas. Ollo, o formato IPS non comproba nada: se a ROM non é a boa, o resultado sairá roto sen aviso ningún.

Garda sempre unha copia da ROM orixinal. O parche aplícase sobre unha copia e, se algo sae mal, volves empezar.

## Xogos de PC

Nos xogos de PC non hai ROM: a tradución vén cun instalador que traduce os ficheiros da túa instalación de Steam e garda unha copia dos orixinais para poder desfacelo. As instrucións están en cada ficha.

## E onde consigo o xogo?

Iso non podemos dicilo nin facilitalo: aquí non se distribúe ningún xogo. O lóxico é que fagas a copia do teu propio cartucho ou que o teñas comprado.
