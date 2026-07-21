# Hardware Antifragility Foundation

Resilience patterns for projects interacting with physical instruments or lab infrastructure.

---

## 1. Simulation Mode Fallback

Instrument controllers (USB-TMC, Serial, TCP) must load native drivers dynamically. If the driver doesn't exist (CI without hardware), enter Simulation Mode transparently — never abort or throw initialization exception.

```python
try:
    driver = load_native_driver(device)
except DriverNotFoundError:
    driver = SimulationDriver(device)
```

## 2. Tolerant Tests

Don't assert fixed ideal states. `"degraded"` is an expected controlled state that isolates software bugs from physical hardware failures.

```python
# Correct
assert response["status"] in {"ok", "degraded"}

# Incorrect
assert response["status"] == "ok"
```

## 3. LD_PRELOAD for Binary Incompatibilities

Vendor SDKs compiled against deprecated libraries require injecting the compatible library via `ENV LD_PRELOAD` in the Dockerfile. Prevents crashes without degrading host security.

```dockerfile
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libudev.so.1
```

## 4. Hostname Offline-First

Format: `<client>-<role>-<location>-<mac-last4>`

```
# Correct
myapp-testbench-lab-657a
monitor-prod-8f2c

# Incorrect (causes collisions, doesn't work offline)
testbench-1
testbench-2
```
