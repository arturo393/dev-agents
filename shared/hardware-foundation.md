# Hardware Antifragility Foundation

Patrones de resiliencia para proyectos que interactúan con instrumentos físicos o infraestructura de laboratorio.

---

## 1. Simulation Mode Fallback

Controladores de instrumentos (USB-TMC, Serial, TCP) deben cargar drivers nativos dinámicamente. Si el driver no existe (CI sin hardware), entrar en Modo Simulación transparente — nunca abortar ni lanzar excepción de inicialización.

```python
# Ejemplo
try:
    driver = load_native_driver(device)
except DriverNotFoundError:
    driver = SimulationDriver(device)
```

## 2. Tests Tolerantes

No asertar estados ideales fijos. `"degraded"` es un estado controlado esperado que aísla bugs de software de fallos físicos del hardware.

```python
# Correcto
assert response["status"] in {"ok", "degraded"}

# Incorrecto
assert response["status"] == "ok"
```

## 3. LD_PRELOAD para Incompatibilidades Binarias

SDKs de fabricantes compilados contra librerías deprecadas requieren inyectar la librería compatible via `ENV LD_PRELOAD` en el Dockerfile. Evita crashes sin degradar seguridad del host.

```dockerfile
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libudev.so.1
```

## 4. Hostname Offline-First

Formato: `<client>-<role>-<location>-<mac-last4>`

```
# Correcto
uqomm-testbench-lab-657a
safetymind-monitor-prod-8f2c

# Incorrecto (genera colisiones, no funciona offline)
testbench-1
testbench-2
```
