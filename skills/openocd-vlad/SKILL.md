---
name: openocd-vlad
description: >
  Leer, flashear y diagnosticar las placas VLAD25 (STM32G474) por SWD con OpenOCD sobre SSH,
  y leer su log por USB CDC. Usar cuando se necesite: grabar firmware, leer una variable o
  contador del firmware en la placa, leer la causa de un reinicio o un volcado de HardFault,
  identificar CUAL de las varias placas del banco esta conectada, o capturar el log de arranque.
  REGLA CRITICA: verificar la placa por UID ANTES de escribir nada — hay 3 o 4 unidades VLAD25
  en el banco y ya se midio y casi se grabo la equivocada.
---

# OpenOCD + VLAD25 por SSH

**Para qué:** operar las placas VLAD25 por SWD y USB desde otra máquina, con los controles que
evitan medir o grabar la unidad equivocada. **No hace:** no reemplaza al osciloscopio para
problemas eléctricos, y no diagnostica RF.

## Por qué SSH y no un puerto TCP

OpenOCD en **batch** (`-c "init; …; shutdown"`) por SSH, no un servidor escuchando:

- No deja nada con estado que se cuelgue. El ST-Link se colgó cuatro veces en un día con
  `LIBUSB_ERROR_IO`, y un `openocd` residente además retiene el adaptador.
- No abre acceso de depuración a la red. OpenOCD escucha en `:3333` (GDB), `:4444` (telnet),
  `:6666` (Tcl); bindear a `0.0.0.0` expone el control del equipo.
- Es determinista y scripteable.

**Excepción:** una sesión interactiva de GDB (breakpoints, paso a paso). Ahí sí conviene TCP —
pero bindeado a `localhost` y **tunelizado por SSH**, nunca expuesto.

## Las seis reglas, y qué costó no tenerlas

| Regla | Lo que pasó sin ella |
|---|---|
| **Verificar por UID antes de escribir** | hay 3–4 unidades; se midió y casi se grabó otra |
| **Puerto CDC por `by-id`, nunca `ttyACM<n>`** | se leyó `ttyACM0` tras un reflasheo que movió la placa a `ttyACM1`, donde `ttyACM1` era el generador Signal Hound. Media hora creyendo que la placa estaba muda |
| **Direcciones desde el ELF, no anotadas** | el relink las mueve; una dirección vieja dio `0` y se leyó como "el firmware no corre" |
| **`md5` en toda transferencia** | el enlace con `.101` trunca sin avisar: 0 B, 98304 B y 116012 B contra 132396 B, y ninguno avisó |
| **`--serial` del probe si hay más de uno** | hubo dos probes con dos targets distintos, los dos `chipid 0x469` |
| **Distinguir el fallo del adaptador del fallo del objetivo** | ver la tabla de abajo |

## Identidad: siempre primero

```sh
ssh HOST 'sudo -n timeout 60 openocd -f interface/stlink.cfg -f target/stm32g4x.cfg \
  -c "init; halt; echo [format \"UID %08x %08x %08x\" {*}[read_memory 0x1FFF7590 32 3]]; resume; shutdown" \
  2>&1 | grep -E "^UID|Error"'
```

El serial USB que ST deriva del UID es **`UID[0] + UID[2]`**, y los últimos 4 caracteres salen de
`UID[1] >> 16`. Unidades conocidas:

| UID[0] + UID[2] | Serial USB | Cuál es |
|---|---|---|
| `0x2075338F` | `2075338F3645` | la de referencia del banco |
| `0x206C3688` | `206C36884531` | segunda placa |
| `0x206F376F` | — | tercera |
| `0x2070378D` | — | cuarta |

## Leer una variable del firmware

**La dirección sale del ELF que coincide con lo flasheado**, nunca de una nota:

```sh
arm-none-eabi-nm vlad25_vhf/Debug/vlad25_vhf.elf | grep -E " [bBdD] g_mi_variable$"
```

Y después, con `halt` / `resume` alrededor — sin `halt` la lectura no devuelve nada:

```sh
ssh HOST 'sudo -n timeout 60 openocd -f interface/stlink.cfg -f target/stm32g4x.cfg \
  -c "init; halt; echo [format \"valor=%d\" [read_memory 0x20000060 32 1]]; resume; shutdown" \
  2>&1 | grep -E "^valor|Error"'
```

> **`mdw` NO imprime** cuando se pasa por `-c` en OpenOCD 0.12. Usar `read_memory` + `echo`
> + `format`, que además devuelve una lista Tcl y sirve para leer varias palabras de una.

Anchos: `read_memory <addr> <bits> <cantidad>` — `32` para `uint32_t`, `8` para bytes.

## Flashear

```sh
# 1. Binario y md5 de origen
arm-none-eabi-objcopy -O binary vlad25_vhf.elf /tmp/fw.bin && md5sum /tmp/fw.bin

# 2. Copiar y VERIFICAR el md5 en destino. Si no coincide, NO se graba.
scp /tmp/fw.bin HOST:/tmp/fw.bin && ssh HOST 'md5sum /tmp/fw.bin'

# 3. Confirmar la identidad por UID (arriba)

# 4. Grabar
ssh HOST 'sudo -n timeout 180 openocd -f interface/stlink.cfg -f target/stm32g4x.cfg \
  -c "program /tmp/fw.bin 0x08000000 verify reset exit" 2>&1 \
  | grep -iE "Programming Finished|Verified OK|Error"'
```

Éxito es **las dos** líneas: `** Programming Finished **` y `** Verified OK **`.

`interface/stlink.cfg` sirve para V2 y V3. Con varios probes, agregar
`-c "adapter serial <SERIAL>"` **antes** de `-f target/...`.

## Reiniciar sin grabar

```sh
ssh HOST 'sudo -n timeout 60 openocd -f interface/stlink.cfg -f target/stm32g4x.cfg \
  -c "init; reset run; shutdown" 2>&1 | tail -3'
```

## Registros de respaldo: lo que sobrevive al reinicio

Viven en el TAMP, base **`0x40002500`** (BKP0R), 32 registros de 32 bits. **Sobreviven al reset**
pero no a un corte de alimentación sin VBAT — un contador de arranques en 1 significa corte real.

| Índice | Dirección | Contenido |
|---|---|---|
| 0 | `0x40002500` | contador de arranques |
| 1 | `0x40002504` | causa: 1 POWER_ON · 2 PIN · 3 SOFTWARE · 4 IWDG |
| 2 | `0x40002508` | marca (`Error_Handler`, desborde de pila, heap agotado) |
| 3 | `0x4000250C` | reinicios pedidos por el supervisor de BLE |
| 4 | `0x40002510` | firma de quién pidió el último reinicio (`ResetSrc`) |
| 20–26 | `0x40002550`+ | volcado del HardFault: magic, PC, LR, CFSR, HFSR, tick, BFAR |

```sh
ssh HOST 'sudo -n timeout 60 openocd -f interface/stlink.cfg -f target/stm32g4x.cfg \
  -c "init; halt; echo [format \"arranques=%d causa=%d\" {*}[read_memory 0x40002500 32 2]]; \
      echo [format \"crash magic=%08x PC=%08x LR=%08x CFSR=%08x HFSR=%08x tick=%d BFAR=%08x\" \
      {*}[read_memory 0x40002550 32 7]]; resume; shutdown" 2>&1 | grep -E "^arranques|^crash|Error"'
```

Con el `PC` a mano, el nombre de la línea sale de:

```sh
arm-none-eabi-addr2line -f -C -i -e vlad25_vhf/Debug/vlad25_vhf.elf 0x0800e938
```

> `CFSR` con `0x8200` es `PRECISERR` + `BFARVALID`: error de bus preciso, y `BFAR` tiene la
> dirección culpable. `HFSR` con `0x40000000` es `FORCED`, o sea que escaló a HardFault.

## Option bytes: el registro NO es la flash

Leer y escribir los option bytes (RDP, BFB2, DBANK, nBOOT…) del G474:

```sh
# Leer: OPTR vive en 0x40022020. bit 20 = BFB2, bit 22 = DBANK.
ssh HOST 'sudo -n timeout 60 openocd -f interface/stlink.cfg -f target/stm32g4x.cfg \
  -c "init; halt; echo [format \"OPTR=%08x\" [read_memory 0x40022020 32 1]]; resume; shutdown" \
  2>&1 | grep -E "^OPTR|Error"'

# Escribir: option_write <bank_id> <offset> <valor> <mascara>, y DESPUES option_load <bank_id>
ssh HOST 'sudo -n timeout 150 openocd -f interface/stlink.cfg -f target/stm32g4x.cfg -c "
  init; halt
  stm32l4x option_write 0 0x20 0x00100000 0x00100000
  stm32l4x option_load 0
  shutdown" 2>&1 | tail -3'
```

Tres trampas, las tres pisadas:

| Trampa | Qué pasa |
|---|---|
| **Leer `OPTR` justo después de `option_write` NO prueba nada** | muestra el **registro**, no lo que quedó en flash. Una restauración se leyó como exitosa —`BFB2=0`— y al resetear volvió a 1: el registro estaba escrito y la flash no |
| **`option_load` sin `bank_id`** | imprime el *usage* y **no hace nada**, sin error. El cambio queda sin comprometer |
| **`option load failed` es engañoso** | `OBL_LAUNCH` resetea el chip y OpenOCD pierde el handshake, así que reporta fallo **aunque haya comprometido**. No sirve como veredicto |

**La única comprobación válida es resetear y volver a leer**: `init; reset halt; echo [format …]`.
Un reset recarga `OPTR` desde la flash, así que lo que se lee ahí sí es lo persistido.

> Antes de tocar un option byte, confirmar **`RDP level 0`** en la salida de OpenOCD. Con RDP > 0
> la recuperación deja de ser un `option_write` y pasa a implicar borrado masivo.

## El log por USB CDC

Usar `sw-vlad-dac-tools/tools/vlad25_log.py`, que resuelve por `by-id` y **sobrevive a la
re-enumeración** — con `cat` se pierde justo la línea `[BOOT]`, que es la que interesa:

```sh
python3 tools/vlad25_log.py --listar                        # qué unidades hay
python3 tools/vlad25_log.py --serial 2075338F3645 --segundos 40
python3 tools/vlad25_log.py --solo BOOT,CRASH,BLE,SMOKE     # sin el latido
```

Para capturar un arranque: lanzar el lector, y **después** reiniciar por SWD.

Etiquetas y qué significan:

| Línea | Qué dice |
|---|---|
| `[BOOT] #N causa=…` | contador de arranques y causa del reset |
| `[CLK] SYSCLK=…` | el reloj REAL derivado del RCC, no `SystemCoreClock` |
| `[CRASH] …` | el arranque anterior murió en HardFault, con `PC`/`LR`/`CFSR` |
| `[SMOKE] A/B …` | prueba SPI del módulo BLE: `OK` contesta AT · `READY_NO_AT` habla el bus y no el comando · `NO_READY` **no pone nada en MISO** · `RDY_TIMEOUT` no enciende |
| `[BLE] modulo NO inicializado` | el módulo no arrancó y el firmware **no le manda AT**: el equipo sigue entero |

## Cuando falla: el fallo del adaptador NO es el fallo del objetivo

| Síntoma | Qué es | Qué hacer |
|---|---|---|
| `Found 0 stlink programmers` | el probe no está en el bus USB | revisar el cable USB del probe |
| `chipid 0x0000`, `flash 0` | el probe está sano y **no hay nada en SWD** | revisar los cuatro hilos del header —un GND flojo da exactamente esto—, a cuál placa está enchufado, y si esa placa tiene alimentación |
| `LIBUSB_ERROR_IO` | el **adaptador** colgado, no el objetivo | reiniciarlo por `USBDEVFS_RESET` sin desenchufar (ver abajo) |
| `Can not connect to target` con `probe` funcionando | el objetivo se reinicia en bucle y tira la sesión, **o** el hub USB está saturado | ver la nota del hub |
| `libusb submiturb failed, errno=2` | el nodo USB desaparece en medio de la transferencia | casi siempre el hub |

Reiniciar el adaptador colgado, sin tocar cables:

```sh
ssh HOST 'sudo -n python3 -c "
import fcntl, re, subprocess
o = subprocess.check_output([\"lsusb\"]).decode()
for ln in o.splitlines():
    if \"0483:37\" in ln:
        g = re.match(r\"Bus (\d+) Device (\d+)\", ln)
        f = open(\"/dev/bus/usb/%s/%s\" % (g.group(1), g.group(2)), \"wb\")
        fcntl.ioctl(f, 0x5514, 0)   # USBDEVFS_RESET
        f.close(); print(\"adaptador reiniciado\")
"'
```

### El hub compartido: la trampa que costó una tarde

Si el probe **y** el USB de la placa cuelgan del mismo hub, y la placa se reinicia en bucle, cada
re-enumeración martilla el hub y el probe pierde sus transferencias. Se ve como un problema del
SWD y no lo es:

```sh
ssh HOST 'dmesg | grep -iE "error -71|error -110|cannot reset"'
```

`-71` (EPROTO) y `-110` (timeout) sobre el mismo hub lo confirman. La salida es física: mover el
probe a otro puerto, o desenchufar el USB de la placa mientras se graba — el SWD alcanza, y la
placa sigue alimentada por su fuente.

## Antes de creerle a una medición

- Un cero de una lectura por SWD **no es un dato** hasta confirmar que la dirección salió del ELF
  correcto. Una dirección vieja lee cero y parece un firmware muerto.
- Un volcado de HardFault en cero **no prueba que no hubo HardFault** si vive en `.bss`: el
  arranque lo borra. Solo vale la copia del dominio de respaldo.
- La palabra de salud en `0x0000` significa **"todavía no se calculó"** (nadie mandó `0x12` ni
  corrió la telemetría), no "todo mal".
- Si el equipo se reinicia mientras medís, cualquier valor de RAM es de un arranque distinto al
  que crees. Leer el contador de arranques al principio y al final de la medición.
