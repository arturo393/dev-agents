---
applyTo: "products/leaky-feeder/fw-ulad/**"
---

# fw-ulad Firmware Instructions

## Hardware Target
- **MCU**: STM32F030C8T6 (Cortex-M0, 48 MHz, 64 KB Flash, 8 KB RAM)
- **Board**: ULAD Rev 2.2 (Uqomm Leaky-Feeder Amplifier Driver)
- **Toolchain**: arm-none-eabi-gcc 13.3, STM32CubeIDE 1.19, GNU Make

## Build
```
make -C products/leaky-feeder/fw-ulad/firmware/Debug all
```
Flash via STM32_Programmer_CLI SWD port (PA13=SWDIO, PA14=SWCLK).

## Architecture
- **No RTOS** — bare-metal superloop in `main.c`
- **DMA** for ADC (circular, CH0–CH3, CH6–CH9 + TEMPSENSOR → `measurements[]`) and UART1 RX (circular, IDLE IRQ)
- **SPI bit-bang** for MCP4822 DACs (not hardware SPI)
- **I²C1** slave (STM32 receives remote attenuation commands), **I²C2** master (MCP3421 current sensor — disabled)
- **TIM15 PWM** for WS2812 RGB LED panel
- **BDA4601** attenuator: serial bit-bang on PB2/PB10/PB11

## ADC Channel Map (`measurements[]` — DMA fills in CH order)

`ADC_CHANNEL_NUMBER = 9U`. Scan: CH0,1,2,3,6,7,8,9,TEMPSENSOR (CH4/CH5 skipped — PA4/PA5 are digital outputs to U26 MCP4822).

| Index | Enum        | CH  | Pin | Signal         | Description                        |
|-------|-------------|-----|-----|----------------|------------------------------------|
| 0     | `vin`       | CH0 | PA0 | V_IN           | VIN monitor (×13.878/1000 → mV)   |
| 1     | `v_5v`      | CH1 | PA1 | V_SMPS         | +5V SMPS rail (×1.6125 → mV)      |
| 2     | `current`   | CH2 | PA2 | CURR_S_BASE    | INA138, 10 mΩ shunt → mA           |
| 3     | `agc152m`   | CH3 | PA3 | AGC_152M_S     | 152 MHz AGC DAC feedback           |
| 4     | `agc172m`   | CH6 | PA6 | AGC_172M_S     | 172 MHz AGC DAC feedback           |
| 5     | `ref172m`   | CH7 | PA7 | 172MHz_REF     | 172 MHz reference (MAX4003)        |
| 6     | `level172m` | CH8 | PB0 | 172M_SAMPLE    | 172 MHz UL RF level detector       |
| 7     | `tono_level`| CH9 | PB1 | TONO_LEVEL     | Pilot tone detector                |
| 8     | `ucTemperature` | TEMPSENSOR | internal | — | STM32 internal temperature    |

> PA4 = `CS_DAC_AGC` (U26 MCP4822) and PA5 = `LDAC_AGC` (U26 MCP4822) — digital outputs, **not** ADC inputs.

## GPIO Map

| Pin  | Define             | Direction | Peripheral       | Signal         |
|------|--------------------|-----------|------------------|----------------|
| PA0  | V_IN_Pin           | Analog IN | ADC CH0          | VIN monitor    |
| PA1  | V_5V_Pin           | Analog IN | ADC CH1          | 5V monitor     |
| PA2  | CURR_Pin           | Analog IN | ADC CH2          | Current sense  |
| PA3  | AGC_152M_Pin       | Analog IN | ADC CH3          | AGC 152M sample|
| PA4  | DAC_AGC_CS_Pin     | Output    | SPI bit-bang     | U26 MCP4822 CS (AGC DAC) |
| PA5  | DAC_AGC_LDAC_Pin   | Output    | SPI bit-bang     | U26 MCP4822 LDAC (AGC DAC) |
| PA6  | AGC_172M_Pin       | Analog IN | ADC CH6          | AGC 172M sample|
| PA7  | REF_172M_Pin       | Analog IN | ADC CH7          | 172M reference |
| PA8  | CONV_SMART_Pin     | Input     | GPIO             | CON/STT_SW mode|
| PA9  | —                  | Output    | USART1 TX        | TX_EXT serial  |
| PA10 | —                  | Input     | USART1 RX (DMA)  | RX_EXT serial  |
| PA11 | Con_Rev_Pin        | Input     | GPIO             | CONV_REVERSE   |
| PA12 | D4_Pin             | Input (pull-up) | GPIO        | Rotary switch Input4 (active-low) |
| PA13 | SWDIO              | —         | SWD              | Debugger       |
| PA14 | SWCLK              | —         | SWD              | Debugger       |
| PA15 | SPI_SS_Pin         | Output    | SPI1 (unused)    | SPI_SS         |
| PB0  | LEVEL_172M_Pin     | Analog IN | ADC CH8          | 172M level     |
| PB1  | TONO_LEVEL_Pin     | Analog IN | ADC CH9          | Tono level     |
| PB2  | LE_ATT_Pin         | Output    | Bit-bang         | BDA4601 LE     |
| PB3  | DAC_CLK_Pin        | Output    | SPI bit-bang     | MCP4822 SCK    |
| PB4  | —                  | Input     | SPI1 MISO        | (unused)       |
| PB5  | DAC_MOSI_Pin       | Output    | SPI bit-bang     | MCP4822 MOSI   |
| PB6  | —                  | I²C1 SCL  | I²C1 slave       | SCL_L          |
| PB7  | —                  | I²C1 SDA  | I²C1 slave       | SDA_L          |
| PB8  | LED_1_Pin          | Output    | GPIO             | Status LED 1   |
| PB9  | LED_2_Pin          | Output    | GPIO             | Keep-alive pulse LED (keepAliveON/OFF) |
| PB15 | —                  | Output    | TIM15 CH1N PWM   | WS2812 RGB panel data (complementary output) |
| PB10 | CLK_ATT_Pin        | Output    | Bit-bang         | BDA4601 CLK    |
| PB11 | DATA_ATT_Pin       | Output    | Bit-bang         | BDA4601 DATA   |
| PB12 | DAC_GAIN_CS_Pin    | Output    | SPI bit-bang     | U27 MCP4822 CS (GAIN DAC) |
| PB13 | DAC_GAIN_LDAC_Pin  | Output    | SPI bit-bang     | U27 MCP4822 LDAC (GAIN DAC) |
| PC13 | D1_Pin             | Input (pull-up) | GPIO        | Rotary switch Input1 (active-low) |
| PC14 | D2_Pin             | Input (pull-up) | GPIO        | Rotary switch Input2 (active-low) |
| PC15 | D3_Pin             | Input (pull-up) | GPIO        | Rotary switch Input3 (active-low) |

> PA4 = `CS_DAC_AGC` (U26 AGC DAC) and PA5 = `LDAC_AGC` (U26 AGC DAC) are **digital outputs** — confirmed by schematic Rev 2.2 sheet 2. CH4/CH5 are not configured in the ADC scan.

## Key Modules

| File                | Responsibility                                      |
|---------------------|-----------------------------------------------------|
| `main.c`            | Init, superloop, USART1_IRQHandler (IDLE detection) |
| `ulad.c / ulad.h`   | AGC logic, DAC control, telemetry, serial command parser |
| `uart1.c`           | UART DMA circular RX + IDLE IRQ frame detection     |
| `bda4601.c`         | BDA4601 attenuator SPI bit-bang driver + rotary SW  |
| `dac_mcp4822.c`     | MCP4822 DAC SPI bit-bang driver (GAIN + AGC)        |
| `i2c.c`             | I²C1 slave raw driver (remote attenuation via I²C)  |
| `log.c`             | UART log formatter (TEL / SIG / CMD / ATT lines)    |
| `eeprom.c`          | EEPROM page RW for persistent GAIN/AGC/ATT values   |
| `ws2812.c`          | WS2812 RGB LED panel driver (TIM15 PWM DMA)         |

## Coding Conventions
- MISRA-C subset: explicit casts, no VLAs, bounded loops, `uint8_t`/`uint16_t`/`uint32_t` everywhere
- No dynamic allocation — all static or stack
- Constants end in `U` (e.g. `10U`), pointers checked before use
- Log output via `writeTxStr()` — blocking per-char TX
- EMA (exponential moving average) filter on slow ADC channels (VIN/V5V/current/temp): `EMA_SHIFT = 3U` (α=1/8). RF channels bypass EMA for fast AGC response.
- See `KNOWN_ISSUES.md` for tracked bugs and pending fixes
