---
description: "Compile a markdown doc to HTML/PDF/DOCX with UQOMM brand style using compile.py. Use when: generating branded documentation, creating HTML from markdown, compiling docs, uqomm-professional style, compile.py"
name: "Compilar Doc UQOMM"
argument-hint: "Ruta al archivo .md a compilar (o deja vacío para el archivo activo)"
agent: "agent"
tools: ["run_in_terminal", "read_file", "file_search"]
---

# Compilar documentacion con estilo UQOMM

## Instrucciones

Compila el archivo Markdown indicado (o el archivo activo en el editor) a HTML usando `compile.py` con estilo `uqomm-professional`.

### Paso 1 — Identificar el archivo fuente

Si el usuario proporcionó una ruta como argumento, usarla directamente.
Si no, usar el archivo activo en el editor (`$input`).
Si tampoco hay archivo activo, preguntar.

### Paso 2 — Verificar que compile.py existe

El compilador está en:
```
C:\Users\artur\development\shared\sw-documentation\compile.py
```

Si no existe, notificar y detenerse.

### Paso 3 — Revisar el documento antes de compilar

Busca y corrige problemas comunes:
- Headers duplicados consecutivos (e.g., `### Foo\n\n### Foo`)
- Tablas con columnas desalineadas evidentes
- YAML frontmatter sin cerrar (si lo tiene el doc)

### Paso 4 — Compilar

Ejecuta:
```powershell
cd "C:\Users\artur\development\shared\sw-documentation"
python compile.py --file "<ruta-absoluta-al-archivo.md>" --format html --html-style uqomm-professional
```

Para generar también PDF:
```powershell
python compile.py --file "<ruta>" --format html pdf --html-style uqomm-professional
```

Para generar también DOCX:
```powershell
python compile.py --file "<ruta>" --format html docx --html-style uqomm-professional
```

### Paso 5 — Confirmar resultado

Verifica que el archivo `.html` fue generado en el mismo directorio que el `.md` fuente.
Informa la ruta de salida al usuario.

## Notas de estilo disponibles

| Estilo              | Descripcion                                          |
|---------------------|------------------------------------------------------|
| `uqomm-professional`| Diseño moderno, Oswald/Roboto, naranja corporativo   |
| `copilot`           | Estilo por defecto, limpio                           |
| `copilot_scroll`    | Con TOC lateral scrollable                           |
| `copilot_sub`       | Con subsecciones destacadas                          |
| `manual`            | Estilo técnico para manuales                         |
