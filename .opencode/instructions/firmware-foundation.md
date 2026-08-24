# Firmware Engineering Foundation

Patterns and rules for embedded C/C++ development on microcontrollers (STM32, Cortex-M).

---

## Alcance: que cosa tiene que cumplir esto, y desde cuando

### Un repo no es un firmware

Censo del 19-Ago-2026: **7 repos, ~24 productos**. `fw-rutherford` tiene 7 apps sobre una capa
`modules/`; `fw-gateway2lora` tiene 5 proyectos; `fw-vlad` tiene 4 (`vlad25_vhf`, `vlad_vhf`,
`vlad_vhf_cpp`, `vlad_vhf_stg`); `fw-snifferTelemetry` 3; `fw-diagnostico-remoto-vlad` 3.

**Estas reglas se predican de un producto, no de un repo.** «fw-gateway2lora cumple» no significa
nada: son cinco binarios distintos, con builds distintos, y cuatro de ellos con tests propios.
Cualquier afirmacion de cumplimiento nombra el producto —`fw-vlad/vlad25_vhf`— o no dice nada.

Corolario para medir: un `grep -r` sobre la raiz del repo **suma productos que no comparten nada**.
El promedio de cinco firmwares no describe a ninguno.

### Alcance por era

La fundacion se escribio el 21-Jul-2026 y crecio el 13-Ago. De los ~24 productos, **uno solo nacio
despues**. Leer estas reglas como si aplicaran retroactivamente a 811 commits de 2021 es lo que
hace que no se apliquen a ninguno.

| Situacion del producto | Que se le exige |
|---|---|
| **Nuevo** (primer commit posterior a esta fundacion) | Todo. Sin excepciones, y son baratas al empezar |
| **Vivo** (se le agregan funciones) | Lo nuevo cumple entero. Lo viejo se migra **solo si se toca** |
| **En mantenimiento** (solo arreglos) | No romperlo. Los flags de warning SI, porque encuentran defectos sin reescribir nada |
| **Congelado** | Nada. Y decirlo en su `CLAUDE.md`, para que no aparezca como incumplimiento en cada auditoria |

**La excepcion se declara, no se hereda.** Un producto que no puede cumplir una regla lo escribe en
su propio `CLAUDE.md` con el motivo —como `fw-vlad` hace con `-Og`—. Un incumplimiento sin declarar
es indistinguible de un olvido, y se vuelve a "descubrir" en cada revision.

**Evidencia de que el orden importa:** `fw-netreference`, el unico producto nacido despues de esta
fundacion, es el unico con **cero heap**, con el set completo de warnings y con `-Werror` desde el
primer commit. No costo una migracion: costo no tener que hacerla.

---

## Code UX (Embedded Specific)

### Directrices viejas, mecanismos nuevos

La disciplina de MISRA y de la era pre-C++11 sigue siendo correcta. Lo que cambio es que hoy
**casi toda esa disciplina se puede delegar al compilador** en vez de recordarla. Una regla que
vive en una tabla es una promesa; la misma regla como tipo, atributo o flag es un mecanismo.

Cada fila: la directriz vieja, el mecanismo que la hace cumplir, y **que vuelve imposible**.

| Directriz vieja | Mecanismo C++20 | Vuelve imposible | Uso (19-Ago-2026) |
|---|---|---|---|
| Revisar TODO retorno de la HAL | `[[nodiscard]]` | ignorar un status en silencio | **112 archivos** |
| `T* + size` en la firma | `std::span` | pasar el largo equivocado | **55** |
| `bool` + parametro de salida | `std::optional<T>` | leer el valor cuando fallo | **31** |
| Arrays C con tamano aparte | `static constexpr std::array` | perder el tamano | **36** |
| No Magic Numbers | `enum class` + `constexpr` | comparar dos dominios distintos | **43 / 117** |
| Invariantes en un comentario | `static_assert` | compilar con el invariante roto | **84** |
| Contrato en la documentacion | `concept` | instanciar con un tipo que no lo cumple | **15** |
| Guardar y restaurar estado de HW a mano | ScopeGuard RAII | salir por un `return` temprano sin restaurar | **10** |
| Strict Typing (tabla MISRA) | `-Wconversion -Wsign-conversion` | truncar sin aviso | recien en `vlad25` |
| Type punning por union o cast | **`std::bit_cast`** — `constexpr`, verifica tamano | reinterpretar tipos de tamano distinto | **0** — R4 ya se cumple con `memcpy`; `bit_cast` lo hace `constexpr` |
| `volatile` + `__disable_irq()` a mano | **`std::atomic<T>`** + `static_assert(std::atomic<T>::is_always_lock_free)` | asumir atomicidad que el nucleo no da | **1** |
| Tiempos como `uint32_t` de ms | **`std::chrono`** + literales (`100ms`) | sumar ms a segundos | **0** |
| Mascaras y bucles de bits a mano | **`<bit>`**: `popcount`, `countl_zero`, `has_single_bit`, `bit_width` | contar bits mal en un caso borde | **0** — 24 `1 << n` a mano |

**Golden rule:** si el compilador no puede verificar tu invariante en tiempo de compilacion, tu
diseno no es lo bastante expresivo.

**Lo que dice la ultima columna:** de 13 filas, **9 ya se aplican** y bien. Las 4 que faltan no son
deuda de disciplina: son las que C++20 agrego *despues* de que se escribieran estas reglas. Es
doctrina desactualizada, no incumplimiento.

**Y una leccion de como se lee esta tabla.** La fila de `bit_cast` decia primero «0 usos, y 11
`reinterpret_cast` en `Core/`», como si la regla se estuviera violando. Al leer los 11: **cuatro son
comentarios que explican que NO se uso el cast, citando R4**, y los otros siete son
`direccion -> puntero` para registros mapeados —`GPIO_TypeDef*`, `SPI_TypeDef*`, `DAC_TypeDef*`—,
que es el unico modo de llegar a un periferico desde una direccion numerica y que **ningun
mecanismo de C++20 reemplaza**. R4 se cumple al 100 %. Un conteo de `grep` respondio «cuantas
lineas coinciden», no «existe el defecto», que es justo lo que esta fundacion advierte en
`software-foundation.md -> Method Before Diagnosis`.

**Un patron que ya existe y conviene nombrar:** esos accesos viven en plantillas parametrizadas por
la direccion (`GpioPin.hpp`, `SpiBus.hpp`, `AgcDac.hpp`), con el `reinterpret_cast` aislado en un
solo accessor `static`. Eso **es** el acceso a registros por templates de Kormanyos, ya construido:
el cast peligroso queda en un lugar, verificable, y el resto del codigo habla de tipos. Cualquier
periferico nuevo se escribe asi.

`std::variant` **salio de este checklist**: estaba listado como reemplazo del `switch` y vive en
1 archivo. Con `-fno-exceptions`, un `std::visit` sobre un variant sin valor llama a
`std::terminate`, asi que la recomendacion era peor que lo que reemplazaba. Una regla que nadie
sigue y que empeora el caso de falla se borra, no se reitera.

---

## MISRA-C / Safety

| Rule | Description |
|------|-------------|
| No Dynamic Allocation | NEVER use `malloc()` or `free()`. Static or stack only. |
| Strict Typing | Use `<stdint.h>` types (`uint8_t`, `int16_t`). Plain `int` prohibited. |
| Unsigned Constants | Use `U` suffix: `100U`, `0x55U` |
| Const Correctness | `const` for read-only: `const uint8_t *data` |
| Volatile in ISRs | Variables shared with ISR MUST be `volatile` |
| Atomic Access | **Sin scheduler:** `__disable_irq(); ... __enable_irq();` para lecturas multi-byte en Cortex-M0. **Con scheduler: `taskENTER_CRITICAL()`** — ver «Con scheduler y sin scheduler» |
| Error Handling | Check EVERY HAL return: `if (status != HAL_OK)` |
| No Magic Numbers | All constants via `#define` or `enum` |

### Mandatory Toolchain Flags

**Generacion de codigo** — todos los targets:

```
-Os                                  # tamano (fw-vlad declara -Og como excepcion)
-fdata-sections -ffunction-sections  # una seccion por simbolo
-Wl,--gc-sections                    # el linker descarta lo no alcanzado
-fno-exceptions -fno-rtti            # C++ sin excepciones ni RTTI
```

**Warnings** — minimo obligatorio, y **solo sobre codigo propio**:

```
-Wall -Wextra -Wshadow
-Wconversion -Wsign-conversion     # la forma EJECUTABLE de "Strict Typing"
-Wdouble-promotion                 # float->double en M4F: emulacion silenciosa
-Wcast-align                       # en Cortex-M el acceso desalineado es un fault
-Wimplicit-fallthrough             # las maquinas de estado son switch
-Wnon-virtual-dtor -Woverloaded-virtual   # solo C++
```

Recortado de [cppbestpractices](https://github.com/cpp-best-practices/cppbestpractices) cap. 2
a lo que rinde en embebido.

**«Solo sobre codigo propio» es la parte que decide si sirve.** La HAL del fabricante y el
RTOS producen cientos de avisos que nadie va a arreglar, y aplicar los flags a todo el arbol
equivale a no aplicarlos. Con reglas por directorio en el Makefile son dos variables.
Medido en `fw-vlad/vlad25_vhf` (19-Ago-2026): **640 avisos** aplicandolos a todo el arbol,
**60 propios** aplicandolos solo a `Core/`.

`-Wold-style-cast` y `-Wuseless-cast` quedan **fuera**: 3156 avisos, de los cuales 2828 nacen
en headers de la HAL incluidos desde nuestros `.cpp`. Reevaluar el dia que los includes de
vendor pasen a `-isystem`.

`-Werror` **cuando el repo llega a cero**, no antes. Un `-Werror` sobre 60 avisos
preexistentes no se activa: se comenta, y entonces no hay flag ni regla.

> **Una regla de tipos que no esta en un flag no es una regla.** "Strict Typing" vivio como
> promesa en una tabla mientras el producto principal compilaba con `-Wall` a secas, sin
> `-Wconversion` y sin el `-Wdouble-promotion` que esta misma seccion declaraba obligatorio
> —en un M4F con FPU de simple precision, que es justo donde ese flag paga—.

---

## Memory Safety (ASan / UBSan / Valgrind)

> **Alcance: los tests de host.** ASan, UBSan y Valgrind no corren en el microcontrolador. Esta
> seccion gobierna el codigo compilado para host —los tests del Tier 2— donde SI hay heap y SI hay
> sanitizers. En el target manda la regla de arriba: **static o stack, nada mas**. Sin esta
> aclaracion, R3 se leia como permiso para usar `std::vector` en firmware y contradecia
> «No Dynamic Allocation» treinta lineas antes.

### Mandatory Rules

| Rule | Description | Alcance |
|------|-------------|---------|
| **R1** | Always compile with ASan in Debug: `-fsanitize=address,undefined -fno-omit-frame-pointer` | host |
| **R2** | Zero tolerance to memory leaks: `definitely lost` blocks deploy | host |

**Ergodicidad (tiempo secuencial ≠ paralelo):** pasar 10.000 pruebas en paralelo durante 5 min
con 0 fugas no prueba nada sobre 5 años en un solo dispositivo. Una fuga de 1 byte/hora es
ruina matemática en trayectoria secuencial aunque el promedio del ensemble sea 100 % verde.
Los tests del Tier 2 miden el *ensemble*; el firmware vive la *trayectoria*. Diseñar y revisar
optimizando para la ejecución infinita en un solo equipo, no para el promedio de la batería.
| **R3** | No raw `new`/`delete` — use `std::make_unique`, `std::vector`, RAII | **host solamente** |
| **R4** | No `reinterpret_cast`. En C++20, `std::bit_cast` para tipos del mismo tamano —es `constexpr` y el tamano lo verifica el compilador—; `std::memcpy` solo cuando difieren | ambos |
| **R5** | Use `.at()` instead of `operator[]` in debug for bounds checking | ambos |
| **R6** | Check division by zero before critical calculations | ambos |
| **R7** | Verify `int` → `double` conversions don't overflow | ambos |

### Finding Classification

| Severity | Tool | Action |
|----------|------|--------|
| Critical | ASan (overflow, use-after-free) | Block deploy |
| Critical | Valgrind (definitely lost) | Block deploy |
| High | UBSan (signed overflow, nullptr) | Fix immediately |
| Medium | LSan (memory leak) | Fix this sprint |
| Low | cppcheck (uninitialized var) | Document |
| Info | clang-tidy (performance) | Evaluate |

### Frequency

| When | What |
|------|------|
| Every PR commit | `cppcheck` + `clang-tidy` |
| Before merge to main | `ASan + UBSan` (full suite) |
| Before production deploy | `Valgrind` dry-run |
| Monthly | Full audit (ASan + UBSan + Valgrind + cppcheck) |

---

## Testing Tiers

### Tier 1: Compile-Time Assertions (Zero Cost) — MANDATORY

```cpp
static_assert(sizeof(MyPacket_t) == 74U, "Size changed");
static_assert(BUFFER_SIZE % 4U == 0U, "Must be 4-byte aligned for DMA");
static_assert(TABLE.size() > 0);
```

If it compiles, the condition holds. If it doesn't compile, you caught a bug before flashing.

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

### Regla de Oro: Validar el Protocolo Antes de Blindarlo

> No agregues patrones de resiliencia (circuit breakers, ISR guards, memory
> barriers, retry logic, crash dumps) a una interfaz de comunicación nueva
> hasta tener un smoke test end-to-end trivial (Tier 3, ~10 líneas) que
> confirme el protocolo correcto contra el hardware real.

**Por qué:** Blindar un driver que habla el protocolo equivocado no arregla
nada — solo hace más difícil ver que la causa raíz nunca fue el timing o
la robustez, sino una asunción de protocolo incorrecta.

**Checklist antes de escribir resiliencia sobre un driver nuevo:**
1. Existe un test mínimo (`AT\r\n` -> `OK\r\n`, o equivalente) que confirme
   el protocolo básico contra el hardware real, sin RTOS, sin DMA, sin bridges?
2. El pin de selección de modo (boot mode, config straps) coincide con el
   firmware/protocolo que el driver asume? Verificarlo contra la hoja de datos
   y el esquemático, no contra el SDK de referencia del fabricante.
3. Si el smoke test falla, la prioridad es corregir el protocolo/modo -- no
   anadir reintentos, timeouts mas largos, o guards de sincronizacion.

---

## Escribir un Parametro No Es Aplicarlo

En un periferico con registros, **persistir un valor y programarlo son dos operaciones
distintas**. Un setter que guarda en memoria y devuelve el valor guardado parece correcto
en todo camino de prueba que no mire el hardware.

### La asimetria que lo esconde

Un mismo defecto puede ser invisible en un sentido y fatal en el otro:

| Camino | Reprograma | Efecto del defecto |
|---|---|---|
| Transmision | en cada envio, porque tiene que fijar la frecuencia | **se auto-cura**: nadie lo nota |
| Recepcion | una sola vez, al entrar en modo escucha | **queda sordo hasta el reset** |

Por eso el sintoma aparece solo de un lado, y el lado que funciona hace creer que el
codigo es correcto.

### Checklist al tocar cualquier setter de periferico

| # | Pregunta |
|---|---|
| 1 | Despues de guardar, ¿algo **escribe el registro** del periferico? |
| 2 | La funcion que configura, ¿deja el periferico en el modo en que lo encontro? |
| 3 | El valor que se devuelve, ¿sale del **hardware** o de la variable recien escrita? |
| 4 | ¿Existe un camino que lo aplique **sin** reiniciar el equipo? |

**Regla:** si la respuesta a la 4 es no, decirlo en la respuesta al usuario y en la
documentacion. Un cambio que exige reset y no lo declara es peor que uno que falla, porque
el operador se va convencido de que quedo aplicado.

**Patron preferido:** que la funcion de configuracion restaure el modo con un `ScopeGuard`
RAII, para que el invariante no dependa de que cada llamador se acuerde. Si se difiere,
declararlo como deuda y decir por que.

---

## Estado Compartido con ISR: Diferir, No Bloquear

Nunca hacer E/S bloqueante dentro de un handler. Ademas de lo obvio:

- **Los timeouts de la HAL no pueden expirar.** Se miden con `HAL_GetTick()`, y si SysTick
  tiene prioridad mas baja que el handler, el tick esta **congelado** ahi dentro. Un bus
  trabado gira para siempre, y el watchdog tampoco salva si su refresh vive en el
  super-loop.
- **Reentrancia sobre el mismo handle.** Un flanco a mitad de transaccion la corrompe.
- **Sin debounce**, un contacto que rebota escribe en cada flanco.

**Patron:** la ISR lee y marca; el super-loop persiste.

```c
/* En la ISR */
valor_isr = leer_pin();
pendiente  = true;

/* En el super-loop */
if (pendiente) {
    pendiente = false;      /* limpiar ANTES de leer el valor */
    persistir(valor_isr);
}
```

**El orden importa:** limpiar la marca antes de leer el valor pierde, como maximo, una
escritura redundante. Al reves —leer y despues limpiar— se pierde el flanco que llegue en
el medio, que es una actualizacion real.

**Sobre `volatile`:** va en las variables que comparte la ISR, no en las que solo usa el
lazo. Si una variable se pasa a plantillas o a contenedores, marcarla `volatile` complica
la deduccion de tipos: conviene aislar el estado compartido en variables propias.

---

## Medir un Embebido sin Enganarse

> Todo lo de esta seccion salio de un dia en que el equipo estaba bien **seis veces** y el
> instrumento estaba mal. Cada vez el sintoma parecia del hardware.

### Un valor que solo se actualiza al acertar no puede probar una ausencia

El caso: se leyo el RSSI del receptor de LoRa y estaba clavado en su valor inicial. Se concluyo "el
receptor no corre". **Falso**: el codigo actualiza el RSSI unicamente cuando LLEGA un paquete, asi que
sin nadie transmitiendo se queda en el inicial aunque el receptor funcione perfecto. Medía el ultimo
paquete, no el canal.

**Regla:** antes de leer una ausencia como un fallo, buscar en el codigo **cuando se escribe** ese
valor. Si solo se escribe en el camino de exito, su valor inicial no significa nada.

### Muestrear el PC no distingue "bloqueado" de "no corre"

Se muestreo el PC 18 veces buscando el receptor y las 18 cayeron en el idle task de FreeRTOS. Eso es
compatible con las dos hipotesis: una tarea que espera con `osDelay` entre sondeos **esta bloqueada**, y
el CPU aparece en idle corra o no corra lo que se busca.

**Regla:** para saber si un camino se ejecuta, **contar los intentos**, no muestrear donde esta el CPU.
Un contador de intentos distingue; separar exitos de timeouts distingue mejor: "escucha y no hay nadie"
frente a "no escucha".

### Cada conexion del depurador puede resetear el objetivo

Un contador de arranques subio de 8 a 33 a 64 entre lecturas y parecia un bucle de reinicios. No lo era:
**cada sesion de OpenOCD resetea la placa al conectar**, asi que se contaban las propias mediciones.

**Regla:** para medir estabilidad, hacer las dos lecturas **dentro de una sola sesion** del depurador,
con la espera en el medio. Y para leer un flag de estado, resetear primero: sin reset se lee estado
viejo de la sesion anterior, que es lo que hizo confundir un `0` con una regresion que no existia.

### Cuando el instrumento no puede fallar, es peor que no tenerlo

Un volcado de HardFault decidia entre MSP y PSP con `tst lr, #4` desde una funcion C normal. El prologo
del compilador ya habia pisado `LR`, asi que elegia la pila equivocada — y **daba direcciones
plausibles**: reporto un PC que resulto ser la direccion de un handle de I2C, y mando a buscar durante
horas una corrupcion que no existia. Un watchpoint sobre esa direccion demostro que nadie la escribia.

**Regla:** un handler de excepcion que lea el marco tiene que ser `__attribute__((naked))` con el
trabajo en C aparte. Y ante un error de bus **imprecisó**, activar `DISDEFWBUF` (`ACTLR` bit 1) antes de
sacar conclusiones: sin eso el `PC` apilado no es el del culpable y `BFAR` no vale.

### El watchpoint es el instrumento que no opina

Para "quien escribe esta direccion" y "quien pide este reset", un watchpoint de datos responde sin
teoria. Dos veces en un dia convirtio una hipotesis en un hecho — y una de esas veces **refuto** la
hipotesis, que es lo valioso.

**Cuidado con los falsos positivos:** un watchpoint sobre `SCB->AIRCR` para cazar un
`NVIC_SystemReset()` dispara tambien en `HAL_NVIC_SetPriorityGrouping`, que escribe el mismo registro
legitimamente. Leer el VALOR escrito, no solo el hecho de que se escribio.

---

## Con Scheduler y Sin Scheduler

**1 de 7 repos usa RTOS**: `fw-vlad/vlad25_vhf` (5 tareas, 37 mutex, 28 `osDelay`, sin colas ni
flags de evento). Los otros ~23 productos son super-loop. Los patrones de este documento —maquina
de estados llamada en el lazo, timeout no bloqueante girando sobre `HAL_GetTick()`, «la ISR marca y
el super-loop persiste»— **son de super-loop**. Con scheduler cambian tres cosas:

| Sin scheduler | Con scheduler |
|---|---|
| `__disable_irq()` para acceso atomico | `taskENTER_CRITICAL()` — deshabilitar a mano pisa el anidamiento del kernel |
| `while (!flag)` girando sobre `HAL_GetTick()` | bloquear en un semaforo o cola: girar le roba CPU a tareas de menor prioridad |
| `self_test_run()` antes del super-loop | antes de arrancar el scheduler, no antes del lazo de una tarea |

### El watchdog tiene que poder observar a todas las tareas

En super-loop, si el lazo se traba el perro muerde. **Con scheduler eso deja de ser cierto:** la
tarea que refresca puede estar perfectamente viva mientras otra se muere de hambre, y el watchdog
sigue comiendo sobre un equipo medio muerto.

Es la misma clase que «State With No Age» en `software-foundation.md`: una confirmacion que sigue
siendo verdadera despues de dejar de significar algo.

**Regla:** el refresco se hace donde se pueda comprobar que **cada** tarea critica avanzo —un
contador por tarea que el refrescador lee y exige que haya cambiado—, no en la primera tarea que
tenga un lazo a mano.

**`vlad25_vhf` ya lo hace, y esta linea decia lo contrario hasta el 21-Ago-2026.** Verificado en el
codigo: `health_monitor_pet_watchdog()` llama a `health_monitor_all_healthy()`, que compara el ultimo
latido de cada una de las cinco tareas contra su plazo —el de BLE es distinto, a proposito— y con
`HEALTH_ENFORCE = true` **solo refresca el IWDG si ninguna llego tarde**. La unica excepcion es un
FOTA en curso, que inhibe el reinicio para no dejar firmware a medias.

Le queda un hueco, y conviene nombrarlo porque es la version fina de esta misma regla: una tarea que
**nunca** latio se saltea (`g_task_health_mask`), asi que el watchdog ve morir a una tarea pero no ve
a una que no arranco. Es deliberado —permite que el equipo funcione sin el modulo BLE— y aplica a
las cinco por igual. Cerrarlo pide `eTaskGetState()` sobre el handle, y eso se toca con banco
delante: es el camino que refresca el perro.

### Los hooks del RTOS matan con marca, no loguean

Un `vApplicationStackOverflowHook` que solo imprime deja correr un sistema con la pila pisada, y el
log se pierde con el proximo reset. `vlad25_vhf` lo hace bien y por eso queda escrito aca: loguea el
nombre de la tarea y llama `morir_con_marca(BOOT_MARK_STACK_OVF)`, asi la causa sobrevive al
reinicio. Lo mismo `vApplicationMallocFailedHook`.

### El heap del RTOS existe aunque la regla diga que no

`vlad25_vhf` declara `configTOTAL_HEAP_SIZE 32768` y `configSUPPORT_DYNAMIC_ALLOCATION 1`. Que en la
practica las tareas se creen estaticas (`stack_mem` / `cb_mem`) no borra los 32 KB reservados.

**Regla:** si el producto prohibe heap, `configSUPPORT_DYNAMIC_ALLOCATION` va en **0** y el
compilador lo hace cumplir. Dejarlo en 1 y confiar en la disciplina es una regla sin mecanismo.

---

## El `.ioc` No Es el Esquematico

**El `.ioc` describe como esta configurado el microcontrolador. El esquematico describe que hay en la
placa.** No son lo mismo, y cuando una senal no llega al micro **el `.ioc` muestra el residuo, no la
intencion**.

Cinco afirmaciones sobre hardware salieron mal en un dia, todas por leer el `.ioc`, el codigo o un
documento de plan en vez de el esquematico:

| Se afirmo | Era |
|---|---|
| "no existe el hardware para medir potencia de salida" | el detector esta en la placa; falta poblar un puente de 0 ohm marcado **DNP** |
| "ese pin es un control, no mide nada" | es la salida del detector; el `.ioc` lo declara salida **porque** la senal no llega |
| "falta el ADC de ese riel, es limitacion de hardware" | la medicion existe, por otro camino |

**Regla:** cualquier afirmacion de la forma "el hardware no puede medir X" se verifica **en el
esquematico** antes de decirla. Si el esquematico no esta disponible, la afirmacion se formula como
pregunta.

**Y buscar `DNP`.** Un componente sin poblar convierte una capacidad que existe en una que no llega, sin
dejar rastro en el codigo ni en el `.ioc`.

---

## Provenance del Binario

**Las tres reglas generales estan en `software-foundation.md` -> Build Provenance**, y valen para
cualquier artefacto desplegado. No se repiten aca a proposito: estaban escritas dos veces, en dos
idiomas, y dos copias de una regla derivan sin que nada lo reporte —el mismo defecto que esta
fundacion le senala a `@mirror-of`—.

Lo que agrega el firmware es **quien puede romperlas sin tocar codigo**: el generador del IDE.

**Caso:** un `.ioc` declaraba un prescaler de watchdog distinto al del codigo. Regenerar
bajaba el timeout de 24 s a 3 s, por debajo del retardo de arranque: ciclo de reset sin
salida. No fallaba ese dia; fallaba **la proxima vez que alguien abriera el `.ioc`** — que es la
forma en que un repo de firmware incumple la regla 2 sin un solo commit de codigo.

---

## Layered Architecture

### Mandatory Separation

```
┌─────────────────────────────────┐
│  Application Layer              │  State machines, business logic
│  (no direct HW access)         │  Never call HAL_* directly
├─────────────────────────────────┤
│  Service Layer                  │  Communication, logging, watchdog
│  (optional intermediaries)      │  Reusable across projects
├─────────────────────────────────┤
│  Driver Layer                   │  Init, read, write, control
│  (one per peripheral)           │  Exposes clean interface
├─────────────────────────────────┤
│  HAL Layer                      │  Vendor-provided (STM32 HAL)
│  (never modify)                 │  Access to registers
└─────────────────────────────────┘
```

### Rules
1. Application NEVER calls HAL_* directly — always through Driver
2. Drivers NEVER contain business logic — only hardware control
3. Services are stateless and testable on host
4. Dependencies point DOWN only (Application → Driver → HAL)

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

In release, `logger_->debug(...)` compiles to zero instructions. The string isn't even in flash.

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
    void run() { radio_->set_fsk_frequency(144000000); }
};
```

If the device doesn't satisfy the concept, it won't compile. Zero runtime overhead.

---

## Naming Conventions (C/C++)

### C

| Element | Convention | Example |
|---------|------------|---------|
| Functions | `snake_case` + module prefix | `my_module_init()` |
| Local variables | `snake_case` | `byte_count` |
| Static variables | `s_` prefix | `static MyDevice_t s_instance;` |
| Global variables | `g_` prefix | `volatile uint32_t g_tick_ms;` |
| Structs / Enums | `PascalCase` + `_t` | `UartRxRing_t` |
| Constants / Macros | `ALL_CAPS_SNAKE` | `SENSOR_TIMEOUT_MS` |

### C++

| Element | Convention | Example |
|---------|------------|---------|
| Classes | `PascalCase` | `CommandHandler` |
| Member variables | `m_` prefix | `m_huart` |
| Member methods | `snake_case` | `set_frequency()` |
| Enum class values | `UPPER_SNAKE` | `DeviceOperatingMode::RX_CONTINUOUS` |
