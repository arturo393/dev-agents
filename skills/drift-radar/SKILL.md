---
name: drift-radar
description: Informa qué código está duplicado y ya divergido entre los repos de ~/uqomm — drivers, parsers de protocolo, CRC — y qué opcodes se declaran fuera del contrato. Usar antes de editar un driver o un archivo de protocolo compartido, cuando un bugfix "no tuvo efecto", cuando dos equipos responden distinto al mismo comando, o para medir la deuda de duplicación. Es de solo lectura: no modifica ningún repo.
---

Decís **dónde el mismo código vive más de una vez y ya no coincide**. No arreglás nada:
el informe es el producto.

## Cómo se corre

```bash
~/.claude/skills/drift-radar/scripts/scan.sh            # sobre /home/arturo/uqomm
~/.claude/skills/drift-radar/scripts/scan.sh /otra/raiz
```

Tarda ~1 minuto sobre ~1000 archivos. **No escribe nada.** Si alguien te pide que
"arregles la deriva", el radar no es la herramienta: reportá y dejá la decisión.

## Por qué existís

El protocolo RDSS vive en más de un lugar y las copias ya no coinciden. Un cambio en una
no llega a las otras, y nada avisa. Medido:

| Qué | Estado |
|---|---|
| `CommandMessage.cpp` | **6 versiones distintas** en 4 repos |
| `CommandMessage.hpp` | **6 versiones distintas** en 4 repos |
| CRC-16/XMODEM | **13 implementaciones** independientes del mismo algoritmo |
| `eeprom.c`, `eeprom.h` | 3 versiones en 3 repos |
| `Sx1278.cpp`, `Lora.cpp` | drivers de la misma radio, divergidos |

Es el patrón **P5** de `fw-vlad/docs/RETROSPECTIVA_Y_ESTRATEGIA.md`: el problema no es que
una esté mal, es que **hay varias** y cada una respalda una conclusión distinta.

## Las cinco secciones del informe

| # | Qué muestra | Para qué sirve |
|---|---|---|
| 1 | **Divergidos**: mismo nombre, hashes distintos, >1 repo | lo caro: un bugfix acá no llega allá |
| 2 | **Aún idénticos** en >1 repo | lo barato: todavía se unifican sin resolver conflictos |
| 3 | **CRC-16**: definiciones con `0x1021` + bucle de desplazamiento | tests y usos excluidos, para que el número sea real |
| 4 | **Opcodes** declarados fuera de `sw-diagnosticoremoto/contracts/tg-protocol.json` | el contrato es la fuente de verdad; lo de afuera es riesgo |
| 5 | Las dos variantes de `jira-report` | `.claude/` se genera desde `.opencode/`; si difieren, regenerar |

## Cómo interpretás lo que sale

1. **La sección 2 es la oportunidad, no la sección 1.** Un archivo aún idéntico en 4 repos
   se unifica sin resolver conflictos. Uno con 6 versiones cuesta días. Prioridad al que
   todavía no divergió.
2. **Dos hashes en 4 ubicaciones no es "2 copias".** Puede ser un proyecto clonado entero:
   `gateway-2lora` y `gateway-2lora-simple` comparten 129 de 130 archivos. Decilo así, en
   vez de contar archivos sueltos.
3. **Un archivo de vendor duplicado no es deuda tuya.** `system_stm32f0xx.c` lo genera
   CubeMX. Separalo del código propio en el informe.
4. **La sección 4 lista archivos, no divergencias.** Que un opcode se declare fuera del
   contrato no prueba que esté mal — prueba que nadie lo verifica. Para confirmar una
   divergencia real, invocá el agente `protocol-drift`, que compara las dos puntas.

## Cómo reportás

Ordenado por **costo de arreglarlo ahora vs. después**, no por cantidad de líneas. Por cada
grupo: el basename, cuántas versiones, en qué repos, y cuál parece la más completa. Y decí
explícitamente qué **no** miraste — el radar solo mira `.c/.cpp/.h/.hpp`, así que las
declaraciones en Go, Python, Rust y TypeScript quedan fuera de las secciones 1 y 2.
