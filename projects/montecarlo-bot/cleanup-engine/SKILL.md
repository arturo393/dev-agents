---
name: Cleanup Engine
description: Dead code removal and repo sanitation. SKILL.md = dynamic inspection. agent.py = static checks.
---

# Cleanup Engine

1. **SKILL.md** — inspección dinámica de código muerto y dependencias
2. **`python3 agent.py discover`** — descubre estructura del repo, dead code, basura + corre cleanup
3. **Aprendizaje** — codificá nuevos patrones de dead code

## 1. Revisión Dinámica

```bash
cd /Users/arturo/development/lumina/monteCarlo/cpp_bot

# ¿Qué archivos compila trading_bot?
grep -A50 'set(SOURCES' CMakeLists.txt | grep 'src/'

# ¿Cuáles se usan realmente en main.cpp?
for src in $(grep -A50 'set(SOURCES' CMakeLists.txt | grep 'src/' | sed 's/.*\///;s/\.cpp//'); do
  refs=$(grep -rc "$src" src/main.cpp)
  echo "$src: $refs refs in main"
done

# Verificar cadena de señales
grep -n 'analyze\|get_score\|should_enter\|signal' src/main.cpp | head -15
```

## 2. Descubrimiento

```bash
python3 agent.py discover
```

## 3. Cleanup Estático

```bash
python3 agent.py cleanup
```

## 4. Aprendizaje

Si descubrís un nuevo tipo de dead code o basura, codificalo:
```bash
echo '# $(date): nuevo dead code pattern' >> scripts/run-cleanup.sh
```
