---
name: Cleanup Guidelines
description: Políticas para identificación y eliminación de código muerto, basura y deuda técnica.
---

# 🧹 Cleanup Guidelines — Dead Code & Technical Debt

## 🧠 Filosofía

> "El código que no se ejecuta no es un activo, es un pasivo."

Cada archivo muerto en el binario:
- Aumenta el tiempo de compilación
- Incrementa el tamaño del binario
- Confunde a nuevos desarrolladores
- Oculta bugs reales (¿ese error es de código vivo o muerto?)

## 📜 Reglas de Dead Code

### D1: Código muerto = código que no afecta el resultado

Un componente es "vivo" solo si:
1. Su ejecución cambia el estado del sistema (posición, DB, orden, log)
2. O su ejecución cambia el flujo de control hacia un componente vivo

**No cuenta como vivo**:
- Instanciar un objeto y no llamar a sus métodos
- Compilar un archivo que solo se usa en backtesting
- Tener headers que nadie incluye en producción

### D2: Si existe en producción pero no se usa → se elimina

No importa si "podría servir algún día". Eso se llama **especulación**. Si se necesita, se recupera de git.

### D3: Backtest != Producción

El `backtest_simulator` es un binario separado y puede tener sus propias dependencias. No hay problema en que incluya estrategias que producción no necesita. Pero NO deben compartir el mismo target de compilación.

### D4: Backup antes de modificar build system

Siempre hacer backup de `CMakeLists.txt` antes de editar:
```bash
cp CMakeLists.txt CMakeLists.txt.bak.$(date +%Y%m%d)
```

## 📊 Priorización

| Prioridad | Categoría | Ejemplo | Cuándo hacerlo |
|-----------|-----------|---------|----------------|
| P0 | Binario muerto | Archivos compilados en trading_bot que no se usan | Inmediato |
| P1 | Código comentado | Bloques `/* ... */` enormes | En cada refactor |
| P2 | Dependencias no usadas | Librerías en CMakeLists.txt que nadie linkea | Sprint planning |
| P3 | Backups viejos | `*.bak` > 30 días | Limpieza mensual |
| P4 | Logs rotacionales | `*.log` > 7 días | Automatizar con logrotate |

## 🧹 Checklist de Limpieza Mensual

- [ ] Ejecutar `audit_dead_code.sh`
- [ ] Revisar si hay nuevos archivos muertos desde la última auditoría
- [ ] Eliminar `.DS_Store` y `__pycache__`
- [ ] Revisar `*.bak` y eliminar los que tengan >30 días
- [ ] Verificar que `CMakeLists.txt` no tenga dependencias sin usar
- [ ] Verificar que `tools/` no tenga scripts huérfanos (sin `#!` ni referencias)
- [ ] Correr `master_integrator/scripts/audit_all.sh`

## ⚠️ Anti-patrones

- ❌ **"Lo dejo por si acaso"** — El código muerto no es seguro, es ruido
- ❌ **"Lo borro del file system pero no del build"** — Peor, ahora da error de linkeo
- ❌ **"El backtest lo necesita"** → No lo borres, solo sácalo del target de producción
- ❌ **"Está comentado pero lo voy a necesitar"** → Git está para eso
