---
name: siglent-scope
description: >
  Configurar el osciloscopio Siglent SDS824X HD (192.168.60.223) y capturar
  pantallazos (screenshots) de forma fiable sin saturar el servidor SCPI.
  Usar SOLO cuando se necesite configurar el scope, armar captura SPI, o
  tomar pantallazos del osciloscopio para inspeccion visual.
  REGLA CRITICA: ESPERAR 1 SEGUNDO ENTRE COMANDOS SCPI para no matar el scope.
---

# Siglent SDS824X HD — Config + Screenshots

## Contexto

- **Scope:** Siglent SDS824X HD @ `192.168.60.223`, SCPI port `5025` (LXI).
- **VNC web:** `http://192.168.60.223/Instrument/novnc/vnc_auto.php`
- El servidor SCPI del scope es **inestable con sesiones persistentes** y
  **se cae (timeout/offline) si le mandas comandos muy rapido**.
- **REGLA DE ORO:** esperar **1 segundo** (`time.sleep(1.0)`) entre CADA comando
  SCPI. Nunca mandar un lote de comandos sin delay. Si el scope deja de responder
  a ping, lo mataste — hay que ir fisicamente a despertarlo.

## Transporte recomendado

Una conexion TCP por comando (ver `tools/siglent_lib.py::SiglentSCPI`).
Cada `cmd()` abre socket, manda `\n`, cierra. El `sleep(1)` va FUERA del socket,
entre comandos:

```python
from siglent_lib import SiglentSDS800X
import time

scope = SiglentSDS800X("192.168.60.223")
scope.connect()
time.sleep(1)                      # <-- SIEMPRE esperar 1s tras connect

scope.cmd("CHANnel1:DISPlay ON")
time.sleep(1)                      # <-- 1s entre comandos
scope.cmd("TIMebase:SCALe 0.00002")
time.sleep(1)
# ...
```

## Config estandar SPI (sniffer CC1125)

Canal mapping (wiring fisico NUCLEO-G070RB → CC1125):
- CH1 = CS   (PB0, trigger falling @ 1.65V)
- CH3 = CLK  (PA5 SCK)
- CH4 = MOSI (PA7)
- CH2 = MISO (PA6)

```bash
python tools/siglent_lib.py sds-spi-standard --ip 192.168.60.223
```
Eso ya hace `configure_spi_standard()` con 1V/div, BW20M, 20µs/div, trigger CS.

## Armar captura + esperar trigger

```python
scope.single()                 # arma single
time.sleep(1)
scope.wait_trigger(timeout_s=15)   # poll TRIGger:STATus? cada 50ms
```
Luego el usuario dispara el SPI (envia `C`+`D` o `T` al NUCLEO).

## Pantallazos (SCREENSHOTS) — la parte dificil

### Lo que NO funciona

| Metodo | Por que falla |
|--------|---------------|
| `SCReen:DATA?` (SCPI) | Timeout — el scope rechaza bulk transfer grande |
| `WAVeform:DATA?` (10M pts) | Devuelve `#9000000346WAVEDESC...` (blob, no datos) |
| `WAVeform:DATA?` (4k-20k pts) | Timeout en socket SCPI |
| Chrome headless `--screenshot` | Canvas VNC queda NEGRO (no hay GPU para pintar) |
| Puppeteer headless (waitUntil load) | Pagina carga pero canvas VNC queda negro |
| `curl http://.../screenshot` | Puerto 80 cerrado, no hay endpoint HTTP directo |

### Lo que SI funciona: puppeteer + --use-gl=swiftshader

El canvas VNC se pinta con WebGL/Canvas. Headless Chrome necesita un
renderizador de software (SwiftShader) para decodificar el stream VNC:

```javascript
// /tmp/scope_shot.js  (requiere: npm install puppeteer en /tmp)
const puppeteer = require('/tmp/node_modules/puppeteer');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/google-chrome-stable',
    headless: 'new',
    args: [
      '--no-sandbox', '--disable-setuid-sandbox',
      '--use-gl=swiftshader',     // <-- CLAVE: render software para el canvas VNC
      '--ignore-gpu-blocklist',
      '--window-size=1366,850'
    ],
  });
  const page = await browser.newPage();
  await page.setViewport({width:1366, height:850});
  await page.goto('http://192.168.60.223/Instrument/novnc/vnc_auto.php',
    {waitUntil:'load', timeout:20000}).catch(()=>{});
  await new Promise(r => setTimeout(r, 12000));   // esperar a que VNC pinte
  await page.screenshot({path:'/tmp/scope_shots/scope.png'});
  await browser.close();
})();
```

```bash
mkdir -p /tmp/scope_shots
timeout 45 node /tmp/scope_shot.js
```

**Nota:** `google-chrome-stable` y `node`/`npm` estan en el dev box.
`puppeteer` va en `/tmp/node_modules` (npm install puppeteer).
Este dev box NO tiene pip/ensurepip/sudo → Playwright no se puede instalar.

### Secuencia completa (scope config + screenshot)

1. Esperar que el scope este online (ping 192.168.60.223).
2. `sds-spi-standard` (config estandar, ya con sleeps 1s internos).
3. `scope.single()` + sleep 1s.
4. Disparar SPI en el NUCLEO (SSH a 192.168.60.140, `echo D > /dev/nucleo_g070rb`).
5. `wait_trigger(15)` para confirmar captura.
6. `node /tmp/scope_shot.js` → `/tmp/scope_shots/scope.png`.
7. Leer el PNG con la herramienta Read para inspeccion visual.

## Troubleshooting

- **Scope no responde a ping:** lo mataste con comandos rapidos. Hay que ir
  fisicamente a despertarlo/reiniciarlo. No sirve de nada reintentar por red.
- **TRIGger:STATus? = "Ready" siempre:** el CS (PB0) no esta togglando, o el
  probe no esta en PB0. Revisar wiring.
- **MISO/CLK planos en pantallazo:** CC1125 sin energia (el PIC era su VCC).
