---
name: Runtime Sanitizer
description: Memory safety and UB profiling. SKILL.md = dynamic review. agent.py = static sanitizer checks.
---

# Runtime Sanitizer

1. **SKILL.md** — revisión dinámica de memory safety y undefined behavior
2. **`python3 agent.py discover`** — descubre tools, compilador, flags + corre sanitizer checks
3. **Aprendizaje** — codificá nuevos UB patterns

## 1. Revisión Dinámica

```bash
cd /Users/arturo/development/lumina/monteCarlo/cpp_bot

# Herramientas disponibles
ssh arturo@100.74.53.2 "which valgrind cppcheck clang-tidy 2>&1"
ssh arturo@100.74.53.2 "g++ --version | head -1; cmake --version | head -1"

# Flags de compilación actuales
grep 'CMAKE_CXX_FLAGS' CMakeLists.txt

# UB patterns
echo '=== new sin delete ==='
grep -rn 'new ' src/*.cpp | grep -v '//\|delete' | head -10

echo '=== Variables sin inicializar ==='
grep -rn 'int \w\+;\|double \w\+;\|bool \w\+;' src/*.cpp | grep -v '= ' | grep -v '//' | head -5

echo '=== Shared globals sin mutex ==='
grep -rn 'static.*double\|static.*int\|static.*bool' src/main.cpp | grep -v 'const\|//'

echo '=== C-style casts ==='
grep -rn '(int)\|(float)\|(double)' src/*.cpp | head -5
```

## 2. Descubrimiento

```bash
python3 agent.py discover
```

## 3. Sanitizer Estático

```bash
python3 agent.py sanitizer
```

## 4. Aprendizaje

Si descubrís un nuevo patrón de UB, memory leak, o data race, codificalo:
```bash
echo '# $(date): nuevo UB pattern' >> scripts/run-sanitizer.sh
```
