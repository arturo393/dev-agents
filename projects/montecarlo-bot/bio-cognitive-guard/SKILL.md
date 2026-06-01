---
name: Bio-Cognitive Guard
description: Cognitive load, alert fatigue, circadian resilience. SKILL.md = dynamic review. agent.py = static audits.
---

# Bio-Cognitive Guard

1. **SKILL.md** — revisión de código fuente para carga cognitiva y fatiga
2. **`python3 agent.py discover`** — descubre sistema de archivos, systemd, errores + corre audits
3. **Aprendizaje** — codificá nuevos anti-patrones

## 1. Revisión Dinámica

```bash
cd /Users/arturo/development/lumina/monteCarlo/cpp_bot
# Funciones largas (>100 líneas)
grep -rn '^{' src/main.cpp | wc -l

# Anidamiento profundo
grep -rn 'for\|while\|if\|switch' src/main.cpp | grep '.*{.*{' | head -10

# Nombres de variables de 1 letra
grep -rn '\<[a-z]\s*[\[;=)]' src/*.cpp | grep -v '//\|i\|j\|k\|x\|y\|z\s*[\[+;=)]' | head -10

# Revisión de systemd timers en servidor
ssh arturo@100.74.53.2 "systemctl list-timers --all --no-legend | head -20"
```

## 2. Descubrimiento

```bash
python3 agent.py discover
```

## 3. Audits Estáticos

```bash
python3 agent.py cognitive_load
python3 agent.py alert_fatigue
```

## 4. Aprendizaje

Si encontrás un nuevo anti-patrón cognitivo, codificalo:
```bash
echo '# $(date): nuevo anti-patron' >> /Users/arturo/development/lumina/monteCarlo/tools/skills/bio_cognitive_guard/scripts/audit_cognitive_load.sh
```
