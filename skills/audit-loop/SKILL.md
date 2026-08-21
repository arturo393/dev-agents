---
name: audit-loop
description: Retro-inspección de un repo hasta que deje de rendir: cómo enumerar candidatos por una propiedad en vez de por intuición, qué instrumento usar en cada ronda y qué NO puede ver cada uno. Usar cuando el usuario pida auditar, sanear, buscar código muerto, inconsistencias, redundancias, "revisá todo", "hasta no encontrar nada", o una retrospectiva del estado de un repo.
---

Auditás un repo por **rondas**, y cada ronda usa un instrumento distinto. No buscás defectos
leyendo: enumerás candidatos por una **propiedad mecánica** y después los leés.

## La regla que hace la diferencia

**Un conteo de `grep` no es un hallazgo.** Responde «cuántas líneas coinciden», no «existe el
defecto». Un comentario que describe un bug coincide con el mismo patrón que el bug. **Siempre
imprimí las coincidencias y leelas** antes de llamar a algo defecto.

Evidencia de una auditoría de diez rondas (fw-vlad, 21-Ago-2026): de 79 referencias «a archivos
inexistentes», 3 eran reales — el resto eran de otros repos o citas históricas legítimas. De 30
referencias `archivo:línea` «inválidas», **todas** eran válidas: el script buscaba en el
directorio equivocado.

## Todo instrumento tiene un punto ciego, y no lo ve

Es la trampa central. Un chequeo que da cero puede significar «no hay defectos» o «no sabe
verlos», y las dos cosas se leen igual. Tres casos reales de la misma auditoría, los tres del
auditor y no del repo:

| El chequeo | Dio | Lo que no podía ver |
|---|---|---|
| citas `archivo:línea` validando el **rango** | «21, 0 inválidas» | 5 apuntaban a otra cosa dentro del archivo |
| rutas entre comillas invertidas en docs | limpio | el único enlace roto estaba en sintaxis `[](...)` |
| existencia de archivos citados | 30 «inválidas» | vivían en el repo legacy de al lado |

**Antes de creerle a un cero, preguntá si el chequeo puede fallar.** Y si dejás un mecanismo
armado, rompelo a propósito una vez: si no falla, no protege — decora.

## Instrumentos, y qué no ve cada uno

| # | La pregunta mecánica | Encuentra | No ve |
|---|---|---|---|
| 1 | ¿qué archivos hay versionados, y con qué flags compilan? | build fuera de git, flags que la doctrina exige y no están | nada del contenido |
| 2 | ¿qué archivos citan los documentos que no existen? | punteros muertos, docs que mandan a la nada | otros repos: hay que enumerarlos aparte |
| 3 | ¿qué símbolos descartó el linker de nuestros objetos? | código muerto real, funciones sin llamador | **no distingue** duplicados de plantilla, que son la mayoría |
| 4 | ¿qué números declaran los documentos, y cuánto miden hoy? | presupuestos vencidos, conteos duplicados y divergidos | números que nadie escribió |
| 5 | ¿qué nombres de una tabla de renombres siguen vivos? | migraciones a medias | los que son del legacy y **deben** quedarse |
| 6 | ¿a qué apunta cada cita `archivo:línea`? | citas corridas, incluidas las que rompió tu propia edición | si solo validás el rango, nada |
| 7 | ¿qué afirma ser «el único» y de verdad lo es? | invariantes roto por un segundo camino | las que no son comprobables por `grep` |
| 8 | ¿qué dice la doctrina sobre ESTE producto, y sigue siendo cierto? | fundaciones que citan como contraejemplo algo ya arreglado | lo que la doctrina no nombra |
| 9 | ¿los scripts de operación miran lo que afirman? | grabar sin verificar, sin gate de identidad, con seriales caducos | lo que no es un script |
| 10 | ¿qué contesta el hardware? | **todo lo demás es escritorio** | nada: es el único que responde «funciona» |

Sin usar todavía, para quien siga: el `.map` por tamaño de símbolo (quién ocupa flash y no
debería), los `static_assert` contra lo que de verdad afirman, y el cruce de opcodes contra los
repos consumidores — para eso está `drift-radar`.

## El protocolo, y su límite honesto

Máximo 10 rondas. Se para cuando una ronda da cero hallazgos, o cuando dos rondas seguidas no
producen ningún arreglo. Informe final: rondas, hallazgos por ronda, y lo bloqueado.

**No converge por agotamiento.** En esa auditoría las diez rondas encontraron algo, y ninguna
encontró lo mismo que la anterior: rindieron porque cambió el instrumento, no porque quedara
superficie sin barrer. «Hasta no encontrar nada» termina cuando se te acaban las formas de
preguntar, y siempre queda una más. Decí eso en el informe en vez de declarar convergencia.

## Qué hacer con cada hallazgo

| Si el chequeo es… | va a… |
|---|---|
| binario y determinista | un **script que se ejecute ya**, no uno nuevo que nadie corre. En `fw-vlad` son los invariantes de `patches/verificar.sh` |
| un número que puede empeorar | un **trinquete** (`<=`): bajar permitido, subir falla. Un tope fijo se queda viejo del lado peligroso |
| interpretable | acá, en esta skill: el valor es el criterio de lectura, no el comando |
| doctrina transversal | `.opencode/instructions/*-foundation.md` |

Y el orden importa: **los invariantes primero**. Una skill sin ellos es otra promesa.

## Dónde suelen estar los defectos

En el borde entre el código y su descripción. En diez rondas, los seis hallazgos con consecuencia
fueron: el build fuera de git, un bootloader que brickeaba descrito como el actual, un flasheo sin
gate de identidad, dos literales del reloj sin atar, un watchdog documentado al revés, y citas
corridas. **Cada vez que un mecanismo mejoró, el comentario que lo describía quedó atrás** — y esa
superficie es donde la próxima persona toma decisiones.
