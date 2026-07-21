# Firmware Engineering Foundation

Patrones y reglas para desarrollo embedded C/C++ en microcontroladores (STM32, Cortex-M).

---

## Code UX (Embedded Specific)

### Checklist C++20

| # | Rule | How to verify |
|---|------|---------------|
| 1 | `[[nodiscard]]` en TODA función que retorna valor | `grep -c nodiscard` vs `grep -c 'bool\|uint'` |
| 2 | `std::span` sobre `T* + size` | `grep -rn '\bspan\b' Core/Inc/` |
| 3 | `std::optional<T>` sobre `bool + T&` | `grep -rn 'optional' Core/Inc/` |
| 4 | `static constexpr std::array` sobre C arrays | `grep -rn 'static const.*\[\]' Core/Inc/` |
| 5 | `static_assert` por módulo — mínimo 1 | `grep -c 'static_assert'` por archivo |
| 6 | RAII guard para estado HW | `grep -rn 'ScopeGuard' Core/` |
| 7 | `constexpr` todo lo posible | Inspección manual |
| 8 | `std::variant` dispatch sobre switch | `grep -rn 'std::variant' Core/` |

**Regla de oro:** Si el compilador no puede verificar tu invariante en compile-time, tu diseño no es lo suficientemente expresivo.

---

## MISRA-C / Safety

| Rule | Description |
|------|-------------|
| No Dynamic Allocation | NEVER use `malloc()` or `free()`. Static or stack only. |
| Strict Typing | Use `<stdint.h>` types (`uint8_t`, `int16_t`). Plain `int` prohibited. |
| Unsigned Constants | Use `U` suffix: `100U`, `0x55U` |
| Const Correctness | `const` for read-only: `const uint8_t *data` |
| Volatile in ISRs | Variables shared with ISR MUST be `volatile` |
| Atomic Access | Wrap multi-byte reads on Cortex-M0: `__disable_irq(); ... __enable_irq();` |
| Error Handling | Check EVERY HAL return: `if (status != HAL_OK)` |
| No Magic Numbers | All constants via `#define` or `enum` |

### Mandatory Toolchain Flags

```
-Os                          # Optimize for size
-fdata-sections -ffunction-sections  # Strip dead code
-Wl,--gc-sections            # Link with dead code elimination
-Wdouble-promotion           # Detect float->double on M4F
-fno-exceptions -fno-rtti    # No C++ exceptions/RTTI
```

---

## Testing Tiers

### Tier 1: Compile-Time Assertions (Zero Cost) — OBLIGATORIO

```cpp
static_assert(sizeof(UladPacket_t) == 74U, "Size changed");
static_assert(BUFFER_SIZE % 4U == 0U, "Must be 4-byte aligned for DMA");
static_assert(TABLE.size() > 0);
```

Si compila, la condición se cumple. Si no compila, atrapaste un bug antes de flashear.

### Tier 2: Off-Target Host Unit Tests

Extract pure-logic (CRC, parsers, state machines) from HAL dependencies:

```c
/* Compile with: gcc test_crc.c crc.c -o test_crc && ./test_crc */
#include <assert.h>
#include "crc.h"
int main(void) {
    uint8_t data[] = {0x01, 0x02, 0x03};
    assert(crc16_compute(data, sizeof(data)) == 0x6131U);
    return 0;
}
```

### Tier 3: On-Target Smoke Self-Tests

Add `self_test_run()` called once at boot (after peripheral init, before super-loop).

- Failed self-test → log via UART/RTT + flag LED
- NEVER infinite-hang on failure

---

## Driver Structure

### Header Interface Pattern

```c
#ifndef MY_DRIVER_H
#define MY_DRIVER_H

#include "stm32f0xx_hal.h"

#define MY_DEVICE_I2C_ADDR  (0x4AU << 1U)

typedef struct {
    I2C_HandleTypeDef *hi2c;
    uint32_t           timeout;
    uint16_t           cached_value;
} MyDevice_t;

HAL_StatusTypeDef my_device_init(MyDevice_t *const dev, I2C_HandleTypeDef *const hi2c);
HAL_StatusTypeDef my_device_read(MyDevice_t *const dev, uint16_t *const out_val);

#endif
```

### State Machine Pattern

```c
typedef enum {
    SYS_STATE_BOOT = 0U,
    SYS_STATE_IDLE,
    SYS_STATE_TX,
    SYS_STATE_ERROR,
    SYS_STATE_COUNT
} SysState_t;

static SysState_t s_app_state = SYS_STATE_BOOT;

void app_state_machine_process(void) {
    switch (s_app_state) {
        case SYS_STATE_BOOT:
            if (self_test_run()) { s_app_state = SYS_STATE_IDLE; }
            else { s_app_state = SYS_STATE_ERROR; }
            break;
        case SYS_STATE_IDLE:
            break;
        default:
            s_app_state = SYS_STATE_BOOT; /* Safe recovery */
            break;
    }
}
```

### Non-Blocking Timeout Pattern

```c
uint32_t tick = HAL_GetTick();
while (!flag) {
    if ((HAL_GetTick() - tick) > TIMEOUT_MS) { return HAL_TIMEOUT; }
}
```

---

## C++20 Embedded Patterns

### RAII ScopeGuard

```cpp
#include "ScopeGuard.hpp"

void do_something() {
    radio->set_packet_mode(true);
    ScopeGuard guard([radio]() { radio->set_packet_mode(false); });
    // ... early-returns here ...
    // destructor restores packet_mode automatically
}
```

### Compile-Time Log Level

```cpp
#ifdef NDEBUG
constexpr LogLevel COMPILE_TIME_LOG_LEVEL = LogLevel::WARN;
#else
constexpr LogLevel COMPILE_TIME_LOG_LEVEL = LogLevel::VERBOSE;
#endif

template<LogLevel L = LogLevel::INFO>
void info(const char* format, ...) {
    if constexpr (L <= COMPILE_TIME_LOG_LEVEL) {
        va_list args; va_start(args, format);
        vprintf(format, args); va_end(args);
    }
}
```

En release, `logger_->debug(...)` compila a cero instrucciones. El string ni siquiera está en flash.

### Template Radio Concept

```cpp
template<typename R>
concept RadioDevice = requires(R& r, uint32_t freq, uint8_t* buf, uint8_t len) {
    { r.set_fsk_frequency(freq) } -> std::same_as<void>;
    { r.receive_packet(buf, len, bool{}, uint16_t{}) } -> std::same_as<uint8_t>;
};

template<RadioDevice Radio>
class MyApp {
    Radio* radio_;
public:
    explicit MyApp(Radio* r) : radio_(r) {}
    void run() { radio_->set_fsk_frequency(174925000); }
};
```

Si Lora no satisface el concept, no compila. Cero overhead en runtime.

---

## Naming Conventions (C/C++)

### C

| Element | Convention | Example |
|---------|------------|---------|
| Functions | `snake_case` + module prefix | `ulad_set_gain()` |
| Local variables | `snake_case` | `byte_count` |
| Static variables | `s_` prefix | `static Ulad_t s_instance;` |
| Global variables | `g_` prefix | `volatile uint32_t g_tick_ms;` |
| Structs / Enums | `PascalCase` + `_t` | `UartRxRing_t` |
| Constants / Macros | `ALL_CAPS_SNAKE` | `SENSOR_TIMEOUT_MS` |

### C++

| Element | Convention | Example |
|---------|------------|---------|
| Classes | `PascalCase` | `LoraCommandHandler` |
| Member variables | `m_` prefix | `m_huart` |
| Member methods | `snake_case` | `set_frequency()` |
| Enum class values | `UPPER_SNAKE` | `DeviceOperatingMode::RX_CONTINUOUS` |
